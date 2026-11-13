"""
Fault injection for the path B failure drills.

Off unless you ask for it. Set AI201_FAULTS to a comma-separated list before
starting the service, and the matching failure happens on purpose:

    AI201_FAULTS=model_timeout python app.py

    model_timeout   the model signal hangs past MODEL_SIGNAL_TIMEOUT_S
    model_crash     the model signal raises an unexpected error
    style_crash     the style signal raises an unexpected error
    log_flaky       every audit-log write fails until its last attempt
    log_down        every audit-log write fails, every attempt

`run_failures.py` flips these in-process instead, so one run covers them all.
`GET /health` reports which faults are on, so a drill is never mistaken for
the real service.
"""

import os

KNOWN = {"model_timeout", "model_crash", "style_crash", "log_flaky", "log_down"}

ACTIVE: set[str] = {
    name.strip() for name in os.getenv("AI201_FAULTS", "").split(",") if name.strip()
}

_unknown = ACTIVE - KNOWN
if _unknown:
    raise SystemExit(f"AI201_FAULTS has unknown fault(s): {', '.join(sorted(_unknown))}. "
                     f"Known: {', '.join(sorted(KNOWN))}")


def on(name: str) -> bool:
    """Is this fault switched on right now?"""
    return name in ACTIVE
