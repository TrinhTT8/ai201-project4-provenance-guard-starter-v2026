#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import sys
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout

from flask import Flask, jsonify, request

import audit
import config
import faults
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        _log_rejection_safely(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
        # Path B instrumentation: counts since this process started.
        "faults_active": sorted(faults.ACTIVE),
        "audit_writes": dict(audit.WRITE_STATS),
        "signal_failures": dict(SIGNAL_STATS),
    })


# ── Running the signals so a failure can't become a verdict (path B) ─────────
#
# Each signal runs behind a wrapper that returns (score, None) when it worked
# and (None, reason) when it didn't. The route never sees an exception from a
# signal — except a too-short text, which is a problem with the input, not the
# signal, and still gets a 400.

SIGNAL_STATS = {"model_timeout": 0, "model_error": 0, "style_unmeasurable": 0, "style_error": 0}

# A thread can't be killed, so a timed-out call keeps running in the
# background until it finishes. Four workers means a few hung calls don't
# block every later submission; the timeout still answers the writer on time.
_model_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="model-signal")


def _model_work(text):
    import detector

    if faults.on("model_crash"):
        raise RuntimeError("injected fault: model signal crashed")
    if faults.on("model_timeout"):
        time.sleep(config.MODEL_SIGNAL_TIMEOUT_S + 1)
    return detector.model_signal(text)


def _run_model_signal(text):
    import detector

    future = _model_pool.submit(_model_work, text)
    try:
        return future.result(timeout=config.MODEL_SIGNAL_TIMEOUT_S), None
    except FutureTimeout:
        SIGNAL_STATS["model_timeout"] += 1
        return None, f"model_timeout: no answer within {config.MODEL_SIGNAL_TIMEOUT_S:g}s"
    except ValueError:
        raise                                   # too short: the input's fault → 400
    except detector.DetectorUnavailable as exc:
        SIGNAL_STATS["model_error"] += 1
        return None, f"model_unavailable: {str(exc).splitlines()[0]}"
    except Exception as exc:  # noqa: BLE001 — any crash is a failed signal, not a 500
        SIGNAL_STATS["model_error"] += 1
        return None, f"model_error: {type(exc).__name__}: {exc}"


def _run_style_signal(text):
    try:
        if faults.on("style_crash"):
            raise RuntimeError("injected fault: style signal crashed")
        return stylometry.style_signal(text), None
    except stylometry.StyleUnmeasurable as exc:
        SIGNAL_STATS["style_unmeasurable"] += 1
        return None, f"style_unmeasurable: {exc}"
    except Exception as exc:  # noqa: BLE001
        SIGNAL_STATS["style_error"] += 1
        return None, f"style_error: {type(exc).__name__}: {exc}"


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    # ── Pull out the two fields ──────────────────────────────────────────────
    text = payload.get("text")
    creator_id = payload.get("creator_id")
    if not isinstance(creator_id, str) or not creator_id.strip():
        creator_id = "unknown"

    # ── Bad input gets a 400, never a crash (criterion 5) ────────────────────
    if not isinstance(text, str) or not text.strip():
        return _reject(creator_id, "missing_text", "Send some text in the \"text\" field.")
    if len(text.split()) > MAX_WORDS:
        return _reject(creator_id, "text_too_long", f"Text is over {MAX_WORDS} words.")

    # ── Both signals, each behind a wrapper that can't throw (path B) ────────
    try:
        model_score, model_failure = _run_model_signal(text)
    except ValueError:
        return _reject(creator_id, "text_too_short", "Text is too short to score — a few sentences at least.")
    style_score, style_failure = _run_style_signal(text)
    failed_signals = {name: why for name, why in
                      (("model", model_failure), ("style", style_failure)) if why}

    # ── Nothing worked: no evidence, so no decision at all ───────────────────
    if len(failed_signals) == 2:
        return _reject(creator_id, "scoring_unavailable",
                       "We couldn't check this text right now. Nothing has been decided "
                       "about it. Please try again in a few minutes.",
                       503, failed_signals=failed_signals)

    # ── A broken signal never produces an accusation ─────────────────────────
    # One working signal is half the evidence, and the disagreement rule
    # already says half the evidence isn't enough. Always "unsure", never a
    # verdict either way, and the log says which signal failed and why.
    if failed_signals:
        combined_score = 0.5
        guess, label = "unsure", scoring.LABEL_DEGRADED
    else:
        combined_score = scoring.combine_signals(model_score, style_score)
        guess, label = scoring.score_to_label(combined_score)

    # ── Log it. The content_id is what /appeal looks up later ────────────────
    # If the decision can't be written, the writer doesn't get a content_id:
    # an id that isn't in the log is an appeal that would be refused later.
    content_id = str(uuid.uuid4())
    try:
        audit.log_decision(
            content_id=content_id,
            creator_id=creator_id,
            guess=guess,
            model_score=model_score,
            style_score=style_score,
            combined_score=combined_score,
            label=label,
            degraded=bool(failed_signals),
            failed_signals=failed_signals or None,
        )
    except audit.AuditWriteError as exc:
        print(f"[submit] decision NOT recorded for {creator_id}: {exc}", file=sys.stderr)
        return jsonify({
            "error": "not_recorded",
            "message": "We checked your text but couldn't save the result, so no label "
                       "has been given. Please submit it again in a moment.",
        }), 503

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined_score,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "degraded": bool(failed_signals),
        "failed_signals": sorted(failed_signals),
    })


