# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    advance_received_account_id = fields.Many2one(
        "account.account",
        related="company_id.advance_received_account_id",
        readonly=False,
        string="Advance Received From Customers",
        domain="[('account_type', 'in', ['liability_current', 'liability_non_current'])]",
        help="Liability account for customer advances. This account is credited when receiving advance payments and debited when applying advance deduction on invoices.",
    )
    retention_receivable_account_id = fields.Many2one(
        "account.account",
        related="company_id.retention_receivable_account_id",
        readonly=False,
        string="Retention Receivable (10%)",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable'])]",
        help="Asset account for retention amounts. This represents the portion of invoice amount retained by the customer, typically 10% of the invoice total.",
    )
    performance_bonds_account_id = fields.Many2one(
        "account.account",
        related="company_id.performance_bond_receivable_account_id",
        readonly=False,
        string="Performance Bonds Receivable",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable'])]",
        help="Asset account for performance bond amounts. This represents amounts held as security for contract performance.",
    )
    deduction_against_invoice_account_id = fields.Many2one(
        "account.account",
        related="company_id.deduction_account_id",
        readonly=False,
        string="Deduction Against Invoice",
        domain="[('account_type', 'in', ['asset_current', 'asset_receivable'])]",
        help="Account for penalties and other deductions against invoice. This reduces the receivable amount for various types of contractual deductions.",
    )
