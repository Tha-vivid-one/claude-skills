---
name: progressive-summary
description: >-
  Lay a non-destructive "scan-layer" onto ONE long note the user explicitly
  points you at: bold the keeper sentences and ==highlight== the few
  keepers-of-keepers, leaving the note otherwise completely untouched
  (AI-assisted progressive summarization — it only ADDS emphasis and never
  rewrites, summarizes, condenses, deletes, or restructures). This is a
  deliberate, opt-in move, NOT an ambient one. Trigger only when the user clearly
  asks to emphasize/mark up a specific note in place for faster rereading or
  skimming — e.g. "/progressive-summary", "progressive summarize this", "lay a
  scan-layer on this", "bold the keepers and highlight the essence", "mark up
  this transcript so I can reread it fast". Operate ONLY on the single note or
  section they name; never auto-run, never pick the target yourself, never touch
  other notes. Do NOT trigger merely because a long transcript or article is
  mentioned, and explicitly do NOT trigger for: summarize / condense / shorten /
  TL;DR (those rewrite), extracting content into a separate note, splitting a
  note into atomic notes, answering "what are the key takeaways" in chat,
  cleaning up or reformatting prose, or anything aimed at the user's own evolving
  journal / working / trade notes. When unsure, do NOT trigger — this is invoked
  deliberately, so under-triggering is the safe failure.
---

# Progressive Summary

## What this is, and why it works

Progressive summarization lays a *scannable* layer over a long note **without changing a word of it**. You bold the load-bearing sentences (Layer 2), then highlight the few that are the absolute essence (Layer 3). Future-you then reads the note at three depths:

- **highlights only** → the ~10-second essence
- **highlights + bold** → the full argument in ~30 seconds
- **drop into the raw prose** → only where a section earns it

The reason this beats rewriting a note into a summary: the note stays **whole**. Nothing is lost, the author's voice and the surrounding context remain, and the full thing is always there to reread. You're adding a fast path, not paving over the road. (It's the deliberate opposite of breaking a note into atomic fragments — keep it intact.)

This is best on long *source* material the user wants to revisit — podcast/NotebookLM transcripts, saved articles, research dumps — especially before a second read-through.

## Core rules — these *are* the skill, don't break them

- **Add only.** Wrap text in `**bold**` and `==highlight==`. Never reword, summarize, delete, reorder, or "fix" typos or links. The entire value is that it is still the original note, just easier to scan — it must be fully reversible, so a `git checkout` or undo restores the original exactly.
- **Only touch what you're pointed at.** Mark up the specific file or section the user named — nothing else. Don't go looking for other notes, and never run on your own initiative.
- **Don't over-mark.** If everything is bold, nothing is. Over-marking is the most common failure. Aim for roughly **10–20% of the body** bolded, and of *that*, roughly **10–20% highlighted**. When in doubt, mark less.
- **Leave existing distillations alone.** Source notes often already carry a hand-written summary or an already-highlighted block (frequently at the top). Don't re-mark those — aim the layer at the raw body. If it's genuinely ambiguous which part to mark, ask before editing.

## Procedure

1. **Read the target** the user pointed you at. If they named a section ("the article part", "just section III"), scope to exactly that.
2. **Check for an existing distillation.** Multi-section notes often stack a hand-written highlights block + a worksheet/template + the raw source. Mark up the raw source; skip what's already distilled, and say which part you worked on.
3. **Bold the keepers (Layer 2).** Pick the sentences that carry the argument — the ones that, read alone in order, deliver the whole point. Bold the meaningful clause, not the throat-clearing around it. Spread them across the *whole* piece so scanning the bold traces the full arc, not just the opening.
4. **Highlight the keepers-of-keepers (Layer 3).** From the bolded set, choose the **4–8** lines that are the irreducible essence — the thesis, the turn, the line you'd quote on a card. Wrap those in `==...==`.
5. **Report the spine** (see *Report format* below) so the user gets the payoff without reopening the file.

## Choosing what counts as a "keeper" — the judgment that matters most

A keeper isn't merely an *interesting* sentence — it's one that does **work in the argument**: the claim or thesis, a definition, the turn ("but here's the real reason…"), an actionable instruction, or a memorable formulation. Skip setup, illustrative examples of a point you already bolded, transitions, and hedging.

The test: **read only the bolded sentences, top to bottom — do you get the argument?** If yes, you bolded the right ones. If you get a disconnected highlight reel, rebalance (usually you over-bolded the first section and under-bolded the rest).

A *keeper-of-keepers* is the line you'd put on a flashcard — the one that survives if everything else is forgotten. There should only be a handful per piece. If you're highlighting a dozen, you're really just bolding again — pull back.

## Editing safely (you're making many small wraps in one file)

- **Match a unique substring for each wrap.** On long notes short phrases repeat, so include enough surrounding words to be unambiguous.
- **On multi-section notes, target the body's wording.** When the same idea appears in both a summary block and the raw prose, match the prose version (usually longer / phrased differently) so you mark the right occurrence and don't fail on a non-unique match.
- **Preserve exact characters.** Copy curly quotes (`'` `"` `"`), em dashes (`—`), and the user's own `[single-bracket]` link convention verbatim — don't normalize them, or the match will miss and the text will drift.
- **Wrap at clean boundaries.** Bold/highlight render across a *soft* line break inside one paragraph, but don't span a blank line (that's two paragraphs) — wrap each part separately instead.

## Report format

After the pass, ALWAYS surface the essence back in chat so the user gets value immediately:

> Scan-layer's on **[note]** — [N] bold keepers tracing the argument, [M] `==highlighted==` as the essence. (Worked the [raw article body / section X]; left your existing [Highlights block] untouched.)
>
> The keepers-of-keepers — your reread spine:
> 1. ==…==
> 2. ==…==
> … (4–8 total)
>
> Reread path: scan the highlights → scan the bold → drop into full prose only where a section grabs you. Nothing deleted, fully reversible.

## What NOT to do

- **Don't rewrite or "clean up" the prose.** If you feel the urge to improve a sentence, stop — that's a different task and it breaks the one promise this skill makes.
- **Don't add a TL;DR, summary paragraph, or new headers** unless asked. The whole bet is that emphasis-*in-place* beats a separate summary.
- **Don't touch frontmatter.**
- **Don't mark up the user's own evolving working notes** (journals, trade logs, drafts) unless they explicitly point you there — those are theirs to develop, not yours to annotate.