MAX_WORDS = 1000


def _reject(creator_id, reason, message, status=400, **extra):
    """Refuse a request, and leave a trace of it in the log."""
    _log_rejection_safely(creator_id=creator_id, reason=reason, route=request.path, **extra)
    return jsonify({"error": reason, "message": message}), status


def _log_rejection_safely(**fields):
    """
    A rejection's trace, best effort. If the log itself is down, the writer
    still gets their clear 4xx/5xx — not a 500 from a failed write — and the
    lost trace goes to stderr so it isn't silent.
    """
    try:
        audit.log_rejection(**fields)
    except audit.AuditWriteError as exc:
        print(f"[audit] rejection NOT logged {fields}: {exc}", file=sys.stderr)


# Check-then-write for one appeal must not interleave with another, or two
# simultaneous appeals on the same id would both see "no appeal yet".
_appeal_lock = threading.Lock()


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        payload = {}

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    caller = payload.get("creator_id") if isinstance(payload.get("creator_id"), str) else "unknown"

    if not isinstance(content_id, str) or not content_id.strip():
        return _reject(caller, "missing_content_id",
                       "Send the content_id from your submission's response.")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _reject(caller, "missing_reasoning",
                       "Tell us why you think the label is wrong.")

    # ── The id has to point at a real decision (criterion 2) ─────────────────
    # Logged as attempted_content_id, not content_id, so a bad guess never
    # shows up as part of a real item's history.
    content_id = content_id.strip()

    with _appeal_lock:
        history = audit.entries_for(content_id)
        decisions = [e for e in history if e.get("status") == "decided"]
        if not decisions:
            return _reject(caller, "unknown_content_id",
                           f"No submission found with content_id {content_id}. Check it was copied exactly.",
                           404, attempted_content_id=content_id)

        # ── One appeal per decision (path B) ─────────────────────────────────
        # A writer retrying after a dropped connection must not create a
        # second record. 409 says so plainly — and that the first one stands.
        earlier = [e for e in history if e.get("event") == "appeal"]
        if earlier:
            _log_rejection_safely(creator_id=caller, reason="duplicate_appeal",
                                  route=request.path, attempted_content_id=content_id)
            return jsonify({
                "error": "already_appealed",
                "content_id": content_id,
                "status": "under_review",
                "appealed_at": earlier[0].get("timestamp"),
                "message": "This decision is already under review. Your earlier appeal is on "
                           "file, and a person will look at it — you don't need to send another.",
            }), 409

        # ── Appealing a decision made with a broken signal (path B) ──────────
        # Allowed, and flagged, so a reviewer knows the label rests on half
        # the evidence and can look at it first.
        original = decisions[0]
        degraded = bool(original.get("degraded"))

        # ── Never confirm an appeal that isn't on disk (path B) ──────────────
        # audit retries the write; if every attempt fails, the writer is told
        # it was NOT recorded. The appeal sits after the original decision.
        try:
            audit.log_appeal(
                content_id=content_id,
                creator_id=original.get("creator_id", "unknown"),
                reasoning=reasoning.strip(),
                degraded_decision=degraded,
            )
        except audit.AuditWriteError as exc:
            print(f"[appeal] NOT recorded for {content_id}: {exc}", file=sys.stderr)
            return jsonify({
                "error": "appeal_not_recorded",
                "content_id": content_id,
                "message": "We couldn't save your appeal, so it has NOT been recorded yet. "
                           "Please send it again in a moment — your content_id is still valid.",
            }), 503

    message = "Thanks. Your appeal has been recorded, and a person will review this decision."
    if degraded:
        message += (" This decision was made while one of our checks wasn't working, so it "
                    "has been flagged for the reviewer.")
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "original_guess": original.get("guess"),
        "degraded_decision": degraded,
        "message": message,
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print(f"  model timeout:   {config.MODEL_SIGNAL_TIMEOUT_S:g}s")
    if faults.ACTIVE:
        print(f"  ⚠️  FAULTS ON:    {', '.join(sorted(faults.ACTIVE))}  (failure drill — not real service)")
    print()

    # Load the model now, in the background, so the first writer's request
    # isn't the one that pays the 10–20 s load and trips the timeout.
    def warm():
        import detector
        try:
            print(f"  {detector.warm_up()}")
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠️  model warm-up failed: {exc}", file=sys.stderr)

    threading.Thread(target=warm, daemon=True).start()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
