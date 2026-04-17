---
name: teach-scroll
description: One-time setup that gathers scroll animation design context AND brand voice for your project. Run once to establish persistent scrollytelling guidelines — motion language, easing palette, timing rules, color system, typography scale, scroll journey structure, AND brand story, voice, tone, copy direction. Use PROACTIVELY when starting any scroll-driven website project, or when the user mentions scroll animations, scrollytelling, or animated landing pages for the first time in a project.
user-invokable: true
---

Gather scroll animation design context AND brand voice for this project, then persist both for all future sessions. This is the foundation that every other scroll skill reads from.

## Phase 1: Explore the Codebase

Before asking questions, scan the project thoroughly:

### Design & Visual
- **Package.json**: Is GSAP, Lenis, Framer Motion, or any animation library already installed?
- **Existing components**: Any scroll-driven sections already built? What patterns are they using?
- **CSS/Tailwind config**: Color palette, font stack, spacing scale, dark/light mode
- **Design docs**: Any design briefs, mood boards, brand guidelines, style guides in the repo or nearby
- **Config files**: `.impeccable`, `tailwind.config`, theme files — any existing design system tokens

### Brand & Copy
- **README.md**: Does it explain what the product does and why? Note the tone.
- **Marketing copy**: Any existing landing pages, about pages, taglines, slogans?
- **Messaging docs**: Brand voice guides, tone documents, copy guidelines?
- **Product docs**: PRDs, WHY docs, pitch decks — anything explaining the product story?
- **Social/content**: Blog posts, tweets, social media copy that shows the brand voice?
- **Humanizer profiles**: Check `~/.claude/humanizer-profiles.yaml` — the user may have existing voice profiles for different projects.

Note what you found and what's missing. Pay attention to whether existing copy sounds human-written or AI-generated.

## Phase 2: Evaluate Existing Copy

If you found brand/copy documents, evaluate them:

### AI Copy Detection
Read any existing marketing copy, taglines, or brand docs and look for signs of AI-generated writing:
- Inflated symbolism ("revolutionize," "transform," "empower")
- Em dash overuse
- Rule of three everywhere
- Vague attributions ("experts say," "studies show")
- Promotional superlatives ("cutting-edge," "industry-leading," "best-in-class")
- Negative parallelisms ("not just X, but Y")
- Excessive conjunctive phrases ("moreover," "furthermore," "additionally")
- Every sentence the same length and structure

**If AI patterns detected**, flag them to the user:
"I found brand docs but some sections read AI-generated. A few options:
A) Use them as-is (fine for internal docs or if the tone works)
B) Humanize them — I can run them through the copywriter lens to make them sound more natural
C) Start fresh — let's talk about your voice and write new copy from scratch
D) Mix — keep what works, rewrite what doesn't"

**If copy sounds human-written**, note it as the voice reference: "Your existing copy has a clear voice — [describe it]. I'll use this as the reference for the website copy."

### Check Humanizer Profiles
Look for `~/.claude/humanizer-profiles.yaml`. If it exists, check if any profile matches this project:
- Match by project name or path patterns
- Note the voice profile (technical-professional, thought-leader, conversational, etc.)
- Ask the user: "I found a humanizer profile called '[name]' — should I use this voice for the website copy?"

If no profiles exist, that's fine — we'll establish the voice in the interview.

## Phase 3: Interview

STOP and ask the user these questions. Skip any you already answered from the codebase scan. Split into two parts:

### Part A: Visual & Motion (skip if docs already cover this)

**Brand & Audience**
- Who is this website for? What do they care about?
- 3 words that describe the brand personality
- Any reference sites that capture the right feel?
- What should this explicitly NOT look like?

**Visual Direction**
- Dark mode, light mode, or both?
- Primary accent color?
- Typography preference?

**Scroll & Motion**
- What's the scroll journey? Describe the "moments"
- Fast and punchy or slow and cinematic?
- Any specific interactions they want?

**Technical**
- Framework preference?
- Performance constraints?
- Deployment?

