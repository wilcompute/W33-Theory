# The Qpsi clock is an anchored GQ(2,4) parabolic

The existing objectwise Z6 certificate fixes one conventional (Q_\psi)
chart on the (E_6) minuscule 27.  Its charge-(4) singlet is one cubic-surface
line, the ten lines meeting it have charge (-2), and the remaining sixteen
have charge (1).  The new result is that this is an intrinsic incidence
formula, valid equivariantly for every possible anchor:

\[
\boxed{q_a(i)=1+3\delta_{ai}-3A_{ai}},
\]

where (A) is the adjacency matrix of the 27-point meet graph of
(GQ(2,4)).  Thus choosing one point (a) immediately compiles

\[
27=1_{4}+10_{-2}+16_{1}
\]

without consulting weight coordinates.

## Cubic conservation becomes a quadrangle axiom

Every point of (GQ(2,4)) lies on five three-point lines.  A line through the
anchor has charges

\[
(4,-2,-2),
\]

while the generalized-quadrangle axiom gives exactly one point collinear with
the anchor on each of the other forty lines, hence

\[
(-2,1,1).
\]

All 45 Cartan cubics therefore conserve (Q_\psi) for incidence reasons:

\[
45=5\times(-2,-2,4)+40\times(-2,1,1).
\]

The executable certificate checks this for all 27 choices of anchor, not only
for the conventional chart.

## The SO(10) choice is a point stabilizer

The six exact simple reflections on the minuscule weights generate

\[
|W(E_6)|=51840.
\]

They act transitively on the 27 charge charts.  The five reflections fixing
the highest-weight anchor have the (D_5) Cartan matrix and generate the full
point stabilizer:

\[
|W(D_5)|=1920,\qquad W(E_6)/W(D_5)=27.
\]

So the familiar choice (E_6\supset SO(10)\times U(1)_\psi) has a finite
geometric reading: choose one of the 27 minuscule weights/cubic-surface lines.
Its (D_5) Weyl group is exactly the symmetry that preserves the resulting
clock.  The 27 possible clocks form one (W(E_6)) orbit.

## Virtual-machine consequence

On the frame-address register, the order-12 clock can now be evaluated as

\[
D_{12}(a)|i,p\rangle
=\zeta_{12}^{\,1+3\delta_{ai}-3A_{ai}}|i,p\rangle.
\]

It needs only an equality predicate and one (GQ(2,4)) adjacency predicate.
This closes the address-side compilation of (Q_\psi).  It does not yet say
how that diagonal clock factors in the trinification basis

\[
\mathbb C^9_{\rm mult}\otimes\mathbb C^3_{\rm int}\otimes
\mathbb C^3_{\rm ext}.
\]

The subsequent complete Steiner-atlas certificate exhausts all 51,840
Weyl-compatible monomial factorizations and proves that only powers (0,4,8)
normalize the Pauli execution algebra.  Parallel representation audits also
prove that the missing root-gauge map cannot be an equivariant basis
conjugacy: the maximum ranks are 9 on the 27-dimensional H27 modules and 27
on the 81-dimensional K modules.  A later exact construction supplies a
K-Fourier-coordinate permutation compiler that preserves 27 coordinates and
retypes the minimum possible 54.  The remaining task is to materialize and
compose the frozen-root/address-to-Fourier analysis map and to realize those
retypings physically; neither is needed to answer the finite monomial
normalizer question.

## Ownership and external checks

`analysis/w33_z6_objectwise_33_48_32_carrier.py` owns the previously known
single-anchor (1+10+16) split.  The repository also already records the
quotient count (51840/1920=27).  The increment here is their exact
composition: the closed adjacency formula for all 27 anchors, its
(W(E_6))-equivariance, the full (W(D_5)) stabilizer certificate, and the
incidence-only proof of all 45 cubic charge sums.

The classical facts that the 27 lines form the minuscule (W(E_6)/W(D_5))
orbit and that (GQ(2,4)) has automorphism group (W(E_6)) are external prior
art.  No claim of novelty is made for those ingredients separately.

Scope: this is an exact finite representation/incidence/compiler theorem.  It
does not physically select an anchor, assign observed generations, determine
a vacuum, materialize the frozen-root-to-Fourier analysis matrix, or realize
the 54 representation retypings dynamically.
Full H27/K equivariance is already ruled out by the rank obstructions.  Its
formerly open monomial normalizer follow-up is closed by
\`analysis/w33_steiner_trinification_qpsi_normalizer.py\`.
