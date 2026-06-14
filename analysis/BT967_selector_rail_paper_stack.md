# BT967 — Selector rail theorem paper stack

BT967 writes the BT962--BT966 selector rail results into the corrected paper stack.

## Heavy-math target

```text
paper/BT967_selector_rail_theorem_insert.tex
tools/integrate_bt967_selector_rails_w33.py
```

## Holonet target

```text
paper/BT967_holonet_selector_rail_pointer.tex
tools/integrate_bt967_holonet_selector_rails.py
```

## Payload

The insert records the final selector, rail support sums, phase scores, the selector-fixed 27+27+27 rail faces, and the prefix-to-rail ABI table.

## Boundary

BT965 showed that dynamic lane preservation is still pending executable lane-action maps. BT967 therefore writes the rail theorem and ABI table, not a dynamic preservation theorem.
