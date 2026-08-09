# Part DCMII: Projective Screen / Affine Bulk / QEC Tail Typing Bridge

**Status:** verified finite typing bridge.

## Claim

The new trans-logical `PG(2,3)` language becomes exact when it is typed as a
screen, not as the whole substrate.

There are three related but distinct objects:

```text
PG(2,3) projective screen:
  13 points, 13 lines, 52 incidences
  complete point graph K13 has 78 edges and degree 12

W(3,3) closed screen at anchor x:
  x_perp = {x} union N(x)
  13 points = 1 center + 12 local channels
  induced W33 edges = 24
  screen operator S = A + I

W(3,3) ambient substrate:
  40 vertices, degree 12, 240 edges
```

The shared degree `12` is real.  The objects are still not identical.

## The Exact Split

Every W33 anchor splits the 40-point carrier as

```text
40 = 1 + 12 + 27
```

where:

- `1` is the chosen anchor,
- `12` is the local screen rim / photonic channel alphabet,
- `27` is the non-neighbor or affine bulk by count.

Equivalently,

```text
PG(3,3) = PG(2,3) screen + AG(3,3) affine bulk
40      = 13               + 27
```

This is the exact rescue of the "void geometry" intuition: `PG(2,3)` is the
projective screen, while `W(3,3)` is the crystallized 40-point carrier whose
screen operator is already `A + I`.

## QEC Tail

The bulk is not inert:

```text
27 affine bulk points * q=3 = 81 = H1 logical matter
2 * 81 = 162 = nilpotent QEC-tail lift
40 * 12 = 480 = directed photonic carrier
```

The point stabilizer is also the existing local routing scale:

```text
|Aut(W33)| / 40 = 51840 / 40 = 1296 = Q4 packet length
240 * Phi6^3 = 82320 = protected Steane/Phi6 lift
```

So the typed descent is:

```text
projective screen -> W33 anchor screen -> affine bulk -> H1=81 QEC memory
```

## Meaning

This moves the theory forward by converting the deepest language into a typed
interface:

- `PG(2,3)` supplies the screen cardinality and projective `3/13` share.
- `W(3,3)` supplies the actual substrate, adjacency algebra, and carrier.
- the `27` bulk supplies the ternary matter/QEC sector.
- the `12` rim supplies the local photonic/QEC channel alphabet.

Artifacts:

- Verifier: `verify_dcmii_projective_screen_bulk_qec_bridge.py`
- Data: `data/dcmii_projective_screen_bulk_qec_bridge.json`
- Result: `PART_DCMII_projective_screen_bulk_qec_bridge_results.json`
- Tests: `tests/test_dcmii_projective_screen_bulk_qec_bridge.py`
