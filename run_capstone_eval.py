#!/usr/bin/env python3
"""
Run the five capstone criteria, three trials each.  <- CAPSTONE, MILESTONE 5

    python run_capstone_eval.py --label before
    python run_capstone_eval.py --trials 1 --only 2      # one criterion, one trial

Don't start the service yourself — this does. Each part of each trial starts
the REAL service (`python app.py`, on its own port) with the fault switches
that criterion needs (faults.py), sends real HTTP requests, reads the answers
back out of logs/audit.jsonl, and stops the service again:

    service started with       used by
    ─────────────────────      ─────────────────────────────────────────────
    (no faults)                criterion 2, criterion 5, and the decisions
                               criterion 4 appeals against
    model_timeout              criterion 1 (timeout part) and criterion 3 —
                               the same 5 submissions, timed at the real
                               30-second timeout
    model_crash, style_crash   criterion 1
    log_down, log_flaky        criterion 4

Nothing changes between trials. The verdict for each trial is computed from
the criterion's own sentence; the report goes to
results/capstone_run_<date>_<label>.md with real responses and log lines
underneath the table.
"""

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import time
import uuid

import requests

import config
from capstone_scenarios import BAD_INPUTS, NORMAL_TEXT, OWN_WRITING, UNREADABLE_TEXTS

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

PORT = 5055
URL = f"http://127.0.0.1:{PORT}"
LOG = config.AUDIT_LOG
TIMEOUT_LIMIT_S = 32.0   # criterion 3: the real 30 s timeout + 2 s


# ── The service, started for real ────────────────────────────────────────────

class ServiceDidNotStart(RuntimeError):
    """The service never became ready — a harness problem, not a criterion result."""


class Service:
    """with Service("model_crash"): ... — a real `python app.py`, stopped after."""

    def __init__(self, *faults):
        self.faults = ",".join(faults)

    def __enter__(self):
        # PYTHONUNBUFFERED: two service starts stalled with NO output at all,
        # because output to a file is buffered — this makes a stall readable.
        # HF_HUB_OFFLINE: by default the model loader asks huggingface.co
        # whether the model changed, on every start, even when it's on disk.
        # A slow or hung network call there is the likely cause of those
        # stalls; the model is already downloaded, so load it locally only.
        env = {**os.environ, "PORT": str(PORT), "AI201_DEBUG": "0", "AI201_FAULTS": self.faults,
               "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1", "HF_HUB_OFFLINE": "1"}
        self.out = tempfile.TemporaryFile()
        self.proc = subprocess.Popen([sys.executable, "app.py"], env=env,
                                     stdout=self.out, stderr=subprocess.STDOUT)
        # 300 s, not 180: the first "after" attempt died in trial 2 when one
        # service start took longer than 180 s to load the model.
        deadline = time.time() + 300
        while time.time() < deadline:
            if self.proc.poll() is not None:
                self.out.seek(0)
                raise ServiceDidNotStart(f"Service ({self.faults or 'no faults'}) exited early:\n"
                                         f"{self.out.read().decode(errors='replace')[-3000:]}")
            try:
                health = requests.get(f"{URL}/health", timeout=2).json()
                if health.get("detector_loaded"):
                    assert sorted(health["faults_active"]) == sorted(filter(None, self.faults.split(",")))
                    return self
            except requests.RequestException:
                pass
            time.sleep(1)
        self.proc.kill()
        self.out.seek(0)
        tail = self.out.read().decode(errors="replace")[-3000:]
        self.out.close()
        raise ServiceDidNotStart(f"Service ({self.faults or 'no faults'}) didn't finish loading "
                                 f"the model within 300 s. Its output:\n{tail}")

    def __exit__(self, *exc):
        self.proc.terminate()
        self.proc.wait(timeout=30)
        self.out.close()


def cid():
    return f"cap_{uuid.uuid4().hex[:10]}"


def submit(text, creator=None):
    """
    A request that gets no answer at all within 120 s is recorded as a failed
    request (status None), not allowed to crash the run — the second "after"
    attempt died that way, and a missing answer is exactly what criterion 3
    is meant to catch.
    """
    started = time.perf_counter()
    try:
        r = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator or cid()},
                          timeout=120)
    except requests.Timeout:
        return None, {"error": "no answer within 120 s"}, round(time.perf_counter() - started, 2)
    return r.status_code, _json(r), round(time.perf_counter() - started, 2)


