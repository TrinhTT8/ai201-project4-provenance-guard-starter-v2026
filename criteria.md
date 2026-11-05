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
