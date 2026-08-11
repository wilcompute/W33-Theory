# Passes 4841–4848 — executed outcomes

## 4841 — the 1080-cycle shell has a 59/49-rank orbital refinement

For one binary Levi minimum, the stabilizer has order 24 in `PSp(4,3)` and order 48 in `PGSp(4,3)`.  Exact stabilizer-orbit enumeration on the complete 1080-word shell gives

\[
\boxed{\operatorname{rank}_{\rm perm}(PSp)=59},
\qquad
\boxed{\operatorname{rank}_{\rm perm}(PGSp)=49}.
\]

The PSp subdegree census is

\[
1^1,\;3^1,\;4^2,\;6^2,\;12^{18},\;24^{35},
\]

while the PGSp census is

\[
1^1,\;3^1,\;4^2,\;6^2,\;12^{16},\;24^{18},\;48^9.
\]

Thus the outer involution fuses ten pairs of PSp suborbits.  The coarse shared-edge statistic of Pass4840 is therefore only a drastic projection of the true orbital algebra.

## 4842 + 4846 — a geometric binary incidence kernel

Let

\[
M\in\{0,1\}^{1080\times360}
\]

be the incidence matrix between binary Levi minimum cycles and induced ternary `K3,3` witnesses.  Its modular ranks are

\[
\operatorname{rank}_{2}M=324,
\quad
\operatorname{rank}_{3}M=359,
\quad
\operatorname{rank}_{5}M=\operatorname{rank}_{7}M=360.
\]

Hence the binary right kernel has dimension 36.  Exact MILP optimization and a complete exclusion certificate prove

\[
\boxed{\ker_{\mathbb F_2}M=[360,36,20]_2}.
\]

The complete minimum shell contains exactly 36 words.  Each minimum word is the set of all 20 induced `K3,3` witnesses contained in a twelve-line graph

\[
\boxed{K_{6,6}\setminus M_6}.
\]

The 36 carriers form one PSp orbit and one PGSp orbit, with stabilizers 720 and 1440.  The 36 minimum words span dimension 35, every one of the 360 `K3,3` witnesses lies in exactly two minimum words, and the XOR of all 36 minima is zero.  Therefore one genuine binary kernel direction lies outside the minimum-word span; it is left unresolved rather than identified from the count 36.

## 4847 — characteristic three has exactly one global relation

Because every binary Levi cycle is incident with exactly three `K3,3` witnesses,

\[
M\mathbf1=0\pmod3.
\]

Since `rank_F3(M)=359`, the right kernel is exactly

\[
\boxed{\ker_{\mathbb F_3}M=\langle\mathbf1\rangle}.
\]

Thus all 360 projective `K3,3` witnesses have one and only one ternary incidence relation: their global sum.

## 4848 — exact real incidence spectrum

Two `K3,3` columns share at most one binary cycle, so

\[
M^TM=9I+A,
\]

where `A` is the connected 18-regular graph on the 360 witnesses in which adjacency means sharing a binary Levi cycle.  It has 3240 edges, diameter four, and the uniform distance-shell profile

\[
1,18,108,227,6.
\]

Its exact adjacency spectrum is

\[
18^1,
(-5)^{60},
(-2)^{84},
(-1)^{81},
4^{64},
\left(\frac{13\pm\sqrt{97}}2\right)^{20},
\left(\frac{1\pm\sqrt{73}}2\right)^{15}.
\]

Consequently the squared singular values of `M` are

\[
27^1,
4^{60},
7^{84},
8^{81},
13^{64},
\left(\frac{31\pm\sqrt{97}}2\right)^{20},
\left(\frac{19\pm\sqrt{73}}2\right)^{15}.
\]

The 360-witness graph is not distance-regular despite its uniform distance-shell sizes.  Thus the rank collapses in characteristics two and three are genuinely modular phenomena rather than characteristic-zero linear dependence.

## 4843 + 4845 — the first cross-cell shell reconstructs the global GQ quotient

Pass4832's dependency code on 540 intrinsic repetition classes has dimension 141.  Its 135 disjoint local minimum relations are independent, leaving exactly

\[
141-135=6
\]

cross-cell dimensions.  These are precisely

\[
W_6=[27,6,12]_2,
\]

whose enumerator is

\[
1+36z^{12}+27z^{16}.
\]

On the 540 class carrier the nonzero shell weights become

\[
36z^{180}+27z^{240}.
\]

The residual six-dimensional generator has 135 zero columns (the hot classes) and 27 distinct nonzero column types, each repeated on 15 cold classes.  In every local cell, its three cold classes carry three line types.  Grouping the 135 cells by their unordered triple of line types yields exactly 45 triples, each with multiplicity three.  Therefore

\[
\boxed{27\text{ lines}+45\text{ line-triples}=GQ(4,2)}
\]

is reconstructed from the code shells themselves.

This sharply refines Pass4839: the local weight-two/minimum-weight-four shells alone are too symmetric, but the first cross-cell shell is already sufficient.  At class level the combined-shell automorphism group is

\[
\boxed{S_3^{45}:\operatorname{Aut}(GQ(4,2))},
\]

with `|Aut(GQ(4,2))|=51840`.  The `S3^45` kernel permutes the three indistinguishable sheet cells above each recovered GQ point.  This is not yet the full 2025-coordinate code automorphism group because physical repetition classes still carry additional internal coordinate symmetry.

## 4844 — exact metric of C399/CLevi

The invariant inclusion of Pass4833 gives

\[
\dim(C_{399}/C_{\rm Levi})=335.
\]

Every local `[15,3,7]_2` cell has nonzero weights

\[
7,7,7,8,8,8,15.
\]

Therefore an ambient weight-14 word consists of exactly two local weight-seven singleton generators.  Since the outer code `O21=[27,21,3]_2` has no weight-one or weight-two words, those two singleton generators must carry the same quotient-line label.  There are 15 singleton positions over each of 27 quotient lines, so the complete ambient minimum shell has

\[
\boxed{27\binom{15}{2}=2835}
\]

words.

Since `d(C_Levi)=96`, no two distinct weight-14 words differ by a Levi word.  Hence the quotient physical coset metric has

\[
\boxed{d(C_{399}/C_{\rm Levi})=14}
\]

and exactly 2835 minimum cosets.  No invariant direct-sum splitting is inferred.

## Combined structural statement

The local-to-global reconstruction now has an exact threshold:

\[
\text{weight-2 repetition shell}
+\text{135 local weight-4 relations}
\quad\text{does not recover GQ},
\]

but

\[
\text{those shells}+W_6\text{ cross-cell sector}
\quad\Longrightarrow\quad
GQ(4,2).
\]

Above that quotient, the binary/ternary minimum-cycle incidence produces a new modular code pair: a nontrivial `[360,36,20]_2` relation code in characteristic two and only the global all-one relation in characteristic three.  This is a concrete example of the project’s recurring principle that the same finite carrier can have radically different protected relation spaces in different characteristics.
