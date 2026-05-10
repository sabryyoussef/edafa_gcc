# Labor Accrual Bridge — Playwright E2E

Smoke test: log in, open **Labor Accrual Batches**, open a batch if present, assert **Populate lines** is visible.

## Prerequisites

- Node.js 18+
- Playwright browsers: `npx playwright install chromium`

## Environment

Set variables in your shell (or `set -a; source ../../../.env; set +a` from `e2e/`):

| Variable | Description |
|----------|-------------|
| `GCC_ODOO_WEB_URL` | Base URL (no trailing slash), e.g. `http://localhost:8119` |
| `GCC_ODOO_LOGIN` | User login |
| `GCC_ODOO_PASSWORD` | Password |
| `GCC_ODOO_DB` | Optional database name |
| `GCC_ODOO_LABOR_ACCRUAL_ACTION_ID` | Optional numeric action id for direct navigation |

Resolve action id in Odoo shell:

```python
env.ref('gpc_hr_timesheet_labor_accrual.action_labor_accrual_batch').id
```

## Run

**Recommended** if `npm install` fails on your filesystem (chmod/rename errors on `node_modules`):

```bash
cd projects/edafaa_gcc_clone/gpc_worker_timesheet_labor_accrual_bridge/e2e
chmod +x run.sh
export GCC_ODOO_LOGIN=... GCC_ODOO_PASSWORD=... GCC_ODOO_WEB_URL=http://localhost:8119
./run.sh
```

Standard (install under `e2e/`):

```bash
cd projects/edafaa_gcc_clone/gpc_worker_timesheet_labor_accrual_bridge/e2e
npm install
npx playwright install chromium
npx playwright test
```

Headed:

```bash
npm run test:headed
```

## Notes

- The user must belong to **Accounting / Billing** (or equivalent) so **Labor Accrual Batches** and **Populate lines** are available.
- Menu labels differ by locale; adjust selectors in `tests/labor-accrual-batch.spec.ts` if needed.
