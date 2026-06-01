# Part MMCCCLXXIII: Golden Ordered D4 Torsor

## Claim

The full `864` ordered golden-selector failures are:

```text
K2,2_edges x B27 x D4_orientations
  = 4 * 27 * 8
  = 864.
```

This refines the previous support-level product:

```text
K2,2_edges x B27 = 4 * 27 = 108.
```

## D4 Orientation Torsor

For each active pair and bridge line, the forced quadrangle has canonical
cyclic role order:

```text
(anchor, endpoint_left, bridge, endpoint_right).
```

The eight ordered cycles over this support are exactly:

- the four rotations of that cycle;
- the four rotations of its reverse.

That is the dihedral orientation torsor of the square.

## Profiles

- `108` unique supports.
- `8` ordered cycles per support.
- Each of the `8` orientation labels occurs `108` times.
- Each active K2,2 pair has `27*8 = 216` ordered cycles.
- Each bridge line has `4*8 = 32` ordered cycles.

## Boundary

This proves the ordered carrier inside the draft golden selector. It still does
not identify these ordered product coordinates with signed `AGL(2,3)` candidates
or `O^-(6,2)/A5` cosets.

## Verification

Run:

```bash
python3 analysis/w33_golden_ordered_d4_torsor.py
```

Expected result: `12/12` checks verified.
