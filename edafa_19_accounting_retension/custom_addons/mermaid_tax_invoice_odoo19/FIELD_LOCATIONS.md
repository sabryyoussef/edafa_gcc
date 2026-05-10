# Where to See Retention and Performance Bond Fields

## 📍 Location 1: Invoice Form View

When you open an invoice (Accounting → Customers → Invoices → Open any invoice):

```
┌─────────────────────────────────────────┐
│ Invoice INV/2025/0001                   │
├─────────────────────────────────────────┤
│ Customer: Al-Majd Construction Co.      │
│ Contract No: CTR-2025-CONST-001         │ ← Contract Number field here
│                                         │
│ Invoice Lines:                          │
│ - Consulting Services    50,000 SAR     │
│ - Materials              75,000 SAR     │
├─────────────────────────────────────────┤
│                    TOTALS SECTION:      │
│                                         │
│ Subtotal:                 125,000 SAR   │
│ VAT (15%):                 18,750 SAR   │
│ ─────────────────────────────────────   │
│ Total:                    143,750 SAR   │
│ Amount Due:               143,750 SAR   │ ← This is amount_residual
│                                         │
│ Retention:                -10,000 SAR   │ ← NEW FIELD (in red)
│ Performance Bond:          -5,000 SAR   │ ← NEW FIELD (in red)
│ ═════════════════════════════════════   │
│ Net Amount:               128,750 SAR   │ ← NEW CALCULATED FIELD (bold)
└─────────────────────────────────────────┘
```

## 📍 Location 2: Printed Tax Invoice Report

When you print the invoice (Print → Tax Invoice):

```
┌────────────────────────────────────────────────────────┐
│        [YOUR COMPANY LOGO]                             │
│                                                        │
│  TAX INVOICE                                           │
│                                                        │
│  Invoice Date: 2025-12-07    Contract No: CTR-2025... │ ← Contract here
│  Due Date: 2025-01-06                                  │
│                                                        │
│  Invoice To:                                           │
│  Al-Majd Construction Co.                              │
│  King Fahd Road, Riyadh                                │
│  VAT: 310123456789003                                  │
│                                                        │
├────────────────────────────────────────────────────────┤
│  Description              Qty    Price      Amount     │
├────────────────────────────────────────────────────────┤
│  Consulting Services      10     5,000     50,000 SAR  │
│  Materials                 5    15,000     75,000 SAR  │
├────────────────────────────────────────────────────────┤
│                                                        │
│                           Subtotal:     125,000 SAR    │
│                           VAT (15%):     18,750 SAR    │
│                           ─────────────────────────    │
│                           Total:        143,750 SAR    │
│                                                        │
│                           Retention:    -10,000 SAR    │ ← RED TEXT
│                           Performance:   -5,000 SAR    │ ← RED TEXT
│                           ═════════════════════════    │
│                           Net Amount:   128,750 SAR    │ ← BOLD
└────────────────────────────────────────────────────────┘
```

## 🎨 Visual Styling

### In the Report (PDF):
- **Subtotal**: Normal black text
- **VAT**: Normal black text
- **Total**: Bold black text with border separator
- **Retention**: ⚠️ RED text (indicates deduction)
- **Performance Bond**: ⚠️ RED text (indicates deduction)
- **Net Amount**: BOLD black text with thick border separator

### Display Rules:
- **Retention** row: Only shows if x_retention ≠ 0
- **Performance Bond** row: Only shows if x_performance_bond ≠ 0
- **Net Amount** row: Only shows if either retention OR performance bond exists
- If both are 0, invoice shows normal Total only

## 📊 Demo Data Examples

### Example 1: Invoice with BOTH deductions
```
Total:              143,750 SAR
Retention:          -10,000 SAR   (10% retention)
Performance Bond:    -5,000 SAR   (5% bond)
══════════════════════════════
Net Amount:         128,750 SAR   (what customer actually pays)
```

### Example 2: Invoice with ONLY Retention
```
Total:               44,850 SAR
Retention:           -2,875 SAR   (5% retention)
══════════════════════════════
Net Amount:          41,975 SAR
```

### Example 3: Invoice with ONLY Performance Bond
```
Total:               51,750 SAR
Performance Bond:    -1,725 SAR   (3% bond)
══════════════════════════════
Net Amount:          50,025 SAR
```

### Example 4: Standard Invoice (NO deductions)
```
Total:               57,500 SAR
(No additional lines shown - clean invoice)
```

## 🚀 How to View Demo Data

1. **Upgrade Module** with demo data:
   ```bash
   bash scripts/update_modules.sh mermaid_tax_invoice_odoo19
   ```

2. **Go to Invoices**:
   - Accounting → Customers → Invoices

3. **Find Demo Invoices**:
   - Search for "CTR-2025" in the contract number
   - You'll see 4 demo invoices

4. **Test Each Scenario**:
   - Open each invoice to see fields in form
   - Click **Print → Tax Invoice** to see PDF
   - Compare with examples above

## 📝 Field Details

| Field Name         | Type      | Description                                    |
|--------------------|-----------|------------------------------------------------|
| x_contract_no      | Char      | Contract/PO reference number                   |
| x_retention        | Monetary  | Amount withheld as retention (entered manually)|
| x_performance_bond | Monetary  | Performance bond amount (entered manually)     |
| x_net_amount       | Computed  | Total - Retention - Performance Bond           |

## ✅ Next Steps

After upgrading the module, you should:
1. ✅ See Contract No field on invoice form (after customer field)
2. ✅ See Retention, Performance Bond, Net Amount in totals section
3. ✅ Print sample invoices to verify PDF layout
4. ✅ Confirm red text for deductions in PDF
5. ✅ Verify Net Amount auto-calculates correctly
