# Passes 3506–3512 — permutation CSP, exact descendants, scheme blindness, spectral transplantation, and two high-risk bridges

## Status

The standard-library verifier reports

```text
PASS_7_FRONTS 15ab9b21e744e755917e0b4c40ec806b43c5463b8a11cfbfac7bdbb4a9c8dfe7
```

This packet executes all five continuations from Passes 3500–3505 and two independent outside-the-box experiments. It preserves the existing boundaries: the missing degree-57 Moore graph is not declared to exist or not exist; recent automorphism work is marked as a preprint; and shared spectra are not promoted to objectwise graph identifications.

---

## Pass 3506 — a gauge-reduced Moore-57 permutation CSP

Fix an edge of a hypothetical

\[
\operatorname{SRG}(3250,57,0,1).
\]

The residual core is the previously proved \(56\times56\) double-fibred grid. For rows \(i\ne j\), let

\[
p_{ij}(a)
\]

be the column in row \(j\) adjacent to column \(a\) in row \(i\). The independent matching data contain

\[
\binom{56}{2}\cdot56
=
\boxed{86\,240}
\]

permutation entries. A direct CP-SAT implementation with explicit inverse arrays has

\[
56\cdot55\cdot56
=
\boxed{172\,480}
\]

integer variables, compared with

\[
\binom{56}{2}\cdot56\cdot55
=
\boxed{4\,743\,200}
\]

nonfixed one-hot Boolean variables.

The exact base model contains:

- \(1\,540\) row-pair `AllDifferent` constraints;
- \(1\,540\) inverse-channel constraints;
- \(3\,136\) vertex-star `AllDifferent` constraints;
- \(55\) gauge equalities.

Thus the pre-separation structural model has

\[
\boxed{6\,271}
\]

constraints.

The gauge is fixed around the base residual vertex by

\[
p_{0j}(0)=j,
\qquad
1\le j\le55.
\]

Triangle constraints are not materialized as billions of static clauses. Candidate solutions are inspected over the

\[
\binom{56}{3}=27\,720
\]

row triples, and fixed points of the non-Abelian triangle holonomy are returned as concrete no-good cuts. A second separator is reserved for residual nonedges having the wrong number of common neighbors.

Executable exporter:

```text
analysis/bt3506_m57_permutation_csp.py
```

This is a source-complete model and separator architecture. It is not a solved \(56\)-fibre instance and it is not an unsatisfiability certificate.

---

## Pass 3507 — literal descendant atlas for five of the seven graphs

### Clebsch to Petersen

The Clebsch graph is reconstructed on the sixteen even-weight vectors of
\(\mathbb F_2^5\), with adjacency at Hamming distance four. At the zero vector,
the second subconstituent consists of the ten weight-two words. Two such words
are adjacent precisely when their supports are disjoint, giving

\[
KG(5,2)=\text{Petersen}.
\]

The verifier checks objectwise

\[
\operatorname{SRG}(16,5,0,2)
\longrightarrow
\operatorname{SRG}(10,3,0,1).
\]

### One Golay/Witt object produces Higman–Sims, \(M_{22}\), and Gewirtz

The verifier independently generates the binary Golay code from a cyclic
\([23,12,7]\) generator and extends it by parity. Its exact weight distribution is

\[
1+759z^8+2576z^{12}+759z^{16}+z^{24}.
\]

Fixing two coordinates in the 759 octads and deleting those coordinates yields
exactly 77 six-subsets of a 22-set. Exhausting all triples verifies the Steiner law

\[
S(3,6,22):
\qquad
\text{every 3-subset lies in exactly one hexad}.
\]

Disjointness of hexads gives

\[
\operatorname{SRG}(77,16,0,4)=M_{22}.
\]

Avoiding one fixed point leaves 56 hexads and gives

\[
\operatorname{SRG}(56,10,0,2)=\text{Gewirtz}.
\]

Finally, adjoining the 22 points and one infinity vertex, with point–hexad
incidence and hexad-disjointness edges, reconstructs

\[
\operatorname{SRG}(100,22,0,6)=\text{Higman--Sims}.
\]

The second subconstituent at infinity is literally the \(M_{22}\) graph. Hence

\[
\boxed{
\text{Higman--Sims}
\longrightarrow
M_{22}
\longrightarrow
\text{Gewirtz}
}
\]

is now executable from one Golay/Witt incidence object.

