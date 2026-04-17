---
name: scroll-overdrive
description: Push scroll-driven sections past conventional limits with technically ambitious implementations — shader-based transitions, scroll-velocity-reactive visuals, advanced parallax, WebGL backgrounds, physics-based animations, or cinematic pinned sequences. Use when a section works but needs to make someone stop and say "how did they do that?"
user-invokable: true
args:
  - name: target
    description: The specific section or component to push into overdrive
    required: false
---

Take a section of a scroll-driven website and push it to award-winning territory.

## Before You Start

1. Read the scroll design context for this project
2. Identify the target section — if the user didn't specify, ask which section they want to elevate
3. **Propose 2-3 directions before building.** This skill has the highest potential to misfire. A shader background on a pricing section is embarrassing. The same shader on a hero section wins Awwwards. Context matters.

STOP and ask the user which direction they prefer before writing code.

## Techniques Available

Listed from most impactful to most subtle:

### Scroll-Velocity Reactive Visuals
Map scroll speed to visual intensity. Faster scroll = more energy, slower = calmer:
```js
ScrollTrigger.create({
  onUpdate: (self) => {
    const velocity = Math.abs(self.getVelocity()) / 1000;
    gsap.to(element, { blur: velocity * 2, duration: 0.3 });
  }
});
```

### Chaos-to-Order Physics
Elements start scattered with pseudo-random positions, compress and snap into organized layout on scroll:
```js
elements.forEach((el, i) => {
  // Start state: chaos
  gsap.set(el, {
    x: (Math.sin(i * 127.1) * 43758.5453 % 1 - 0.5) * window.innerWidth * 0.8,
    y: (Math.cos(i * 269.5) * 43758.5453 % 1 - 0.5) * 400,
    rotation: (Math.sin(i * 43.1) * 100 % 1 - 0.5) * 30,
    opacity: 0.3 + Math.random() * 0.4,
  });
  // End state: order (driven by scroll)
  ScrollTrigger.create({
    trigger: container, scrub: 2,
    start: "top center", end: "bottom center",
    onUpdate: (self) => {
      gsap.to(el, { x: targetX[i], y: targetY[i], rotation: 0, opacity: 1, duration: 0.3 });
    }
  });
});
```

### SVG Mask Reveals
Content revealed through animated SVG masks — blinds, wave patterns, radial reveals:
```js
gsap.to(maskRects, {
  scaleX: 1, stagger: { from: "random", each: 0.05 },
  scrollTrigger: { trigger: section, scrub: 2, pin: true }
});
```

### Shader Gradient Backgrounds
Animated gradient mesh that responds to scroll position (use ShaderGradient library or custom CSS):
```css
.shader-bg {
  background: conic-gradient(from calc(var(--scroll) * 360deg),
    var(--accent) 0%, transparent 30%, var(--accent) 60%, transparent 100%);
  filter: blur(80px);
  animation: rotate 20s linear infinite;
}
```

### Advanced Parallax with Depth
Multi-layer parallax where elements move at different rates based on their "depth":
```js
layers.forEach((layer, i) => {
  const speed = 1 - (i / layers.length); // 1.0 (back) to 0.0 (front)
  gsap.to(layer, {
    y: () => -speed * ScrollTrigger.maxScroll(window) * 0.3,
    ease: "none",
    scrollTrigger: { trigger: section, scrub: true }
  });
});
```

### Cinematic Text Sequences
Words that assemble, morph, or sequence dramatically:
```js
const tl = gsap.timeline({ scrollTrigger: { trigger: section, scrub: 1, pin: true, end: "+=300%" }});
tl.from(word1Chars, { y: 100, rotateX: -90, stagger: 0.02, duration: 1 })
  .to(word1Chars, { y: -100, opacity: 0, stagger: 0.01, duration: 0.5 }, "+=0.5")
  .from(word2Chars, { scale: 3, opacity: 0, stagger: 0.03, duration: 1 }, "-=0.3");
```

## Rules

- Every overdrive enhancement must serve the content, not distract from it
- Performance budget: still 60fps after the enhancement
- Test on a real device, not just your dev machine
- If it doesn't make someone stop and look, it's not overdrive — it's decoration
- Provide a `prefers-reduced-motion` fallback that still looks intentional, not broken
