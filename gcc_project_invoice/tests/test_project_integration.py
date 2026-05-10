# -*- coding: utf-8 -*-

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProjectIntegration(TransactionCase):
    
    def setUp(self):
        super().setUp()
        
        # Create test company and currency
        self.company = self.env.company
        self.currency = self.company.currency_id
        
        # Create test partner (customer)
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'is_company': True,
        })
        
        # Create test project
        self.project = self.env['project.project'].create({
            'name': 'Test Construction Project',
            'partner_id': self.partner.id,
            'project_value': 100000.0,
            'has_down_payment': True,
            'down_payment_percent': 30.0,
        })
        
        # Create test accounts for deductions
        account_type_receivable = self.env.ref('account.data_account_type_receivable')
        account_type_current_liabilities = self.env.ref('account.data_account_type_current_liabilities')
        
        self.advance_account = self.env['account.account'].create({
            'name': 'Advance Received Test',
            'code': 'TEST_ADV',
            'account_type': 'liability_current',
        })
        
        # Configure company accounts
        self.company.advance_received_account_id = self.advance_account.id

    def test_project_down_payment_calculation(self):
        """Test project down payment amount calculation."""
        # Test automatic calculation
        self.assertEqual(self.project.down_payment_amount, 30000.0)
        
        # Test percentage change
        self.project.down_payment_percent = 25.0
        self.project._compute_down_payment_amount()
        self.assertEqual(self.project.down_payment_amount, 25000.0)
        
        # Test disabling down payment
        self.project.has_down_payment = False
        self.project._compute_down_payment_amount()
        self.assertEqual(self.project.down_payment_amount, 0.0)

    def test_project_validation(self):
        """Test project field validations."""
        # Test negative project value
        with self.assertRaises(ValidationError):
            self.project.project_value = -1000.0
            self.project._check_project_value()
        
        # Test invalid down payment percentage
        with self.assertRaises(ValidationError):
            self.project.down_payment_percent = -10.0
            self.project._check_down_payment_percent()
        
        with self.assertRaises(ValidationError):
            self.project.down_payment_percent = 150.0
            self.project._check_down_payment_percent()

    def test_down_payment_creation_and_states(self):
        """Test down payment record creation and state management."""
        # Create down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 30000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'BANK-TRF-001',
        })
        
        # Test initial state
        self.assertEqual(down_payment.state, 'draft')
        self.assertEqual(down_payment.remaining_amount, 30000.0)
        self.assertEqual(down_payment.reconciled_amount, 0.0)
        
        # Test confirmation
        down_payment.action_confirm()
        self.assertEqual(down_payment.state, 'confirmed')
        
        # Test project totals update
        self.project._compute_down_payment_totals()
        self.assertEqual(self.project.total_down_payments_received, 30000.0)
        self.assertEqual(self.project.available_down_payment_balance, 30000.0)

    def test_down_payment_validation(self):
        """Test down payment validations."""
        # Test negative amount
        with self.assertRaises(ValidationError):
            self.env['project.down.payment'].create({
                'project_id': self.project.id,
                'amount': -1000.0,
                'date_received': fields.Date.today(),
            })
        
        # Test exceeding project expectations
        large_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 35000.0,  # > 30% + 5% tolerance
            'date_received': fields.Date.today(),
        })
        
        # Should not raise error within tolerance
        large_payment.action_confirm()
        
        # But should raise error if way over
        with self.assertRaises(ValidationError):
            self.env['project.down.payment'].create({
                'project_id': self.project.id,
                'amount': 50000.0,  # Way over expected 30%
                'date_received': fields.Date.today(),
            })

    def test_invoice_project_integration(self):
        """Test invoice creation with project integration."""
        # Create and confirm down payment first
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 30000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-001',
        })
        down_payment.action_confirm()
        
        # Create product for invoice line
        product = self.env['product.product'].create({
            'name': 'Construction Service',
            'type': 'service',
            'list_price': 50000.0,
        })
        
        # Create invoice with project
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 50000.0,
            })],
        })
        
        # Test project-related computations
        self.assertEqual(invoice.available_down_payment, 30000.0)
        
        # Test auto-deduction trigger
        invoice._onchange_project_id()
        self.assertEqual(invoice.down_payment_to_deduct, 30000.0)
        self.assertEqual(invoice.advance_payment_deduction, 30000.0)

    def test_invoice_down_payment_validation(self):
        """Test invoice down payment validation."""
        # Create down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 20000.0,
            'date_received': fields.Date.today(),
        })
        down_payment.action_confirm()
        
        # Create product for invoice
        product = self.env['product.product'].create({
            'name': 'Service',
            'type': 'service',
            'list_price': 50000.0,
        })
        
        # Create invoice trying to deduct more than available
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'down_payment_to_deduct': 25000.0,  # More than available 20,000
            'auto_deduct_down_payment': True,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 50000.0,
            })],
        })
        
        # Should raise validation error
        with self.assertRaises(ValidationError):
            invoice._check_down_payment_availability()

    def test_customer_project_mismatch_validation(self):
        """Test validation for customer-project mismatch."""
        # Create different customer
        other_partner = self.env['res.partner'].create({
            'name': 'Different Customer',
        })
        
        # Create product for invoice
        product = self.env['product.product'].create({
            'name': 'Service', 
            'type': 'service',
            'list_price': 10000.0,
        })
        
        # Create invoice with mismatched customer and project
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': other_partner.id,  # Different from project customer
            'project_id': self.project.id,   # Project belongs to self.partner
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 10000.0,
            })],
        })
        
        # Should raise validation error
        with self.assertRaises(ValidationError):
            invoice._check_down_payment_availability()

    def test_down_payment_reconciliation_process(self):
        """Test the complete down payment reconciliation process."""
        # Create and confirm down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 30000.0,
            'date_received': fields.Date.today(),
            'payment_reference': 'DP-001',
        })
        down_payment.action_confirm()
        
        # Create product
        product = self.env['product.product'].create({
            'name': 'Construction Phase 1',
            'type': 'service',
            'list_price': 40000.0,
        })
        
        # Create and post invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 25000.0,  # Partial deduction
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 40000.0,
            })],
        })
        
        # Post the invoice (this should trigger reconciliation)
        invoice.action_post()
        
        # Check reconciliation results
        down_payment.refresh()
        self.assertEqual(down_payment.reconciled_amount, 25000.0)
        self.assertEqual(down_payment.remaining_amount, 5000.0)
        self.assertEqual(down_payment.state, 'confirmed')  # Not fully reconciled
        
        # Check project totals
        self.project._compute_down_payment_totals()
        self.assertEqual(self.project.available_down_payment_balance, 5000.0)

    def test_multiple_invoices_down_payment_consumption(self):
        """Test multiple invoices consuming down payment balance."""
        # Create large down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 50000.0,
            'date_received': fields.Date.today(),
        })
        down_payment.action_confirm()
        
        product = self.env['product.product'].create({
            'name': 'Service',
            'type': 'service', 
            'list_price': 20000.0,
        })
        
        # Create first invoice
        invoice1 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 20000.0,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 20000.0,
            })],
        })
        invoice1.action_post()
        
        # Create second invoice
        invoice2 = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 30000.0,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 30000.0,
            })],
        })
        invoice2.action_post()
        
        # Check final state - down payment should be fully consumed
        down_payment.refresh()
        self.assertEqual(down_payment.reconciled_amount, 50000.0)
        self.assertEqual(down_payment.remaining_amount, 0.0)
        self.assertEqual(down_payment.state, 'reconciled')
        
        # Check project balance
        self.project._compute_down_payment_totals()
        self.assertEqual(self.project.available_down_payment_balance, 0.0)

    def test_project_financial_totals(self):
        """Test project financial totals computation."""
        # Create down payment
        down_payment = self.env['project.down.payment'].create({
            'project_id': self.project.id,
            'amount': 30000.0,
            'date_received': fields.Date.today(),
        })
        down_payment.action_confirm()
        
        # Create product
        product = self.env['product.product'].create({
            'name': 'Service',
            'type': 'service',
        })
        
        # Create and post invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'project_id': self.project.id,
            'advance_payment_deduction': 15000.0,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'quantity': 1,
                'price_unit': 40000.0,
            })],
        })
        invoice.action_post()
        
        # Check project totals
        self.project._compute_project_totals()
        self.assertEqual(self.project.total_invoiced_amount, 40000.0)
        self.assertEqual(self.project.total_advance_deducted, 15000.0)
        self.assertEqual(self.project.remaining_project_balance, 60000.0)  # 100k - 40k
        
        # Check down payment balance
        self.project._compute_down_payment_totals()
        self.assertEqual(self.project.available_down_payment_balance, 15000.0)  # 30k - 15k used

    def test_smart_button_actions(self):
        """Test project smart button actions."""
        # Test view invoices action
        action = self.project.action_view_invoices()
        self.assertEqual(action['res_model'], 'account.move')
        self.assertIn(('project_id', '=', self.project.id), action['domain'])
        
        # Test view down payments action
        action = self.project.action_view_down_payments()
        self.assertEqual(action['res_model'], 'project.down.payment')
        
        # Test create invoice action
        action = self.project.action_create_invoice()
        self.assertEqual(action['res_model'], 'account.move')
        self.assertEqual(action['context']['default_project_id'], self.project.id)
        
        # Test add down payment action
        action = self.project.action_add_down_payment()
        self.assertEqual(action['res_model'], 'project.down.payment')
        self.assertEqual(action['context']['default_project_id'], self.project.id)