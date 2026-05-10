# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # --- Mada Fee Settings ---
    # Percentage fee for amounts below the limit (0.8%)
    mada_low_fee_pct = fields.Float(
        string="Mada Fee (< Limit) (%)",
        default=0.8,
        help="Percentage fee applied for amounts below the specified limit."
    )

    # Threshold limit (5000 SAR)
    mada_low_fee_limit = fields.Float(
        string="Mada Fee Limit (SAR)",
        default=5000.0,
        help="The amount threshold (5000 SAR) that separates the two fee tiers."
    )

    # Fixed fee for amounts equal to or above the limit (40 SAR)
    mada_high_fee_fixed = fields.Float(
        string="Mada Fee (>= Limit) (Fixed SAR)",
        default=40.0,
        help="Fixed fee applied for amounts equal to or above the specified limit (e.g., 40 SAR)."
    )

    # --- Visa/Mastercard Fee Settings ---
    # Flat percentage rate (2.5%)
    visa_master_fee_pct = fields.Float(
        string="Visa/Mastercard Fee (%)",
        default=2.5,
        help="Flat percentage fee applied for all Visa/Mastercard transactions."
    )