### Part B: Brand Story & Voice (always ask, even if docs exist)

**The Story**
- Why does this product exist? What's the origin — what problem pissed you off enough to build this?
- What's the pain point in the user's own words? (Not marketing language — how do real people actually describe this problem? Reddit quotes, Slack messages, things your friends say)
- What's the one sentence that would make someone stop scrolling?
- What makes you different from the obvious alternatives? (Not feature comparison — the real reason someone picks you)

**The Voice**
- How do you talk about this product to a friend? (Not in a pitch deck — at a bar, casually)
- Any slang or insider language your audience uses? (Producer slang, dev jargon, industry terms that signal "this person gets it")
- Words you'd NEVER use to describe your product? (e.g., "revolutionary," "cutting-edge," "synergy")
- Show me a headline you love from any product. What do you like about it?

**AI Copy Tolerance**
- Is it OK if the website copy sounds polished/professional (AI-assisted), or does it need to sound like a specific person wrote it?
- If you have a strong voice preference — whose writing style should this sound like? (Could be the user's own writing, a specific brand, a public figure)
- Any existing writing from you that captures how you want this to sound? (Tweets, blog posts, Slack messages, anything)

## Phase 4: Build the Design Context

From everything gathered, produce TWO documents:

### Document 1: scroll-context.md

Save to project root. Same structure as before:

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
- Ambient: [description]
- Reactive: [description]
- Narrative: [description]
- Detail: [description]
```

### Document 2: brand-voice.md

Save to project root alongside scroll-context.md:

```markdown
# Brand Voice Guide

## The Story
- Origin: [why this exists — the real story, not the pitch]
- Pain point: [in the user's actual words]
- One-liner: [the sentence that makes someone stop scrolling]
- Differentiator: [the real reason someone picks this, not feature bullets]

## Voice Rules
- Tone: [direct / playful / technical / warm / confident / casual]
- Person: [first person "we" / second person "you" / third person]
- Sentence length: [short and punchy / varied / long and flowing]
- Humor: [yes — dry / yes — playful / no / occasional]

## Words We Use
- [list of words, phrases, slang that sound like us]

## Words We NEVER Use
- [list of banned words — "revolutionary," "cutting-edge," etc.]

## Example Headlines (Sound Like Us)
- "[example 1]"
- "[example 2]"
- "[example 3]"

## Example Headlines (DON'T Sound Like Us)
- "[anti-example 1]"
- "[anti-example 2]"

## AI Copy Policy
- [OK to use AI-assisted copy / needs human voice / mixed — AI for body, human for headlines]
- Humanizer profile: [profile name from ~/.claude/humanizer-profiles.yaml, if applicable]
- Reference writing: [link to existing writing that captures the voice]

## Copy for Each Scroll Moment
For each moment in the scroll journey, draft the key copy:
- Moment 1 headline: "[draft]"
- Moment 1 subtext: "[draft]"
- Moment 2 headline: "[draft]"
- ...

Mark each as: ✅ approved / 🔄 needs user review / ✍️ user should write this
```

### Defaults for Voice

If the user doesn't have strong voice opinions, use these defaults:
- **Tone**: Direct, confident, no fluff
- **Banned words**: revolutionary, cutting-edge, seamless, robust, leverage, synergy, empower, utilize, innovative, best-in-class, industry-leading, game-changing
- **Sentence length**: Short. Punchy. One idea per sentence.
- **Person**: Second person ("you") for the user, first person ("we") sparingly
- **Humor**: Occasional — earned through specificity, not forced jokes
- **AI policy**: AI-assisted body copy OK, headlines should feel human-written

## Phase 5: Confirm

Show the user both documents and ask:
1. Does the visual/motion context look right?
2. Does the voice guide capture how you actually talk?
3. Are the draft headlines close or do they need rewriting?
4. Anything that sounds too AI / too corporate / too casual?

Once confirmed, save both files. Tell the user:

"Design context and brand voice saved. `/scrollytelling` will use both to build the page. Headlines marked 🔄 or ✍️ are placeholders — you can replace them before or after the build."
