# Odoo 19 Module Plan — Project Invoicing with Advance, Retention & Journal

This plan defines an Odoo 19 module that covers:
- **EXPLAINED.md** (current folder): down payment in a dedicated account, two invoices with advance deduction (e.g. 50k + 50k), retention, performance bond.
- **Invoice image (GCC Tax Invoice):** tax invoice layout with advance payment deduction, penalties & deductions, performance bond, retention 10%, VAT, contract/PO.
- **Journal image:** journal entry structure (Accounts Receivable, Retention, Performance Bonds, Advance Received, Deduction against invoice, VAT Output, Income From Projects).

Target: **Odoo 19**, with correct **journal creation** for each invoice.

---

## 1. Module Overview

| Item | Value |
|------|--------|
| **Technical name** | `project_invoice_advance` (or `gcc_project_invoice`) |
| **Version** | 19.0.1.0.0 |
| **Category** | Invoicing / Accounting |
| **Dependencies** | `account`, `sale` (optional, if linked to SO/project) |

**Scope:**
- Extend **customer invoices** with: advance payment deduction, penalties & deductions, performance bond, retention % and amount.
- Use a **dedicated account** for advance/down payment (not reserve), per EXPLAINED.md.
- **Create journal entries** that match the provided journal layout (debit/credit per account type).
- Support **contract/PO reference** and **invoice reference** as on the tax invoice.

---

## 2. Invoice Fields (from Tax Invoice Image + EXPLAINED.md)

Extend **`account.move`** (customer invoice) with the following. Map to existing Odoo fields where possible; add only what is missing.

### 2.1 Header / Reference (from invoice image)

| Field | Odoo / New | Source | Notes |
|-------|------------|--------|------|
| TAX INVOICE NO. | `name` (existing) | Image | Invoice number |
| Date | `invoice_date` (existing) | Image | |
| Due Date | `invoice_date_due` (existing) | Image | Payment terms |
| Currency | `currency_id` (existing) | Image | e.g. SAR |
| Contract No | **New:** `contract_ref` (Char) | Image | e.g. MC-21323 |
| PO No | **New:** `po_ref` (Char) or link to `purchase.order` | Image | e.g. MC-21323 |
| Inv Ref | **New:** `invoice_ref` (Char) | Image | Internal reference, can default to `name` |
| Covered Period | **New:** `covered_period` (Char) optional | Image | If needed |

### 2.2 Customer (from invoice image)

| Field | Odoo / New | Source | Notes |
|-------|------------|--------|------|
| Client Name | `partner_id` (existing) | Image | MERMAID GENERAL CONTRACTING COMPANY |
| Client ID | **New:** `partner_ref` (Char) on partner or on move | Image | e.g. C0002555 |
| Address | `partner_id.address` (existing) | Image | |
| VAT Number | `partner_id.vat` (existing) | Image | |

Use **res.partner** for customer; add optional **Customer Reference** (`ref` or custom `partner_ref`) if not present.

### 2.3 Line items (from invoice image)

Use **`account.move.line`** linked to **product/product template**:
- **Description:** e.g. "MOHD TUNA KHAN (PIPE FABRICATOR)" → product name or `name` on line.
- **Unit price:** `price_unit`
- **Quantity:** `quantity`
- **Taxable amount:** `quantity * price_unit` (before tax)
- **Tax:** 15% VAT → **account.tax** (15% VAT)
- **VAT amount** and **total** = computed by Odoo from tax configuration.

No structural change needed; ensure **15% VAT** tax exists and is used on invoice lines.

### 2.4 Deductions & totals (from invoice image + EXPLAINED.md)

These drive **journal creation** and must be stored on the invoice.

