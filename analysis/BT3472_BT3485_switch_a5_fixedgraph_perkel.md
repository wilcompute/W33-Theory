# Passes 3472–3485 — complete switch graph, exhaustive A5 separation, fixed-graph port compiler, and the 19×3 Perkel boundary

## Executive theorem

The canonical live-label exact-cover ledger has now been materialized and independently checked:

- 394,200 covers through frame zero;
- 327 `PSp(4,3)` cover orbits;
- 3,547,800 exact covers;
- stabilizer histogram `2^228 4^84 8^15`.

Executing the exact legal four-for-four switch on every orbit representative gives the orbit-species quotient

\[
135+135+19\cdot3,
\]

not the census-only `135+135+57` interpretation. Expanding all covers and executing every legal switch gives the complete literal decomposition

\[
\boxed{\Gamma_{\rm switch}\cong 12{,}960\,H(5,3)\;\sqcup\;132{,}840\,K_3.}
\]

Thus the full graph has 145,800 connected components. The 3,149,280 sheet covers have degree ten and lie in 243-cover Hamming components; the 398,520 exceptional covers have degree two and lie in literal switch triangles.

A further exact carrier-clique theorem collapses the eleven balanced defect spectra to one uniform matrix, and an explicit projective arithmetic encoding reduces the direct source-level transition-oracle upper bound from 56,700 to 1,640 Toffolis.

The live chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

---

## 3472–3473 — all 3,547,800 covers and all legal switches

The legal switch is the retained Pass-3250 operation. Given a 60-frame exact cover, each of the 240 supports receives its unique cover owner. Every outside frame therefore acquires a four-owner signature. A legal switch replaces four owner frames by four pairwise independent outside frames with the same owner signature. The replacement is checked again for size 60, support count 240, and independence.

Across the 327 canonical representatives:

- 270 representatives have five switch loci and ten distinct switch neighbors;
- 57 exceptional representatives have one switch locus and two distinct neighbors.

Resolving every neighbor against all 3,547,800 group images yields:

- two connected orbit quotients of size 135 and cover mass 1,574,640 each;
- nineteen orbit-quotient triangles.

The nineteen triangles split by cover stabilizer as

\[
4+10+5,
\]

corresponding to orders 2, 4, and 8. This refines

\[
57=12+30+15
\]

objectwise.

The literal graph was then computed on all covers, not inferred from the quotient:

- each 1,574,640-cover sheet contains 6,480 connected components of size 243;
- the exceptional cap contains 132,840 connected components of size three;
- every exceptional component is `K3`;
- every sheet component is explicitly isomorphic to `H(5,3)`.

For a 243-cover component, choose a root. Its ten neighbors induce five disjoint edges. Label the two vertices of each edge by the two nonzero values in one ternary coordinate. Distances from any component vertex to the root and these ten neighbors recover a unique vector in `F3^5`; adjacency is exactly Hamming distance one. The component stabilizer in `PSp(4,3)` has order four, so each sheet is one transitive orbit of 6,480 such Hamming components.

This corrects the earlier language: 1,574,640 covers form one closed `PSp`-plus-switch augmentation sheet, not one literal switch component.

---

## 3474–3475 — exhaustive common-A5 module comparison

The surviving rank-20 analogy has been tested over every embedded `A5`, not one hand-picked subgroup.

For the Perkel `-3` projector, all 13,680 `(2,3,5)` generating pairs give character

\[
(20,0,2,0,0)
\]

on `(1A,2A,3A,5A,5B)`, with decomposition

\[
1\oplus3\oplus3'\oplus2\cdot4\oplus5.
\]

For the anchor `-4` projector, all 51,840 generating pairs give exactly two characters:

\[
(20,4,-1,0,0)=1\oplus4\oplus3\cdot5,
\]

and

\[
(20,4,5,0,0)=3\cdot1\oplus3\cdot4\oplus5.
\]

The character sets are disjoint even after swapping the two order-five classes. Therefore the two rational 20-spaces do not become equivalent on any common `A5` restriction.

---

## 3476–3477 — exact fixed-graph port factorization and ten-colour compiler

The fixed 540-vertex frame graph factors objectwise over the 45-anchor graph.

Each anchor block contains twelve frames split into three four-frame cells. Its local graph is

\[
K_{4,4,4}=K_{12}\setminus3K_4,
\]

