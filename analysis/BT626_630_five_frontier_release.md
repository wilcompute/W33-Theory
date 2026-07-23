# Passes 626–630 — 2-adic, local-field, matrix-Hecke, optical, and e-process release

## Pass 626 — Canonical characteristic-two extension filtration

The central transposition class sum on `H2(F2)` yields the basis-free filtration

\[
0\subset \operatorname{im}T\subset \ker T\subset H_2,
\qquad
34\mid57\mid34.
\]

It is square-zero, and it induces an equivariant isomorphism from the top 34-dimensional quotient onto the bottom 34-dimensional image.  The 57-dimensional middle layer has a nonsplit trivial spine

\[
1\mid55\mid1.
\]

This is an exact strengthening of the earlier Jordan census.  It remains a mod-2 shadow rather than a complete computation of the integral `Ext^1` class.

## Pass 627 — Torsion-prime local maximal-order atlas

The seventeen spectral factors contribute total degree 256 and are all totally real.  Exact `p`-maximal order and prime-ideal decomposition data are certified at

\[
p\in\{2,3,5,7,13\}
\]

for all seventeen fields, giving 85 localizations.  The ramification loci are:

- `p=2`: fields 8,10,11,12,13,14,15,16,17;
- `p=3`: fields 4,6,10,11,12,13,14,15,16,17;
- `p=5`: fields 6,8,12,17;
- `p=7`: fields 3,15,17;
- `p=13`: fields 1,10,11.

The local statements are unconditional even though ten global field-discriminant residuals remain unresolved.

## Pass 628 — Regular-fibre matrix-valued Wilson Hecke algebra

Taking the regular `H=C2×C2` fibre gives

\[
\operatorname{Ind}_H^{S_8}\mathbb C[H]\cong\mathbb C[S_8],
\]

so the matrix-valued Hecke algebra is the full opposite group algebra of dimension 40,320.  The scalar corner has dimension 2,892.  Four Wilson holonomy classes and their three moment fingerprints are placed in all 22 Wedderburn blocks.

## Pass 629 — Certified analog optical tolerance region

For rail amplitude error `a`, rail phase error `theta`, and layer operator error `eta`, define

\[
\epsilon=a+2\sin(\theta/2),\qquad
\kappa=(1+\eta)^3-1,
\qquad
r=\kappa+(1+\kappa)\epsilon.
\]

Nearest-codeword decoding is guaranteed for `r<1/sqrt(2)`.  The stronger `r<1/2` region gives explicit finite-photon mode and sign error bounds.  Four declared tolerance profiles pass.

## Pass 630 — Composite-null anytime e-processes

Least-favourable interval endpoints produce Bernoulli and Poisson e-factors valid uniformly over declared phase, leakage, imbalance, and intensity intervals.  All twelve ordered class pairs remain separable.  Optional stopping and predictable adaptive sampling retain the `alpha=0.01` guarantee.

## Verification

- Pass 622 closes the previously missing torsion-prime atlas.
- Passes 621–630 are deterministic and certificate-backed.
- The focused regressions call every pass with `--check`.
- Boundaries are explicit: global residual factoring, full integral `Ext^1`, minimal physical fibre, correlated analog faults, and arbitrary temporal nuisance dependence remain open.
