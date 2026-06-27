# BT1856-BT1858 summary

Executed the three requested moves after BT1852-BT1855.

## BT1856 — code-distance falsifier

The raw BT1853 optical incidence compiler has:

```text
n = 72
payload = 66
parity = 6
field = GF(3)
rank = 6
dimension = 66
minimum distance = 2
```

Verdict:

```text
BT1853 is a finite syndrome/check compiler.
It is not yet a quantum code-distance theorem.
```

Adding the 44 face rows improves local single-edge detection but still does not prove quantum distance.  A genuine protected memory requires a CSS/subsystem split with logical and gauge operators.

## BT1857 — Holonet paper patch

Added:

```text
papers/BT1857_holonet_k12_compiler_patch.tex
```

Suggested insertion point:

```text
before \section{Discussion and Open Questions}
in papers/BT1347_photonic_holonet_journal.tex
```

The patch adds a claim-stratified K12/F12 compiler section:

```text
exact finite: 66 rotations/edges
exact finite: 44 closed triangular face words
exact check surface: [72,66,6] over GF(3)
falsified stronger claim: raw distance > 2
open: quantum stabilizer/subsystem distance
open: physical chip calibration
```

## BT1858 — UTM tape executable witness

BT1342 already gives the BC clock as an aperiodic two-gap clock.  BT1858 combines it with the six genus-hole parity symbols.

Tape tracks:

```text
track A: BC gap symbol in {S,L}
track B: genus-hole parity symbol in Z/6Z
```

Composite alphabet:

```text
2 * 6 = 12 tape symbols
```

Representative length-30 prefix:

```text
S0 L1 S2 S3 L4 S5 L0 S1 L2 S3 S4 L5 S0 L1 S2 L3 S4 L5 S0 S1 L2 S3 L4 S5 S0 L1 S2 S3 L4 S5
```

Verdict:

```text
BC gaps + six parity holes -> executable symbolic tape stream
```

Boundary: this is a tape-alphabet witness, not a full universal transition-table proof.