def appeal(content_id, creator=None, reasoning="I wrote this myself."):
    r = requests.post(f"{URL}/appeal", timeout=60,
                      json={"content_id": content_id, "reasoning": reasoning,
                            "creator_id": creator or cid()})
    return r.status_code, _json(r)


def _json(r):
    try:
        return r.json()
    except ValueError:
        return {"_raw": r.text[:200]}


def log_lines() -> int:
    if not LOG.exists():
        return 0
    with LOG.open(encoding="utf-8") as f:
        return sum(1 for _ in f)


def log_since(n: int) -> list[dict]:
    """Entries written after line n — this trial's part of the log."""
    with LOG.open(encoding="utf-8") as f:
        lines = f.read().splitlines()[n:]
    out = []
    for line in lines:
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def brief(body: dict) -> dict:
    """A response without the long label text, for the report."""
    return {k: (v if k != "label" and k != "message" else (v[:70] + "…" if isinstance(v, str) and len(v) > 70 else v))
            for k, v in body.items()}


# ── The criteria ─────────────────────────────────────────────────────────────
# Each returns (cell text for the table, passed?, evidence dict).

def crit_1_and_3():
    """Criterion 1: 15 forced failures → 15/15 unsure+degraded, none ai/human.
    Criterion 3: the 5 model_timeout ones answer within 32 s, unsure, no 500."""
    results = {}          # fault -> list of (status, body, secs)
    for fault in ("model_timeout", "model_crash", "style_crash"):
        with Service(fault):
            results[fault] = [submit(NORMAL_TEXT) for _ in range(5)]

    flat = [(f, *r) for f, rs in results.items() for r in rs]
    ok1 = [f for f, s, b, _ in flat
           if s == 200 and b.get("guess") == "unsure" and b.get("degraded") is True]
    labelled = [b.get("guess") for _, s, b, _ in flat if b.get("guess") in ("ai", "human")]
    c1_pass = len(ok1) == 15 and not labelled
    c1_cell = f"{len(ok1)}/15 unsure+degraded, {len(labelled)} ai/human"

    timeouts = results["model_timeout"]
    ok3 = [r for r in timeouts if r[2] <= TIMEOUT_LIMIT_S and r[0] == 200 and r[1].get("guess") == "unsure"]
    c3_pass = len(ok3) == 5
    secs = [r[2] for r in timeouts]
    c3_cell = f"{len(ok3)}/5 in time (max {max(secs):.1f}s)"

    ev1 = {f: [{"status": s, "seconds": t, "response": brief(b)} for s, b, t in rs[:1]]
           for f, rs in results.items()}
    ev1["all 15 (fault, status, guess, degraded, failed_signals)"] = [
        (f, s, b.get("guess"), b.get("degraded"), b.get("failed_signals")) for f, s, b, _ in flat]
    ev3 = {"seconds": secs, "statuses": [r[0] for r in timeouts],
           "guesses": [r[1].get("guess") for r in timeouts],
           "failed_signals": [r[1].get("failed_signals") for r in timeouts]}
    return (c1_cell, c1_pass, ev1), (c3_cell, c3_pass, ev3)


def crit_2():
    """10 unreadable texts → 0 labelled high-confidence AI."""
    with Service():
        rows = []
        for name, text in UNREADABLE_TEXTS.items():
            s, b, _ = submit(text)
            rows.append((name, s, b))
    ai = [n for n, s, b in rows if b.get("guess") == "ai"]
    # Milestone 6: also count how many the readability check itself caught
    # (style refused → degraded). Not part of the criterion's pass/fail; it is
    # the tighter measure the improvement is aimed at.
    caught = [n for n, s, b in rows if "style" in (b.get("failed_signals") or [])]
    cell = f"{len(ai)}/10 AI" + (f" ({', '.join(ai)})" if ai else "") + f" · {len(caught)}/10 caught by check"
    ev = [{"text": n, "status": s, "guess": b.get("guess"), "degraded": b.get("degraded"),
           "failed_signals": b.get("failed_signals"), "model_score": b.get("model_score"),
           "style_score": b.get("style_score"), "confidence": b.get("confidence"),
           "error": b.get("error")} for n, s, b in rows]
    return cell, not ai, ev


