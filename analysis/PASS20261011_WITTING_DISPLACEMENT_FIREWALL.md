# 2026-10-11 — Witting displacement firewall: symmetric higher operators cannot nudge the radiative vacuum

Producer: analysis/w33_20261011_witting_displacement_firewall.py
Certificate: data/w33_20261011_witting_displacement_firewall.json

## Exact theorem

Pass 1068 gives the exact parabolic inclusion

\[
G_{25}\hookrightarrow G_{32}
\]

in the standard Eisenstein reflection representation. The first three
\(G_{32}\) reflections fix the Witting reference axis pointwise and act on its
three-complex-dimensional transverse space as \(G_{25}\), order \(648\).
Exact \(\mathbb Q(\omega)\) row reduction gives

\[
\dim T^{G_{25}}=0,\qquad \dim (T^*)^{G_{25}}=0.
\]

Pass 11664 independently identifies this same triplet with the actual
transverse Witting modes of the committed E8/two-qutrit model and exhibits
its \(H_{27}\) clock/shift matrices \(ZX=\omega XZ\).
Let \(V\) be any differentiable \(G_{32}\)-invariant scalar and \(r\) a
Witting ray. Because the pointwise \(G_{25}\) subgroup fixes \(r\), the
restricted differential \(dV_r|_T\) must be a \(G_{25}\)-fixed covector.
There is no such nonzero covector. Therefore

\[
\boxed{dV_r|_T=0.}
\]

By conjugacy the statement holds at all forty Witting rays. In particular,
potentials built only from the \(G_{32}\) invariant generators of degrees
\(12,18,24,30\), their conjugates and scalar functions thereof leave every
Witting ray an exact projective stationary point.

This is a symmetry theorem, not a small-coefficient approximation.

## Correction to Pass 11891

The geometric cusp theorem remains intact:

\[
\operatorname{Im}\Omega =
\left(\frac3\pi+o(1)\right)\log(1/\delta),
\qquad \epsilon\propto\delta.
\]

What must be withdrawn is the proposed source
\[
\delta\sim(v/\Lambda)^8
\]
from a \(G_{32}\)-invariant degree-12 scalar by itself. Such an operator has
zero tangent force at the Witting ray.
It may lift the common phase or modify transverse stability. The execute-all-five follow-up sharpens the
bifurcation option: after the common 84 phase is relaxed, any single nonzero invariant harmonic stabilises the Witting
ray at quadratic order. An invariant-driven projective instability therefore needs competing phase harmonics (minimally
two degrees, such as 12 and 18) or another sector that fixes the phase. It cannot produce a generic perturbative linear
displacement of a projectively stable Witting minimum.

Thus a nonzero small \(\delta\) requires at least one of:

1. an explicit \(G_{32}\)-breaking transverse spurion;
2. a competing-harmonic or phase-fixed bifurcation that changes the tangent Hessian sign;
3. a coupled sector whose background itself breaks the Witting stabilizer.

## New cross-sector target: the flavour qutrit is in the right slot

Pass 11921 independently proves that flux factorises
\(A[3]\cong\mathbb F_3^4\) into two flavour qutrits and that the radiatively
preferred \(H_u\) top space is exactly three-dimensional.

That is precisely the dimension and qutrit representation type of the actual
Witting transverse \(G_{25}/H_{27}\) triplet from Pass 11664. Therefore the
minimal symmetry-breaking field required by the vacuum hierarchy mechanism
has the same representation type as the Higgs flavour variable that the
current quark-sector calculation says must be modified.
This does **not** yet identify the two physical spaces. No phase-resolved
intertwiner from the Pass 11921 theta-function Higgs basis to the Pass 11664
Witting tangent basis is supplied here, and no cross-sector coupling is
derived. The result instead turns two separate open problems into one sharply
posed calculation:

> construct or rule out an \(H_{27}\)-covariant coupling between the flavour
> Higgs qutrit and the Witting transverse triplet whose background weakly
> breaks the magnetic-translation class symmetry while retaining the
> radiative Witting selection.

If such a coupling exists, the same small spurion can in principle generate
both the projective displacement \(\delta\) controlling the theta hierarchy
and the weak cross-class admixture required by Pass 11914/11921. If no such
intertwiner/coupling exists, the single-home two-qutrit flavour programme is
closed more strongly.

## Boundary

The no-displacement theorem is exact finite representation theory. The
cross-sector identification is a representation-compatible research target,
not a derived Standard Model interaction, observed hierarchy, or prediction.
