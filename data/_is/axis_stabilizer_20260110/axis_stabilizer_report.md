# Exceptional axis stabilizer (computed)

## Definitions used
- The **projective clock points** are `sec_s_m` with sector `s∈{0,1,2,3}` and phase `m∈Z3`.
- The **exceptional (unmatched) tomotope triangle** is the sector-0 triple:
  `{sec0_m0, sec0_m1, sec0_m2}` (coming from points 14-,24-,34-).

- Each **liftable doily symmetry** in the D8 subgroup is given as a Z3-linear map on coefficient space;
  it induces a Z3-linear map `B` on the **evaluation 4-tuple** `(m0,m1,m2,m3)` (sector phases).

A D8 element **stabilizes the exceptional axis** (sector-0 triple) iff its induced map satisfies:
- `m0'` depends only on `m0` (row0 of `B` is `1000`), i.e. the sector-0 coordinate does not mix with other sectors.

## Result 1: stabilizer inside the liftable D8 subgroup
- D8 has 8 elements.
- Exactly **2** elements stabilize the sector-0 axis:
  - `element_id ∈ [0, 1]`

Equivalently: only these 2 D8 lifts preserve the “pure sector-0 phase axis” as an intrinsic object.

## Result 2: interaction with the tomotope 15-subset
- Only **identity** (element_id 0) preserves the **tomotope15** subset of 27 hyperplane phase-functions.
- Therefore, within D8:
  - `Stab_D8(axis)` has size 2
  - `Stab_D8(tomotope15)` has size 1
  - intersection has size 1 (identity only)

So the tomotope selection breaks the liftable doily symmetry almost completely.

## Result 3: stabilizer inside the intrinsic automorphism group of the 12-point / 15-line incidence
- The computed incidence automorphism group has order **12**.
- All 12 automorphisms stabilize the sector-0 triple **setwise**.
- Exactly **6** stabilize it **pointwise** (they fix each of `sec0_m0,sec0_m1,sec0_m2`).

This cleanly separates:
- “tomotope incidence symmetries” (order 12), from
- “liftable doily symmetries” (D8 of order 8),
and shows the exceptional axis is a genuine fixed subconfiguration for the tomotope incidence group.

## Artifacts
- `D8_lift_elements_axis_and_tomotope_stabilizers.csv`
- `axis_stabilizer_summary.json`
