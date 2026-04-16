# SDD Phase Templates

Output templates for each Spec-Driven Development phase. Adapt to the project — skip sections that don't apply, add sections that do.

## Table of Contents
- [Constitution](#constitution-template)
- [Specification](#specification-template)
- [Plan](#plan-template)
- [Tasks](#tasks-template)
- [Clarify](#clarify-template)
- [Analyze](#analyze-template)

---

## Constitution Template

```markdown
# Project Constitution: [Project Name]

## Core Principles
1. [Principle] — [Why it matters]
2. ...

## Quality Standards
- **Testing**: [Philosophy and requirements]
- **Code quality**: [Standards, linting, review process]
- **Performance**: [Budgets, benchmarks, targets]
- **Accessibility**: [WCAG level, requirements]

## Architectural Constraints
- [Framework/stack decisions and rationale]
- [Infrastructure constraints]
- [Integration requirements]

## Development Process
- [Branching strategy]
- [Review requirements]
- [Deployment process]
```

**Guidance**: If the project has an existing CLAUDE.md or README with conventions, extract principles from those rather than asking the user to restate everything. Keep it to 10-15 principles max — this document should be scannable, not exhaustive.

---

## Specification Template

```markdown
# Feature Specification: [Feature Name]

## Problem Statement
[What problem does this solve? For whom? Why now?]

## User Stories

### [User Role]
- As a [role], I want to [action] so that [benefit]

## Acceptance Criteria
1. [Criterion] — [How to verify]
2. ...

## Scenarios

### Happy Path
[Step-by-step expected flow]

### Edge Cases
- [Case]: [Expected behavior]

### Error Handling
- [Error condition]: [Expected response]

## Out of Scope
- [Explicitly excluded items]

## Open Questions
- [Unresolved items needing clarification]
```

**Guidance**: The specification should be technology-agnostic. No database schemas, no API endpoints, no framework choices. If the user starts talking implementation details, gently redirect: "Let's capture what it should do first, then we'll figure out how in the Plan phase."

---

## Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Tech Stack
| Component | Choice | Rationale |
|-----------|--------|-----------|
| [Layer] | [Technology] | [Why] |

## Architecture
[High-level design — how components interact]

### Data Model
[Key entities, relationships, schema changes]

### API Contracts
[Endpoints, request/response formats, error codes]

### Integration Points
[How this connects to existing systems]

## Key Decisions
| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Decision] | [A, B, C] | [B] | [Why] |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [H/M/L] | [Strategy] |

## Dependencies
- [External dependencies, sequencing constraints]
```

**Guidance**: Every requirement from the specification should have a technical home in this document. If a requirement doesn't map to anything here, either the spec needs updating or the plan is incomplete. Cross-reference explicitly.

---

## Tasks Template

```markdown
# Implementation Tasks: [Feature Name]

## Overview
- **Total tasks**: [N]
- **Overall complexity**: [S/M/L]
- **Parallelizable**: [Which tasks can run concurrently]

## Tasks

### Task 1: [Title]
- **Description**: [What to do]
- **Acceptance criteria**: [How to verify completion]
- **Dependencies**: None / Task N
- **Complexity**: S/M/L
- **Key files**: [Files to create or modify]

### Task 2: [Title]
...

## Dependency Graph
[Text or ASCII showing which tasks depend on which]

## Testing Plan
- [Unit tests needed]
- [Integration tests needed]
- [Manual verification steps]
```

**Guidance**: Each task should be completable in one focused session. If a task feels like it needs subtasks, it's too big — split it. Order tasks so that each one builds on completed work, and call out which tasks can be done in parallel.

---

## Clarify Template

Use between Specify and Plan when there are ambiguities.

```markdown
# Clarification: [Feature Name]

## Ambiguities Identified

### 1. [Topic]
- **What's unclear**: [Description]
- **Option A**: [Interpretation and implications]
- **Option B**: [Interpretation and implications]
- **Resolved**: [Decision and rationale]

## Assumptions Made
- [Assumption]: [Basis]

## Items Deferred
- [Item]: [Why deferred, when to revisit]
```

---

## Analyze Template

Use between Tasks and Implement to validate consistency.

```markdown
# Analysis: [Feature Name]

## Requirement Coverage
| Requirement | Plan Section | Task | Status |
|------------|-------------|------|--------|
| [Req from spec] | [Plan reference] | [Task N] | Covered / Gap |

## Constitutional Alignment
| Principle | How Addressed | Compliant? |
|-----------|--------------|------------|
| [Principle] | [Implementation approach] | Yes / Partial / No |

## Consistency Issues
- [Cross-reference problems found between artifacts]

## Risks Identified
- [New risks discovered during analysis]
```