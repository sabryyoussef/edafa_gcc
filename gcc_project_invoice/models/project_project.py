# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    # --- Project Financial Configuration ---
    project_value = fields.Monetary(
        string="Project Total Value",
        currency_field="currency_id",
        help="Total contracted value for this project",
    )
    has_down_payment = fields.Boolean(
        string="Enable Down Payment",
        default=False,
        help="Check this to enable down payment management for this project",
    )
    down_payment_percent = fields.Float(
        string="Down Payment %",
        default=0.0,
        help="Percentage of project value expected as down payment",
    )
    
    # --- Computed Financial Fields ---
    down_payment_amount = fields.Monetary(
        string="Expected Down Payment",
        currency_field="currency_id",
        compute="_compute_down_payment_amount",
        store=True,
        help="Calculated expected down payment amount based on percentage",
    )
    total_down_payments_received = fields.Monetary(
        string="Total Down Payments Received", 
        currency_field="currency_id",
        compute="_compute_down_payment_totals",
        store=True,
        help="Sum of all confirmed down payments received",
    )
    available_down_payment_balance = fields.Monetary(
        string="Available Down Payment Balance",
        currency_field="currency_id", 
        compute="_compute_down_payment_totals",
        store=True,
        help="Down payment balance available for invoice deduction",
    )
    total_invoiced_amount = fields.Monetary(
        string="Total Invoiced Amount",
        currency_field="currency_id",
        compute="_compute_project_totals", 
        store=True,
        help="Sum of all posted invoices for this project",
    )
    total_advance_deducted = fields.Monetary(
        string="Total Advance Deducted",
        currency_field="currency_id",
        compute="_compute_project_totals",
        store=True,
        help="Sum of advance payment deductions from invoices",
    )
    remaining_project_balance = fields.Monetary(
        string="Remaining Project Balance",
        currency_field="currency_id",
        compute="_compute_project_totals",
        store=True,
        help="Project value minus invoiced amount",
    )

    # --- Relationship Fields ---
    down_payment_ids = fields.One2many(
        "project.down.payment",
        "project_id", 
        string="Down Payments",
        help="Down payments received for this project",
    )
    invoice_ids = fields.One2many(
        "account.move",
        "project_id",
        string="Project Invoices",
        domain=[('move_type', '=', 'out_invoice')],
        help="Customer invoices related to this project",
    )

    # --- Count Fields for Smart Buttons ---
    down_payment_count = fields.Integer(
        string="Down Payment Count",
        compute="_compute_counts",
    )
    invoice_count = fields.Integer(
        string="Invoice Count", 
        compute="_compute_counts",
    )

    # --- Currency ---
    currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
        store=True,
    )

    @api.depends("project_value", "down_payment_percent")
    def _compute_down_payment_amount(self):
        """Calculate expected down payment amount based on percentage."""
        for project in self:
            if project.has_down_payment and project.project_value and project.down_payment_percent:
                project.down_payment_amount = project.currency_id.round(
                    project.project_value * (project.down_payment_percent / 100.0)
                )
            else:
                project.down_payment_amount = 0.0

    @api.depends("down_payment_ids.amount", "down_payment_ids.state", "total_advance_deducted")
    def _compute_down_payment_totals(self):
        """Calculate down payment totals and available balance."""
        for project in self:
            # Sum confirmed down payments (not cancelled)
            confirmed_payments = project.down_payment_ids.filtered(
                lambda p: p.state in ('confirmed', 'reconciled')
            )
            total_received = sum(confirmed_payments.mapped('amount'))
            
            # Available balance = received - already deducted from invoices
            available_balance = total_received - (project.total_advance_deducted or 0.0)
            
            project.total_down_payments_received = total_received
            project.available_down_payment_balance = max(0.0, available_balance)

    @api.depends("invoice_ids.amount_total_signed", "invoice_ids.state", "invoice_ids.advance_payment_deduction")
    def _compute_project_totals(self):
        """Calculate project financial totals from posted invoices."""
        for project in self:
            posted_invoices = project.invoice_ids.filtered(lambda inv: inv.state == 'posted')
            
            # Sum invoice totals (use amount_total_signed for company currency)
            total_invoiced = sum(posted_invoices.mapped('amount_total_signed'))
            
            # Sum advance payment deductions
            total_advance_deducted = sum(posted_invoices.mapped('advance_payment_deduction'))
            
            # Calculate remaining balance
            remaining = (project.project_value or 0.0) - abs(total_invoiced)
            
            project.total_invoiced_amount = abs(total_invoiced)
            project.total_advance_deducted = total_advance_deducted
            project.remaining_project_balance = remaining

    @api.depends("down_payment_ids", "invoice_ids")
    def _compute_counts(self):
        """Compute counts for smart buttons."""
        for project in self:
            project.down_payment_count = len(project.down_payment_ids)
            project.invoice_count = len(project.invoice_ids.filtered(lambda inv: inv.move_type == 'out_invoice'))

    @api.constrains("down_payment_percent")
    def _check_down_payment_percent(self):
        """Validate down payment percentage is reasonable."""
        for project in self:
            if project.has_down_payment and project.down_payment_percent:
                if project.down_payment_percent < 0:
                    raise ValidationError(_("Down payment percentage cannot be negative."))
                if project.down_payment_percent > 100:
                    raise ValidationError(_("Down payment percentage cannot exceed 100%."))

    @api.constrains("project_value")
    def _check_project_value(self):
        """Validate project value is positive."""
        for project in self:
            if project.project_value and project.project_value < 0:
                raise ValidationError(_("Project value must be positive."))

    @api.onchange("has_down_payment")
    def _onchange_has_down_payment(self):
        """Reset down payment fields when disabled."""
        if not self.has_down_payment:
            self.down_payment_percent = 0.0

    def action_view_down_payments(self):
        """Smart button action to view project down payments."""
        self.ensure_one()
        action = self.env.ref('gcc_project_invoice.action_project_down_payment').read()[0]
        action['domain'] = [('project_id', '=', self.id)]
        action['context'] = {
            'default_project_id': self.id,
            'search_default_project_id': self.id,
        }
        return action

    def action_view_invoices(self):
        """Smart button action to view project invoices."""
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [('project_id', '=', self.id), ('move_type', '=', 'out_invoice')]
        action['context'] = {
            'default_project_id': self.id,
            'default_move_type': 'out_invoice',
            'search_default_project_id': self.id,
        }
        return action

    def action_create_invoice(self):
        """Smart button action to create new invoice for project."""
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['views'] = [(False, 'form')]
        action['context'] = {
            'default_project_id': self.id,
            'default_move_type': 'out_invoice',
            'default_partner_id': self.partner_id.id if self.partner_id else False,
        }
        return action

    def action_add_down_payment(self):
        """Smart button action to add down payment."""
        self.ensure_one()
        return {
            'name': _('Add Down Payment'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.down.payment',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'context': {
                'default_project_id': self.id,
            },
            'target': 'new',
        }