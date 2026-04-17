---
name: scroll-debug
description: Diagnose and fix broken scroll animations — jank, hydration mismatches, ScrollTrigger conflicts, Lenis issues, mobile scroll problems, pinned sections that don't release, animations that fire at wrong scroll positions, elements stuck mid-animation. Use when scroll animations aren't working right, the page stutters, or something "feels off" during scroll.
user-invokable: true
args:
  - name: symptom
    description: What's going wrong — "jank on scroll", "section won't unpin", "animation fires too early", etc.
    required: false
---

Diagnose and fix scroll animation issues systematically.

## Triage

If the user described a symptom, start there. If not, run the full diagnostic.

## Common Issues (Ranked by Frequency)

### 1. Hydration Mismatch (Next.js)
**Symptom**: Console error about server/client HTML mismatch, flickering on load
**Cause**: `Math.random()`, `Date.now()`, `new Date()`, or `window`-dependent values in render
**Fix**: Use deterministic values (seed-based pseudo-random) or wrap in `useEffect` / `'use client'` with `useState` initialized to null
```tsx
// BAD: different on server vs client
const height = Math.random() * 100;

// GOOD: deterministic from index
const height = Math.sin(i * 127.1 + 311.7) * 43758.5453 % 1 * 100;

// GOOD: client-only
const [height, setHeight] = useState(0);
useEffect(() => setHeight(Math.random() * 100), []);

// BAD: different on server vs client
const year = new Date().getFullYear();

// GOOD: hardcode or compute in useEffect
const year = 2026; // or use useState + useEffect
```

### 2. ScrollTrigger Not Triggering
**Symptom**: Animations never play, elements stay invisible
**Causes**:
- Plugin not registered: `gsap.registerPlugin(ScrollTrigger)` missing
- Wrong `start` value: element already past the trigger point on load
- Lenis not connected: `lenis.on('scroll', ScrollTrigger.update)` missing
- Component unmounted before ScrollTrigger initialized

**Diagnostic**:
```js
// Add temporarily to see all triggers
ScrollTrigger.getAll().forEach(st => console.log(st.vars.trigger, st.start, st.end));
```

### 3. Scroll Jank (Not 60fps)
**Symptom**: Stuttering during scroll, especially on fast scroll
**Causes**:
- Animating `width`, `height`, `top`, `left` instead of `transform` and `opacity`
- Heavy re-renders during scroll (React state updates in scroll handler)
- Large images not lazy-loaded
- Too many simultaneous ScrollTriggers (>20 on one page)
- Missing `will-change: transform` on animated elements
- Lenis + CSS `scroll-behavior: smooth` conflict

**Fix checklist**:
- [ ] Only animate `transform` and `opacity`
- [ ] Use `gsap.ticker` not `window.addEventListener('scroll')`
- [ ] Add `html { scroll-behavior: auto !important; }` to prevent Lenis conflict
- [ ] Lazy load below-fold images
- [ ] Use `ScrollTrigger.batch()` for many similar triggers

### 4. Pinned Section Won't Release
**Symptom**: Section stays pinned forever, content below is pushed down
**Causes**:
- `end` value too large or infinite
- `pinSpacing: false` when it should be `true`
- Nested ScrollTriggers with conflicting pins
- Container height changed after pin was created (dynamic content)

**Fix**:
```js
// Refresh after dynamic content loads
ScrollTrigger.refresh();

// Or use invalidateOnRefresh for responsive
ScrollTrigger.create({
  invalidateOnRefresh: true,
  end: () => "+=" + sectionRef.current.offsetHeight,
});
```

### 5. SplitText Broken After Route Change
**Symptom**: Text shows raw HTML spans instead of formatted text, or is invisible
**Cause**: SplitText wraps text in `<span>` elements. On route change, React re-renders and the original text is gone but the spans remain.
**Fix**: Always revert SplitText in cleanup:
```js
useEffect(() => {
  const split = new SplitText(el, { type: "chars" });
  gsap.from(split.chars, { ... });
  return () => split.revert(); // CRITICAL
}, []);
```

### 6. Mobile Scroll Issues
**Symptom**: Animations janky on mobile, touch scroll feels wrong, rubber banding
**Causes**:
- Lenis not handling touch events
- Pinned sections too long for mobile viewport
- Too many GPU-intensive animations running simultaneously
- iOS Safari address bar resize triggers ScrollTrigger recalculation

**Fix**:
```js
// Use matchMedia for mobile-specific settings
gsap.matchMedia().add("(max-width: 768px)", () => {
  // Simpler animations, shorter pins, fewer effects
  ScrollTrigger.create({ ...mobileConfig });
});

// Handle iOS resize
ScrollTrigger.normalizeScroll(true);
```

### 7. GSAP Context Cleanup Leak
**Symptom**: Animations play multiple times, memory leak, console warnings
**Cause**: Missing cleanup in React useEffect
**Fix**:
```tsx
useEffect(() => {
  const ctx = gsap.context(() => {
    // ALL animations in here
  }, sectionRef); // scope to ref
  return () => ctx.revert(); // cleanup
}, []);
```

**IMPORTANT**: `gsap.context().revert()` does NOT revert SplitText DOM modifications. If you use SplitText inside a context, you must also call `split.revert()` separately in your useEffect cleanup. See Section 5 for the correct pattern.

## Full Diagnostic

If the symptom isn't in the list above, run this checklist:

1. **Open browser DevTools → Performance tab** → Record while scrolling → Check for:
   - Long tasks (>50ms blocks)
   - Layout thrashing (purple bars)
   - Paint storms (green bars)

2. **Check the console** for:
   - GSAP warnings ("target not found", "invalid property")
   - ScrollTrigger warnings ("no matching targets")
   - React hydration warnings
   - Lenis errors

3. **Verify the setup chain**:
   - [ ] `gsap.registerPlugin(ScrollTrigger, SplitText)` — called once, at top level
   - [ ] Lenis initialized and connected to ScrollTrigger
   - [ ] `gsap.ticker.lagSmoothing(0)` — prevents ticker from pausing during tab switch
   - [ ] All ScrollTrigger instances created inside `gsap.context()` for cleanup
   - [ ] `html { scroll-behavior: auto !important; }` — no CSS smooth scroll conflict

4. **Test with animations disabled**: Comment out all GSAP code. Does the page scroll smoothly? If yes, the issue is in the animations. If no, it's a layout/CSS issue.

## After Fixing

- Run `npm run build` — verify no errors
- Test in browser — scroll the full page fast, slow, and normal
- Check mobile if applicable
- Report what was wrong and what was fixed
