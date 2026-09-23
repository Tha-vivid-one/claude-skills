#!/usr/bin/env node
// Capture one screen state for /screen-review: a phone viewport, one or more themes, pixels plus facts about
// what is painted. No judgement here; the lenses judge.
//
//   node capture.mjs --out <dir> [--url http://localhost:5173] [--root <static dir>] [--route '#/settings']
//        [--do '<js that reaches the state>'] [--target '<css selector>'] [--themes dark,light]
//        [--seed '<js run before the app boots; THEME holds the theme name>'] [--expect '<regex of known console noise>']
//        [--size 375x812] [--wait 2500]
//
// Serves --root with a static server unless --url points at a running dev server. Each theme gets a fresh load:
// prefers-color-scheme is emulated as the theme name when it is dark or light, and --seed runs first (for apps
// that keep the theme, or a signed-in or onboarded flag, in localStorage), then the page loads again so the
// first paint already has it.
//
// Writes into <out>: base.<theme>.png (the route as it lands), state.<theme>.png (after --do),
// target.<theme>.png (the target's box), facts.<theme>.json, console.json. Needs Chrome (CHROME to override the
// path) and Node 22+ (global WebSocket).
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const route = arg('route', ''), doJs = arg('do', ''), target = arg('target', ''), seedJs = arg('seed', '');
const out = resolve(arg('out', 'screen-review-out')), devUrl = arg('url', ''), root = resolve(arg('root', '.'));
const [W, H] = arg('size', '375x812').split('x').map(Number), settle = Number(arg('wait', '2500'));
const themes = arg('themes', 'dark,light').split(',');
const expect = arg('expect', '') ? new RegExp(arg('expect')) : null;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
mkdirSync(out, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const port = 8600 + (process.pid % 300), dport = 9600 + (process.pid % 300);
const origin = devUrl ? new URL(devUrl).origin : `http://127.0.0.1:${port}`;
const profile = mkdtempSync(join(tmpdir(), 'screen-review-'));
const server = devUrl ? null : spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', root], { stdio: 'ignore' });
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${dport}`,
  '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--force-color-profile=srgb', `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });

