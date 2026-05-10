# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    # Field to store the calculated payment fee (excluding VAT)
    custom_fee_amount = fields.Monetary(
        compute='_compute_custom_fee_amount',
        string='Calculated Fee (No VAT)',
        store=True,
        currency_field='currency_id',
        help="The payment fee calculated based on the journal configuration and payment amount."
    )

    @api.depends('journal_id', 'amount')
    def _compute_custom_fee_amount(self):
        """
        Calculates the fee based on payment journal settings for Mada, Visa, and Mastercard.
        Assumes the journal name or code contains 'Mada' or 'Visa'/'Master' for identification.
        """
        for payment in self:
            payment.custom_fee_amount = 0.0
            journal = payment.journal_id
            amount = payment.amount

            # Only execute this logic for Bank/Cash journals
            if journal and journal.type in ['bank', 'cash'] and amount:
                journal_name = journal.name.lower()

                # --- 1. Visa and Mastercard Logic (2.5% Flat) ---
                if any(keyword in journal_name for keyword in ['visa', 'master', 'mastercard']):
                    fee_rate = journal.visa_master_fee_pct / 100.0
                    payment.custom_fee_amount = amount * fee_rate

                # --- 2. Mada Logic (Tiered Fee) ---
                elif 'mada' in journal_name:
                    # Tier 2: Amount >= 5000 SAR (Fixed fee: 40 SAR)
                    if amount >= journal.mada_low_fee_limit:
                        payment.custom_fee_amount = journal.mada_high_fee_fixed
                    # Tier 1: Amount < 5000 SAR (Percentage fee: 0.8%)
                    else:
                        fee_rate = journal.mada_low_fee_pct / 100.0
                        payment.custom_fee_amount = amount * fee_rate

                # 3. If no payment method matches, fee is zero.
                else:
                    payment.custom_fee_amount = 0.0

