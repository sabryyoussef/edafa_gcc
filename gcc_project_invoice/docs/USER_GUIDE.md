# GCC Project Invoice - User Guide
this is link for canva presentation https://www.canva.com/design/DAHAvN53heY/o5vuGPUMJq1EHOn6NJD37g/edit?utm_content=DAHAvN53heY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
## 📖 Overview

The GCC Project Invoice module now includes comprehensive project management with automated down payment handling. This guide provides step-by-step instructions for using the new project-based invoicing features with real-world use cases.

**Odoo 19 Compatibility**: This module has been updated for Odoo 19 compatibility. Some advanced view features (kanban views, custom search filters) are temporarily simplified to ensure stable operation while maintaining all core functionality.

## 🎯 Key Features

- **Project-Based Invoicing** - Link invoices to specific construction projects
- **Down Payment Management** - Track and automatically deduct advance payments
- **Financial Monitoring** - Real-time project financial status and progress tracking
- **Automated Reconciliation** - Automatic matching of down payments with invoice deductions
- **Multi-Project Support** - Handle multiple projects with different payment terms

---

## 🚀 Getting Started

### Initial Setup

1. **Install the Module**
   - Go to `Apps` → Search "GCC Project Invoice"
   - Click `Install` (Project module will be automatically installed)

2. **Configure Accounting Settings**
   - Navigate to `Accounting` → `Configuration` → `Settings`
   - Scroll to "GCC Project Invoice" section
   - Configure required accounts:
     - Advance Received From Customers
     - Retention Receivable
     - Performance Bonds Receivable
     - Deduction Against Invoice

3. **Enable Project Features**
   - Go to `Project` → `Configuration` → `Settings`
   - Ensure project management is enabled

---

## 📋 Use Case 1: New Construction Project Setup

### Scenario
ABC Construction Company wins a contract to build a shopping mall worth **1,000,000 LE** with **30% down payment** required upfront.

### Step-by-Step Process

#### 1. Create the Project

1. Navigate to `Project` → `Projects` → `Create`
2. Fill in project details:
   ```
   Project Name: Shopping Mall Construction - Phase 1
   Customer: XYZ Development Ltd
   Project Manager: [Select manager]
   ```

3. Configure financial settings:
   ```
   Project Total Value: 1,000,000 LE
   ☑ Enable Down Payment
   Down Payment %: 30%
   ```
   
4. **System automatically calculates**: Expected Down Payment = **300,000 LE**

#### 2. Record Down Payment Receipt

1. In the project form, click the **"Down Payments & Invoicing"** tab
2. Click **"Add Down Payment"** button
3. Enter payment details:
   ```
   Amount: 300,000 LE
   Date Received: [Select date]
   Payment Reference: BANK-TRF-2024-001
   Description: Initial down payment for mall construction
   ```

4. Click **"Confirm"** to activate the down payment

#### 3. Monitor Project Status

The project dashboard now shows:
- **Project Value**: 1,000,000 LE
- **Down Payments**: 300,000 LE (Available: 300,000 LE)
- **Invoiced**: 0 LE
- **Remaining**: 1,000,000 LE

---

## 📋 Use Case 2: Progressive Invoicing with Down Payment Deduction

### Scenario
Continue from Use Case 1. Now invoice the first construction phase worth **400,000 LE** and automatically deduct from the down payment.

### Step-by-Step Process

#### 1. Create Invoice from Project

1. In the project form, click **"Create Invoice"** button
2. Or go to `Accounting` → `Customers` → `Invoices` → `Create`

#### 2. Configure Invoice

1. Select customer and add invoice lines:
   ```
   Customer: XYZ Development Ltd
   Product: Construction Services - Foundation
   Quantity: 1
   Unit Price: 400,000 LE
   ```

2. **Select Project**:
   ```
   Related Project: Shopping Mall Construction - Phase 1
   ☑ Auto-deduct Down Payment (enabled by default)
   ```

3. **System automatically populates**:
   ```
   Available Down Payment: 300,000 LE
   Down Payment to Deduct: 300,000 LE
   Advance Payment Deduction: 300,000 LE
   ```

#### 3. Review Financial Summary

Before posting, review the summary:
```
Gross (Untaxed): 400,000 LE
Total Deductions: 300,000 LE (advance payment)
Tax Base After Deductions: 100,000 LE
Amount Tax: 15,000 LE (15% VAT on 100k)
Amount Total: 415,000 LE
Net Collect Now: 115,000 LE (what customer pays)
```

