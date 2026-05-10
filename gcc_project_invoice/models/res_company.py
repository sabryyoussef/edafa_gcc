# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    advance_received_account_id = fields.Many2one(
        "account.account",
        string="Advance Received From Customers",
        domain="[('account_type', 'in', ['liability_current', 'liability_non_current']), ('company_id', '=', id)]",
        help="Liability account for customer advances. This account is credited when receiving advance payments and debited when applying advance deduction on invoices.",
    )
    retention_receivable_account_id = fields.Many2one(
        "account.account",
        string="Retention Receivable (10%)",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable']), ('company_id', '=', id)]",
        help="Asset account for retention amounts. This represents the portion of invoice amount retained by the customer, typically 10% of the invoice total, to be collected later.",
    )
    performance_bond_receivable_account_id = fields.Many2one(
        "account.account",
        string="Performance Bonds Receivable",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable']), ('company_id', '=', id)]",
        help="Asset account for performance bond amounts. This represents amounts held as security for contract performance and quality assurance.",
    )
    deduction_account_id = fields.Many2one(
        "account.account",
        string="Deduction Against Invoice",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable']), ('company_id', '=', id)]",
        help="Account for penalties and other deductions against invoice. This reduces the receivable amount for various types of contractual deductions and penalties.",
    )
