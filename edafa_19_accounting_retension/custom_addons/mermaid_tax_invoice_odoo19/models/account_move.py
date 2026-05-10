from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    x_contract_no = fields.Char(string='Contract No')
    x_retention = fields.Monetary(string='Retention', currency_field='currency_id', default=0.0)
    x_performance_bond = fields.Monetary(string='Performance Bond', currency_field='currency_id', default=0.0)
    x_net_amount = fields.Monetary(string='Net Amount', compute='_compute_net_amount', store=True, currency_field='currency_id')

    @api.depends('amount_total', 'x_retention', 'x_performance_bond')
    def _compute_net_amount(self):
        for record in self:
            record.x_net_amount = record.amount_total - record.x_retention - record.x_performance_bond
