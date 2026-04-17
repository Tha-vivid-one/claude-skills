---
name: scroll-adapt
description: Adapt scroll-driven animations to work across screen sizes, devices, and contexts. Ensures the scrollytelling experience works on mobile, tablet, and desktop without breaking animations or creating jank. Use when the desktop scroll experience is solid but mobile feels broken, or when you need responsive scroll animations that aren't just "make it smaller."
user-invokable: true
args:
  - name: target
    description: Specific section to adapt, or "all" for the full page
    required: false
---

Make scroll-driven animations responsive — not by just scaling things down, but by rethinking what works at each viewport.

## Philosophy

Mobile scroll animation is NOT just desktop animation on a smaller screen. It's a different medium:
- Touch scroll has different physics than trackpad/mouse wheel
- Smaller viewport means less breathing room between moments
- Mobile GPUs can't handle as many simultaneous animations
- Pinned sections feel different on mobile (address bar resize, rubber banding)
- Horizontal scroll is natural on mobile (swipe) but awkward on desktop (scroll-jack)

## The Adaptation Process

### 1. Audit Current State

Open the site on a mobile viewport (375px) in DevTools and scroll through:
- Which sections break? (overflow, text too large, elements off-screen)
- Which animations are janky? (too many GPU layers, complex transforms)
- Which pinned sections feel too long? (endless scroll on a small screen)
- Which text is unreadable? (display text too large at mobile size)

### 2. Use GSAP matchMedia

Don't use CSS media queries for animation changes — use `gsap.matchMedia()`:

```js
const mm = gsap.matchMedia();

mm.add("(min-width: 769px)", () => {
  // Desktop animations — full complexity
  gsap.from(elements, {
    y: 60, stagger: 0.1, duration: 0.8,
    scrollTrigger: { trigger: section, pin: true, scrub: 1, end: "+=200%" }
  });
});

mm.add("(max-width: 768px)", () => {
  // Mobile animations — simpler, shorter, fewer
  gsap.from(elements, {
    y: 30, stagger: 0.05, duration: 0.5,
    scrollTrigger: { trigger: section, start: "top 85%" }
    // No pin on mobile — it fights with touch scroll
  });
});

// Cleanup handled automatically by matchMedia
```

### 3. Mobile-Specific Adjustments

**Pinned sections**: Reduce or remove pins on mobile. Long pinned sections on touch devices feel like the page is stuck. If you must pin, keep it under 150% viewport height.

**SplitText character animation**: Reduce stagger on mobile (0.01s instead of 0.02s) or switch to word/line animation instead of character. 40 animated characters on a 375px screen is visual noise.

**Parallax**: Reduce range dramatically (5px instead of 15px) or disable entirely. Mouse parallax doesn't exist on touch.

**Scroll velocity effects**: Disable or reduce on mobile. Touch scroll velocity is erratic compared to trackpad.

**Typography scale**: Ensure `clamp()` values work at 375px. Display text should still be impactful but readable:
```css
--display: clamp(2rem, 8vw + 0.5rem, 8rem);  /* 32px at 375px, huge at desktop */
```

**Horizontal scroll sections**: These often work BETTER on mobile (natural swipe) but need touch event handling. Keep panel widths at 85vw on mobile (peek at next panel).

**Noise grain overlay**: Reduce opacity to 1% on mobile or disable — mobile screens are smaller and grain is more noticeable.

### 4. iOS Safari Specifics

The iOS Safari address bar resizes the viewport on scroll, which triggers ScrollTrigger recalculations:

```js
// Normalize scroll to prevent address bar jank
ScrollTrigger.normalizeScroll(true);

// Use dvh instead of vh for full-height sections
.hero { min-height: 100dvh; }
```

### 5. Performance Budget — Mobile

Mobile has a stricter budget:
- Max 10 active ScrollTriggers (vs 20+ on desktop)
- No blur() filters during scroll (GPU killer on mobile)
- Reduce particle counts by 50-75%
- Disable WebGL/shader effects on mobile unless specifically designed for it
- Use `will-change: transform` only on elements about to animate, remove after

### 6. Reduced Motion

Always respect `prefers-reduced-motion`:

```js
gsap.matchMedia().add("(prefers-reduced-motion: reduce)", () => {
  // Disable all scroll-driven animations
  // Show content statically
  // Keep basic fade-ins if any
  ScrollTrigger.getAll().forEach(st => st.kill());
  gsap.set("[data-animate]", { clearProps: "all" });
});
```

## Output

After adapting, verify on:
- [ ] Desktop (1440px+)
- [ ] Tablet (768px)
- [ ] Mobile (375px)
- [ ] iOS Safari (if possible)
- [ ] With `prefers-reduced-motion` enabled
- [ ] `npm run build` clean
