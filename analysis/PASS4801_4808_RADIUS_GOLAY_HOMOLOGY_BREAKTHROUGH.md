# Passes 4801–4808 — exact H10 radius, qutrit logical shell, local Golay and global Levi homology

## Executive result

This packet closes the five continuations from Passes 4793–4800 and adds three outside-the-box consequences.

The new qutrit triangle CSS code now has a precise local-to-global structure:

\[
C=[270,44,18]_3\subset L=G_{10}^{\oplus27}\subset C^\perp=[270,226,4]_3,
\]

where every local ten-coordinate fiber is an explicit punctured ternary Golay code
\(G_{10}=[10,6,4]_3\).  The global quotient is canonical:

\[
C^\perp/L\cong H_1(\operatorname{Levi}(GQ(4,2));\mathbb F_3),\qquad \dim=64.
\]

The overall CSS distance four is entirely local-Golay.  The first nonlocal/homological logical sector occurs at minimum triangle-lift weight six and has a canonical family of 360 induced-\(K_{3,3}\) witnesses.

Separately, the long-open binary H10 covering-radius bracket finally closes:

\[
\boxed{\rho(H_{10})=14}.
\]

## Pass 4801 — exact H10 covering radius

Pass4794 had certified \(14\le\rho(H_{10})\le15\) and Pass4781 supplied the distance-14 witness `253626779097`.

A distance-15 coset exists iff it has a leader \(x\) of weight exactly 15.  For every \(c\in H_{10}\),

\[
d(x,c)=15+\operatorname{wt}(c)-2|\operatorname{supp}(x)\cap\operatorname{supp}(c)|\ge15,
\]

so the remaining problem is a 40-variable cardinality feasibility problem.

By PSp coordinate transitivity, fix coordinate 0 in the leader.  Its intersection with the weight-12 neighborhood codeword \(N(0)\) is \(a=1,\ldots,6\).  The coordinate stabilizer has order 648 and has exactly

\[
1,2,3,6,6,7
\]

orbits on the corresponding \(a\)-subsets of \(N(0)\), for 25 symmetry-complete cases total.  Exact cardinality propagation against all 1,024 H10 codewords rejects all 25 representatives (139,013 search nodes total).  Hence there is no weight-15 coset leader and

\[
\boxed{\rho(H_{10})=14}.
\]

`analysis/w33_pass4801_h10_covering_radius_sat.py` provides an independent PySAT encoding of the same leader problem.

## Pass 4802 — complete minimum-logical shell of [[270,182,4]]_3

All projective weight-four words of \(C^\perp\) were enumerated exactly by signed pair-sum hashing.  There are

\[
\boxed{810}
\]

projective minimum logicals, hence 1,620 nonzero codewords including scalar multiples.  Every one is supported in exactly one of the 27 maximal \(K_5\) fibers.

Per \(K_5\) there are 30 projective minima, splitting geometrically as

\[
5+10+15.
\]

Globally this is

\[
\boxed{135+270+405=810}.
\]

The ten triangle coordinates of one \(K_5\) carry a local kernel

\[
[10,6,4]_3
\]

with exact weight enumerator

\[
1+60z^4+144z^5+60z^6+240z^7+180z^8+20z^9+24z^{10}.
\]

## Pass 4803 — exact single-qutrit decoder and optimal schedule

The 270 columns of the point-triangle incidence matrix \(B\) are distinct weight-three vectors.  Therefore the ordered X/Z syndrome pair uniquely identifies every nontrivial single-qutrit Pauli error:

\[
270(3^2-1)=\boxed{2160}
\]

unique one-qutrit error syndromes.

For syndrome extraction, the combined X/Z Tanner graph has 90 real check vertices of degree 18 and 270 data vertices of degree 6.  An exact 18-regular bipartite completion decomposes into 18 perfect matchings.  Removing dummy interactions leaves 18 conflict-free layers, each servicing all 90 real checks on 90 distinct data qutrits.

The lower bound is also 18 because each check has weight 18, so the schedule is optimal in the one-interaction-per-check/data-per-layer model.

## Pass 4804 — PSp-equivariant F4/E6 crosswalk and extension firewall

The Pass4797 incidence isomorphism between the dependency-cube triality quotient and the compiler F4-normalizer quotient upgrades projectively to a PSp-equivariant map.  Both degree-45 projective images are the simple group

\[
U_4(2)\cong PSp(4,3),\qquad |U_4(2)|=25920.
\]

The two order-51,840 extensions remain different on this same 45-set:

- the central double cover \(Sp(4,3)=2.U_4(2)\) has degree-45 image 25,920 with kernel 2;
- the outer extension \(U_4(2):2\) / PGSp has 51,840 distinct projective permutations.

