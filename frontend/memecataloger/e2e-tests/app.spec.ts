import { test, expect } from '@playwright/test';


test('has title', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');
  await expect(page).toHaveTitle(/MemeCataloger/);
});

test('page header is visible', async ({page}) => {
  await page.goto('http://127.0.0.1:3000');
  await expect(page.getByText('MemeCataloger')).toBeVisible();
  await expect(page.getByText('MemeCataloger')).toHaveCount(1);
});

test('test thumbnails visible', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');
  await expect(page.getByRole('link')).toHaveCount(17);
});

test('thumbnails link to image page', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');
  await page.getByRole('link').first().click();
  await expect(page.getByRole('img')).toBeVisible();
  await expect(page.getByRole('img')).toHaveCount(1);
});
