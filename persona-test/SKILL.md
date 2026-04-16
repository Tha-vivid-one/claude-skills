---
name: persona-test
description: Test any design, copy, UX, or product decision against simulated user personas. Use when the user wants to compare options, test headlines, evaluate button labels, pick between designs, grade copy, or get feedback on any product decision from multiple perspectives. Triggers on phrases like "test this", "which is better", "compare these", "run against personas", "persona test", "grade these options", "which copy works", "test this headline", "which version", or any A/B/C comparison of creative or product options.
---

# Persona Test

Test any product decision against 10 diverse simulated personas. Works for copy, headlines, UI patterns, feature names, pricing, onboarding flows, button labels — anything where you want signal from multiple perspectives before committing.

## How it works

The skill runs in three phases: **Generate**, **Test**, **Rank**.

### Phase 1: Generate (or accept) candidates

If the user provides specific candidates to compare, use those directly.

If the user provides a topic without candidates (e.g., "headline for a productivity app"), research the domain first:
1. Search for best practices, frameworks, and examples in that domain
2. Generate 25 candidate options across varied approaches (benefit-first, identity-first, metaphor, contrast, provocative, etc.)
3. Select the top 15 for testing based on variety and quality

The research step matters — candidates informed by real copywriting/design research outperform random brainstorming.

### Phase 2: Test against personas

Test each candidate against the persona panel. For each persona × candidate combination, collect:
- A 1-10 rating on each dimension
- A 1-sentence gut reaction in the persona's voice

**Default personas** (10, chosen for demographic and professional diversity):

| # | Persona | Why they're useful |
|---|---------|-------------------|
| 1 | 25yo creative freelancer | Tech-comfortable, design-aware, ad-skeptical |
| 2 | 35yo working mom, 2 kids | Time-starved, practical, low patience for jargon |
| 3 | 42yo startup founder | Ambitious, pattern-matching against other products, premium-sensitive |
| 4 | 28yo teacher | Moderate tech comfort, values clarity, limited budget |
| 5 | 50yo corporate executive | High expectations, jargon-tolerant in business context, premium-oriented |
| 6 | 22yo recent grad | Digital native, trend-aware, budget-conscious |
| 7 | 38yo small business owner | Pragmatic, ROI-focused, overwhelmed by options |
| 8 | 30yo software engineer | Technical, skeptical of marketing, values substance |
| 9 | 45yo real estate agent | Relationship-focused, mobile-first, wants tools that save time |
| 10 | 33yo nurse | Shift worker, high stress, needs things to just work |

When simulating each persona, commit to their perspective. A nurse doesn't think about "systems" the same way a software engineer does. A working mom has different patience thresholds than a recent grad. The gut reactions should sound like real people, not marketing evaluations.

**Default dimensions** (3):

| Dimension | What it measures |
|-----------|-----------------|
| Clarity | Could this person understand what's being offered in under 3 seconds? |
| Desire | Does this make them want to continue / buy / engage? |
| Premium Feel | Does this feel high-quality, trustworthy, and worth their time? |

### Phase 3: Rank and report

Compile results into:

1. **Ranked table** — all candidates sorted by total average score, showing per-dimension averages
2. **Dimension winners** — which candidate scored highest on each individual dimension
3. **Top 5 deep dive** — for the top 5 candidates, include:
   - Full score breakdown
   - Notable persona reactions (especially disagreements — bimodal distributions are important signal)
   - Strengths and weaknesses
   - Which audience this candidate works best for
4. **Strategic recommendations** — suggest which candidate to use in which context (e.g., "Use X for Product Hunt launch, Y for mass-market landing page, Z for in-app")
5. **Key insights** — patterns that emerged across the testing (e.g., "personas over 40 consistently preferred concrete language over metaphors")

### Saving results

After presenting results, offer to save them. Ask the user where they'd like the results saved, or save to the current project directory as `persona-test-results/[Topic]-[Date].md`.

Include the full ranked table, top 5 analysis, and strategic recommendations.

## Arguments

The skill accepts these optional arguments:

- **Topic** (positional): What you're testing. E.g., `"headline for welcome screen"`
- **--candidates**: Comma-separated list of specific options to test. Skips the generation phase.
- **--dimensions**: Comma-separated custom dimensions. E.g., `"Trust, Excitement, Clarity"`
- **--personas**: Comma-separated custom personas. E.g., `"tech founders, enterprise buyers, solo creators"`. Brief descriptions are expanded into full personas internally.
- **--count**: Number of candidates to generate (default 25, top 15 tested)
- **--top**: Number of candidates for the deep-dive analysis (default 5)

## Examples

```
/persona-test "headline for welcome screen"
```
Researches headline best practices, generates 25, tests top 15, ranks, saves.

```
/persona-test --candidates "Connect, Enable, Unlock, Turn On" "button label for granting permissions"
```
Tests the 4 provided options directly, no generation phase.

```
/persona-test "onboarding copy tone" --dimensions "Warmth, Trust, Clarity, Motivation" --personas "privacy-conscious millennial, busy executive, first-time app user, skeptical engineer"
```
Custom dimensions and personas.

```
/persona-test "pricing page: monthly vs annual toggle placement"
```
Researches pricing page UX, generates layout/copy candidates, tests.

## What makes this skill different from just asking "which is better?"

Three things:

1. **Structured diversity.** Ten personas with different jobs, ages, and contexts catch blind spots that a single perspective misses. A headline that resonates with a startup founder might alienate a nurse.

2. **Quantified signal.** Gut feelings become comparable numbers. You can see that Option A wins on clarity but loses on premium feel — that's actionable in a way "I like A better" isn't.

3. **Bimodal detection.** The most important finding is often disagreement. If a headline scores 9 with founders and 4 with teachers, that's not an average-of-6.5 situation — it's a targeting decision. The per-persona breakdown reveals these splits.
