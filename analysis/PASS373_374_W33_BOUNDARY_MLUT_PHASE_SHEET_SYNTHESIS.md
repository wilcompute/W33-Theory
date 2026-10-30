# Passes 373-374: W33 boundary MLUT and minimal-logical phase sheets

## Status

Both passes are GAP-owned, exact, and independently regression-tested.

The two results concern different objects on the same 240-edge carrier:

1. the classical triangle-boundary image over `GF(3)`;
2. the scalar sheets above the already-known minimal-logical X/Z ray pairing.

The distinction is essential.  The first is a conventional classical linear
code.  The second is an orbit problem in the logical quotients of the canonical
qutrit CSS code.

## Corpus reconciliation before novelty

Result-first searches found that the canonical qutrit CSS code was already
settled on 2026-05-18 by:

- `analysis/2026-05-18_w33_css_exact_audit.md`;
- `analysis/w33_css_exact_audit.py`;
- `analysis/2026-05-18_minimal_logical_witness_census.md`;
- `analysis/2026-05-18_minimal_logical_e6_pairing.md`.

Those files already prove

\[
[[240,81,3]]_3,\qquad d_X=3,\qquad d_Z=4,
\]

and count 320 minimal X vectors, 3240 unique minimal Z vectors, and 51840
nonzero vector pairings.  Passes 373-374 do not reclaim those results.

The exact new gaps were instead:

- no conventional code parameters or complete MLUT had been proved for
  \(B_1=\operatorname{im}\partial_2\) itself;
- the older BT571/BT637/BT644 lineage already constructed the four
  `F3* x F3*` scalar lifts, their balanced phase character, and deck sign
  involutions, while `w33_visible_pair_orbit_weyl_torsor.py` owned the
  projective 12960-orbit.  None classified the natural group action on all
  51840 scalar lifts or its stabilizers.

## Pass 373: exact boundary code and complete radius-one MLUT

Let

\[
B_1=\operatorname{im}(\partial_2)\subseteq\mathbb F_3^{240},
\]

where the 160 oriented W33 triangles map to the 240 oriented edges.

GAP proves:

\[
\boxed{B_1=[240,120,3]_3.}
\]

The proof is a parity-column certificate, not a search through
\(3^{120}-1\) codewords:

- the triangle-boundary rank is 120;
- the dual parity-check rank is 120;
- all 240 parity-check columns are nonzero, excluding weight one;
- all 240 projective column classes are distinct, excluding weight two;
- every triangle supplies an explicit weight-three word.

Therefore the minimum distance is exactly three.

Every one-edge error has one of two nonzero values, so there are

\[
2\cdot240=480
\]

distinct nonzero single-error syndromes.  Including the zero syndrome gives the
complete radius-one lookup table:

\[
\boxed{|\mathrm{MLUT}_{t=1}|=481.}
\]

This exact certificate replaces an accidental `3**120` exhaustive path in
`scripts/w33_quantum_error_correction.py`.  The runtime now uses the general
ternary parity-column criterion for distances one through three before falling
back to exhaustive enumeration for genuinely modest dimensions.

### Object boundary

The boundary image \([240,120,3]_3\) is not the 81-dimensional logical object.
The CSS code uses both vertex and triangle checks:

\[
H_X=\partial_1,qquad H_Z=\partial_2^T,
\]

and its logical sectors are quotients.  The already-owned result is

\[
[[240,81,3]]_3,\qquad d_X=3, d_Z=4.
\]

In particular, the 81-dimensional Steinberg/H1 module is not a separate bare
`[240,81,4]` classical code.

## Pass 374: the natural action preserves the four known scalar sheets

Let \(X_{\min}\) and \(Z_{\min}\) be the minimal logical vector sets:

\[
|X_{\min}|=320,qquad |Z_{\min}|=3240.
\]

Let

\[
\mathcal P=\{(x,z):\langle x,z\rangle\ne0\}.
\]

The earlier pairing census gives

\[
|\mathcal P|=51840,
\]

with phases split evenly as \(25920+25920\).  The equality
\(|\mathcal P|=|W(E_6)|\) invited a torsor reading.  BT571 and its descendants
already described the fourfold scalar cover and its phase/deck maps, but no
natural \(PSp/PGSp\) action on that cover had been classified.

Pass 374 constructs the natural action explicitly.  A point collineation sends
an oriented edge to the image edge, inserting a minus sign when canonical edge
orientation reverses.  This signed permutation acts on both minimal logical
vector sets and preserves their `GF(3)` pairing.

The full-group label is not inferred from the common order.  Pass 125 already
constructs the same multiplier-two projective similitude and identifies the
resulting \(PGSp(4,3)\) with \(W(E_6)\); Pass 374 reuses that owned action and
computes its new orbit structure on the scalar pair set.

The exact orbit classification is:

The machine-searchable orbit signature is
`[12960,12960,12960,12960]` for both actions.

| Acting group | Order | Orbits on \(\mathcal P\) | Stabilizer |
|---|---:|---:|---:|
| \(PSp(4,3)\) | 25920 | \(12960+12960+12960+12960\) | \(C_2\) |
| \(PGSp(4,3)=PSp(4,3){:}2=W(E_6)\) | 51840 | \(12960+12960+12960+12960\) | \(C_2\times C_2\) |

Thus

\[
\boxed{
\mathcal P\cong
\bigsqcup_{s\in C_2\times C_2} W(E_6)/(C_2\times C_2)
}
\]

as a natural `W(E6)`-set.

The deck group, already owned by the BT571/BT637 scalar-cover lineage, is
concrete:

\[
C_2^X\times C_2^Z,
\qquad
(x,z)\mapsto(-x,z),\quad(x,z)\mapsto(x,-z).
\]

The two pairing phases are each split into two simultaneous-sign sheets.  The
outer similitude preserves all four sheets; it does not fuse them.

### Torsor verdict

\[
\boxed{
51840=|W(E_6)|\text{ is a cardinality identity here, not a regular-action theorem.}
}
\]

The natural full action has four orbits and a Klein-four stabilizer.  A regular
51840-state action would need additional, non-geometric phase transport.  No
such transport is supplied by W33 collineations or by the signed chain functor.

Pass 374 adds the missing equivariant half rather than another count: the
natural signed-chain action, its orbit decomposition, its stabilizers, and the
exact obstruction to a Weyl torsor are now executable.  It reuses rather than
reclaims the earlier scalar bundle and deck transformations.

## Artifacts

- `analysis/w33_pass373_triangle_boundary_mlut.g`
- `data/w33_pass373_triangle_boundary_mlut.json`
- `tests/test_pass373_gap_triangle_boundary_mlut.py`
- `analysis/w33_pass374_minimal_pair_phase_sheet_obstruction.g`
- `data/w33_pass374_minimal_pair_phase_sheet_obstruction.json`
- `tests/test_pass374_gap_minimal_pair_phase_sheet_obstruction.py`
- `scripts/w33_quantum_error_correction.py`
- `tests/test_e8_embedding.py`

The earlier projective owner remains
`analysis/w33_visible_pair_orbit_weyl_torsor.py`; its theorem label and output
have been narrowed to the projective orbit and cardinality lift that it actually
proves.

## Honest scope

Pass 373 proves a classical ternary code and a one-error decoder table.  It does
not by itself establish a quantum threshold.

Pass 374 classifies a finite group action.  It does not provide the extra phase
transport needed for a regular Weyl action, a braid representation, or a
continuum physical dynamics.
