# Submission packet — *Epistemics for adversarial AI-assisted mathematics*

**Status: prepared, NOT submitted.** Submission is an outward-facing, hard-to-reverse
act and is the author's call, not the agent's. Everything below is ready to send;
nothing has been sent, and no account, endpoint, or mailing list has been contacted.

Source: [`METHODOLOGY.md`](../METHODOLOGY.md).

---

## Abstract (150 words, as submitted-ready)

> Two AI agents worked a single mathematics repository in parallel for ~10,700
> commits with no shared memory and no human in the inner loop. We report the
> failure modes that emerged and the controls that measurably contain them. The
> central measurement is a **rediscovery rate of 22.9%**: across 5,708 files,
> 1,308 assert a result that already exists elsewhere in the same corpus,
> uncited. A hand count over a 33× smaller sample gave 21%, so the rate is stable
> rather than anecdotal. We argue that novelty is a property of the corpus, not of
> the claim, and therefore cannot be self-checked — the failure is structural, not
> a discipline problem, and an instruction to "search first" failed twice at a
> measured cost. We give five failure modes with their signatures, six controls
> each traceable to the failure that forced it, and an observed anti-correlation
> between verifiability and novelty when mining a well-studied object.

## Claims a referee can check

Each is reproducible from the public repository; none depends on the mathematics
being correct.

| # | Claim | How to check |
|---|---|---|
| 1 | Rediscovery rate is 22.9% of 5,708 files | `py -3 scripts/rediscovery_sweep.py` |
| 2 | It is stable, not sampling noise | Pass 328's independent hand count of 21% over 173 files |
| 3 | The largest single duplicate cluster is one result in 51 files | `data/rediscovery_sweep.json`, `analysis/CANON_240_81_3.md` |
| 4 | A guard that blocks trains `--no-verify`; a guard that warns does not | design rationale in `scripts/check_rediscovery.py`, and the calibration data (bare integers flagged 97% of files) |
| 5 | Verification theatre is common and detectable | two independent instances: 19/39 Lean modules failing behind workflows aimed at a nonexistent directory; a "fail-closed" certificate carrying hand-edits its own source never emitted |
| 6 | The method produces retractions at the rate it produces results | four retractions committed in one session, listed in `METHODOLOGY.md` |

## Venues, ranked by how adversarial the review is

1. **`arXiv:cs.SE` + `cs.LO` cross-list.** No peer review, but the ratchet metric
   and the guard are the kind of thing that gets replicated or refuted quickly.
   Fastest route to being told we are wrong.
2. **AITP** (Artificial Intelligence and Theorem Proving). The right audience:
   people who will immediately ask whether 22.9% is an artifact of the tokeniser.
   That is the strongest objection and it deserves a hostile reading.
3. **Empirical Software Engineering / MSR.** Treats the repository as the dataset,
   which is what it is. Mining-challenge reviewers are unusually good at spotting
   a measurement that does not survive its own confounds.
4. **A Lean/mathlib community write-up.** Narrow but sharp: the "green over red"
   finding is directly actionable for anyone running formalization CI, and that
   community will not be polite about it.

## Known objections, and the honest answer to each

**"22.9% is an artifact of your tokeniser."** Partly fair, and the strongest
objection. The tokeniser extracts code parameters, distinctive integers and
sequences; bare integers were tried and flagged 97% of files, so they were dropped
as noise. The rate is therefore sensitive to a hand-curated choice. The defence is
the independent hand count at 21%, made before the tool existed, and the fact that
the largest cluster survives manual inspection — 51 files really do quote one code.

**"Per-file counts are dominated by synthesis documents."** True, stated in the
tool's own docstring, and the reason the per-*result* ranking is the reported one.

**"This is one repository."** Yes. The rate is not claimed to generalise; the
*method* for measuring it is. A second corpus would be the obvious next study, and
we cannot supply one.

**"The underlying mathematics is numerology."** Substantially true in places, and
the paper does not depend on it — the retractions are evidence *for* the method,
not against it. The corpus documents its own refuted claims on purpose.

**"You are the agent reporting on your own reliability."** The sharpest objection
and it has no clean answer. Every number here is machine-produced and machine-
checked. Mitigation: all of it is re-runnable by a third party from a public repo,
and the retraction list is deliberately included so the failure rate is visible
rather than inferred.

## Author decisions — RESOLVED

| question | decision |
|---|---|
| repository access | **already public** — claims 1–6 are checkable today; pinned at commit `c013cf09a` |
| authorship | **sole author, AI disclosed in methods** — keeps arXiv and AITP available, which explicit AI co-authorship would have ruled out |
| physics framing | **excised** — see [`METHODOLOGY_STANDALONE.md`](METHODOLOGY_STANDALONE.md) |

The standalone draft is the submittable artifact. It carries its own abstract,
contributions statement, AI-disclosure paragraph and limitations section, and it
describes the subject matter only where "the subject is exhausted" is load-bearing
— that exhaustion is the mechanism behind the anti-correlation, so it cannot be
dropped entirely, but no E₈ claim is made or needed. A referee can litigate the
measurement without being drawn into the mathematics.

**Still not submitted.** Nothing has been sent and no venue contacted; that remains
an outward-facing action for the author to take.
