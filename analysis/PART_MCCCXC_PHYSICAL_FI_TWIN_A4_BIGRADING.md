# Physical FI × Twin-A4 Bi-grading Census

## Exact result

Two recent exact flagship-E8 results can be overlaid without adding any physics
assumption:

1. the measured physical FI Cartan projection gives an inner `Z3` action with
   root grades `78 + 81 + 81`; and
2. the physical Wilson-line and organizer `A4` systems form an index-five
   `A4 + A4` sublattice, whose root sectors obey
   `c_gauge = 3 c_center (mod 5)`.

The new verifier exhausts the same 240 roots and records the full joint table.
It has fourteen nonempty cells. Its marginals recover both parent results:

```text
FI grades:          78 + 81 + 81 = 240
A4 gluing sectors:  20 + 20 + 50 + 50 + 50 + 50 = 240.
```

## New firewall

The two structures are **not** the same quotient. Each nontrivial discriminant
class occurs in more than one FI grade. Thus the FI grade is not a function of
the `Z/5` discriminant label. In particular, the orders 3 and 5 are coprime and
there is no nontrivial homomorphism between the two quotient groups.

This matters because a tempting but unjustified identification of an FI
charge modulo five with the E8 gluing class would be false already at the
finite root-set level.

## What is and is not claimed

This is exact finite arithmetic in the recorded flagship E8 coordinate basis.
It does **not** solve D/F flatness, compute string amplitudes, establish a
vacuum, derive observed fermion generations, or identify the physical FI A2
with the independently constructed W33 tetracode-coordinate A2. The latter
requires an explicit model-identification/intertwiner map and remains open.

## Artifacts

- Verifier: `analysis/w33_physical_fi_twin_a4_bigrading_census.py`
- Frozen result: `data/w33_physical_fi_twin_a4_bigrading_census.json`
- Parents: `analysis/w33_physical_fi_e6_a2_z3_grading.py` and
  `analysis/w33_physical_twin_a4_e8_index5_gluing.py`
