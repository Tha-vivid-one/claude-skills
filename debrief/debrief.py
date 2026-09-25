#!/usr/bin/env python3
"""debrief: find the moments in a Claude Code session where the user got lost or asked
why, sort each one with Jev, and route each real learning gap to the right kind of
material for that exact question.

Code finds the moments, Jev sorts them and picks the channel, Claude finds and checks the
source, the user decides.

    debrief.py find                  # the current session (CLAUDE_CODE_SESSION_ID)
    debrief.py find <id|prefix|path> # a past session
    debrief.py find ... --wide       # every question the user asked is a candidate
    debrief.py find ... --test       # a test run: saved apart, not counted as a real run
    debrief.py find ... --no-jev     # phrase matching only; Claude sorts by hand
    debrief.py runs                  # how many runs so far, and the mix of buckets and channels

Stdlib only. Needs TYPESAFE_API_KEY for the Jev step, and reads it from the shell profile
when the app didn't load it. The key is never printed. An optional config.json next to
this file sets {"log": "path to the learning log", "person": "one line on who the user is"}.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

SKILL = Path(__file__).resolve().parent
RUNS = SKILL / "runs"
PROJECTS = Path.home() / ".claude" / "projects"


def load_config():
    p = SKILL / "config.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except ValueError:
        return {}


CONFIG = load_config()
LIBRARY = SKILL / "library.md" if (SKILL / "library.md").exists() else SKILL / "library.example.md"
LOG = Path(os.environ.get("DEBRIEF_LOG") or CONFIG.get("log")
           or Path.home() / ".claude" / "debrief" / "learning-log.md").expanduser()
PERSON = CONFIG.get("person") or "someone who builds software by directing AI coding agents, not necessarily a trained engineer"

API_URL = os.environ.get("TYPESAFE_ENDPOINT", "https://api.typesafe.ai").rstrip("/") + "/v1/systemone"
MODEL = os.environ.get("DEBRIEF_MODEL", "jev-latest")

# Where the lines sit between buckets. Starting guesses; PROGRESSION.md says how to move them.
T_CONFUSED = 0.5
T_CURIOUS = 0.5
T_JARGON = 0.5
T_LEARN = 0.6
T_AMBIGUOUS = 0.5
MAX_MOMENTS = 24
PER_REQUEST = 6
WORKERS = 4


# ---------------------------------------------------------------- finding the session

def find_session(arg):
    if not arg:
        arg = os.environ.get("CLAUDE_CODE_SESSION_ID")
        if not arg:
            sys.exit("No session given and CLAUDE_CODE_SESSION_ID is not set. Pass a session id or .jsonl path.")
    p = Path(arg).expanduser()
    if p.suffix == ".jsonl" and p.exists():
        return p
    hits = sorted(PROJECTS.glob(f"*/{arg}*.jsonl"))
    if not hits:
        sys.exit(f"No transcript found for '{arg}' under {PROJECTS}.")
    if len(hits) > 1 and not any(h.stem == arg for h in hits):
        sys.exit("That prefix matches several sessions:\n" + "\n".join(str(h) for h in hits[:10]))
    exact = [h for h in hits if h.stem == arg]
    return exact[0] if exact else hits[0]


# ---------------------------------------------------------------- reading the transcript

NOISE_PREFIXES = (
    "<local-command-stdout>", "<local-command-stderr>", "<command-name>", "<command-message>",
    "Caveat:", "[Request interrupted", "<task-notification>", "<bash-stdout>", "<bash-stderr>",
    "This session is being continued", "<user-prompt-submit-hook>",
)


def clean_user(text):
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    text = re.sub(r"<ide_[a-z_]+>.*?</ide_[a-z_]+>", "", text, flags=re.S)
    text = re.sub(r"</?pasted_content[^>]*>", "", text)
    return text.strip()


def turns_of(path):
    """Every typed user message, with the agent's words since the previous one."""
    turns, agent_buf, last_user = [], [], ""
    with open(path, errors="ignore") as fh:
        for line in fh:
            try:
                j = json.loads(line)
            except ValueError:
                continue
            if j.get("isSidechain") or j.get("isMeta"):
                continue
            msg = j.get("message") or {}
            content = msg.get("content")
            if j.get("type") == "assistant":
                if isinstance(content, list):
                    agent_buf += [c.get("text", "") for c in content
                                  if isinstance(c, dict) and c.get("type") == "text"]
                continue
            if j.get("type") != "user" or "toolUseResult" in j:
                continue
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "\n".join(c.get("text", "") for c in content
                                 if isinstance(c, dict) and c.get("type") == "text")
            else:
                continue
            text = clean_user(text)
            if not text or text.startswith(NOISE_PREFIXES):
                continue
            turns.append({
                "n": len(turns),
                "ts": j.get("timestamp", ""),
                "user": text,
                "agent_before": "\n".join(t for t in agent_buf if t.strip()).strip(),
                "earlier_request": last_user,
            })
            agent_buf, last_user = [], text
    return turns


