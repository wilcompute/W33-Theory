# Ledger/W33 continuation — five further pressure tests

This packet begins from the two prior Ledger packets and checks repository prior art before promoting anything. The bouquet/free-group topology is not new: archived exploratory work already owned the q=3 statement and stated the all-q pattern. The contribution here is the missing constructive collapse certificate and its Ledger consequence.

## 1. Three words suffice for an explicit n-party family

For every n>=3 choose three proper regions
\[
R_1=[n]\setminus\{1\},\quad R_2=[n]\setminus\{2\},\quad R_3=[n]\setminus\{3\},
\]
with commuting Weyl books
\[
L_1=\langle Z_2,\ldots,Z_n\rangle,\quad
L_2=\langle X_1,X_3,\ldots,X_n\rangle,
\]
\[
L_3=\langle Z_1,X_2,Z_4,\ldots,Z_n\rangle.
\]
Their span contains every canonical X_i and Z_i, so products of one book element from each region reach every Weyl label in the full n-party operator algebra.

Compatibility with honest reduced density matrices is constructed rather than assumed. Choose nondegenerate Hermitian H_i in each MASA with zero partial trace over every local site of its support, and set
\[
\rho=I/d+\epsilon(H_1+H_2+H_3).
\]
When reduced to R_i, every other H_j is killed by tracing the one site in R_j\R_i; for sufficiently small epsilon the global state is faithful and the three reduced spectral books are exactly the chosen ones. Nondegeneracy and the spanning minor persist under perturbation.

Thus there exists an open faithful family with depth-three audit completeness for every n>=3 and q>=3. This is an existence theorem, not a claim about every state.

## 2. The modular-flow firewall

The previous packet identified the folded standard-form Tomita conjugation with the base W33 anti-symplectic mirror. Continuous modular flow behaves differently:
\[
\sigma_t(P)=\rho^{it}P\rho^{-it}.
\]

If sigma_t maps every projective Pauli ray into the finite W33 Pauli-ray set for all t in an interval, continuity forces the induced finite permutation to be constant. At t=0 it is the identity, so sigma_t(P)=c_P(t)P. For qutrit Paulis P^3=I, hence c_P(t)^3=1; continuity forces c_P(t)=1. The full Pauli algebra then commutes with rho, so rho is scalar.

Therefore the only continuous modular flow that stays entirely inside W33 automorphisms is the trivial tracial flow. The nontrivial Ledger clock, if physical, must live in a continuous operator layer over the finite W33 skeleton rather than as motion inside PSp(4,3) or PGSp(4,3).

## 3. Explicit all-q simple-homotopy collapse

Prior ownership:
- archive/exploratory/w33_aspherical.py and archive/exploratory/w33_free_pi1_analysis.py own q=3: pi_1=F_81, bouquet of 81 circles.
- archive/exploratory/w33_generalization.py states the all-q bouquet pattern.
- Pass 1448 later records the q=3 bouquet in the active analysis line.

The new certificate gives a direct elementary collapse. Every positive-dimensional clique lies in one unique isotropic line, a q-simplex on q+1 point vertices. Fix one point of that simplex as center. Pair every face F not containing the center, with |F|>=2, to F union {center}, processing larger faces first. This is an elementary-collapse sequence and leaves precisely the q-edge star.

Distinct line simplices meet only at point vertices, so all line collapses are independent. With
\[
n=(q+1)(q^2+1)
\]
points/lines, the collapsed connected graph has n vertices and nq edges. Therefore
\[
\operatorname{rank}\pi_1=nq-n+1=q^4
\]
and
\[
K(W(3,q))\simeq_s\bigvee^{q^4}S^1,\qquad \pi_1=F_{q^4}.
\]

For q=3 the full clique complex collapses in exactly 160 elementary pairs to a 40-vertex, 120-edge graph of cycle rank 81.

## 4. Winding is exact — and radically underselective

The free-group theorem makes the Ledger winding sector precise:
\[
\pi_1=F_{q^4},\qquad F_{q^4}^{ab}=\mathbb Z^{q^4}.
\]
Flat abelian holonomies are
\[
\operatorname{Hom}(F_{q^4},U(1))=U(1)^{q^4}.
\]
For W33 this is an 81-dimensional torus. Even forcing ternary holonomy leaves
\[
|\operatorname{Hom}(F_{81},\mathbb Z_3)|=3^{81}
=443426488243037769948249630619149892803.
\]

So winding is a genuine topological carrier, but winding alone cannot select the observed matter/charge spectrum. A symmetry quotient, action/energy, anomaly constraint, or other selector is mathematically necessary. The positive bridge is that the abelianized winding channel is exactly the certified 81-dimensional H1 sector.

## 5. Auxiliary Weinberg contact: a narrower radiative upgrade

The algebraic auxiliary candidate is
\[
\mathcal L_{\rm aux}=\frac M2 NN+yN(LH)+\mathrm{h.c.}
\]
with no kinetic term for N. Its equation of motion is algebraic,
\[
N=-\frac yM(LH),
\]
giving
\[
\mathcal L_{\rm eff}=-\frac{y^2}{2M}(LH)(LH)+\mathrm{h.c.}
\]
with a local inverse kernel 1/M, not a propagating heavy pole.

This removes the ordinary propagating-heavy-neutrino threshold graph by construction. Brivio and Trott's type-I seesaw matching explicitly contains a one-loop Higgs-potential threshold when the heavy Majorana field propagates. Separately, JHEP 06 (2023) 123, Renormalisation of SMEFT bosonic interactions up to dimension eight by LNV operators, reports that two Weinberg insertions feed higher-dimensional bosonic operators and do not directly renormalise the renormalisable bosonic coefficients at order 1/Lambda^2 in dimensional regularisation.

That upgrades the candidate from tree-level only to no ordinary heavy-pole threshold and EFT-safe through the cited order. It still does not solve the UV problem: a completion that generates this auxiliary structure may reintroduce propagating states or threshold sensitivity.

## Three-level conjugation synthesis

Pass 1900 already proved that the outer Z/2 of PSp(4,3):2 acts as complex conjugation precisely on complex-type irreducible characters. The newer Tomita fold says
\[
J L_AJ=R_{A^\dagger}\xrightarrow{\mathrm{transpose\ fold}}L_{\bar A},
\]
and on Weyl labels
\[
(x_A,x_B,z_A,z_B)\mapsto(x_A,x_B,-z_A,-z_B).
\]
Thus the same outer coset has a consistent reading at three levels: algebra-to-commutant conjugation, qutrit phase-space conjugation, and representation-ring complex conjugation. The firewall is equally clear: state dependence lives in Delta_rho, not in 540 different standard-form J operators.
