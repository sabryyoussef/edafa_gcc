# Demo Data Documentation

## Overview

This module includes comprehensive demo data to showcase the payment fee calculator functionality. The demo data is automatically loaded when you install the module with demo data enabled.

## What's Included

### Demo Journals (4 Payment Gateways)

1. **Mada Payment Gateway (Demo)** - Code: `MADA`
   - Mada Low Fee: 0.8%
   - Mada Threshold: 5,000 SAR
   - Mada High Fee: 40 SAR (fixed)

2. **Visa Card Account (Demo)** - Code: `VISA`
   - Visa/Mastercard Fee: 2.5%

3. **Mastercard Gateway (Demo)** - Code: `MCARD`
   - Visa/Mastercard Fee: 2.5%

4. **Mada Premium Processor (Demo)** - Code: `MADAP`
   - Mada Low Fee: 0.6% (better rate)
   - Mada Threshold: 5,000 SAR
   - Mada High Fee: 35 SAR (better rate)

### Demo Payments (10 Sample Transactions)

| # | Reference | Type | Amount (SAR) | Journal | Expected Fee | Description |
|---|-----------|------|--------------|---------|--------------|-------------|
| 1 | MADA-SMALL-001 | Customer | 2,500 | Mada | 20.00 | Below threshold |
| 2 | MADA-LARGE-001 | Customer | 8,000 | Mada | 40.00 | Above threshold (fixed) |
| 3 | VISA-001 | Customer | 15,000 | Visa | 375.00 | Standard Visa |
| 4 | MCARD-001 | Customer | 4,500 | Mastercard | 112.50 | Standard Mastercard |
| 5 | MADA-THRESHOLD-001 | Customer | 5,000 | Mada | 40.00 | Exactly at threshold |
| 6 | MADAP-SMALL-001 | Customer | 3,000 | Mada Premium | 18.00 | Premium processor - low |
| 7 | MADAP-LARGE-001 | Customer | 10,000 | Mada Premium | 35.00 | Premium processor - high |
| 8 | VISA-LARGE-001 | Customer | 25,000 | Visa | 625.00 | Large Visa transaction |
| 9 | MADA-BELOW-001 | Customer | 4,999 | Mada | 39.99 | Just below threshold |
| 10 | VISA-VENDOR-001 | Vendor | 7,500 | Visa | 187.50 | Outbound payment |

## How to Load Demo Data

### Method 1: Install with Demo Data (New Installation)

1. Before installing the module, ensure demo data is enabled:
   - Go to **Settings → Technical → System Parameters**
   - Or use command line:
   ```bash
   # Install module with demo data
   odoo-bin -d your_database -i payment_fee_calculator_19 --without-demo=False
   ```

2. In Odoo UI:
   - Go to **Apps**
   - Remove "Apps" filter
   - Search for "Payment Method Fee Calculator"
   - Click **Install**

### Method 2: Reinstall with Demo Data (Module Already Installed)

If the module is already installed without demo data:

1. Uninstall the module:
   - Go to **Apps**
   - Find "Payment Method Fee Calculator"
   - Click **Uninstall**

2. Enable demo data for the database (if not already enabled)

3. Reinstall the module

### Method 3: Manual Import (Advanced)

You can manually import the demo data files:

1. Go to **Settings → Technical → Import Records**
2. Select model: `account.journal`
3. Import: `demo/account_journal_demo.xml`
4. Select model: `account.payment`
5. Import: `demo/account_payment_demo.xml`

## Exploring the Demo Data

### View Demo Journals

1. Go to **Accounting → Configuration → Journals**
2. Filter by "(Demo)" in the name
3. Open any journal to see the configured fees:
   - **Mada Payment Gateway (Demo)**: Standard Mada rates
   - **Visa Card Account (Demo)**: Standard Visa rates
   - **Mastercard Gateway (Demo)**: Standard Mastercard rates
   - **Mada Premium Processor (Demo)**: Better rates for comparison

### View Demo Payments

1. Go to **Accounting → Customers → Payments**
2. You'll see 9 customer payments with calculated fees
3. Go to **Accounting → Vendors → Payments**
4. You'll see 1 vendor payment with calculated fee

### Verify Fee Calculations

Open any demo payment and check the **"Calculated Fee (No VAT)"** field:

**Example Verification:**
- Payment: MADA-SMALL-001
- Amount: 2,500 SAR
- Journal: Mada Payment Gateway
- Expected Fee: 2,500 × 0.8% = **20.00 SAR** ✓

## Use Cases Demonstrated

### Use Case 1: Mada Tiered Pricing
Compare these payments to see the two-tier structure:
- **MADA-BELOW-001**: 4,999 SAR → 39.99 SAR fee (percentage)
- **MADA-THRESHOLD-001**: 5,000 SAR → 40.00 SAR fee (fixed)
- **MADA-LARGE-001**: 8,000 SAR → 40.00 SAR fee (fixed)

### Use Case 2: Payment Method Comparison
Compare fees for the same amount across different methods:
- For 3,000 SAR:
  - **MADAP-SMALL-001** (Mada Premium): 18.00 SAR (0.6%)
  - Visa would be: 75.00 SAR (2.5%)
  - Savings: 57.00 SAR by using Mada!

