---
name: scrollytelling
description: Build award-winning scroll-driven animated websites with GSAP, Lenis, and ScrollTrigger. Takes a design brief or scroll moment descriptions and generates a complete scrollytelling page — Lenis smooth scroll, pinned sections, character-level text animation, scroll-scrubbed transitions, variety in motion per section. Use when the user wants to build an animated landing page, marketing site, portfolio, or any scroll-driven web experience. Triggers on "build a scroll website", "animated landing page", "scrollytelling", "scroll-driven", "make it like Godly/Awwwards", "scroll animation website".
user-invokable: true
args:
  - name: brief
    description: Path to a design brief markdown file, or inline description of what to build
    required: false
---

Build a complete scroll-driven animated website from a design brief.

## Before You Start

### 1. Check for design context
Look for `scroll-context.md` in the project root or design docs. If it doesn't exist, tell the user: "No scroll design context found. Run `/teach-scroll` first to set up your design system, or describe what you want and I'll use sensible defaults."

### 2. Check for brand voice (CRITICAL FOR COPY)
Look for `brand-voice.md` in the project root. This file controls:
- What tone the copy should have
- Words to use and words to avoid
- Whether AI-generated copy is acceptable
- Draft headlines for each scroll moment
- The product's origin story and differentiator

**If `brand-voice.md` exists**: Use it. Copy the draft headlines from "Copy for Each Scroll Moment" section. Respect the "Words We NEVER Use" list. Match the tone and voice rules. If headlines are marked ✍️ (user should write), use a clear placeholder like `[YOUR HEADLINE HERE — user to write]` instead of generating AI copy.

**If `brand-voice.md` doesn't exist**: Search the project for ANY brand/copy context:
- README.md (often has the product pitch)
- PRD or WHY docs (motivation, story)
- Existing marketing pages
- Package.json description field

If nothing is found, STOP and tell the user: "I don't have enough brand context to write compelling copy. I can either: (A) run `/teach-scroll` to establish your voice, or (B) build the page with placeholder copy you'll replace later. Which do you prefer?"

**Never generate generic SaaS copy** like "Transform your workflow" or "The future of X" without explicit brand context. Bad copy on a beautiful scroll experience is worse than no copy at all.

### 3. Accept input

If no context exists and the user wants to proceed anyway, use the defaults from `/teach-scroll`.

## Input

Accept one of:
1. A markdown design brief file (path passed as argument)
2. Inline description in the conversation
3. An existing `scroll-context.md` + `brand-voice.md` in the project

The brief should describe **scroll moments** — what the user experiences at each stage of scrolling. If the user gives a vague brief ("make a cool landing page for my app"), interview them to get specific moments before building.

A good brief has:
- What the page is selling/showing
- The scroll journey as a sequence of moments (what happens as you scroll)
- Colors, fonts, vibe (or defer to scroll-context.md)
- Any specific interactions they want

## Architecture

### Project Setup

If the project doesn't exist yet, scaffold:
```bash
npx create-next-app@latest <name> --typescript --tailwind --app --src-dir
cd <name>
npm install gsap @gsap/react lenis
```

If the project exists, just install the animation deps:
```bash
npm install gsap @gsap/react lenis
```

Note: Tailwind v4 uses CSS-based configuration (@theme in globals.css) instead of tailwind.config.ts. 
Define custom colors and spacing via CSS custom properties in globals.css rather than a config file.

### File Structure

```
src/
├── app/
│   ├── page.tsx          # Composes all sections
│   ├── layout.tsx        # Metadata, fonts
│   └── globals.css       # Theme, grain, base styles
├── components/
│   ├── LenisProvider.tsx  # Smooth scroll wrapper
│   ├── Navbar.tsx         # Sticky nav (appears on scroll)
│   └── sections/
│       ├── Hero.tsx       # Moment 1
│       ├── [Name].tsx     # Moment 2, 3, etc.
│       └── Footer.tsx     # Final moment
```

### LenisProvider (always include)

```tsx
'use client';
import { useEffect } from 'react';
import Lenis from 'lenis';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function LenisProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const lenis = new Lenis();
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => lenis.raf(time * 1000));
    gsap.ticker.lagSmoothing(0);
    return () => { lenis.destroy(); gsap.ticker.remove(lenis.raf); };
  }, []);
  return <>{children}</>;
}
```

### Section Component Pattern

Every section follows this pattern:
```tsx
'use client';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function SectionName() {
  const sectionRef = useRef<HTMLElement>(null);
  // If using SplitText, declare the instance outside context for proper cleanup
  let splitInstance: any = null;

  useEffect(() => {
    const ctx = gsap.context(() => {
      // All GSAP animations go here
      // If using SplitText: splitInstance = new SplitText(ref.current, { type: "words,chars" });
    }, sectionRef);
    return () => {
      splitInstance?.revert(); // Revert SplitText FIRST (if used)
      ctx.revert(); // Then revert GSAP context
    };
  }, []);

  return <section ref={sectionRef} className="...">...</section>;
}
```

## Building Each Moment

For each moment in the brief, build a section component. The critical rule: **every section must have a DIFFERENT motion treatment.** If every section fades up the same way, the page feels dead.

### Motion Variety Palette

Pick a different primary technique for each section:

| Technique | GSAP Code Pattern | Best For |
|-----------|-------------------|----------|
| **Character reveal** | SplitText + stagger 0.02s, power3.out | Headlines, hero text |
| **Scroll-scrubbed transform** | ScrollTrigger scrub: 1, pin: true | Hero sequences, parallax |
| **Staggered entrance** | gsap.from(elements, { stagger: 0.1, y: 40, power2.out }) | Feature cards, lists |
| **Sticky + scroll** | pin left panel, right side scrolls naturally | Product showcases |
| **Directional slides** | Elements enter from different directions per item | Comparisons, testimonials |
| **Scale + overshoot** | gsap.from({ scale: 0.8 }, { ease: "back.out(1.4)" }) | Pricing cards, CTAs |
| **Draw/reveal** | clip-path or SVG mask animated on scroll | Image reveals, dividers |
| **Chaos to order** | Scattered elements → organized grid on scrub | Before/after, organization demos |

