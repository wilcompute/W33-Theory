# Heawood Clifford Packet Theorem

## Summary

Heawood graph Laplacian (14 nodes from Fano 7-point/7-line) has spectrum:
- 0 (multiplicity 1)
- 3 - √2 (multiplicity 6)
- 3 + √2 (multiplicity 6)

Centering around q = 3 gives operator `C = L_H - 3 I` with mid-shell eigenvalues ±√2 (12 modes). Normalizing by √2,

`H_mid = C_mid / √2`

satisfies `H_mid^2 = I` (on mid-shell). The projector

`P_mid = (I + H_mid) / 2`

is idempotent with trace 6 (rank 6). This realizes a finite `Cl(1,1)` packet turning the 12 real modes into a 6+6 complex packet.

## Equivalent statements

- `x^2 - 6x + 7 = 0` with roots `3 ± √2` determines the Heawood middle shell.
- The Fano and Torus Laplacians obey:
  - Fano selector: `F = 2 I + J`
  - Toroidal selector: `T = 7 I - J`
  - `F + T = 9 I` (natural unit vacuum normalization)

## Data provenance

- `heawood_from_fano_7cycles.py`
- `heawood_fano7_tetra_alignment.py`
- `heawood_projector_clifford.py`
- `tetrahedral_harmonic_crack_summary.py`

## Consequences

1. Heawood dissolves into gauge shell + toroidal/QCD shell at q=3.
2. Nontrivial trace packet 12 + 42 = 54 and 84→168→336 lifts are consistent.
3. The normalized middle shell is the emergent finite Clifford quantum packet (canonical 6D complex).
