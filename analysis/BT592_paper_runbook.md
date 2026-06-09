# BT592 - Paper Runbook

Purpose: record the current preprint support order.

## Inserts

- BT588: raw cubic leakage ratios insert.
- BT589: Levi versus phase-cover fiber homology insert.

## Geometry chain

- BT545 to BT551: Levi graph, cycle projector, flag association scheme.
- BT571 to BT580: scalar phase cover over the Levi support base.
- BT583 to BT589: separation of Levi homology from scalar-fiber homology.
- BT552 to BT588: cubic transform, repaired map, stability, and leakage-ratio table.

## Build chain

Run in this order:

1. `python tools/integrate_bt588_bt589_inserts.py`
2. `python analysis/bt574_latex_sanity_verifier.py`
3. `python tools/build_w33_preprint.py`
4. `bash tools/check_w33_preprint_static.sh`
5. `python tools/build_w33_preprint.py --compile`

The final compile step depends on local TeX availability.

## Review boundary

The scalar phase cover and the Levi graph have related counts but different homology ranks. The repaired cubic map fixes the protected Gram, while the unrepaired cubic transform has structured companion-sector leakage.
