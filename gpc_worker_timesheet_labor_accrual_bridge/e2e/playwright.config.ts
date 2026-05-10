import { defineConfig, devices } from "@playwright/test";

/**
 * Optional: numeric ir.actions.act_window id for Labor Accrual Batches.
 * Resolve with (Odoo shell): env.ref('gpc_hr_timesheet_labor_accrual.action_labor_accrual_batch').id
 */
if (!process.env.GCC_ODOO_LABOR_ACCRUAL_ACTION_ID) {
  process.env.GCC_ODOO_LABOR_ACCRUAL_ACTION_ID = "";
}

const baseURL =
  process.env.GCC_ODOO_WEB_URL ||
  process.env.GCC_ODOO_BASE_URL ||
  process.env.ODOO_URL ||
  "http://localhost:8119";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: [["list"], ["html", { open: "never" }]],
  timeout: 120_000,
  expect: { timeout: 30_000 },
  use: {
    baseURL: baseURL.replace(/\/$/, ""),
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "off",
    actionTimeout: 30_000,
    navigationTimeout: 60_000,
    locale: "en-US",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
