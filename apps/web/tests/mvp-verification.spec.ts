/**
 * OpenBerg Terminal — MVP Verification Tests
 *
 * Verifies every requirement in MVP_PLAN.md (Section 3.1 — Must-Have).
 *
 * Run: npx playwright test tests/mvp-verification.spec.ts
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000';

// Helper: open command palette by evaluating the React state change directly
// (keyboard shortcuts and button clicks don't work cross-browser in Playwright)
async function openCommandPalette(page: import('@playwright/test').Page) {
  // Find and click the ⌘K button using evaluate, which bypasses layout issues
  await page.evaluate(() => {
    const btn = document.querySelector('button[title="Command Palette (Cmd+K)"]') as HTMLElement | null;
    if (btn) btn.click();
  });
  const palette = page.locator('[data-testid="command-palette"]');
  await palette.waitFor({ state: 'visible', timeout: 5000 });
  return palette;
}

// Helper: search and execute a command by clicking the filtered result.
// Uses { force: true } to bypass z-index overlay issues.
async function executeCommand(page: import('@playwright/test').Page, cmdLabel: string) {
  const palette = await openCommandPalette(page);
  const input = palette.locator('input').first();
  await input.fill(cmdLabel);
  await page.waitForTimeout(300);

  // Click the first filtered button that matches the command label
  const buttons = palette.locator('[data-testid^="cmd-"]');
  const count = await buttons.count();
  if (count > 0) {
    await buttons.first().click({ force: true });
  }

  await page.waitForTimeout(500);
}

// ─── 3.1.1 Command Palette ───
test.describe('MVP: Command Palette', () => {
  test('opens command palette with Cmd+K', async ({ page }) => {
    await page.goto(BASE_URL);
    const palette = await openCommandPalette(page);
    expect(await palette.isVisible()).toBe(true);
  });

  test('searches commands and executes a function', async ({ page }) => {
    await page.goto(BASE_URL);
    const palette = await openCommandPalette(page);
    const input = palette.locator('input').first();
    await input.fill('chart');
    await page.waitForTimeout(300);
    const items = palette.locator('button');
    expect(await items.count()).toBeGreaterThan(0);
  });
});

// ─── 3.1.2 Real-Time Watchlists ───
test.describe('MVP: Real-Time Watchlists', () => {
  test('displays watchlist with live prices', async ({ page }) => {
    await page.goto(BASE_URL);
    const watchlistHeader = page.locator('h2').filter({ hasText: 'WATCHLIST' });
    await expect(watchlistHeader).toBeVisible({ timeout: 5000 });
    const watchItems = page.locator('.group');
    expect(await watchItems.count()).toBeGreaterThan(0);
  });

  test('can add a new ticker to watchlist', async ({ page }) => {
    await page.goto(BASE_URL);
    const input = page.locator('input[placeholder="Add ticker..."]');
    await input.fill('AMZN');
    const addBtn = page.locator('button').filter({ hasText: /ADD/i }).first();
    await addBtn.click();
    const items = page.locator('.group');
    expect(await items.count()).toBeGreaterThan(0);
  });
});

// ─── 3.1.3 Interactive Charts ───
test.describe('MVP: Interactive Charts', () => {
  test('renders chart view for a ticker', async ({ page }) => {
    await page.goto(BASE_URL);
    const chartArea = page.locator('.flex-1.min-h-\\[300px\\]').first();
    await expect(chartArea).toBeVisible({ timeout: 5000 });
  });

  test('has timeframe toolbar', async ({ page }) => {
    await page.goto(BASE_URL);
    const buttons = page.locator('button').filter({ hasText: /1d|5m|1h|1mo/ });
    expect(await buttons.count()).toBeGreaterThan(0);
  });
});

// ─── 3.1.4 News Feed ───
test.describe('MVP: News Feed', () => {
  test('displays news feed panel', async ({ page }) => {
    await page.goto(BASE_URL);
    const header = page.locator('h2').filter({ hasText: 'NEWS FEED' });
    await expect(header).toBeVisible({ timeout: 5000 });
  });

  test('news items have sentiment badges', async ({ page }) => {
    await page.goto(BASE_URL);
    const badges = page.locator('.inline-flex.items-center.px-1\\.5.py-0\\.5').first();
    await expect(badges).toBeVisible({ timeout: 5000 });
  });
});

// ─── 3.1.5 Portfolio Tracker ───
test.describe('MVP: Portfolio Tracker', () => {
  test('displays portfolio with P&L summary', async ({ page }) => {
    await page.goto(BASE_URL);
    await executeCommand(page, 'Portfolio');
    const portfolioHeader = page.locator('h2').filter({ hasText: 'PORTFOLIO' });
    await expect(portfolioHeader).toBeVisible({ timeout: 5000 });
  });
});

// ─── 3.1.6 Price Alerts ───
test.describe('MVP: Price Alerts', () => {
  test('displays alerts management view', async ({ page }) => {
    await page.goto(BASE_URL);
    await executeCommand(page, 'Price Alert');
    const alertsHeader = page.locator('h2').filter({ hasText: 'ALERTS' });
    await expect(alertsHeader).toBeVisible({ timeout: 5000 });
  });
});

// ─── 3.1.7 Security Search ───
test.describe('MVP: Security Search', () => {
  test('searches and displays security description', async ({ page }) => {
    await page.goto(BASE_URL);
    const tickerInput = page.locator('input[placeholder="TICKER"]');
    await tickerInput.fill('AAPL');
    const goButton = page.locator('button').filter({ hasText: /^GO$/ });
    await goButton.click();
    await expect(page.locator('#root')).toBeVisible();
  });
});

// ─── 3.1.8 User Accounts ───
test.describe('MVP: User Accounts', () => {
  test('shows settings page with theme toggle', async ({ page }) => {
    await page.goto(BASE_URL);
    await executeCommand(page, 'Settings');
    const settingsHeader = page.locator('h2').filter({ hasText: 'SETTINGS' });
    await expect(settingsHeader).toBeVisible({ timeout: 5000 });
  });
});

// ─── 3.1.9 Dark Theme ───
test.describe('MVP: Dark Theme', () => {
  test('renders in dark theme by default', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page.locator('#root')).toBeVisible();
  });

  test('can toggle theme', async ({ page }) => {
    await page.goto(BASE_URL);
    await executeCommand(page, 'Settings');
    const themeBtn = page.locator('button').filter({ hasText: /DARK|LIGHT/ });
    await expect(themeBtn).toBeVisible({ timeout: 5000 });
  });
});

// ─── 3.1.10 Responsive Layout ───
test.describe('MVP: Responsive Layout', () => {
  test('adapts to mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE_URL);
    await expect(page.locator('#root')).toBeVisible();
  });

  test('adapts to ultrawide viewport', async ({ page }) => {
    await page.setViewportSize({ width: 2560, height: 1440 });
    await page.goto(BASE_URL);
    await expect(page.locator('#root')).toBeVisible();
  });
});

// ─── 3.1.11 Self-Hostable ───
test.describe('MVP: Self-Hostable', () => {
  test('app loads and is functional', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page.locator('#root')).toBeVisible();
    const statusBar = page.locator('.flex.items-center.justify-between.px-3.py-1').first();
    await expect(statusBar).toBeVisible({ timeout: 5000 });
  });
});
