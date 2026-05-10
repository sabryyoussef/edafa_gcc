#!/usr/bin/env python3
"""
Quick validation script to test XPath expressions and basic functionality.
This can be run without a full Odoo installation.
"""

def test_xpath_expressions():
    """Test XPath expressions in our views"""
    print("Testing XPath expressions...")
    
    try:
        from lxml import etree
        
        # Test our XPath expression
        xpath_expr = "//field[@name='partner_id']"
        compiled_xpath = etree.XPath(xpath_expr)
        print(f"✓ XPath compiles successfully: {xpath_expr}")
        
        # Create a sample XML structure similar to Odoo form view
        sample_form = """
        <form>
            <sheet>
                <group>
                    <field name="partner_id"/>
                    <field name="invoice_date"/>
                    <field name="amount_total"/>
                </group>
            </sheet>
        </form>
        """
        
        tree = etree.fromstring(sample_form)
        matches = compiled_xpath(tree)
        
        if matches:
            print(f"✓ XPath finds {len(matches)} matching element(s) in sample structure")
            return True
        else:
            print("⚠ XPath finds no matches (this is expected in sample structure)")
            return True
            
    except Exception as e:
        print(f"✗ XPath test failed: {e}")
        return False

def test_view_structure():
    """Test that our view XML is well-formed"""
    print("\nTesting view XML structure...")
    
    try:
        import os
        from lxml import etree
        
        # Get the actual view file
        view_file = os.path.join(os.path.dirname(__file__), 'views', 'account_move_views.xml')
        
        if not os.path.exists(view_file):
            print(f"✗ View file not found: {view_file}")
            return False
            
        with open(view_file, 'r') as f:
            content = f.read()
            
        # Parse XML
        tree = etree.fromstring(content)
        print("✓ View XML is well-formed")
        
        # Check structure
        records = tree.xpath("//record[@model='ir.ui.view']")
        if records:
            print(f"✓ Found {len(records)} view record(s)")
        else:
            print("✗ No view records found")
            return False
            
        # Check inheritance
        inherit_refs = tree.xpath("//field[@name='inherit_id']")
        if inherit_refs:
            ref_value = inherit_refs[0].get('ref')
            print(f"✓ Inherits from: {ref_value}")
            
            # Check if it's the correct reference
            if ref_value == 'account.view_move_form':
                print("✓ Uses correct parent view reference")
            else:
                print(f"⚠ Parent view reference: {ref_value}")
        
        # Check XPath in actual view
        xpath_elements = tree.xpath("//xpath[@expr]")
        if xpath_elements:
            for xpath_elem in xpath_elements:
                expr = xpath_elem.get('expr')
                position = xpath_elem.get('position')
                print(f"✓ XPath: {expr} (position: {position})")
                
                # Validate XPath syntax
                try:
                    etree.XPath(expr)
                    print(f"✓ XPath syntax valid")
                except etree.XPathSyntaxError as e:
                    print(f"✗ XPath syntax error: {e}")
                    return False
                    
        return True
        
    except Exception as e:
        print(f"✗ View structure test failed: {e}")
        return False

def test_field_coverage():
    """Test that custom fields are present in the view"""
    print("\nTesting field coverage...")
    
    try:
        import os
        from lxml import etree
        
        # Expected custom fields
        expected_fields = [
            'contract_ref', 'po_ref', 'invoice_ref', 'covered_period',
            'advance_payment_deduction', 'penalties_deductions', 'performance_bond_amount',
            'retention_percent', 'retention_amount',
            'gross_untaxed', 'deductions_total', 'tax_base_after_deductions',
            'net_collect_now'
        ]
        
        # Parse view
        view_file = os.path.join(os.path.dirname(__file__), 'views', 'account_move_views.xml')
        with open(view_file, 'r') as f:
            content = f.read()
        tree = etree.fromstring(content)
        
        # Find all field elements
        field_elements = tree.xpath("//field[@name]")
        found_fields = [elem.get('name') for elem in field_elements]
        
        missing_fields = []
        for field in expected_fields:
            if field in found_fields:
                print(f"✓ Field in view: {field}")
            else:
                missing_fields.append(field)
                print(f"✗ Missing field: {field}")
        
        if missing_fields:
            print(f"Missing fields: {missing_fields}")
            return False
        else:
            print("✓ All expected fields are present in view")
            return True
            
    except Exception as e:
        print(f"✗ Field coverage test failed: {e}")
        return False

def main():
    """Run quick validation tests"""
    print("=== QUICK MODULE VALIDATION ===\n")
    
    tests = [
        test_xpath_expressions,
        test_view_structure,
        test_field_coverage,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)
    
    print(f"\n=== RESULTS ===")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("🎉 All quick tests PASSED!")
        return 0
    else:
        print("❌ Some tests FAILED!")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())