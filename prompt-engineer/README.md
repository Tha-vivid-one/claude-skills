# prompt-engineer-skill

A Claude Code skill that turns rough descriptions into production-quality system prompts through structured interview, research, and test-driven refinement.

## Install

```bash
npx skills add Tha-vivid-one/prompt-engineer-skill
```

## What it does

Takes your vague idea, stream-of-consciousness rant, or existing prompt and turns it into a tight, tested system prompt. Works for CLAUDE.md files, API system prompts, SKILL.md instructions, agent configs, and heartbeat/cron prompts.

## Modes

| Mode | Trigger | What happens |
|------|---------|-------------|
| **Create** | "I need a prompt for..." | Interview → candidates → critique → synthesize → test |
| **Optimize** | "Fix this prompt..." | Diagnose weaknesses → targeted fixes → test |
| **Raw** | Passionate stream-of-consciousness | Extract signal from fire, mirror energy, move fast |
| **Heartbeat** | "Run every night and fix things" | Health checks, confidence gates, circuit breakers, reports |

## Methodology

Combines four proven approaches:

- **Test-Driven Prompting** (Amanda Askell, Anthropic) — write test cases first, then find the prompt that passes them
- **Multi-Candidate Synthesis** (PromptWizard, Microsoft) — generate 3-5 candidates, critique each, synthesize best parts
- **Harness Engineering** (Mitchell Hashimoto) — every failure becomes a permanent rule
- **Signal Discipline** (Boris Cherny) — ~2.5k token budget, every line must justify its existence

## Files

```
prompt-engineer-skill/
├── SKILL.md              # Core skill instructions (~230 lines)
├── references/
│   └── methodology.md    # Deep background on the four approaches
└── evals/
    └── evals.json        # Test cases for skill evaluation
```

## License

MIT
