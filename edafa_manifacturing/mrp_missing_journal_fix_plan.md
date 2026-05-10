# Odoo MRP / Inventory Valuation “Missing Journal (journal_id)” – Work Log + Fix Plan

**Date:** 2026-01-28  
**Scope:** Manufacturing Orders (MRP) failing to generate valuation journal entries with error:  
> **Validation Error**: Missing required value for the field **Journal** (journal_id)  
> Model: **Journal Entry** (account.move)

---

## 1) Symptoms

- While confirming/processing MOs, Odoo tries to create a valuation **account.move**.
- The move creation fails because **journal_id is missing**.
- You noticed:
  - Some **Product Categories** had **Stock Account / Stock Journal** empty.
  - If valuation-related fields are cleared (so Odoo skips postings), “everything works”.

**Note:** Clearing valuation accounts is a workaround that disables proper accounting postings.

---

## 2) What we did (current state)

### A) Product Category configuration
We opened Product Category form (example: **stock meterial**) and checked **Account Properties**:

- Income Account
- Expense Account
- Stock Account
- Stock Journal

✅ Action taken:
- For **Stock Journal**, you chose **Miscellaneous Operations** from the journals list.
- You confirmed later that **all ~15 categories are filled** similarly now.

### B) Product side confirmation
Products show **Income/Expense: From Category** (so they inherit category accounts as expected).

---

## 3) Why the issue can still happen even when categories look “filled”

### Most likely root cause: **Multi-company property mismatch**
You are working in a **multi-company** setup (you had many companies enabled in the selector, e.g., “17/17”).

In Odoo, **accounting properties** (Stock Account / Stock Journal / valuation properties) are **company-dependent**.

So this can happen:
- You set Stock Journal for **Company A**
- The MO / stock move / accounting entry is being created under **Company B**
- For **Company B**, that property is effectively **empty**
- Result: **Missing journal_id** → Odoo blocks the entry creation

This matches your observation:
- “If we make it empty everything works” → because valuation postings are bypassed → no journal required.

---

## 4) Correction plan (fix the last point properly)

### Step 1 — Force correct company context before testing (critical)
1. Open the failing **Manufacturing Order**.
2. In the top-right company switcher, select **ONLY the MO company** (single company), NOT “all companies”.
3. Refresh the page.
4. Retry the same action (Confirm / Produce / Mark as Done).

✅ Expected:
- If multi-company mismatch is the cause, the error should disappear immediately.

---

### Step 2 — Validate the journal exists for that company
1. Go to **Accounting → Configuration → Journals**
2. Search: **Miscellaneous Operations**
3. Open it and verify:
   - **Company** = the same company you selected in Step 1
   - Journal is **Active**

If the journal belongs to a different company:
- Create/duplicate a journal for the correct company, then use that journal in categories.

---

### Step 3 — Re-save category properties under the correct company
1. Keep **single company** selected (Step 1).
2. Go to **Inventory → Configuration → Product Categories**
3. For each relevant category:
   - Set **Stock Journal** (the company-correct journal)
   - Set **Stock Account** (the company-correct account)
4. Save.

✅ Why:
- These are **company-dependent properties** and must be set while the right company is active.

---

### Step 4 — Validate the Stock Account itself
1. Go to **Accounting → Configuration → Chart of Accounts**
2. Open the **Stock Account** used in categories
3. Confirm:
   - Account is **Active**
   - **Company** matches
   - Type is appropriate (commonly Current Assets for stock valuation)

---

## 5) Quick control checks

### Check A — Does the error disappear after selecting 1 company?
- **Yes** → root cause confirmed: multi-company mismatch.
- **No** → then we check whether the journal/account is missing in locations or any custom logic.

### Check B — Are there locations influencing valuation?
Production/Stock Locations can have accounting/valuation-related settings (depends on setup).  
If category looks correct, we’ll inspect location settings next.

---

## 6) What NOT to do as a “final fix”
- Leaving valuation accounts empty permanently  
  - You’ll stop valuation journal entries and break inventory valuation in accounting.

---

## 7) Next step you should do now
Do **Step 1** on a failing MO (select only the MO company) and retry.  
Then send me:
- Did the “Missing Journal (journal_id)” error still appear?
- Which company name you selected?

