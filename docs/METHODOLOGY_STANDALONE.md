# Rediscovery is a measurable rate: epistemics for adversarial AI-assisted mathematics

**Author:** Wil (sole author).
**AI disclosure:** the corpus studied here was produced by two AI agents working in
parallel, and the measurement tooling described in §3 was written by one of them
under the author's direction. Method, framing and all claims are the author's
responsibility. See §7 for the full contributions statement.

**Artifacts:** <https://github.com/wilcompute/W33-Theory> — public. All claims below
are checkable at commit `c013cf09a`; every command is given inline.

---

## Abstract

Two AI agents worked a single mathematics repository in parallel for ~10,700
commits with no shared memory and no human in the inner loop. We report the failure
modes that emerged and the controls that measurably contain them. The central
measurement is a **rediscovery rate of 22.9%**: across 5,708 files, 1,308 assert a
result that already exists elsewhere in the same corpus, uncited. An independent
hand count over a 33× smaller sample gave 21%, so the rate is stable rather than
anecdotal. We argue that novelty is a property of the corpus, not of the claim, and
therefore cannot be self-checked — the failure is structural, not a discipline
problem, and a standing instruction to "search first" failed twice at measured cost.
We give five failure modes with their signatures, six controls each traceable to the
failure that forced it, and an observed anti-correlation between verifiability and
novelty when mining a well-studied object.

## 1. Setting

The subject matter is deliberately not the point of this paper and is described
only to the extent that it shapes the measurement: a finite geometry and an
associated root system, both studied continuously for over a century. What matters
methodologically is that the subject is **exhausted** — the space of true,
reachable, novel structural facts is close to empty, while the space of false
patterns is enormous and a machine generates them quickly.

Scale: ~19,800 tracked files, ~2,900 JSON certificates, ~3,000 tests, ~1,030
numbered work units. Two agents, neither reading the other's filenames, neither
retaining memory between sessions.

## 2. The corpus is indexed by time, not by content

Files are named for the date they were produced (`2026-07-10_levi_next5.md`) or for
a sequence number (`PASS178_…`). A file named for a date carries no topic signal, so
**a topic search cannot find it**. The operative rule that follows:

> Search for the **result** — the formula, the integer, the parameter triple — not
> the topic. A distinctive integer hits on day one; the word "rank" never does.

## 3. The measurement

```bash
py -3 scripts/rediscovery_sweep.py
#   scanned                  5708
#   with uncited collisions  1308   (22.9%)
#   merge-list rows           859
```

The tool extracts *results* (code parameters, distinctive integers, sequences, and a
hand-curated lexicon of named objects) from every file, looks them up in an inverted
index, and reports collisions where the asserting file cites none of the prior
locations. Largest single cluster: one code quoted in **51 files** that cite none of
the others.

**Confounds, stated.** The per-*file* ranking is dominated by synthesis documents
that legitimately name many results; the per-*result* ranking is the reported one.
Token classes are hand-curated: bare integers were tried and flagged 97% of files,
so they were dropped as noise. The rate is therefore sensitive to that choice, which
is the strongest objection to this paper (§6).

**It is tracked, not merely measured.** A CI job re-measures on every push and fails
when the ratio worsens, as a ratchet against a checked-in baseline rather than a
fixed threshold — a threshold either never fires or blocks unrelated work.

## 4. Five failure modes

| # | Mode | Signature | Control |
|---|---|---|---|
| 1 | Coordinate artefact | metric claim refuted by a second realization | check a second basis before publishing anything metric |
| 2 | Over-read | result right, framing exceeds the proof | state the scope the witness establishes, not its implication |
| 3 | Unbuilt object | a claim naming no map — unrefutable *and* unusable | name the map or state the open question |
| 4 | Unbuilt half | one ungrounded sentence in a sound file | read; a file-level audit passes it |
| 5 | **Rediscovery** | nothing internal is wrong; only novelty is false | **cannot be self-checked** |

Mode 5 is why the rest exists:

> **Novelty is not a property of the claim. It is a property of the corpus.** A unit
> of work can be internally flawless — correct, witnessed, proportionately framed,
> with a named object — and still be worthless, and nothing inside it can detect this.

## 5. Six controls, each with the failure that forced it

1. **Search by result before computing.** Two rediscoveries cost ~19 work units.
2. **Reserve identity before working.** An empty commit claiming the sequence number,
   pushed first. Three renumbers in one day preceded this rule; one produced a
   silently wrong ledger row.
3. **Warn, never block.** Blocking trains `--no-verify`, which is worse than no hook.
4. **Idempotent certificates, tested by deletion.** This caught an artifact carrying
   hand-edits its own generator never emitted, inside a job configured to fail closed
   on stale certificates.
5. **Ownership by first commit**, resolved with `git log --diff-filter=A`, not memory.
6. **Read, don't grep-and-discard.** Two conclusions were retracted after shallow
   searches; a negative search must state which space it covered.

## 6. The anti-correlation, and the one exception

Across a full verification session, every claim that survived was **classical**
(results from 1912, 1954, 1974, and standard finite geometry) and every claim that
was **novel** was false — including one asserted identically across five files.

The exception is what makes the programme continue:

> **Obstructions.** A claim that something *cannot* exist can be novel even when
> every ingredient is classical. In this corpus every positive claim proved fragile
> and every obstruction held.

**Honest failure.** A method producing only results is not a method. From one
session, all committed: an identification abandoned when every component turned out
to already exist, one of them in CI; a proposed correspondence killed as a **type
error** (two objects of equal order in different categories); a claim about a CI
workflow retracted after re-reading it; a reserved number released when the other
agent shipped first; and a "20 broken proofs" finding **downgraded** when the errors
turned out to be transient artifacts of concurrent builds rather than mathematics.

That last one is the paper's own cautionary tale: the author's tooling produced a
confident, specific, wrong diagnosis, and only a clean serialized re-run caught it.

## 7. Contributions and limitations

**Contributions.** Rediscovery in a machine-generated corpus is a measurable, trackable
rate. Novelty cannot be self-checked and requires an index kept separately from the
narrative. Guards should warn, not block. Prefer obstructions to facts when mining an
exhausted subject. Reserve identity before working when agents are concurrent.
Reproducibility means byte-identical from tracked source, tested by deletion.

**Limitations.** One repository; the *rate* is not claimed to generalise, only the
method for measuring it. The tokeniser is hand-curated. And the sharpest objection has
no clean answer: **much of this analysis was produced by the same class of system it
evaluates.** Mitigation is that every number is re-runnable by a third party from a
public repository, and the retraction list is included so the failure rate is visible
rather than inferred.

**AI contributions statement.** An AI agent wrote the measurement tooling
(`rediscovery_sweep.py`, `check_rediscovery.py`), ran the computations, and drafted
this document. The author directed the work, set the framing, and is responsible for
all claims. The corpus under study was itself generated by two such agents, which is
the object of study rather than a disclaimer about it.
