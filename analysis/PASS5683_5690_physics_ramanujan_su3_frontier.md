# Passes 5683–5690 — Ramanujan refinement, affine orientation, and the first exact `su(3)` bracket on the vertical eight

This packet executes the five physics continuations left open by Pass5675–5682 plus three deliberately high-risk probes. The central theme is sharper than the starting prompt: several structures that were previously only dimension matches now either acquire an exact operator/algebraic mechanism or fail under the relevant structure test.

## Pass 5683 — the W33 Levi graph is already Ramanujan, so an infinite good 2-lift tower exists

The W33 point-line Levi graph has 80 vertices, 160 edges, degree four, and exact adjacency spectrum

\[
\boxed{\pm4^1\oplus\pm\sqrt6^{24}\oplus0^{30}}.
\]

For a four-regular graph the Ramanujan threshold is

\[
2\sqrt{d-1}=2\sqrt3.
\]

Since

\[
\sqrt6<2\sqrt3,
\]

the Levi graph is a bipartite Ramanujan graph.

This lets us import a precise external theorem rather than extrapolate from numerical search: the Marcus–Spielman–Srivastava 2-lift theorem implies that every regular bipartite Ramanujan graph has a regular bipartite Ramanujan 2-lift. Iteration therefore gives an **existential infinite 4-regular Ramanujan 2-lift tower rooted at the W33 Levi graph**. Every level can keep all nontrivial adjacency eigenvalues inside

\[
[-2\sqrt3,2\sqrt3],
\]

so its combinatorial Laplacian gap is bounded below by

\[
\boxed{4-2\sqrt3\approx0.535898.}
\]

This directly repairs the Pass5678 bottleneck at the existence level.

The verifier also contains an explicit first-level locally balanced signing: 80 of the 160 Levi incidences are negative and **every Levi vertex sees exactly two negative edges**. Its signed spectral radius is approximately

\[
\boxed{3.28376887568<2\sqrt3},
\]

so the corresponding 160-vertex 2-lift is connected and Ramanujan.

The theorem boundary is important. MSS gives existence at every subsequent level, not a canonical signing selected by W33. The repo now has one explicit good first lift and an existential infinite good tower.

## Pass 5684 — the collision projector is exactly the support mask of the old `L_infinity` firewall

The old E8/firewall chain deleted nine cubic supports from the 45 E6 cubic triads and repaired the induced Jacobi anomaly through higher-bracket/L∞ machinery. Pass5676 independently introduced the gauge-invariant same-fiber collision observable

\[
\mathcal C(T)=\sum_b\binom{n_b(T)}2.
\]

The horizontal/vertical decomposition gives

\[
\mathcal C=0\quad\text{on all 36 horizontal affine lifts},
\]

and

\[
\mathcal C=3\quad\text{on all 9 vertical full fibers}.
\]

Therefore the normalized collision operator is literally the firewall deletion bit:

\[
\boxed{\delta_{\rm fw}(T)=\frac{\mathcal C(T)}3.}
\]

Equivalently, the cubic portion of the firewall bracket is

\[
\boxed{l_{2,\rm fw}=P_Hl_{2,\rm cubic},\qquad P_H=I-\frac{\mathcal C}{3}.}
\]

This is stronger than saying the two constructions produce the same count. They are the same support projector.

But the next tempting simplification is false. The Jacobiator contains two nested copies of `l2`, so under `l2 -> l2-D` it produces retained/deleted cross terms as well as a `D-D` contribution. The L∞ `l3` repair is therefore **not simply proportional to the scalar collision observable**. The collision projector identifies exactly which cubic supports are removed; the full Jacobi tensor contains compositional information beyond that support mask.

## Pass 5685 — geometric locality and flat bonds discretely protect the magnetic ratio `2`

Pass5675 proved that the full stabilizer-equivariant, particle-hole-compatible deck-odd Hamiltonian cone is four-real-dimensional and equivalent to `Herm_2` on the multiplicity space. Symmetry alone therefore leaves one continuous absolute level ratio after overall scaling.

The missing constraints were already visible in the intrinsic magnetic carrier itself.

Write

\[
H=iS,
\]

with `S` real skew. Among the 120 undirected pairs of the 16 carrier events, the magnetic operator has

\[
\boxed{60\text{ zero bonds}+60\text{ nonzero bonds}},
\]

and every nonzero bond has the same absolute magnitude.

Impose two geometric conditions on the four-dimensional equivariant cone:

1. preserve exactly the magnetic zero/nonzero support pattern;
2. require constant absolute magnitude on every surviving bond.

The first condition cuts the four-real-dimensional cone to dimension two. The second reduces that projective line to exactly

\[
\boxed{2\text{ real projective rays}.}
\]

Both rays have spectrum

\[
\boxed{-2a^4\oplus-a^4\oplus a^4\oplus2a^4}
\]

