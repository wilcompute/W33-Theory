# Passes 1300–1304 — Exact Triality, Matrix-Unit, and Cycle Release

Status: **machine-checkable exact release**

This packet closes the five frontiers opened after Passes 1193–1197 while preserving all parallel commits through Pass 1277.

## Pass 1300 — 81-sector sign-twist bridge

The exact Hashimoto projectors onto eigenvalues `+1` and `-1`, folded to the 160 Levi flags and projected by the rank-81 Hodge projector `E4`, both have rank 81. Their target scalars are

\[
E_4TP_+T^TE_4=2E_4,\qquad E_4TP_-T^TE_4=E_4.
\]

The character-table verdict is

\[
81_-=81_+\otimes\mathrm{sgn}.
\]

Thus the two Weyl extensions are inequivalent over `W(E6)` but restrict to the same irreducible `PSp(4,3)` module.

## Pass 1301 — Carrier-level matrix units

The outer `2C` class sum on each 432 carrier gives an integer rank-81 numerator `N` satisfying

\[
N^2=716800N.
\]

Together with the central `A2` Coxeter transport, the nine operators

\[
E_{ij}=716800^{-1}\tau_{j\to i}N_j
\]

satisfy the full `M3` matrix-unit law. The cubic-incidence map identifies the unique size-240 species-20 copy as the image copy; deleting it leaves 21 geometrically anchored kernel copies and an explicit `M21` multiplicity algebra with 441 hashed sparse units.

## Pass 1302 — Exact Hecke equality

For

\[
G=W(E_6),\;N=PSp(4,3),\;H=S_5,\;K=A_5,
\]

the actions `G/H` and `N/K` have exactly the same 26 orbitals, the same subdegrees, relation matrices, and structure constants. Their common Hecke algebra is noncommutative; one witness is `p[1,2,3]=0` but `p[2,1,3]=1`.

## Pass 1303 — Literal cycle orbits through length eight

The rooted-edge algorithm classifies every primitive oriented rotation class without enumerating all starting points.

- Length 7: `2,739,840` cycles; `108` projective orbits and `57` Weyl orbits.
- Length 8: `26,750,160` cycles; `1,066` projective orbits and `565` Weyl orbits.

The compact certificate stores orbit-size and stabilizer distributions plus a SHA-256 of the deterministic full representative/fusion stream.

## Pass 1304 — Normalizer triality correction

The central `W(A2) ≅ S3` commutes with `W(E6)`. The product subgroup has order `311040`; the full `A2`-subsystem normalizer has order `622080` and index `1120` in `W(E8)`.

The three 432 carriers are `S3/S2`, not a free `S3` torsor. Their orientation-preserving `C3` subgroup acts freely and transitively. The six signed 27-carriers form the genuine regular `S3` torsor.

## Verification

```bash
PYTHONPATH=analysis python analysis/w33_pass1300_81_sign_twist_intertwiner.py
PYTHONPATH=analysis python analysis/w33_pass1301_m3_m21_matrix_units.py
PYTHONPATH=analysis python analysis/w33_pass1302_a5_s5_hecke_equality.py
PYTHONPATH=analysis python analysis/w33_pass1303_literal_cycle_orbits_7_8.py
PYTHONPATH=analysis python analysis/w33_pass1304_a2_normalizer_triality.py
pytest -q tests/test_w33_pass1300_1304.py
```

Scope: exact finite-group, finite-geometry, and integer/rational representation calculations. No experimental or continuum claim follows solely from these identities.