| Field | Odoo / New | Source | Notes |
|-------|------------|--------|------|
| **Gross Amount** | Computed | Image | Sum of line subtotals (taxable amount) |
| **Advance Payment Deduction** | **New:** `advance_payment_deduction` (Monetary) | Image + EXPLAINED | Amount to deduct from this invoice (e.g. 50,000). Dedicated account, not reserve. |
| **Penalties & Deductions** | **New:** `penalties_deductions` (Monetary) | Image | 120.00 in example; reduces payable |
| **Performance Bond** | **New:** `performance_bond_amount` (Monetary) | Image + EXPLAINED | Deduction; 0.00 in example |
| **Total Excluding VAT** | Computed | Image | Gross − Advance deduction − Penalties − Performance bond |
| **VAT Amount 15%** | From tax computation | Image | 15% of (Total Excluding VAT) or standard Odoo VAT on lines |
| **Retention 10%** | **New:** `retention_percent` (Float) + `retention_amount` (Monetary) | Image + EXPLAINED | 10% retention; can be 0.00. Liability until released. |
| **Net Total** | Computed | Image | Total Excl. VAT + VAT − Retention (or as per local rule) |

**Business rule (EXPLAINED.md):** Advance (down payment) is stored in a **dedicated account** (e.g. Advance Received From Customers). When posting an invoice, **advance_payment_deduction** reduces the amount due and is applied against that account (so the journal debits Advance Received and credits A/R or offsets revenue).

**Computation order (aligned with image):**
1. Gross = sum of line taxable amounts  
2. Total after deductions = Gross − Advance deduction − Penalties − Performance bond  
3. VAT 15% on that total (or on lines, depending on tax setup)  
4. Retention 10% (if applicable)  
5. Net Total = Total Excl. VAT + VAT − Retention  

---

## 3. Chart of Accounts & Journal Structure (from Journal Image)

Define or map these **account types** and use them in the module’s journal logic.

| Account (from journal image) | Type / Usage | Debit/Credit in journal | Odoo account type (suggested) |
|------------------------------|-------------|--------------------------|-------------------------------|
| **Accounts Receivable** | Customer balance to collect | Debit | Receivable |
| **RETENTION FROM PROJECTS - NON ARAMCO 10%** | 10% retention (liability until release) | Debit (increases asset / retention receivable) or Credit (liability) depending on POV | Current Asset or Current Liability |
| **PERFORMANCE BONDS RECEIVABLE** | Performance bond amount | Debit | Current Asset |
| **ADVANCE RECEIVED FROM CUSTOMERS** | Down payment / advance (EXPLAINED: dedicated account) | Credit when received; **Debit** when deducting from invoice | Current Liability |
| **Deduction against invoice** | Penalties & deductions | Debit (expense or reduction of revenue) | Expense or contra-revenue |
| **VAT Output** | VAT on sales | Credit | Tax Payable |
| **INCOME FROM PROJECTS** | Revenue from project invoices | Credit | Income |

**Journal entry pattern (per invoice) — aligned with image and EXPLAINED:**

When posting a **customer invoice** that has:
- Advance payment deduction
- Penalties & deductions
- Performance bond
- Retention 10%

Suggested **journal items** (one invoice):

| Account | Partner | Debit | Credit |
|---------|---------|-------|--------|
| Accounts Receivable | Customer | Net Total (or amount receivable) | |
| Retention (10%) | Customer | retention_amount | |
| Performance Bonds Receivable | Customer | performance_bond_amount | |
| Advance Received From Customers | (or Customer) | advance_payment_deduction | |
| Deduction against invoice | | penalties_deductions | |
| VAT Output | | | vat_amount |
| INCOME FROM PROJECTS | | | Total Excluding VAT (or gross − deductions) |

Totals: **Total Debit = Total Credit**. Exact sign (debit/credit) for retention and performance bond depends on whether they are stored as receivable (debit) or liability (credit); the image shows Retention and Performance Bonds as **Debit**, so they are treated as **receivables** (amounts to be collected later). Advance Received is **Debit** in the image when it’s being **reduced** (deduction from invoice).

