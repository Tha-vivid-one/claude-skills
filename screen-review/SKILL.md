---
name: screen-review
description: Review one screen or component of a web app on the real running app, at phone size and in every theme, and say why it reads off and the exact tweak for each problem. Runs Impeccable's critique, distill, layout, typeset, clarify and audit as four independent lenses (eyes, structure, words, code), merges and ranks them, then fixes or offers concept options, and confirms once. Use when someone says a screen "reads wrong", asks what is off with a screen, shares a screenshot of a screen, or asks to improve one.
argument-hint: "<screen or component> [what bothers you]"
---

# /screen-review

Four lenses look at one screen state without seeing each other. You merge what they find, rank it, and hand back what is off plus the tweak for each. Then fix, or show options, and confirm once. One review, one fix batch, one confirm round, then stop. Impeccable's own rule is "verify in bounded passes, not a loop"; run the skill again for another pass.

Needs the Impeccable skill (`impeccable@impeccable` plugin), Chrome and Node 22+.

## 1. Set up

- `IMP=$(ls -d ~/.claude/plugins/cache/impeccable/impeccable/*/skills/impeccable | sort -V | tail -1)`
- Find the project's own sources of truth and note their paths:
  - its design doc (DESIGN.md, a design-system doc, the token file)
  - its rules (CLAUDE.md, AGENTS.md, a contributing guide)
  - its copy rules, if any
  - any list of routes and states (a dev overlay, a storybook, a routes file)
- Review what users run. If the working tree is not the production branch, `git fetch` and use a detached worktree at `origin/<production branch>`. Never edit in it.
- Resolve the target:
  - the route
  - a JS snippet that reaches the state (usually one click)
  - the element's selector
  - the source files: screen, components, styles
- Work out how the app sets its theme and any gate before the screen, such as onboarding or sign-in. That is the `--seed` for the capture.
- If the person attached a screenshot, it is evidence, and their device is the reference.
- `RUN=${TMPDIR:-/tmp}/screen-review/<slug>/<YYYY-MM-DDTHH-MM>`

## 2. Capture (code, once)

`node <skill dir>/capture.mjs --url <dev server> | --root <static dir> --route '#/x' --do "<js>" --target '<selector>' --seed "<js>" --out $RUN`

This writes `base|state|target.<theme>.png`, `facts.<theme>.json` and `console.json`:
- every text run with its font, contrast and whether it is clipped
- every control with its size, state and whether something covers it
- anything that paints over the target

Look at one `state.*.png` yourself before you go on. If it is not the state you meant, fix `--do` or `--seed` and capture again. For more states (empty, a filter on, an error), capture each into a subfolder. Pass `--expect '<regex>'` for console lines the project always produces locally, such as a missing backend on a static server.

## 3. Four lenses, in parallel, isolated

Spawn four agents in one message. None sees another's output.
- Do not pass the person's complaint to any lens. It is checked in step 4, so the lenses stay an honest test.
- Every lens reads the project's design doc and `$IMP/reference/craft-floor.md`, plus the files below.

The lenses:
- **Eyes.** Reads the PNGs and the person's screenshot only: no code, no facts. References: `$IMP/reference/critique.md` (Assessment A, cognitive load, heuristics) and `distill.md`. Answers: what a person reads first, what reads wrong, what competes, and what does not earn its place. Also scores Nielsen's ten heuristics as a total out of 40.
- **Structure.** Reads the PNGs, the facts and the styles. References: `layout.md`, `typeset.md`, `operate.md`. Answers: reading order, the columns and edges (`summary.leftEdges`/`rightEdges`), grouping, rhythm, type roles, and overlaps.
- **Words.** Reads every string in the facts and the source, in every state. Reference: `clarify.md`, plus the project's copy rules.
- **Code.** Reads the source, facts, console, and the output of `"$IMP/scripts/impeccable" detect --json <markup files>`. References: `audit.md`, `harden.md`, `adapt.md`. Covers: contrast in every theme, tap targets, covered or clipped controls, states the capture did not reach, token use, and the project's rules. Entries marked `expected` in the console are known noise.

Each lens returns at most six findings, one line each:

`[P0-3] what's off | why it matters to the person using it | tweak: the concrete change (CSS, copy, structure) | evidence: png + region, file:line, or facts field | fix or taste`

Eyes also returns a one-line gut read and the Nielsen total.

## 4. Merge

- When two or more lenses report the same issue, make it one finding and say how many saw it.
- Drop a finding with no evidence, or one whose rule does not apply to this screen.
- If a tweak contradicts the design doc, the token file, or a dated decision recorded in a code comment, keep the finding and name the conflict. Never pick silently, and never propose a token change the project says needs sign-off; flag it instead.
- If the person named a complaint, say which lenses found it unprompted. If none did, say that.
- Rank in this order: blocks the task, misleads, reads wrong, polish.

## 5. Report

Short bullets. No tables and no essay.

- At most eight lines of **what's off** → tweak, with the lenses and evidence in brackets.
- Then one line with the score out of 40, and the trend if an earlier critique exists.
- Persist the report so `/impeccable polish` reads it as its backlog:

`IMPECCABLE_CRITIQUE_META='{"target":"<words>","total_score":N,"max_score":40,"na_heuristics":"","p0_count":N,"p1_count":N}' "$IMP/scripts/impeccable" critique-storage write <main source file> <body file>`

Delete the body file afterwards.
- Then ask one multi-select question: which findings to act on.

## 6. Act, then confirm once

- **Fix items.** Read the matching reference (`layout.md`, `typeset.md`, `clarify.md` or `polish.md`), then `craft-floor.md`, right before editing. Apply them as one batch on a branch off the production branch.
- **Taste items.** Get the person options and let them choose the direction:
  - **Concept previews.** This is the default. Plan three variants the way `$IMP/reference/live.md` section 4 does: an identity lock first, then three different primary axes. Draw each one inside the real app: pass `capture.mjs --do` a script that opens the component and redraws it with the app's own tokens. Capture every theme and lay them out side by side, for example with `magick montage`. Previews only; build the one picked.
  - `/impeccable generate`: live variants in the browser. Check it runs first: some engine versions list it but answer "verb 'live-generate' is not implemented yet", and `impeccable live` refuses to start without `PRODUCT.md` and `DESIGN.md` at the repo root.
- **Confirm.** Capture the same states again and rerun only the lenses that raised the fixed findings. Report what cleared and what did not. Then run the project's own verify steps and stop.
