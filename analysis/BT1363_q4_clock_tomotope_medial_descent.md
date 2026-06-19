# BT1363 -- Q4 Clock Descent to the Tomotope Medial Layer

## Summary

BT1362 proved that the local Q4 `[[32,4,4]]` gauge quotient can preserve the
clock stabilizer

```text
C2^4 : C4
```

of order `64`.  The antipodal translation `1111` is one of those `C2^4`
translations.  Since MCLXXXII already proves

```text
Q4 face-edge incidence / <1111> = Reye = tomotope edge-triangle medial layer,
```

the BT1362 clock descends to the tomotope middle layer.

The descended group is:

```text
(C2^4 / <1111>) : C4 = C2^3 : C4
order = 64 / 2 = 32.
```

## The Main Lock

The tomotope/Reye middle layer has

```text
12 tomotope edge labels
16 tomotope face labels
48 edge-face middle blocks.
```

BT1363 verifies two simultaneous readings of the same 48 blocks:

```text
pure C4 clock:          48 = 12 * 4
full descended clock:   48 = 3 * 16
```

So the local Q4 clock is not just binary.  The pure cyclic axis clock gives
twelve four-tick cycles, while the translation quotient fuses those cycles into
three ternary sheets, each containing all sixteen tomotope face labels exactly
once.

## Orbit Data

Under the descended `C2^3:C4` action:

```text
tomotope edge labels:   4 + 8
tomotope face labels:   16
middle blocks:          16 + 16 + 16
```

Each 16-block sheet projects to all 16 tomotope face labels with multiplicity
one.  Its edge-label projection is either `8` labels twice each or `4` labels
four times each.  Thus the ternary sheet structure is visible directly in the
incidence geometry.

Under the pure `C4` coordinate clock:

```text
tomotope edge labels:   2 + 2 + 4 + 4
tomotope face labels:   4 + 4 + 4 + 4
middle blocks:          12 cycles of length 4
```

## Architecture Reading

This is the first objectwise lift of BT1362 out of the local gauge quotient.
The 4-by-4 toroidal-square Q4 router descends to the tomotope packet ABI as a
binary/ternary interface:

```text
C4 axis clock      -> four-tick local packet cycles
C2^3 translations  -> sheet fusion
3 sheets           -> ternary/qutrit tomotope bus
16 face labels     -> full local packet face register
```

That is the concrete mechanism behind the slogan that the binary hypercube
router feeds a ternary substrate computer.  The binary Q4 clock does not replace
the qutrit layer; it descends into exactly three tomotope sheets.

## Boundary

This proves the clock action on the tomotope/Reye middle layer.  It does not yet
identify the full Q6 flag bus or the global `2160` D12 atlas with this clock.
Those remain the next objectwise lifts.

## Verification

```bash
python3 analysis/bt1363_q4_clock_tomotope_medial_descent.py
python3 tests/test_bt1363_q4_clock_tomotope_medial_descent.py
python3 -m py_compile analysis/bt1363_q4_clock_tomotope_medial_descent.py tests/test_bt1363_q4_clock_tomotope_medial_descent.py
python3 -m json.tool data/bt1363_q4_clock_tomotope_medial_descent.json
```
