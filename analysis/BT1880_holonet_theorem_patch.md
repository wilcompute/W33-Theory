# BT1880 — Holonet Finite CSS Theorem Patch

BT1880 adds a paper-ready theorem patch for the Holonet paper.

## Patch file

```text
papers/BT1880_holonet_finite_css_theorem_patch.tex
```

Suggested insertion:

```text
after papers/BT1857_holonet_k12_compiler_patch.tex
```

## Theorem content

The patch states the exact finite CSS code:

```text
physical qutrits = 66 K12/F12 edge payloads
X checks = 44 oriented triangular face rows
Z checks = 12 signed vertex-star rows
rank(HX) = 42
rank(HZ) = 11
HX HZ^T = 0
[[66,13,3]]_3
```

## Corollary

It also states the gauge-refined subsystem model:

```text
[[66,8,3;5]]_3
```

with the six-distance/hole layer interpreted as gauge/clock phase rather than stabilizer protection itself.

## Schedule and decoder boundaries

The patch records:

```text
five-round optical syndrome schedule
264 edge/check touches per cycle
528 unique single-error Pauli syndromes
weight-two correction not claimed
hardware threshold open
```

## Boundary

This is a theorem patch for exact finite matrix-code claims and compiler-level scheduling.  It does not claim a calibrated photonic threshold, decoder threshold, or physical hardware implementation.
