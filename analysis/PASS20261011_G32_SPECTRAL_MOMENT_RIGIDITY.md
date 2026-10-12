# 2026-10-11 — G32 spectral-moment rigidity: the first angular power sum is p4

Producer: `analysis/w33_20261011_g32_spectral_moment_rigidity.py`
Certificate: `data/w33_20261011_g32_spectral_moment_rigidity.json`

## Representation theorem on the actual Vinberg Cartan

Use the five committed generators of the four-dimensional \(G_{32}\) Cartan action from Pass 11879. On the normalized
symmetric tensor powers, the numerical commutant dimensions are

\[
\dim\operatorname{End}_{G_{32}}\operatorname{Sym}^k(\mathbb C^4)
=
1,1,1,2,\qquad k=1,2,3,4.
\]

The smallest nonzero singular value in the four stacked commutant calculations is \(>0.85\), while the numerical null
singular values are at the \(10^{-15}\) level. Thus this is not a near-degeneracy.

Consequently a \(G_{32}\)-invariant Hermitian form of bidegree \((k,k)\) is forced to be radial for \(k\le3\).
At \(k=4\), exactly one additional angular invariant becomes available.

The vector mass-squared power sums

\[
p_k(c)=\sum_{i=1}^{80}e_i(c)^k
\]

are precisely such invariant Hermitian forms. Calibrating on the exact Witting spectrum

\[
0^{24},\qquad (1/3)^{54},\qquad 1^2
\]

therefore gives, on the unit Cartan sphere,

\[
\boxed{p_1=20,\qquad p_2=8,\qquad p_3=4.}
\]

The first angular power sum is \(p_4\). At the Witting ray \(p_4=8/3\); over 128 deterministic random Cartan directions
the certificate sees a broad nonzero \(p_4\) range while \(p_{1,2,3}\) remain fixed to \(2.2\times10^{-14}\).

## Why this matters for loop dynamics

For an exact positive scalar mass shift \(s\), one elementary one-loop spectral contribution is

\[
H_s(c)=\sum_i\Big[(e_i+s)^2\log(e_i+s)-e_i^2\log e_i\Big].
\]

At large \(s\),

\[
H_s=
\text{radial}(s,p_1,p_2)-F
+\frac{p_3}{3s}
-\frac{p_4}{12s^2}
+\frac{p_5}{30s^3}
-\frac{p_6}{60s^4}+\cdots,
\qquad
F=\sum_i e_i^2\log e_i.
\]

Because \(p_3=4\) is also radial, the first finite-\(s\) angular correction to the asymptotic \(-F\) selector is

\[
\boxed{-\frac{p_4}{12s^2}.}
\]

This explains why the finite-soft phase diagram is much more constrained than a generic spectral deformation: the
quadratic, quartic and sixth-order power sums cannot independently steer the Cartan angle.

## Relation to classical E8 design theory

The rigidity is consonant with the classical fact that the 240 minimal vectors of the \(E_8\) lattice form a spherical
7-design. In particular, polynomial averages through degree seven are isotropic on the root shell. The present result
is narrower and more model-specific: it computes the commutants in the repository's actual four-dimensional
\(G_{32}\) Vinberg-Cartan representation and applies them directly to the committed SU(9) vector-mass spectrum.

Useful external references:
- E. Bannai et al., *Spherical designs and extremal lattices*: \(E_8/\sqrt2\) is a spherical 7-design.
- Delsarte–Goethals–Seidel / Venkov design theory for extremal even unimodular lattices.

## Boundary

The dimensions above are obtained with double-precision matrices for the exact committed finite-group generators,
not an exact CHEVIE character-table computation. The singular-value gap is large and the mass-moment replay is
independent, but this certificate is Tier-C numerical representation theory.

No particle mass, SUSY-breaking scale, renormalisation prescription or Standard Model parameter is inferred.
