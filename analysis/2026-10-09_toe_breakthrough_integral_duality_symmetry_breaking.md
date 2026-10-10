# TOE frontier — a canonical **integral and isometric** bridge from the W33 clique/Hodge code to Levi gauge cycles

**9 October 2026.** Native W(3,3) geometry, not a new physical Theory of Everything.
This exploratory packet was chosen independently of Round20's engineering five-step list.
It compares the symmetry-preserving topological substrate with the minimal breaking
required to obtain a nondegenerate quadratic spectrum.

## Distinguish the prior art before claiming novelty

Already established in this repo:
- `analysis/w33_20260901_clique_h1_equals_building_steinberg.py`:
  complete 25,920-element **character equality** of rational clique-Hodge
  H1(81) and Levi building H1(81), so each is a Steinberg G-module.
- `analysis/w33_20260902_ternary_css_building_steinberg.py`: a **mod-3**
  reverse star map, chamber (p,L) -> sum_{q != p}[p->q], identifies the
  ternary W33 clique CSS H1 with Levi H1 by a complementary decomposition.
- `analysis/w33_pass11076_atlas_nerve_steinberg_chain_map.py`:
  local-E8 atlas H1 -> Levi H1, already chain-certified.
- `analysis/w33_pass11289_cycle_gram_gluing_flux.py`, Pass5031 and
  Pass5441: the exact Levi cycle Gram, spanning-tree determinant
  `10^23*4^30`, critical group `(Z/4)^6 + (Z/40)^22 + Z/160`, and
  Heegaard shear. **These orders are not discoveries of this packet.**
- Pass213/BT1688: order-three characters and irreducibility.

An independent full-character recomputation during this packet
agreed on all 25,920 elements, but it **reproduced existing work and
is deliberately not included as a fresh research claim**.

## 1. New canonical **integral** path map and exact harmonic isometry

Let K be the 40-vertex W33 collinearity **clique complex**,
L its 80-vertex point-line Levi graph, and M the integer matrix
of shape 160 flags x 240 oriented clique edges:

`M([p->q]) = [(p,L)] - [(q,L)]`,
where L is the unique isotropic line through collinear p,q.

All source oriented edges belong to a unique K4 line. For the integer
boundaries d1:Z^240->Z^40, d2:Z^160->Z^240 and D:Z^160->Z^80:
- `D M = J d1`, where J includes point vertices in Levi vertices.
- `M d2 = 0`.
- On each K4: M has image exactly the **saturated** rank-3
  sum-zero flag lattice and kernel the rank-3 triangle-boundary lattice.
- Every Levi cycle is already sum-zero on the flags at each line.
  A source integer lift follows by choosing an anchor in every line,
  and its clique boundary vanishes because its Levi image is a cycle.
  Therefore **H1(K;Z) canonically equals H1(L;Z)** via M,
  naturally and PSp(4,3)-equivariantly.

The source constructs all 240×160 integer coefficients, an explicit
fundamental cycle basis Z(160×81) with chord minor the identity,
and a 240×160 integral right lift R with `M R Z=Z`.
It checks six actual group transformations, including the
projective-symplectic similitude action.

A stronger **metric identity** is exact:
`M^T Z` lies in the kernel of the actual clique Hodge
`L1=d1^T d1 + d2 d2^T`; and

`(M^T Z)^T (M^T Z)=4 Z^T Z`, `M M^T Z=4Z`.

Hence `U=(1/2)M^T`, restricted from real Levi cycles to the
clique **harmonic** 81-space, is exactly an **isometric**
PSp-equivariant identification. Its inverse on the harmonic space
is `(1/2)M`. This is more constructive than character equality:
it normalizes the relative canonical Euclidean inner products.

The earlier characteristic-three reverse-star map is **exactly**
`Psi=M^T`. Its composite `M Psi=4I` on the Levi cycles
becomes `1I` modulo three, explaining WHY that previously certified
F3 injection is an inverse without invoking a mysterious modular coincidence.

## 2. The fourth power q^4 in the entire symplectic GQ family

The finite symplectic generalized quadrangle W(3,q) has
`P=L=(q+1)(q²+1)` points/lines and
`F=(q+1)^2(q²+1)` flags, so

`rank H1(Levi;Z) = F - 2P + 1 = (q²-1)(q²+1)+1 = q^4`.

Every maximal point-graph clique is a line simplex. Its integer
edge-to-flag path map has the same exact integral homology result,
and `M M^T=(q+1)I-J` on each line's flag block.
On cycles `J=0`, so `(q+1)^(-1/2)M^T`
gives the Hodge isometry for general q.

Exact finite q=2,3,5 constructions give:
`(P,F,b1)=(15,45,16),(40,160,81),(156,936,625)`.
At q=2 the full small chain/Hodge Gram equality was computed explicitly.