# ---------------------------------------------------------------- phrases that mark a moment

TRIGGERS = [
    # lost
    ("means?", r"\bwhat (?:does|do|did|would) .{0,60}?\bmean\b"),
    ("what is a", r"\bwhat(?:'s| is|s) (?:a|an) [a-z0-9]"),
    ("wtf is", r"\bwhat the (?:fuck|hell|heck) (?:is|are|does|do|was|were)\b"),
    ("don't understand", r"\bi (?:do ?n[o']?t|dont|didn'?t|didnt|can'?t|cant) (?:understand|get it|follow|know what)\b"),
    ("idk what", r"\bidk (?:what|why|how|where|if)\b"),
    ("confused", r"\bconfus(?:ed|ing|ion)\b"),
    ("what do you mean", r"\bwhat ?do (?:you|u) mean\b|\bwdym\b|\bwhat are you (?:talking about|saying)\b"),
    ("too technical", r"\btoo (?:technical|long)\b|\btechnical as fuck\b|\blong winded\b|\bnovel of\b"),
    ("lost", r"\brabbit hole\b|\bconvoluted\b|\bgoing in circles\b|\blost me\b"),
    ("so wait", r"\bso wait\b|\bwait,? what\b|\bwait so\b"),
    # curious
    ("explain", r"\bexplain (?:this|that|it|what|how|why)\b|\bexplain (?:it |this |that )?to me\b|\bcan you explain\b|\bhelp me understand\b|\bwalk me through\b|\bplain english\b|\bplain terms\b|\blay ?m[ae]n'?s terms\b|\beli5\b"),
    ("why?", r"\bwhy\b[^\n.!]{0,120}\?"),
    ("have to be", r"\b(?:does|do|did|would|should|has|have) (?:it|this|that|they|we|you) (?:have|need|got) to be\b"),
    ("what if", r"\bwhat if\b|\bif we (?:did|do|were|made|used|went|changed|switched|added|took|had|just)\b[^\n.!]{0,120}\?"),
    ("how come", r"\bhow come\b|\bwhat'?s the point\b|\bwhat (?:does|do) (?:it|this|that) (?:even )?do\b"),
    ("how does it work", r"\bhow (?:does|do|would) (?:this|that|it|these|those) (?:work|happen)\b"),
    ("difference", r"\bdifference between\b|\bwhat'?s the difference\b"),
    ("where from", r"\bwhere did (?:we|you|that|this|it) (?:get|derive|come)\b|\bhow did (?:we|you) (?:get|derive|come up with)\b|\bhow do (?:we|you) know\b"),
    ("why rule", r"\bwhy (?:does|do|would|should) (?:it|this|that|we|they) (?:have|need)\b"),
    # mismatch
    ("i thought", r"\bi thought (?:we|you|it|this|that|there|the)\b"),
    ("correction", r"\bi never said\b|\bthat'?s not what i\b|\bthats not what i\b|\bnot what i (?:asked|meant|said)\b|\bi (?:already )?(?:said|told you)\b|\byou misunderstood\b"),
    ("why did you", r"\bwhy (?:did|would) you\b"),
]
TRIGGERS = [(name, re.compile(rx)) for name, rx in TRIGGERS]
CORRECTIONS = {"correction", "why did you", "i thought"}


def norm(q):
    return re.sub(r"[^a-z0-9 ]", "", q.lower())[:120].strip()


