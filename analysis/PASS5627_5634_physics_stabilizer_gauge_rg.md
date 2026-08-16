# Passes 5627–5634 — signed stabilizers, the E6 gauge-action no-go, and finite sheet RG

This packet executes the five physics continuations from Pass5619–5626 plus three deliberately high-risk probes.  The dominant outcome is not a new phenomenological fit.  It is a sharper separation of which structures are genuinely forced by the finite geometry and which tempting physical readings fail once the correct symmetry/action is imposed.

## Pass 5627 — the signed 16 is spinorial only for the carrier stabilizer

The 16 Segre events are not a `PSp(4,3)`-invariant carrier.  Direct generation from symplectic transvections gives

- `|PSp(4,3)| = 25920`,
- setwise stabilizer of the Segre 16: `48`,
- `|Sp(4,3)| = 51840`,
- vector preimage stabilizer: `96`.

On the deck-odd basis the central `-I` in `Sp(4,3)` acts as

\[
\boxed{-I_{16}}.
\]

The signed character has value distribution

\[
16^1,\quad (-16)^1,\quad 4^8,\quad (-4)^8,\quad 0^{78},
\]

and self-inner-product `8`.

This is a genuine finite double-valued/central-sign representation of the **96-element vector carrier stabilizer**.  It cannot descend to `PSp(4,3)`.  Consequently it cannot be either Pass332 D5 half-spin 16: those are ordinary `PSp(4,3)` modules, whose pullback to `Sp(4,3)` has central `-I` in the kernel.

So the dimension-16 coincidence is now closed structurally rather than left suggestive.

## Pass 5628 — gauge invariance does not kill the E6 vertical nine

Pass5620 proved that the 45 E6 cubic supports split into

\[
36\ \text{horizontal covariantly-affine line lifts}
\quad\sqcup\quad
9\ \text{complete vertical }\mathbb Z_3\text{ fibers}.
\]

Writing the actual local bundle gauge action reveals the next obstruction.  A gauge translation `t -> t+s_b` transports the horizontal connection and its 36 cubic monomials covariantly, but the vertical support

\[
\{(b,0),(b,1),(b,2)\}
\]

is itself setwise invariant.  Therefore gauge symmetry permits

\[
\boxed{
S_{\rm cubic}
=g_H\sum_{T\in H_{36}} C_T
+g_V\sum_{b=1}^{9}V_b .
}
\]

Neither local `Z3` covariance nor the neutral total charge from Pass5618 forces `g_V=0`.

This removes an attractive but false mechanism: the bad9 are geometrically vertical gauge fibers, but **being a gauge fiber does not make the corresponding cubic vanish**.  The selector must come from an additional horizontal/locality principle, the already-known `L_infinity`/Jacobi obstruction, representation theory, or a dynamical action that sets the vertical coupling to zero.

## Pass 5629 — the obvious connected C2 continuum tower dies after one lift

The exact Pass4719 270-vertex regular closure is the bipartite/Kronecker double cover of selected135.  It is connected, 12-regular, and has spectrum

\[
12^1,6^{30},3^{44},0^{120},(-3)^{44},(-6)^{30},(-12)^1.
\]

Trying to iterate the same construction gives the exact identity

\[
(G\times K_2)\times K_2
=G\times(K_2\times K_2)
=2\,(G\times K_2).
\]

Equivalently, the second lift has top adjacency eigenvalue 12 with multiplicity two, hence two connected components.  Its distinct eigenvalue set is unchanged.

Thus the existing parity/Kronecker class **cannot** be the missing connected refinement hierarchy, and no Weyl exponent can be extracted from repeatedly applying it.  The separate repo cover `810 -> 1620` is not a certified child of this 270 carrier.  A real tower needs a new nontrivial voltage/cohomology class at every level.

## Pass 5630 — the magnetic 16 is `2A + 2 Abar`, and the ratio 2 is not protected

Resolving the four magnetic eigenspaces under the exact 96-element vector stabilizer gives irreducible four-dimensional modules with pattern

\[
\begin{array}{c|cccc}
h&-6&-3&3&6\\\hline
\text{module}&A&\overline A&A&\overline A.
\end{array}
\]

Hence

\[
\boxed{V_{16}\cong 2A\oplus2\overline A}
\]

with `A` non-real, and

\[
\boxed{\dim_{\mathbb C}\operatorname{End}_G(V)=8}.
\]

The real commutant splits into four symmetric and four skew directions.  Since a `K`-odd Hermitian perturbation is `i` times a real skew-symmetric commuting matrix, there are

\[
\boxed{4}
\]

real symmetry-allowed particle-hole-compatible Hamiltonian directions.

An explicit Reynolds-averaged perturbation preserves the entire carrier stabilizer and `K H K^{-1}=-H` but moves the positive levels at probe `epsilon=0.1` to approximately

\[
3.0793013,\qquad6.0793013,
\]

so the ratio becomes

\[
\boxed{1.974247\ldots\neq2}.
\]

Therefore Pass5622's `6/3=2` is an exact property of the chosen intrinsic magnetic operator, **not a symmetry-protected mass prediction**.

## Pass 5631 — what the q=5 fixed line could map to if the F4 gate closes

