---
name: scroll-normalize
description: Enforce consistency across all sections of a scroll-driven website. Ensures the motion language, easing palette, timing, spacing rhythm, typography, and color usage follow the project's scroll design context. The "normalizer" — finds where sections deviate from the established patterns and brings them in line. Use when the page has good individual sections but they feel disjointed, or after multiple people (or multiple AI sessions) have worked on different sections.
user-invokable: true
---

Review a scroll-driven website for consistency violations and normalize everything to match the project's design system.

## Preparation

Read the project's scroll design context (scroll-context.md or equivalent). If none exists, run `/teach-scroll` first — normalizing without a reference system is arbitrary.

## What Gets Normalized

### 1. Easing Consistency

Scan every GSAP tween and verify it uses the project's easing palette:

| Context | Should Be | Red Flags |
|---------|-----------|-----------|
| Element entrance | `power2.out` | `ease`, `linear`, `power1.out`, missing ease |
| Headline animation | `power3.out` | `power2.out` (too weak), `power4.out` (too dramatic) |
| Scroll-linked | `scrub: 1` | `scrub: true` (too snappy), `scrub: 0.3` (too tight) |
| Hover | `power2.out, 0.2s` | `0.5s` (too slow), `linear` |
| Exit | `power2.in` | `power2.out` (wrong direction) |
| Ambient | `power2.inOut, 3-8s` | `1s` (too fast), `linear` |

**How to find violations:**
```bash
# Find all ease values in the project
grep -rn "ease:" src/components/ --include="*.tsx"
grep -rn "duration:" src/components/ --include="*.tsx"
```

### 2. Timing Consistency

| Animation Type | Target Duration | Violation |
|---------------|----------------|-----------|
| Micro (hover, press) | 0.15-0.3s | > 0.4s |
| Entrance (fade, slide) | 0.4-0.8s | < 0.2s or > 1.2s |
| Section transition | 0.6-1.2s | < 0.4s or > 1.5s |
| Hero / first load | 1.0-2.0s | < 0.5s or > 3.0s |
| Ambient / loops | 3.0-8.0s | < 2s (too frantic) or > 15s (imperceptible) |

### 3. Stagger Consistency

| Element Group | Target Stagger | Violation |
|--------------|---------------|-----------|
| Characters (SplitText) | 0.02s | > 0.05s (too slow) or < 0.01s (invisible) |
| List items / cards | 0.05-0.1s | > 0.2s (feels broken) |
| Grid items | 0.08s | > 0.15s |
| Navigation links | 0.05s | > 0.1s |

### 4. Spacing Rhythm

- Between major sections: should be consistent (all 100vh, or all 80vh — not mixing)
- Pin duration: consistent pattern (all 200%, or all 150% — not one at 100% and another at 400%)
- Padding: using the same scale (`clamp()` values should repeat, not vary randomly)
- Max-width for text: all body text at 60ch (or whatever the context specifies)

### 5. ScrollTrigger Start/End Positions

All similar animations should trigger at similar scroll positions:
```js
// These should match across all entrance animations
start: "top 80%"  // Standard entrance trigger

// NOT a mix of:
// start: "top 50%"  (too late — user sees blank space)
// start: "top 95%"  (too early — user barely sees it)
// start: "top center" (ambiguous)
```

### 6. Typography Usage

- Are all display headlines using the display font + weight?
- Are all body texts using the body font + weight?
- Is mono consistently used for data/code/filenames?
- Is letter-spacing consistent per text level?
- Are `clamp()` values consistent across sections?

### 7. Color Usage

- Is the accent color used consistently? (Not two different shades of teal in different sections)
- Are backgrounds following the pattern? (deep → section → deep, or consistent)
- Is text color consistent? (primary text same shade everywhere, secondary same shade everywhere)
- Is the accent used sparingly? (If one section has teal everywhere and another barely uses it, normalize)

### 9. Supporting Text Animations
Check that body text and subtitles have entrance animations, not just headlines:
- If a headline uses SplitText character animation but the body text below just appears, add a simple entrance (y: 20, opacity: 0, power2.out, 0.6s)
- Stagger body paragraphs at 0.1s delay after the headline
- Don't animate body text character-by-character — just fade/slide the whole paragraph

### 8. Animation Property Variety

This is the opposite — check that sections DON'T all animate the same way:
- If every section does `y: 40, opacity: 0` entrance, that's monotonous
- Each section should have a distinct primary animation technique (see the Motion Variety Palette in `/scrollytelling`)
- But the SUPPORTING animations (stagger timing, easing) should be consistent

## The Normalize Process

1. **Audit**: Read every component file. List every GSAP tween with its ease, duration, stagger, and trigger position.
2. **Identify deviations**: Compare against the scroll design context. Flag anything that doesn't match.
3. **Fix**: Update the code to match the design system. Don't just change values — understand WHY the deviation exists. Maybe a section intentionally broke the rules (a dramatic moment that needs different timing). If so, leave it and note it.
4. **Verify**: Build and test. Scroll through the entire page. The experience should feel cohesive — like one person designed it, even if five sessions built it.

## Output

Report:
- How many deviations found
- What was changed (before/after for each)
- Any intentional deviations left in place (with reasoning)
- `npm run build` clean