### Use Case 3: Processor Comparison
Compare standard vs premium Mada processors:
- For amounts < 5,000 SAR:
  - **Standard Mada**: 0.8% fee
  - **Premium Mada**: 0.6% fee
- For amounts ≥ 5,000 SAR:
  - **Standard Mada**: 40 SAR fixed
  - **Premium Mada**: 35 SAR fixed

### Use Case 4: Break-Even Analysis
See where the threshold makes a difference:
- **MADA-BELOW-001**: 4,999 SAR → 39.99 SAR
- **MADA-THRESHOLD-001**: 5,000 SAR → 40.00 SAR
- Break-even point: Exactly 5,000 SAR

### Use Case 5: High-Value Transactions
See how fees scale (or don't) with amount:
- **VISA-001**: 15,000 SAR → 375.00 SAR (2.5%)
- **VISA-LARGE-001**: 25,000 SAR → 625.00 SAR (2.5%)
- **MADA-LARGE-001**: 8,000 SAR → 40.00 SAR (fixed)
- **MADAP-LARGE-001**: 10,000 SAR → 35.00 SAR (fixed)

Insight: For large amounts, Mada's fixed fee is much cheaper than Visa's percentage!

## Testing Scenarios

### Scenario 1: Modify a Demo Payment
1. Open payment **MADA-SMALL-001** (2,500 SAR)
2. Current fee: 20.00 SAR
3. Change amount to 1,000 SAR
4. Fee auto-updates to: 8.00 SAR (1,000 × 0.8%)
5. Change amount to 6,000 SAR
6. Fee auto-updates to: 40.00 SAR (fixed, ≥ 5,000)

### Scenario 2: Change Payment Journal
1. Open payment **VISA-001** (15,000 SAR)
2. Current fee: 375.00 SAR (Visa @ 2.5%)
3. Change journal to **Mada Payment Gateway (Demo)**
4. Fee auto-updates to: 40.00 SAR (Mada fixed, ≥ 5,000)
5. Savings: 335.00 SAR!

### Scenario 3: Create New Payment Using Demo Journal
1. Go to **Accounting → Customers → Payments**
2. Click **Create**
3. Select journal: **Mada Payment Gateway (Demo)**
4. Enter amount: 3,500 SAR
5. Fee automatically calculated: 28.00 SAR (3,500 × 0.8%)

### Scenario 4: Compare All Payment Methods
Create a list view with these columns:
- Reference
- Amount
- Journal
- Calculated Fee
- Effective Rate (Fee/Amount × 100)

Sort by "Effective Rate" to see which payment method is most cost-effective for different amounts.

## Fee Calculation Summary

Based on the demo data:

| Amount Range | Mada Standard | Mada Premium | Visa/Mastercard |
|--------------|---------------|--------------|-----------------|
| 1,000 SAR | 8.00 (0.8%) | 6.00 (0.6%) | 25.00 (2.5%) |
| 2,500 SAR | 20.00 (0.8%) | 15.00 (0.6%) | 62.50 (2.5%) |
| 4,999 SAR | 39.99 (0.8%) | 29.99 (0.6%) | 124.98 (2.5%) |
| 5,000 SAR | 40.00 (fixed) | 35.00 (fixed) | 125.00 (2.5%) |
| 10,000 SAR | 40.00 (fixed) | 35.00 (fixed) | 250.00 (2.5%) |
| 25,000 SAR | 40.00 (fixed) | 35.00 (fixed) | 625.00 (2.5%) |

**Key Insights:**
- ✅ Mada is cheaper for all amounts
- ✅ Mada is significantly cheaper for amounts ≥ 5,000 SAR
- ✅ Mada Premium offers better rates than Standard Mada
- ✅ Break-even point: 1,600 SAR (where Mada 0.8% = Visa 2.5%)

## Cleanup Demo Data

To remove demo data:

### Option 1: Delete Individual Records
1. Go to **Accounting → Configuration → Journals**
2. Select journals with "(Demo)" in name
3. Click **Action → Delete**
4. Go to **Accounting → Customers/Vendors → Payments**
5. Filter by demo references (MADA-*, VISA-*, etc.)
6. Select and delete

### Option 2: Reinstall Without Demo Data
1. Uninstall the module
2. Ensure demo data is disabled in database settings
3. Reinstall the module

## Customizing Demo Data

To modify the demo data for your needs:

1. Edit files:
   - `demo/account_journal_demo.xml` - Add/modify journals
   - `demo/account_payment_demo.xml` - Add/modify payments

2. Update fee rates, thresholds, or add new journals

3. Upgrade the module:
   ```bash
   odoo-bin -d your_database -u payment_fee_calculator_19
   ```

## Support

For questions about demo data:
- Review the USER_GUIDE.md for detailed usage instructions
- Check the payment calculation logic in `models/account_payment.py`
- Verify journal configuration in `models/account_journal.py`

---

**Demo Data Version**: 19.0.1.0.0  
**Last Updated**: December 2025