### Easing Rules

These are non-negotiable — they're what makes motion feel professional vs amateur:

- **NEVER use `linear`** for UI animation. Ever.
- **NEVER use `ease`** (the CSS default). It's mushy.
- **Entrances**: `power2.out` (decelerating arrival)
- **Headlines**: `power3.out` (stronger decel, more dramatic)
- **Exits**: `power2.in` (accelerating away)
- **Scroll-linked**: `scrub: 1` standard, `scrub: 2` for dreamy/slow
- **Hover**: `power2.out`, 0.2s max
- **Playful moments**: `back.out(1.4)` (slight overshoot — use sparingly)
- **Ambient loops**: `power2.inOut`, 3-8 second duration

### ScrollTrigger Configuration

```js
// Standard section entrance
ScrollTrigger.create({
  trigger: sectionRef.current,
  start: "top 80%",      // Trigger when 80% down viewport
  toggleActions: "play none none none",
});

// Pinned hero section
ScrollTrigger.create({
  trigger: heroRef.current,
  start: "top top",
  end: "+=200%",          // 2x viewport of scroll distance
  pin: true,
  scrub: 1,
});

// Sticky left panel
ScrollTrigger.create({
  trigger: containerRef.current,
  start: "top top",
  end: "bottom bottom",
  pin: leftPanelRef.current,
  pinSpacing: false,
});
```

### Typography Animation

For headlines only — never animate body text character by character:

```js
import { SplitText } from 'gsap/SplitText';
gsap.registerPlugin(SplitText);

// SplitText cleanup must be handled OUTSIDE gsap.context — context.revert() does NOT revert SplitText
let splitInstance: any = null;

useEffect(() => {
  const ctx = gsap.context(() => {
    // CRITICAL: Use "words,chars" not just "chars" — wrapping each char in a span
    // breaks CSS word-wrap, causing mid-word line breaks like "bro ken" and "em ail"
    splitInstance = new SplitText(headingRef.current, { type: "words,chars" });
    gsap.from(splitInstance.chars, {
      y: 60, opacity: 0, rotateX: -40,
      stagger: 0.02, duration: 0.8, ease: "power3.out",
      scrollTrigger: { trigger: headingRef.current, start: "top 85%" }
    });
  }, sectionRef);
  
  return () => {
    splitInstance?.revert(); // Revert SplitText FIRST
    ctx.revert(); // Then revert GSAP context
  };
}, []);
```

**Word-break fix**: SplitText wraps each character in a `<span>`, which lets CSS break words at any character. Always use `type: "words,chars"` so words stay together. Also add this CSS globally:
```css
/* Prevent SplitText from breaking words mid-line */
[style*="display: inline-block"] {
  word-break: keep-all;
}
```

### The Four Layers

Every page should have all four running. Don't skip any:

1. **Ambient** — always moving, barely noticeable. Examples: noise grain overlay, subtle background color shift, waveform/particle pulse. 3-8 second loops.

2. **Reactive** — responds to mouse or scroll velocity. This layer is often the lightest — a cursor-following glow (mouse lerp at 0.08), subtle parallax on mouse move (5-15px range), or scroll velocity mapped to visual intensity. If you skip it entirely, the page still works — but it won't feel aware of the user. Even a simple mouse-position-to-CSS-variable is enough:
```js
document.addEventListener('mousemove', (e) => {
  document.body.style.setProperty('--mx', (e.clientX / window.innerWidth).toFixed(3));
  document.body.style.setProperty('--my', (e.clientY / window.innerHeight).toFixed(3));
});
```
Then use `var(--mx)` and `var(--my)` in CSS transforms for subtle movement.

3. **Narrative** — the scroll-driven story. This is the main content — pinned sections, choreographed reveals, the scroll journey itself.

4. **Detail** — micro-interactions. Hover states, link underline animations, button scale on press, cursor changes. These are last but not optional.

## Global Styles

Always include:

```css
/* Noise grain overlay */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.02;
  pointer-events: none;
  z-index: 9999;
}

/* Remove default smooth scroll — Lenis handles this */
html {
  scroll-behavior: auto !important;
}

/* Selection color matching accent */
::selection {
  background: var(--accent);
  color: var(--bg-primary);
}
```

## Quality Checklist

Before reporting the build as complete:

- [ ] Lenis smooth scroll is working (no jank on scroll)
- [ ] Every section has a different motion treatment
- [ ] No `linear` or default `ease` easing anywhere
- [ ] Headlines use SplitText character animation (body text does NOT)
- [ ] At least one pinned/scroll-scrubbed section exists
- [ ] Noise grain overlay at 2-4% opacity
- [ ] Dark theme backgrounds (#0a0a0a to #1a1a1a)
- [ ] 100vh+ breathing room between major moments
- [ ] `npm run build` compiles with zero errors
- [ ] Test in browser — scroll through entire page, verify all animations trigger
- [ ] No hydration mismatches (no Math.random or Date.now in render)
- [ ] prefers-reduced-motion respected (animations disabled for users who need it)

## What This Skill Does NOT Do

- Does not handle responsive adaptation (use `/scroll-adapt`)
- Does not diagnose broken animations (use `/scroll-debug`)
- Does not enforce consistency across sections (use `/scroll-normalize`)
- Does not push sections to extreme ambition (use `/scroll-overdrive`)
- Does not do final polish passes (use `/scroll-polish`)
