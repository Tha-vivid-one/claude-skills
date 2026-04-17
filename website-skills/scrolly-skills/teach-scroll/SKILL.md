---
name: teach-scroll
description: One-time setup that gathers scroll animation design context for your project and saves it to your AI config file. Run once to establish persistent scrollytelling guidelines — motion language, easing palette, timing rules, color system, typography scale, and the scroll journey structure. Use PROACTIVELY when starting any scroll-driven website project, or when the user mentions scroll animations, scrollytelling, or animated landing pages for the first time in a project.
user-invokable: true
---

Gather scroll animation design context for this project, then persist it for all future sessions. This is the foundation that every other scroll skill reads from.

## Step 1: Explore the Codebase

Before asking questions, scan the project thoroughly:

- **Package.json**: Is GSAP, Lenis, Framer Motion, or any animation library already installed?
- **Existing components**: Any scroll-driven sections already built? What patterns are they using?
- **CSS/Tailwind config**: Color palette, font stack, spacing scale, dark/light mode
- **Design docs**: Any design briefs, mood boards, brand guidelines, style guides in the repo or nearby
- **Config files**: `.impeccable`, `tailwind.config`, theme files — any existing design system tokens

Note what you found and what's missing.

## Step 2: Interview

STOP and ask the user these questions. Skip any you already answered from the codebase scan:

### Brand & Audience
- Who is this website for? What do they care about?
- 3 words that describe the brand personality
- Any reference sites that capture the right feel? (Specific URLs help — "like Linear's homepage" is more useful than "clean and modern")
- What should this explicitly NOT look like? Anti-references?

### Visual Direction
- Dark mode, light mode, or both?
- Primary accent color? (hex if they have it)
- Typography preference? (serif, sans-serif, mono accents, specific fonts)
- Any existing brand assets (logo, icon, color palette)?

### Scroll & Motion
- What's the scroll journey? Describe the "moments" — what should the user experience as they scroll?
- Fast and punchy or slow and cinematic?
- Any specific interactions they want? (pinned sections, text reveals, parallax, chaos-to-order, etc.)
- How much animation? (Subtle and restrained vs. every section has a wow moment)

### Technical
- Framework preference? (Next.js, Astro, vanilla JS + Vite)
- Any performance constraints? (mobile-first, specific devices, Core Web Vitals targets)
- Existing deployment? (Vercel, Netlify, self-hosted)

## Step 3: Build the Design Context

From the interview and codebase scan, synthesize into a structured design context. This is what every other scroll skill will read.

### The Context Document

Write this to the project's AI config file (`.claude/settings.local.json` or a `scroll-context.md` in the project root):

```markdown
# Scroll Design Context

## Brand
- Personality: [3 words]
- Audience: [who]
- References: [URLs]
- Anti-references: [what to avoid]

## Visual
- Theme: dark / light / both
- Background: [hex]
- Accent: [hex]
- Text primary: [hex]
- Text secondary: [hex]
- Font display: [name, weight]
- Font body: [name, weight]
- Font mono: [name] (if applicable)

## Motion Language
- Feel: [cinematic / punchy / dreamy / technical / playful]
- Easing palette:
  - Entrance: power2.out (0.6s)
  - Exit: power2.in (0.4s)
  - Headlines: power3.out with SplitText char stagger 0.02s
  - Scroll-linked: scrub: 1 (standard) or scrub: 2 (dreamy)
  - Hover: power2.out (0.2s)
  - Ambient: power2.inOut (3-8s loops)
- What NOT to do: [no bounce, no linear, no parallax on everything, etc.]

## Scroll Journey
- Moment 1: [description]
- Moment 2: [description]
- ...

## Typography Scale
- Display: clamp(3rem, 8vw + 1rem, 8rem), weight 300, letter-spacing -0.04em
- H1: clamp(2rem, 5vw + 0.5rem, 4rem)
- H2: clamp(1.25rem, 2vw + 0.5rem, 2rem)
- Body: clamp(1rem, 0.5vw + 0.875rem, 1.25rem), line-height 1.6
- Mono: 0.8125rem (filenames, data labels)

## Tech Stack
- Framework: [Next.js / Astro / Vite]
- Animation: GSAP + ScrollTrigger + SplitText
- Scroll: Lenis
- Styling: [Tailwind / CSS modules / vanilla CSS]
- Deployment: [Vercel / Netlify / other]

## Four-Layer Model
- Ambient: [what's always subtly moving — particles, grain, color cycling, waveform pulse]
- Reactive: [what responds to mouse/scroll — parallax, cursor glow, velocity effects]
- Narrative: [scroll-driven content reveals — pinned sections, choreographed entrances]
- Detail: [micro-interactions — hover states, cursor changes, link animations]
```

### Defaults

If the user doesn't have strong opinions on motion, use these battle-tested defaults (derived from analysis of Awwwards/Godly winners and creative studio practices):

- **Easing**: `power2.out` for entrances, `power3.out` for headlines, `scrub: 1` for scroll-linked, `power2.inOut` for ambient
- **Duration**: 0.15-0.3s for micro (hover), 0.4-0.8s for entrance, 0.6-1.2s for section transition, 1.0-2.0s for hero load
- **Spacing**: 100vh breathing room between major scroll moments. Pin for 150-300% viewport height.
- **Typography**: Display weight 300 (light, not bold), tight letter-spacing (-0.04em), body weight 400 minimum
- **Dark theme**: `#0a0a0a` deep background, `#1a1a1a` section backgrounds, 2-4% noise grain overlay
- **Text animation**: SplitText character stagger at 0.02s, `power3.out` — headlines only, never body text
- **Choreography**: Lead with most important element, overlap animations with `"-=0.2"`, vary the animated property per element (translateY for headings, scale for buttons, clip-path for images)

## Step 4: Confirm

Show the user the synthesized design context and ask if anything needs adjusting. Once confirmed, save it. Tell them:

"Design context saved. You can now use `/scrollytelling` to build the page, `/scroll-polish` to refine it, or any other scroll skill. They'll all read from this context."
