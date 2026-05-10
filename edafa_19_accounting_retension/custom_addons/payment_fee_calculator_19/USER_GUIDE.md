# Payment Fee Calculator Module - User Guide

## Overview

The **Payment Method Fee Calculator** module automatically calculates payment processing fees for Saudi Arabian payment methods (Mada, Visa, and Mastercard) based on configurable fee structures. Fees are calculated exclusive of VAT and displayed on payment records.

---

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [How It Works](#how-it-works)
4. [Use Cases](#use-cases)
5. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Odoo 19.0
- `account` module (installed by default)
- `stock` module (installed by default)

### Installation Steps

1. **Copy Module to Addons Folder**
   ```bash
   cp -r payment_fee_calculator_19 /path/to/odoo/custom_addons/
   ```

2. **Update Apps List**
   - Go to **Apps** menu
   - Click on the **Update Apps List** (you may need to activate Developer Mode)
   - Click **Update**

3. **Install the Module**
   - In the **Apps** menu, search for "Payment Method Fee Calculator"
   - Click **Install**

4. **Verify Installation**
   - Navigate to **Accounting → Configuration → Journals**
   - Open any Bank or Cash journal
   - You should see a new section: "Payment Card Fees (Custom)"

---

## Configuration

### Setting Up Payment Fee Rates

1. **Navigate to Journal Configuration**
   - Go to **Accounting → Configuration → Journals**
   - Select a **Bank** or **Cash** journal (e.g., "Bank", "Mada Bank", "Visa Card")

2. **Configure Fee Settings**

   The module adds a new section called **"Payment Card Fees (Custom)"** with the following configurable fields:

   #### Visa & Mastercard Fee Configuration
   - **Visa & Mastercard Fee (%)**: Default is 2.5%
     - This is a flat percentage applied to all transaction amounts
     - Example: For a 1,000 SAR payment, the fee would be 25 SAR (1,000 × 2.5%)

   #### Mada Fee Configuration (Tiered Structure)
   - **Mada Fee Limit (SAR)**: Default is 5,000 SAR
     - This is the threshold that separates the two fee tiers
   
   - **< Limit Fee (%)**: Default is 0.8%
     - Applied to amounts **below** the limit
     - Example: For a 3,000 SAR payment, the fee would be 24 SAR (3,000 × 0.8%)
   
   - **>= Limit Fee (Fixed SAR)**: Default is 40 SAR
     - Applied to amounts **equal to or above** the limit
     - Example: For a 10,000 SAR payment, the fee would be 40 SAR (fixed)

3. **Save the Journal Configuration**

### Important Notes

- **Journal Naming Convention**: The module identifies payment methods by journal name:
  - Journals with "**Mada**" in the name → Uses Mada fee structure
  - Journals with "**Visa**" or "**Master**"/"**Mastercard**" in the name → Uses Visa/Mastercard fee structure
  - Other journals → No fee calculated

- **Case Insensitive**: Journal name matching is case-insensitive (e.g., "MADA", "mada", "Mada" all work)

---

## How It Works

### Automatic Fee Calculation

When you create or modify a payment record, the module automatically:

1. Checks the payment's journal name
2. Identifies the payment method (Mada, Visa/Mastercard, or Other)
3. Calculates the fee based on:
   - Payment amount
   - Journal configuration
   - Fee structure rules
4. Displays the calculated fee in the **"Calculated Fee (No VAT)"** field

### Fee Calculation Logic

```
IF Journal name contains "Visa" OR "Master":
    Fee = Amount × (Visa/Mastercard Fee % / 100)

ELSE IF Journal name contains "Mada":
    IF Amount >= Mada Fee Limit:
        Fee = Mada High Fee (Fixed)
    ELSE:
        Fee = Amount × (Mada Low Fee % / 100)

ELSE:
    Fee = 0
```

---

## Use Cases

### Use Case 1: Small Mada Transaction (Below Threshold)

**Scenario**: A customer pays 2,500 SAR using Mada card.

**Steps**:
1. Create a payment record
2. Select journal: "Mada Bank"
3. Enter amount: 2,500 SAR
4. **Result**: Fee automatically calculated = 20 SAR (2,500 × 0.8%)

**Configuration Used**:
- Mada Low Fee %: 0.8%
- Amount: 2,500 SAR (below 5,000 SAR limit)

---

### Use Case 2: Large Mada Transaction (Above Threshold)

**Scenario**: A customer pays 8,000 SAR using Mada card.

**Steps**:
1. Create a payment record
2. Select journal: "Mada Payment Gateway"
3. Enter amount: 8,000 SAR
4. **Result**: Fee automatically calculated = 40 SAR (fixed fee)

**Configuration Used**:
- Mada High Fee (Fixed): 40 SAR
- Amount: 8,000 SAR (≥ 5,000 SAR limit)

---

### Use Case 3: Visa/Mastercard Transaction

**Scenario**: A customer pays 15,000 SAR using Visa card.

**Steps**:
1. Create a payment record
2. Select journal: "Visa Card Account"
3. Enter amount: 15,000 SAR
4. **Result**: Fee automatically calculated = 375 SAR (15,000 × 2.5%)

**Configuration Used**:
- Visa/Mastercard Fee %: 2.5%
- Flat rate applies regardless of amount

---

### Use Case 4: Adjusting Default Fee Rates

**Scenario**: Your payment processor has new rates:
- Visa/Mastercard: 2.0% (down from 2.5%)
- Mada below limit: 0.6% (down from 0.8%)
- Mada above limit: 35 SAR (down from 40 SAR)

**Steps**:
1. Go to **Accounting → Configuration → Journals**
2. Open the relevant journal (e.g., "Visa Card Account")
3. Locate **"Payment Card Fees (Custom)"** section
4. Update the values:
   - Visa & Mastercard Fee: Change to **2.0**
   - Mada < Limit Fee: Change to **0.6**
   - Mada >= Limit Fee: Change to **35.0**
5. Click **Save**
6. All future payments will use the new rates

---

### Use Case 5: Multiple Journals with Different Rates

**Scenario**: You have different payment processors with different rates.

**Setup**:
1. **Journal 1**: "Mada - Processor A"
   - Mada Low Fee %: 0.8%
   - Mada High Fee: 40 SAR
   
2. **Journal 2**: "Mada - Processor B" (better rates)
   - Mada Low Fee %: 0.6%
   - Mada High Fee: 35 SAR

**Usage**:
- When creating payments, select the appropriate journal
- The system automatically applies the correct fee structure
- Each journal maintains its own independent configuration

---

### Use Case 6: Creating Payment with Fee Visibility

**Scenario**: Recording a customer payment and reviewing the fee.

**Steps**:
1. Navigate to **Accounting → Customers → Payments**
2. Click **Create**
3. Fill in payment details:
   - **Customer**: Select customer
   - **Amount**: 7,500 SAR
   - **Journal**: "Mada Bank"
   - **Payment Date**: Today
4. **Observe**: The "Calculated Fee (No VAT)" field automatically shows **40 SAR**
5. **Save** the payment

**Result**: 
- Payment recorded for 7,500 SAR
- Fee of 40 SAR is visible and stored
- Fee can be used for accounting entries, reports, or reconciliation

---

### Use Case 7: Comparing Fees Across Payment Methods

**Scenario**: Determine the most cost-effective payment method for a 4,000 SAR transaction.

**Comparison**:
1. **Mada Journal**: 4,000 SAR → Fee = 32 SAR (4,000 × 0.8%)
2. **Visa Journal**: 4,000 SAR → Fee = 100 SAR (4,000 × 2.5%)

**Decision**: Mada is more cost-effective for this amount (saves 68 SAR)

---

### Use Case 8: Threshold Analysis

**Scenario**: Understanding when Mada switches from percentage to fixed fee.

**Analysis**:
- **At 4,999 SAR**: Fee = 39.99 SAR (4,999 × 0.8%)
- **At 5,000 SAR**: Fee = 40 SAR (fixed, reached threshold)
- **At 10,000 SAR**: Fee = 40 SAR (fixed, still above threshold)

**Insight**: 
- For amounts just below 5,000 SAR, the percentage fee is cheaper
- For amounts at or above 5,000 SAR, the fixed 40 SAR fee is beneficial
- Break-even point: 5,000 SAR (where 0.8% = 40 SAR)

---

## Viewing Payment Fees

### In Payment Form

1. Navigate to **Accounting → Customers → Payments** or **Accounting → Vendors → Payments**
2. Open any payment record (or create a new one)
3. Look for the field: **"Calculated Fee (No VAT)"**
4. The fee is automatically calculated and displayed

### In Payment List View

You can add the fee column to the list view:
1. Go to payment list view
2. Click on the **settings icon** (gear icon)
3. Add **"Calculated Fee (No VAT)"** to visible columns
4. Compare fees across multiple payments

---

## Troubleshooting

### Issue 1: Fee is Not Being Calculated

**Possible Causes**:
1. Journal name doesn't contain keywords ("Mada", "Visa", "Master")
2. Journal type is not "Bank" or "Cash"
3. Payment amount is zero or empty

**Solution**:
- Verify journal name includes proper keywords
- Check journal type in journal configuration
- Ensure payment amount is filled

---

### Issue 2: Wrong Fee Amount

**Possible Causes**:
1. Incorrect fee configuration in journal
2. Wrong journal selected for payment method
3. Currency conversion issues

**Solution**:
- Review journal configuration: **Accounting → Configuration → Journals**
- Verify the correct journal is selected in the payment
- Check that payment amount and currency are correct

---

### Issue 3: Fee Field Not Visible

**Possible Causes**:
1. Module not properly installed
2. User permissions issue
3. View customization hiding the field

**Solution**:
- Verify module is installed: **Apps → Search "Payment Method Fee Calculator"**
- Check user has accounting access rights
- Clear browser cache and reload

---

### Issue 4: Installation Error

**Error**: `ValueError: External ID not found in the system: account.account_journal_form`

**Solution**: This error has been fixed in the latest version. If you encounter it:
1. Update to the latest version of the module
2. The correct external ID is now: `account.view_account_journal_form`
3. Reinstall the module

---

## Advanced Configuration

### Custom Fee Structures

If you need different fee structures, you can modify the journal configuration:

**Example**: Three-tier Mada structure
1. Keep the default two-tier system in the journal
2. Use reporting or custom code to implement additional logic
3. Or create multiple journals for different tiers

### Integration with Accounting

The calculated fee is stored and can be used for:
- **Expense Accounting**: Create journal entries to record fees as expenses
- **Reconciliation**: Match fees with bank statement charges
- **Reporting**: Analyze total fees paid per payment method
- **Budgeting**: Forecast payment processing costs

---

## Best Practices

1. **Consistent Naming**: Use clear, consistent names for journals
   - ✅ Good: "Mada Bank Account", "Visa Card Gateway"
   - ❌ Avoid: "Bank 1", "Payment Method A"

2. **Regular Review**: Review and update fee rates when processors change pricing

3. **Documentation**: Document which journal corresponds to which payment processor

4. **Testing**: Test fee calculations with sample payments before going live

5. **User Training**: Ensure accounting staff understand:
   - How fees are calculated
   - Which journal to use for each payment method
   - How to interpret the calculated fee field

6. **Audit Trail**: The fee is computed and stored, providing an audit trail for all payment costs

---

## Technical Notes

### Fee Calculation Timing
- Fees are calculated when:
  - Payment is created
  - Payment amount is changed
  - Payment journal is changed
- Calculation is automatic (no manual trigger needed)

### VAT Handling
- The module calculates fees **exclusive of VAT**
- If your fees include VAT, you'll need to account for it separately
- The field name explicitly states "No VAT" for clarity

### Currency Support
- Fees are calculated in the payment's currency
- Multi-currency is supported (respects payment currency)
- Default configuration uses SAR but works with any currency

---

## Support and Customization

For custom requirements or support:
- Review the module code in `models/account_payment.py` for calculation logic
- Modify `views/account_journal_views.xml` for UI customization
- Extend the module to add:
  - More payment methods
  - Additional fee tiers
  - Automated journal entries for fees
  - Custom reports

---

## Appendix: Quick Reference

### Default Fee Configuration

| Payment Method | Structure | Default Rate |
|---------------|-----------|--------------|
| Visa/Mastercard | Flat | 2.5% |
| Mada (< 5,000 SAR) | Percentage | 0.8% |
| Mada (≥ 5,000 SAR) | Fixed | 40 SAR |

### Journal Name Keywords

| Keyword | Payment Method |
|---------|---------------|
| mada | Mada |
| visa | Visa/Mastercard |
| master, mastercard | Visa/Mastercard |

### Fee Formula Reference

```
Visa/Mastercard: Fee = Amount × (Rate% / 100)

Mada:
  If Amount < Limit: Fee = Amount × (LowRate% / 100)
  If Amount ≥ Limit: Fee = FixedFee
```

---

**Module Version**: 19.0.1.0.0  
**Last Updated**: December 2025  
**License**: LGPL-3
