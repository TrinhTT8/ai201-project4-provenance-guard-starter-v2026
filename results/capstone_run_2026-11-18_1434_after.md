# Capstone run log — after

- Produced by: `run_capstone_eval.py::main` — each part starts the real service (`python app.py`) with the fault switches it needs, sends HTTP requests, and reads `logs/audit.jsonl`
- 3 trial(s) per criterion · 2026-11-18 14:34 · nothing changed between trials
- Inputs: `capstone_scenarios.py`. Criteria: `criteria.md`, Capstone section

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Broken signal never accuses | 15/15 unsure+degraded, 0 ai/human | 15/15 unsure+degraded, 0 ai/human | 14/15 unsure+degraded, 0 ai/human | 15/15 unsure+degraded, 0 ai/human | **MISSED** |
| 2. Unreadable text never labelled AI | 0 of 10 labelled AI | 0/10 AI · 10/10 caught by check | 0/10 AI · 10/10 caught by check | 0/10 AI · 10/10 caught by check | **MET** |
| 3. Hung model still answers in time | 5/5 within 32 s, unsure, no 500 | 5/5 in time (max 30.1s) | 4/5 in time (max 410.8s) | 5/5 in time (max 30.1s) | **MISSED** |
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
        "content_id": "fe8c9270-584c-4024-a9c8-6ec8ad71a723",
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
        "content_id": "46a48fa0-57b4-4ec3-ac53-d18832c3dcc4",
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
      "seconds": 0.41,
      "response": {
        "confidence": 0.5,
        "content_id": "5cd953c2-d0c9-43a5-a6e0-b673629e0379",
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

**Trial 2: 14/15 unsure+degraded, 0 ai/human — FAIL**

```json
{
  "model_timeout": [
    {
      "status": 200,
      "seconds": 30.03,
      "response": {
        "confidence": 0.5,
        "content_id": "036470f9-85ce-48da-8ca6-d55e83f5a901",
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
      "seconds": 0.04,
      "response": {
        "confidence": 0.5,
        "content_id": "9dcab867-2fc0-4513-887a-0735fccb6aa8",
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
      "seconds": 0.42,
      "response": {
        "confidence": 0.5,
        "content_id": "eb172ece-7ed7-4596-b93b-2502f7873e1b",
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
      null,
      null,
      null,
      null
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

**Trial 1: 0/10 AI · 10/10 caught by check — pass**

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
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.1885,
    "style_score": null,
    "confidence": 0.5,
    "error": null
  },
  {
    "text": "french",
    "status": 200,
    "guess": "unsure",
    "degraded": true,
    "failed_signals": [
      "style"
    ],
    "model_score": 0.3591,
    "style_score": null,
    "confidence": 0.5,
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
    30.03,
    30.05,
    30.05
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

**Trial 2: 4/5 in time (max 410.8s) — FAIL**

```json
{
  "seconds": [
    30.03,
    30.03,
    410.82,
    30.31,
    30.02
  ],
  "statuses": [
    200,
    200,
    null,
    200,
    200
  ],
  "guesses": [
    "unsure",
    "unsure",
    null,
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
    null,
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
      "content_id": "a7c775e1-eee4-4766-8be8-207a5ba5955a",
      "error": "appeal_not_recorded",
      "message": "We couldn't save your appeal, so it has NOT been recorded yet. Please …"
    },
    {
      "status": 503,
      "content_id": "6ed35a0a-d2e3-499b-bc24-f0d7faa5ee17",
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
        "timestamp": "2026-11-18T20:18:52+00:00",
        "content_id": "8e655cdc-fb7c-4a97-a7c2-36593c129e5a",
        "creator_id": "cap_fc1e0367fc",
        "event": "appeal",
        "status": "under_review",
        "reasoning": "I wrote this myself.",
        "degraded_decision": false,
        "request_id": "e61d3e799954",
        "route": "/appeal",
        "duration_ms": 17.8,
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
      "timestamp": "2026-11-18T20:19:04+00:00",
      "content_id": "824081f8-8b9e-4233-b8bb-84270d07ddbc",
      "creator_id": "cap_ccad61bab9",
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
      "model_ms": 119.6,
      "style_ms": 0.4,
      "request_id": "a4a1589d9a8f",
      "route": "/submit",
      "duration_ms": 121.0,
      "cpu_ms": 1250.0
    },
    {
      "timestamp": "2026-11-18T20:19:04+00:00",
      "creator_id": "unknown",
      "event": "rejected",
      "status": "rejected",
      "reason": "missing_text",
      "request_id": "8216cb99425a",
      "route": "/submit",
      "duration_ms": 0.4,
      "cpu_ms": 0.0,
      "input_type": "NoneType"
    },
    {
      "timestamp": "2026-11-18T20:19:04+00:00",
      "content_id": "59d6307e-25d7-4082-921e-3ea2eb5922df",
      "creator_id": "cap_0c031375f9",
      "event": "appeal",
      "status": "under_review",
      "reasoning": "I wrote this myself.",
      "degraded_decision": false,
      "request_id": "1835df429c58",
      "route": "/appeal",
      "duration_ms": 22.1,
      "cpu_ms": 328.1
    },
    {
      "timestamp": "2026-11-18T20:19:04+00:00",
      "creator_id": "cap_bcfd08d8b1",
      "event": "rejected",
      "status": "rejected",
      "reason": "duplicate_appeal",
      "request_id": "924e25a8f72c",
      "route": "/appeal",
      "duration_ms": 17.4,
      "cpu_ms": 0.0,
      "attempted_content_id": "c4898bc9-410b-41b4-8ba0-c2bc2803b4c0"
    }
  ]
}
```