The plan will assume:
- **Advance Received From Customers:** Credit on receipt of advance; **Debit** when applying advance deduction on invoice (reducing the liability).
- **Retention 10%:** Debit to Retention account (receivable), Credit to A/R or separate clearing so net receivable = Net Total − retention.
- **Performance bond:** Debit to Performance Bonds Receivable when applicable.
- **Penalties & deductions:** Debit to “Deduction against invoice” (expense/contra), reducing net revenue.

---

## 4. Configuration (Company / CoA)

### 4.1 Accounts (to create or link via configuration)

Add a **settings** or **company** configuration (e.g. `res.config.settings` or custom model) to store:

| Configuration field | Purpose |
|--------------------|---------|
| **Advance Received Account** | Dedicated account for down payment (EXPLAINED: not reserve) |
| **Retention 10% Account** | e.g. “RETENTION FROM PROJECTS - NON ARAMCO 10%” |
| **Performance Bonds Receivable Account** | Performance bond receivable |
| **Deduction against invoice Account** | Penalties & deductions expense/contra account |
| **VAT Output Account** | 15% VAT output (usually from tax definition) |
| **Income From Projects Account** | Revenue account for project invoices |

These can be **company-dependent** and linked to **account.account**.

### 4.2 Tax

- **15% VAT:** One **account.tax** record for 15% VAT (SAR or multi-currency), used on invoice lines. VAT amount on invoice = from Odoo tax computation; ensure it matches “VAT Amount 15%” (e.g. 15% of Total Excluding VAT).

---

## 5. Technical Implementation Plan

### 5.1 Models

| Model | Extension / New | Purpose |
|-------|------------------|---------|
| **account.move** | Extend | Add: `contract_ref`, `po_ref`, `invoice_ref`, `advance_payment_deduction`, `penalties_deductions`, `performance_bond_amount`, `retention_percent`, `retention_amount`, optional `covered_period`. Add computed: `gross_amount`, `total_excluding_vat`, `net_total` (or use existing totals and adjust). |
| **account.move.line** | Use as-is or minimal extend | Invoice lines; ensure product and 15% tax. |
| **res.company** or **res.config.settings** | Extend | Store default accounts: advance, retention, performance bond, deduction, income (project). |
| **res.partner** | Optional extend | Add `partner_ref` (e.g. C0002555) if not using `ref`. |

### 5.2 Invoice form view

- Add a **group** or **section** “Project / Deductions” with:
  - Contract No, PO No, Inv Ref
  - Advance Payment Deduction
  - Penalties & Deductions
  - Performance Bond
  - Retention % and Retention Amount
- Optionally show computed: Gross, Total Excl. VAT, VAT, Net Total (or rely on Odoo’s standard totals if you override computation).

### 5.3 Journal entry creation (core logic)

- **Override** or **extend** the method that creates journal items when the invoice is **posted** (e.g. `account.move` `_post()` or the method that creates `account.move.line` for the invoice).
- **Logic:**
  1. Create standard Odoo invoice lines (revenue + VAT) if not already created.
  2. **Apply advance deduction:** Debit **Advance Received From Customers** (reduce liability), Credit **Accounts Receivable** (or reduce revenue by same amount depending on desired effect). EXPLAINED: advance is used to reduce amount due on this invoice.
  3. **Apply penalties/deductions:** Debit **Deduction against invoice** account, Credit **Accounts Receivable** (or reduce revenue).
  4. **Apply performance bond:** Debit **Performance Bonds Receivable**, Credit **Accounts Receivable** (or similar so net A/R is correct).
  5. **Apply retention 10%:** Debit **Retention (10%)** account, Credit **Accounts Receivable** so that net receivable = Net Total − retention.
  6. **Resulting A/R:** Should equal **Net Total** (or the amount the customer actually owes). Ensure **VAT Output** and **Income From Projects** (revenue) credits match the invoice totals.

