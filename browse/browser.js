#!/usr/bin/env node
/**
 * Browser tool — Playwright-based browser automation with persistent sessions.
 * Uses real Chrome (not bundled Chromium) to bypass anti-bot detection on sites
 * like X/Twitter, Reddit, etc. Login sessions persist across runs.
 *
 * Usage:
 *   node browser.js navigate <url>                    — navigate and return page text
 *   node browser.js screenshot <url> [output.png]     — screenshot a page
 *   node browser.js extract <url> <css_selector>      — extract text from elements matching selector
 *   node browser.js evaluate <url> <js_expression>    — run JS on a page and return result
 *   node browser.js html <url> [css_selector]         — return raw HTML (or inner HTML of selector)
 *
 * Env:
 *   BROWSER_USER_DATA_DIR — override user data dir (default: ~/.browse-skill/browser-data)
 *   BROWSER_HEADLESS      — set to "false" for headed mode (default: true)
 *   BROWSER_TIMEOUT       — navigation timeout ms (default: 30000)
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const os = require('os');

const USER_DATA_DIR = process.env.BROWSER_USER_DATA_DIR
  || path.join(os.homedir(), '.browse-skill', 'browser-data');
const HEADLESS = process.env.BROWSER_HEADLESS !== 'false';
const TIMEOUT = parseInt(process.env.BROWSER_TIMEOUT || '30000', 10);

// Ensure user data dir exists
fs.mkdirSync(USER_DATA_DIR, { recursive: true });

async function launchBrowser() {
  // Remove stale lock file if present (leftover from headed sessions)
  const lockFile = path.join(USER_DATA_DIR, 'SingletonLock');
  try { fs.unlinkSync(lockFile); } catch {}

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: HEADLESS,
    channel: 'chrome',
    viewport: { width: 1280, height: 900 },
    timeout: TIMEOUT,
    args: ['--disable-blink-features=AutomationControlled'],
    ignoreDefaultArgs: ['--enable-automation'],
  });
  const page = context.pages()[0] || await context.newPage();
  return { context, page };
}

async function navigate(url) {
  const { context, page } = await launchBrowser();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    await page.waitForSelector('article, main, [role="main"]', { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(3000);
    const text = await page.innerText('body').catch(() => '');
    const maxLen = 50000;
    console.log(text.length > maxLen ? text.slice(0, maxLen) + '\n\n[...truncated]' : text);
  } finally {
    await context.close();
  }
}

async function screenshot(url, outputPath) {
  const { context, page } = await launchBrowser();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    await page.waitForSelector('article, main, [role="main"]', { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(2000);
    const out = outputPath || 'screenshot.png';
    await page.screenshot({ path: out, fullPage: false });
    console.log(out);
  } finally {
    await context.close();
  }
}

async function extract(url, selector) {
  const { context, page } = await launchBrowser();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    await page.waitForTimeout(2000);
    const elements = await page.$$eval(selector, els => els.map(el => el.textContent.trim()));
    console.log(JSON.stringify(elements, null, 2));
  } finally {
    await context.close();
  }
}

async function evaluate(url, expression) {
  const { context, page } = await launchBrowser();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    await page.waitForTimeout(2000);
    const result = await page.evaluate(expression);
    console.log(typeof result === 'string' ? result : JSON.stringify(result, null, 2));
  } finally {
    await context.close();
  }
}

async function html(url, selector) {
  const { context, page } = await launchBrowser();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    await page.waitForTimeout(2000);
    let content;
    if (selector) {
      content = await page.$eval(selector, el => el.innerHTML).catch(() => 'Selector not found');
    } else {
      content = await page.content();
    }
    const maxLen = 50000;
    console.log(content.length > maxLen ? content.slice(0, maxLen) + '\n\n[...truncated]' : content);
  } finally {
    await context.close();
  }
}

async function main() {
  const [,, action, ...args] = process.argv;

  if (!action) {
    console.error('Usage: node browser.js <navigate|screenshot|extract|evaluate|html> <url> [args...]');
    process.exit(1);
  }

  switch (action) {
    case 'navigate':
      await navigate(args[0]);
      break;
    case 'screenshot':
      await screenshot(args[0], args[1]);
      break;
    case 'extract':
      await extract(args[0], args[1]);
      break;
    case 'evaluate':
      await evaluate(args[0], args[1]);
      break;
    case 'html':
      await html(args[0], args[1]);
      break;
    default:
      console.error(`Unknown action: ${action}`);
      process.exit(1);
  }
}

main().catch(err => {
  console.error(err.message);
  process.exit(1);
});
