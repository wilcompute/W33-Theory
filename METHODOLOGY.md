# Epistemics for adversarial AI-assisted mathematics

*What this repository learned about keeping a machine-generated corpus honest, stated
as a method rather than as a result. Every number below is measured in this repo and
reproducible from it. The mathematics is the case study; the method is the claim.*

---

## The setting

Two AI agents work this repository in parallel. Neither reads the other's filenames.
Both can run code, commit, and push. Neither remembers the previous session. Over
~10,700 commits they have produced ~19,800 tracked files, ~2,900 JSON certificates,
~3,000 tests, and ~1,030 numbered "passes."

That is an unusual laboratory: high output, no shared memory, no human in the
inner loop, and a subject matter — the E₈ root system and the generalized
quadrangle W(3,3) — that has been studied for over a century. It turns out to
break in specific, measurable, repeatable ways.

## The central measurement

**22.9% of the corpus asserts a result that already exists elsewhere, uncited.**

```text
scripts/rediscovery_sweep.py     scanned                  5708
                                 with uncited collisions  1308   (22.9%)
                                 merge-list rows           859
```

Pass 328 first measured this by hand over 173 pass files and got 21%. The automated
sweep reproduces it at 33× the sample size. **This is not two agents forgetting to
search. It is a stable property of the corpus**, and no amount of "search harder" has
moved it — that instruction was already standing, and failed twice at a cost of ~19
passes.

The single largest duplication cluster: the CSS code `[[240,81,3]]`, asserted in **52
files that cite none of the others**.

## Why the obvious fix does not work

The corpus is indexed by *when* someone worked, not by *what* they found. Files are
named `2026-07-10_levi_next5.md`, `PASS178_...`, `BT1654_...`. A file named for a date
carries no topic signal, so **a search for a topic cannot find it**.

The operational consequence, learned the expensive way:

> **Search for the RESULT, not the topic.** Grep the formula `(q^2+1)(q+2)`, the
> integer `51840`, the sequence `25/91/225`. Those hit on day one. The word `rank`
> does not.

## The five failure modes

Ordered by how hard they are to catch. Each was found the expensive way, and each has
a distinct signature.

| # | Mode | Signature | Fix |
|---|---|---|---|
| 1 | **Coordinate artefact** | a metric/basis claim refuted by a second drawing | check another realization before publishing anything metric |
| 2 | **Over-read** | the result is right, the framing exceeds the proof | state the scope the witness establishes, not its implication |
| 3 | **Unbuilt object** | a claim naming no map ("a coupled module") — cannot be refuted *or* used | name the map, or state the open question |
| 4 | **Unbuilt half** | a sound file with one ungrounded sentence (a dimensionless eigenvalue asserted to be a mass) | read, don't grep — a file-level audit passes it |
| 5 | **Rediscovery** | nothing internal to the pass is wrong; only its novelty is false | **cannot be self-checked** — see below |

Mode 5 is the expensive one and the reason for everything else here:

> **Novelty is not a property of the claim. It is a property of the corpus.**
> A pass can be internally flawless — correct maths, passing witness, proportionate
> framing, named object — and still be worthless. Nothing inside it can detect this.

## The measured law

Across a full session of verification, the pattern was uniform enough to state:

> **In a corpus mining a well-studied object, verifiability and novelty are
> anti-correlated.** Claims sort into *true-and-classical* and *novel-and-false*. The
> intersection is close to empty.

Survived verification, all classical: Springer's regular elements (1974),
Shephard–Todd G₃₂ (1954), the Witting polytope (1912), Seidel's regular two-graphs,
Thas' ovoid theorem, the Eisenstein structure of E₈.

Failed verification, all novel: `Sp(4,3) ≅ W(E6)` (in five files), "no proper subgroup
of W(E₈) is transitive on 240 roots", "W(E6) has 15 orbits" (it has 13), an equivariant
edge–root bijection, a mislabeled E₈ action, `[[137,1,3]]`, a Φ₄(3) identification.

The reason is structural. The prior probability that a *new true structural fact* about
E₈ is reachable by matching integers is essentially zero, while the space of *false*
patterns is enormous and a machine generates them quickly.

