# spec-kit-skill

A Claude Code skill that implements [GitHub's Spec-Driven Development](https://github.com/github/spec-kit) methodology. Instead of jumping into code, you write structured specifications first and let those specs drive the implementation.

## What it does

When you're about to build something non-trivial, this skill guides you through a phased workflow:

| Phase | What happens | Output |
|-------|-------------|--------|
| **Constitution** | Establish project principles and constraints | `constitution.md` |
| **Specify** | Define what to build (not how) -- user stories, acceptance criteria, edge cases | `specification.md` |
| **Plan** | Technical implementation strategy -- architecture, data models, API contracts | `plan.md` |
| **Tasks** | Ordered, actionable implementation steps with dependencies | `tasks.md` |
| **Implement** | Execute tasks against the spec | Working code |

Optional phases: **Clarify** (resolve ambiguities), **Analyze** (cross-check consistency), **Checklist** (quality validation).

The skill is smart about where to start -- it won't force you through Constitution if your project already has established conventions. It assesses context and picks the right entry point.

## Install

### Via skills CLI (recommended)

```bash
npx skills add Tha-vivid-one/spec-kit-skill -g
```

### Manual

Copy the skill directory to your Claude Code skills folder:

```bash
cp -r . ~/.claude/skills/spec-kit/
```

## Usage

### Direct invocation

```
/spec-kit <feature-name>
```

### Natural language (auto-triggers)

The skill activates when you say things like:
- "Let's plan this feature before we start coding"
- "Can you help me spec out the notification system?"
- "I need to break this down into tasks"
- "Write a spec for the onboarding flow"
- "I keep going back and forth on the architecture -- help me think this through"

### What you get

All spec artifacts are saved to `.specify/features/<feature-name>/` in your project:

```
.specify/
  features/
    offline-mode/
      constitution.md
      specification.md
      plan.md
      tasks.md
```

Each phase is reviewed with you before moving to the next. You control the pace and can skip phases that don't apply.

## When to use it

- Building a feature that touches multiple files or systems
- Requirements are unclear and you need to think before coding
- Handing off work to another developer or AI agent
- Going back and forth on architecture without making progress
- Starting a new project and want structure from the beginning

## When NOT to use it

- Bug fixes
- Simple refactors with obvious scope
- You explicitly want to vibe-code and iterate fast
- Trivial changes (rename a function, update copy)

## Eval results

We tested the skill across 5 realistic feature-planning scenarios, comparing Claude's output with the skill loaded vs without it.

| Metric | With Skill | Without Skill |
|--------|:---------:|:------------:|
| **Overall pass rate** | **84%** | **36%** |
| Follows phase structure | 5/5 | 0/5 |
| Picks correct starting phase | 5/5 | 0/5 |
| Asks targeted questions first | 4/5 | 3/5 |
| Produces structured output | 5/5 | 5/5 |
| References output file paths | 2/5 | 1/5 |

**Key finding:** Without the skill, Claude produces good advice but always mixes requirements with implementation details. The skill enforces the discipline of separating *what* from *how*, which catches requirement gaps before you're deep in code.

### Test scenarios used

1. Adding offline mode to an iOS app
2. Redesigning a trading bot's scanner architecture
3. Building a real-time P&L dashboard widget
4. Designing a user onboarding flow
5. Writing a contractor handoff document

## How it works

The skill uses Claude Code's [skills system](https://docs.anthropic.com/en/docs/claude-code/skills). The SKILL.md file contains the methodology and workflow instructions. When triggered, Claude reads the skill and follows the SDD phases, asking you targeted questions at each stage and producing structured output documents.

Reference templates for each phase's output format are in `references/templates.md` -- Claude reads these when it needs the exact document structure.

## Credits

- **Methodology**: [github/spec-kit](https://github.com/github/spec-kit) -- GitHub's open-source Spec-Driven Development toolkit. This skill captures the SDD methodology as a Claude Code skill, so you get the structured workflow without installing the CLI.
- **Co-authored with**: [Claude](https://claude.ai) (Opus 4.6) -- skill creation, eval framework, and documentation were built collaboratively using Claude Code with the [skill-creator](https://skills.sh/anthropics/skills/skill-creator) workflow.

## License

MIT
