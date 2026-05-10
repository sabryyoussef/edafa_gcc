# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestResCompany(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.Company = self.env['res.company']
        self.Account = self.env['account.account']
        
        self.company = self.env.company
    
    def test_company_fields_exist(self):
        """Test that all custom company fields exist"""
        # Test that fields can be read
        field_names = [
            'advance_received_account_id',
            'retention_receivable_account_id', 
            'performance_bond_receivable_account_id',
            'deduction_account_id',
        ]
        
        for field_name in field_names:
            self.assertTrue(
                hasattr(self.company, field_name),
                f"Field '{field_name}' not found in res.company model"
            )
    
    def test_account_domain_restrictions(self):
        """Test that account fields have proper domain restrictions"""
        # Create test accounts
        test_account_1 = self.Account.create({
            'name': 'Test Account 1',
            'code': 'TEST001',
            'account_type': 'liability_current',
            'company_id': self.company.id,
        })
        
        # Account for different company
        other_company = self.Company.create({
            'name': 'Other Company',
        })
        
        test_account_2 = self.Account.create({
            'name': 'Test Account 2', 
            'code': 'TEST002',
            'account_type': 'liability_current',
            'company_id': other_company.id,
        })
        
        # Should be able to set account from same company
        self.company.advance_received_account_id = test_account_1
        self.assertEqual(self.company.advance_received_account_id, test_account_1)
        
        # Setting account from different company should work (domain enforced in UI)
        # but we can test the domain logic exists in field definition
        field_def = self.Company._fields['advance_received_account_id']
        domain = field_def.domain
        self.assertTrue(domain, "Field should have domain restriction")
        self.assertIn('company_id', str(domain))
    
    def test_field_help_text(self):
        """Test that fields have appropriate help text"""
        field_help_mapping = {
            'advance_received_account_id': 'Liability account for customer advances',
            'retention_receivable_account_id': 'Asset account for retention amounts',
            'performance_bond_receivable_account_id': 'Asset account for performance bond amounts',
            'deduction_account_id': 'Expense or contra-revenue account for penalties',
        }
        
        for field_name, expected_help_text in field_help_mapping.items():
            field_def = self.Company._fields[field_name]
            self.assertTrue(field_def.help, f"Field '{field_name}' should have help text")
            self.assertIn(expected_help_text.lower(), field_def.help.lower())
    
    def test_field_string_labels(self):
        """Test that fields have correct string labels"""
        field_string_mapping = {
            'advance_received_account_id': 'Advance Received From Customers',
            'retention_receivable_account_id': 'Retention Receivable',
            'performance_bond_receivable_account_id': 'Performance Bonds Receivable',
            'deduction_account_id': 'Deduction Against Invoice',
        }
        
        for field_name, expected_string in field_string_mapping.items():
            field_def = self.Company._fields[field_name]
            self.assertIn(expected_string, field_def.string)
    
    def test_field_types(self):
        """Test that all fields are Many2one to account.account"""
        field_names = [
            'advance_received_account_id',
            'retention_receivable_account_id',
            'performance_bond_receivable_account_id', 
            'deduction_account_id',
        ]
        
        for field_name in field_names:
            field_def = self.Company._fields[field_name]
            self.assertEqual(field_def.type, 'many2one', f"Field '{field_name}' should be Many2one")
            self.assertEqual(field_def.comodel_name, 'account.account', 
                           f"Field '{field_name}' should reference account.account")
    
    def test_accounts_can_be_set_and_retrieved(self):
        """Test that accounts can be properly set and retrieved"""
        # Create different types of accounts
        advance_account = self.Account.create({
            'name': 'Customer Advances',
            'code': 'ADV001',
            'account_type': 'liability_current',
            'company_id': self.company.id,
        })
        
        retention_account = self.Account.create({
            'name': 'Retention Receivable',
            'code': 'RET001', 
            'account_type': 'asset_receivable',
            'company_id': self.company.id,
        })
        
        performance_bond_account = self.Account.create({
            'name': 'Performance Bonds',
            'code': 'PB001',
            'account_type': 'asset_current',
            'company_id': self.company.id,
        })
        
        deduction_account = self.Account.create({
            'name': 'Penalties & Deductions',
            'code': 'DED001',
            'account_type': 'expense',
            'company_id': self.company.id,
        })
        
        # Set all accounts
        self.company.write({
            'advance_received_account_id': advance_account.id,
            'retention_receivable_account_id': retention_account.id,
            'performance_bond_receivable_account_id': performance_bond_account.id,
            'deduction_account_id': deduction_account.id,
        })
        
        # Verify they were set correctly
        self.assertEqual(self.company.advance_received_account_id, advance_account)
        self.assertEqual(self.company.retention_receivable_account_id, retention_account)
        self.assertEqual(self.company.performance_bond_receivable_account_id, performance_bond_account)
        self.assertEqual(self.company.deduction_account_id, deduction_account)
    
    def test_fields_are_optional(self):
        """Test that all account fields are optional (can be empty)"""
        field_names = [
            'advance_received_account_id',
            'retention_receivable_account_id',
            'performance_bond_receivable_account_id',
            'deduction_account_id',
        ]
        
        for field_name in field_names:
            field_def = self.Company._fields[field_name]
            # Fields should not be required by default
            self.assertFalse(getattr(field_def, 'required', False), 
                           f"Field '{field_name}' should not be required")
    
    def test_multiple_companies_independence(self):
        """Test that different companies can have different account configurations"""
        # Create another company
        company2 = self.Company.create({
            'name': 'Second Company',
        })
        
        # Create accounts for each company
        advance_account_1 = self.Account.create({
            'name': 'Advances Company 1',
            'code': 'ADV001',
            'account_type': 'liability_current',
            'company_id': self.company.id,
        })
        
        advance_account_2 = self.Account.create({
            'name': 'Advances Company 2',
            'code': 'ADV002', 
            'account_type': 'liability_current',
            'company_id': company2.id,
        })
        
        # Set different accounts for each company
        self.company.advance_received_account_id = advance_account_1
        company2.advance_received_account_id = advance_account_2
        
        # Verify independence
        self.assertEqual(self.company.advance_received_account_id, advance_account_1)
        self.assertEqual(company2.advance_received_account_id, advance_account_2)
        self.assertNotEqual(self.company.advance_received_account_id, 
                          company2.advance_received_account_id)