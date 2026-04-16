# claude-skills

A collection of Claude Code skills for prompt engineering, browser automation, spec-driven development, and persona-based testing.

## Skills

| Skill | Directory | Description |
|-------|-----------|-------------|
| [prompt-engineer](#prompt-engineer) | `prompt-engineer/` | Turn rough descriptions into production-quality system prompts via interview + test-driven refinement |
| [browse](#browse) | `browse/` | Browser automation with persistent authenticated sessions (Playwright + real Chrome) |
| [spec-kit](#spec-kit) | `spec-kit/` | Spec-Driven Development (SDD) — structured feature planning with Constitution > Specify > Plan > Tasks > Implement phases |
| [persona-test](#persona-test) | `persona-test/` | Test any design, copy, UX, or product decision against 10 simulated user personas |

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

## License

MIT
