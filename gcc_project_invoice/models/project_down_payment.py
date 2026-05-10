# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectDownPayment(models.Model):
    _name = "project.down.payment"
    _description = "Project Down Payment"
    _order = "date_received desc, id desc"
    _rec_name = "display_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    _sql_constraints = [
        ('amount_positive', 'CHECK (amount > 0)', 'Down payment amount must be positive.'),
        ('date_received_not_future', 'CHECK (date_received <= CURRENT_DATE)', 'Date received cannot be in the future.'),
    ]

    # --- Basic Information ---
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        ondelete="cascade",
        index=True,
        help="Project for which this down payment is received",
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        tracking=True,
        help="Down payment amount received",
    )
    date_received = fields.Date(
        string="Date Received",
        required=True,
        default=fields.Date.context_today,
        help="Date when the down payment was received",
    )
    payment_reference = fields.Char(
        string="Payment Reference",
        help="Bank transfer reference, check number, or other payment identifier",
    )
    description = fields.Text(
        string="Description",
        help="Additional notes about this down payment",
    )

    # --- Accounting Integration ---
    account_move_id = fields.Many2one(
        "account.move",
        string="Related Journal Entry",
        help="Journal entry created for this down payment",
        readonly=True,
    )
    account_payment_id = fields.Many2one(
        "account.payment",
        string="Related Payment",
        help="Payment record if created through payment module",
        readonly=True,
    )

    # --- State Management ---
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True, tracking=True,
        help="Status of the down payment")

    # --- Reconciliation Tracking ---
    reconciled_amount = fields.Monetary(
        string="Reconciled Amount",
        currency_field="currency_id",
        compute="_compute_reconciled_amount",
        store=True,
        help="Amount already used in invoice deductions",
    )
    remaining_amount = fields.Monetary(
        string="Remaining Amount",
        currency_field="currency_id",
        compute="_compute_reconciled_amount",
        store=True,
        help="Amount still available for invoice deductions",
    )
    invoice_reconciliation_ids = fields.One2many(
        "project.down.payment.reconciliation",
        "down_payment_id",
        string="Invoice Reconciliations",
        help="Invoices that have used this down payment",
    )

    # --- Related Fields ---
    partner_id = fields.Many2one(
        related="project_id.partner_id",
        string="Customer",
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        related="project_id.company_id",
        string="Company",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        related="project_id.currency_id",
        readonly=True,
        store=True,
    )

    # --- Display Field ---
    display_name = fields.Char(
        string="Display Name",
        compute="_compute_display_name",
        store=True,
    )

    @api.depends("project_id.name", "amount", "date_received", "payment_reference")
    def _compute_display_name(self):
        """Compute display name for the record."""
        for record in self:
            project_name = record.project_id.name or "Unknown Project"
            amount_str = f"{record.amount:,.2f}" if record.amount else "0.00"
            currency_symbol = record.currency_id.symbol or ""
            
            if record.payment_reference:
                record.display_name = f"{project_name} - {currency_symbol}{amount_str} ({record.payment_reference})"
            else:
                record.display_name = f"{project_name} - {currency_symbol}{amount_str}"

    @api.model
    def _rec_names_search(self, name='', args=None, operator='ilike', limit=100, order=None):
        """Enable search by project name and payment reference."""
        if args is None:
            args = []
        
        if name:
            domain = ['|', '|',
                      ('project_id.name', operator, name),
                      ('payment_reference', operator, name),
                      ('display_name', operator, name)]
            return self._search(domain + args, limit=limit, order=order)
        
        return super()._rec_names_search(name=name, args=args, operator=operator, limit=limit, order=order)

    @api.depends("invoice_reconciliation_ids.amount")
    def _compute_reconciled_amount(self):
        """Compute reconciled and remaining amounts."""
        for record in self:
            reconciled = sum(record.invoice_reconciliation_ids.mapped('amount'))
            record.reconciled_amount = reconciled
            record.remaining_amount = record.amount - reconciled

    @api.constrains("amount")
    def _check_amount_positive(self):
        """Validate amount is positive."""
        for record in self:
            if record.amount <= 0:
                raise ValidationError(_("Down payment amount must be positive."))

    @api.constrains("project_id", "amount")
    def _check_project_limits(self):
        """Validate down payment doesn't exceed project expectations."""
        for record in self:
            if not record.project_id.has_down_payment:
                continue
                
            project = record.project_id
            expected_amount = project.down_payment_amount
            
            if expected_amount > 0:
                # Calculate total down payments including this one
                other_payments = project.down_payment_ids.filtered(
                    lambda p: p.id != record.id and p.state in ('confirmed', 'reconciled')
                )
                total_with_current = sum(other_payments.mapped('amount')) + record.amount
                
                # Allow some tolerance (5%) over expected amount
                tolerance = expected_amount * 0.05
                if total_with_current > (expected_amount + tolerance):
                    raise ValidationError(_(
                        "Total down payments (%(total)s) exceed expected amount (%(expected)s) by more than 5%%. "
                        "Expected: %(expected)s, Current total: %(total)s"
                    ) % {
                        'total': f"{total_with_current:,.2f}",
                        'expected': f"{expected_amount:,.2f}"
                    })

    def action_confirm(self):
        """Confirm the down payment."""
        for record in self:
            if record.state != 'draft':
                continue
            record.state = 'confirmed'

    def action_cancel(self):
        """Cancel the down payment."""
        for record in self:
            if record.reconciled_amount > 0:
                raise ValidationError(_(
                    "Cannot cancel down payment that has been reconciled with invoices. "
                    "Please first remove the reconciliation from related invoices."
                ))
            record.state = 'cancelled'

    def action_set_to_draft(self):
        """Set back to draft."""
        for record in self:
            if record.reconciled_amount > 0:
                raise ValidationError(_(
                    "Cannot reset to draft a down payment that has been reconciled. "
                    "Please first remove the reconciliation from related invoices."
                ))
            record.state = 'draft'

    def action_create_payment_entry(self):
        """Create journal entry for the down payment."""
        self.ensure_one()
        
        if self.account_move_id:
            return self.account_move_id.action_show_details()
            
        # This could be extended to automatically create journal entries
        # For now, return action to create payment
        return {
            'name': _('Create Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'context': {
                'default_amount': self.amount,
                'default_partner_id': self.partner_id.id,
                'default_payment_type': 'inbound',
                'default_partner_type': 'customer',
                'default_ref': f"Down payment - {self.project_id.name}",
            },
            'target': 'new',
        }

    def allocate_to_invoice(self, invoice, amount):
        """
        Allocate part of this down payment to an invoice.
        
        :param invoice: account.move record
        :param amount: Amount to allocate
        :return: Created reconciliation record
        """
        self.ensure_one()
        
        if self.state != 'confirmed':
            raise ValidationError(_("Can only allocate confirmed down payments."))
            
        if amount <= 0:
            raise ValidationError(_("Allocation amount must be positive."))
            
        if amount > self.remaining_amount:
            raise ValidationError(_(
                "Cannot allocate %(amount)s, only %(remaining)s available."
            ) % {'amount': amount, 'remaining': self.remaining_amount})

        # Create reconciliation record
        reconciliation = self.env['project.down.payment.reconciliation'].create({
            'down_payment_id': self.id,
            'invoice_id': invoice.id,
            'amount': amount,
        })

        # Update down payment state if fully reconciled
        if self.remaining_amount <= 0.01:  # Allow small rounding differences
            self.state = 'reconciled'
            
        return reconciliation

    @api.model
    def get_available_for_project(self, project_id):
        """
        Get available down payment balance for a project.
        
        :param project_id: ID of the project
        :return: Total available amount
        """
        payments = self.search([
            ('project_id', '=', project_id),
            ('state', 'in', ['confirmed', 'reconciled']),
        ])
        
        return sum(payments.mapped('remaining_amount'))


