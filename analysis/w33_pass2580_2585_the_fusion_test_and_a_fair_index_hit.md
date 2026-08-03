# Passes 2580–2585 — a correct fusion test, an inadequate search, and the index earns its keep

---

## Pass 2580 — the fusion test, done correctly and made fast

Pass 2575 withdrew a fusion search that used pairwise commutativity, which does **not**
imply a closed algebra. The correct test is on **intersection numbers**.

Precomputing `p[i][j][k]` once from the 22 orbital matrices (3.3 s), a partition is a
fusion iff for all classes `I, J, K` the sum `Σ_{i∈I, j∈J} p[i][j][k]` is constant over
`k ∈ K`, and commutative iff that sum is symmetric in `I, J`. Every subsequent test is
pure integer arithmetic on a `22³` array — instant.

Sanity gate: `{I, J−I}` returns `fusion=True, commutative=True`, as a rank-2 scheme must.

A byproduct worth recording:

> **The 18 transpose-closed classes are NOT a coherent configuration** (`fusion=False`).
> Merging each orbital with its transpose does not preserve coherence — the rank-22
> configuration is coherent, its symmetrisation is not.

---

## Pass 2581 — the rank 10–14 search: **inadequate, not negative**

30,000 random merge sequences from the 18 transpose-classes, each merging until the
partition passes both tests:

```text
commutative fusion ranks found : [3, 4]
   rank 4 : 2 valency profiles
   rank 3 : 3 valency profiles
rank 9 found ?      False
ranks 10-14 found ? []
```

> **The search never reached rank 9 either — the one rank we know exists.** So this is
> evidence about the *method*, not about the ranks. Random greedy merging collapses far
> past any fine fusion; the window 10–14 remains **unsearched**.

The parallel track's approach is the right one and I should have used it: start from a
single symmetric relation as a **seed** and take its coherent closure, rather than merging
blindly. Their 65,535 binary seeds are exactly that. The correction to make is to seed
from **non-binary** starting partitions, since binary seeds are what they already
exhausted, and the ceiling `Σ m = 14` (Pass 2569) still bounds the answer.

**Consequence:** the idempotent-level assignment is also not closed, since it needs a
real fusion in hand.

---

## Pass 2582 — the five flagged certificates: integer keys explain **four of five**

```text
w33_pass1872_1876_five_frontiers          integer-like keys 53   floats 0
w33_pass1891_tutte_coxeter_voltage_lift   integer-like keys 87   floats 0
w33_pass2011_2015_five_frontiers          integer-like keys  5   floats 0
w33_pass2012_d8_orbit_parallel_witness    integer-like keys  4   floats 0
w33_pass1887_exact_global_weight5_decoder integer-like keys  0   floats 0
```

Pass 2493 withdrew the single-cause theory on the strength of `1887` alone. That
withdrawal was **over-corrected**: the integer-key defect (Pass 2482) is present in
**four of the five**, and `1887` is the lone outlier.

The honest statement, replacing both earlier ones:

> **The integer-key round-trip defect is the necessary condition in four of the five
> flagged certificates. `1887` has none and is stale in the ordinary sense.** Reversing
> the round-trip did not reproduce their digests either (Pass 2517), so integer keys are
> necessary but not sufficient — those four need their producers inspected, not just the
> key types counted.

Still **not repaired**. They now surface on every push via the Pass 2577 CI job.

---

## Pass 2583 — the index, fairly tested, finds something

Pass 2570 validated the value index on the seven answers already known to be hiding —
which is circular. A fair test asks it about numbers I have *not* searched:

```text
1152          -> bt1493_row_action_physical_pulse_compiler.json/...   (unrelated)
576           -> bt1001_full_heat_supertrace_estimator_stack.json/... (unrelated)
13333289472   -> w33_pass2471_radius4_signature_trade_obstruction.json/...
                     exact_fiber_reconstruction/cover_pair_candidates_tested
42912         -> w33_pass1843_second_orbit_no_lift.json/candidate_total
```

The last one is a genuine hit.

> **`42,912` is the parallel track's Pass 2432 nine-signature fibre total. The index
> shows the same number sitting in `w33_pass1843_second_orbit_no_lift.json` as
> `candidate_total` — a pass about a *second orbit failing to lift*, from long before
> the signature work.**

Neither track cited the other. Whether it is one object or a count match needs the
Pass 1843 construction read — but **that is exactly the question the index exists to
surface, and no topic search would have raised it**, since neither file mentions the
other's vocabulary.

Flagged for the parallel track: their radius-4 and radius-5 signature obstructions may
already have a precursor in Pass 1843.

*(`1152` and `576` — their block-stabiliser orders — land in unrelated files. Count
matches, rejected.)*

---

## Pass 2584 — `χ(H)`

Unchanged at `10 ≤ χ(H) ≤ 11`, both bounds theirs. Nothing this batch bears on it.

---

## Pass 2585 — ledger

| claim | discharged by | status |
|---|---|---|
| intersection-number fusion test | rank-2 sanity gate passes | correct, fast, reusable |
| the 18 transpose-classes are coherent | `fusion=False` | **refuted** |
| ranks 10–14 are empty | — | **not shown; search inadequate** |
| integer keys explain the flagged certificates | 4 of 5 have them | **Pass 2493's withdrawal over-corrected** |
| `42,912` appears in Pass 1843 | index lookup | **new cross-reference** |
| idempotent assignment | — | still open |

---

## Prior art

- Pass 2433 (parallel track) — the binary-seed fusion classification whose method I
  should have copied.
- Pass 2432 / 2471 (parallel track) — the signature fibre totals.
- Pass 1843 — `second_orbit_no_lift`, surfaced here by the index.
- Passes 2482 / 2493 / 2575 (mine) — corrected here.

## Still open

- Ranks 10–14, by seeded coherent closure rather than random merging.
- The idempotent assignment.
- Whether `42,912` in Pass 1843 is the same object.
- Four certificates needing their producers inspected; `1887` needing re-derivation.
