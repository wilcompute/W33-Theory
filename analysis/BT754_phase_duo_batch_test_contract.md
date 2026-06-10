# BT754 — Phase-Duo Batch-Test Contract

BT753 adds the executable enumerator for all local phase-duo selector candidates:

```text
analysis/bt753_phase_duo_candidate_enumerator.py
```

The candidate space is

```text
chirality epsilon in {0,1},
phase phi in {0,...,5},
duo delta in {0,1},
```

so there are

```text
2 x 6 x 2 = 24
```

candidate selectors.

## Why phase-only died

BT750 proved that a reflection/phase fixes two lifts related by the central half-turn `r^6`.  Those two lifts are different Levi octagons.  Therefore:

```text
constant phase  ->  two apartments per rectangle
constant phase + constant duo -> one apartment per rectangle.
```

So BT754 tests phase+duo selectors, not phase-only selectors.

## Full-run pass conditions

For each candidate `(epsilon, phi, delta)`, the next full run must check:

1. `selected_rows = 2160`.
2. `rank_mod_1000003 = 81`.
3. `root_triples_hit = 540`.
4. `root_hit_distribution = {4: 540}`.
5. BT741-style gluing quotient is connected and leaves global dimension `4` over `F2`.

The first four are implemented by BT753.  The fifth is intentionally left as the next heavy verifier because it requires reusing the BT741 local-register gluing relation, not just the selector rows.

## Boundary

BT754 is a contract/result schema.  It does not claim a candidate has passed before the full local-coordinate enumeration and gluing pass are run.  This is deliberate: the previous BT718 sheet was rank-complete but root-nonuniform, so the next canonical selector must be certified against all criteria at once.

The compact JSON contract is:

```text
data/bt754_phase_duo_batch_contract.json
```