def crit_4():
    """log_down: 0/5 'recorded', 5/5 get 503. log_flaky: 5/5 recorded exactly once."""
    with Service():
        down_ids = [submit(NORMAL_TEXT)[1]["content_id"] for _ in range(5)]
        flaky_ids = [submit(NORMAL_TEXT)[1]["content_id"] for _ in range(5)]

    start = log_lines()
    with Service("log_down"):
        down = [appeal(c) for c in down_ids]
    with Service("log_flaky"):
        flaky = [appeal(c) for c in flaky_ids]
    new = log_since(start)

    def records(c):
        return [e for e in new if e.get("content_id") == c and e.get("event") == "appeal"]

    recorded_msgs = [b for s, b in down if "has been recorded" in b.get("message", "")
                     or b.get("status") == "under_review"]
    got_503 = [s for s, _ in down if s == 503]
    down_records = sum(len(records(c)) for c in down_ids)
    flaky_once = [c for (s, b), c in zip(flaky, flaky_ids)
                  if s == 200 and len(records(c)) == 1]

    passed = not recorded_msgs and len(got_503) == 5 and down_records == 0 and len(flaky_once) == 5
    cell = (f"down: {len(recorded_msgs)}/5 'recorded', {len(got_503)}/5 503 · "
            f"flaky: {len(flaky_once)}/5 once")
    ev = {"log_down responses": [{"status": s, **brief(b)} for s, b in down[:2]],
          "log_down appeal records written": down_records,
          "log_flaky responses (status)": [s for s, _ in flaky],
          "log_flaky appeal records": [records(c) for c in flaky_ids[:1]],
          "log_flaky records per appeal": [len(records(c)) for c in flaky_ids]}
    return cell, passed, ev


def crit_5():
    """20 mixed requests → 20/20 in the log with timestamp, route, duration_ms."""
    start = log_lines()
    sent = []      # (kind, how to find its entry)
    with Service():
        ids = []
        for text in OWN_WRITING[:10]:
            c = cid()
            s, b, _ = submit(text, c)
            ids.append(b.get("content_id"))
            sent.append(("submission", s, lambda e, c=c: e.get("creator_id") == c and e.get("route") == "/submit"))
        for name, how in BAD_INPUTS:
            c = cid()
            if "json" in how:
                body = json.loads(json.dumps(how["json"]).replace("{cid}", c))
                r = requests.post(f"{URL}/submit", json=body, timeout=60)
                match = (lambda e, c=c: e.get("creator_id") == c)
            else:
                r = requests.post(f"{URL}/submit", data=how["raw"].replace("{cid}", c),
                                  headers={"Content-Type": "application/json"}, timeout=60)
                match = (lambda e: e.get("creator_id") == "unknown" and e.get("reason") == "missing_text"
                         and e.get("route") == "/submit")
            sent.append((f"bad input: {name}", r.status_code, match))
        for content_id in ids[:3]:
            c = cid()
            s, _ = appeal(content_id, c)
            sent.append(("appeal", s, lambda e, x=content_id: e.get("content_id") == x and e.get("event") == "appeal"))
        for content_id in ids[:2]:
            c = cid()
            s, _ = appeal(content_id, c, "Sending it again.")
            sent.append(("repeat appeal", s, lambda e, c=c, x=content_id:
                         e.get("creator_id") == c and e.get("reason") == "duplicate_appeal"
                         and e.get("attempted_content_id") == x))
    new = log_since(start)

    rows = []
    for kind, status, match in sent:
        found = [e for e in new if match(e)]
        complete = len(found) == 1 and all(found[0].get(k) not in (None, "")
                                           for k in ("timestamp", "route", "duration_ms"))
        rows.append((kind, status, len(found), complete, found[0] if found else None))
    n = sum(r[3] for r in rows)
    ev = {"requests": [{"request": k, "status": s, "entries found": f, "complete": ok}
                       for k, s, f, ok, _ in rows],
          "log entries (one of each kind)": [e for _, e in {r[0].split(':')[0]: r[4] for r in rows}.items()]}
    return f"{n}/20 logged", n == 20, ev


