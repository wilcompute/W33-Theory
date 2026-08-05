# Passes 3694–3700 — spread ETF, Norton axes, Monster targets, and two bonkers closures

## Release status

The self-contained exact verifier

`analysis/w33_pass3694_3700_spread_etf_axial_closure.py`

reconstructs the forty points, forty totally isotropic lines, and all thirty-six spreads of \(W(3,3)\). It passes twenty exact checks and freezes the semantic certificate

`ddbe48339458f56f1d5b10b6d544a64be0e00ecdab73ce73c5203a7482fad65a`.

| front | exact outcome |
| --- | --- |
| rank-three representation/idempotents | explicit rational primitive idempotents \(E_{15}\) and \(E_{20}\); line–spread incidence realizes \(E_{15}\) exactly |
| magic-ray separation | spread SRG separated from the 36-ray orthogonality graph by degree, spectrum, and an exact \(4\times9\) quotient |
| Monster class fusion | CTblLib target enumerates constrained fusions and degree-81 multiplicities; executed artifact remains pending |
| concrete Monster words | `mmgroup` harness validates serialized words by closure, subgroup signatures, order census, and character fingerprints; candidate words remain absent |
| local Majorana/Griess front | canonical positive Frobenius Norton algebra on the rank-15 sector, with 36 primitive axes and exact fusion; explicitly not Majorana |
| bonkers I | centered 40-line by 36-spread incidence is a real \(\operatorname{ETF}(15,36)\), saturating Welch with coherence \(1/5\) |
| bonkers II | Norton products create 120 triples; every W33 line partitions its nine containing spreads into three algebraic triples |
| extra no-go | an unbranched type-preserving cover cannot turn ternary parabolic panels into binary polytope panels |

## I. Exact rank-three idempotents

Let \(A\) be the adjacency matrix on the thirty-six spreads, where two spreads are adjacent when they share four W33 lines. The pair census is

\[
270\text{ pairs sharing }4,
\qquad
360\text{ pairs sharing }1,
\]

and \(A^2=9I+6J\). Thus \(A\) is \(\operatorname{SRG}(36,15,6,6)\), with spectrum

\[
15^1\oplus3^{15}\oplus(-3)^{20}.
\]

The nontrivial rational primitive idempotents are

\[
E_{15}=\frac12I+\frac16A-\frac1{12}J,
\qquad
E_{20}=\frac12I-\frac16A+\frac1{18}J.
\]

The verifier checks their ranks, idempotence, and mutual orthogonality exactly.

## II. Bonkers I: a hidden \(\operatorname{ETF}(15,36)\)

Let \(B\) be the \(40\times36\) line–spread incidence matrix. Every spread contains ten lines and every W33 line lies in nine spreads. Pair intersections give

\[
B^{\mathsf T}B=9I+3A+J.
\]

Center the columns by \(C=B-\frac14J_{40\times36}\). Then

\[
\boxed{C^{\mathsf T}C=18E_{15}.}
\]

Every centered column has norm squared \(15/2\). After normalization, distinct columns have inner product \(+1/5\) when the spreads share four lines and \(-1/5\) when they share one line. The Welch bound is

\[
\frac{36-15}{15(36-1)}=\frac1{25},
\]

so the coherence \(1/5\) is optimal. Therefore the centered incidence columns form

\[
\boxed{\operatorname{ETF}(15,36).}
\]

The Seidel matrix \(S=I+2A-J\) satisfies

\[
S^2-2S-35I=0
\]

and has spectrum \(7^{15}\oplus(-5)^{21}\).

## III. Exact Naimark/photonic dimension certificate

Rescaling the fifteen-dimensional synthesis matrix gives a row isometry whose Gram projector is \(E_{15}\). Its orthogonal complement is

\[
I_{36}-E_{15}=E_{20}+\frac1{36}J,
\]

of rank twenty-one. Hence an exact passive 36-mode unitary completion requires

\[
\boxed{21\text{ orthogonal guard dimensions}.}
\]

Fewer guard dimensions cannot complete the frame analysis map to a unitary. This is a linear-optical dimension theorem, not a fabricated device or experimental claim.

