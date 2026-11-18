#!/usr/bin/env python3
"""
Measure what one run costs.  <- CAPSTONE, MILESTONE 3

    python app.py                     # in one terminal, and wait for "gpt2 loaded"
    python measure_cost.py            # in another
    python measure_cost.py --runs 20

This project calls no paid API, so the cost of a run is compute: the seconds a
writer waits and the CPU-seconds the machine spends. Both are measured, not
looked up:

  - client_ms     wall-clock round trip, timed here around each request
  - duration_ms   wall-clock inside the service, from the audit log entry
  - cpu_ms        CPU time the service process used during the request
  - model_ms      the part of duration_ms spent in the GPT-2 signal

It sends your own-writing texts from scenarios.py one at a time (so cpu_ms is
exact), reads each run's entry back from GET /log by content_id, and writes
results/cost_<timestamp>.md.

It also times the one-off cost — loading the model — in a fresh process.
"""

import argparse
import datetime as dt
import statistics
import subprocess
import sys
import time
import uuid

import config
from scenarios import SCENARIOS

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"
FIELDS = ("client_ms", "duration_ms", "cpu_ms", "model_ms")


def model_load_seconds() -> float:
    """Time loading gpt2 in a brand-new process — the cold-start cost."""
    code = ("import time, detector; t = time.perf_counter(); detector.warm_up(); "
            "print(time.perf_counter() - t)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    return float(out.stdout.strip().splitlines()[-1])


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    import requests

    try:
        health = requests.get(f"{args.url}/health", timeout=5).json()
    except requests.RequestException:
        sys.exit(f"No service at {args.url}. Start it first: python app.py")
    if not health.get("detector_loaded"):
        sys.exit("The model is still loading — wait for 'gpt2 loaded and ready' and run again. "
                 "(This measures warm runs; the load is timed separately.)")
    if health.get("faults_active"):
        sys.exit(f"Faults are on ({health['faults_active']}) — restart without AI201_FAULTS.")

    texts = next(s["texts"] for s in SCENARIOS if s["name"] == "my own writing")
    rows = []
    print(f"{args.runs} runs against {args.url}")
    for i in range(args.runs):
        text = texts[i % len(texts)]
        started = time.perf_counter()
        r = requests.post(f"{args.url}/submit",
                          json={"text": text, "creator_id": f"cost_{uuid.uuid4().hex[:8]}"},
                          timeout=120)
        client_ms = round((time.perf_counter() - started) * 1000, 1)
        body = r.json()
        if r.status_code != 200:
            sys.exit(f"Run {i + 1} got {r.status_code}: {body}. Fix that before measuring cost.")

        entries = requests.get(f"{args.url}/log", params={"limit": 20}, timeout=10).json()["entries"]
        entry = next(e for e in entries if e.get("content_id") == body["content_id"])
        row = {"run": i + 1, "words": entry.get("input_words"), "client_ms": client_ms,
               "duration_ms": entry.get("duration_ms"), "cpu_ms": entry.get("cpu_ms"),
               "model_ms": entry.get("model_ms"), "guess": body.get("guess")}
        rows.append(row)
        print(f"  run {row['run']:>2}  {row['words']:>3} words  client {client_ms:>7.1f} ms  "
              f"service {row['duration_ms']:>7.1f} ms  cpu {row['cpu_ms']:>7.1f} ms  "
              f"model {row['model_ms']:>7.1f} ms")

    print("Timing a cold model load in a fresh process...")
    load_s = model_load_seconds()

    stats = {f: {"mean": statistics.mean(r[f] for r in rows),
                 "median": statistics.median(r[f] for r in rows),
                 "min": min(r[f] for r in rows), "max": max(r[f] for r in rows)}
             for f in FIELDS}
    path = write_report(rows, stats, load_s, args)

    print(f"\nMean per run: {stats['duration_ms']['mean'] / 1000:.2f} s wall, "
          f"{stats['cpu_ms']['mean'] / 1000:.2f} CPU-s "
          f"({stats['model_ms']['mean'] / stats['duration_ms']['mean']:.0%} of it the model). "
          f"Cold model load: {load_s:.1f} s.\nReport: {path}")


def write_report(rows, stats, load_s, args):
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"cost_{stamp}.md"
    config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Cost of one run",
        "",
        f"- Produced by: `measure_cost.py::main` · {args.runs} sequential runs · "
        f"{dt.datetime.now():%Y-%m-%d %H:%M}",
        f"- Model: `{config.DETECTOR_MODEL}` on CPU, max {config.DETECTOR_MAX_TOKENS} tokens",
        "- Inputs: the 'my own writing' texts from `scenarios.py`",
        "",
        "| Run | Words | Client ms | Service ms | CPU ms | Model ms | Guess |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['run']} | {r['words']} | {r['client_ms']} | {r['duration_ms']} | "
                     f"{r['cpu_ms']} | {r['model_ms']} | {r['guess']} |")
    lines += ["", "| Measure | Mean | Median | Min | Max |", "|---|---|---|---|---|"]
    for f in FIELDS:
        s = stats[f]
        lines.append(f"| {f} | {s['mean']:.1f} | {s['median']:.1f} | {s['min']:.1f} | {s['max']:.1f} |")
    lines += ["", f"**One-off cost:** loading the model in a fresh process took **{load_s:.1f} s** "
              "(paid once per server start, not per run)."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


if __name__ == "__main__":
    main()
