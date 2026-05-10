# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestAccountMove(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.AccountMove = self.env['account.move']
        self.Partner = self.env['res.partner']
        self.Account = self.env['account.account']
        self.Product = self.env['product.product']
        self.Company = self.env['res.company']
        
        # Create test partner
        self.partner = self.Partner.create({
            'name': 'Test Customer',
            'is_company': True,
            'customer_rank': 1,
        })
        
        # Create test product
        self.product = self.Product.create({
            'name': 'Test Service',
            'type': 'service',
            'list_price': 1000.0,
        })
        
        # Get default company and set up accounts
        self.company = self.env.company
        
        # Create test accounts
        self.advance_account = self.Account.create({
            'name': 'Advance Received Test',
            'code': 'ADV001',
            'account_type': 'liability_current',
            'company_id': self.company.id,
        })
        
        self.retention_account = self.Account.create({
            'name': 'Retention Receivable Test',
            'code': 'RET001',
            'account_type': 'asset_receivable',
            'company_id': self.company.id,
        })
        
        self.performance_bond_account = self.Account.create({
            'name': 'Performance Bond Test',
            'code': 'PB001',
            'account_type': 'asset_receivable',
            'company_id': self.company.id,
        })
        
        self.deduction_account = self.Account.create({
            'name': 'Deductions Test',
            'code': 'DED001',
            'account_type': 'expense',
            'company_id': self.company.id,
        })
        
        # Configure company accounts
        self.company.write({
            'advance_received_account_id': self.advance_account.id,
            'retention_receivable_account_id': self.retention_account.id,
            'performance_bond_receivable_account_id': self.performance_bond_account.id,
            'deduction_account_id': self.deduction_account.id,
        })
    
    def _create_test_invoice(self, **kwargs):
        """Create a test invoice with default values"""
        default_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': '2026-02-03',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'name': 'Test Service',
            })],
        }
        default_vals.update(kwargs)
        return self.AccountMove.create(default_vals)
    
    def test_basic_fields_exist(self):
        """Test that all custom fields exist and can be set"""
        invoice = self._create_test_invoice()
        
        # Test reference fields
        invoice.write({
            'contract_ref': 'MC-21323',
            'po_ref': 'PO-12345',
            'invoice_ref': 'INV-001',
            'covered_period': 'Jan 2026',
        })
        
        self.assertEqual(invoice.contract_ref, 'MC-21323')
        self.assertEqual(invoice.po_ref, 'PO-12345') 
        self.assertEqual(invoice.invoice_ref, 'INV-001')
        self.assertEqual(invoice.covered_period, 'Jan 2026')
        
        # Test monetary fields
        invoice.write({
            'advance_payment_deduction': 100.0,
            'penalties_deductions': 50.0,
            'performance_bond_amount': 200.0,
            'retention_percent': 10.0,
        })
        
        self.assertEqual(invoice.advance_payment_deduction, 100.0)
        self.assertEqual(invoice.penalties_deductions, 50.0)
        self.assertEqual(invoice.performance_bond_amount, 200.0)
        self.assertEqual(invoice.retention_percent, 10.0)
    
    def test_retention_amount_computation(self):
        """Test retention amount is computed correctly"""
        invoice = self._create_test_invoice()
        
        # Test with 10% retention
        invoice.retention_percent = 10.0
        self.assertEqual(invoice.retention_amount, 100.0)  # 10% of 1000
        
        # Test with deductions that reduce tax base
        invoice.advance_payment_deduction = 200.0
        # tax_base_after_deductions = 1000 - 200 = 800
        # retention = 10% of 800 = 80
        self.assertEqual(invoice.retention_amount, 80.0)
        
        # Test with 0% retention
        invoice.retention_percent = 0.0
        self.assertEqual(invoice.retention_amount, 0.0)
    
    def test_deduction_totals_computation(self):
        """Test all computed fields are calculated correctly"""
        invoice = self._create_test_invoice()
        
        invoice.write({
            'advance_payment_deduction': 100.0,
            'penalties_deductions': 50.0,
            'performance_bond_amount': 80.0,
            'retention_percent': 10.0,
        })
        
        # Check computed values
        self.assertEqual(invoice.gross_untaxed, 1000.0)  # Original untaxed amount
        self.assertEqual(invoice.deductions_total, 230.0)  # 100 + 50 + 80
        self.assertEqual(invoice.tax_base_after_deductions, 770.0)  # 1000 - 230
        self.assertEqual(invoice.retention_amount, 77.0)  # 10% of 770
        
        # net_collect_now = amount_total - retention - advance - penalties - bond
        # Assuming tax is 0 for simplicity, amount_total = 1000
        expected_net = 1000.0 - 77.0 - 100.0 - 50.0 - 80.0
        self.assertEqual(invoice.net_collect_now, expected_net)
    
    def test_only_applies_to_customer_invoices(self):
        """Test computations only apply to customer invoices (out_invoice)"""
        # Test vendor bill (in_invoice)
        vendor_bill = self.AccountMove.create({
            'move_type': 'in_invoice',
            'partner_id': self.partner.id,
            'invoice_date': '2026-02-03',
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 1000.0,
                'name': 'Test Service',
            })],
            'advance_payment_deduction': 100.0,
            'retention_percent': 10.0,
        })
        
        # These should be 0 for vendor bills
        self.assertEqual(vendor_bill.gross_untaxed, 0)
        self.assertEqual(vendor_bill.deductions_total, 0)
        self.assertEqual(vendor_bill.tax_base_after_deductions, 0)
        self.assertEqual(vendor_bill.retention_amount, 0)
    
    def test_negative_deductions_validation(self):
        """Test that negative deductions are not allowed"""
        invoice = self._create_test_invoice()
        
        # Test negative advance payment
        with self.assertRaises(ValidationError):
            invoice.advance_payment_deduction = -100.0
        
        # Test negative penalties
        with self.assertRaises(ValidationError):
            invoice.penalties_deductions = -50.0
        
        # Test negative performance bond
        with self.assertRaises(ValidationError):
            invoice.performance_bond_amount = -80.0
        
        # Test negative retention (via computed field)
        with self.assertRaises(ValidationError):
            invoice.write({
                'retention_percent': -10.0,
            })
    
    def test_deductions_not_exceed_total_validation(self):
        """Test that total deductions cannot exceed invoice total"""
        invoice = self._create_test_invoice()  # Total = 1000
        
        # Test exceeding total with deductions
        with self.assertRaises(ValidationError):
            invoice.write({
                'advance_payment_deduction': 500.0,
                'penalties_deductions': 300.0,
                'performance_bond_amount': 200.0,
                'retention_percent': 20.0,  # This will make retention = 0, but others = 1000 > total
            })
    
    def test_get_deduction_amounts_method(self):
        """Test the _get_deduction_amounts helper method"""
        invoice = self._create_test_invoice()
        
        invoice.write({
            'advance_payment_deduction': 100.0,
            'penalties_deductions': 50.0,
            'performance_bond_amount': 80.0,
            'retention_percent': 10.0,
        })
        
        amounts = invoice._get_deduction_amounts()
        self.assertIsNotNone(amounts)
        self.assertEqual(amounts['advance'], 100.0)
        self.assertEqual(amounts['penalties'], 50.0)
        self.assertEqual(amounts['performance_bond'], 80.0)
        self.assertEqual(amounts['retention'], 77.0)  # 10% of (1000-230)
        
        # Test with no deductions
        invoice.write({
            'advance_payment_deduction': 0.0,
            'penalties_deductions': 0.0,
            'performance_bond_amount': 0.0,
            'retention_percent': 0.0,
        })
        
        amounts = invoice._get_deduction_amounts()
        self.assertIsNone(amounts)
    
    def test_validate_deduction_accounts(self):
        """Test account validation before posting"""
        invoice = self._create_test_invoice()
        invoice.write({
            'advance_payment_deduction': 100.0,
        })
        
        # Should not raise error with accounts configured
        try:
            invoice._validate_deduction_accounts()
        except ValidationError:
            self.fail("_validate_deduction_accounts raised ValidationError unexpectedly")
        
        # Remove advance account and test validation
        self.company.advance_received_account_id = False
        with self.assertRaises(ValidationError):
            invoice._validate_deduction_accounts()
    
    def test_currency_conversion(self):
        """Test currency conversion in _get_deduction_amounts"""
        # Create USD currency
        usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if not usd:
            usd = self.env['res.currency'].create({
                'name': 'USD',
                'symbol': '$',
                'rate_ids': [(0, 0, {'name': '2026-02-03', 'rate': 1.2})],  # 1 USD = 1.2 company currency
            })
        
        # Create invoice in USD
        invoice = self._create_test_invoice(currency_id=usd.id)
        invoice.write({
            'advance_payment_deduction': 100.0,  # USD
        })
        
        amounts = invoice._get_deduction_amounts()
        # Should be converted: 100 USD * 1.2 rate = 120 in company currency
        self.assertEqual(amounts['advance'], 120.0)
    
    def test_journal_lines_creation_on_post(self):
        """Test that additional journal lines are created when invoice is posted"""
        invoice = self._create_test_invoice()
        invoice.write({
            'advance_payment_deduction': 100.0,
            'penalties_deductions': 50.0,
            'performance_bond_amount': 80.0,
            'retention_percent': 10.0,
        })
        
        # Count lines before posting
        lines_before = len(invoice.line_ids)
        
        # Post the invoice
        invoice.action_post()
        
        # Should have additional lines for deductions
        lines_after = len(invoice.line_ids)
        self.assertGreater(lines_after, lines_before)
        
        # Check for specific deduction lines
        advance_lines = invoice.line_ids.filtered(
            lambda l: l.account_id == self.advance_account
        )
        self.assertEqual(len(advance_lines), 1)
        self.assertEqual(advance_lines.debit, 100.0)
        
        retention_lines = invoice.line_ids.filtered(
            lambda l: l.account_id == self.retention_account
        )
        self.assertEqual(len(retention_lines), 1)
        self.assertEqual(retention_lines.debit, 77.0)  # 10% of tax_base_after_deductions