# browse-skill

A Claude Code skill for browser automation with persistent authenticated sessions. Uses Playwright with **real Chrome** (not bundled Chromium) to bypass anti-bot detection on sites like X/Twitter.

## Why?

Most browser automation tools use Playwright's bundled Chromium, which gets instantly detected and blocked by sites like X/Twitter, Reddit, and others with anti-bot measures. This skill uses your **real installed Chrome** browser via Playwright's `channel: 'chrome'` option, making it indistinguishable from a real user.

Sessions persist — log in once, browse forever.

## Quick Start

```bash
# Install
npm install

# Login to X (opens visible Chrome window)
BROWSER_HEADLESS=false node browser.js navigate "https://x.com/login"

# Now browse X headlessly
node browser.js navigate "https://x.com/home"
node browser.js screenshot "https://x.com/home" feed.png
node browser.js extract "https://x.com/home" "article [data-testid='tweetText']"
```

## Actions

| Action | Description |
|--------|-------------|
| `navigate <url>` | Get page text content |
| `screenshot <url> [file]` | Take a screenshot |
| `extract <url> <selector>` | Extract text from CSS-matched elements |
| `evaluate <url> <js>` | Run JavaScript on the page |
| `html <url> [selector]` | Get raw HTML |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_USER_DATA_DIR` | `~/.browse-skill/browser-data` | Where sessions are stored |
| `BROWSER_HEADLESS` | `true` | Set `false` for visible browser |
| `BROWSER_TIMEOUT` | `30000` | Navigation timeout (ms) |

## As a Claude Code Skill

Copy into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/browse
cp SKILL.md browser.js ~/.claude/skills/browse/
cd ~/.claude/skills/browse && npm install
```

Claude will auto-invoke this when you ask it to browse websites, check X, take screenshots, or extract content.

## Key Design Decisions

- **Real Chrome, not Chromium**: Sites like X detect and block Playwright's bundled Chromium. Using `channel: 'chrome'` with `ignoreDefaultArgs: ['--enable-automation']` makes the browser indistinguishable from manual browsing.
- **Persistent sessions**: User data dir stores cookies, localStorage, and login state. Log in once interactively, then all future headless runs are authenticated.
- **SingletonLock cleanup**: Headed sessions leave lock files that block headless runs. Auto-cleaned on every launch.
- **SPA-aware waits**: Waits for `article`, `main`, or `[role="main"]` elements before extracting content, handling JS-heavy SPAs like X.

## Gotchas

- **X never reaches `networkidle`** — it streams content forever. We use `domcontentloaded` + element selectors.
- **Close headed windows before headless runs** — or you'll hit a SingletonLock conflict.
- **Chrome must be installed** — this won't work with Chromium alone.
- **Session expiry** — if a site logs you out, re-run with `BROWSER_HEADLESS=false`.

## Requirements

- Google Chrome (installed on the system)
- Node.js 18+
- Playwright (`npm install`)

## License

MIT

<!--
## OPEN-SOURCE READINESS — PRIVATE INFO FLAGS

Before making this repo public, review the following:

1. **SKILL.md line about @tha_panoptic** — REMOVED in this version (was in the
   internal ductor copy). Clean.
2. **browser-data directory** — contains session cookies. NEVER commit this.
   It's in .gitignore.
3. **No API keys or tokens** in this repo.
4. **No personal paths** — all paths use ~ or env vars.
5. **No usernames/accounts** referenced in code.

STATUS: Ready for public release. No private information present.
-->