## IV. The canonical rank-15 Norton algebra

On \(V=\operatorname{im}E_{15}\), define

\[
x\star y=E_{15}(x\circ y),
\qquad
a_i=6E_{15}e_i.
\]

All thirty-six axes are primitive idempotents. Left multiplication by any axis has spectrum

\[
1^1\oplus\left(-\frac12\right)^5\oplus\left(\frac16\right)^9.
\]

The exact fusion law is

\[
\begin{array}{c|ccc}
\star & 1 & -\tfrac12 & \tfrac16\\\hline
1 & 1 & -\tfrac12 & \tfrac16\\
-\tfrac12 & -\tfrac12 & 1,\tfrac16 & -\tfrac12\\
\tfrac16 & \tfrac16 & -\tfrac12 & 1,\tfrac16
\end{array}
\]

with \(\mathbb Z_2\)-grading: even \(\{1,1/6\}\), odd \(\{-1/2\}\). The standard positive form is Frobenius. This is an axial/Norton algebra, but not a Monster Majorana algebra: the negative eigenvalue and fusion spectrum provide an exact firewall.

## V. Pair products and the 120-triple system

For the 270 adjacent spread pairs,

\[
a_i\star a_j=\frac{a_i+a_j}{6}.
\]

For every one of the 360 nonadjacent pairs, there is a unique third axis \(a_k\) such that

\[
a_i\star a_j=-\frac{a_i+a_j}{6}+\frac{a_k}{3}.
\]

The resulting unordered triples number \(360/3=120\). Every triple consists of three spreads sharing a unique W33 line. Conversely, each of the forty W33 lines lies in nine spreads, and those nine spreads split into exactly three disjoint Norton triples:

\[
40\cdot3=120.
\]

Each spread lies in ten triples, one for each constituent line. This is an objectwise algebra–geometry dictionary, not a count coincidence.

## VI. Magic-ray firewall

The 36 Witting magic rays have an exact 11-regular orthogonality graph with spectrum

\[
11^1\oplus2^{20}\oplus(-1)^3\oplus(-4)^{12}.
\]

It has four eigenvalues and is not strongly regular. Its four blocks of nine rays form an equitable partition with quotient \(3J_4-I_4\), and each internal block is three disjoint triangles.

The spread graph is 15-regular with spectrum \(15^1\oplus3^{15}\oplus(-3)^{20}\). Degree and spectrum separate the two graphs exactly; the recurring number thirty-six does not identify their carriers.

## VII. Ternary panels cannot be thinned by an ordinary cover

Passes 3670–3686 found rank-one residues of size three in the four-parabolic chamber system. Each chamber has two neighbors of a given panel type. A thin abstract-polytope panel has size two and colored neighbor degree one.

A type-preserving chamber-system cover is locally bijective on every residue, preserving panel cardinality and colored degree. Therefore

\[
\boxed{\text{no unbranched type-preserving cover can turn these }C_3\text{ panels into binary panels}.}
\]

A successful binary resolution must instead be a quotient, deletion, branched construction, or change of incidence structure.

## VIII. Monster fronts: executable, still fail-closed

`analysis/w33_mmgroup_u42_candidate_harness.py` requires four explicit serialized Monster words. It validates generator orders, pair-product orders, four order-648 triple closures, total order 25,920, full element-order census, integer serialization round trips, and available Monster character fingerprints. With no candidate, it reports pending or fails; it never substitutes the abstract 40-point representation.

`analysis/w33_monster_u42_class_fusion_target.g` uses CTblLib to impose the 5B-containing class constraints, enumerate possible \(U_4(2)\to\mathbb M\) fusions, restrict the 196883-dimensional Monster character, and record every degree-81 multiplicity. Until the GAP artifact executes and freezes, no multiplicity is claimed.

## Evidence boundary

Proved here: the ETF, rational idempotent carrier, 21-dimensional Naimark complement, stated Norton-axis fusion law, all 120 triples and their line partition, magic-ray separation, and unbranched-cover no-go.

Not proved here: concrete Monster words, an executed class-fusion multiplicity, a Majorana/Griess/VOA identification, a regular thin polytope cover, or laboratory realization.
