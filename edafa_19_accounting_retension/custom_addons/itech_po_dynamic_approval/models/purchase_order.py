from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_team_id = fields.Many2one(comodel_name='purchase.order.teams', string="Purchase Team" , default=lambda self: self._default_purchase_team())
    # default=lambda self: self.env['purchase.order.teams'].search([('short_code', '=', 'DefaultPO')], limit=1))
    purchase_approve_line = fields.One2many(comodel_name="purchase.approve.route", inverse_name="purchase_id")
    team_lead_id = fields.Many2one('res.users', related='purchase_team_id.team_lead_id')
    is_approval_member = fields.Boolean(string="Is Approval Member", compute='_compute_is_approval_member')

    def _compute_is_approval_member(self):
        for order in self:
            if order.purchase_approve_line.filtered(lambda l: l.partner_id.id == order.env.user.id):
                order.is_approval_member = True
            else:
                order.is_approval_member = False

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if order.purchase_team_id and order.purchase_team_id.team_member:
                for member_id in order.purchase_team_id.team_member:
                    self.env["purchase.approve.route"].create({
                        "purchase_id": order.id,
                        "partner_id": member_id.partner_id.id,
                        "role": member_id.role,
                        "state": "draft",
                    })
        return orders

    def write(self, vals):
        res = super().write(vals)
        if 'purchase_team_id' in vals:
            for line_id in self.purchase_approve_line:
                line_id.sudo().unlink()
            if self.purchase_team_id and self.purchase_team_id.team_member:
                for member_id in self.purchase_team_id.team_member:
                    self.env["purchase.approve.route"].create({
                        "purchase_id": self.id,
                        "partner_id": member_id.partner_id.id,
                        "role": member_id.role,
                        "state": "draft",
                    })
        return res

    def button_confirm(self):
        for order in self:
            if order.purchase_approve_line and order.team_lead_id and order.team_lead_id.id != order.env.user.id:
                pending_approvals = order.purchase_approve_line.filtered(lambda l: l.state != 'done')
                if pending_approvals:
                    pending_users = ', '.join(pending_approvals.mapped('partner_id.name'))
                    raise UserError(_('Purchase Order %s cannot be confirmed. Pending approvals from: %s') % (order.name, pending_users))
        return super().button_confirm()

    def approve_purchase(self):
        self.ensure_one()
        if not self.purchase_approve_line:
            raise UserError(_("No approval route configured for this purchase order."))
        
        approval_lines = self.purchase_approve_line.filtered(
            lambda l: l.partner_id.id == self.env.user.id)
        
        if not approval_lines:
            raise UserError(_("You are not authorized to approve %s. Only team members can approve.") % self.name)
        
        for line_id in approval_lines:
            if line_id.state in ['draft', 'cancel']:
                line_id.write({"state": "done"})
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'Thank You! The Purchase Order Has Been Approved From Your Side!',
                        'type': 'rainbow_man',
                        'img_url': 'itech_po_dynamic_approval/static/img/approved.png'
                    },
                }
            else:
                raise UserError(_("This purchase order has already been approved by you."))

    def disapprove_purchase(self):
        self.ensure_one()
        if not self.purchase_approve_line:
            raise UserError(_("No approval route configured for this purchase order."))
        
        approval_lines = self.purchase_approve_line.filtered(
            lambda l: l.partner_id.id == self.env.user.id)
        
        if not approval_lines:
            raise UserError(_("You are not authorized to reject %s. Only team members can reject.") % self.name)
        
        for line_id in approval_lines:
            if line_id.state in ['draft', 'done']:
                line_id.write({"state": "cancel"})
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': 'The Purchase Order Has Been Rejected!!',
                        'type': 'rainbow_man',
                        'img_url': 'itech_po_dynamic_approval/static/img/reject.png'
                    },
                }
            else:
                raise UserError(_("This Purchase Order Has Already Been Rejected By You."))

    def _default_purchase_team(self):
        return self.env['purchase.order.teams'].search([('short_code', '=', 'DefaultPO')], limit=1)
