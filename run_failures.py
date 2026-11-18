#!/usr/bin/env python3
"""
The path B failure drill.  <- CAPSTONE, MILESTONE 2

    python run_failures.py                 # all scenarios, 5 trials each
    python run_failures.py --trials 3
    python run_failures.py --only appeal_log_down

Each scenario switches a fault on (see faults.py), sends real requests through
the real routes, and checks what came back AND what landed in the audit log.
Unlike run_eval.py, the verdict is computed: every trial either meets the
bad-path rule or it doesn't, and a scenario passes only if all trials do.

It runs the app in-process (Flask's test client) so faults can be flipped
between scenarios without restarting anything. The drill writes to its own
log, logs/failure_drill.jsonl, so your real audit log is untouched, and its
report goes to results/failure_drill_<timestamp>.md.
"""

import argparse
import datetime as dt
import json
import sys
import threading
import time
import uuid

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

# Before the app is imported: a drill log of its own, and a shorter timeout so
# the timeout scenario doesn't take minutes. A warm model call is 1–2 s.
config.AUDIT_LOG = config.LOG_DIR / "failure_drill.jsonl"
config.MODEL_SIGNAL_TIMEOUT_S = 5.0

import app as service  # noqa: E402
import audit  # noqa: E402
import detector  # noqa: E402
import faults  # noqa: E402

client = service.app.test_client()

# An ordinary paragraph both signals can read. Its own score doesn't matter
# here — only what happens when something around it breaks.
NORMAL_TEXT = (
    "The implementation of the proposed framework requires careful consideration "
    "of several key factors. First, it is important to note that the system must "
    "be able to handle a wide variety of different inputs. Additionally, the "
    "overall performance of the solution depends on a number of important variables."
)