where the superscript denotes multiplicity four on each level. Hence both satisfy

\[
\boxed{\frac{|\lambda_{\rm high}|}{|\lambda_{\rm low}|}=2.}
\]

One ray is the intrinsic magnetic Hamiltonian. The other differs, up to global sign, on 12 of the 60 bond signs and has normalized correlation `0.6` with the magnetic ray.

Thus the correct statement is now:

\[
\boxed{\text{symmetry alone does not fix }2,\quad\text{but symmetry+local support+flat bonds does.}}
\]

A discrete two-ray sign/chirality ambiguity remains. This is a finite spectral theorem, not a physical fermion-mass assignment; no dimensional energy scale or particle labels are supplied.

## Pass 5686 — breaking `AGL(2,3)` only by affine orientation produces an exact compact `su(3)`

Pass5681 established the exact vertical-site module

\[
\mathbb C^9=\mathbf1\oplus V_8
\]

for the full affine group

\[
AGL(2,3),\qquad |AGL(2,3)|=432,
\]

and proved

\[
\operatorname{Hom}_{AGL(2,3)}(\Lambda^2V_8,V_8)=0.
\]

So the eight-dimensional augmentation space is not an `su(3)` adjoint while the full affine symmetry is preserved.

The new subgroup scan enumerates every linear subgroup of `GL(2,3)`. There are 55 in total. The unique subgroup of order 24 is

\[
SL(2,3).
\]

Consequently the largest proper affine subgroup is

\[
ASL(2,3)=\mathbb F_3^2:SL(2,3),\qquad |ASL(2,3)|=216.
\]

At exactly this index-two orientation-preserving reduction,

\[
\boxed{\dim\operatorname{Hom}_{ASL(2,3)}(\Lambda^2V_8,V_8)=1.}
\]

The unique bracket has an elementary finite-affine formula. For sites `x,y,z in F_3^2`, define

\[
\phi(x,y,z)=\operatorname{sgn}_3\det(y-x,z-x),
\]

where

\[
\operatorname{sgn}_3(0)=0,\qquad
\operatorname{sgn}_3(1)=+1,\qquad
\operatorname{sgn}_3(2)=-1.
\]

On the zero-sum real site space `V8`, define the alternating bracket by

\[
\boxed{
\langle[f,g],h\rangle
=\sum_{x,y,z}\phi(x,y,z)f(x)g(y)h(z).
}
\]

The verifier checks, with integer arithmetic:

- all 216 elements of `ASL(2,3)` preserve `phi`;
- a determinant-two affine transformation reverses `phi` and hence the bracket sign;
- Jacobi is exactly zero on all `8^3` augmentation-basis triples;
- the Killing form on `V8` is exactly

\[
\boxed{K=-54I_8.}
\]

The Killing form is nondegenerate and negative definite, so this is an eight-dimensional compact semisimple real Lie algebra. Its complexification is the unique eight-dimensional semisimple type `A2`; hence, up to overall bracket scale,

\[
\boxed{V_8\cong\mathfrak{su}(3).}
\]

This is the strongest physics-facing result of the packet, and its firewall must be equally strong. It does **not** derive QCD. It shows that the previously observed affine `8` admits an exact compact `su(3)` Lie bracket once an affine orientation/chirality is selected, while determinant-reversing affine transformations flip the bracket. A physical gauge interpretation still requires a Yang–Mills kinetic term, coupling normalization, matter representation, and a dynamical explanation for the orientation choice.

## Pass 5687 — a Ramanujan cover tower is a good network but a bad naive spacetime graph

If a cover level doubles the number of cells,

\[
N_{n+1}=2N_n,
\]

and one **assumes** those cells refine a fixed physical `d`-dimensional volume, uniform cell length must scale as

\[
\boxed{\frac{\ell_{n+1}}{\ell_n}=2^{-1/d}.}
\]

Pass5624 gives the split-step continuum conversion

\[
c=\frac{\ell}{\tau}.
\]

Keeping one physical causal speed therefore requires

\[
\boxed{\frac{\tau_{n+1}}{\tau_n}=2^{-1/d}.}
\]

If the split-step parameter `a` scales with the same refinement, its first-order finite-step anisotropy also decays by `2^{-1/d}` per level.

But Pass5683 changes how this should be interpreted. A Ramanujan tower has a uniform normalized spectral gap and therefore a nonvanishing conductance lower bound. It is an expander. In contrast, a local fixed-dimensional manifold refinement has large macroscopic regions whose boundary-to-volume ratio becomes small as resolution increases.

So the raw Ramanujan graph metric should **not** be declared emergent physical space. Its natural role is an internal routing/state/refinement network unless an additional embedding/local metric is supplied.

