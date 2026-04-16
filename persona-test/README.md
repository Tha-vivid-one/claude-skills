# persona-test

A Claude Code skill that tests any product decision against 10 diverse simulated personas. Works for copy, headlines, UI patterns, feature names, pricing, onboarding flows, button labels — anything where you want signal from multiple perspectives before committing.

## Install

```bash
claude skill add --from Tha-vivid-one/claude-skills --subdirectory persona-test
```

## How it works

Three phases: **Generate** (or accept candidates), **Test** (against 10 personas across 3 dimensions), **Rank** (with deep-dive analysis on the top 5).

The default persona panel covers creative freelancers, working parents, startup founders, teachers, corporate executives, recent grads, small business owners, software engineers, real estate agents, and nurses — chosen for demographic and professional diversity.

Default dimensions: **Clarity**, **Desire**, **Premium Feel**. Both personas and dimensions are customizable.

## Usage

```
/persona-test "headline for welcome screen"
/persona-test --candidates "Connect, Enable, Unlock, Turn On" "button label"
/persona-test "onboarding copy" --dimensions "Warmth, Trust, Clarity" --personas "tech founders, enterprise buyers"
```

## What makes this different

1. **Structured diversity** — 10 personas catch blind spots a single perspective misses
2. **Quantified signal** — gut feelings become comparable numbers across dimensions
3. **Bimodal detection** — disagreements between personas reveal targeting decisions, not just averages

## Files

```
persona-test/
└── SKILL.md    # Core skill instructions
```

## License

MIT
