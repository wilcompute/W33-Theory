# Maximal compiler symmetry: 36 safe planes and four Pappus controllers

## Executive result

The full scheduler
\[
K=H_{27}^{\rm address}\times C_3^{\rm external}
\]
cannot be conjugated equivariantly into the landed matter-81 operator action. The largest subgroup on which an invertible address-to-operator compiler can still be equivariant is exactly
\[
\boxed{|L|_{\max}=9,\qquad L\cong C_3^2,\qquad \#\{L_{\max}\}=36.}
\]

These 36 maximal compiler-safe planes form a three-sheet Hesse controller. Their incidence with the 36 noncentral order-three subgroups of the scheduler is
\[
\boxed{4\ \text{disjoint Pappus configurations}.}
\]

## Character criterion

Let
\[
D=[K,K]=Z(H_{27})\times\{0\}\cong C_3.
\]
The address carrier is the regular 81-dimensional representation of \(K\). The landed operator carrier has character supported exactly on \(D\):
\[
\chi_{\rm op}(1)=81,\qquad
\chi_{\rm op}(z^c)=81\omega^c,\qquad
\chi_{\rm op}(g)=0\quad(g\notin D).
\]
Therefore
\[
\operatorname{Reg}(K)|_L\cong \mathcal H_{\rm op}|_L
\quad\Longleftrightarrow\quad
L\cap D=1.
\]

Any safe \(L\) is abelian and injects into \(K/D\cong\mathbf F_3^3\). The induced alternating commutator form has rank two and a one-dimensional radical, so a totally isotropic subspace has dimension at most two. Hence \(|L|\le9\).

The exhaustive census is:

- order 3: 40 total, 39 safe;
- order 9: 49 total, 36 safe and 13 containing \(D\);
- order 27: 13 maximal subgroups, all containing \(D\).

## Three-sheet Hesse controller

In the fixed physical Clifford lift gauge, the four projective H27 directions use the selected lifts
\[
(0,1;1),\ (1,0;1),\ (1,1;0),\ (1,2;2).
\]
Every noncentral cyclic subgroup of the internal H27 is labeled by a projective direction \(d\) and a lift phase \(c\). Map it to the affine Hesse line
\[
\boxed{\langle d,v\rangle_{\rm symp}=c-c_0(d).}
\]
This recovers all twelve lines of \(AG(2,3)\): four parallel classes with three lines per class.

Each maximal safe plane has one further label, namely one of the three center lines complementary to \(D\). Thus
\[
36=12_{\rm Hesse\ lines}\times3_{\rm center\ sheets}.
\]
The fixed-center Heisenberg automorphism group has order 216 and acts with orbit split
\[
12+12+12.
\]

## Exact plane-intersection law

For distinct safe planes \(L,L'\):

- same center sheet: \(|L\cap L'|=3\);
- different sheets and parallel Hesse lines: \(|L\cap L'|=3\);
- different sheets and meeting Hesse lines: \(|L\cap L'|=1\).

The all-pairs census is
\[
324+162+108+36=630.
\]

## Four Pappus configurations

There are exactly 36 noncentral order-three subgroups of \(K\). Join one to a maximal safe plane when it is contained in that plane. The resulting bipartite graph has
\[
72\ \text{vertices},\qquad108\ \text{edges},\qquad\deg=3.
\]
It has four connected components of size 18, one for each qutrit projective direction, and every component is the Pappus graph.

For one fixed direction the nine noncentral \(C_3\) subgroups are points \((c,p)\in\mathbf F_3^2\), while the nine safe planes are blocks
\[
\boxed{c=\alpha+\beta p.}
\]
This is \(AG(2,3)\) with one parallel class removed, i.e. the classical Pappus \(9_3\) configuration.

The repository already owns a different Pappus occurrence in scripts/w33_witting_packet_foliation_incidence_audit.py, where Pappus comes from affine-foliation leaf incidence. The present carrier is subgroup incidence.

## Count-collision firewalls

Published finite geometry gives 36 \(GQ(2,2)\) doily hyperplanes inside \(GQ(2,4)\), and the repository owns the E6/double-six graph
\[
\operatorname{SRG}(36,20,10,12).
\]
No identification is made. The natural compiler-plane graph obtained by joining pairs with order-three intersection is 17-regular, not 20-regular, so the repeated count 36 does not define an incidence equivalence.

The repository also owns an ordinary \(36=12\times3\) phase-decorated Hesse lift in docs/PAYNE_HESSE_PACKET_DICTIONARY.md. The current theorem supplies a natural dual target, but an objectwise pairing is still open.

## TOE reading

The address and execution pictures cannot be related by a full \(H_{27}\times C_3\)-equivariant basis change. Their largest exact common control surface is instead a qutrit plane \(C_3^2\). There are 36 maximal choices, organized by Hesse/Pappus geometry.

The next compiler target is therefore a selector or patching rule on these 36 safe planes, not another search for a nonexistent full-group conjugacy.

## Prior-art boundary

Saniga et al., The Veldkamp Space of GQ(2,4), arXiv:0903.0715, owns the classical 27 perp hyperplanes, 36 \(GQ(2,2)\) hyperplanes, and \(V(GQ(2,4))\cong PG(5,2)\). The Pappus configuration itself is classical. The increment here is its exact appearance as the maximal common-symmetry controller forced by the independently landed address/operator H27 representations.