// Runs in the page. Plain facts: every visible text run, every control, and whatever paints over the target.
const FACTS = (sel) => {
  const cv = document.createElement('canvas'); cv.width = cv.height = 1; const cx = cv.getContext('2d', { willReadFrequently: true });
  const rgba = (c) => { cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1); const d = cx.getImageData(0, 0, 1, 1).data; return [d[0], d[1], d[2], d[3] / 255]; };
  const over = (top, bot) => { const a = top[3]; return [0, 1, 2].map((i) => top[i] * a + bot[i] * (1 - a)).concat(1); };
  const lum = ([r, g, b]) => { const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return Math.round(((x + 0.05) / (y + 0.05)) * 100) / 100; };
  const R = (r) => ({ x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
  const tag = (el) => el.tagName.toLowerCase() + (el.id ? `#${el.id}` : '') + (el.classList.length ? '.' + [...el.classList].join('.') : '');
  const shown = (el) => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; } const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  // The colour behind an element: its ancestors' backgrounds composited, the page's own ground last.
  const ground = rgba(getComputedStyle(document.body).backgroundColor)[3] ? rgba(getComputedStyle(document.body).backgroundColor) : rgba(getComputedStyle(document.documentElement).backgroundColor);
  const behind = (el) => { const layers = []; let glass = false; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const s = getComputedStyle(e); const c = rgba(s.backgroundColor); if (c[3] > 0) layers.push(c); if (s.backdropFilter && s.backdropFilter !== 'none') glass = true; if (c[3] >= 1) break; } let bg = ground[3] ? ground : [0, 0, 0, 1]; for (const c of layers.reverse()) bg = over(c, bg); return { bg, glass: glass && layers.every((c) => c[3] < 1) }; };
  // Cut off by a scrolling or clipping ancestor, or by the viewport.
  const clipped = (el, r) => { for (let e = el.parentElement; e; e = e.parentElement) { const s = getComputedStyle(e); if (/(auto|scroll|hidden)/.test(s.overflowY)) { const c = e.getBoundingClientRect(); if (r.top < c.top - 1 || r.bottom > c.bottom + 1) return true; } } return r.bottom > innerHeight || r.top < 0; };
  const topAt = (x, y) => document.elementFromPoint(Math.min(innerWidth - 1, Math.max(0, x)), Math.min(innerHeight - 1, Math.max(0, y)));

  const scope = sel ? document.querySelector(sel) : document.body;
  if (!scope) return { error: `no element matches ${sel}` };
  const box = scope.getBoundingClientRect();

  const text = []; const seen = new Set();
  const walk = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.textContent.trim() ? 1 : 3) });
  for (let n; (n = walk.nextNode());) {
    const el = n.parentElement; if (!el || seen.has(el) || !shown(el)) continue; seen.add(el);
    const s = getComputedStyle(el); const rg = document.createRange(); rg.selectNodeContents(el); const r = rg.getBoundingClientRect();
    const fg = rgba(s.color); const { bg, glass } = behind(el); const ink = over(fg, bg);
    let op = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) op *= +getComputedStyle(e).opacity;
    text.push({ text: [...el.childNodes].filter((c) => c.nodeType === 3).map((c) => c.textContent).join('').trim().slice(0, 80), el: tag(el), box: R(r),
      font: `${s.fontWeight} ${s.fontSize}/${s.lineHeight} ${s.fontFamily.split(',')[0].replace(/["']/g, '')}`, tracking: s.letterSpacing, transform: s.textTransform,
      contrast: ratio(ink, bg), overGlass: glass || undefined, opacity: op < 1 ? Math.round(op * 100) / 100 : undefined, clipped: clipped(el, r) || undefined });
  }

  const controls = [...document.querySelectorAll('button, a[href], input, select, textarea, [role="button"], [role="switch"], [role="tab"], [role="radio"], [tabindex]:not([tabindex="-1"])')]
    .filter(shown).map((el) => {
      const r = el.getBoundingClientRect(); const t = topAt(r.x + r.width / 2, r.y + r.height / 2);
      const covered = t && !el.contains(t) && !t.contains(el) ? tag(t.closest('[class]') || t) : undefined;
      return { name: (el.getAttribute('aria-label') || el.innerText || el.value || '').trim().replace(/\s+/g, ' ').slice(0, 60), el: tag(el), box: R(r),
        small: r.width < 44 || r.height < 44 || undefined, inTarget: scope.contains(el) || undefined,
        pressed: el.getAttribute('aria-pressed') ?? undefined, checked: el.getAttribute('aria-checked') ?? undefined, expanded: el.getAttribute('aria-expanded') ?? undefined,
        disabled: el.disabled || undefined, coveredBy: covered, clipped: clipped(el, r) || undefined };
    });

  // Anything outside the target whose box crosses it, and which of the two paints on top there.
  const overlaps = sel ? [...document.body.querySelectorAll('*')].filter((el) => !scope.contains(el) && !el.contains(scope) && shown(el) && /fixed|absolute|sticky/.test(getComputedStyle(el).position))
    .map((el) => { const r = el.getBoundingClientRect(); const x = Math.max(r.left, box.left), y = Math.max(r.top, box.top), w = Math.min(r.right, box.right) - x, h = Math.min(r.bottom, box.bottom) - y;
      if (w <= 4 || h <= 4) return null; const t = topAt(x + w / 2, y + h / 2); return { el: tag(el), box: R(r), overlap: { x: Math.round(x), y: Math.round(y), w: Math.round(w), h: Math.round(h) }, onTop: t && scope.contains(t) ? 'target' : t && el.contains(t) ? 'this' : 'other' }; })
    .filter(Boolean).filter((o, i, a) => !a.some((p, j) => j < i && p.overlap.x === o.overlap.x && p.overlap.y === o.overlap.y && p.overlap.w === o.overlap.w)) : [];

  const uniq = (xs) => [...new Set(xs)].sort((a, b) => a - b);
  return { theme: document.documentElement.dataset.theme || null, viewport: `${innerWidth}x${innerHeight}`, target: sel ? { sel, box: R(box) } : null,
    summary: { fonts: [...new Set(text.map((t) => t.font))], leftEdges: uniq(text.map((t) => t.box.x)), rightEdges: uniq(text.map((t) => t.box.x + t.box.w)),
      lowContrast: text.filter((t) => t.contrast < 4.5).length, smallControls: controls.filter((c) => c.small).length, clippedText: text.filter((t) => t.clipped).length },
    text, controls, overlaps };
};

