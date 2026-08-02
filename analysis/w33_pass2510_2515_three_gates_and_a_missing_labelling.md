# Passes 2510–2515 — the frame action is built, the `K₈` run is blocked on a **missing labelling**, and the gate fired three times

---

## Pass 2510 — the 540-frame action, built correctly in GAP

Pass 2503 failed twice trying to do this in Python. Doing it where the group and its
invariant form already agree:

```text
|Sp(4,3)|                 51840
projective points            40
totally isotropic lines      40      (all of size 4)
frames                      540
group order ON FRAMES     25920      = |PSp(4,3)|, the centre acts trivially
transitive on 540            true
frame stabiliser              48      = 25920/540
```

Exported to `data/w33_pass2510_frame_action.json` as two 540-point permutations. Python
reproduces the closure order 25920 exactly. **This object is correct**, and it is the
piece Pass 2503 could not build.

*(Correction to Pass 2455, which said the frame stabiliser has order 96: that is the
`PGSp` figure. `PSp` acts on frames with stabiliser 48, and `PGSp`'s centre-quotient acts
identically, so 25920 is the effective order.)*

---

## Pass 2511 — the `K₈` run, and the third gate

C++ worker (`analysis/cpp/w33_pass2511_link_cliques.cpp`, `g++ -O2`), reading the GAP
permutations and the 327 frozen representatives, with the validation gate kept in place.

```text
group order on frames : 25920          correct
orbit representatives :   327          correct
covers                : 8,475,840      frozen total is 3,547,800   MISMATCH
```

`8,475,840 = 327 × 25920` **exactly** — every representative has a *trivial* stabiliser
under my labelling, with no collisions at all. But the frozen census records stabilisers
of order 2, 4 and 8:

```text
frozen orbit sizes : {12960: 228 orbits, 6480: 84, 3240: 15}   total 3,547,800
```

> **A genuine cover has a stabiliser of order 2, 4 or 8. Trivial stabilisers for all 327
> means the frozen frame *indices* do not denote the same frames in my GAP-derived
> labelling.** Under a wrong relabelling their representatives are arbitrary 60-subsets,
> which have no stabiliser and full orbits — exactly what was measured.

**The run printed link sizes 4848 / 5019 / 4561 with clique numbers 2 / 2 / 3. Those are
computed on mislabelled data and are DISCARDED.** They are recorded here only so that the
numbers are never mistaken for results if they surface in a log.

### What is actually blocking

`data/w33_pass1511_cover_orbit_representatives.json.gz.b64` stores **index lists only**.
It does not store the frame ordering that gives those indices meaning — the ordering is
implicit in whatever construction `w33_pass1505/1511` used. **The labelling cannot be
recovered from the frozen file**, so the `K₈` computation cannot be run against it
without either:

- the producing script's frame construction (to reproduce the ordering), or
- a labelling-independent invariant to match on — e.g. re-deriving each representative's
  stabiliser order and matching the multiset `{12960: 228, 6480: 84, 3240: 15}`, then
  searching for the relabelling that realises it.

The second is a graph-isomorphism-style search and is the honest next step.

---

## Pass 2512 — three gates, and why they are the point

| gate | what it caught |
|---|---|
| Pass 2503 #1 | hand-written generators gave group order **192**, not 25920 |
| Pass 2503 #2 | GAP's `SP(4,3)` preserves a **different form** than my convention |
| Pass 2511 #3 | frame **labelling** mismatch, exposed by trivial stabilisers |

Three separate wrong answers, none published. Without the frozen `3,547,800` and `13,648`
to check against, run #1 would have reported a link size of 53 and run #3 a clique number
of 2 — both confident, both meaningless, and neither obviously wrong on its face.

> **The lesson is not "be careful". It is that this computation is only trustworthy when
> it reproduces a number somebody else froze first.** Every stage of it looked correct
> until compared.

This is the same rule as *a disagreement with the corpus is a bug in the new code* —
sixth occurrence — but in its constructive form: **build the check before building the
result.**

---

## Pass 2513 — a concrete request to the parallel track

The single missing item is small and you already have it:

> **Publish the frame ordering** — the 540 frames as explicit pairs of line indices, plus
> the line ordering as explicit 4-sets of point indices, in whatever convention
> `w33_pass1505/1511` uses.

That is ~540 short pairs. With it, the `K₈` computation runs in seconds on the C++ worker
already committed here, over all 327 orbits, and either exhibits a `K₈` or refutes
`χ(H) = 9` on the frozen frontier.

Everything else is built: the GAP frame action, the closure, the cover regeneration, the
link construction, and the bounded clique search with an early exit at 8.

---

## Pass 2514 — the other items, honestly

- **Frontier completeness** (Pass 2505) — untouched. Still the load-bearing question, and
  still the thing that would make a `K₈`-free verdict mean anything.
- **Is the missing zero mode the chirality?** Not tested. Pass 2502 showed the chiral half
  is the pentagon's augmentation ideal (no trivial character); Pass 2437 showed the
  point-side fibre quotient is `C₃`. Whether those are the same absence is a well-posed
  question and was not reached.
- **The other seven pentagons** — not tested. All eight are permuted transitively by an
  order-5 element's normaliser, so the *individual* restrictions are forced to agree;
  whether the eight are *simultaneously* compatible is the real question and is untouched.
- **The certificate value index** — still proposed, not built.

---

## Pass 2515 — ledger

| claim | discharged by | status |
|---|---|---|
| 540-frame action, order 25920, transitive | GAP + Python closure | **built and correct** |
| frame stabiliser is 48 under `PSp` | `25920/540` | corrects Pass 2455's 96 |
| C++ `K₈` worker compiles and runs | `g++ -O2` | built |
| any link size or clique number | — | **DISCARDED; mislabelled** |
| frozen reps carry no frame ordering | inspection of the b64 file | established |
| frontier completeness | — | open, load-bearing |
| zero mode = chirality | — | not tested |
| eight pentagons simultaneously | — | not tested |
| certificate value index | — | not built |

---

## Prior art

- `pass1505`/`pass1511`/`pass1533` — own the covers, representatives and frontier numbers.
- Pass 2496 (mine) — the `K₈` reduction this tried to execute.
- Pass 2510 (mine) — the frame action, which is new and correct.

## Still open

- The frame labelling. **One small publication unblocks the whole computation.**
- Frontier completeness.
- Whether the pentagon zero mode and the `C₃` orientation are the same absence.
