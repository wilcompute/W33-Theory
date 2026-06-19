# BT1362 -- Symmetric Q4 Gauge Quotient

## Summary

BT1341 proved that the Q4 edge carrier admits a gauge quotient with code
parameters `[[32,4,4]]`.  BT1344 then found the honesty boundary: the particular
BT1341 quotient is valid, but it is generic under the full Q4 automorphism group
and has stabilizer `1`.

BT1362 closes the next layer.  A second quotient proves the same code parameters
while preserving a visible affine cyclic symmetry:

```text
Stab(Q_sym) = C2^4 : C4
|Stab(Q_sym)| = 16 * 4 = 64
|Aut(Q4)| / |Stab(Q_sym)| = 384 / 64 = 6
```

The six residual choices are the six cyclic orderings of the four hypercube axes.
This turns the local Q4 router from a generic quotient certificate into a
clocked quotient certificate.

## Verified Code

The symmetric quotient functionals on the 17-dimensional Q4 cycle space are:

```text
0x024a, 0x4805, 0xbdbe, 0x11d31
```

The verifier recomputes the entire BT1341 code certificate:

- Q4 edge count: `n=32`.
- vertex/star X-check rank: `15`.
- quotient-kernel Z-check rank: `13`.
- logical dimension: `32 - 15 - 13 = 4`.
- X distance: `4`.
- Z distance: `4`.
- all X/Z checks commute.
- the quotient avoids every weight `<4` dual obstruction.

So the code is again `[[32,4,4]]`.

## Symmetry Upgrade

Under the active action of the full Q4 automorphism group

```text
Aut(Q4) = C2^4 : S4,  |Aut(Q4)| = 384,
```

the original BT1341 quotient has orbit size `384` and stabilizer size `1`.
The BT1362 quotient has:

```text
orbit size = 6
stabilizer size = 64
orbit * stabilizer = 384
```

The stabilizer is exactly:

```text
all 16 translations of Q4
times
the cyclic coordinate group <(0 1 2 3)> of order 4.
```

Equivalently, the quotient preserves the bit-flip fabric of the 4-cube and fixes
a cyclic axis clock.

## Architecture Reading

This is the missing local-router refinement behind the toroidal hypercube
language.  The Q4 packet router does not have to be an arbitrary
`[[32,4,4]]` gauge quotient.  It can be gauge-fixed to an oriented four-axis
cycle:

```text
Q4 translations        -> address offsets
C4 coordinate cycle    -> packet clock
six quotient choices   -> six cyclic axis orderings
```

That is exactly the local form expected from the 4-by-4 toroidal square clue:
the toroidal boundary makes the 16-square board into Q4, and BT1362 supplies the
cyclic axis gauge needed to use that Q4 as a clocked router rather than just a
counting skeleton.

## Boundary

This is still a finite binary Q4 gauge-quotient theorem.  It does not yet prove
the objectwise intertwiner from this `C2^4:C4` quotient to the W33 incidence
action, the tomotope cover family, or the full Clifford algebra.  The next
target is to lift the cyclic Q4-axis clock into the Q6/tomotope flag bus and the
`2160` D12 mirror G-set.

## Verification

```bash
python3 analysis/bt1362_symmetric_q4_gauge_quotient.py
python3 tests/test_bt1362_symmetric_q4_gauge_quotient.py
python3 -m py_compile analysis/bt1362_symmetric_q4_gauge_quotient.py tests/test_bt1362_symmetric_q4_gauge_quotient.py
python3 -m json.tool data/bt1362_symmetric_q4_gauge_quotient.json
```
