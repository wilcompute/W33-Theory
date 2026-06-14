# BT963 — Selector phase-slot scoring

BT963 scores the four final-selector rails as canonical phase slots.

## Rule

```text
phase_score = rail_support_sum + popcount(rail_xor_mask)
```

## Scores

```text
rail 0: support 12, xor 71,  xor weight 4, score 16
rail 1: support 12, xor 46,  xor weight 4, score 16
rail 2: support 14, xor 91,  xor weight 5, score 19
rail 3: support 22, xor 234, xor weight 5, score 27
```

Canonical score order:

```text
[1,0,2,3]
```

## Reading

The final selector removes arbitrary symplectic-basis choice. It leaves a real two-light-rail degeneracy between rails 0 and 1, followed by rail 2 and then the high-support rail 3.

## Boundary

This is a canonical phase-slot gauge artifact, not a new CKM/PMNS prediction.

## Witness

```text
analysis/bt963_selector_phase_slot_scoring.py
data/bt963_selector_phase_slot_scoring.json
```
