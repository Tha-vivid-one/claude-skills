# Scrollytelling Skill Suite

Build award-winning scroll-driven animated websites with GSAP, Lenis, and ScrollTrigger. A coordinated set of 7 skills that take you from design context to polished scrollytelling experience.

## Skills

| Skill | Command | What It Does |
|-------|---------|-------------|
| **teach-scroll** | `/teach-scroll` | One-time setup — interviews about brand, gathers design docs, saves scroll design context |
| **scrollytelling** | `/scrollytelling` | Main builder — takes a design brief, builds the full Next.js page with animations |
| **scroll-polish** | `/scroll-polish` | Final quality pass — fixes timing, easing, spacing, choreography details |
| **scroll-overdrive** | `/scroll-overdrive` | Push a section past limits — shaders, parallax, physics, cinematic sequences |
| **scroll-debug** | `/scroll-debug` | Diagnose and fix — jank, hydration, ScrollTrigger conflicts, mobile issues |
| **scroll-adapt** | `/scroll-adapt` | Responsive — make scroll animations work across screen sizes and devices |
| **scroll-normalize** | `/scroll-normalize` | Consistency enforcer — same motion language, easing, timing across all sections |

## The Flow

```
/teach-scroll          → Set up design context (run once per project)
    ↓
/scrollytelling        → Build the page
    ↓
/scroll-normalize      → Enforce consistency
    ↓
/scroll-debug          → Fix any issues
    ↓
/scroll-polish         → Final quality pass
```

Use `/scroll-overdrive` on specific sections you want to push further.
Use `/scroll-adapt` when desktop is solid but mobile needs work.

## Tech Stack

- **GSAP** (v3.15+, free) — ScrollTrigger, SplitText, Flip, all plugins
- **Lenis** (3KB) — smooth scroll
- **Next.js** — App Router, TypeScript, Tailwind CSS
- **Vercel** — deployment

## Key Concepts

### The Four-Layer Model

Every page should have all four layers running:
1. **Ambient** — always subtly moving (grain, color shifts, pulse animations)
2. **Reactive** — responds to mouse/scroll (parallax, cursor glow, velocity effects)
3. **Narrative** — scroll-driven story (pinned sections, choreographed reveals)
4. **Detail** — micro-interactions (hover states, link animations, cursor changes)

### Motion Variety

Every section gets a DIFFERENT primary animation technique — character reveal, scroll-scrub, stagger entrance, sticky panel, directional slides, scale overshoot, SVG mask reveal, chaos-to-order.

### Easing Palette

- Entrances: `power2.out`
- Headlines: `power3.out` + SplitText char stagger 0.02s
- Scroll-linked: `scrub: 1` (standard) or `scrub: 2` (dreamy)
- Hover: `power2.out`, 0.2s
- Ambient: `power2.inOut`, 3-8s loops
- Never: `linear`, default CSS `ease`

## Install

Copy the skill folders into `~/.claude/skills/`:

```bash
cp -r scrolly-skills/* ~/.claude/skills/
```

Or install individual skills:

```bash
cp -r scrolly-skills/scrollytelling ~/.claude/skills/
```

## Works With

- [gsap-core, gsap-scrolltrigger, gsap-timeline, gsap-plugins, gsap-react](https://github.com/greensock/gsap-skills) — official GSAP skills from GreenSock
- [impeccable](https://github.com/pbakaus/impeccable) — UI/UX skill suite (complementary, not competing)

## License

MIT
