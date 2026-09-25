# Leveling up /debrief

The skill makes four guesses. It guesses which messages are worth a look, from phrases
people use when they're lost or curious. It guesses where the lines sit between "worth
learning", "the agent talked past you", "how to ask" and noise, from five thresholds on
Jev's answers. It guesses the channel, meaning what kind of material fits each question. And
it guesses the source, from a web search shaped by the user's own words. Each level below
replaces one of those guesses with evidence from real runs. Change one thing per level, and
only when a run shows the need. Skills like this break by growing a paragraph at a time with
no test behind each addition.

If `PROGRESSION.local.md` exists beside this file, it holds this install's own findings and
the past sessions to re-run after any change. Read it together with this one.

## Level 0: where it starts

Code finds moments by phrase: confusion ("what does this mean"), curiosity ("why?", "what if
we...", "does it have to be like that?") and mismatch ("I never said that"). Jev answers
five yes/no questions per moment and picks a channel and a topic. Claude finds the source
for each channel, checks that it exists, and writes the debrief. Every learning moment goes
into the learning log, quick answers included, and every run is saved in `runs/`, which is
what the higher levels read.

## Level 1: trust the finder (after about five real runs)

Open the run files for five sessions and read the flagged moments. Mark each one as a real
learning moment or not. Then skim one of those sessions by eye for questions the phrases
missed. Two things come out of that: phrases that keep firing on plain instructions (drop
or tighten them), and ways the user asks that the list doesn't know (add them). If misses
keep costing real moments, make `--wide` the default: every question becomes a candidate
and Jev sorts out the rest. It costs a few more calls and nothing else.

A numbered reply can hide a real question inside one line. If that keeps happening, split
numbered replies into separate moments before they reach Jev.

## Level 2: tune the sort and the channel (after about ten real runs)

Put Jev's numbers beside the marks from Level 1. If real moments sit at 0.4 on `confused`
or `curious`, lower that bar; if noise sits at 0.6, raise it or rewrite the question. Jev's
numbers move by up to about 0.15 between identical runs, so don't tune finer than that.

Count how often the channel was overridden, and which way. If "explainer" keeps getting
swapped for "tool_docs", the channel descriptions need examples in the user's own phrasing.
The topic question has the same weakness: it misses when the gap isn't named in the user's
words. Rewrite a question only by the rules for asking Jev well: one property per question,
both sides of any comparison in the state, nothing the code already knows. This is also when
to write the marked moments into an `eval-cases.json`, so every later change has a score to
beat.

## Level 3: learn what lands (once about a dozen picks are in the log)

Add a one-word status to each log line when the user gets to it: done, skipped, or not
useful. After a dozen picks the pattern shows, by channel and by format. Maybe docs pages and
short videos get finished and books don't; maybe "latest" picks go unread. Teach the
debrief to prefer what lands.

## Level 4: keep it fresh and varied (ongoing)

Three numbers keep the picks from turning into the same list:

- **Repeat rate**: the share of picks that were already in `past_picks`. If it climbs, the
  searches are too broad. Tighten them around the user's exact words.
- **Variety**: how many different sources a month of picks came from. A handful of sites
  answering everything means the search has a favorite.
- **Freshness**: the age of "latest" picks. Anything older than six months isn't the
  latest.

A deep-study pick that the user finished and found useful goes into `library.md`. The
library holds only what proved itself, not what a syllabus thinks someone needs.

## Level 5: fix the agent side (when the same kind of talking-past repeats)

When "the agent talked past you" keeps landing on the same habit, such as unexplained
acronyms, walls of text, or saying one fact three times, turn the one-line fix into a memory
or CLAUDE.md rule, with the user's OK. Then watch whether that kind of moment drops in later
runs. If it does, the skill is fixing both sides of the conversation, which is the real
goal. The bullets that are really about how the user wants to be spoken to can also feed a
taste or style rules file, with approval.

## Level 6: check it landed (optional)

When a term shows up in the log a second time, the next debrief asks the user to explain it
in one sentence before pointing anywhere. If they can, mark it learned and stop suggesting
it. This is the only exam in the skill, and it stays optional.

## Level 7: fold it into a close-out skill (only when the user asks)

The natural next home is a session close-out skill such as /wrap: a confusing session gets
its debrief while closing out, and the talked-past bullets feed that skill's step for
capturing taste rulings. Don't wire it in until the user asks.

## Signs it's time to move up

- Most runs find zero or one moment: the finder is too strict (Level 1).
- Most runs find fifteen or more: the finder is too loose (Level 1).
- The user disagrees with a bucket or a channel more than once in a run (Level 2).
- The same picks keep getting skipped (Level 3).
- Picks start repeating, or "latest" picks are old (Level 4).
- The same agent habit shows up in three runs (Level 5).

## What never changes

Code finds, Jev sorts, Claude finds and checks the source, the user decides. No link that
wasn't found or opened. At most three things to read, watch or listen to. The agent's
mistakes are never the user's homework. Whole transcripts never leave the machine.
