---
name: debrief
description: After a session where the user got lost or kept asking why, find those moments, work out whose gap each one was, and point every real learning gap to the right kind of material for that exact question, such as a one-line answer, the tool's own docs, a short explainer, the newest research, a book, or the person to ask. Use when the user says "/debrief", "debrief this session", "what should I learn from this", "where did we misunderstand each other", or at the end of a session full of "what does this mean", "why?" and "what if we..." moments. Also runs on a past session given its id.
---

# Debrief

The questions someone asks in the middle of building are the best syllabus they have.
Every "what does this mean" or "why does it have to be like that" marks a gap at the moment
it mattered. This skill finds those moments, works out whose gap each one was, and sends
each real learning gap to the right kind of material for that exact question. It is not a
curriculum: some gaps need one sentence, some need one docs page, some need this month's
research, and only a few need a book.

The rule behind it: **code finds the moments, Jev sorts them and picks the channel, you find
and check the source, the user decides.** A moment where the agent talked past the user is
the agent's fault, not the user's homework.

## Run it

```bash
python3 ~/.claude/skills/debrief/debrief.py find                       # this session
python3 ~/.claude/skills/debrief/debrief.py find <id-or-prefix>         # a past session
python3 ~/.claude/skills/debrief/debrief.py find <id-or-prefix> --wide  # every question counts
python3 ~/.claude/skills/debrief/debrief.py find <id-or-prefix> --test  # testing the skill
```

The output is JSON: each moment with the user's words, the end of the agent message before
it, Jev's numbers, a bucket, a channel, a topic, and what the learning log already holds
(`past_terms`, `past_picks`). A run costs a fraction of a cent and a few seconds. `--wide`
treats every question the user asked as a candidate, which suits long or curious sessions.
`--test` keeps the run out of the count that drives leveling up.

If the notes say Jev didn't run (no `TYPESAFE_API_KEY`, or an API error), every moment is
`unsorted`: sort them yourself with the same buckets and channels, and say once that Jev
was off.

## The channels

Jev picks one channel per moment. Use it unless it is plainly wrong for the question.

- **quick_answer**: answer it in one sentence. Nothing to read.
- **tool_docs**: the exact page in that tool's own documentation. Search the tool's official
  docs for the user's exact question, open the page to confirm it covers it, and name the
  page (and the section, if it has one).
- **explainer**: one short article or video about that exact idea. Search the term plus a
  few words from the user's question, not the broad topic. Prefer a focused piece that
  answers this question over a famous general one.
- **latest**: the newest research, paper, report or write-up. Search with the current
  month and year, prefer the last six months, and always show the date.
- **deep_study**: a book or course. Use `library_menu` when it has a fit. Otherwise search
  for one widely recommended for exactly this skill, and check it exists.
- **ask_someone**: who to ask and the exact question to put to them. Nothing to read.

## Finding the source

- Search the user's own words plus the term. Two different questions on the same topic
  should get two different picks.
- Check `past_picks`. Don't recommend a source again unless it's the same gap again; if it
  is, say "second time" and offer a different format (a video if it was an article).
- Only show a link that came back from a search or that you opened. Never guess a URL, a
  chapter, a page number or an episode.
- Keep queries short: the term and a few words. Never put secrets, names, or pasted text
  from the session into a search.

## Write the debrief

Short bullets, no preamble, no recap. Skip any empty section.

**Worth learning** (at most three things to read, watch or listen to; quick answers and
people to ask don't count toward the three)
- Built from `worth_learning` moments. Several moments about the same thing share one pick;
  quote the clearest.
- The user's words from the moment, quoted short, then one plain sentence that answers it
  right there, so they learn it even if they never open the pick.
- Then the pick, labeled by channel: `[Docs]`, `[Explainer]`, `[Latest, Month YYYY]`,
  `[Book]` or `[Course]`, or `[Ask <who>]`, with the title and link, or the exact question
  to ask.
- If the term is in `past_terms`, say "second time" (or "third time, worth a proper
  sit-down"). Repeats matter more than new gaps.

**The agent talked past you** (at most three)
- Built from `agent_talked_past` moments and any moment whose `also` lists it. A learning
  gap the agent also buried in jargon belongs in both sections.
- The term or habit (an unexplained acronym, a wall of text, the same fact said three times,
  a misread request) and a one-line instruction that would have prevented it. Offer it for
  memory or CLAUDE.md; don't write it anywhere unless the user says so.

**How to ask next time** (at most two)
- For a `how_to_ask` moment: one line on the wording that would have avoided it.

`one_off` moments get a one-line answer at most, no pick. A moment whose `also` lists
`near_learning` scored just under the learning bar: give the one-sentence answer, no pick.
`noise` is hidden; don't mention it.

If nothing survives, say "Nothing worth studying from this one" and stop.

## Log it

After a debrief of the **current** session, append one line per worth-learning moment,
quick answers included, so the log captures the whole process. The path is `log.path` in
the output (set in `config.json`; the default is `~/.claude/debrief/learning-log.md`).
Write nowhere else. If the note or its folder doesn't exist, create it with a short header.
Use this exact shape so the script can count repeats:

```
- 2026-09-25 · channel: explainer · topic: subscription_economics · term: expected lifetime · pick: <title> (<link>) · session: 1a2b3c4d
```

A quick answer logs as `pick: answered inline`. When debriefing a past session with
`--test`, don't log unless the user asks.

## Level up

The output prints `runs_so_far`. At every fifth run, read `PROGRESSION.md` (and
`PROGRESSION.local.md` if it exists) and add one line at the end of the debrief: which
level the skill is at and the single change the runs now justify. Don't change triggers,
questions, thresholds, channels or the library without a run that shows the need.

## What leaves the machine

Only the flagged moments go to TypeSafe, each as three trimmed strings: the end of the
agent's message, the user's reply, and the user's earlier request. Keys, tokens, webhooks
and emails are redacted in code first. Web searches carry only short queries. Whole
transcripts never leave the machine. Run records stay in `runs/`, which git ignores.

## Setup

- `TYPESAFE_API_KEY` in the environment or the shell profile (Jev is TypeSafe's model).
- Optional `config.json` beside this file, shaped like `config.example.json`: where the
  learning log lives, and one line on who the user is.
- Optional `library.md` for the deep-study channel, shaped like `library.example.md`. Its
  subjects are also the topics Jev sorts moments into.