try {
  let tgt; for (let i = 0; i < 80 && !tgt; i++) { try { tgt = (await (await fetch(`http://127.0.0.1:${dport}/json/list`)).json()).find((t) => t.type === 'page'); } catch {} if (!tgt) await sleep(250); }
  if (!tgt) throw new Error(`headless Chrome did not start (${CHROME})`);
  const ws = new WebSocket(tgt.webSocketDebuggerUrl); await new Promise((r) => { ws.onopen = r; });
  let id = 0; const pending = new Map(); const logs = []; let theme = '';
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); return; }
    if (m.method === 'Runtime.consoleAPICalled' && /warn|error/.test(m.params.type)) logs.push({ theme, level: m.params.type, text: m.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300) });
    if (m.method === 'Runtime.exceptionThrown') logs.push({ theme, level: 'exception', text: (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 300) });
    if (m.method === 'Log.entryAdded' && /warn|error/.test(m.params.entry.level)) logs.push({ theme, level: m.params.entry.level, text: `${m.params.entry.text} ${m.params.entry.url || ''}`.slice(0, 300) });
  };
  const send = (method, params = {}) => new Promise((res, rej) => { const n = ++id; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, method, params })); });
  const run = async (expression) => { const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text); return r.result.value; };
  const shoot = async (file, clip) => { const s = await send('Page.captureScreenshot', { format: 'png', ...(clip ? { clip: { ...clip, scale: 1 } } : {}) }); writeFileSync(join(out, file), Buffer.from(s.data, 'base64')); };
  await send('Page.enable'); await send('Runtime.enable'); await send('Log.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: true });
  await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  for (theme of themes) {
    if (/^(dark|light)$/.test(theme)) await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: theme }] });
    await send('Page.navigate', { url: `${origin}/` });
    await sleep(600);
    if (seedJs) await run(`(async () => { const THEME = ${JSON.stringify(theme)}; ${seedJs} })()`);
    // A query makes this a new document: a hash-only change would keep whatever the app booted with.
    await send('Page.navigate', { url: `${origin}/?screen-review=${encodeURIComponent(theme)}${route}` });
    await sleep(settle);
    await shoot(`base.${theme}.png`);
    if (doJs) { await run(`(async () => { ${doJs} })()`); await sleep(1400); }
    await shoot(`state.${theme}.png`);
    const facts = await run(`(${FACTS})(${JSON.stringify(target)})`);
    if (target && facts.target) { const b = facts.target.box, m = 12; await shoot(`target.${theme}.png`, { x: Math.max(0, b.x - m), y: Math.max(0, b.y - m), width: Math.min(W, b.w + 2 * m), height: Math.min(H, b.h + 2 * m) }); }
    writeFileSync(join(out, `facts.${theme}.json`), JSON.stringify({ route, do: doJs || null, captureTheme: theme, ...facts }, null, 1));
    console.log(`${theme}: ${facts.error || `${facts.text.length} text runs, ${facts.controls.length} controls, ${facts.overlaps.length} overlaps`}`);
  }
  // Lines a capture produces that are not the app's fault, plus whatever --expect names for this project.
  for (const l of logs) {
    if (/navigator\.vibrate/.test(l.text)) l.expected = 'a scripted tap is not a user gesture';
    if (/favicon\.ico/.test(l.text)) l.expected = 'Chrome asks the bare origin for /favicon.ico';
    if (expect && expect.test(l.text)) l.expected = 'named by --expect';
  }
  writeFileSync(join(out, 'console.json'), JSON.stringify(logs, null, 1));
  console.log(`console: ${logs.filter((l) => !l.expected).length} unexpected warnings/errors · wrote ${out}`);
  ws.close();
} finally {
  // Chrome can still be writing its profile as it exits; wait for it, and never fail a finished capture over a temp folder.
  const gone = new Promise((r) => { chrome.once('exit', r); setTimeout(r, 3000); });
  chrome.kill(); server?.kill(); await gone;
  try { rmSync(profile, { recursive: true, force: true }); } catch {}
}