#### 4. Post Invoice

1. Click **"Post"** to finalize the invoice
2. **System automatically**:
   - Creates journal entries for advance deduction
   - Reconciles 300,000 LE from down payment balance
   - Updates project financial status

#### 5. Verify Results

**Project Status After Invoice**:
- **Project Value**: 1,000,000 LE
- **Down Payments**: 300,000 LE (Available: 0 LE - fully used)
- **Invoiced**: 400,000 LE  
- **Remaining**: 600,000 LE

**Customer Payment Required**: 115,000 LE (instead of full 415,000 LE)

---

## 📋 Use Case 3: Multiple Down Payments Management

### Scenario
Customer makes an additional down payment of **200,000 LE** for the next phase before invoicing.

### Step-by-Step Process

#### 1. Record Additional Down Payment

1. Go to project → **"Down Payments & Invoicing"** tab
2. Click **"Add Down Payment"**
3. Enter details:
   ```
   Amount: 200,000 LE
   Date Received: [Current date]
   Payment Reference: BANK-TRF-2024-002
   Description: Additional payment for Phase 2
   ```

#### 2. Create Second Invoice

1. Create new invoice:
   ```
   Customer: XYZ Development Ltd
   Product: Construction Services - Structure Work
   Quantity: 1
   Unit Price: 350,000 LE
   Related Project: Shopping Mall Construction - Phase 1
   ```

2. **System shows**:
   ```
   Available Down Payment: 200,000 LE
   Down Payment to Deduct: 200,000 LE (auto-populated)
   ```

3. **Optional**: Adjust deduction amount if needed (e.g., use only 150,000 LE)

#### 3. Progressive Project Tracking

**After Second Invoice**:
- **Total Invoiced**: 750,000 LE (400k + 350k)
- **Total Down Payments Used**: 500,000 LE (300k + 200k)
- **Remaining Project Balance**: 250,000 LE
- **Available Down Payment**: 0 LE (if fully used)

---

## 📋 Use Case 4: Handling Partial Down Payment Usage

### Scenario
Use only part of available down payment balance in an invoice, saving the rest for later phases.

### Step-by-Step Process

#### 1. Create Invoice with Partial Deduction

1. Create invoice for **150,000 LE** service
2. Available down payment: **200,000 LE**
3. **Manually adjust**:
   ```
   Down Payment to Deduct: 100,000 LE (instead of full 200k)
   Advance Payment Deduction: 100,000 LE
   ```

#### 2. Results

- **Invoice Total**: 172,500 LE (150k + VAT)
- **Customer Pays**: 72,500 LE (172.5k - 100k advance)
- **Remaining Down Payment**: 100,000 LE (still available for future invoices)

---

## 📋 Use Case 5: Project Without Down Payment

### Scenario
Handle a time-and-materials project without upfront down payment, using only retention and penalties.

### Step-by-Step Process

#### 1. Create Project

```
Project Name: Office Renovation - Building A
Customer: Corporate Client Ltd
Project Total Value: 500,000 LE
☐ Enable Down Payment (unchecked)
```

#### 2. Create Invoice with Other Deductions

```
Product: Renovation Services
Unit Price: 200,000 LE
Related Project: Office Renovation - Building A
Auto-deduct Down Payment: N/A (no down payments)

Manual Deductions:
- Retention %: 10% = 20,000 LE
- Performance Bond: 10,000 LE
- Penalties & Deductions: 5,000 LE
```

#### 3. Financial Summary

```
Gross (Untaxed): 200,000 LE
Total Deductions: 35,000 LE (retention + bond + penalties)
Tax Base After Deductions: 165,000 LE
Amount Tax: 24,750 LE (15% VAT)
Amount Total: 224,750 LE
Net Collect Now: 189,750 LE
```

---

## 🔍 Monitoring and Reports

### Project Dashboard

Access via `Project` → `Projects` → **Kanban View**

Each project card shows:
- **Progress Bar**: Visual completion percentage
- **Financial Summary**: Quick overview of key amounts
- **Quick Actions**: Create invoice, add down payment
- **Status Indicators**: Color-coded project health

### Down Payment Management

Access via `Project` → `Down Payments`

