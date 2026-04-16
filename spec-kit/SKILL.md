---
name: spec-kit
description: Guide users through Spec-Driven Development (SDD) to plan and implement software features with structured specifications. Use this skill whenever the user wants to plan a feature, spec something out, start a new project, create requirements, define an implementation strategy, or mentions "spec-driven development." Also trigger when the user says things like "let's plan this feature," "what should we build," "write a spec for," "break this down into tasks," or "I need to think through this before coding." Even if they don't say "spec" explicitly — if they're about to build something non-trivial and haven't planned it yet, suggest this workflow.
argument-hint: <feature-name>
---

# Spec-Driven Development

Spec-Driven Development flips the traditional workflow: instead of jumping into code and figuring it out as you go, you write clear specifications first and let those specs drive the implementation. This produces more predictable, higher-quality results because every line of code traces back to a defined requirement.

Source methodology: [github/spec-kit](https://github.com/github/spec-kit)

## The Workflow

SDD has 5 core phases and 3 optional phases. Run them in order, but skip what doesn't apply — a small feature might only need Specify → Tasks → Implement.

### Core Phases

| Phase | Purpose | Input | Output |
|-------|---------|-------|--------|
| **1. Constitution** | Establish project principles | Project context | `constitution.md` |
| **2. Specify** | Define what to build (not how) | User stories, scenarios | `specification.md` |
| **3. Plan** | Technical implementation strategy | Spec + tech stack | `plan.md` |
| **4. Tasks** | Actionable implementation steps | Plan | `tasks.md` |
| **5. Implement** | Build it | Tasks | Working code |

### Optional Phases (use when needed)

| Phase | When to Use | Purpose |
|-------|------------|---------|
| **Clarify** | After Specify, when requirements are ambiguous | Resolve gaps before planning |
| **Analyze** | After Tasks, before Implement | Cross-check consistency across all artifacts |
| **Checklist** | Anytime | Custom quality validation |

## How to Guide the User

### Starting a new feature

1. **Ask for the feature name** (use as `$ARGUMENTS` or ask). Always create the feature directory and tell the user where outputs will go:
   ```
   .specify/features/<feature-id>/
   ```
   Every phase output file goes here. Name this path explicitly in your response so the user knows where to find their specs.

2. **Determine starting phase.** Ask: "Do you have existing project principles, or should we start from scratch?"
   - No existing specs → Start at Constitution
   - Has project principles → Start at Specify
   - Has requirements, needs technical plan → Start at Plan
   - Has a plan, needs task breakdown → Start at Tasks

3. **Run each phase sequentially.** For each phase:
   - Explain what this phase produces and why it matters
   - Ask the user targeted questions (see phase guides in `references/templates.md`)
   - Write the output file to `.specify/features/<feature-id>/`
   - Confirm with the user before moving to the next phase

### Phase-by-phase guidance

#### Phase 1: Constitution
Establish the governing principles for this project. These are high-level constraints that every subsequent decision must respect — think code quality standards, testing requirements, UX principles, performance budgets, accessibility requirements.

If the project already has a `CLAUDE.md` or established conventions, extract principles from there rather than starting from scratch.

**Key questions to ask:**
- What are your non-negotiable quality standards?
- What's the testing philosophy? (TDD, integration-first, etc.)
- Any architectural constraints? (monorepo, microservices, specific frameworks)
- Performance or accessibility requirements?

#### Phase 2: Specify
Define WHAT will be built — user stories, scenarios, acceptance criteria. Deliberately avoid technology choices here. Focus on the user's perspective and desired outcomes.

**Key questions to ask:**
- Who are the users of this feature?
- What problem does it solve for them?
- What are the success criteria? How do you know it works?
- What are the edge cases and failure modes?
- What's explicitly out of scope?

#### Phase 3: Plan
Now layer in the HOW — technology choices, architecture, integration patterns, data models, API contracts. Reference the specification to ensure every requirement has a technical home.

**Key questions to ask:**
- What's the tech stack? (or recommend based on project context)
- How does this integrate with existing systems?
- What are the key architectural decisions and their tradeoffs?
- Any dependencies or sequencing constraints?

#### Phase 4: Tasks
Break the plan into ordered, actionable implementation steps. Each task should be completable in a single focused session. Include dependencies between tasks and mark which can be parallelized.

**Output format:** Numbered task list with:
- Clear description of what to do
- Acceptance criteria (how you know it's done)
- Dependencies (which tasks must complete first)
- Estimated complexity (S/M/L)

#### Phase 5: Implement
Execute the tasks in order. For each task:
1. Read the task description and acceptance criteria
2. Implement it
3. Verify against acceptance criteria
4. Mark complete and move to the next

## File Structure

```
.specify/
└── features/
    └── <feature-id>/
        ├── constitution.md    (Phase 1)
        ├── specification.md   (Phase 2)
        ├── plan.md           (Phase 3)
        ├── tasks.md          (Phase 4)
        └── implementation/   (Phase 5 - working notes)
```

## When to Suggest This Workflow

- User is about to build a non-trivial feature (more than a few files)
- User seems uncertain about requirements or approach
- User asks "how should we build this?" or "what's the plan?"
- User wants to hand off work to another developer or AI agent
- User has been going back and forth on implementation without clear direction

## When NOT to Use This

- Bug fixes (just fix it)
- Simple refactors with clear scope
- User explicitly wants to vibe-code and iterate fast
- Trivial changes (rename, add a field, update copy)

## Reference Files

- See `references/templates.md` for detailed output templates for each phase