There is a universal representation identity behind every `1+12` permutation action.  Let `f` be the fixed basis vector and `e_i` the moving twelve.  The centered 13-point module is

\[
\langle 12e_f-\sum_i e_i\rangle\oplus M_0,
\]

where `M_0` is the moving zero-sum 11-space.  The ordinary moving 12-point permutation module is

\[
\langle\sum_i e_i\rangle\oplus M_0.
\]

Therefore

\[
\boxed{
\operatorname{centered}(1+12)\cong\operatorname{Perm}(12)
}
\]

equivariantly, for the same moving action.

If the still-pending direct Pass5606 GAP conjugator proves that the q=5 moving12 action is the Latin/F4 short-root-pair action, the q=5 invariant direction

\[
12e_f-\sum e_i
\]

must map to the **constant vector** on the q=3 12-orbit.  It does not map to a singled-out q=3 projective point.  Moreover q=3 has two isomorphic 12-orbits exchanged by a quadratic-form similarity.

So even the strongest possible successful cross-q bridge gives a collective orbit-average singlet, not a unique physical vacuum point.

## Pass 5632 — no equivariant Kramers/Pin shortcut

The deck-odd Hamiltonian is purely imaginary Hermitian,

\[
H=iS,\qquad S^T=-S,
\]

and ordinary complex conjugation obeys

\[
KHK^{-1}=-H,\qquad K^2=1.
\]

This is precisely the algebraic Majorana/BdG form familiar from the standard free-fermion literature.  But a second antiunitary time reversal `T=UK` commuting with `H` would require

\[
UR_g=R_gU,
\qquad
UH+HU=0.
\]

The exact finite linear system has

\[
\boxed{\text{nullity}=0}.
\]

There is no nonzero stabilizer-equivariant `U`, hence no carrier-derived time reversal and in particular no `T^2=-1` Kramers structure.  In tenfold-way vocabulary the algebra is therefore **class-D-like**, not DIII-like, if one chooses to second-quantize it as a Majorana/BdG Hamiltonian.

This is not the relativistic spin-statistics theorem.

## Pass 5633 — the bad9 are in the wrong cochain degree to be gauge bosons

The reconstructed AG(2,3) base has 9 points and 12 affine lines.  Every pair of points lies on a unique line, so its full affine one-skeleton is

\[
K_9,\qquad E=36.
\]

For the oriented incidence map,

\[
\operatorname{rank}d_0=8,
\qquad
\dim Z_1=36-8=28.
\]

Thus the natural gauge complex has

- `C0`: 9 local gauge parameters, 8 nonconstant after the global mode;
- `C1`: 36 link variables;
- cycle space: 28.

The nine bad cubics are indexed by the nine **sites/fibers**, so their natural degree is `C0`, not connection `C1`.  A three-state fiber also Fourier-splits as `1 + chi + chibar`, giving `9+9+9` linear fiber modes.

The count `9` therefore points much more naturally to local gauge generators/constraints, site singlets, or vertical potential terms than to propagating gauge bosons.  The `bad9 = gauge bosons` count match is rejected by cochain degree.

## Pass 5634 — the old section Hamiltonian is the bare sheet block

In the intrinsic vector basis ordered by the two lifts, the magnetic Hamiltonian has exact form

\[
\boxed{
H_{32}=\begin{pmatrix}A&B\\B&A\end{pmatrix}},
\qquad
H_+=A+B,
\qquad
H_-=A-B.
\]

The diagonal block `A` is, up to the `omega <-> omega^2` complex-conjugation convention, exactly the old Pass5609 16-point section-dependent magnetic operator.  Its 16 eigenvalues have 15 distinct values.

Thus the Pass5613 correction receives a more precise interpretation: the old matrix was not an intrinsic projective observable, but it **is the bare Hamiltonian seen on one chosen sheet** of the intrinsic two-sheet theory.

Eliminating the opposite sheet gives the exact Feshbach/Schur operator

\[
\boxed{
H_{\rm eff}(E)=A+B(E-A)^{-1}B .
}
\]

The block commutator is nonzero, so this self-energy is not a scalar function that simply rescales `A`.  It has poles at the 15 distinct one-sheet energies and the large-energy expansion

\[
\Sigma(E)=\frac{B^2}{E}+\frac{BAB}{E^2}+\cdots .
\]

This is a genuine finite energy-dependent dressing/decimation flow.  It is not yet a Wilsonian spacetime RG, but it gives the first exact sense in which the nonintrinsic section operator is a **bare gauge choice** whose physics is repaired by integrating the second sheet back in.

## External boundary

The standard Majorana quadratic-Hamiltonian and tenfold-way language is prior art.  See `analysis/PASS5627_5634_external_prior_art.md`, especially Kitaev arXiv:0901.2686 and Schnyder–Ryu–Furusaki–Ludwig arXiv:0905.2029 / 0803.2786.  No novelty claim is made for that framework.

## Overall physics boundary

The packet proves finite group-action, module, bundle-gauge, graph-cover, cochain, BdG-algebra, and resolvent statements.  It does **not** derive relativistic spin-statistics, a Standard Model generation, physical fermion masses, a measured Yukawa coupling, physical gauge bosons, a continuum Weyl law, a Wilsonian fixed point, or an SI value of `c`.