with 48 local edges. Two blocks are joined exactly when their anchors are adjacent in the 45-vertex `SRG(45,32,22,24)`. Every adjacent block pair contributes exactly nine edges, and those edges are precisely

\[
K_{3,3}
\]

between one selected port from each of the three cells on both sides.

For each block, its 32 anchor neighbors select only sixteen distinct port triples, each twice. The sixteen triples form

\[
OA(16,3,4,2)
\]

and every block is isotopic to the Klein-four Latin square

\[
p_2=p_0\oplus p_1.
\]

Every one of the twelve ports is selected by exactly eight anchor neighbors.

This gives an exact CSP compression: a ten-colouring is 135 four-port cell words; the three cell supports in each block must be pairwise disjoint, and the selected three-colour transversals across every anchor edge must be disjoint.

An exact DIMACS instance has been compiled with:

- 5,400 Boolean variables;
- 111,243 clauses;
- all 8,640 graph edges;
- a sound three-unit color-permutation symmetry break;
- SHA-256 `7c4a7cfede03f5af3fa12b98111e1867cc6addf7af00dc765f21847ff6001521`.

A bounded local search did not find a model and is a non-result. No SAT or UNSAT conclusion is promoted.

### Carrier-K9 defect-Laplacian collapse

The 8,640 frame-graph edges partition into the 240 cliques induced by the nine frames through each W33 edge:

\[
8640=240\binom92.
\]

In any proper ten-colouring each such `K9` uses nine different colours and has one missing colour. If colour `i` has class size `n_i`, put `d_i=60-n_i`. It occurs on `4n_i` carrier edges and is missing on

\[
m_i=240-4n_i=4d_i.
\]

Consequently every colour-pair edge count is forced by the class sizes alone:

\[
E_{ij}=240-m_i-m_j=4(n_i+n_j)-240.
\]

The complete defect Gram therefore becomes

\[
K_{ii}=d_i(60-d_i),\qquad K_{ij}=-d_i d_j,
\]

so that

\[
\boxed{K=60\operatorname{diag}(d)-dd^{\mathsf T}}.
\]

This is exactly the weighted Laplacian of the complete colour graph with edge weights `d_i d_j`. If `s` deficits are positive, `rank(K)=s-1`, and the matrix-tree cofactor is

\[
60^{s-2}\prod_{d_i>0}d_i.
\]

For the balanced profile `n_i=54`, all `d_i=6`, every pair count is 192, and

\[
\operatorname{spec}(K)=0^1,360^9.
\]

Thus the 15 split-tagged PSD candidates and eleven distinct spectra collapse on the actual graph to five duplicate tags representing one matrix. Ten of the eleven spectra are now eliminated exactly. This still does not decide whether the surviving balanced matrix or an unbalanced profile is realized.

---

## 3478–3479 — arithmetic oracle versus mixed-radix compiler

The 135-state arithmetic oracle and the `27×5` compiler are not two classical lookup encodings of the same transition function.

The 135 tau-orbits have 81 singleton barycenter fibers and 27 double fibers. Applying one signed two-point transform

\[
H_2=\begin{pmatrix}1&1\\1&-1\end{pmatrix}
\]

to every double fiber gives an exact basis decomposition

\[
135=108\oplus27.
\]

The transformed walk has zero cross-block entries. Its 108-state barycentric block has 864 nonzero entries; the hidden 27-state signed block has 162. The full, barycentric, and hidden spectral moments agree exactly with the previously frozen spectra.

The support graph of the original 135-state quotient is connected, so no permutation similarity can produce a nontrivial `108+27` block diagonalization. The mixed-radix compiler is therefore a genuine signed basis change, requiring 27 local Hadamard-type transforms, not a classical relabeling of the arithmetic oracle.

### Projective arithmetic source compiler

There is nevertheless an exact direct-state factorization after shifting by the fixed point

\[
x_0=(0,0,1,0,0).
\]

With shifted coordinates `y=x-x0`, define

\[
u=(2(y_1-y_4),2(y_2-y_3),y_5),\qquad
v=(2(y_1+y_4),2(y_2+y_3)).
\]

Then

\[
\tau(u,v)=(u,-v),
\]

which gives the exact orbit-set decomposition

\[
\boxed{\mathbb F_3^5/\langle\tau\rangle\cong\mathbb F_3^3\times(\{0\}\sqcup\mathbf P^1(\mathbb F_3))}.
\]