Thus equality of extension orders is explicitly not promoted to an extension identification.

## Pass 4805 — q=9 becomes the first three-class BLT shell

Using the already proved theorem that minimum line-kernel words are exactly BLT sets, Betten's complete q=9 BLT classification transfers to the minimum shell of
\(\ker_{\mathbb F_2}A_*(W(3,9))\).

The code has length 820 and minimum distance 10.  Under full projective-semilinear orthogonal equivalence there are exactly three classes:

- Linear: stabilizer 28,800, class size 239,112;
- K1: stabilizer 5,760, class size 1,195,560;
- Fi/Mondello: stabilizer 400, class size 17,216,064.

The complete shell therefore contains 18,650,736 minimum words at this equivalence level.  No finer PSp orbit claim is made.

## Pass 4806 — bonkers: every K5 fiber is punctured ternary Golay

The local \([10,6,4]_3\) code was not identified from parameters alone.  Exhausting all linear one-coordinate extensions shows exactly four nonzero functionals, i.e. two projective directions, raise the distance to five.  Either gives

\[
G_{11}=[11,6,5]_3
\]

with enumerator

\[
1+132z^5+132z^6+330z^8+110z^9+24z^{11}.
\]

Adjoining representatives of both projective directions gives a self-dual

\[
G_{12}=[12,6,6]_3
\]

with enumerator

\[
1+264z^6+440z^9+24z^{12}.
\]

Therefore the ten triangle coordinates of every GQ(4,2) \(K_5\) carry an explicit punctured ternary Golay code.

## Pass 4807 — bonkers: local Golay / global homology filtration

Let \(L\) be the direct sum of the 27 local Golay punctures.  Exact ranks give

\[
\dim C=44,\qquad \dim L=162,\qquad \dim C^\perp=226,
\]

with

\[
C\subset L\subset C^\perp.
\]

The GQ(4,2) Levi graph has 72 vertices and 135 edges, so over \(\mathbb F_3\)

\[
\dim H_1=135-72+1=64.
\]

The line-local point-sum map from triangle coefficients to the 135 Levi incidences has kernel exactly \(L\), sends \(C^\perp\) onto the Levi cycle space, and therefore induces the canonical isomorphism

\[
\boxed{C^\perp/L\cong H_1(\operatorname{Levi}(GQ(4,2));\mathbb F_3)}.
\]

Equivalently the logical space has the canonical short exact sequence

\[
0\to L/C\to C^\perp/C\to H_1(\mathrm{Levi};\mathbb F_3)\to0
\]

with dimensions \(118\to182\to64\).  No canonical splitting is asserted.

## Pass 4808 — bonkers: the first topological logical has lift weight six

Reduce triangle-coordinate words modulo the local Golay sum \(L\).  On one K5 the 81 possible local point-sum syndromes have minimum preimage-cost distribution

\[
1\times0,\qquad20\times1,\qquad60\times2.
\]

An exact symmetry-broken MILP rules out every nonzero global homology class with triangle-lift weight at most five.  Weight six is attained by induced \(K_{3,3}\) subgraphs of the 27-line intersection graph: put opposite F3 signs on the two three-line parts, and on each line select the triangle of its three intersection points with the opposite part.

The 27-line graph contains exactly 360 induced \(K_{3,3}\)'s, hence a canonical family of 360 projective weight-six homology witnesses.

Therefore

\[
\boxed{d_{\mathrm{lift}}(C^\perp/L)=6}.
\]

The 360 K3,3 witnesses are not claimed to exhaust the complete weight-six quotient shell.

## New structural compression

The triangle CSS code is no longer one undifferentiated [[270,182,4]] object.  It has a provable two-scale architecture:

\[
\boxed{
\text{27 local punctured Golay blocks}
\quad\longrightarrow\quad
\text{64-dimensional Levi homology sector}
}
\]

with local logical distance four and first nonlocal lift distance six.  This gives a mathematically exact meaning to “local” versus “global/topological” logical operators in this finite model without importing microscopic physics.

## Firewalls

1. The H10 code/enumerator remains prior art; the exact radius-14 computation is a new repository computation, not a publication-priority claim.
2. BLT class names/completeness at q=9 are Betten prior art; only transfer to the already-proved line-kernel minimum shell is claimed here.
3. Ternary Golay identification is by explicit extension, not parameter matching.
4. The 45-point PSp map does not identify the central Sp and outer PGSp extensions.
5. The CSS schedule is hardware-independent and does not establish a fault-tolerance threshold.
6. The 360 K3,3 objects are a certified witness family, not a complete weight-six quotient classification.
