# Pass 10975 — The native E6 cubic contains the clock selector

Producer: `analysis/w33_pass10975_e6_cubic_reynolds_clock_weld.py`
Certificate: `data/w33_pass10975_e6_cubic_reynolds_clock_weld.json`
Regression: `tests/test_w33_pass10975_e6_cubic_reynolds_clock_weld.py`

## Result

Pass 10972 left one sharp missing weld: the clock augmentation module was known
abstractly as the standard three-dimensional representation of
[
S_4=PGL_2(3)=W(A_3),
]
but it had not been embedded objectwise into the 27-coordinate carrier of the
signed (E_6) cubic.

That embedding now exists.
Write a current (H_{27}) address as ((a,b,c)).
The three addresses with ((a,b)=(0,0)) form the central fibre.
The other 24 coordinates split canonically into four six-point fibres according
to the projective direction
[
[a:b]inmathbf P^1(mathbf F_3).
]
Their four indicator vectors span the permutation module
[
mathbf 1oplus V_3,
]
and the zero-sum subspace (V_3) is exactly the clock augmentation module of
Passes 10971–10972.

This is objectwise, not a dimension match. All 48 elements of (GL_2(3)) have
a unique (H_{27}) automorphism lift preserving the selected five cubic
direction classes, and their projective action on the four six-point fibres is
the same 24-element (S_4) action already certified on the temporal null,
Hesse-striation and (4A_2) clock carrier.
The scalar matrix (-I) is a useful firewall. It is nontrivial on the
27-coordinate carrier, with cycle shape
[
1^3,2^{12},
]
but acts trivially on the four fibre indicators. Thus the fibre module really
does factor through (GL_2(3)/{pm I}=S_4).

## The signed-gauge obstruction

The 45 cubic triads split as
[
9+9+9+9+9
]
over the four projective directions plus the central direction. The central
nine are exactly the already-certified firewall bad-nine spread.

At support level the full (GL_2(3)) action is exact. At signed-coefficient
level it is not: among the 48 support permutations, **only the identity**
preserves the frozen signed cubic by a bare coordinate permutation.
This is not a contradiction with the earlier cubic symmetry packets. For every
one of the 48 support operations, the binary sign-repair system has
[
operatorname{rank}=21,qquad operatorname{nullity}=6,
]
hence exactly
[
2^6=64
]
diagonal sign repairs.

So the correct statement is:

> the clock symmetry is native to the cubic **support**, while the frozen cubic
> coefficient gauge realizes it only projectively/monomially.

This distinction turns out to matter for the dynamical weld.
## Restrict the actual cubic

Set the three central coordinates to zero. On each of the four noncentral
six-point fibres, set every coordinate equal to one clock amplitude (y_i).

Exactly 32 of the 45 signed cubic triads survive. Before symmetrization their
coefficient pattern is not (S_4)-invariant; the four cube coefficients have
multiset
[
{-2,-2,0,0},
]
and the four distinct-triple coefficients have multiset
[
{-2,-2,4,4}.
]

So the naive statement “the (E_6) cubic simply restricts to the clock cubic”
is false.
## Reynolds projection

Now apply the finite-group Reynolds operator for the exact clock support action:
[
mathcal R(D)=rac1{24}sum_{sigmain S_4}sigmacdot D.
]

The executable calculation gives
[
oxed{
mathcal R(D)
=
-sum_{i=1}^4 y_i^3
+sum_{1le i<j<kle4}y_i y_j y_k
}.
]

Write
[
p_3=sum_i y_i^3,qquad
e_3=sum_{i<j<k}y_i y_j y_k.
]
Then
[
mathcal R(D)=-p_3+e_3.
]
On the clock augmentation hyperplane
[
p_1=sum_i y_i=0,
]
Newton's identity gives (p_3=3e_3). Therefore
[
oxed{
mathcal R(D)ig|_{V_3}
=
-rac23,p_3.
}
]

That coefficient is exact in the frozen cubic normalization.

This closes the representation-theoretic target left open by Pass 10972:
the native signed (E_6) cubic has a **nonzero invariant component** on the
exact clock augmentation module, and that component is necessarily the same
tetrahedral cubic that selects the four (S_4/S_3) clock vacua.
## What this means

The status has changed from

> “find some W33 cubic that could act on the clock order parameter”

to

> “the existing (E_6) cubic already projects onto the unique clock cubic,
> with coefficient (-2/3); explain dynamically why the invariant component
> is selected.”

That is a substantially narrower dynamics problem.

If an effective theory equilibrates, averages or otherwise projects over the
exact clock-support (S_4), then no new cubic anisotropy has to be invented:
the tetrahedral selector is already present in the native interaction.
## Prior-art boundary

Finite-group Reynolds averaging is classical invariant theory: the Reynolds
operator is the group average projecting a polynomial onto its invariant
component. Likewise (S_4=W(A_3)) and its degree-three invariant on the
standard representation are classical.

The new repository content is the explicit objectwise weld:

1. four projective clock directions (leftrightarrow) four six-point fibres
   inside the current 27-coordinate (E_6/H_{27}) carrier;
2. all 48 exact (GL_2(3)) support lifts and their (S_4) projective action;
3. the complete signed-gauge obstruction/repair census;
4. the exact restriction of the frozen signed (E_6) cubic;
5. its nonzero Reynolds component (-rac23p_3) on the clock augmentation
   module.
Useful general reference for the averaging construction: B. Sturmfels,
*Algorithms in Invariant Theory*, 2nd ed. (Springer, 2008).

## Boundary

The Reynolds operator is a mathematically canonical projection, **not** a
derived physical time-averaging mechanism. This pass does not derive an energy
scale, a continuum field, a vacuum, or a Hamiltonian implementing that
projection.

The raw frozen signed cubic is not itself (S_4)-invariant on the
fibre-constant subspace. Any physical TOE claim now has to explain why the
(S_4)-invariant component is dynamically selected—or replace the simple
fibre-constant field by a larger signed-equivariant order parameter.
