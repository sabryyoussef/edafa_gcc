# Demo Data for Mermaid Tax Invoice Module

## Overview
This demo data provides sample invoices showcasing the retention and performance bond functionality.

## Demo Data Includes

### Customers
1. **Al-Majd Construction Co.** - Construction company in Riyadh
2. **Gulf Trading Est.** - Trading company in Jeddah

### Products
1. **Project Management Consulting** - Service @ 5,000 SAR/unit
2. **Premium Construction Materials** - Product @ 15,000 SAR/ton
3. **Heavy Equipment Rental** - Service @ 8,000 SAR/month

### Sample Invoices

#### Invoice 1: With Retention (10%) AND Performance Bond (5%)
- Customer: Al-Majd Construction Co.
- Contract: CTR-2025-CONST-001
- Line Items:
  - 10 × Consulting @ 5,000 SAR = 50,000 SAR
  - 5 × Materials @ 15,000 SAR = 75,000 SAR
- **Subtotal**: 125,000 SAR
- **VAT (15%)**: 18,750 SAR
- **Total**: 143,750 SAR
- **Retention**: -10,000 SAR
- **Performance Bond**: -5,000 SAR
- **Net Amount**: 128,750 SAR

#### Invoice 2: With Retention Only (5%)
- Customer: Gulf Trading Est.
- Contract: CTR-2025-TRADE-055
- Line Items:
  - 3 × Equipment Rental @ 8,000 SAR = 24,000 SAR
  - 5 × Consulting @ 3,000 SAR = 15,000 SAR
- **Subtotal**: 39,000 SAR
- **VAT (15%)**: 5,850 SAR
- **Total**: 44,850 SAR
- **Retention**: -2,875 SAR
- **Net Amount**: 41,975 SAR

#### Invoice 3: With Performance Bond Only (3%)
- Customer: Al-Majd Construction Co.
- Contract: CTR-2025-CONST-002
- Line Items:
  - 3 × Materials @ 15,000 SAR = 45,000 SAR
- **Subtotal**: 45,000 SAR
- **VAT (15%)**: 6,750 SAR
- **Total**: 51,750 SAR
- **Performance Bond**: -1,725 SAR
- **Net Amount**: 50,025 SAR

#### Invoice 4: Standard Invoice (No Retention/Bond)
- Customer: Gulf Trading Est.
- Contract: PO-2025-089
- Line Items:
  - 20 × Consulting @ 2,500 SAR = 50,000 SAR
- **Subtotal**: 50,000 SAR
- **VAT (15%)**: 7,500 SAR
- **Total**: 57,500 SAR
- **Net Amount**: 57,500 SAR (no deductions)

## How to View Demo Data

1. **Install/Upgrade Module** with demo data enabled
2. **Go to**: Accounting → Customers → Invoices
3. **Filter**: Look for invoices with "CTR-2025" or "PO-2025" in contract numbers
4. **Print Report**: Click Print → Tax Invoice to see retention/bond on PDF

## Testing Scenarios

### Scenario 1: View Retention and Performance Bond Fields
- Open Invoice #1 (CTR-2025-CONST-001)
- See retention and performance bond in totals section
- Net amount automatically calculated

### Scenario 2: Print Tax Invoice with Deductions
- Open any invoice with retention/bond
- Click **Print → Tax Invoice**
- PDF shows:
  - Total in black
  - Retention in red (if exists)
  - Performance Bond in red (if exists)
  - Net Amount in bold (if deductions exist)

### Scenario 3: Standard Invoice (No Deductions)
- Open Invoice #4 (PO-2025-089)
- No retention/bond fields shown
- Total = Net Amount
- Clean invoice format

## Notes
- Demo data uses `noupdate="1"` to avoid conflicts
- All amounts in SAR (Saudi Riyal)
- VAT at 15% (Saudi standard rate)
- Dates are relative to installation date