**The corollary is the useful part.** Obstructions are the exception: a claim that
something *cannot* exist can be novel even when every ingredient is classical. In this
corpus every positive claim has been fragile and every obstruction has held. Physics is
mostly selection rules; a substrate should forbid, not produce.

## The controls that actually work

Each exists because a specific failure made it necessary.

**1. Search the corpus by result, before computing.** Not after.

**2. Reserve the pass number before computing, not after.** Push an empty commit
`Pass NNN reserved: <topic> (<track>)` as the *first* action. Cost: one commit. Cost of
not doing it: a renumber, a rebase race, and (measured once) a silently wrong ledger
row. Three renumbers in one day preceded this rule.

**3. A guard that warns and never blocks.** `scripts/check_rediscovery.py` runs at
commit time and prints the prior art. It is deliberately advisory — *blocking trains
`--no-verify`, which is worse than no hook*. Calibrated to code parameters only: bare
integers flagged 97% of files and were pure noise. It was also extended to named
objects after a rediscovery whose result was `A2 = the q=3 hexagonal lattice`, from
which a numbers-only tokeniser extracts nothing.

**4. Idempotent certificates.** Every claim emits JSON; rerunning must reproduce it
byte-for-byte. This catches more than flakiness — it caught a certificate carrying two
hand-edits its own script never emitted, inside a CI job configured to *fail closed on
stale certificates*.

**5. Cross-track citation and ownership.** When both agents hold a result, **the
earlier commit owns it and the later one cites it**, checked with
`git log --diff-filter=A`, not memory. When a guard flags your file against theirs,
read theirs.

**6. Read, don't grep-and-discard.** Two conclusions were retracted after shallow
searches. A negative search must state *which space* it covered.

## What honest failure looks like

The method is only worth anything if it produces retractions at the same rate as
results. From a single session, all committed:

- A proposed identification of a section obstruction with the Kochen–Specker
  obstruction — **abandoned**, every component already in the repo, one of them in CI.
- A proposed identification of a ℤ₆ fibre with the Standard Model's ℤ₆ quotient —
  **killed as a type error**: one lives in a Weyl group, the other in a Lie group
  centre. Same order, different category; the same mistake as `Sp(4,3) ≅ W(E6)`.
- A claim that a CI workflow swallowed Lean failures — **retracted after re-reading
  it**; the workflow enforces correctly. The real defect was different and worse: two
  other workflows pointed at a directory that does not exist.
- A pass number reserved and then **released** because the other track shipped it first.

> **Write the retraction into the artifact, not just the conversation.** A caveat that
> lives only in a chat log is not a caveat. Pass 1019's certificate carried
> "whether they already contain it is NOT established here" for a week before anyone
> resolved it by actually reading the three files.

## Green over red

Two independent instances in one session of a check that reported success while
verifying nothing:

- `lake build` in `formal/` fails — 20 of 39 imported modules have real compile errors
  — while two of the three Lean workflows ran `working-directory: proofs/lean`, **a
  directory that does not exist**, degrading to no-ops by design (`|| true`,
  `|| echo "...continuing"`, an explicit "skipping Lean build" branch).
- Four `.lean` files were never imported by the library root at all, so `lake build`
  had never type-checked them. One of them does not compile.

> **A workflow that cannot fail is worse than no workflow, because it looks like one.**
> Before trusting any verification badge, verify the verifier: delete its input and
> confirm it goes red.

## The transferable claims

1. Duplication in a machine-generated corpus is a **measurable rate**, not an anecdote;
   measure it continuously and rank the merge list.
2. **Novelty cannot be self-checked.** It requires an index of results, kept separately
   from the narrative, and consulted before work starts.
3. Guards should **warn, not block**; a blocked agent routes around the guard.
4. Prefer **obstructions to facts** when mining a well-studied object — it is the one
   category where a machine can still be both correct and novel.
5. **Reserve identity before doing work** when agents are concurrent.
6. Reproducibility means **byte-identical from the tracked source**, and must be tested
   by deletion, not by inspection.

---

*Artifacts: `scripts/check_rediscovery.py` (per-commit guard), `scripts/rediscovery_sweep.py`
(corpus-wide merge list), `RESULTS_INDEX.md` (inverted index, result → file),
`scripts/audit_batch.py` (intake harness), `CLAUDE.md` (the standing protocol).*