**Current Features**:
- **List View**: Table format showing all down payments with key details
- **Form View**: Detailed editing and viewing of individual down payments
- **Usage Tracking**: Monitor which invoices used which payments through form view
- **Remaining Balances**: View available amounts in list and form views
- **Basic Search**: Use the search bar to find payments by project, customer, or reference

**Note**: Advanced filtering and kanban views are temporarily unavailable due to Odoo 19 compatibility. Basic search functionality is available through the standard search bar.

### Financial Reports

**Smart Buttons on Project**:
- **📋 Invoices**: View all project invoices with status
- **💰 Down Payments**: Manage project down payments
- **📊 Financial Summary**: Detailed project financial report

---

## ⚠️ Validation and Controls

### Automatic Validations

The system prevents common errors:

1. **Over-deduction Prevention**
   ```
   Error: "Cannot deduct 150,000 LE from project down payments. 
   Available balance: 100,000 LE"
   ```

2. **Customer Mismatch Protection**
   ```
   Error: "Invoice customer (ABC Ltd) must match 
   project customer (XYZ Ltd)."
   ```

3. **Negative Amount Prevention**
   ```
   Error: "Down payment amount must be positive."
   ```

### Best Practices

1. **Always confirm down payments** before creating invoices
2. **Review available balance** before setting deduction amounts
3. **Use project-specific references** for easy tracking
4. **Monitor project progress** regularly through dashboard
5. **Reconcile payments** promptly after receipt

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. Down Payment Not Showing in Invoice

**Problem**: Available down payment shows 0 LE despite having confirmed payments

**Solutions**:
- Verify down payment state is "Confirmed" (not Draft)
- Check if down payment has already been fully reconciled
- Ensure invoice project matches down payment project
- Confirm customer consistency between project and invoice

#### 2. Cannot Cancel Down Payment

**Problem**: Error when trying to cancel down payment

**Solutions**:
- Check if down payment has been used in posted invoices
- First reverse/cancel related invoices if needed
- Contact system administrator for reconciliation cleanup

#### 3. Incorrect Financial Calculations

**Problem**: Project totals don't match expectations

**Solutions**:
- Refresh project data (F5 or navigate away and back)
- Check for draft invoices not yet posted
- Verify all invoices are linked to correct project
- Review currency conversion if multi-currency

#### 4. Auto-deduction Not Working

**Problem**: Advance payment deduction not auto-populated

**Solutions**:
- Ensure "Auto-deduct Down Payment" checkbox is enabled
- Verify project has confirmed down payments with available balance
- Check if project customer matches invoice customer
- Try manually triggering with project selection change

#### 5. Limited Down Payment View Options

**Problem**: Cannot find advanced filtering or kanban view for down payments

**Solution**: 
- Advanced views are temporarily unavailable due to Odoo 19 compatibility updates
- Use the list view with basic search functionality
- Access detailed information through individual form views
- Future updates will restore advanced filtering capabilities

---

## 📞 Support and Training

### Getting Help

1. **Documentation**: Review this guide and module README
2. **System Administrator**: Contact your Odoo administrator
3. **Training**: Request user training session for advanced features
4. **Community**: Odoo community forums for general questions

### Advanced Features

For advanced usage scenarios:
- Multi-currency projects
- Complex retention schemes  
- Custom deduction types
- Integration with other modules
- Automated workflows

**Current Status**: Advanced down payment views (kanban, custom filters) are being redesigned for Odoo 19 compatibility. Core functionality remains fully available through list and form views.

Contact your system administrator for configuration and training.

---

## 📈 Benefits Summary

### For Project Managers
- **Real-time financial visibility** into project status
- **Automated down payment tracking** reduces manual work  
- **Progress monitoring** through project dashboard
- **Quick actions** for invoice creation and payment management

### For Accounting Team  
- **Automated reconciliation** reduces errors
- **Consistent deduction handling** across all projects
- **Complete audit trail** for all down payment usage
- **Seamless integration** with existing accounting workflows

### For Management
- **Project portfolio overview** with financial metrics
- **Cash flow visibility** from down payment pipeline
- **Performance tracking** against project budgets
- **Standardized processes** across all projects
- **Odoo 19 compatibility** ensures future-proof operation

---

*This user guide covers the most common scenarios. For additional use cases or customization needs, consult with your system administrator or Odoo implementation partner.*