This simultaneously preserves the usefulness of the good cover tower and strengthens the earlier speed-of-light firewall: neither physical dimension, absolute edge length, nor clock duration is fixed by the cover topology.

## Pass 5688 — the single-chord bottleneck was a pathological signing, not generic `H^1`

Three explicit signings were compared on the same 160-edge Levi graph.

The Pass5678-style single negative chord gives signed spectral radius

\[
\rho_\sigma\approx3.973117,
\]

far outside the Ramanujan new-eigenvalue threshold.

The locally balanced two-factor witness from Pass5683 gives

\[
\rho_\sigma\approx3.283769.
\]

A second exactly-half-negative spectral-search witness gives

\[
\rho_\sigma\approx3.198157.
\]

Both satisfy

\[
\rho_\sigma<2\sqrt3.
\]

A deterministic baseline of 256 random exactly-half-negative signings found 246 below the Ramanujan threshold. The single-chord bottleneck is therefore a highly sparse/pathological corner of the voltage space, not evidence that generic nontrivial cohomology destroys expansion.

No finite search establishes global optimality. Infinite good-tower existence comes from Pass5683's use of the MSS theorem, not from repeatedly applying either hard-coded witness.

## Pass 5689 — ordinary Pauli exclusion does not explain the bad9

The fermionic analogy was tested at the correct level.

Let

\[
W=\bigoplus_{b=1}^9W_b,
\qquad \dim W_b=3,
\]

be the 27 resolved fiber modes. In the ordinary fermionic exterior algebra `Lambda^3 W`, a vertical full-fiber support is

\[
\boxed{e_{b,0}\wedge e_{b,1}\wedge e_{b,2}\ne0.}
\]

The three internal modes are distinct, so Pauli exclusion does not remove the bad9.

If, however, one first imposes the Pass5676 hard-core quotient that collapses each fiber to one base occupancy mode,

\[
W\longrightarrow\mathbb C^9,
\]

then a vertical triple becomes

\[
e_b\wedge e_b\wedge e_b=0,
\]

while every horizontal support uses three distinct base fibers and survives.

Therefore exterior algebra reproduces exactly the 36/9 collision selector **only after the same one-occupancy-per-fiber quotient is imposed**. Standard fermionic antisymmetry on the full 27 modes is insufficient. This is a useful negative result: the hard-core principle is not secretly just Pauli exclusion.

## Pass 5690 — the deck16 Hamiltonian cone has synthetic Berry charge `|c1|=8`

Remove the scalar part of the `Herm_2` multiplicity matrix and normalize its traceless part:

\[
X(\mathbf n)=n_x\sigma_x+n_y\sigma_y+n_z\sigma_z,
\qquad \mathbf n\in S^2.
\]

Thus the normalized nondegenerate traceless multiplicity Hamiltonians form a Bloch sphere.

In the projector-curvature convention used by the verifier, the lower and upper two-level eigenlines have

\[
c_1(L_-)=+1,\qquad c_1(L_+)=-1.
\]

The full deck16 normal form is

\[
H(\mathbf n)=I_A\otimes X(\mathbf n)
\oplus
I_{\bar A}\otimes[-\overline{X(\mathbf n)}].
\]

Complex conjugation reflects the parameter sphere,

\[
R(n_x,n_y,n_z)=(n_x,-n_y,n_z),\qquad\deg R=-1.
\]

The negative-energy rank-eight bundle is therefore

\[
E_-=A\otimes L_-
\oplus
\bar A\otimes R^*L_+,
\]

and, since `dim A=4`,

\[
\boxed{c_1(E_-)=8}
\]

in the fixed convention, with orientation-independent magnitude

\[
\boxed{|c_1|=8.}
\]

A direct projector-curvature integration returns `c1(L_-)=1.000002...`, numerically confirming the analytic line-bundle calculation.

This is a Berry invariant over a **synthetic Hamiltonian-parameter sphere**. It is not a Brillouin-zone invariant, not a 2D topological material phase, and not evidence for eight particles or eight gauge bosons.

## Overall physics boundary

The promoted results are finite graph-spectrum, representation, Lie-bracket, support-projector, exterior-algebra, Berry-bundle, and conditional scaling statements.

The Ramanujan 2-lift theorem and discrepancy/2-lift framework are external prior art. Finite Hessian/`SU(3)` subgroup theory is also external prior art. The repo-specific results are the exact W33 Levi input and explicit balanced witness, the collision/firewall operator identity, the two-ray flat-bond classification, and the exact oriented `AG(2,3)` augmentation bracket with Jacobi/Killing certificate.

Nothing in this packet proves physical QCD, a Yang–Mills action or coupling, a Standard Model mass assignment, an absolute energy scale, a Lorentz-invariant spacetime limit, the SI value of `c`, a dynamical affine-orientation selector, or a canonical explicit infinite sequence of Ramanujan signings.
