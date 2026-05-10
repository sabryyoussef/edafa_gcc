# Custom Document Reports Module

This Odoo module provides custom report templates based on extracted PDF documents. The reports are designed to match real-world document formats used in business operations.

## Features

### Inventory Reports (Stock Pickings)
1. **Delivery Note (Custom)**
   - Customer and consignee information
   - Delivery note details with dates and references
   - Item list with quantities
   - Delivery mode and sales person information
   - Receipt confirmation section

2. **Packing List (Custom)**
   - Bilingual support (English/Arabic)
   - VAT information display
   - Applicant and company details
   - Packing list details with bank references
   - Item list with bilingual descriptions
   - Pack type and number of packs
   - Signature sections

### Accounting Reports (Customer Invoices)
1. **Tax Invoice (Custom)**
   - VAT number display (English/Arabic)
   - Buyer/customer information
   - Invoice details with dates
   - Itemized list with tax rates
   - Tax breakdown and totals
   - Contact information

2. **Commercial Invoice (Custom)**
   - Bilingual header (English/Arabic)
   - Applicant and beneficiary information
   - L/C (Letter of Credit) details section
   - Itemized goods/services list
   - Advance payment calculation
   - Shipping information (place of dispatch and destination)
   - Signature sections for both parties
   - Delivery confirmation statement

## Installation

1. Copy the `custom_document_reports` folder to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the module from the Apps menu

## Dependencies

- `account` - For invoice reports
- `stock` - For delivery note and packing list reports
- `sale` - For sales order integration

## Usage

### Delivery Note and Packing List
- Navigate to Inventory → Transfers
- Open any delivery/picking record
- Click "Print" and select:
  - "Delivery Note (Custom)" or
  - "Packing List (Custom)"

### Tax Invoice and Commercial Invoice
- Navigate to Accounting → Customers → Invoices
- Open any customer invoice
- Click "Print" and select:
  - "Tax Invoice (Custom)" or
  - "Commercial Invoice (Custom)"

## Module Structure

```
custom_document_reports/
├── __init__.py
├── __manifest__.py
├── README.md
├── reports/
│   ├── account_reports.xml    # Tax Invoice & Commercial Invoice
│   └── stock_reports.xml      # Delivery Note & Packing List
└── security/
    └── ir.model.access.csv
```

## Report Features

- **Bilingual Support**: Arabic and English text support
- **VAT Information**: Displays VAT numbers and tax breakdowns
- **Professional Layout**: Based on real business document formats
- **Complete Information**: Includes all relevant business details
- **Signature Sections**: Ready for manual signatures
- **Shipping Details**: Place of dispatch and destination information

## Notes

- Reports are based on extracted content from real PDF documents
- All monetary values use Odoo's currency formatting
- Dates are formatted according to Odoo's date widget
- Arabic text is properly displayed with RTL direction where needed

## Version

- Version: 18.0.1.0.0
- Compatible with: Odoo 18.0

## License

LGPL-3

