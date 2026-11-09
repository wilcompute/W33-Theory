# The canonical differential across a chiral pezzotope pair

The [Pass 12634 pentad construction](PASS12634_NARUKI_FAN.md) and the [real Yoshida atlas](2026-11-09_yoshida_integral_fibers_and_chirality.md) label 432 chambers and give the double-six reflection over each of the 216 ten-line supports. The canonical form and its orbit of 432 translates are prior results. Here the two forms over each support are compared as rational differential forms in one function field. The comparison uses the orientations obtained by transporting the published seed form. [Early et al., Positive del Pezzo Geometry, Theorem 10.5](https://arxiv.org/html/2306.13604v3#S10)

## Identify the reflection before comparing the forms

Match the six simple covectors in the difference, triple-sum and conic-root chart to the integral $E_6$ root chart, then check the Gram matrix on the full six-dimensional span. At an exact point of the published positive parametrization, calibrate all 40 products of minors against the oriented root products. The resulting atlas mask is 0x580155600. Its partner is 0x1c152b2f51, and its distinguished root is the triple 135. The corresponding quadratic Cremona involution uses columns 1, 3, and 5 as centers. A direct Cremona computation at the sample gives the partner mask. The conic-root Gale involution gives a different comparison for this seed. The root labels in the paper's combinatorial picture need a chart crosswalk before they can be used as labels of the positive parametrization.

In the chart with first three columns the identity, fourth column $(1,1,1)$ and last columns $(1,x,y)$ and $(1,z,w)$, let $\Omega$ be the published canonical form. Let $\Omega'=s_{135}^{*}\Omega$. Compute the pullback with the signed Jacobian of the Cremona map. The Plücker formula and the wedge of the four $d\log$ parameters give exactly the same coefficient in this chart. Their partner comparison simplifies to
\[
\frac{\Omega'}{\Omega}
  =-\prod_{i=1}^{10}u_i \prod_{j=11}^{15}u_j^2 .
\]
In the positive logarithmic coordinates $(a,b,c,d)$ this equals
\[
-\frac{ab^2cd}{g_3g_8g_{10}},
\]
with the three polynomials from the published parametrization. Each is positive there, and their product contains the numerator monomial and a positive constant term. Thus the ratio lies strictly between $-1$ and $0$ on the seed. Under the involution it goes to its reciprocal and lies below $-1$ on the partner. In particular $\log|\Omega'/\Omega|$ distinguishes the ordered pair and changes sign under the reflection. It is a function on the union of this pair of real components. Relabeling the two chambers changes its sign.

The certificate contains Weyl words from the seed to all 432 chambers and checks that the distinguished roots are transported at every generator step. This gives the same relation for all 216 pairs in transported coordinates. The published form has 432 distinct Weyl translates, so its stabilizer is the chamber stabilizer. In particular the transported comparison is independent of the chosen word carrying the seed to a specified chamber. [Early et al., Proposition 9.1 and Theorems 10.5–10.6](https://arxiv.org/html/2306.13604v3#S9)

## Residues separate the boundary supports

The two chambers in each pair have disjoint sets of the 15 atlas facet labels. The 432 chamber labels here are a separate inventory from the 432 incident double-six/line flags counted in [Pass 1139](PASS1139_COMPLETE_DEGREE540_SPECIES_CENSUS.md). On the seed side the ratio vanishes to order one on each of the ten root facets and order two on each of the five cusp facets. Consequently $\Omega'$ is regular along the seed's root facets and vanishes to first order along the seed's cusp facets. The reciprocal result holds on the partner. This statement concerns generic points of the divisors.

The exact root valuation crosswalk gives the primitive normal of each ordered $u_i$ boundary in the four logarithmic parameters. Contract the oriented logarithmic volume form with the primitive normal to get each facet residue, and take the determinant of the four ordered normals to get a maximal iterated residue. The 45 vertex residues have absolute value one. The matrices on paired boundaries agree after pulling back by the reflection and transporting their labels and orientations. The signed ratio in a common chart and the equality of the transported residues describe different comparisons.

## The boundary comparison uses the order-three character

On the root-arrangement chart, let $L$ be the integer span of the 39 projective Yoshida exponent rows. Its saturation has quotient $\mathbb Z/3$ as in the earlier atlas calculation. All 15 facet functions have the same nonzero exponent class in this quotient. With $[u_1]$ as generator, the four canonical logarithmic parameters have classes $(2,1,2,1)$ and the absolute form ratio has class 2. Reflection takes $[u_1]$ to class 2. The 15 primitive facet valuations pair with the 15 facet exponents as an identity matrix. Thus the exponents form an integral basis of the saturation, and the Yoshida lattice consists of combinations whose coefficient sum is divisible by three. Exact Smith decomposition gives integral Yoshida exponents for $u_1^3$, for each $u_i/u_1$, for $u_1(u_1\circ s_{135})$, and for $|\Omega'/\Omega|/u_1^2$ on the positive component, with constant signs depending on root conventions.

One cube root of a Yoshida character thus suffices to express the facet parameters in the ambient monomial lattice. The existing marked-moduli function $u_1$ already supplies the root on the actual very affine variety. This exponent obstruction does not force a nontrivial three-sheet cover of the marked moduli space or a physical discrete charge.

## The ratio fixes one scattering potential

In the Schwinger parametrization of Theorem 10.8 the ratio selects weights $(1,\ldots,1,2,\ldots,2)$ on the ten root and five cusp facets. It yields the positive tropical potential
\[
F(w)=\langle (1,2,1,1),w\rangle-\operatorname{trop}(g_3g_8g_{10})(w),
\]
where tropicalization takes the minimum exponent pairing. The exact minimizer sets show that this three-factor product has a coarser normal fan than the published eleven-factor product. In this specialized kinematic direction the 45 maximal cones select 19 Newton vertices. Five receive one cone each, eight receive two each, and six receive four each. The published 45-cone refinement still partitions the integral into unimodular domains. Each cone contributes the reciprocal product of its four weights. There are five root-only cones and forty with one cusp, so the selected Schwinger integral is $5+40/2=25$. This is a mathematical amplitude evaluation in the published conventions. No particle cross section or fitted coupling is inferred. [Early et al., Theorem 10.8](https://arxiv.org/html/2306.13604v3#S10)

## Reproduce

Run python analysis/toe_20261109_pezzotope_canonical_partner.py from the repository root. The output gives the two rational forms, the coordinate involution, facet crosswalk, signed residues, transport words and integral character identities. An independent server calculation verifies the involution with its differential and the ratio identity at 90 nonsingular finite-field points across three primes. The exact symbolic check is over characteristic zero.