def detect(turns, max_moments, wide=False):
    seen, moments = {}, []
    for t in turns:
        low = t["user"][:1500].lower()
        hits = [name for name, rx in TRIGGERS if rx.search(low)]
        if wide and not hits and "?" in low:
            hits = ["question"]
        key = norm(t["user"])
        if "?" in t["user"] and len(key) > 12:
            if key in seen and seen[key] != t["n"]:
                hits.append("asked again")
            seen.setdefault(key, t["n"])
        if hits and t["agent_before"]:
            moments.append(dict(t, triggers=hits))
    if len(moments) > max_moments:
        keep = sorted(moments, key=lambda m: -len(m["triggers"]))[:max_moments]
        moments = sorted(keep, key=lambda m: m["n"])
    return moments


# ---------------------------------------------------------------- scrubbing before anything leaves

SECRETS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]+?-----END [A-Z ]*PRIVATE KEY-----", "[redacted key]"),
    (r"https://(?:discord(?:app)?\.com)/api/webhooks/\S+", "[redacted webhook]"),
    (r"sk-ant-[A-Za-z0-9_\-]{10,}", "[redacted]"),
    (r"\bsk-[A-Za-z0-9_\-]{20,}", "[redacted]"),
    (r"\bAIza[0-9A-Za-z_\-]{20,}", "[redacted]"),
    (r"\bAQ\.[0-9A-Za-z_\-\.]{20,}", "[redacted]"),
    (r"\b(?:ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}", "[redacted]"),
    (r"\bxox[abprs]-[A-Za-z0-9\-]{10,}", "[redacted]"),
    (r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", "[redacted]"),
    (r"\bAKIA[0-9A-Z]{16}\b", "[redacted]"),
    (r"(?i)\b(bearer|token|api[_-]?key|secret|password|passwd)(\s*[:=]\s*|\s+)[\"']?[^\s\"']{8,}", r"\1 [redacted]"),
    (r"\b[A-Za-z0-9_\-]{40,}\b", "[redacted]"),
    (r"[\w.+-]+@[\w-]+\.[\w.-]+", "[email]"),
]
SECRETS = [(re.compile(rx), sub) for rx, sub in SECRETS]


def scrub(text):
    for rx, sub in SECRETS:
        text = rx.sub(sub, text)
    return text


def trim(text, head, tail=0):
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(text) <= head + tail + 20:
        return text
    return text[:head].rstrip() + (" … " + text[-tail:].lstrip() if tail else " …")


# ---------------------------------------------------------------- the library (deep study only)

def load_library():
    subjects, cur = {}, None
    if not LIBRARY.exists():
        return subjects
    for line in LIBRARY.read_text().splitlines():
        m = re.match(r"^## (\w+): (.+)$", line)
        if m:
            cur = m.group(1)
            subjects[cur] = {"title": m.group(2).strip(), "covers": "", "items": []}
        elif cur and line.startswith("Covers:"):
            subjects[cur]["covers"] = line[len("Covers:"):].strip()
        elif cur and line.startswith("- "):
            subjects[cur]["items"].append(line[2:].strip())
    return subjects


# ---------------------------------------------------------------- the learning log

def read_log():
    topics, terms, picks = {}, [], []
    if not LOG.exists():
        return topics, terms, picks
    for line in LOG.read_text(errors="ignore").splitlines():
        t = re.search(r"topic: (\w+)", line)
        if t:
            topics[t.group(1)] = topics.get(t.group(1), 0) + 1
        w = re.search(r"term: ([^·]+)", line)
        if w:
            terms.append(w.group(1).strip())
        p = re.search(r"pick: ([^·]+)", line)
        if p and "inline" not in p.group(1):
            picks.append(p.group(1).strip())
    return topics, terms[-80:], picks[-80:]


# ---------------------------------------------------------------- Jev

class JevError(Exception):
    pass


def api_key():
    key = os.environ.get("TYPESAFE_API_KEY", "")
    if key:
        return key
    for rc in (".zshrc", ".zshenv", ".zprofile", ".bash_profile", ".bashrc"):
        p = Path.home() / rc
        if p.exists():
            m = re.search(r"^\s*export\s+TYPESAFE_API_KEY=[\"']?([^\"'\s]+)", p.read_text(errors="ignore"), re.M)
            if m:
                return m.group(1)
    return ""


