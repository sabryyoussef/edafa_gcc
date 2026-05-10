# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from lxml import etree


class TestViewsXPath(TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.View = self.env['ir.ui.view']
        self.AccountMove = self.env['account.move']
    
    def test_parent_view_exists(self):
        """Test that the parent view we're inheriting from exists"""
        parent_view = self.View.search([
            ('model', '=', 'account.move'),
            ('name', 'ilike', 'account.move.form')
        ], limit=1)
        
        if not parent_view:
            # Try alternative view names
            parent_view = self.env.ref('account.view_move_form', raise_if_not_found=False)
        
        self.assertTrue(parent_view, "Parent view 'account.view_move_form' not found")
        self.assertEqual(parent_view.model, 'account.move')
        self.assertEqual(parent_view.type, 'form')
    
    def test_partner_id_field_exists_in_parent(self):
        """Test that the partner_id field exists in the parent view"""
        parent_view = self.env.ref('account.view_move_form')
        
        # Parse the view arch
        arch_tree = etree.fromstring(parent_view.arch)
        
        # Look for partner_id field
        partner_fields = arch_tree.xpath("//field[@name='partner_id']")
        self.assertTrue(partner_fields, "partner_id field not found in parent view")
    
    def test_custom_view_inheritance_works(self):
        """Test that our custom view inheritance is working"""
        # Get our custom view
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice', raise_if_not_found=False)
        self.assertTrue(custom_view, "Custom view not found")
        
        # Check inheritance is correct
        self.assertEqual(custom_view.model, 'account.move')
        self.assertEqual(custom_view.inherit_id.id, self.env.ref('account.view_move_form').id)
    
    def test_xpath_expression_is_valid(self):
        """Test that our XPath expression is syntactically correct"""
        # Parse our view arch
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        # Find the xpath element
        xpath_elements = arch_tree.xpath("//xpath")
        self.assertTrue(xpath_elements, "No xpath elements found in custom view")
        
        xpath_element = xpath_elements[0]
        expr = xpath_element.get('expr')
        self.assertEqual(expr, "//field[@name='partner_id']", "XPath expression is incorrect")
        
        position = xpath_element.get('position')
        self.assertEqual(position, 'after', "XPath position should be 'after'")
    
    def test_custom_fields_in_view_arch(self):
        """Test that all our custom fields are present in the view"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        # List of expected fields
        expected_fields = [
            'contract_ref',
            'po_ref', 
            'invoice_ref',
            'covered_period',
            'advance_payment_deduction',
            'penalties_deductions',
            'performance_bond_amount',
            'retention_percent',
            'retention_amount',
            'gross_untaxed',
            'deductions_total',
            'tax_base_after_deductions',
            'amount_tax',
            'amount_total',
            'net_collect_now',
        ]
        
        for field_name in expected_fields:
            field_elements = arch_tree.xpath(f"//field[@name='{field_name}']")
            self.assertTrue(field_elements, f"Field '{field_name}' not found in view arch")
    
    def test_view_renders_without_error(self):
        """Test that the combined view (parent + inheritance) renders without errors"""
        # Create a test invoice record
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'customer_rank': 1,
        })
        
        invoice = self.AccountMove.create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
        })
        
        # Try to render the view for this record
        try:
            view_result = self.env['ir.ui.view'].with_context(
                active_id=invoice.id,
                active_model='account.move'
            ).get_view(
                view_id=self.env.ref('account.view_move_form').id,
                view_type='form',
                context={'form_view_initial_mode': 'edit'}
            )
            
            # Check that the view has arch
            self.assertTrue(view_result.get('arch'), "View rendering failed - no arch returned")
            
        except Exception as e:
            self.fail(f"View rendering failed with error: {e}")
    
    def test_group_visibility_conditions(self):
        """Test that visibility conditions on groups are correct"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        # Find the main project deductions group
        project_groups = arch_tree.xpath("//group[@name='gcc_project_deductions']")
        self.assertEqual(len(project_groups), 1, "Project deductions group not found or duplicated")
        
        group = project_groups[0]
        attrs = group.get('attrs')
        self.assertTrue(attrs, "Group should have visibility attributes")
        
        # Should be invisible for non-customer invoices
        self.assertIn("'invisible'", attrs)
        self.assertIn("'move_type'", attrs) 
        self.assertIn("'out_invoice'", attrs)
    
    def test_readonly_fields_configuration(self):
        """Test that computed fields are marked as readonly"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        readonly_fields = [
            'gross_untaxed',
            'deductions_total', 
            'tax_base_after_deductions',
            'amount_tax',
            'amount_total',
            'retention_amount',
            'net_collect_now',
        ]
        
        for field_name in readonly_fields:
            field_elements = arch_tree.xpath(f"//field[@name='{field_name}']")
            self.assertTrue(field_elements, f"Field '{field_name}' not found")
            
            field = field_elements[0]
            readonly_attr = field.get('readonly')
            self.assertEqual(readonly_attr, '1', f"Field '{field_name}' should be readonly")
    
    def test_field_placeholders(self):
        """Test that input fields have appropriate placeholders"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        # Check specific placeholders
        contract_field = arch_tree.xpath("//field[@name='contract_ref']")[0]
        self.assertEqual(contract_field.get('placeholder'), 'e.g. MC-21323')
        
        po_field = arch_tree.xpath("//field[@name='po_ref']")[0]
        self.assertEqual(po_field.get('placeholder'), 'PO No')
        
        invoice_field = arch_tree.xpath("//field[@name='invoice_ref']")[0]
        self.assertEqual(invoice_field.get('placeholder'), 'Inv Ref')
    
    def test_view_structure_hierarchy(self):
        """Test that the view structure and hierarchy is correct"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        # Should have main group with name 'gcc_project_deductions'
        main_group = arch_tree.xpath("//group[@name='gcc_project_deductions']")[0]
        self.assertEqual(main_group.get('string'), 'Project / Deductions')
        
        # Should have nested groups inside
        nested_groups = main_group.xpath(".//group")
        self.assertGreaterEqual(len(nested_groups), 2, "Should have at least 2 nested groups")
        
        # Check summary group
        summary_groups = arch_tree.xpath("//group[@name='gcc_summary']")
        self.assertEqual(len(summary_groups), 1, "Summary group not found")
        self.assertEqual(summary_groups[0].get('string'), 'Summary')
    
    def test_view_validation_passes(self):
        """Test that the view passes Odoo's internal validation"""
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        
        try:
            # This will trigger view validation
            custom_view._check_xml()
        except Exception as e:
            self.fail(f"View validation failed: {e}")
    
    def test_all_model_fields_have_definitions(self):
        """Test that all fields used in the view are defined in the model"""
        # Get the model
        account_move_model = self.env['account.move']
        
        # Get field names from our view
        custom_view = self.env.ref('gcc_project_invoice.view_move_form_inherit_gcc_project_invoice')
        arch_tree = etree.fromstring(custom_view.arch)
        
        field_elements = arch_tree.xpath("//field[@name]")
        field_names = [elem.get('name') for elem in field_elements]
        
        # Check each field exists in the model
        for field_name in field_names:
            self.assertTrue(
                hasattr(account_move_model, field_name),
                f"Field '{field_name}' used in view but not defined in model"
            )
            
            # Also check field is in model._fields
            self.assertIn(
                field_name, 
                account_move_model._fields,
                f"Field '{field_name}' not in model._fields"
            )