Together with Clebsch \(\to\) Petersen, five of the seven standard
non-complete-bipartite triangle-free SRGs now lie in two exact descendant chains.
The pentagon and Hoffman–Singleton graph remain separate roots in this atlas.

---

## Pass 3508 — the rank-three association scheme cannot see the 57-vertex hole

For the fixed

\[
\mu=4,\qquad r=2
\]

ladder, the verifier computes all primitive-idempotent Krein products exactly.
Every rung passes:

1. the SRG feasibility equation;
2. integral spectrum and multiplicities;
3. both standard absolute embedding bounds;
4. every rank-three Krein nonnegativity inequality.

This includes the nonexistent rung

\[
\operatorname{SRG}(57,14,1,4),
\]

whose exact nontrivial Krein rows are

\[
q_{11}
=
\left(
38,\frac{1273}{49},\frac{1140}{49}
\right),
\]

\[
q_{12}
=
\left(
0,\frac{540}{49},\frac{722}{49}
\right),
\]

\[
q_{22}
=
\left(
18,\frac{342}{49},\frac{111}{49}
\right).
\]

All entries are nonnegative.

Therefore the nonexistence theorem cannot be recovered from the ordinary
rank-three Bose–Mesner algebra or its first Krein/absolute-bound filters:

\[
\boxed{
\text{the }\lambda=1\text{ obstruction is scheme-invisible}.
}
\]

Published proofs use finer local compatibility and star-complement information.
This negative theorem sharply identifies where a successful generalization must
look: Terwilliger/local modules, star complements, or higher coherent refinements.

---

## Pass 3509 — a W33/Gewirtz spectral-transplant compiler

On the augmentation module, both W33 and Gewirtz satisfy

\[
A^2+2A-8I=0.
\]

The new compiler reduces every polynomial \(f(A)\) to one canonical two-channel
normal form

\[
f(A)=aA+bI
\]

in

\[
\mathbb Q[x]/(x^2+2x-8).
\]

For example,

\[
A^2=-2A+8I,
\qquad
A^4=-40A+96I,
\]

and the verifier checks all reductions at the two restricted eigenvalues
\(2\) and \(-4\).

A second exact universal object appears. On augmentation, complement adjacency is

\[
\overline A=-I-A,
\]

so

\[
U=\frac{-I-A}{3}
\]

has eigenvalues \(-1,+1\) and satisfies

\[
\boxed{U^2=I}.
\]

Thus both graphs carry the same polynomially defined reflection and projectors

\[
P_\pm=\frac{I\pm U}{2}.
\]

The packet classifies claims into three evidence levels:

- **polynomial-only:** identities in the quotient ring, two-channel functional
  calculus, and the complement reflection;
- **multiplicity-sensitive:** traces, determinants, and projector ranks;
- **geometry-sensitive:** lines, cliques, incidence factorizations, automorphism
  groups, codes, and descendant maps.

This is an executable falsifier for proposed W33–Gewirtz transfers: only the
first class transports automatically.

---

## Pass 3510 — the 57-cell/M57 symmetry firewall has one surviving odd shadow

The regular 57-cell/Perkel symmetry group has

\[
|PSL(2,19)|=3420.
\]

Peer-reviewed work bounds a hypothetical M57 automorphism group by 375 in the
odd-order case and 110 in the even-order case. A June 2026 preprint claims that
involutions are impossible, which would force odd order.

Conditional on that preprint:

- \(\operatorname{Aut}(M57)\) is solvable by the odd-order theorem;
- it cannot contain \(A_5\);
- it cannot contain \(PSL(2,19)\);
- the repo's proposed common-\(A_5\) comparison of two rational 20-planes
  cannot be realized as a common automorphism action.

But parity does **not** annihilate every possible shadow of the 57-cell group.
A point stabilizer in \(PSL(2,19)\) is the odd Borel subgroup

\[
C_{19}\rtimes C_9,
\qquad
|C_{19}\rtimes C_9|=171.
\]

Since

\[
171<375,
\]

the known order bound and oddness alone do not exclude this Borel shadow. The
next exact symmetry test is therefore narrower and better posed:

> restrict the Perkel \(-3\) twenty-plane to \(19{:}9\), and compare its
> rational constituents against every allowed M57 fixed-point profile.

The global \(PSL(2,19)\) and \(A_5\) identifications die; an odd \(19{:}9\)
residue remains open.

---

## Pass 3511 BONKERS — Moore graphs carry non-Abelian permutation curvature