def system_one(state, questions, key):
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    for attempt in range(5):
        req = urllib.request.Request(API_URL, data=body, method="POST", headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="ignore")[:300]
            if e.code in (429, 500, 502, 503, 529) and attempt < 4:
                time.sleep(min(float(e.headers.get("retry-after") or 0) or 0.5 * 2 ** attempt, 10))
                continue
            raise JevError(f"TypeSafe API {e.code}: {detail}")
        except urllib.error.URLError as e:
            if attempt < 4:
                time.sleep(0.5 * 2 ** attempt)
                continue
            raise JevError(f"TypeSafe API unreachable: {e.reason}")
    raise JevError("TypeSafe API: out of retries")


CHANNELS = {
    "quick_answer": "One sentence settles it: a fact, a quick definition, a status, a detail of this project, or where something is. Nothing to read.",
    "tool_docs": "It is about how one named tool, service, app, API, library or file format works, such as Stripe, Heroku, Cloudflare, git, Figma or a Python package. That tool's own documentation is the best source.",
    "explainer": "It is a general idea or term that holds across tools and companies, such as a webhook, churn, lifetime value, calibration or positioning. One short article or video about that exact idea would make it clear.",
    "latest": "It is about something that changes month to month, such as AI models and agents, security threats, crypto tokens and markets, app store or platform rules, or current benchmarks and prices. The newest research, paper, report or write-up matters more than a textbook.",
    "deep_study": "It points at a broad skill that takes real study to get good at, such as statistics, accounting, writing, pricing strategy or trading discipline. A book or course fits better than one article.",
    "ask_someone": "Only a specific person can answer it: a teammate's decision, a vendor's terms, the settings of an account, or something that was never written down.",
}


def questions_for(k, m, subjects):
    q = {
        f"confused::{k}": {
            "type": "noul",
            "instructions": f"In `moments[{k}].user_replied`, the user shows that they did not understand something the agent said or did.",
            "criteria": {
                "true": "The user asks what something means, says they are confused or lost, asks how something works or where a number came from, or says the agent misread them.",
                "false": "The user gives an instruction, reports a bug or a result, approves, or vents without showing confusion about anything the agent said or did.",
            },
        },
        f"curious::{k}": {
            "type": "noul",
            "instructions": f"In `moments[{k}].user_replied`, the user asks why something is the way it is, how it works, or what would happen if it were done differently.",
            "criteria": {
                "true": "The user asks for a reason, a mechanism, or the result of a hypothetical, such as 'why?', 'does it have to be like that?', 'what if we did this?' or 'explain this to me'.",
                "false": "The user gives an instruction, reports a result, or asks only about status, next steps or where something is.",
            },
        },
        f"jargon::{k}": {
            "type": "noul",
            "instructions": f"`moments[{k}].agent_said` uses a term, acronym, internal name or step without explaining it, that {PERSON} would need explained.",
            "criteria": {
                "true": "Contains at least one unexplained acronym, internal label, code identifier or technical term, such as ADR, SHA, env var or a function name, that this person would need explained.",
                "false": "Written in plain words, or every technical term is explained where it first appears.",
            },
        },
        f"learnable::{k}": {
            "type": "noul",
            "instructions": f"The thing the user asked about or did not understand in `moments[{k}].user_replied` is a general concept from software, business, design, writing or markets that is worth learning.",
            "criteria": {
                "true": "A concept with a name people use across many companies, such as lifetime value, a git branch, a webhook, calibration, positioning, a stop loss or an API.",
                "false": "Something only this project uses, such as a file name, an internal label, a one-off setting, a person's plan, or where a button is.",
            },
        },
        f"channel::{k}": {
            "type": "choice",
            "instructions": f"Which kind of source would best help the user understand the thing they asked about or did not understand in `moments[{k}].user_replied`?",
            "criteria": CHANNELS,
        },
        f"topic::{k}": {
            "type": "choice",
            "instructions": f"Which subject does the thing the user asked about or did not understand in `moments[{k}].user_replied` belong to?",
            "criteria": dict({key: s["covers"] or s["title"] for key, s in subjects.items()},
                             other="Something else: a tool quirk, a project detail, or a subject not listed here."),
        },
    }
    if CORRECTIONS & set(m["triggers"]):
        q[f"ambiguous::{k}"] = {
            "type": "noul",
            "instructions": f"`moments[{k}].earlier_request` can fairly be read the way the agent acted on it in `moments[{k}].agent_said`, even though `moments[{k}].user_replied` shows the user meant something else.",
            "criteria": {
                "true": "The request left out a detail or used words with two readings, so the agent's reading was fair.",
                "false": "The request was clear, and the agent misread it, ignored part of it, or did something unrelated.",
            },
        }
    return q


