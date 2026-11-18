# Capstone run log — before

- Produced by: `run_capstone_eval.py::main` — each part starts the real service (`python app.py`) with the fault switches it needs, sends HTTP requests, and reads `logs/audit.jsonl`
- 3 trial(s) per criterion · 2026-11-18 11:12 · nothing changed between trials
- Inputs: `capstone_scenarios.py`. Criteria: `criteria.md`, Capstone section

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Broken signal never accuses | 15/15 unsure+degraded, 0 ai/human | 15/15 unsure+degraded, 0 ai/human | 15/15 unsure+degraded, 0 ai/human | 15/15 unsure+degraded, 0 ai/human | **MET** |
| 2. Unreadable text never labelled AI | 0 of 10 labelled AI | 0/10 AI | 0/10 AI | 0/10 AI | **MET** |
| 3. Hung model still answers in time | 5/5 within 32 s, unsure, no 500 | 5/5 in time (max 30.1s) | 5/5 in time (max 30.1s) | 5/5 in time (max 30.1s) | **MET** |
| 4. Appeal never falsely confirmed | down: 0/5 'recorded' + 5/5 503; flaky: 5/5 once | down: 0/5 'recorded', 5/5 503 · flaky: 5/5 once | down: 0/5 'recorded', 5/5 503 · flaky: 5/5 once | down: 0/5 'recorded', 5/5 503 · flaky: 5/5 once | **MET** |
| 5. Every run leaves a trace | 20/20 logged with timestamp, route, duration_ms | 20/20 logged | 20/20 logged | 20/20 logged | **MET** |

---

## What actually came back

Real responses and log entries from **trial 1** (and from any trial that failed).

### 1. Broken signal never accuses

Produced by `app.py::submit` (`_run_model_signal`, `_run_style_signal`).

**Trial 1: 15/15 unsure+degraded, 0 ai/human — pass**

```json
{
  "model_timeout": [
    {
      "status": 200,
      "seconds": 30.04,
      "response": {
        "confidence": 0.5,
        "content_id": "118eb164-a291-46e6-bd54-ae7c31fddf98",
        "degraded": true,
        "failed_signals": [
          "model"
        ],
        "guess": "unsure",
        "label": "We couldn't finish checking this text: one of our checks didn't work t…",
        "model_score": null,
        "style_score": 0.6688
      }
    }
  ],
  "model_crash": [
    {
      "status": 200,
      "seconds": 0.03,
      "response": {
        "confidence": 0.5,
        "content_id": "be0f3a41-ce8f-497b-87a7-8c67155eca9d",
        "degraded": true,
        "failed_signals": [
          "model"
        ],
        "guess": "unsure",
        "label": "We couldn't finish checking this text: one of our checks didn't work t…",
        "model_score": null,
        "style_score": 0.6688
      }
    }
  ],
  "style_crash": [
    {
      "status": 200,
      "seconds": 0.44,
      "response": {
        "confidence": 0.5,
        "content_id": "55f4418a-f46e-4891-a10a-221a8fb1c375",
        "degraded": true,
        "failed_signals": [
          "style"
        ],
        "guess": "unsure",
        "label": "We couldn't finish checking this text: one of our checks didn't work t…",
        "model_score": 0.8864,
        "style_score": null
      }
    }
  ],
  "all 15 (fault, status, guess, degraded, failed_signals)": [
    [
      "model_timeout",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_timeout",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_timeout",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_timeout",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_timeout",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_crash",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_crash",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_crash",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_crash",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "model_crash",
      200,
      "unsure",
      true,
      [
        "model"
      ]
    ],
    [
      "style_crash",
      200,
      "unsure",
      true,
      [
        "style"
      ]
    ],
    [
      "style_crash",
      200,
      "unsure",
      true,
      [
        "style"
      ]
    ],
    [
      "style_crash",
      200,
      "unsure",
      true,
      [
        "style"
      ]
    ],
    [
      "style_crash",
      200,
      "unsure",
      true,
      [
        "style"
      ]
    ],
    [
      "style_crash",
      200,
      "unsure",
      true,
      [
        "style"
      ]
    ]
  ]
}
```

### 2. Unreadable text never labelled AI

Produced by `app.py::submit`, `stylometry.py::check_measurable`.

**Trial 1: 0/10 AI — pass**

```json
[
  {
    "text": "korean",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.9543,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "chinese",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.6004,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "russian",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.923,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "arabic",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.8859,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "vietnamese",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.5662,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "spanish",
    "status": 200,
    "guess": "unsure",
    "degraded": false,
    "failed_signals": [],
    "model_score": 0.1885,
    "style_score": 0.6399,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "french",
    "status": 200,
    "guess": "unsure",
    "degraded": false,
    "failed_signals": [],
    "model_score": 0.3591,
    "style_score": 0.4343,
    "confidence": 0.3967,
    "error": null
  },
  {
    "text": "emoji_only",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.9797,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "korean_english_mix",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.9184,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "short_english",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.4927,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  }
]
```