class ProjectDownPaymentReconciliation(models.Model):
    _name = "project.down.payment.reconciliation"
    _description = "Down Payment to Invoice Reconciliation"
    _order = "create_date desc"

    # --- Basic Fields ---
    down_payment_id = fields.Many2one(
        "project.down.payment",
        string="Down Payment",
        required=True,
        ondelete="cascade",
    )
    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
        required=True,
        ondelete="cascade",
        domain=[('move_type', '=', 'out_invoice')],
    )
    amount = fields.Monetary(
        string="Amount",
        currency_field="currency_id",
        required=True,
        help="Amount of down payment allocated to this invoice",
    )
    date_reconciled = fields.Datetime(
        string="Date Reconciled",
        default=fields.Datetime.now,
        required=True,
    )

    # --- Related Fields ---
    project_id = fields.Many2one(
        related="down_payment_id.project_id",
        string="Project",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        related="down_payment_id.currency_id",
        readonly=True,
        store=True,
    )

    @api.constrains("amount")
    def _check_amount_positive(self):
        """Validate amount is positive."""
        for record in self:
            if record.amount <= 0:
                raise ValidationError(_("Reconciliation amount must be positive."))

    @api.constrains("down_payment_id", "amount")
    def _check_available_amount(self):
        """Validate enough amount is available in down payment."""
        for record in self:
            down_payment = record.down_payment_id
            other_reconciliations = down_payment.invoice_reconciliation_ids.filtered(
                lambda r: r.id != record.id
            )
            total_allocated = sum(other_reconciliations.mapped('amount')) + record.amount
            
            if total_allocated > down_payment.amount:
                raise ValidationError(_(
                    "Cannot allocate %(amount)s. Down payment total is %(total)s, "
                    "already allocated %(allocated)s."
                ) % {
                    'amount': record.amount,
                    'total': down_payment.amount,
                    'allocated': total_allocated - record.amount,
                })

    @api.constrains("invoice_id", "project_id")
    def _check_project_consistency(self):
        """Validate invoice belongs to same project."""
        for record in self:
            if record.invoice_id.project_id != record.project_id:
                raise ValidationError(_(
                    "Invoice project (%(invoice_project)s) must match down payment project (%(dp_project)s)."
                ) % {
                    'invoice_project': record.invoice_id.project_id.name or 'None',
                    'dp_project': record.project_id.name,
                })