def top2(answer):
    probs = sorted((answer.get("probabilities") or {}).items(), key=lambda kv: -kv[1])
    first = answer.get("choice")
    p = round((answer.get("probabilities") or {}).get(first, 0), 2)
    runner = probs[1][0] if len(probs) > 1 and p < 0.7 and probs[1][1] >= 0.15 else None
    return first, p, runner


def sort_with_jev(moments, subjects, key):
    state_items = [{
        "agent_said": scrub(trim(m["agent_before"], 500, 1300)),
        "user_replied": scrub(trim(m["user"], 900, 200)),
        "earlier_request": scrub(trim(m["earlier_request"], 400, 100)),
    } for m in moments]
    chunks = [list(range(i, min(i + PER_REQUEST, len(moments)))) for i in range(0, len(moments), PER_REQUEST)]
    usage = {"calls": 0, "input_tokens": 0, "model": None}

    def call(idx):
        state = {"moments": [state_items[i] for i in idx]}
        qs = {}
        for local, i in enumerate(idx):
            qs.update(questions_for(local, moments[i], subjects))
        return idx, system_one(state, qs, key)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        results = list(pool.map(call, chunks))
    for idx, r in results:
        usage["calls"] += 1
        usage["input_tokens"] += (r.get("usage") or {}).get("input_tokens") or 0
        usage["model"] = r.get("model")
        ans = r.get("answers") or {}
        for local, i in enumerate(idx):
            m = moments[i]
            m["jev"] = {k: round(ans[f"{k}::{local}"]["noul"], 2)
                        for k in ("confused", "curious", "jargon", "learnable", "ambiguous") if f"{k}::{local}" in ans}
            m["topic"], m["topic_p"], m["alt_topic"] = top2(ans.get(f"topic::{local}") or {})
            m["channel"], m["channel_p"], m["alt_channel"] = top2(ans.get(f"channel::{local}") or {})
    return usage


def bucket(m):
    """Primary bucket plus flags. A moment can be both a learning gap and the agent's fault.
    Curiosity ("why?", "what if we...") can lead to learning but never blames the agent."""
    j = m.get("jev")
    if not j:
        return "unsorted", []
    lost = j.get("confused", 0) >= T_CONFUSED
    curious = j.get("curious", 0) >= T_CURIOUS
    jargon = j.get("jargon", 0) >= T_JARGON
    learn = j.get("learnable", 0) >= T_LEARN
    if CORRECTIONS & set(m["triggers"]):
        # A mismatch: the agent misread them, or the ask had two readings. Not homework.
        if j.get("ambiguous", 0) >= T_AMBIGUOUS:
            return "how_to_ask", []
        if lost or jargon:
            return "agent_talked_past", []
    if not (lost or curious):
        return "noise", []
    if learn:
        return "worth_learning", (["agent_talked_past"] if lost and jargon else [])
    # Jev's numbers move by up to ~0.15 between identical runs, so flag the near misses.
    near = ["near_learning"] if j.get("learnable", 0) >= T_LEARN - 0.1 else []
    if lost and jargon:
        return "agent_talked_past", near
    return "one_off", near


# ---------------------------------------------------------------- commands