CRITERIA = [
    (1, "Broken signal never accuses", "15/15 unsure+degraded, 0 ai/human", "`app.py::submit` (`_run_model_signal`, `_run_style_signal`)"),
    (2, "Unreadable text never labelled AI", "0 of 10 labelled AI", "`app.py::submit`, `stylometry.py::check_measurable`"),
    (3, "Hung model still answers in time", "5/5 within 32 s, unsure, no 500", "`app.py::_run_model_signal`"),
    (4, "Appeal never falsely confirmed", "down: 0/5 'recorded' + 5/5 503; flaky: 5/5 once", "`app.py::appeal`, `audit.py::_append`"),
    (5, "Every run leaves a trace", "20/20 logged with timestamp, route, duration_ms", "`audit.py::_append`, `app.py::_run_fields`"),
]


# ── Running and reporting ────────────────────────────────────────────────────

def NOT_RUN(exc):
    """A trial whose service never started: recorded, not counted as pass or fail."""
    return "not run (service didn't start)", None, {"harness error": str(exc)}


def status(result):
    return {True: "pass", False: "FAIL", None: "NOT RUN"}[result[1]]

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--only", type=int, help="run one criterion (1-5); 1 and 3 run together")
    args = parser.parse_args()

    try:
        requests.get(f"{URL}/health", timeout=1)
        sys.exit(f"Something is already running on port {PORT}. Stop it first.")
    except requests.RequestException:
        pass

    want = {args.only} if args.only else {1, 2, 3, 4, 5}
    if want & {1, 3}:
        want |= {1, 3}
    trials = {n: [] for n in want}

    for t in range(1, args.trials + 1):
        print(f"── Trial {t} ──", flush=True)
        if 1 in want:
            try:
                r1, r3 = crit_1_and_3()
            except ServiceDidNotStart as exc:
                r1 = r3 = NOT_RUN(exc)
            trials[1].append(r1)
            trials[3].append(r3)
            print(f"  1: {r1[0]}  {status(r1)}\n  3: {r3[0]}  {status(r3)}", flush=True)
        for n, fn in ((2, crit_2), (4, crit_4), (5, crit_5)):
            if n in want:
                try:
                    r = fn()
                except ServiceDidNotStart as exc:
                    r = NOT_RUN(exc)
                trials[n].append(r)
                print(f"  {n}: {r[0]}  {status(r)}", flush=True)

    path = write_report(trials, args)
    print(f"\nReport: {path}")


def write_report(trials, args):
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    suffix = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"capstone_run_{stamp}{suffix}.md"
    lines = [
        f"# Capstone run log{' — ' + args.label if args.label else ''}",
        "",
        "- Produced by: `run_capstone_eval.py::main` — each part starts the real service "
        "(`python app.py`) with the fault switches it needs, sends HTTP requests, and reads `logs/audit.jsonl`",
        f"- {args.trials} trial(s) per criterion · {dt.datetime.now():%Y-%m-%d %H:%M} · nothing changed between trials",
        "- Inputs: `capstone_scenarios.py`. Criteria: `criteria.md`, Capstone section",
        "",
        "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " | Verdict |",
        "|---|---|" + "---|" * args.trials + "---|",
    ]
    for n, name, target, _ in CRITERIA:
        if n not in trials:
            continue
        cells = [c for c, _, _ in trials[n]]
        if any(p is None for _, p, _ in trials[n]):
            verdict = "INCOMPLETE"          # a trial never ran — no verdict either way
        else:
            verdict = "MET" if all(p for _, p, _ in trials[n]) else "MISSED"
        lines.append(f"| {n}. {name} | {target} | " + " | ".join(cells) + f" | **{verdict}** |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real responses and log entries from **trial 1** (and from any trial that failed).", ""]
    for n, name, _, where in CRITERIA:
        if n not in trials:
            continue
        lines += [f"### {n}. {name}", "", f"Produced by {where}.", ""]
        for i, (cell, passed, ev) in enumerate(trials[n], 1):
            if i == 1 or not passed:
                lines += [f"**Trial {i}: {cell} — {'pass' if passed else 'FAIL'}**", "",
                          "```json", json.dumps(ev, indent=2, ensure_ascii=False), "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    main()
