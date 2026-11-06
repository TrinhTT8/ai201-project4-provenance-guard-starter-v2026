# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Step 1: The text arrives as the JSON body of an HTTP request. It's sent to `POST /submit` with `text` and `creator_id`. The route in `app.py` pulls those two fields out of the request.

Step 2: `detector.py::model_signal` reads in the text and scores how predictable it is, giving a model score from 0 to 1 (higher means more likely AI).

Step 3: `stylometry.py::style_signal` analyzes the text's shape and gives it a style score from 0 to 1 as well (higher means more likely AI).

Step 4: `scoring.py::combine_signals` combines the scores of step 2 and 3 into one score.

Step 5: Based on the combined score, `scoring.py::score_to_label` guesses whether the text was written by AI or a human. If the score falls in the middle, it guesses unsure. It also produces the label sentence a reader will see.

Step 6: `audit.py::log_decision` saves the guess, the combined score and both signal scores to the audit log, under a new `content_id`.

Step 7: The route returns a JSON response to the writer with the `content_id`, guess, confidence, label and both signal scores. The writer needs the `content_id` if they want to appeal.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** This signal measures how predictable the input text is to a local language model (GPT-2). This is called perplexity: low perplexity means the model could have guessed the text, and high perplexity means the text surprised it. `detector.py::model_signal` turns that into a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** Language models are built to predict the most likely next word, so text a model wrote tends to be text a model finds easy to predict. Human texts are more unpredictable. For instance, human texts can have sharp changes and odd word choices, and different people write with the words and tone they're used to.

**What it can't see:** Predictability is not the same thing as authorship. If a human writes simply, using common words in short, ordinary sentences, the text is predictable and scores as AI. That includes someone writing in a second language, a younger writer, or anyone writing plainly on purpose. These are the writers this signal is most likely to accuse falsely. Going the other way, dense writing full of rare words can score as human even if AI wrote it. Very short texts are also hard to judge, because there's too little to be surprised by.

### Signal two — the style signal

**What it measures:** This signal measures the shape of the text without reading it: how much sentence lengths vary, how varied the vocabulary is (unique words over total words), and how much punctuation is used. `stylometry.py::style_signal` combines these into a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** Human writing is less repetitive and more uneven. A short sentence can sit next to a very long one, some texts contain a lot more punctuation, and some of it isn't placed by the rules. AI writing follows a pattern: sentence length, punctuation and vocabulary are more even and limited, because picking the most likely next word produces average, mid-length sentences. AI also tends to use a narrower vocabulary than humans.

**What it can't see:** This signal can't read the text. It doesn't judge the meaning, so anything that changes the shape without changing the meaning moves the score. Adding typos, breaking up sentences or pasting in a quotation can make AI text look human without changing what it says.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Scores from `detector.py` (signal one) and `stylometry.py` (signal two) are averaged with equal 50/50 weights, so neither signal overrules the other. Both carry useful information and both have blind spots. There's one exception: if the two scores are 0.30 or more apart, the signals are contradicting each other, so the combined score is set to 0.5 (unsure) instead of the average. A split vote should never be enough to accuse someone.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`, `DISAGREEMENT_GAP = 0.30`

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
I took an AI-written paragraph about time management and lightly edited it: casual words, a couple of very short sentences, an exclamation mark. Signal one scored it 0.68 (AI-ish), because the word choices were still predictable. Signal two scored it 0.37 (human-ish), because the short sentences and extra punctuation made its shape look human. The gap is 0.31, over my 0.30 limit, so the rule sets the combined score to 0.5 (unsure) instead of the plain average of 0.53. The label is the same either way, but the rule makes the reason explicit: the signals disagree, so the system doesn't guess.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range | The exact text a reader sees                                                                                                                                                                                                                                                    |
| --------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high-confidence human | 0.00 -0.35  | We think this was probably written by a person.                                                                                                                                                                                                                                 |
| unsure                | 0.35 - 0.65 | We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it. |
| high-confidence AI    | 0.65 - 1.00 | This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.                                                               |

**Why I worded the "unsure" one this way:** I want the message to acknowledge that the system can be wrong because the person may have written every word themselves, yet their writing can still look similar to AI writing. It's important that in these cases, we don't accuse the writer but let them have a chance to appeal and understand the reasons why their text was labelled as unsure.

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "My favorite ice cream flavor is cookies and cream. The ice cream shop near my house sells the best cookie and cream flavor ever! I go back all the time!", "creator_id": "me"}'
```

