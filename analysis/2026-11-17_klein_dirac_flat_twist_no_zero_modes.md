# Klein cubic link quotient: a sharp ordinary Dirac gap and a flat-twist firewall

**Date:** 2026-11-17. **Status:** exact finite group checks and a conditional application of a standard analytic eigenvalue theorem. **Scope:** the free order-55 quotient of the *Sasaki--Einstein* seven-link of the Klein cubic. This does not construct an observed vacuum or prove Standard Model chirality.

## Parent sources and collision check

Read the entire October 17, 2026 215-page \`papers/forty_points/main.pdf\` and audited 370 full Git patch bodies dated November 10--17. In particular, commit \`3095ad3e9\` establishes the invariant cubic/free subgroup and the SE metric input; \`bdf464270\` adds a 660-flag/60-orbit bridge; concurrent **uncommitted** \`analysis/2026-11-17_Klein_quotient_integral_flux_and_protected_modes.md\` develops integral cohomology and the independent 15 flat C-field sectors. That work is not edited or incorporated as an unreviewed Git artifact. Search of the GitHub code index for "Friedrich" and "Dirac gap" did not find this specific 7D link result.

## An exact group-theoretic prelude

For the Klein cubic
\[
f(x)=\sum_{i=0}^4x_i^2x_{i+1},\qquad i\ \mathrm{mod}\ 5,
\]
put \(\zeta=e^{2\pi i/11}\), \(w=(1,9,4,3,5)\),
\(D=\mathrm{diag}(\zeta^{w_i})\), and let \(P\) cyclically permute the five coordinates. The script verifies term by term
\(2w_i+w_{i+1}=0\pmod {11}\), \(\sum w_i=0\pmod {11}\), \(\det P=1\), and
\(PDP^{-1}=D^9\).
Consequently \(G=\langle D,P\rangle=C_{11}\rtimes C_5\), order 55. Its derived subgroup is \(C_{11}\), so
\[
G_{\mathrm{ab}}\cong C_5,\qquad \mathrm{Hom}(G,U(1))\cong\mathbb Z/5.
\]
Its seven complex irreducible representations have dimensions
\[
1,1,1,1,1,5,5
\]
(the two five-dimensional irreducibles arise from two five-element orbits of nonzero characters of \(C_{11}\)). The sum of squared dimensions is exactly 55.

The 55 group elements have no fixed point on the link. For \(D^a\ne 1\) the diagonal eigenvalues differ from one. For \(b\ne0\), \(D^aP^b\) is conjugate by a power of \(D\) to \(P^b\). The latter's fixed line is \(t(1,1,1,1,1)\) where \(f=5t^3\); the only fixed vector on the cone is zero. Our verifier checks the exact modular conjugation identities for all 44 mixed elements. The given smoothness and Einstein metric input remain separately cited, not established by this arithmetic alone.

## New conditional spinorial obstruction

Let \(Y\) be the smooth seven-link with its invariant Sasaki--Einstein metric, \(\mathrm{Ric}_Y=6g_Y\), and \(M=Y/G\). Since the action is free and isometric, \(M\) is a closed Einstein seven-manifold with
\[
\mathrm{Ric}_M=6g_M,\qquad \mathrm{Scal}_M=7\cdot6=42.
\]
The parent report verifies the spin quotient. An additional independent group check is that \(G\) has odd order, hence no nontrivial homomorphism \(G\to C_2\). Because the link is simply connected, its quotient has a unique spin structure whenever spin; \(H^1(M;\mathbb Z_2)=0\).

For the **ordinary Riemannian spin Dirac operator**, Friedrich's estimate is
\[
\lambda(D)^2\ge\frac{n}{4(n-1)}\inf_M\mathrm{Scal}
  =\frac{7}{24}\cdot42
  =\boxed{\frac{49}{4}},
\qquad |\lambda(D)|\ge\boxed{\frac72}.
\]
Proof sketch: decompose the spinor covariant derivative into its twistor and Clifford-trace parts. The twistor norm is nonnegative; the Lichnerowicz identity \(D^2=\nabla^*\nabla+\mathrm{Scal}/4\) yields the quoted bound. Equality forces a real Killing spinor, as is standard for Sasaki--Einstein geometry.

**More strongly:** for a unitary flat vector bundle \(E_\rho\) associated to *any* unitary representation \(\rho:G\to U(r)\), its curvature is zero. The twisting curvature term in the Weitzenbock identity vanishes; the same twistor proof gives
\[
|\lambda(D_{E_\rho})|\ge7/2.
\]
Thus \(\ker D_{E_\rho}=0\) for **all** unitary flat twists, including each of the five line characters and both five-dimensional irreducibles. This says neither Wilson-line holonomy nor an uncharged ordinary bulk spinor alone produces a zero eigenmode on this smooth positive-Ricci quotient.

## Why this is a TOE constraint, not a no-go for all physical fermions

- The bound is for the *untwisted spin connection with optional flat unitary bundles*, **not** for the supercovariant/gravitino internal operator with \(G_4\) terms, charged non-flat gauge bundles, or localized M2/M5 sectors. A flux-induced zeroth-order term can shift a nonzero Dirac eigenvalue into a massless four-dimensional equation.
- There are **five** flat complex line characters, not 15. The \(\mathbb Z_{15}\) flat degree-four C-field sector in the concurrent integral-cohomology analysis is a different differential-cohomological object. It does not create 15 ordinary line bundles.
- The \(7/2\) bound does not by itself select a chiral Standard Model spectrum, Yukawa couplings, or four-dimensional Minkowski spacetime.
- Equality is compatible with the Killing spinors of a Sasaki--Einstein metric; it should not be confused with a harmonic spinor of eigenvalue zero.

**Physical decision:** Any Standard Model matter claim for this *smooth* Klein-link quotient must supply an explicit flux-coupled, non-flat bundle, or localized-sector spectral operator and calculate its zero-mode content. Assigning fermions from the order-55 group labels or 15 torsion C-fields is insufficient.

## Verification and sources

Run:
\`\`\`powershell
python analysis/toe_20261117_klein_dirac_flat_twist_gap.py
python -m unittest discover -s tests -p test_toe_20261117_klein_dirac_flat_twist_gap.py -v
\`\`\`

The verifier writes \`data/toe_20261117_klein_dirac_flat_twist_gap.json\` with exact group and rational eigenvalue certificate.

External mathematical sources:
- Friedrich/Hijazi estimate and equality case: https://link.springer.com/article/10.1007/s00220-022-04420-y
- Geometric spinor proof of equality and Killing spinors: https://prf.uhk.cz/geometry/DiracNotesSchool2019Chrysikos.pdf
- Classical seven-dimensional Killing-spinor context: https://www.researchgate.net/publication/251315393_The_Second_Dirac_Eigenvalue_of_a_Nearly_Parallel_G_2_Manifold
- Klein-cubic subgroup and Einstein input: \`analysis/2026-11-17_11cell_Klitzing_Klein_cubic_11D.md\`.

## Five independent follow-ups

1. Compute the genuine flux-shifted 11D fermion/gravitino KK operator and its spectrum on this quotient.
2. Calculate the equivariant eta-invariant and phase of the fermion determinant for all seven flat irreps.
3. Model localized M2/M5 or singular-sector charged chiral matter, including anomaly cancellation.
4. Compare the Klein seven-link M-theory branch directly with the alternate Type IIB \(T^{p,q}\) stability route, without identifying their geometries.
5. Search for a non-W33 finite incidence/Clifford construction that *derives* an observed dimensionless coupling or mass ratio with a null-model comparison.
