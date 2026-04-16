# Methodology Reference

Deep background on the four approaches this skill combines. Read this when you need to understand
*why* the skill works the way it does, or when the user asks about the methodology.

## Table of Contents
1. [Test-Driven Prompting](#test-driven-prompting)
2. [Multi-Candidate Synthesis](#multi-candidate-synthesis)
3. [Harness Engineering](#harness-engineering)
4. [Signal Discipline](#signal-discipline)
5. [Anti-Patterns](#anti-patterns)

---

## Test-Driven Prompting

**Source**: Amanda Askell, Anthropic's prompt engineering lead

> "The boring yet crucial secret behind good system prompts is test-driven development.
> You don't write down a system prompt and find ways to test it. You write down tests
> and find a system prompt that passes them."

### The Process

1. Write a set of test messages where the model fails (cases where default behavior isn't what you want)
2. Find a system prompt that causes those tests to pass
3. Find messages the prompt is misapplied to — fix the prompt to handle them
4. Expand the test set and repeat

### Key Practices

- **Hundreds of iterations**: In 15-minute spans, Askell sends hundreds of prompts. This isn't about getting it right — it's about systematic probing.
- **Diagnostic questions**: When the model fails, ask it "Why did you do that?" to identify which instruction is weak or ambiguous.
- **Edge case anticipation**: Empty inputs, unexpected formats, tasks at the boundary of the model's training.
- **Regression testing**: Every fix must not break previously passing cases.

### Analogy to Software Testing

| Software Testing | Prompt Testing |
|-----------------|----------------|
| Unit tests | Individual test messages |
| Integration tests | Multi-turn conversations |
| Edge case tests | Unusual inputs, boundary conditions |
| Regression tests | Re-running after prompt changes |
| CI/CD | Periodic re-evaluation as models update |

---

## Multi-Candidate Synthesis

**Source**: PromptWizard (Microsoft Research, 2024)

Instead of writing one prompt and iterating, generate multiple structurally different candidates
and combine the best parts.

### The Process

1. **Generate** 3-5 prompt candidates with different structural approaches
2. **Critique** each candidate against known failure modes
3. **Score** on a rubric (coverage of failure modes, clarity, conciseness)
4. **Synthesize** the best elements into a single draft
5. **Jointly optimize** instructions and examples together (not separately)

### Why This Works

- Different structures have different blind spots
- Critique reveals which structures handle which failure modes
- Synthesis combines complementary strengths
- Much more efficient than serial iteration (PromptWizard achieves superior results with 69 API calls vs competitors' thousands)

### Candidate Archetypes

- **Minimal**: Bare instructions, no examples. Tests whether the task is simple enough for this.
- **Example-heavy**: 2-3 examples with minimal instructions. Best for format-sensitive tasks.
- **Role-first**: Strong persona definition. Best for tone/style-sensitive tasks.
- **Structured**: XML tags, explicit sections, output templates. Best for complex multi-part outputs.
- **Domain-specific**: Uses domain terminology and conventions. Best for specialized tasks.

---

## Harness Engineering

**Source**: Mitchell Hashimoto (HashiCorp founder)

> "Anytime you find an agent makes a mistake, engineer a solution so it never happens that way again."

### The Process

1. Agent fails at a task
2. Diagnose the root cause
3. Add a rule/tool/example to the prompt that prevents this specific failure
4. The prompt accumulates institutional knowledge over time

### Application to Prompt Engineering

Every failure during testing becomes a permanent part of the prompt:

```markdown
<!-- Added after test case 3 failed: model was including raw SQL in user-facing summaries -->
Never include raw code snippets in the summary. If the finding involves code,
describe what the code does in plain language. The audience is business stakeholders
who won't understand technical syntax.
```

The comment documents *why* the rule exists. This is crucial because:
- Future editors know not to remove it without understanding the context
- The model can use the reasoning to generalize to similar situations
- It creates an audit trail of the prompt's evolution

---

## Signal Discipline

**Source**: Boris Cherny (Claude Code creator)

### The Constraint

- Target ~2.5k tokens for system prompts (~60-80 lines)
- Claude can follow ~150-200 instructions; the system prompt uses ~50
- Every token competes for attention — noise dilutes signal

### The Test

For every line in the prompt, ask: **"Would removing this cause errors?"**

If the answer is no, remove it. If the answer is "maybe", run a test case without it and see.

### Compression Techniques

1. **Merge redundant rules**: "Be concise" and "Keep responses short" → one instruction with context
2. **Replace rules with examples**: A single example often teaches more than three sentences of instruction
3. **Cut defensive instructions**: If the model doesn't exhibit a failure mode in testing, don't preemptively guard against it
4. **Explain why instead of listing rules**: "Responses go in a daily digest email read on mobile" teaches conciseness, formatting, and structure in one sentence

---

## Anti-Patterns

Common mistakes this methodology helps you avoid:

### The Kitchen Sink
Adding every possible instruction "just in case." This dilutes the important instructions and
makes the prompt fragile — changing any one thing risks cascading effects.

### The Shouting Prompt
Using ALL CAPS, MUST, NEVER, ALWAYS excessively. This signals that the prompt author doesn't
trust the model to understand reasoning. Replace with explanations of why something matters.

### The Example Trap
Including so many examples that the model pattern-matches to examples rather than understanding
the task. 2-3 diverse examples are usually optimal.

### The Phantom Fix
Adding a rule to prevent a failure that never actually happened in testing. Every rule should
trace back to a specific observed failure.

### The Frozen Prompt
Treating the prompt as done after the first version passes tests. Prompts are living documents —
they should evolve as you discover new failure modes in production.