```json
{
  "confidence": 0.6521,
  "content_id": "2de372b7-07ed-4fe2-a2fe-b0dbe7d027b1",
  "guess": null,
  "label": "PLACEHOLDER \u2014 labels come in Milestone 5.",
  "model_score": 0.6521,
  "style_score": null
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c5a9e990-ceb9-43dc-8d6c-7616d1ca9dbc",
  "reasoning": "I wrote this myself for a study skills class. I didn''t use any AI tools."}'
```

```json
{
  "content_id": "c5a9e990-ceb9-43dc-8d6c-7616d1ca9dbc",
  "message": "Thanks. Your appeal has been recorded, and a person will review this decision.",
  "original_guess": "ai",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.6425,
      "content_id": "5fd4b842-0f89-46f6-b562-0bb6c13a1f49",
      "creator_id": "test-unsure",
      "guess": "unsure",
      "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written.",
      "model_score": 0.6406,
      "status": "decided",
      "style_score": 0.6444,
      "timestamp": "2026-11-05T05:11:42+00:00"
    },
    {
      "combined_score": 0.6935,
      "content_id": "c5a9e990-ceb9-43dc-8d6c-7616d1ca9dbc",
      "creator_id": "test-ai",
      "guess": "ai",
      "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
      "model_score": 0.8323,
      "status": "decided",
      "style_score": 0.5548,
      "timestamp": "2026-11-05T05:11:50+00:00"
    },
    {
      "content_id": "c5a9e990-ceb9-43dc-8d6c-7616d1ca9dbc",
      "creator_id": "test-ai",
      "event": "appeal",
      "reasoning": "I wrote this myself for a study skills class. I didn't use any AI tools.",
      "status": "under_review",
      "timestamp": "2026-11-05T19:51:28+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- _What I asked for:_ I have used Claude to help critic my criteria.
- _What came back:_ It suggested to me that my first 3 criteria were weak and that they will never passed due to the wording.
- _What I changed:_ I went back and reworded my criteria and added more specific numbers such as # out of # times, # of AI labels, # of human labels, etc.

**Moment 2**

- _What I asked for:_ I asked Claude to help me to finish `detector.py` and `stylometry.py` files.
- _What came back:_ It filled in the functions within two files and explained the code that it had written.
- _What I changed:_ I read all the code that it generated, and added in comments so I could understand them better.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** **5** per minute, **150** per day

**Why those numbers and not others:** A real writer submits their work a few times at most: once, maybe again after a revision, maybe once more to check a label. 5 per minute leaves plenty of room for that. What 5 per minute blocks is someone changing a single word or quotation and resubmitting over and over to watch the score move. That's how a person or script maps my thresholds to sneak AI text under them. 150 per day is far more than any honest writer needs, but it caps a script at 150 attempts per creator_id per day instead of thousands. The weakness is that a script can switch to a new creator_id to get a fresh limit, so these numbers slow down an attacker but can't stop one alone.

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** creator_id, falling back to the IP address when no creator_id is sent. The weakness: a script can send a different creator_id on every request and never hit the limit. The upside: people sharing one network, like a household or a classroom, don't use up each other's limits.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

I have ran `run_attacks.py` once before flooding it with 15 more requests. Therefore, you will see the cut off is at request 4 and not 5.

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 429
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 429 429 429 429 429 429 429 429 429 429 429
============================================================
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

**1. EV01 · evasion · typos raise word variety**

```json
{
  "timestamp": "2026-11-05T21:02:56+00:00",
  "content_id": "d23fa7cf-ef8c-4055-a364-c39e3e6ee599",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "model_score": 0.1635,
  "style_score": 0.6452,
  "combined_score": 0.5,
  "label": "We couldn't tell whether this was written by a person or with help from AI. This is not an accusation. Our checks gave mixed results, and your work has not been marked as AI-written. If you'd like, you can appeal and tell us how you wrote it, and a person will review it.",
  "status": "decided"
}
```

**2. EV05 · evasion · heavy human editing pass**

```json
{
  "timestamp": "2026-11-05T21:02:57+00:00",
  "content_id": "d4834c1e-a7d9-4553-bc5a-2ea0565d31f7",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "model_score": 0.3212,
  "style_score": 0.2474,
  "combined_score": 0.2843,
  "label": "We think this was probably written by a person.",
  "status": "decided"
}
```

**3. EV10 · evasion · repeated stanza structure**

```json
{
  "timestamp": "2026-11-05T21:02:58+00:00",
  "content_id": "d215aa9e-cbea-49f6-a24d-10f670f35cbb",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "model_score": 0.9792,
  "style_score": 0.8707,
  "combined_score": 0.9249,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**4. FP03 · false positive · a non-native English speaker writing carefully**

```json
{
  "timestamp": "2026-11-05T21:02:59+00:00",
  "content_id": "af9d5ef3-1d34-423f-b8c7-1946766ec7a9",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "model_score": 0.8051,
  "style_score": 0.6669,
  "combined_score": 0.736,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**5. FP05 · false positive · technical documentation written by a person**

```json
{
  "timestamp": "2026-11-05T21:02:59+00:00",
  "content_id": "6af0a137-c747-42ea-9a75-ec186a686065",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "model_score": 0.8005,
  "style_score": 0.8535,
  "combined_score": 0.827,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**6. FP07 · false positive · human writing that repeats a phrase deliberately**

```json
{
  "timestamp": "2026-11-05T21:03:00+00:00",
  "content_id": "754142d2-9d25-417c-be46-caf70f2985eb",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "model_score": 0.8816,
  "style_score": 0.6667,
  "combined_score": 0.7742,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**7. PI02 · prompt injection · instruction disguised as a system message**

```json
{
  "timestamp": "2026-11-05T21:03:00+00:00",
  "content_id": "454b2d2e-6b76-4e39-9c04-28035ef52af2",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "model_score": 0.2044,
  "style_score": 0.3521,
  "combined_score": 0.2782,
  "label": "We think this was probably written by a person.",
  "status": "decided"
}
```

**8. MF06 · malformed · text is emoji only**

```json
{
  "timestamp": "2026-11-05T21:03:02+00:00",
  "content_id": "045673ea-12f0-4856-be57-cc8a0aeff746",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "model_score": 0.9969,
  "style_score": 0.8333,
  "combined_score": 0.9151,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**9. MF07 · malformed · text is right-to-left script**

```json
{
  "timestamp": "2026-11-05T21:03:02+00:00",
  "content_id": "60efe6a7-3bd5-443b-83f6-aa6fcfef9e57",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "model_score": 0.9064,
  "style_score": 0.8333,
  "combined_score": 0.8699,
  "label": "This writing has strong patterns that are common in AI-generated text. Our checks can be wrong, especially with plain or simple writing. If you wrote this yourself, you can appeal, and a person will review it.",
  "status": "decided"
}
```

**10. FL01 · flood · 20 rapid submissions from one creator (rejected by the rate limit)**

```json
{
  "timestamp": "2026-11-05T21:03:03+00:00",
  "creator_id": "attacker_flood",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "5 per 1 minute"
}
```

**The single worst outcome:** FP03, a non-native English speaker writing carefully.

I chose FP03 because the system has no guardrails for people writing in a second language.

This is the outcome I'd least want to explain, because this writer did everything right. They wrote carefully, and that care is what got them accused. They may also be the person least confident about arguing back in English, so the appeal path is weakest exactly where it's needed most. It's the false positive I traced in Milestone 1, showing up exactly as predicted.

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
