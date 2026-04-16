---
name: browse
description: Browse websites using Playwright with persistent authenticated sessions. Use when asked to check X/Twitter, browse a URL, take a screenshot, extract web content, or interact with sites requiring login. Also use when cron tasks need web content from authenticated sources.
allowed-tools: Bash, Read, Write
---

# Browse

Browse any website using a persistent Playwright session with real Chrome. Authenticated sessions (X, Reddit, etc.) are preserved across runs.

## Tool Location

```
node browser.js <action> <url> [args]
```

## Actions

| Action | Usage | Returns |
|--------|-------|---------|
| `navigate` | `navigate <url>` | Page text content |
| `screenshot` | `screenshot <url> [output.png]` | Screenshot path |
| `extract` | `extract <url> <css_selector>` | JSON array of matched element texts |
| `evaluate` | `evaluate <url> <js_expression>` | JS evaluation result |
| `html` | `html <url> [css_selector]` | Raw HTML |

## Examples

```bash
# Read X timeline
node browser.js navigate "https://x.com/home"

# Screenshot a specific profile
node browser.js screenshot "https://x.com/elonmusk" screenshot.png

# Extract all tweet texts from a profile
node browser.js extract "https://x.com/elonmusk" "article [data-testid='tweetText']"

# Get page HTML for parsing
node browser.js html "https://x.com/search?q=polymarket" "main"
```

## Setup

### Prerequisites

- **Google Chrome** installed (real Chrome, not Chromium)
- **Node.js** 18+
- **Playwright** (`npm install playwright`)

### First Login (Interactive)

For sites requiring authentication, run in headed mode to log in manually:

```bash
BROWSER_HEADLESS=false node browser.js navigate "https://x.com/login"
```

A Chrome window will open. Log in, then close the window. The session is saved and all future headless runs will be authenticated.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_USER_DATA_DIR` | `~/.browse-skill/browser-data` | Persistent session storage |
| `BROWSER_HEADLESS` | `true` | Set `false` for visible browser |
| `BROWSER_TIMEOUT` | `30000` | Navigation timeout (ms) |

## Critical Details

- **Must use real Chrome** (`channel: 'chrome'`). Playwright's bundled Chromium gets blocked by X/Twitter and other anti-bot sites.
- SingletonLock is auto-cleared before each launch (handles stale headed sessions).
- Session data persists in `BROWSER_USER_DATA_DIR` — cookies, localStorage, login state all survive restarts.

## Gotchas

- X/Twitter never reaches `networkidle` — always use `domcontentloaded` or `load`.
- X splash screen needs ~5s to render feed. The tool waits for `article` elements automatically.
- If a login session expires, re-login via headed mode (see Setup above).
- Body text may be empty on JS-heavy SPAs — use `html` action + parse, or `evaluate` with custom JS.
- Close any headed Playwright windows before running headless (SingletonLock conflict).

## When NOT to Use

- Public APIs exist (crypto, weather, etc.) — use those directly.
- Simple HTML pages without JS — use a lightweight fetch instead.
- Sites with anti-bot that blocks even real Chrome — try stealth scraping tools.

## Claude Code Skill Integration

To use as a Claude Code skill, copy the `SKILL.md` and `browser.js` into your skills directory:

```bash
mkdir -p ~/.claude/skills/browse
cp SKILL.md browser.js ~/.claude/skills/browse/
```

Claude will automatically invoke this skill when you ask it to browse websites, check X, take screenshots, or extract web content.