### 3. Hung model still answers in time

Produced by `app.py::_run_model_signal`.

**Trial 1: 5/5 in time (max 30.1s) — pass**

```json
{
  "seconds": [
    30.04,
    30.05,
    30.04,
    30.05,
    30.07
  ],
  "statuses": [
    200,
    200,
    200,
    200,
    200
  ],
  "guesses": [
    "unsure",
    "unsure",
    "unsure",
    "unsure",
    "unsure"
  ],
  "failed_signals": [
    [
      "model"
    ],
    [
      "model"
    ],
    [
      "model"
    ],
    [
      "model"
    ],
    [
      "model"
    ]
  ]
}
```

### 4. Appeal never falsely confirmed

Produced by `app.py::appeal`, `audit.py::_append`.

**Trial 1: down: 0/5 'recorded', 5/5 503 · flaky: 5/5 once — pass**

```json
{
  "log_down responses": [
    {
      "status": 503,
      "content_id": "b22df542-e771-4d39-ab0c-c5edd0ec9dec",
      "error": "appeal_not_recorded",
      "message": "We couldn't save your appeal, so it has NOT been recorded yet. Please …"
    },
    {
      "status": 503,
      "content_id": "fe52af04-8552-4f50-b8d1-2f6de1b8a4b1",
      "error": "appeal_not_recorded",
      "message": "We couldn't save your appeal, so it has NOT been recorded yet. Please …"
    }
  ],
  "log_down appeal records written": 0,
  "log_flaky responses (status)": [
    200,
    200,
    200,
    200,
    200
  ],
  "log_flaky appeal records": [
    [
      {
        "timestamp": "2026-11-18T17:04:51+00:00",
        "content_id": "9c0a741a-f79a-4ff2-88bc-363a5e4b8a2d",
        "creator_id": "cap_3366f6b602",
        "event": "appeal",
        "status": "under_review",
        "reasoning": "I wrote this myself.",
        "degraded_decision": false,
        "request_id": "bcc12cf825d0",
        "route": "/appeal",
        "duration_ms": 7.4,
        "cpu_ms": 15.6,
        "write_attempts": 3
      }
    ]
  ],
  "log_flaky records per appeal": [
    1,
    1,
    1,
    1,
    1
  ]
}
```

### 5. Every run leaves a trace

Produced by `audit.py::_append`, `app.py::_run_fields`.

**Trial 1: 20/20 logged — pass**

```json
{
  "requests": [
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "submission",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "bad input: empty text",
      "status": 400,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "bad input: no text field",
      "status": 400,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "bad input: too short",
      "status": 400,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "bad input: over 1000 words",
      "status": 400,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "bad input: not JSON",
      "status": 400,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "appeal",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "appeal",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "appeal",
      "status": 200,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "repeat appeal",
      "status": 409,
      "entries found": 1,
      "complete": true
    },
    {
      "request": "repeat appeal",
      "status": 409,
      "entries found": 1,
      "complete": true
    }
  ],
  "log entries (one of each kind)": [
    {
      "timestamp": "2026-11-18T17:05:04+00:00",
      "content_id": "f4c79b11-b50c-415f-8d10-73d72c7ce362",
      "creator_id": "cap_5a6bb387aa",
      "guess": "unsure",
      "model_score": 0.8123,
      "style_score": 0.4166,
      "combined_score": 0.5,
      "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
      "status": "decided",
      "degraded": false,
      "failed_signals": null,
      "input_words": 74,
      "input_chars": 403,
      "input_preview": "This is a sentence, just a sentence. You know how sentences ",
      "model_ms": 156.8,
      "style_ms": 0.4,
      "request_id": "d620fd93ba5b",
      "route": "/submit",
      "duration_ms": 158.2,
      "cpu_ms": 1671.9
    },
    {
      "timestamp": "2026-11-18T17:05:04+00:00",
      "creator_id": "unknown",
      "event": "rejected",
      "status": "rejected",
      "reason": "missing_text",
      "request_id": "9cb3667a3780",
      "route": "/submit",
      "duration_ms": 0.7,
      "cpu_ms": 0.0,
      "input_type": "NoneType"
    },
    {
      "timestamp": "2026-11-18T17:05:05+00:00",
      "content_id": "018cb557-f588-4f95-96b0-42fb2bff958d",
      "creator_id": "cap_e1e54d0505",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this myself.",
      "degraded_decision": false,
      "request_id": "5e5a2336789b",
      "route": "/appeal",
      "duration_ms": 15.7,
      "cpu_ms": 140.6
    },
    {
      "timestamp": "2026-11-18T17:05:05+00:00",
      "creator_id": "cap_a32d94b604",
      "event": "rejected",
      "status": "rejected",
      "reason": "duplicate_appeal",
      "request_id": "1a96cade063f",
      "route": "/appeal",
      "duration_ms": 15.5,
      "cpu_ms": 187.5,
      "attempted_content_id": "1eb743e8-834d-4a85-a250-0b3da8d25338"
    }
  ]
}
```
