---
name: scroll-polish
description: Final quality pass on scroll-driven animated websites. Fixes timing, easing, spacing, choreography, and detail issues that separate good from great. Use after building with /scrollytelling when the page works but doesn't feel quite right — animations are slightly off, spacing is inconsistent, transitions feel abrupt, or the page lacks the final layer of craft.
user-invokable: true
args:
  - name: target
    description: Specific section or area to polish (optional — polishes entire page if omitted)
    required: false
---

Review a scroll-driven animated page and apply the final layer of craft that separates functional from exceptional.

## Preparation

Read the project's scroll design context (scroll-context.md or equivalent). If none exists, run `/teach-scroll` first — polishing without a design system is guessing.

## The Polish Pass

Work through each section systematically:

### 1. Timing Audit
- Are entrance animations fast enough? (0.4-0.8s for elements, not longer)
- Are hover states instant? (0.15-0.3s, never more)
- Does the hero feel too slow or too fast on initial load?
- Are scroll-triggered animations starting at the right scroll position? (`start: "top 80%"` is usually right — `top 50%` means the user has already been staring at a blank space)
- Is there dead scroll space where nothing happens? Either add content or reduce the gap.

### 2. Easing Audit
- Scan for any `linear` or default CSS `ease` — replace with proper GSAP easing
- Verify headlines use `power3.out` (not `power2.out` — headlines deserve more drama)
- Check ambient loops use `power2.inOut` (symmetrical, breathing feel)
- Look for `elastic.out` or `bounce` on UI elements — remove unless intentionally playful

### 3. Choreography Audit
- Do animations overlap properly? Adjacent elements should start before the previous finishes (`"-=0.2"` or `"-=0.3"`)
- Is the most important element animating first in each section?
- Do staggered groups have the right delay? (`0.02s` for characters, `0.05-0.08s` for list items, `0.1s` for cards)
- Are different properties animated per element? (If everything just fades up, vary it — translateY for headings, scale for buttons, clip-path for images, opacity for supporting text)

### 4. Spacing Audit
- Is there 100vh+ breathing room between major scroll moments?
- Are pinned sections holding long enough? (150-300% viewport height)
- Is body text max-width capped at 60ch?
- Are sections using generous padding? (`clamp(3rem, 6vw, 8rem)` vertically)

### 5. Detail Layer Check
- Do links have hover animations? (underline slide, color transition)
- Do buttons have active/pressed states? (scale 0.98, subtle)
- Is there a noise grain overlay? (2-4% opacity, fixed position)
- Does selection color match the accent?
- Are scrollbar styles considered? (thin, accent-colored or hidden)

### 6. Performance Check
- Verify 60fps scroll (no jank when scrolling fast)
- Check that only `transform` and `opacity` are animated (no `width`, `height`, `top`, `left`)
- Verify images are lazy-loaded below the fold
- Check JS bundle isn't over 200KB gzipped

## Output

For each issue found, fix it directly in the code. Don't just report issues — fix them. After all fixes:
- Run `npm run build` to verify clean build
- Test in browser — scroll through entire page
- Report what was changed in a concise summary
