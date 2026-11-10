# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 01:17
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

**How I judged:** "unsure" counts as HELD in every family, because it is neither an accusation nor a pass. Evasion breaks if AI text is labelled human; false_positive breaks if human text is labelled AI; prompt_injection breaks if the result is what the instruction asked for; malformed breaks on a crash or junk labelled with confidence; flood breaks if the limit never triggers. Same rules as the before run.

**Totals (after):** evasion 9 held / 1 broke (EV05) · false_positive 6 held / 2 broke (FP05, FP07) · prompt_injection 5 held / 1 broke (PI02) · malformed 18 held / 2 broke (MF06, MF07) · flood 12 held / 0 broke · **50 held / 6 broke** (before: 47 held / 9 broke).

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `60467f09-4264-473f-89fc-d4eb52aef8b7` | unsure | 0.500 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `18491c5f-740b-46c5-8e56-e7e642a19fa3` | unsure | 0.458 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `be188340-b70c-4ad7-bbfd-232d3198e893` | unsure | 0.531 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `2e1f20db-ceed-4dc6-bd51-f0b0462d1c98` | unsure | 0.612 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d15fdaf6-538d-4240-893d-ce7996b291a6` | human | 0.284 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `21fbd1f4-f638-44d4-8896-a3607b220908` | unsure | 0.481 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `52b8d862-6dee-436e-a182-8960c94fffb8` | unsure | 0.500 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `06c9153c-e59c-4513-990e-f4ccd06fd53e` | unsure | 0.500 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `40ea70f0-4aad-45f1-986a-a7643ea1221f` | unsure | 0.575 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5ffde6ee-e97c-42af-94b0-cadcacfc4ea6` | ai | 0.925 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ecacb64a-efd8-4669-9d4c-4b754f0b872e` | unsure | 0.607 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `754e8602-f847-440f-8eb9-78add555df79` | unsure | 0.739 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `6a2dc14d-12ce-4594-b243-594c969d1d17` | unsure | 0.736 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `028baf0c-1955-4380-872f-830110f25d23` | unsure | 0.694 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `e10be01b-3ee8-43c0-a693-24f86cea0d95` | ai | 0.827 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `3455c768-bca3-48e9-be7a-5898d3f28415` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `db3e8e0a-f73f-4255-9041-9725d6a123d9` | ai | 0.774 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `66398042-6ea0-4c67-aa94-d2e1c5267692` | unsure | 0.417 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `09b6dc3b-6c12-4d46-a1a0-ad19666212b8` | unsure | 0.410 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `39153841-cbe7-49cd-93a4-b305ae4487d2` | human | 0.278 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8c373e26-5911-4cab-a8b7-772ed3a63956` | unsure | 0.561 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2ce6b55a-495a-4b8b-9cc2-45dc192b84e0` | unsure | 0.460 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ae860e32-dee3-4582-84ac-d4a48463a08b` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7f0aa2e2-8e60-4ef6-8bec-39b19f4d0f0d` | unsure | 0.582 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `1d4a1f12-54de-4e27-a0a1-43a88d742fc2` | unsure | 0.500 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `300571bc-24b3-4a0d-b43c-af13beba1e23` | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `dfa4fdfd-56d4-46c6-9082-97927929ea52` | unsure | 0.500 | HELD |
| MF06 | malformed | text is emoji only | 200 | `fb6a5d5e-a7ec-48a6-bcb0-ad928dcc82ba` | ai | 0.915 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `5315b9c9-c6c1-4546-b1fc-b4804215b172` | ai | 0.870 | BROKE |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `70887ea9-d76c-471b-b940-f20b0aba78e8` | unsure | 0.370 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `86d19511-a9f6-49e0-b870-16c2e5e97d74` | unsure | 0.500 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a41d7e3f-318e-4c74-ae19-036b553e74a0` | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `00bc20f1-78ca-4229-8af9-1ed83c45d362` | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `59bf8c22-2fb1-4d01-96c8-e8d2b90912fd` | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dd27c287-d649-4501-b7f5-61173b6c506d` | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bce8b6d6-a2c2-47e3-a110-b5039aee96ea` | unsure | 0.500 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "60467f09-4264-473f-89fc-d4eb52aef8b7",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.1635,
  "style_score": 0.6452,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "18491c5f-740b-46c5-8e56-e7e642a19fa3",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4577,
  "model_score": 0.5943,
  "style_score": 0.3212,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "be188340-b70c-4ad7-bbfd-232d3198e893",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5315,
  "model_score": 0.6662,
  "style_score": 0.3968,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "2e1f20db-ceed-4dc6-bd51-f0b0462d1c98",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6116,
  "model_score": 0.6114,
  "style_score": 0.6118,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "d15fdaf6-538d-4240-893d-ce7996b291a6",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2843,
  "model_score": 0.3212,
  "style_score": 0.2474,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "21fbd1f4-f638-44d4-8896-a3607b220908",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4808,
  "model_score": 0.5727,
  "style_score": 0.3889,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "52b8d862-6dee-436e-a182-8960c94fffb8",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5862,
  "style_score": 0.1964,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "06c9153c-e59c-4513-990e-f4ccd06fd53e",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.2452,
  "style_score": 0.6115,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "40ea70f0-4aad-45f1-986a-a7643ea1221f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5749,
  "model_score": 0.7042,
  "style_score": 0.4456,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "5ffde6ee-e97c-42af-94b0-cadcacfc4ea6",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9249,
  "model_score": 0.9792,
  "style_score": 0.8707,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "ecacb64a-efd8-4669-9d4c-4b754f0b872e",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.607,
  "model_score": 0.6175,
  "style_score": 0.5964,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "754e8602-f847-440f-8eb9-78add555df79",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7389,
  "model_score": 0.7387,
  "style_score": 0.7392,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "6a2dc14d-12ce-4594-b243-594c969d1d17",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.736,
  "model_score": 0.8051,
  "style_score": 0.6669,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "028baf0c-1955-4380-872f-830110f25d23",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6942,
  "model_score": 0.8329,
  "style_score": 0.5555,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e10be01b-3ee8-43c0-a693-24f86cea0d95",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.827,
  "model_score": 0.8005,
  "style_score": 0.8535,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "3455c768-bca3-48e9-be7a-5898d3f28415",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.5268,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "db3e8e0a-f73f-4255-9041-9725d6a123d9",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7742,
  "model_score": 0.8816,
  "style_score": 0.6667,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "66398042-6ea0-4c67-aa94-d2e1c5267692",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4168,
  "model_score": 0.3223,
  "style_score": 0.5113,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "09b6dc3b-6c12-4d46-a1a0-ad19666212b8",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4103,
  "model_score": 0.4625,
  "style_score": 0.3582,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "39153841-cbe7-49cd-93a4-b305ae4487d2",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2782,
  "model_score": 0.2044,
  "style_score": 0.3521,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "8c373e26-5911-4cab-a8b7-772ed3a63956",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5608,
  "model_score": 0.5943,
  "style_score": 0.5273,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2ce6b55a-495a-4b8b-9cc2-45dc192b84e0",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4595,
  "model_score": 0.4998,
  "style_score": 0.4192,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "ae860e32-dee3-4582-84ac-d4a48463a08b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.1524,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "7f0aa2e2-8e60-4ef6-8bec-39b19f4d0f0d",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5818,
  "model_score": 0.5583,
  "style_score": 0.6053,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "1d4a1f12-54de-4e27-a0a1-43a88d742fc2",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "300571bc-24b3-4a0d-b43c-af13beba1e23",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.8333,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "dfa4fdfd-56d4-46c6-9082-97927929ea52",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "fb6a5d5e-a7ec-48a6-bcb0-ad928dcc82ba",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9151,
  "model_score": 0.9969,
  "style_score": 0.8333,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "5315b9c9-c6c1-4546-b1fc-b4804215b172",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8699,
  "model_score": 0.9064,
  "style_score": 0.8333,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "70887ea9-d76c-471b-b940-f20b0aba78e8",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3698,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "86d19511-a9f6-49e0-b870-16c2e5e97d74",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "a41d7e3f-318e-4c74-ae19-036b553e74a0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "00bc20f1-78ca-4229-8af9-1ed83c45d362",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "59bf8c22-2fb1-4d01-96c8-e8d2b90912fd",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "dd27c287-d649-4501-b7f5-61173b6c506d",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "bce8b6d6-a2c2-47e3-a110-b5039aee96ea",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