# Text the style signal can't read. Before path B, the first two were
# labelled high-confidence AI (style 0.83, combined ~0.90).
UNREADABLE = {
    "korean": "나는 어제 친구와 함께 공원에 갔다. 날씨가 정말 좋아서 우리는 오랫동안 걸었다. "
              "그리고 근처 카페에서 커피를 마시면서 이야기를 나눴다.",
    "emoji": "🔥🔥🔥 😂😂 🙌🙌🙌🙌 ❤️❤️ 🎉🎉🎉 👍👍",
    "russian": "Вчера я ходил в парк с другом. Погода была отличная, и мы долго гуляли. "
               "Потом мы пили кофе в маленьком кафе.",
    "few_words": "Honestly I just liked the movie a lot.",
    "mixed": "오늘은 정말 바쁜 하루였다. 회의가 세 번이나 있었고 점심도 못 먹었다. OK fine.",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def creator():
    # The rate limit keys on creator_id; a fresh one per request keeps the
    # drill from tripping it (that's a different scenario).
    return f"drill_{uuid.uuid4().hex[:8]}"


def submit(text=NORMAL_TEXT):
    started = time.perf_counter()
    r = client.post("/submit", json={"text": text, "creator_id": creator()})
    return r.status_code, r.get_json(), round(time.perf_counter() - started, 2)


def appeal(content_id, reasoning="I wrote this myself, over two evenings."):
    r = client.post("/appeal", json={"content_id": content_id, "reasoning": reasoning})
    return r.status_code, r.get_json()


def entries(content_id):
    return audit.entries_for(content_id)


def appeals_for(content_id):
    return [e for e in entries(content_id) if e.get("event") == "appeal"]


class Faults:
    """with Faults("log_down"): ... — on for the block, off after, always."""

    def __init__(self, *names):
        self.names = set(names)

    def __enter__(self):
        faults.ACTIVE |= self.names

    def __exit__(self, *exc):
        faults.ACTIVE -= self.names


def check(conditions):
    """[(description, bool)] -> (passed, [failed descriptions])"""
    failed = [desc for desc, ok in conditions if not ok]
    return not failed, failed


# ── Scenarios ────────────────────────────────────────────────────────────────
# Each returns (passed, failed_conditions, evidence) for ONE trial.

def s_model_timeout(trial):
    with Faults("model_timeout"):
        status, body, secs = submit()
    cid = (body or {}).get("content_id")
    log = entries(cid) if cid else []
    limit = config.MODEL_SIGNAL_TIMEOUT_S + 3
    return (*check([
        ("200", status == 200),
        ("guess is unsure", body.get("guess") == "unsure"),
        ("degraded, model failed", body.get("degraded") and body.get("failed_signals") == ["model"]),
        (f"answered within {limit:g}s", secs <= limit),
        ("logged as degraded decision", len(log) == 1 and log[0].get("degraded") is True),
    ]), {"seconds": secs, "response": body, "log": log})


def s_model_crash(trial):
    with Faults("model_crash"):
        status, body, secs = submit()
    cid = (body or {}).get("content_id")
    log = entries(cid) if cid else []
    return (*check([
        ("200, not 500", status == 200),
        ("guess is unsure", body.get("guess") == "unsure"),
        ("degraded, model failed", body.get("failed_signals") == ["model"]),
        ("failure reason logged", bool(log) and "model_error" in str(log[0].get("failed_signals"))),
    ]), {"seconds": secs, "response": body, "log": log})


def s_style_crash(trial):
    with Faults("style_crash"):
        status, body, secs = submit()
    cid = (body or {}).get("content_id")
    log = entries(cid) if cid else []
    return (*check([
        ("200, not 500", status == 200),
        ("guess is unsure", body.get("guess") == "unsure"),
        ("degraded, style failed", body.get("failed_signals") == ["style"]),
        ("model score still reported", isinstance(body.get("model_score"), float)),
        ("failure reason logged", bool(log) and "style_error" in str(log[0].get("failed_signals"))),
    ]), {"seconds": secs, "response": body, "log": log})


def s_unreadable_text(trial):
    """No faults: real text the style signal can't read. One input per trial."""
    name = list(UNREADABLE)[(trial - 1) % len(UNREADABLE)]
    status, body, secs = submit(UNREADABLE[name])
    return (*check([
        ("never labelled AI", body.get("guess") != "ai"),
        ("unsure+degraded, or refused with 4xx",
         (status == 200 and body.get("guess") == "unsure" and body.get("degraded"))
         or 400 <= status < 500),
    ]), {"input": name, "status": status, "response": body})


def s_both_signals_fail(trial):
    before = len(audit.read_entries())
    with Faults("model_crash", "style_crash"):
        status, body, secs = submit()
    new = audit.read_entries()[before:]
    return (*check([
        ("503", status == 503),
        ("no content_id, no guess", "content_id" not in body and "guess" not in body),
        ("no decision logged", not any(e.get("status") == "decided" for e in new)),
        ("rejection logged with both reasons",
         any(e.get("reason") == "scoring_unavailable" and len(e.get("failed_signals", {})) == 2
             for e in new)),
    ]), {"response": body, "log": new})


def s_appeal_log_flaky(trial):
    _, sub, _ = submit()
    cid = sub["content_id"]
    with Faults("log_flaky"):
        status, body = appeal(cid)
    recs = appeals_for(cid)
    return (*check([
        ("200 under_review", status == 200 and body.get("status") == "under_review"),
        ("exactly one appeal record", len(recs) == 1),
        (f"record shows {config.AUDIT_WRITE_ATTEMPTS} write attempts",
         bool(recs) and recs[0].get("write_attempts") == config.AUDIT_WRITE_ATTEMPTS),
    ]), {"response": body, "log": recs})


def s_appeal_log_down(trial):
    _, sub, _ = submit()
    cid = sub["content_id"]
    with Faults("log_down"):
        status, body = appeal(cid)
    recs_while_down = appeals_for(cid)
    status2, body2 = appeal(cid)            # log back up: the writer retries
    recs_after = appeals_for(cid)
    return (*check([
        ("503 while down", status == 503),
        ("never says 'recorded' while down",
         body.get("status") != "under_review" and "has NOT been recorded" in body.get("message", "")),
        ("nothing written while down", len(recs_while_down) == 0),
        ("retry after recovery → 200", status2 == 200 and body2.get("status") == "under_review"),
        ("exactly one record after retry", len(recs_after) == 1),
    ]), {"response_down": body, "response_retry": body2, "log": recs_after})


def s_submit_log_down(trial):
    before = len(audit.read_entries())
    with Faults("log_down"):
        status, body, _ = submit()
    new = audit.read_entries()[before:]
    return (*check([
        ("503", status == 503),
        ("no content_id handed out", "content_id" not in body),
        ("no label handed out", "guess" not in body and "label" not in body),
        ("nothing in the log", not new),
    ]), {"response": body})


def s_unknown_content_id(trial):
    fake = str(uuid.uuid4())
    status, body = appeal(fake)
    log = entries(fake)
    rejected = [e for e in audit.read_entries(limit=5) if e.get("attempted_content_id") == fake]
    return (*check([
        ("404", status == 404),
        ("no appeal record", not any(e.get("event") == "appeal" for e in log)),
        ("rejection logged under attempted_content_id", len(rejected) == 1),
    ]), {"response": body, "log": rejected})


def s_duplicate_appeal(trial):
    _, sub, _ = submit()
    cid = sub["content_id"]
    s1, b1 = appeal(cid)
    s2, b2 = appeal(cid, "Sending again in case the first didn't go through.")
    recs = appeals_for(cid)
    return (*check([
        ("first 200", s1 == 200),
        ("second 409 already_appealed", s2 == 409 and b2.get("error") == "already_appealed"),
        ("second still says under_review", b2.get("status") == "under_review"),
        ("exactly one appeal record", len(recs) == 1),
    ]), {"first": b1, "second": b2, "log": recs})


def s_concurrent_appeals(trial):
    """Five appeals on one id at the same instant — the race the lock exists for."""
    _, sub, _ = submit()
    cid = sub["content_id"]
    results = []
    gate = threading.Barrier(5)

    def go():
        local = service.app.test_client()
        gate.wait()
        r = local.post("/appeal", json={"content_id": cid, "reasoning": "same time"})
        results.append(r.status_code)

    threads = [threading.Thread(target=go) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    recs = appeals_for(cid)
    return (*check([
        ("exactly one 200", results.count(200) == 1),
        ("four 409s", results.count(409) == 4),
        ("exactly one appeal record", len(recs) == 1),
    ]), {"statuses": sorted(results), "log": recs})


def s_appeal_degraded_decision(trial):
    with Faults("model_crash"):
        _, sub, _ = submit()
    cid = sub["content_id"]
    status, body = appeal(cid)
    recs = appeals_for(cid)
    return (*check([
        ("decision was degraded", sub.get("degraded") is True),
        ("appeal accepted", status == 200 and body.get("status") == "under_review"),
        ("response flags it", body.get("degraded_decision") is True),
        ("record flags it for reviewer", len(recs) == 1 and recs[0].get("degraded_decision") is True),
    ]), {"response": body, "log": recs})


SCENARIOS = [
    # (key, theme, what the bad-path rule says, function)
    ("model_timeout", "broken signal",
     "Model hangs → 200 'unsure' within timeout+3 s, logged as degraded", s_model_timeout),
    ("model_crash", "broken signal",
     "Model raises → 200 'unsure', never 500, reason logged", s_model_crash),
    ("style_crash", "broken signal",
     "Style raises → 200 'unsure', model score kept, reason logged", s_style_crash),
    ("unreadable_text", "broken signal",
     "Korean / Russian / emoji / few-words / mixed text → never 'ai'", s_unreadable_text),
    ("both_signals_fail", "broken signal",
     "Both fail → 503, no decision, rejection logged", s_both_signals_fail),
    ("appeal_log_flaky", "appeal never lost",
     "Log fails twice then works → appeal recorded once, retries visible", s_appeal_log_flaky),
    ("appeal_log_down", "appeal never lost",
     "Log down → 503, never a false 'recorded'; retry after recovery works", s_appeal_log_down),
    ("submit_log_down", "appeal never lost",
     "Log down on submit → 503, no content_id handed out", s_submit_log_down),
    ("unknown_content_id", "appeal never lost",
     "Made-up id → 404, no appeal record, attempt logged", s_unknown_content_id),
    ("duplicate_appeal", "appeal never lost",
     "Second appeal → 409, still one record", s_duplicate_appeal),
    ("concurrent_appeals", "appeal never lost",
     "5 simultaneous appeals → one 200, four 409, one record", s_concurrent_appeals),
    ("appeal_degraded_decision", "appeal never lost",
     "Appeal on a degraded decision → accepted and flagged", s_appeal_degraded_decision),
]


# ── Running and reporting ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--only", help="run one scenario by key")
    args = parser.parse_args()

    if faults.ACTIVE:
        sys.exit(f"Unset AI201_FAULTS first — the drill switches faults itself (on: {faults.ACTIVE}).")

    audit.clear()
    print(f"Loading {config.DETECTOR_MODEL}...")
    detector.warm_up()

    chosen = [s for s in SCENARIOS if not args.only or s[0] == args.only]
    if not chosen:
        sys.exit(f"No scenario '{args.only}'. Keys: {', '.join(s[0] for s in SCENARIOS)}")

    results = []
    for key, theme, rule, fn in chosen:
        trials = []
        for t in range(1, args.trials + 1):
            try:
                passed, failed, evidence = fn(t)
            except Exception as exc:  # noqa: BLE001 — a crashing trial is a failed trial
                passed, failed, evidence = False, [f"drill crashed: {type(exc).__name__}: {exc}"], {}
            trials.append((passed, failed, evidence))
        n_pass = sum(p for p, _, _ in trials)
        ok = n_pass == len(trials)
        print(f"  [{'PASS' if ok else 'FAIL'}] {key:<26} {n_pass}/{len(trials)}")
        for i, (p, failed, _) in enumerate(trials, 1):
            if not p:
                print(f"         trial {i}: {'; '.join(failed)}")
        results.append((key, theme, rule, trials))

    with service.app.test_request_context():
        health = service.health().get_json()

    path = write_report(results, health, args)
    total = sum(all(p for p, _, _ in tr) for *_, tr in results)
    print(f"\n{total}/{len(results)} scenarios passed every trial. Report: {path}")
    return 0 if total == len(results) else 1


def write_report(results, health, args):
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"failure_drill_{stamp}.md"
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Failure drill — path B",
        "",
        "- Produced by: `run_failures.py::main` (in-process, faults from `faults.py`)",
        f"- {args.trials} trials per scenario · {dt.datetime.now():%Y-%m-%d %H:%M}",
        f"- Model timeout for the drill: {config.MODEL_SIGNAL_TIMEOUT_S:g}s · "
        f"audit write attempts: {config.AUDIT_WRITE_ATTEMPTS}",
        "- A scenario passes only if **every** trial meets every condition.",
        "",
        "| Theme | Scenario | Bad-path rule | Trials passed | Verdict |",
        "|---|---|---|---|---|",
    ]
    for key, theme, rule, trials in results:
        n = sum(p for p, _, _ in trials)
        lines.append(f"| {theme} | `{key}` | {rule} | {n}/{len(trials)} | "
                     f"**{'MET' if n == len(trials) else 'MISSED'}** |")

    lines += ["", "## Instrumentation at the end of the run (`GET /health`)", "",
              "```json", json.dumps({k: health[k] for k in
                                     ("audit_writes", "signal_failures", "faults_active")},
                                    indent=2, ensure_ascii=False), "```", "",
              "## Evidence — trial 1 of each scenario, plus any failed trial", ""]

    for key, _, _, trials in results:
        lines.append(f"### `{key}`")
        for i, (p, failed, evidence) in enumerate(trials, 1):
            if i == 1 or not p:
                lines.append(f"\n**Trial {i}: {'pass' if p else 'FAIL — ' + '; '.join(failed)}**\n")
                lines += ["```json", json.dumps(evidence, indent=2, ensure_ascii=False), "```"]
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    sys.exit(main())