def cmd_find(args):
    path = find_session(args.session)
    t0 = time.time()
    turns = turns_of(path)
    moments = detect(turns, args.max, args.wide)
    subjects = load_library()
    notes, usage = [], None

    key = "" if args.no_jev else api_key()
    if moments and key:
        try:
            usage = sort_with_jev(moments, subjects, key)
        except JevError as e:
            notes.append(f"Jev failed ({e}); every moment is unsorted, so sort them yourself.")
    elif moments and not args.no_jev:
        notes.append("TYPESAFE_API_KEY not found, so nothing was sorted. Sort the moments yourself.")
    for m in moments:
        m["bucket"], m["also"] = bucket(m)

    topics_past, terms_past, picks_past = read_log()
    # The library is only for deep study and for gaps that keep coming back.
    wanted = set()
    for m in moments:
        if m["bucket"] == "unsorted":
            wanted = set(subjects)
            break
        if m["bucket"] == "worth_learning" and (m.get("channel") == "deep_study" or topics_past.get(m.get("topic"), 0) >= 2):
            wanted |= {t for t in (m.get("topic"), m.get("alt_topic")) if t}
    menu = {k: {"title": s["title"], "items": s["items"]} for k, s in subjects.items() if k in wanted}

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + path.stem[:8]
    record = {
        "run_id": run_id, "session": str(path), "session_id": path.stem, "when": datetime.now().isoformat(timespec="seconds"),
        "turns": len(turns), "found": len(moments), "usage": usage, "notes": notes, "wide": args.wide,
        "thresholds": {"confused": T_CONFUSED, "curious": T_CURIOUS, "jargon": T_JARGON, "learnable": T_LEARN, "ambiguous": T_AMBIGUOUS},
        "moments": moments, "seconds": round(time.time() - t0, 1),
    }
    where = RUNS / "regression" if args.test else RUNS
    where.mkdir(parents=True, exist_ok=True)
    (where / f"{run_id}.json").write_text(json.dumps(record, indent=1))

    counts, channels = {}, {}
    for m in moments:
        counts[m["bucket"]] = counts.get(m["bucket"], 0) + 1
        if m["bucket"] == "worth_learning" and m.get("channel"):
            channels[m["channel"]] = channels.get(m["channel"], 0) + 1
    out = {
        "run_id": run_id,
        "session": path.stem[:8],
        "project": re.sub(r"^-Users-[^-]+-(?:Documents-)?", "", path.parent.name),
        "typed_messages": len(turns),
        "moments_found": len(moments),
        "buckets": counts,
        "channels": channels,
        "jev": usage,
        "notes": notes,
        "moments": [{
            "n": m["n"], "when": m["ts"][:16], "triggers": m["triggers"], "bucket": m["bucket"], "also": m.get("also", []),
            "jev": m.get("jev"), "channel": m.get("channel"), "channel_p": m.get("channel_p"), "alt_channel": m.get("alt_channel"),
            "topic": m.get("topic"), "topic_p": m.get("topic_p"), "alt_topic": m.get("alt_topic"),
            "they_said": trim(m["user"], 400),
            "agent_before_end": trim(m["agent_before"][-600:], 600),
        } for m in moments if m["bucket"] != "noise" or args.all],
        "noise_hidden": 0 if args.all else counts.get("noise", 0),
        "library_menu": menu,
        "log": {"path": str(LOG), "exists": LOG.exists(), "past_topics": topics_past,
                "past_terms": terms_past, "past_picks": picks_past},
        "runs_so_far": len(list(RUNS.glob("*.json"))),
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))


def cmd_runs(args):
    files = sorted(RUNS.glob("*.json"))
    buckets, channels = {}, {}
    for f in files:
        r = json.loads(f.read_text())
        for m in r.get("moments", []):
            buckets[m.get("bucket", "?")] = buckets.get(m.get("bucket", "?"), 0) + 1
            if m.get("bucket") == "worth_learning" and m.get("channel"):
                channels[m["channel"]] = channels.get(m["channel"], 0) + 1
    print(json.dumps({"runs": len(files), "buckets_all_runs": buckets, "channels_all_runs": channels,
                      "latest": [f.stem for f in files[-5:]]}, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("find")
    f.add_argument("session", nargs="?")
    f.add_argument("--no-jev", action="store_true")
    f.add_argument("--all", action="store_true", help="also print moments Jev called noise")
    f.add_argument("--wide", action="store_true", help="every question the user asked is a candidate, not just the trigger phrases")
    f.add_argument("--max", type=int, default=MAX_MOMENTS)
    f.add_argument("--test", action="store_true", help="a test on a past session: saved under runs/regression, not counted")
    f.set_defaults(fn=cmd_find)
    r = sub.add_parser("runs")
    r.set_defaults(fn=cmd_runs)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
