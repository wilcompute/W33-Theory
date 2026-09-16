# Pass 2026-09-15 — execute-all-five Pauli / Cartan / glue / rank-24 closure

Status: **PASS**, with one deliberately preserved heterotic boundary.

This pass executes the five follow-ups to the exact E8 -> two-qutrit Pauli grading closure.  The computations are separated into machine-readable certificates so that group-theoretic, Lie-theoretic, lattice-VOA, and heterotic statements do not borrow strength from one another.

## 1. The explicit E8 -> Pauli lift is now fully materialized

`data/w33_e8_pauli_cocycle_lift.json` plus the four `...entries_00..03.json` shards now contain all 80 oriented A2 root-orbit generators and their actual 9x9 tensor-qutrit Pauli monomials.  The verifier `analysis/w33_e8_pauli_cocycle_lift_shard_verify.py` checks that the shards cover orbit indices 0..79 exactly once, contain all 80 nonzero F3^4 degrees, and agree with the core PASS certificate.

The exact Lie map remains

\[
\Phi(E_v)=\frac{\zeta_{12}^{m_v}}{\sqrt3}
\left(X^{x_1}Z^{z_1}\otimes X^{x_2}Z^{z_2}\right),
\]

with all 2160 nonzero brackets matched after the solved phase rescaling.

## 2. The E8 Weyl normalizer is the extended Pauli grading symmetry

Certificate: `data/w33_e8_pauli_normalizer.json`.

For the canonical Coxeter element `c` and `g=c^10`,

- `|W(E8)| = 696729600`;
- `|C_W(E8)(g)| = 155520`;
- an explicit length-14 simple-reflection word gives an involution `h` with `hgh^{-1}=g^{-1}`;
- `|N_W(E8)(<g>)| = 311040`;
- on the 80 oriented Pauli degrees, the centralizer image has order `51840` and the normalizer image has order `103680`;
- the kernel is exactly `<g>` of order 3;
- the centralizer generators are symplectic and `h` is anti-symplectic.

Hence

\[
C_{W(E_8)}(g)/\langle g\rangle\cong Sp(4,3),
\]

and the full normalizer induces its index-two anti-symplectic extension.

## 3. Every W33 line is an sl9 Cartan

Certificate: `data/w33_pauli_cartans.json`.

A W33 line is a Lagrangian two-space in F3^4.  Its four projective points are eight oriented nonzero Pauli degrees.  Their symplectic pairings vanish, so the eight homogeneous Pauli generators commute.  They are finite-order semisimple matrices and span dimension 8, equal to `rank(sl9)`.  Therefore every W33 line gives a Cartan subalgebra of `sl9`.

All 40 lines give 40 Cartans.  Among the 780 pairs,

- 240 pairs intersect in dimension 2 (one projective Pauli point, i.e. degrees `+-v`);
- 540 pairs are disjoint.

The graph joining Cartans with nonzero intersection is itself `srg(40,12,2,4)`, i.e. W33 again by point-line self-duality.

## 4. The A8^3 Niemeier coupling is center-charge glue, not diagonal Pauli identification

Certificate: `data/w33_a8_cubed_niemeier_glue.json`.

The Niemeier extension of `A8^3` uses the subgroup

\[
C=\langle(1,1,4),(1,4,1),(4,1,1)\rangle\le (\mathbb Z_9)^3,
\]

with

\[
|C|=27,\qquad C\cong \mathbb Z_9\times\mathbb Z_3.
\]

It is totally isotropic for the discriminant quadratic/bilinear form and invariant under permutation of the three A8 factors.  Its nonidentity conformal ground weights are exactly

- 18 sectors at weight 2;
- 8 sectors at weight 3.

There are no weight-one glue fields.  Thus the weight-one algebra remains `sl9^3`; the first genuine cross-factor operators occur at weight 2.  For example `(1,1,4)` has finite ground representation

\[
9\otimes9\otimes\Lambda^4 9
\]

of dimension `10206` and vertex-operator form

\[
V_{[1,1,4]}\sim
\exp i(\langle\lambda_1,\phi_1\rangle+
       \langle\lambda_1,\phi_2\rangle+
       \langle\lambda_4,\phi_3\rangle).
\]

The glue constrains the three SU(9) **center/simple-current charges**.  It does not identify the three F3^4 adjoint Pauli labels: adjoint Pauli currents have center charge zero.  The three two-qutrit systems therefore remain independent at weight one and are coupled by higher-weight center-charge sectors.

## 5. E8^3 and Leech have the same six-qutrit register but different shells

Certificate: `data/w33_e8cubed_leech_six_qutrit_register.json`.

Both fixed-point-free order-three rank-24 twists have characteristic polynomial `Phi_3^12`.  Therefore both have

- quotient `F3^12` of order `3^12=531441`;
- symplectic geometry `W(11,3)`;
- `265720` projective Pauli classes;
- twisted ground weight `4/3`;
- a `729=3^6` dimensional irreducible Heisenberg register of shape `3^(1+12)`.

By finite Stone-von Neumann, once a symplectic identification of their F3^12 quotients is chosen, the ground registers are equivalent as six-qutrit Heisenberg modules.

Their distinguished lattice shells are emphatically different.

For E8^3 the visible root shadow is the union of three mutually orthogonal embedded W33s: 240 oriented degrees / 120 projective points.  The full projective W(11,3) partitions by block support as

\[
120+9600+256000=265720.
\]

A shadow point has 92 shadow neighbours, while outside points of support two and three see respectively 66 and 39 shadow points.  Thus this 120-set is not a tight set.

For Leech, the certified p=3 minimal shell contains 196560 minimal vectors, three per hit nonzero quotient class, giving 65520 oriented classes and 32760 projective points.  This is the 90-tight `2.Suz` orbit, occupying exactly `9/73` of W(11,3).

So there is no shell-preserving symplectic identification: the common object is the **six-qutrit register kinematics**, while the ambient lattice chooses a radically different shell and orbifold extension (`E8^3 -> A8^3` versus Leech -> moonshine).

## Heterotic cross-track result

The two finite-geometric follow-ups were pushed to Holotrade rather than duplicated here:

- `30e1bef2`, `bb621ce4`: all 240 two-Cartan hinges form one `PSp(4,3)` orbit; all 2160 hinges decorated by one outer point on each Cartan form one orbit.  The frozen net-three witness is in this unique orbit, so bare hinge incidence is not a selector.
- `4a9e8f38`, `e45dbc44`: the frozen three-family SU(5) witness has the canonical SU(5) hypercharge embedding `Y^2=5/6`, hence `k_Y=5/3`, with 3 chiral tens, net 3 anti-fives and nine SU(5)-vectorlike `5+5bar` pairs.  However none of its 405 weighted massless states has an exact opposite under the full rank-16 Cartan.  The extra pairs therefore carry spectator charges and are not yet certified removable by a direct mass term.  Actual level-1 GUT breaking and exotic removal remain open.

## Boundary

This pass materially tightens the algebraic and lattice-VOA bridge.  It does **not** turn the heterotic model into a completed Standard Model vacuum and does not constitute a physical theory-of-everything derivation.  In particular, a dynamical GUT-breaking mechanism, allowed singlet couplings, and full exotic lifting remain open.
