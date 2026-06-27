# BT1856 — Code-Distance Falsifier

BT1856 tests the honest coding-theory status of the BT1853 optical incidence compiler.

## Object tested

```text
n = 72 total symbols
payload = 66 edge/rotation symbols
parity = 6 cyclic-distance symbols
field = GF(3)
```

## Six-row parity code

The six cyclic-distance rows are independent, so the raw linear code has:

```text
rank = 6
dimension = 66
minimum distance = 2
```

A single-symbol error is detected, but two nonzero errors in the same parity row can cancel over GF(3).  Therefore the raw `[72,66,6]` incidence compiler is a check code, not a standalone distance-bearing quantum stabilizer code.

## Adding face rows

Adding the 44 face-current rows improves local detection:

```text
single edge error syndrome weight = 3
single parity error syndrome weight = 1
```

but this still does not prove distance greater than 2 because the parity symbols are only tied to the six distance rows unless an additional logical/gauge split is imposed.

## Verdict

```text
BT1853 is a finite syndrome/check compiler.
It is not yet a quantum code distance theorem.
```

The surviving candidate is a subsystem/stabilizer construction that adds face rows, antipodal-sheet rows, and a logical/gauge split.

Boundary: this is a finite GF(3) linear-code falsifier, not a full CSS/subsystem quantum-code proof.
