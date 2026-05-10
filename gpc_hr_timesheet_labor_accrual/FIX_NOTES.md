# Fix Notes — gpc_hr_timesheet_labor_accrual

## Fix: Analytic Distribution on Labor Accrual Journal Entry Lines

**Date:** 2026-05-10  
**Module version:** 19.0.1.0.0  
**Files changed:**
- `models/labor_accrual_batch.py`
- `tests/test_labor_accrual.py`

---

### Problem

When clicking **"Generate Draft Entry"** on a Labor Accrual Batch, the created
`account.move` always contained exactly **2 journal lines** (one debit, one credit),
both without any `analytic_distribution`. This meant:

- All timesheet lines from all projects collapsed into one single total debit line.
- The Analytic Distribution column on every journal item was empty.
- The client had to fill analytic accounts manually on each journal entry, which is
  error-prone and non-scalable.

---

### Root Cause

`_prepare_labor_accrual_move_vals` built a single aggregated debit line for the batch
total, with no `analytic_distribution` key in the move line vals dict.

---

### Fix

#### 1. New helper method — `_get_analytic_distribution_for_batch_line`

Added to `LaborAccrualBatch` in `models/labor_accrual_batch.py`.

Resolves the analytic distribution for a single `labor.accrual.batch.line` using
the following priority chain:

| Priority | Source | Field |
|----------|--------|-------|
| 1 | Timesheet line's own analytic account | `timesheet_line_id.account_id` |
| 2 | Project analytic account (Odoo 19) | `project_id.account_id` |
| 3 | None | Entry generated without analytic — no crash |

Returns `{"<account_id>": 100.0}` or `None`.

#### 2. Refactored `_prepare_labor_accrual_move_vals`

- Batch lines are now **grouped by analytic distribution key** before building the
  journal entry.
- Each unique analytic group produces its own **debit line** carrying
  `analytic_distribution`.
- Lines with no analytic account are grouped together into one debit line without
  `analytic_distribution`.
- The **credit (offset) line remains a single aggregated line** with no analytic —
  this is standard accounting practice for clearing/WIP accounts.

#### 3. Rounding guard

After rounding each group amount individually, the last group absorbs any rounding
difference so that `sum(debit lines) == credit line` to the cent.

---

### Behaviour Before vs After

| Scenario | Before | After |
|----------|--------|-------|
| 1 timesheet, project has analytic | 2 lines, no analytic | 2 lines, debit carries `{"<id>": 100.0}` |
| 2 timesheets, different projects | 2 lines, no analytic | 3 lines (1 debit/project + 1 credit) |
| 2 timesheets, same project | 2 lines, no analytic | 2 lines (grouped debit + 1 credit) |
| No analytic on timesheet or project | 2 lines, no analytic | 2 lines, no analytic — no error |
| Re-generate draft entry | Old move replaced | Old move replaced (unchanged) |
| Post / Reverse | Works normally | Works normally (unchanged) |

---

### Odoo 19 Field References Confirmed

| Field | Model | Confirmed |
|-------|-------|-----------|
| `analytic_distribution` | `account.move.line` | `fields.Json` — Odoo 19 native |
| `account_id` | `account.analytic.line` | Analytic account on timesheet line |
| `project_id` | `account.analytic.line` | Project on timesheet line |
| `task_id` | `account.analytic.line` | Task on timesheet line |
| `account_id` | `project.project` | Project's analytic account (Odoo 19) |

---

### Tests Added

New test class `TestLaborAccrualAnalyticDistribution` in
`tests/test_labor_accrual.py` covering:

| Test | What it verifies |
|------|-----------------|
| `test_helper_returns_ts_account_id_first` | Priority 1: timesheet `account_id` takes precedence |
| `test_helper_falls_back_to_project_account_id` | Priority 2: fallback to `project_id.account_id` |
| `test_helper_returns_none_when_no_analytic` | Priority 3: returns `None`, no crash |
| `test_single_project_analytic_on_debit_line` | Debit line has correct `analytic_distribution` |
| `test_no_analytic_entry_still_generated_no_crash` | Missing analytic → entry still created cleanly |
| `test_two_projects_produce_two_debit_lines_one_credit_line` | 2 projects → 2 debit lines, 1 credit |
| `test_two_lines_same_project_grouped_into_one_debit_line` | Same project → grouped into 1 debit line |
| `test_debit_always_equals_credit_multi_project` | Rounding guard: total debit always equals total credit |
| `test_regenerate_draft_replaces_old_move` | Re-generating replaces the old draft without duplication |

**Existing tests:** All pre-existing tests in `TestLaborAccrualPhase1` remain
unchanged and continue to pass. The `test_draft_move_created_balanced_linked`
test (which asserts `len(lines) == 2`) still passes because with a single
timesheet line there is exactly 1 debit group → 1 debit line + 1 credit line = 2.

---

### Not Changed

- `labor_accrual_batch_line.py` — no new fields added to the batch line model.
- `gpc_worker_timesheet_labor_accrual_bridge` — bridge module only overrides
  `action_populate_lines` and amount resolution; no changes needed.
- All views, security CSV, wizard, and menu files — untouched.
- Posted and reversed journal entries — the fix only affects newly generated
  **draft** entries via `action_generate_draft_move`.

---

### Decision Required (Finance)

**Credit / offset line analytic:** Currently the credit line carries no analytic
distribution (standard practice for clearing accounts). If the finance team
requires analytic tracking on the credit side as well, the same grouping logic
can be applied symmetrically to the credit lines. This is a one-line change in
`_prepare_labor_accrual_move_vals` and has not been implemented by default.