The point graph eigenvalues give
`tau(Levi)= (q²+1)^[q(q+1)²/2-1] (q+1)^[q(q²+1)]`.
Thus no prime dividing q divides tau. By the cycle-lattice
matrix-tree determinant identity, the standard edge pairing on H1
is **perfect in defining characteristic p|q**.
For q=3 the **existing** critical-group determinant factors
`2^83*5^23`; newly joint-audited finite ranks of the cycle
Gram are mod2=52, mod3=81, mod5=58, mod7=81, mod11=81.
The prior Gram and critical group results remain the owners of those
component facts; this packet ties them to the integral Hodge map.

**Physics boundary:** an exponent four in q^4 does **not**
establish physical 4D spacetime. A finite group/homology space
has no metric signature, time, speed of light, Einstein equations
or mass scale without further structure.

## 3. Full symmetry enforces exactly degenerate quadratic masses

Prior BT1688 proved that the 81-dimensional **complexified**
PSp(4,3) harmonic/Levi H1 representation is irreducible.
Schur's lemma then imposes a clean **TOE no-go**:
every quadratic Hermitian mass matrix commuting with the full group
is scalar on this 81-space.

So PSp symmetry alone cannot give 3 different family masses,
chiral masses, or a physical 27+27+27 generation separation.
Selection of an order-three element already breaks G to a proper
subgroup, and no native element is distinguished by G.

A direct integral action on the 81 fundamental Levi cycles checks
five distinct symplectic transvections: each has order 3,
`trace(I,g,g²)=(81,0,0)`. Thus the complex eigenspace
multiplicities are (27,27,27). Mod3 it has `(g-I)^3=0`
and `rank(g-I)=54,rank((g-I)^2)=27`, precisely
27 Jordan blocks of size 3. This is a qutrit **clock action**,
not a dynamical 3-family mass matrix.

Also, an 81-dimensional vector space cannot carry a nondegenerate
alternating symplectic form (odd dimension); the associated
81-qutrit Pauli phase space needs the doubled `V+V*`
of dimension 162. The Weyl-Heisenberg group has order `3^163`
and its irreducible Schrödinger Hilbert space dimension `3^81`;
the **81-dim homology coefficient module is not that Hilbert space**.

## 4. A symmetry-breaking *mechanism candidate*: exact 3-mode stars

Earlier `w33_pass1083_levi_frame_steinberg_intertwiner.py`
provides a native integer 160x160 signed chamber-distance matrix K
with `K²=160 K`; `P_H=K/160` is the rank81 cycle projector.
For each of **all 80** native 4-flag point or line stars S:

`K[S,S]=108 I4 - 27 J4`.

Define the **conditional** Hermitian defect on the 81 harmonic space
`H_defect=lambda * P_H P_S P_H`.
There are exactly **three** nonzero eigenvalues `lambda*27/40`,
and 78 zero eigenvalues. No parameters besides chosen scale and
the selected star enter the eigenvalue ratio.

For two separately selected stars the spectrum depends only on
their actual incidence relation. We enumerated **every one of the
3,160 unordered distinct pairs** and computed exact integer
characteristic polynomials of their union flag blocks:

| Pair type | Number of pairs | Nonzero eigenvalues of P_H(P_A+P_B)P_H |
|---|---:|---|
| Two collinear points / two intersecting lines | 240 each | 9/20, 27/40 (×4), 9/10 |
| Two noncollinear points / two skew lines | 540 each | 13/20 (×3), 7/10 (×3) |
| Incident point and line | 160 | 27/40 (×4), 27/32 |
| Nonincident point and line | 1440 | 3/5, 27/40 (×4), 3/4 |

**New conceptual consequence:** a single selected star enables exactly
3 harmonic modes, and two selected stars produce geometric
6-mode or 5-mode mass textures with sharp rational eigenvalues.
Under full symmetry no star is selected and all 81 remain degenerate.
This is a **testbed for an emergent order parameter**: a real
symmetry-breaking potential must select a star/relative pair
and fix its scale; the combinatorics alone does neither.
The values are NOT Standard Model mass ratios.

## What closes, what remains open

This packet builds an explicit integer and metric identification of
clique/CSS homology and the Levi gauge cycle lattice. It shows what
symmetry allows and forbids, and exposes concrete finite-dimensional
mass *texture operators* after a geometric choice.

It does **not** derive a 4D continuum, Lorentzian metric, conserved
stress tensor, Einstein gravity, dynamical order parameter, actual
Yukawa coupling, Higgs field, CKM matrix, clock speed or mass gap.
An integer homology isometry is a necessary structural bridge, not
an action principle, experiment, or proof of a TOE.

### Reproducers

- `analysis/w33_20261009_toe_integral_clique_levi_bridge.py`
- `analysis/w33_20261009_toe_q4_family_theorem.py`
- `analysis/w33_20261009_toe_star_defect_spectra.py`
- `analysis/w33_20261009_toe_c3_clock_phase_nogo.py`
- `tests/test_w33_20261009_toe_integral_bridge_and_symmetry.py`

The certificates record six equivariance checks, integer chain
identities, canonical Gram congruence, generalized q=2/3/5
cross-checks, all 3,160 two-star relation types, and actual 81x81
order-three group action matrices' trace/Jordan ranks. Correctness
does not rely on unrun speculative applications.
