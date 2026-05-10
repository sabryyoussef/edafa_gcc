# Mermaid Tax Invoice for Odoo 19

## Overview

The **Mermaid Tax Invoice** module provides a professional, customized tax invoice report layout for Odoo 19. This module adds a custom field (`x_contract_no`) to invoices and generates a formatted tax invoice report matching specific business requirements.

---

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Use Cases](#use-cases)
6. [Technical Details](#technical-details)

---

## Features

- ✅ **Custom Contract Number Field** - Add contract reference numbers to invoices
- ✅ **Professional Tax Invoice Layout** - Clean, business-ready invoice template
- ✅ **Automatic VAT Calculation** - Displays tax amounts and totals
- ✅ **Company Branding** - Includes company logo and information
- ✅ **Customer Details** - Complete customer/partner information display
- ✅ **Line Items** - Detailed product/service listing with quantities and prices
- ✅ **Multi-Currency Support** - Works with any currency configured in Odoo
- ✅ **PDF Export** - Generate professional PDF invoices for printing or emailing

---

## Installation

### Prerequisites

- Odoo 19.0
- `account` module (installed by default)
- `web` module (installed by default)

### Installation Steps

1. **Copy the Module**
   ```bash
   cp -r mermaid_tax_invoice_odoo19 /path/to/odoo/addons/
   ```

2. **Update Apps List**
   - Go to **Apps** menu
   - Click **Update Apps List**
   - Activate Developer Mode if not already active

3. **Install the Module**
   - Search for "Mermaid Tax Invoice"
   - Click **Install**

4. **Verify Installation**
   - Go to **Accounting → Customers → Invoices**
   - Open any invoice
   - You should see a new field: **Contract No**
   - Check the **Print** dropdown for the tax invoice report

---

## Configuration

### No Additional Configuration Required

The module works out of the box. However, you can customize:

1. **Company Information**
   - Go to **Settings → General Settings → Companies**
   - Update company name, address, phone, VAT number
   - Upload company logo

2. **Invoice Layout**
   - The tax invoice automatically uses your company's external layout
   - Configure headers/footers in **Settings → Technical → Reports → Report Layout**

---

## Usage

### Adding Contract Number to Invoices

1. **Create or Edit an Invoice**
   - Go to **Accounting → Customers → Invoices**
   - Click **Create** or open existing invoice

2. **Enter Contract Number**
   - Locate the **Contract No** field
   - Enter the contract reference number (e.g., "CTR-2025-001")

3. **Save the Invoice**

### Printing Tax Invoice

1. **Open an Invoice**
   - Go to **Accounting → Customers → Invoices**
   - Select the invoice to print

2. **Print the Report**
   - Click the **Print** dropdown button
   - Select **Tax Invoice** (or the custom report name)

3. **PDF Generation**
   - The system generates a professional PDF
   - Download, print, or email directly to the customer

---

## Use Cases

### Use Case 1: Standard Sales Invoice with Contract

**Scenario**: Your company has a service contract with a client and needs to invoice monthly fees.

**Steps**:
1. Create a new customer invoice
2. Add customer: "ABC Corporation"
3. Add invoice lines:
   - Service: "Monthly Maintenance" - Quantity: 1 - Price: 5,000 SAR
   - Product: "Support Package" - Quantity: 1 - Price: 2,000 SAR
4. Enter **Contract No**: "CTR-2025-ABC-001"
5. Add tax (e.g., 15% VAT)
6. Confirm the invoice
7. Print **Tax Invoice** report

**Result**: 
- Professional invoice with contract reference
- Clear line items with VAT breakdown
- Total: 8,050 SAR (including 1,050 SAR VAT)

---

### Use Case 2: Product Sales with Multiple Items

**Scenario**: Selling multiple products to a customer with standard VAT.

**Steps**:
1. Create invoice for customer "XYZ Trading"
2. Add multiple product lines:
   - Product A: Qty 10 × 150 SAR = 1,500 SAR
   - Product B: Qty 5 × 300 SAR = 1,500 SAR
   - Product C: Qty 20 × 75 SAR = 1,500 SAR
3. Enter **Contract No**: "PO-2025-XYZ-100"
4. Apply 15% VAT
5. Generate tax invoice

**Result**:
- Subtotal: 4,500 SAR
- VAT (15%): 675 SAR
- Total: 5,175 SAR
- All items clearly listed with quantities and prices

---

### Use Case 3: Service Invoice Without Contract

**Scenario**: One-time consulting service without a formal contract.

**Steps**:
1. Create invoice for "New Client Ltd"
2. Add service:
   - Consulting Services: 8 hours × 500 SAR/hour = 4,000 SAR
3. **Contract No**: Leave blank or enter "N/A"
4. Apply 15% VAT
5. Print tax invoice

**Result**:
- Professional invoice even without contract number
- Service details clearly shown
- VAT compliant format

---

### Use Case 4: International Customer (VAT Exempt)

**Scenario**: Invoicing an international customer who is VAT exempt.

**Steps**:
1. Create invoice for international customer
2. Set customer country to outside your tax jurisdiction
3. Add products/services
4. **Contract No**: "INTL-2025-001"
5. Apply 0% VAT or no tax
6. Generate invoice

**Result**:
- Clean invoice showing 0% or no tax
- Subtotal equals total
- Professional format for international business

---

### Use Case 5: Credit Note with Reference

**Scenario**: Issuing a credit note for returned goods.

**Steps**:
1. Go to original invoice
2. Click **Add Credit Note**
3. Select reason: "Returned Goods"
4. Enter **Contract No**: Same as original invoice
5. Adjust quantities/amounts
6. Confirm and print

**Result**:
- Credit note with negative amounts
- Reference to original invoice
- Professional documentation for refund

---

### Use Case 6: Recurring Contract Invoices

**Scenario**: Monthly invoicing for a long-term contract.

**Steps**:
1. Create first invoice with **Contract No**: "CTR-2025-LT-001"
2. Set up recurring invoice:
   - Go to **Accounting → Configuration → Recurring**
   - Create subscription based on the invoice
   - Set to monthly recurrence
3. Each month, invoice auto-generates with same contract number

**Result**:
- Consistent invoicing format
- Same contract reference on all invoices
- Time-saving automation

---

### Use Case 7: Multi-Currency Invoice

**Scenario**: Invoicing a customer in USD while your base currency is SAR.

**Steps**:
1. Create invoice
2. Set currency to USD
3. Add invoice lines (prices in USD)
4. Enter **Contract No**: "USD-CTR-2025-001"
5. Apply applicable tax
6. Print tax invoice

**Result**:
- Invoice displays in USD
- Currency symbol shown correctly
- Exchange rate applied if needed
- Professional multi-currency support

---

### Use Case 8: Batch Invoice Printing

**Scenario**: Print tax invoices for multiple confirmed invoices at once.

**Steps**:
1. Go to **Accounting → Customers → Invoices**
2. Filter by status: "Posted"
3. Select multiple invoices (checkbox)
4. Click **Print → Tax Invoice**

**Result**:
- Single PDF with all selected invoices
- Each invoice on separate page
- Batch processing for efficiency

---

## Technical Details

### Module Structure

```
mermaid_tax_invoice_odoo19/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── account_move.py          # Adds x_contract_no field
├── report/
│   └── report.xml               # Report action definition
├── security/
│   └── ir.model.access.csv      # Access rights
└── views/
    ├── account_move_view.xml    # Form view extension
    └── report_tax_invoice.xml   # Report template
```

### Custom Field

**Field Name**: `x_contract_no`
- **Type**: Char (Text)
- **Label**: Contract No
- **Model**: account.move
- **Optional**: Yes
- **Usage**: Reference contract or purchase order numbers

### Report Details

**Report Name**: Tax Invoice
- **Technical Name**: mermaid_tax_invoice_odoo19.report_tax_invoice
- **Model**: account.move
- **Type**: QWeb PDF
- **Paper Format**: A4
- **Binding**: Automatically added to invoice Print menu

### Supported Invoice Types

- ✅ Customer Invoices
- ✅ Vendor Bills
- ✅ Credit Notes
- ✅ Debit Notes
- ✅ Refunds

---

## Customization

### Modifying the Report Template

1. **Edit Template**
   - File: `views/report_tax_invoice.xml`
   - Modify HTML/QWeb template as needed
   - Upgrade module to apply changes

2. **Common Customizations**:
   - Add company logo in header
   - Change colors or styling
   - Add additional fields
   - Modify footer text
   - Adjust spacing/layout

### Adding More Fields

1. **Edit Model**
   ```python
   # models/account_move.py
   x_custom_field = fields.Char(string="Custom Field")
   ```

2. **Update View**
   ```xml
   <!-- views/account_move_view.xml -->
   <field name="x_custom_field"/>
   ```

3. **Add to Report**
   ```xml
   <!-- views/report_tax_invoice.xml -->
   <span t-field="o.x_custom_field"/>
   ```

---

## Best Practices

1. **Consistent Contract Numbering**
   - Use a standard format: "CTR-YYYY-CLIENT-###"
   - Example: "CTR-2025-ABC-001"

2. **Complete Customer Information**
   - Ensure customers have complete address
   - Add VAT numbers for tax-registered customers
   - Include phone and email

3. **Accurate Tax Configuration**
   - Configure taxes properly in Odoo
   - Use correct tax rates for your jurisdiction
   - Set tax positions for international customers

4. **Regular Backups**
   - Backup invoices and reports regularly
   - Keep PDF archives for legal compliance

5. **Testing**
   - Test invoice generation before going live
   - Verify calculations and tax amounts
   - Check printing on actual paper

---

## Troubleshooting

### Issue 1: Contract No Field Not Visible

**Solution**: 
- Upgrade the module
- Clear browser cache
- Refresh the page

### Issue 2: Report Not in Print Menu

**Solution**:
- Check module is installed
- Verify report definition in `report/report.xml`
- Restart Odoo server

### Issue 3: PDF Generation Errors

**Solution**:
- Check wkhtmltopdf is installed
- Verify template syntax in XML
- Check Odoo logs for errors

### Issue 4: Wrong Company Logo

**Solution**:
- Go to **Settings → Companies**
- Upload correct logo
- Ensure logo file is not too large (< 1MB recommended)

---

## Support and Development

### Module Information
- **Version**: 19.0.1.0.0
- **Category**: Accounting/Reports
- **License**: LGPL-3
- **Odoo Version**: 19.0

### Getting Help
- Review Odoo documentation
- Check module code in `models/` and `views/`
- Consult Odoo community forums

### Contributing
To enhance this module:
1. Fork the code
2. Make improvements
3. Test thoroughly
4. Submit changes

---

## Changelog

### Version 19.0.1.0.0
- Initial release for Odoo 19
- Added `x_contract_no` field to invoices
- Created custom tax invoice report template
- Compatible with Odoo 19.0

---

## FAQ

**Q: Can I use this with Odoo 18 or earlier?**  
A: No, this module is specifically for Odoo 19. Port the code for earlier versions.

**Q: Does it work with community edition?**  
A: Yes, fully compatible with Odoo Community Edition 19.

**Q: Can I customize the invoice layout?**  
A: Yes, edit `views/report_tax_invoice.xml` to modify the template.

**Q: Is the contract number field required?**  
A: No, it's optional. Leave blank if not needed.

**Q: Can I add more custom fields?**  
A: Yes, extend `models/account_move.py` and update the views.

**Q: Does it support multiple languages?**  
A: The interface inherits Odoo's language settings. Translate field labels as needed.

**Q: Is VAT calculation automatic?**  
A: Yes, Odoo's standard tax calculation applies. Configure taxes in Settings.

---

## License

This module is licensed under LGPL-3. See LICENSE file for details.

---

**Module**: Mermaid Tax Invoice (Odoo 19)  
**Version**: 19.0.1.0.0  
**Last Updated**: December 2025
