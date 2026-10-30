# Passes 1330--1334 exact release

This release turns the literal \(26\)-dimensional Hecke multiplication tensor
into a prime-by-prime modular atlas, completes the nine-axis triality scheme,
types two selected cyclic words without pretending to classify all cycles,
and replaces the old species-\(20\) scaffold with an executed AtlasRep witness.

## Pass 1330 — exact modular algebra

Let
\[
H_{26}=\operatorname{End}_{W(E_6)}\bigl(\mathbb Q[W(E_6)/S_5]\bigr)
\]
in the frozen orbital basis. Direct finite-field algebra gives:

| \(p\) | \(\dim J,\dim J^2,\ldots,0\) | \(H_{26,\mathbb F_p}/J\) | central-block dimensions |
|---|---|---|---|
| \(2\) | \(21,17,13,7,2,0\) | \(M_2(\mathbb F_2)\oplus\mathbb F_2\) | \(4,22\) |
| \(3\) | \(22,16,10,4,0\) | \(\mathbb F_3^4\) | \(1,25\) |
| \(5\) | \(6,2,0\) | \(M_3(\mathbb F_5)\oplus M_2(\mathbb F_5)\oplus\mathbb F_5^7\) | \(1,1,1,1,4,9,9\) |

The producer reconstructs the center, enumerates all central idempotents, and
extracts the primitive blocks; these dimensions are not copied from a prior
certificate. This is a radical/quotient/Loewy/center/block profile, not a claim
to classify every finite-dimensional algebra up to isomorphism.

## Passes 1331–1332 — exact scheme, selected words

The Pass-1327 \(S_3^{\rm internal}\times S_3^{\rm triality}\) grid has
eigenmatrix
\[
\begin{pmatrix}
1&2&2&4\\
1&-1&2&-2\\
1&2&-1&-2\\
1&-1&-1&1
\end{pmatrix}
\]
and primitive-idempotent ranks \(1,2,2,4\). Coordinate swap fuses it to
\(H(2,3)\), with ranks \(1,4,4\).

The selected cyclic words are
\[
(0,1,2,3,22,4,13),\qquad
(0,1,2,3,22,4,7,14).
\]
Their ordered and dihedral stabilizer orders in \(W(E_6)\) are respectively
\(2\) and \(1\), so their orbit sizes are \(25920\) and \(51840\). Both supports
have five chords and are not induced cycles. These are two deterministic
representatives, not a classification of every length-\(7\) or length-\(8\)
cycle orbit. Copy nonselection remains the theorem of Pass 1328.

## Pass 1333 — genuine AtlasRep execution

GAP 4.12.1 with AtlasRep, CTblLib, TomLib, and Repsn 3.1.2 constructs all three
degree-\(20\) representations of \(U_4(2).2\). Each has two \(20\times20\)
generators and image order \(51840\), hence is faithful. The table of marks
contains:

- an index-\(432\) action with degree-\(20\) multiplicities \([0,3,0]\);
- an index-\(480\) action with a single degree-\(20\) constituent.

This is the executed representation-theoretic result, not the earlier
coordinate-only plan.

## Pass 1334 — publication boundary

The theorem insert occurs exactly once in both `w33_paper.tex` and
`photonic_holonet.tex`. Source integration and static TeX checks pass. A full
PDF build remains an explicit CI boundary because this local environment has
no TeX engine; the release does not report a local PDF compilation.

## Reproduce

```bash
python3 analysis/w33_pass1330_1334_modular_triality_cycle_atlas.py
gap -q analysis/w33_pass1333_atlasrep_species20.g
python3 -m pytest -q tests/test_w33_pass1330_1334.py
```

Primary artifacts:

- [combined certificate](data/w33_pass1330_1334_modular_triality_cycle_atlas.json),
  SHA-256 `75ecd8ab12b4908907021b3088f35edd4d20b68c32584831dad9146622f28750`;
- [AtlasRep certificate](data/w33_pass1333_atlasrep_species20.json),
  SHA-256 `9fbc22720fb3cf64229a53e19f8b47476efee9be76de90e69084dedb6b5b0415`;
- [exact producer](analysis/w33_pass1330_1334_modular_triality_cycle_atlas.py);
- [GAP AtlasRep witness](analysis/w33_pass1333_atlasrep_species20.g);
- [focused contract](tests/test_w33_pass1330_1334.py).

The combined status is `PASS_WITH_DECLARED_TEX_BUILD_BOUNDARY`.
