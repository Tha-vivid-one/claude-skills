# claude-skills

A collection of Claude Code skills for prompt engineering, browser automation, spec-driven development, persona-based testing, and note distillation.

## Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| [prompt-engineer](#prompt-engineer) | `prompt-engineer/` | Turn rough descriptions into production-quality system prompts via interview + test-driven refinement |
| [browse](#browse) | `browse/` | Browser automation with persistent authenticated sessions (Playwright + real Chrome) |
| [spec-kit](#spec-kit) | `spec-kit/` | Spec-Driven Development (SDD) — structured feature planning with Constitution > Specify > Plan > Tasks > Implement phases |
| [persona-test](#persona-test) | `persona-test/` | Test any design, copy, UX, or product decision against 10 simulated user personas |
| [progressive-summary](#progressive-summary) | `progressive-summary/` | Lay a non-destructive bold/highlight "scan-layer" over a long note for fast rereads — never rewrites or summarizes |
| [map-feature](#map-feature) | `map-feature/` | Adversarial reality-check before building — reads the codebase, hunts for prior art, shows a current→proposed Mermaid diff, stops for approval before any code |
| [website-skills](#website-skills) | `website-skills/` | Scrollytelling suite — 7 skills to build, polish, debug, and adapt scroll-driven animated websites (GSAP / Lenis / ScrollTrigger) |

## Installation

Install individual skills by subdirectory:

```bash
# prompt-engineer
claude skill add --from Tha-vivid-one/claude-skills --subdirectory prompt-engineer

# browse
claude skill add --from Tha-vivid-one/claude-skills --subdirectory browse

# spec-kit
claude skill add --from Tha-vivid-one/claude-skills --subdirectory spec-kit

# persona-test
claude skill add --from Tha-vivid-one/claude-skills --subdirectory persona-test

# progressive-summary
claude skill add --from Tha-vivid-one/claude-skills --subdirectory progressive-summary

# map-feature
claude skill add --from Tha-vivid-one/claude-skills --subdirectory map-feature

# website-skills — a suite; install any sub-skill, e.g.:
claude skill add --from Tha-vivid-one/claude-skills --subdirectory website-skills/scrolly-skills/scrollytelling
```

Or install manually by copying a skill's directory into `~/.claude/skills/`.

---

## prompt-engineer

Turn rough descriptions into production-quality system prompts through structured interview, research, and test-driven refinement.

**Modes:**

| Mode | Trigger | What happens |
|------|---------|-------------|
| Create | "I need a prompt for..." | Interview, candidates, critique, synthesize, test |
| Optimize | "Fix this prompt..." | Diagnose weaknesses, targeted fixes, test |
| Raw | Passionate stream-of-consciousness | Extract signal, mirror energy, move fast |
| Heartbeat | "Run every night and fix things" | Health checks, confidence gates, circuit breakers |

**Methodology:** Combines Amanda Askell's Test-Driven Prompting, Microsoft's Multi-Candidate Synthesis (PromptWizard), Mitchell Hashimoto's Harness Engineering, and Boris Cherny's Signal Discipline.

```
prompt-engineer/
├── SKILL.md
├── README.md
├── references/methodology.md
└── evals/evals.json
```

---

## browse

Browser automation with persistent authenticated sessions. Uses Playwright with real Chrome (not bundled Chromium) to bypass anti-bot detection on sites like X/Twitter.

**Key features:**
- Real Chrome via `channel: 'chrome'` — indistinguishable from manual browsing
- Persistent sessions — log in once, browse forever
- SPA-aware waits for JS-heavy sites

**Actions:** `navigate`, `screenshot`, `extract`, `evaluate`, `html`

```
browse/
├── SKILL.md
├── README.md
├── browser.js
├── package.json
└── .gitignore
```

---

## spec-kit

Implements GitHub's [Spec-Driven Development](https://github.com/github/spec-kit) methodology. Write structured specifications first, then let those specs drive the implementation.

**Phases:**

| Phase | Output |
|-------|--------|
| Constitution | `constitution.md` — project principles and constraints |
| Specify | `specification.md` — what to build (not how) |
| Plan | `plan.md` — technical implementation strategy |
| Tasks | `tasks.md` — ordered, actionable steps with dependencies |
| Implement | Working code |

**Eval results:** 84% pass rate with skill loaded vs 36% without.

```
spec-kit/
├── SKILL.md
├── README.md
├── LICENSE
├── references/templates.md
└── evals/evals.json
```

---

## persona-test

Test any product decision against 10 diverse simulated personas. Works for copy, headlines, UI patterns, feature names, pricing, onboarding flows, button labels.

**Three phases:** Generate (or accept) candidates, Test against personas across dimensions, Rank with deep-dive analysis.

**Default personas:** Creative freelancer, working mom, startup founder, teacher, corporate executive, recent grad, small business owner, software engineer, real estate agent, nurse.

**Default dimensions:** Clarity, Desire, Premium Feel. All customizable via arguments.

```
persona-test/
├── SKILL.md
└── README.md
```

---

## progressive-summary

Lay a non-destructive "scan-layer" over a long note so a reread takes ~30 seconds instead of 20 minutes. Bold the load-bearing sentences, `==highlight==` the handful that are the essence — the note itself is never reworded, summarized, or restructured, just made scannable. AI-assisted progressive summarization (Tiago Forte's Distill layer).

**Three reading depths after a pass:**
- highlights only → the ~10-second essence
- highlights + bold → the full argument in ~30 seconds
- raw prose → only where a section earns it

**Deliberately opt-in** — it runs only on the specific note you point it at, never auto-fires, and never rewrites, splits, or extracts (the opposite of summarize/condense). Best on long transcripts, saved articles, and research dumps before a second read-through. Highlight syntax (`==...==`) renders in Obsidian and other Obsidian-flavored-markdown tools.

```
progressive-summary/
└── SKILL.md
```

---

## map-feature

Map what a feature actually touches **before** building it. Reads the existing codebase, hunts for prior art and reusable pieces, then shows a current→proposed architecture diff (Mermaid) with a reuse-first recommendation — and stops for approval before any code is written.

This is an adversarial reality-check against the current code, **not** a generative design doc (use a PRD skill for that). Use it before building any non-trivial feature, when you suspect the work is about to over-build or duplicate something that already exists, or to verify the right approach before committing days of effort.

**Triggers:** "map this feature", "before we build", "is there already something that does this", "what does this feature touch", "should I build this or reuse".

```
map-feature/
└── SKILL.md
```

---

## website-skills

A suite of 7 skills for building scroll-driven narrative ("scrollytelling") websites with GSAP, Lenis, and ScrollTrigger. They live under `website-skills/scrolly-skills/`.

| Skill | What it does |
|-------|--------------|
| `teach-scroll` | One-time setup — gathers scroll motion language + brand voice into persistent project guidelines |
| `scrollytelling` | Build a complete scroll-driven animated page from a brief (Lenis smooth scroll + ScrollTrigger) |
| `scroll-polish` | Final quality pass — timing, easing, spacing, and choreography that separate good from great |
| `scroll-overdrive` | Push past conventional limits — shader transitions, velocity-reactive visuals, WebGL, advanced parallax |
| `scroll-debug` | Diagnose & fix broken scroll animations — jank, hydration mismatches, ScrollTrigger/Lenis conflicts, mobile |
| `scroll-adapt` | Make the experience work across mobile / tablet / desktop without breaking animations |
| `scroll-normalize` | Enforce consistent motion language, easing, timing, and spacing across all sections |

Typical flow: `teach-scroll` once, then `scrollytelling` to build, then `scroll-polish` / `scroll-adapt` / `scroll-normalize` to refine and `scroll-debug` when something breaks.

```
website-skills/
└── scrolly-skills/
    ├── teach-scroll/
    ├── scrollytelling/
    ├── scroll-polish/
    ├── scroll-overdrive/
    ├── scroll-debug/
    ├── scroll-adapt/
    └── scroll-normalize/
```

---

## License

MIT
