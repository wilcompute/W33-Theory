# BT1857 — Holonet Paper Patch

BT1857 adds a claim-stratified patch section for the Holonet TeX.

## Patch file

```text
papers/BT1857_holonet_k12_compiler_patch.tex
```

Suggested insertion point:

```text
before \section{Discussion and Open Questions}
in papers/BT1347_photonic_holonet_journal.tex
```

## Purpose

The Holonet paper proves or states:

```text
single-photon qutrit carrier
27-dimensional coherent routing
W(3,3) contextual magic supply
Boerdijk-Coxeter aperiodic clock
```

but explicitly leaves open:

```text
qutrit error correction
multi-photon scaling
UTM tape mapping
```

The patch adds a finite compiler layer:

```text
K12/F12 face code
66 edge/rotation payloads
44 triangular face checks
6 genus-hole parity symbols
```

## Claim stratification

The patch distinguishes:

```text
exact finite: 66 rotations/edges
exact finite: 44 closed triangular face words
exact check surface: [72,66,6] over GF(3)
falsified stronger claim: raw distance > 2
open: quantum stabilizer/subsystem distance
open: physical chip calibration
```

## Boundary

This patch is intentionally conservative.  It adds the compiler layer without claiming that the raw incidence code is already a protected quantum memory.