The edge-rooted matching permutations can be treated as an \(S_{d-1}\)-valued
connection on the complete graph of row fibres. For a row triangle \(i,j,k\),
define the holonomy

\[
H_{ijk}
=
\sigma_{ki}\sigma_{jk}\sigma_{ij}.
\]

Gauge changes conjugate \(H_{ijk}\), so its cycle type is gauge invariant.
Triangle-freeness requires every \(H_{ijk}\) to be fixed-point-free.

The verifier reconstructs the Hoffman–Singleton graph from five pentagons,
five pentagrams, and the standard affine cross-incidence rule. For one fixed
edge, its \(6\times6\) residual chart has the striking exact property:

\[
\boxed{
\text{all 15 pair matchings have cycle type }2^3
}
\]

and

\[
\boxed{
\text{all 20 triangle holonomies have cycle type }2^3.
}
\]

Thus the Hoffman–Singleton connection is not merely derangement-valued; in this
gauge every edge and curvature element is a fixed-point-free involution.

This motivates a deliberately high-risk M57 solver branch:

\[
\sigma_{ij}\sim2^{28},
\qquad
H_{ijk}\sim2^{28}
\]

for all 1,540 row pairs and 27,720 row triangles.

This involutive-curvature ansatz is **not necessary** for M57. Its value is
computational: it replaces arbitrary derangements with one sharply constrained
conjugacy class inspired by the largest known nontrivial Moore witness.

---

## Pass 3512 BONKERS — the sporadic descendant chain is a Golay puncture functor

The exact construction sequence is

\[
[23,12,7]
\overset{\rm parity}{\longrightarrow}
[24,12,8]
\overset{\rm fix\ 2}{\longrightarrow}
S(3,6,22)
\overset{\rm disjointness}{\longrightarrow}
M_{22}
\overset{\rm avoid\ 1}{\longrightarrow}
\text{Gewirtz},
\]

while restoring the 22 point vertices and infinity produces Higman–Sims.

This is more than three matching parameter tables. It is one executable
puncture/avoidance pipeline whose intermediate objects retain enough incidence
data to reconstruct every descendant objectwise.

The provocative comparison with the repo's W33 face tower

\[
240\to120\to40
\]

is now sharply bounded:

- the Golay chain uses coordinate fixing, point avoidance, and incidence
  extension;
- the W33 face tower uses antipodal quotienting and a \(40K_3\) quotient;
- both are information-losing descendant functors;
- no category equivalence or group identification is claimed.

The next worthwhile question is whether both towers admit the same abstract
``quotient–reconstruct'' axioms, not whether their objects should be identified.

---

## Reproduction

```bash
python analysis/bt3506_3512_seven_graph_csp_scheme_symmetry.py
pytest -q tests/test_bt3506_bt3512_seven_graph_csp_scheme_symmetry.py
python analysis/bt3506_m57_permutation_csp.py --stats-only
```

Expected verifier output:

```text
PASS_7_FRONTS 15ab9b21e744e755917e0b4c40ec806b43c5463b8a11cfbfac7bdbb4a9c8dfe7
```

Materializing or solving the CP-SAT model additionally requires OR-Tools.

## Evidence boundary

Promoted exactly:

- the CSP variable/constraint census and source-complete exporter;
- the Clebsch/Petersen and Golay/Witt sporadic descendant constructions;
- the full exact Krein table and scheme-blindness result;
- the polynomial reduction and universal complement reflection;
- the group-order/Borel arithmetic;
- the Hoffman–Singleton matching and holonomy cycle-type census.

Not promoted:

- an M57 solution or nonexistence certificate;
- sufficiency of the base CSP constraints;
- necessity of the involutive-curvature ansatz;
- peer-reviewed status for the June 2026 no-involution theorem;
- an actual M57 \(19{:}9\) action;
- a canonical W33–Gewirtz intertwiner;
- a categorical equivalence between the Golay and W33 descendant towers.

## Literature boundary

- M. Mačaj and J. Širáň, *Search for properties of the missing Moore graph*,
  Linear Algebra and its Applications 432 (2010), 2381–2398.
- Y. Ishida, *No involutions in the missing Moore graph*, arXiv:2606.29183
  (June 2026 preprint).
- M. Milošević, *An example of using star complements in classifying strongly
  regular graphs*, Filomat 22:2 (2008), 53–57.
- H. A. Wilbrink and A. E. Brouwer, *A (57,14,1) strongly regular graph does
  not exist*, Indagationes Mathematicae 86 (1983), 117–121.
