# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

At most 1 out of 10 human-written pieces is labelled high-confidence AI, in every trial.

**Why this target:** On a writing site, wrongly accusing a real writer costs that person far more than a missed AI text costs the site. Both signals have blind spots, especially signal one with plain, simple writing, so zero mistakes isn't realistic. But false accusations should be rare, so I allow at most 1 in 10.

---

## 2.

An appeal on a real `content_id` gets recorded in the audit log and its status changes to `under_review` in 5 out of 5 tries. An appeal on a `content_id` that doesn't exist returns an error and records nothing, in 5 out of 5 tries.

**Why this target:** This is a mandatory process that doesn't rely on the AI prediction. All appeals are expected to be recorded and given a status as they come in. An appeal is the only thing standing between a wrong accusation and nothing at all, so it can't fail silently, and a typo in the `content_id` has to tell the writer something went wrong.


---

## 3.

<!-- Your criterion. -->
At least 4 of 5 clearly-AI texts score above 0.65, and at least 4 of 5 clearly-human texts score below 0.35, in every trial.


**Why this target:** The unsure range is 0.30 wide (from 0.35 to 0.65), so clearly-AI and clearly-human text need to be at least that far apart for the system to actually tell them apart. If fewer than 80% (4 of 5) land on the correct side, our signals aren't separating them well enough and need tightening.



---

## 4.

Of my 5 test texts (2 clearly human, 2 clearly AI, 1 borderline), no more than 2 are labelled unsure, in every trial.


**Why this target:** Only 1 of the 5 texts is genuinely borderline, so it's the only one that should land in unsure. I allow 1 extra for the signals' blind spots. If 3 or more (60%) are unsure, the system isn't making clear judgements, which usually means one signal isn't varying enough.



---

## 5.

<!-- Your criterion. -->
When `text` is missing, empty, or over 1000 words, `/submit` returns a 400 error with a message explaining the problem, never a 500 crash and never a score, in 5 out of 5 cases.


**Why this target:**
If there is no given text, the system cannot predict; therefore, this criterion makes sure no empty text is being passed through and scored. Enormous text is a common way to break or slow down a service, so it gets rejected the same way. The writer should always get a clear message instead of a crash.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Capstone criteria — path B, harden against failure

Written before any capstone test was run. Criteria 1–4 are about the extension; criterion 5 is about the run log from Milestone 3.

---

## 1.

When one signal is broken on purpose — the model times out, the model crashes, or the style signal crashes, 5 submissions each (15 total) — 15 out of 15 come back as `unsure` with `degraded: true`, and none of them is labelled AI or human, in every trial.

**Why this target:** This is the whole point of the extension. If a broken signal produces even one "AI" label, a real writer got accused because of a bug, not because of their writing, so I don't allow any. It isn't allowed to say "human" either, because one working signal is only half the evidence, and my disagreement rule already says half the evidence isn't enough to decide.

---

## 2.

Of 10 texts the style signal wasn't built to read — Korean, Chinese, Russian, Arabic, Vietnamese, Spanish, French, emoji only, Korean mixed with English, and one short English sentence — 0 are labelled high-confidence AI, in every trial.

**Why this target:** Before the extension, a Korean paragraph was labelled high-confidence AI (combined score 0.89) only because the style signal counted it as zero words. People writing in their own language, or a second one, are exactly the writers this system is most likely to accuse, so 0 is the only fair number. My first criterion allows 1 in 10 for human writing because the signals can honestly misjudge it, but here the signal can't read the text at all, so any AI label comes from a broken measurement. I put Spanish, French and Vietnamese in on purpose: they mostly use English letters, so the readability check might still let them through, and I want to know if it does.

---

## 3.

When the model hangs, `/submit` still answers within 32 seconds (the real 30-second timeout plus 2 seconds) in 5 out of 5 tries, and every answer is `unsure`, never a 500 error.

**Why this target:** Before the extension, a hung model meant the writer waited forever with no answer. A normal run takes about 0.4–2 seconds and loading the model takes about 17, so 30 seconds is long enough that a slow-but-working model isn't cut off. I allow only 2 extra seconds because everything after the timeout (the style signal, the log write, the reply) takes milliseconds; a looser margin would hide a second slow step I don't know about.

---

## 4.

When the audit log can't be written at all, 0 out of 5 appeals get a "recorded" message and all 5 get a 503 error. When the log fails twice and then works, 5 out of 5 appeals are recorded exactly once. In every trial.

**Why this target:** A false "your appeal has been recorded" is worse than an error. The writer stops trying, and nobody ever reviews their case, so I allow 0. The retry also can't create extra copies of the appeal, because a reviewer seeing the same appeal twice can't tell if the writer appealed twice. Since the appeal is the only thing standing between a wrong accusation and nothing at all, it has to be all or nothing.

---

## 5.

Of 20 requests sent to the running service — 10 normal submissions, 5 bad inputs (empty text, no `text` field, too short, over 1000 words, and a body that isn't JSON), 3 appeals and 2 repeat appeals — 20 out of 20 show up in `logs/audit.jsonl` with a `timestamp`, `route` and `duration_ms`, in every trial.

**Why this target:** If a request isn't in the log, I can't diagnose it later, and a failure that only shows up as a missing line is one I'll never find. Bad inputs and repeat appeals are in the set on purpose, because those are the requests most likely to be skipped. I don't allow 19 out of 20, because the missing one could be an appeal, and a missing appeal is a lost appeal.