This is `27×5=135`. Storing the three `u` trits directly and the five-state projective fiber uses nine species bits. The projective-section transition table has the same row multisets as the lexicographic arithmetic oracle, hence gives the same uniform-token Markov operator after state-dependent token relabeling.

A clean-ancilla equality-row source construction requires 50 seven-control fiber rows and 30 six-control updated-trit rows. Using `2k-3` Toffolis for a `k`-controlled flag and computing/uncomputing each flag gives

\[
1100+540=\boxed{1640\text{ Toffolis}},
\]

with a conservative `11,480 T` upper bound at seven `T` gates per Toffoli. This is a 34.57-fold reduction from the earlier 56,700-Toffoli direct table bound, at the cost of one additional species bit. It remains a source-level upper bound, not an optimized minimum or physical synthesis result.

---

## 3480–3481 — exhaustive intrinsic Perkel search on the 57 cap

The exceptional orbit quotient has nineteen switch triangles. This gives the exact carrier fibration

\[
57=19\times3.
\]

The Perkel `Z3×Z19` model also has nineteen three-point columns, but its columns are independent sets rather than triangles.

To test whether the missing cross-fiber Perkel adjacency is intrinsic, each unordered pair of cap species was classified by:

1. its two stabilizer orders;
2. whether it belongs to one switch triangle;
3. the complete `PSp(4,3)` distribution of inner products between its 45-coordinate cover signatures.

These data produce twenty exact pair relations. Every one of their

\[
2^{20}=1{,}048{,}576
\]

unions was tested. None is even 6-regular. Hence no graph in this intrinsic relation algebra is Perkel.

The `19×3` carrier resonance survives, but the Perkel adjacency does not arise from the complete natural relation algebra tested here.

The parallel Pass-3500 atlas supplies a necessary nomenclature firewall. Our cap and the Perkel graph both have 57 vertices; the `SRG(57,14,1,4)` rung in the `μ=4,r=2` parameter ladder is a third object and is nonexistent; the missing Moore graph uses **degree** 57 and would have 3,250 vertices. None of those latter two objects is identified with the cover cap.

---

## 3482 BONKERS — fiber-completed Perkel graph

Add `K3` inside each of the nineteen canonical columns of the explicit Perkel model. The resulting exact graph has:

- 57 vertices;
- degree eight;
- 228 edges;
- diameter three;
- shells `1,8,42,6`;
- exactly nineteen triangles;
- automorphism group order 171;
- spectrum

\[
8^1,\quad(-4)^2,
\]

with each root of

\[
x^3-10x+5
\]

occurring with multiplicity eighteen.

This graph combines the cap’s internal triangle channel with the Perkel cross-fiber channel. It is an exact comparison construction, not a canonical identification of the nineteen cap triangles with the nineteen Perkel columns.

---

## 3483 BONKERS — doubled V4-Latin hardware lift

The fixed inter-block graph is not an arbitrary 24-regular residual. It is a doubled Klein-four selector lift of the anchor `SRG(45,32,22,24)`:

- the selector alphabet is the 16-point `OA(16,3,4,2)`;
- every selector occurs twice among the 32 anchor neighbors;
- every anchor edge instantiates one selected `K3,3`;
- the 6,480 inter-block edges are exactly `720×9`;
- each physical port is used eight times.

This turns the fixed graph into a typed port network with a four-symbol V4 local controller, and gives the exact architecture on which future SAT, RTL, and routing work should operate.

---

## Evidence boundary

Promoted here:

- the canonical 327-representative ledger;
- every legal switch on all 3,547,800 covers;
- the literal component decomposition;
- exhaustive common-A5 restriction mismatch;
- exact fixed-graph port factorization;
- exact carrier-K9 defect-Laplacian collapse;
- exact ten-colour CNF and compact equality-model compilation;
- exact signed mixed-radix basis compiler;
- exact projective arithmetic source compiler and 1,640-Toffoli upper bound;
- exhaustive intrinsic cap relation search;
- both high-risk graph constructions.

Not promoted:

- a ten-colour SAT model or UNSAT proof;
- an optimized Clifford+T minimum;
- a canonical cap-to-Perkel fiber bijection;
- remote CI, PDF, synthesis, placement, hardware, laboratory, detector, fabrication, power, spacetime, or topological-order claims.
