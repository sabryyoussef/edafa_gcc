import { test, expect } from "@playwright/test";

async function odooLogin(page: import("@playwright/test").Page) {
  const login =
    process.env.GCC_ODOO_LOGIN ||
    process.env.ODOO_LOGIN ||
    "";
  const password =
    process.env.GCC_ODOO_PASSWORD ||
    process.env.ODOO_PASSWORD ||
    "";
  const db =
    process.env.GCC_ODOO_DB ||
    process.env.ODOO_DB ||
    "";

  test.skip(!login || !password, "Set GCC_ODOO_LOGIN and GCC_ODOO_PASSWORD (e.g. via .env)");

  const loginPath = `/web/login${db ? `?db=${encodeURIComponent(db)}` : ""}`;
  await page.goto(loginPath);

  await page.locator('input[name="login"], input#login').first().fill(login);
  await page.locator('input[name="password"], input#password').first().fill(password);

  await page.getByRole("button", { name: /Log in|Sign in/i }).click();

  await expect(page.locator("body.o_web_client")).toBeVisible({ timeout: 90_000 });
}

/** Open Accounting app from home / app switcher (Odoo 16+). */
async function openAccountingApp(page: import("@playwright/test").Page) {
  await page.keyboard.press("Escape").catch(() => {});
  await page.waitForTimeout(300);

  const accountingOption = page.getByRole("option", { name: /^Accounting$/i }).first();
  const accountingLink = page.getByRole("link", { name: /Accounting|المحاسبة/i }).first();

  if ((await accountingOption.count()) > 0 && (await accountingOption.isVisible())) {
    await accountingOption.click();
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(1500);
    return;
  }
  if ((await accountingLink.count()) > 0 && (await accountingLink.isVisible())) {
    await accountingLink.click();
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(1500);
    return;
  }

  await page.goto("/web");
  await page.waitForTimeout(1000);
  const opt2 = page.getByRole("option", { name: /^Accounting$/i }).first();
  if ((await opt2.count()) > 0) {
    await opt2.click();
    await page.waitForLoadState("domcontentloaded");
    await page.waitForTimeout(1500);
  }
}

/**
 * Navigate to Labor Accrual Batches list:
 * - Prefer direct action URL if GCC_ODOO_LABOR_ACCRUAL_ACTION_ID is set.
 * - Else Accounting → Transactions → Labor Accrual Batches (menu label may vary by locale).
 */
async function openLaborAccrualBatches(page: import("@playwright/test").Page) {
  const actionId = process.env.GCC_ODOO_LABOR_ACCRUAL_ACTION_ID?.trim();
  if (actionId) {
    await page.goto(`/web#action=${encodeURIComponent(actionId)}`, {
      waitUntil: "domcontentloaded",
    });
    await page.waitForTimeout(2500);
    const listOrKanban = page.locator(".o_list_view, .o_kanban_view").first();
    if (await listOrKanban.isVisible().catch(() => false)) {
      return;
    }
  }

  await openAccountingApp(page);
  await page.keyboard.press("Escape").catch(() => {});
  await page.waitForTimeout(400);

  const transactionsRe = /Transactions|حركات|Accounting/i;
  const transactionsNav = page
    .getByRole("link", { name: transactionsRe })
    .or(page.getByRole("button", { name: transactionsRe }))
    .first();

  if (await transactionsNav.isVisible().catch(() => false)) {
    await transactionsNav.hover().catch(() => {});
    await transactionsNav.click({ timeout: 15_000 }).catch(() => {});
    await page.waitForTimeout(600);
  }

  const batchMenu = page
    .getByRole("menuitem", {
      name: /Labor Accrual Batches|دفعات استحقاق العمالة/i,
    })
    .first();

  await batchMenu.waitFor({ state: "visible", timeout: 25_000 });
  await batchMenu.click({ timeout: 15_000 });
  await page.waitForTimeout(2000);
}

test.describe("Labor Accrual Batch (bridge smoke)", () => {
  test("login and reach Labor Accrual Batches list or form", async ({ page }) => {
    await odooLogin(page);

    await openLaborAccrualBatches(page);

    const listView = page.locator(".o_list_view");
    const formView = page.locator(".o_form_view");
    const kanbanView = page.locator(".o_kanban_view");
    const hasList = await listView.isVisible().catch(() => false);
    const hasForm = await formView.isVisible().catch(() => false);
    const hasKanban = await kanbanView.isVisible().catch(() => false);

    expect(
      hasList || hasForm || hasKanban,
      "Expected list, kanban, or form after navigation",
    ).toBe(true);

    if (hasList || hasKanban) {
      const row = page.locator(".o_list_table tbody tr.o_data_row").first();
      if ((await row.count()) > 0) {
        await row.click();
        await page.waitForTimeout(2000);
      }
    }

    const populateBtn = page.getByRole("button", {
      name: /Populate lines|ملء البنود/i,
    });
    const onForm = await page.locator(".o_form_view").isVisible().catch(() => false);
    if (onForm) {
      await expect(populateBtn).toBeVisible({ timeout: 30_000 });
    } else {
      test.info().annotations.push({
        type: "note",
        description:
          "Stayed on list/kanban (no row opened or empty). Set GCC_ODOO_LABOR_ACCRUAL_ACTION_ID or create a draft batch to assert Populate lines.",
      });
    }
  });
});
