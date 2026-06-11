# BT756 — Phase-Duo Execution Driver Contract

BT753 introduced the executable local enumerator:

```text
analysis/bt753_phase_duo_candidate_enumerator.py
```

BT754 introduced the pass/fail contract for the 24 candidates

```text
(epsilon, phi, delta) in {0,1} x {0,...,5} x {0,1}.
```

BT756 is the exact run instruction and result schema for the full execution pass.

## Command

Run from the repository root:

```bash
python analysis/bt753_phase_duo_candidate_enumerator.py \
  --out data/bt753_phase_duo_candidate_enumerator.json
```

## Required BT754 checks

For every candidate key `(epsilon, phi, delta)`, the output JSON must satisfy:

```text
selected_rows = 2160
rank_mod_1000003 = 81
root_triples_hit = 540
root_hit_distribution = {"4": 540}
root_uniform_4 = true
```

## Result schema

The full data artifact must be:

```text
data/bt753_phase_duo_candidate_enumerator.json
```

with the top-level fields:

```text
theorem
rectangles_processed
candidate_count
boundary
candidates
```

and each candidate record must contain:

```text
selected_rows
rank_mod_1000003
root_triples_hit
root_hit_distribution
root_uniform_4
```

## Current boundary

I could push the executable enumerator and this execution contract through the connector, but the connector path does not execute repository Python on GitHub. Therefore this note does not claim the full 2160-rectangle run has completed. It pins the command and the exact pass criteria so that the local or CI run has no interpretation ambiguity.

## Next layer

BT757 adds the gluing-register test that BT754 deliberately left separate: selected rows alone certify local rank/root-uniformity; the final root-natural selector must also pass the BT741-style global register test.