Ensure **debits = credits** for the whole move. Reuse Odoo’s existing logic where possible (e.g. automatic A/R and revenue lines) and **add** only the extra lines for advance, retention, performance bond, and penalties.

### 5.4 Down payment (advance) receipt (EXPLAINED.md)

- When the **customer pays an advance** (e.g. 100,000 at 10% of 1M project):
  - Record in **Advance Received From Customers** (Credit) and Bank/Cash (Debit).
- Optionally: add a **“Register advance”** wizard or a specific **payment** type that credits **Advance Received From Customers** and links to the project/contract, so that when you post the first and second invoice you can **deduct** 50,000 + 50,000 from that account (as in EXPLAINED.md).

### 5.5 Reports / Print (Tax Invoice)

- **Invoice report** (e.g. QWeb): extend or duplicate standard invoice report to include:
  - Contract No, PO No, Inv Ref, Covered Period
  - Line table with Unit price, Qty, Taxable amount, Tax %, VAT amount, Total
  - Gross Amount, Advance Payment Deduction, Penalties & Deductions, Performance Bond, Total Excluding VAT, VAT Amount 15%, Retention 10%, Net Total
  - Net Total in words (e.g. SAR SIX THOUSAND FOUR HUNDRED EIGHTY SIX ONLY)
  - Bank details (from company/partner bank)

---

## 6. Implementation Checklist (order of work)

1. **Module scaffold:** `project_invoice_advance` for Odoo 19, manifest, dependencies `account` (+ optional `sale`).
2. **Accounts:** Define or map in CoA: Advance Received, Retention 10%, Performance Bonds Receivable, Deduction against invoice, Income From Projects, VAT Output (or use tax’s account).
3. **Company settings:** Add configuration fields for the above accounts (and optionally default retention %).
4. **account.move:** Add all new fields; add constraints (e.g. advance_deduction ≥ 0, retention ≥ 0).
5. **Computed totals:** Implement or hook Gross, Total Excl. VAT, Net Total, Retention amount from %.
6. **Invoice form view:** New section “Project / Deductions” with all new fields.
7. **Journal creation:** Implement posting logic so that:
   - Advance deduction debits Advance Received and reduces A/R/revenue as per design.
   - Penalties debit Deduction account.
   - Performance bond debits Performance Bonds Receivable.
   - Retention debits Retention account and reduces A/R.
   - Revenue and VAT credits match invoice.
8. **Advance receipt:** Optional wizard or payment type to record advance in Advance Received From Customers and link to partner/contract.
9. **Tax:** Ensure 15% VAT exists and is used on invoice lines; reconcile with “VAT Amount 15%” on report.
10. **Invoice report:** Extend QWeb report with contract/PO/ref, deduction block, totals, net in words, bank details.
11. **Testing:** Create invoice matching the tax invoice image (line, amounts, deductions); post and compare journal to the journal image (debits = credits, same account types).
12. **EXPLAINED.md flow:** Test 1M project, 100k advance in dedicated account; two invoices each with 50k advance deduction; retention/performance bond if needed.

---

## 7. Summary Table (Invoice → Journal)

| Invoice field / concept | Journal effect |
|-------------------------|----------------|
| **Gross (line subtotals)** | Revenue credit (Income From Projects) |
| **Advance Payment Deduction** | Debit Advance Received From Customers; reduce A/R or revenue |
| **Penalties & Deductions** | Debit Deduction against invoice; reduce A/R |
| **Performance Bond** | Debit Performance Bonds Receivable; reduce A/R |
| **Retention 10%** | Debit Retention account; reduce A/R |
| **VAT 15%** | Credit VAT Output |
| **Net Total** | Accounts Receivable Debit (amount customer owes) |

This plan covers the points from **current/EXPLAINED.md** (down payment account, two invoices with 50k+50k deduction) and the two invoice/journal images, with journal creation for **Odoo 19**.
