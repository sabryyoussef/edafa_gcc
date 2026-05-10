# -*- coding: utf-8 -*-

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestDownPaymentFlow(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create test data
        cls.partner = cls.env['res.partner'].create({
            'name': 'ABC Construction Ltd',
            'is_company': True,
        })
        
        cls.project = cls.env['project.project'].create({
            'name': 'Shopping Mall Construction',
            'partner_id': cls.partner.id,
            'project_value': 1000000.0,  # 1M LE
            'has_down_payment': True,
            'down_payment_percent': 20.0,  # 20% = 200K LE
        })
        
        cls.service_product = cls.env['product.product'].create({
            'name': 'Construction Services',
            'type': 'service',
            'list_price': 100000.0,
        })

    def test_complete_down_payment_workflow(self):
        """Test complete workflow: down payment → multiple invoices → reconciliation."""
        
        # Step 1: Receive down payment (200K LE as expected)
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 200000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'BANK-TRF-2024-001',
            'description': 'Initial down payment for mall construction',
        })
        
        # Confirm the down payment
        down_payment.action_confirm()
        self.assertEqual(down_payment.state, 'confirmed')
        
        # Verify project calculations
        self.project.refresh()
        self.assertEqual(self.project.down_payment_amount, 200000.0)
        self.assertEqual(self.project.total_down_payments_received, 200000.0)
        self.assertEqual(self.project.available_down_payment_balance, 200000.0)
        
        # Step 2: Create first invoice (Phase 1 - 300K LE)
        invoice1 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'auto_deduct_down_payment': True,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Construction Phase 1 - Foundation',
                'quantity': 1,
                'price_unit': 300000.0,
            })],
        })
        
        # Trigger onchange to populate down payment deduction
        invoice1._onchange_project_id()
        self.assertEqual(invoice1.available_down_payment, 200000.0)
        self.assertEqual(invoice1.down_payment_to_deduct, 200000.0)
        self.assertEqual(invoice1.advance_payment_deduction, 200000.0)
        
        # Post the invoice
        invoice1.action_post()
        
        # Verify reconciliation
        down_payment.refresh()
        self.assertEqual(down_payment.reconciled_amount, 200000.0)
        self.assertEqual(down_payment.remaining_amount, 0.0)
        self.assertEqual(down_payment.state, 'reconciled')
        
        # Verify project totals after first invoice
        self.project.refresh()
        self.assertEqual(self.project.total_invoiced_amount, 300000.0)
        self.assertEqual(self.project.total_advance_deducted, 200000.0)
        self.assertEqual(self.project.available_down_payment_balance, 0.0)
        self.assertEqual(self.project.remaining_project_balance, 700000.0)  # 1M - 300K
        
        # Step 3: Create second invoice without down payment (Phase 2 - 250K LE)
        invoice2 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Construction Phase 2 - Structure',
                'quantity': 1,
                'price_unit': 250000.0,
            })],
        })
        
        # Should not auto-populate since no down payment balance available
        invoice2._onchange_project_id()
        self.assertEqual(invoice2.available_down_payment, 0.0)
        self.assertEqual(invoice2.advance_payment_deduction, 0.0)
        
        # Post second invoice
        invoice2.action_post()
        
        # Verify final project totals
        self.project.refresh()
        self.assertEqual(self.project.total_invoiced_amount, 550000.0)  # 300K + 250K
        self.assertEqual(self.project.total_advance_deducted, 200000.0)  # Still only from first invoice
        self.assertEqual(self.project.remaining_project_balance, 450000.0)  # 1M - 550K

    def test_partial_down_payment_usage(self):
        """Test using down payment partially across multiple invoices."""
        
        # Create large down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 300000.0,  # More than expected 20%
            'date_received': fields.Date.today(),
            'payment_reference': 'EXTRA-PAYMENT-001',
        })
        down_payment.action_confirm()
        
        # Create first invoice with partial deduction
        invoice1 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'down_payment_to_deduct': 150000.0,  # Use only part of available
            'auto_deduct_down_payment': True,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Partial Work Phase 1',
                'quantity': 1,
                'price_unit': 200000.0,
            })],
        })
        
        # Manually set the deduction amount
        invoice1.advance_payment_deduction = 150000.0
        invoice1.action_post()
        
        # Verify partial reconciliation
        down_payment.refresh()
        self.assertEqual(down_payment.reconciled_amount, 150000.0)
        self.assertEqual(down_payment.remaining_amount, 150000.0)
        self.assertEqual(down_payment.state, 'confirmed')  # Not fully reconciled
        
        # Create second invoice using remaining balance
        invoice2 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 150000.0,  # Use remaining balance
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Partial Work Phase 2',
                'quantity': 1,
                'price_unit': 180000.0,
            })],
        })
        invoice2.action_post()
        
        # Verify full reconciliation
        down_payment.refresh()
        self.assertEqual(down_payment.reconciled_amount, 300000.0)
        self.assertEqual(down_payment.remaining_amount, 0.0)
        self.assertEqual(down_payment.state, 'reconciled')

    def test_multiple_down_payments_single_project(self):
        """Test handling multiple down payments for one project."""
        
        # Create first down payment
        dp1 = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 100000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-001',
        })
        dp1.action_confirm()
        
        # Create second down payment
        dp2 = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 150000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-002',
        })
        dp2.action_confirm()
        
        # Verify project totals
        self.project.refresh()
        self.assertEqual(self.project.total_down_payments_received, 250000.0)
        self.assertEqual(self.project.available_down_payment_balance, 250000.0)
        
        # Create invoice that uses both down payments
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 200000.0,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Combined Phase Work',
                'quantity': 1,
                'price_unit': 350000.0,
            })],
        })
        invoice.action_post()
        
        # Verify reconciliation happened in FIFO order (oldest first)
        dp1.refresh()
        dp2.refresh()
        
        # First payment should be fully used (100K)
        self.assertEqual(dp1.reconciled_amount, 100000.0)
        self.assertEqual(dp1.remaining_amount, 0.0)
        self.assertEqual(dp1.state, 'reconciled')
        
        # Second payment should be partially used (100K out of 150K)
        self.assertEqual(dp2.reconciled_amount, 100000.0)
        self.assertEqual(dp2.remaining_amount, 50000.0)
        self.assertEqual(dp2.state, 'confirmed')
        
        # Project should show remaining balance
        self.project.refresh()
        self.assertEqual(self.project.available_down_payment_balance, 50000.0)

    def test_down_payment_cancellation_scenarios(self):
        """Test various down payment cancellation scenarios."""
        
        # Create down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 200000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-CANCEL-TEST',
        })
        
        # Test cancellation from draft state
        down_payment.action_cancel()
        self.assertEqual(down_payment.state, 'cancelled')
        
        # Test reset to draft
        down_payment.action_set_to_draft()
        self.assertEqual(down_payment.state, 'draft')
        
        # Confirm and try to cancel
        down_payment.action_confirm()
        down_payment.action_cancel()
        self.assertEqual(down_payment.state, 'cancelled')
        
        # Create new down payment and use it in invoice
        down_payment2 = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 100000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-USED',
        })
        down_payment2.action_confirm()
        
        # Create invoice using the down payment
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 50000.0,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.service_product.id,
                'name': 'Test Service',
                'quantity': 1,
                'price_unit': 80000.0,
            })],
        })
        invoice.action_post()
        
        # Should not be able to cancel used down payment
        with self.assertRaises(ValidationError):
            down_payment2.action_cancel()

    def test_project_financial_reporting(self):
        """Test project financial reporting after various transactions."""
        
        # Initial state
        self.assertEqual(self.project.total_down_payments_received, 0.0)
        self.assertEqual(self.project.total_invoiced_amount, 0.0)
        self.assertEqual(self.project.remaining_project_balance, 1000000.0)
        
        # Add down payments
        dp1 = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 200000.0,
            'date_received': '2024-01-15',
            'payment_reference': 'Q1-DP',
        })
        dp1.action_confirm()
        
        dp2 = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 100000.0,
            'date_received': '2024-02-15',
            'payment_reference': 'Q1-DP-EXTRA',
        })
        dp2.action_confirm()
        
        # Create multiple invoices
        invoices_data = [
            ('Phase 1 - Foundation', 300000.0, 200000.0),
            ('Phase 2 - Structure', 250000.0, 100000.0),
            ('Phase 3 - Finishing', 200000.0, 0.0),  # No down payment left
        ]
        
        for name, amount, advance in invoices_data:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.partner.id,
                'project_id': self.project.id,
                'advance_payment_deduction': advance,
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.service_product.id,
                    'name': name,
                    'quantity': 1,
                    'price_unit': amount,
                })],
            })
            invoice.action_post()
        
        # Verify final project status
        self.project.refresh()
        
        # Down payment totals
        self.assertEqual(self.project.total_down_payments_received, 300000.0)
        self.assertEqual(self.project.available_down_payment_balance, 0.0)
        
        # Invoice totals
        self.assertEqual(self.project.total_invoiced_amount, 750000.0)
        self.assertEqual(self.project.total_advance_deducted, 300000.0)
        self.assertEqual(self.project.remaining_project_balance, 250000.0)  # 1M - 750K
        
        # Verify count fields for smart buttons
        self.assertEqual(self.project.down_payment_count, 2)
        self.assertEqual(self.project.invoice_count, 3)

    def test_currency_conversion_scenarios(self):
        """Test down payment handling with different currencies (if applicable)."""
        # This would test multi-currency scenarios if the project uses different currency
        # For simplified testing, we'll verify the currency is properly inherited
        
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 200000.0,
            'date_received': fields.Date.today(),
        })
        
        # Verify currency inheritance
        self.assertEqual(down_payment.currency_id, self.project.currency_id)
        self.assertEqual(down_payment.currency_id, self.project.company_id.currency_id)

    def test_down_payment_display_names(self):
        """Test down payment display name computation."""
        
        # Test with payment reference
        dp_with_ref = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 150000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'BANK-TRF-001',
        })
        
        expected_name = f"{self.project.name} - 150,000.00 (BANK-TRF-001)"
        self.assertEqual(dp_with_ref.display_name, expected_name)
        
        # Test without payment reference
        dp_no_ref = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 75000.0,
            'date_received': fields.Date.today(),
        })
        
        expected_name = f"{self.project.name} - 75,000.00"
        self.assertEqual(dp_no_ref.display_name, expected_name)