# Intake audit — E8 spectral descent is exact; the proposed W33 bridge is not

## Verdict

Commit `ee1ff4ac7` brought in a useful exhaustive computation, but its theorem
surface mixed three different statuses:

1. exact spectral facts;
2. rediscoveries of results already owned by this corpus; and
3. bare equalities presented as maps that were never constructed.

The exact content survives. The statement that E8 spectral descent derives a
33-vertex W33 object is retracted. The symplectic generalized quadrangle
`W(3,3)` has

\[
(3+1)(3^2+1)=40
\]

points, and its point-collinearity graph is `SRG(40,12,2,4)`, with spectrum

\[
12^1\oplus 2^{24}\oplus(-4)^{15}.
\]

Both the repaired Python source and an independent GAP construction now check
this directly.

## What survives exactly

For the graph on all 240 signed E8 roots, with adjacency
`<alpha,beta>=+1`, the repaired witness certifies over the integers

\[
56^1\oplus28^8\oplus8^{35}\oplus(-2)^{112}\oplus(-4)^{84}.
\]

The neighborhood of a root is a 56-vertex **E7 minuscule carrier**, not an
E7 root system. Its spectrum is

\[
27^1\oplus9^7\oplus(-1)^{27}\oplus(-3)^{21}.
\]

One further neighborhood gives the Schlaefli graph
`SRG(27,16,10,8)` with spectrum

\[
16^1\oplus4^6\oplus(-2)^{20}.
\]

These are now checked by distinct-root annihilating polynomials plus exact
trace moments. No floating-point eigensolver is part of the certificate.
The 27 cubic-surface lines and their E6 geometry agree with the classical
construction discussed by Manivel in
[Configurations of Lines and Models of Lie Algebras](https://arxiv.org/abs/math/0507118).

The E8 graph has exactly 60,480 triangles, and

\[
60480=240\,\sigma_3(6).
\]

That equality is exact, but the theta coefficient `60480` was already recorded
in `analysis/w33_BREAKTHROUGH_70_eisenstein_trees_GUT_universal.py` and
`analysis/w33_BREAKTHROUGH_183_E8_theta_series_substrate_GF.py`.

## What was already ours

- The complete E8 positive-inner-product spectrum is already stated in
  `analysis/PASS7163_7170_e8_hexagonal_lift_insert.tex` and owned again with
  its five-class association algebra in
  `analysis/BT7171_BT7186_e8_d4_h27_q9.md`.
- The Schlaefli parameters and spectrum are already certified in
  `analysis/PASS4640_4647_RESERVATION.md`.
- Most decisively, `analysis/PASS7017_7024_schlafli_w33_equivariant_no_go.md`
  already compares the actual 27- and 40-point carriers under the common
  `PSp(4,3)` action and proves

  \[
  \dim\operatorname{Hom}_{PSp(4,3)}
  (\mathbb C^{27},\mathbb C^{40})=1.
  \]

  The one channel is constant. Thus equality of nearby integers cannot supply
  the missing nonconstant full-group bridge.

## What is refuted or remains unbuilt

| Incoming statement | Audited status |
|---|---|
| `W33` has 33 vertices obtained as `27+6` | **Refuted.** `W(3,3)` has 40 points. |
| the 56-vertex local object is an E7 root graph | **Corrected.** It is the E7 minuscule carrier; E7 has 126 roots. |
| the Schlaefli multiplicity 6 supplies six W33 vertices | **Unbuilt and carrier-invalid.** An eigenspace dimension is not a vertex set. |
| `84=168/2` gives a W33 bridge | **Arithmetic only.** No group map or incidence map is named. |
| `240=8*2*15` is an eight-doily decomposition | **Unbuilt.** A factorization is not a partition, much less an invariant one. |
| `60480=240*sigma_3(6)` identifies triangles with theta vectors | **Exact equality, old result, no bijection supplied.** |

## The bridge that actually exists

The adjacent Passes 7317–7320 build an object-level E8/E6 bridge rather than
inferring one from cardinalities. Starting with the selected E8 D4 spread code,
they intrinsically recover 36 double-sixes, identify their signed switching
class with 36 actual E8 root lines in an `A2` orthogonal complement, and prove
the centered incidence factorization

\[
-\frac{N_0}{\sqrt{18}}
=
\left(\frac{T_0}{\sqrt6}\right)^T
\left(\frac{R_0}{\sqrt{12}}\right).
\]

Here the matrices and maps are explicit: double-sixes pass through the common
20-dimensional E6 constituent to selected E8 D4-pairs. That is a usable bridge;
`27+6=33` is not.

## Replay

```bash
python3 scripts/PART_CCCCCXCIX_e8_spectral_w33_bridge.py
gap -q analysis/w33_e8_spectral_descent_scope_audit.g
```

Expected terminal facts are the three exact spectra, 40 W33 points,
`SRG(40,12,2,4)`, and the explicit rejection of `27+6=33` as a W33 vertex
decomposition.
