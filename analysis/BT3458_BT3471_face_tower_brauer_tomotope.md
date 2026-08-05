# Passes 3458–3471 — Face-tower reconstruction, modular descent, noncommuting amplitudes, and the tomotope boundary

## Status

This packet executes all five requested continuations and two additional high-risk constructions after reconciling Passes 3418–3457 and the merged cover/Perkel lane.

The exact verifier reports **PASS 12/12**. It independently reconstructs the 45-point Hermitian surface, the 240 filled-face orbit, the full `PSp(4,3)` actions on 240 and 120 states, the rank-five association scheme, the characteristic-three endomorphism algebras, the product-code coset census, and the oriented-tetrahedron incidence surface.

The live boundaries remain

\[
\boxed{389\leq R_{\rm defect}\leq436},
\qquad
\boxed{10\leq\chi(H)\leq11}.
\]

No exact radius endpoint, ten-colour decision, simple-module label for the 81-dimensional modular summand, optimized FPGA result, tomotope monodromy identification, or physical interpretation is promoted.

---

## 3458 — the level-zero Delsarte relaxation is exhausted

The previous packet identified the labelled minimum-defect diameter with the fifth generalized covering radius of the ternary support code

\[
K=\operatorname{im}[R\;N]\subseteq\mathbb F_3^{720},
\qquad \dim K=284.
\]

After scalar extension to \(\mathbb F_{243}\), one local filled-face quotient has length enumerator

\[
1+726z+58{,}322z^2.
\]

The 240-fold product sphere first reaches the quotient size at radius 389. Because the local metric is transitive, the uniform fractional-cover solution is optimal for the level-zero covering LP. Therefore the first Delsarte/fractional relaxation reproduces exactly the existing lower bound:

\[
\boxed{R_{\rm frac}=389}.
\]

It cannot prove \(R\geq390\).

The useful closure is the complete symmetry deck for the next SDP level. The filled-face action has coherent rank ten, and its antipodal quotient is a symmetric rank-five association scheme with valencies

\[
\boxed{1,36,27,2,54}.
\]

Its exact eigenmatrix rows, written with multiplicity first, are

\[
\begin{array}{c|rrrrr}
1&1&36&27&2&54\\
15&1&-12&3&2&6\\
20&1&0&9&-1&-9\\
24&1&6&-3&2&-6\\
60&1&0&-3&-1&3.
\end{array}
\]

The complete intersection tensor is frozen in the JSON certificate. It is the exact small orbital input needed for a symmetry-reduced two-point/Lasserre-style SDP; no 240-factor matrix needs to be carried explicitly.

---

# 3459–3460 BONKERS — the canonical face tower recovers W33

The action of `PSp(4,3)` on the 240 filled faces has stabilizer subdegrees

\[
1,18,27,4,18,108,1,27,18,18.
\]

The second singleton orbital is a canonical fixed-point-free involution. It partitions the filled faces into 120 antipodal pairs:

\[
240\longrightarrow120.
\]

On the 120 pairs, the valency-two relation is exactly

\[
\boxed{40K_3}.
\]

Quotienting those forty triangles gives a faithful degree-40 action with subdegrees

\[
1,12,27.
\]

The valency-12 quotient graph satisfies

\[
\boxed{\operatorname{SRG}(40,12,2,4)},
\]

so it is the original W33 graph. This is an objectwise reconstruction, not a parameter match:

\[
\boxed{
240\text{ filled faces}
\longrightarrow
120\text{ antipodal pairs}
\longrightarrow
40\text{ W33 points}.
}
\]

Every W33 point therefore carries six filled faces, arranged as three antipodal pairs.

### Exact block laws

For two quotient fibres of size three:

- over every W33 edge, relation 1 is the full block \(J_3\);
- over every W33 nonedge, relation 2 is a permutation matrix;
- relation 4 is the complementary block \(J_3-P\).

The relation-2 matching connection has nontrivial triangle holonomy on the 3,240 triangles of the W33 complement:

\[
\boxed{1080\text{ identity loops}+2160\text{ transposition loops}},
\]

with no three-cycle loops.

This is the first exact nontrivial transport bundle to emerge from the filled-face carrier. The earlier scalar magnetic searches had no access to this `S3` matching holonomy.

### Local tetrahedral chart

The stabilizer of one W33 point has order

\[
648=3^3\cdot24.
\]

Its induced action on the six faces over that point is exactly the `S4` action on the six edges of a tetrahedron. The three antipodal face pairs correspond to the three pairs of disjoint tetrahedron edges. The quotient action on those three pairs is `S3`, with kernel `V4`.

Thus each W33 point carries the canonical local chart

\[
\boxed{3^3:S_4},
\]

not merely a chosen four-object `S4` analogy.

---

## 3461 — characteristic-three Brauer descent

### The symmetric 120-state module

The five ordinary association-scheme characters all reduce modulo three to

\[
\boxed{(1,0,0,2,0)}.
\]

Consequently the five-dimensional endomorphism algebra becomes local. Its Jacobson radical has dimensions

\[
\boxed{\dim J=4,\quad\dim J^2=1,\quad J^3=0}.
\]

The endomorphism-algebra Loewy profile is therefore

\[
\boxed{1\mid3\mid1}.
\]

A local endomorphism ring implies that the 120-dimensional pair permutation module is indecomposable over \(\mathbb F_3\), even though in characteristic zero it separates into dimensions

\[
1+15+20+24+60.
\]

### The antisymmetric 120-state module

The antipodal involution splits the 240-face module into symmetric and antisymmetric 120-dimensional summands. The antisymmetric endomorphism algebra has basis \(1,x,y\) with multiplication

\[
x^2=2y,\qquad xy=y,\qquad y^2=2y
\quad\text{over }\mathbb F_3.
\]

The idempotent \(2y\) has rank 81. Its complement has rank 39. Hence

\[
\boxed{M_-=M_{81}\oplus M_{39}}.
\]

The 39-dimensional summand has endomorphism ring

\[
\boxed{\mathbb F_3[\varepsilon]/(\varepsilon^2)},
\]

so it is indecomposable and glues the ordinary 15- and 24-dimensional sectors. The 81-dimensional summand has scalar endomorphism ring in the computed orbital algebra, but it is deliberately called a brick rather than a simple module until an independent MeatAxe composition-series calculation is executed.

The complete ordinary fingerprint of the 240-face action is

\[
\boxed{1+15_a+15_b+20+2\cdot24+60+81}.
\]

---

## 3462 — the full-\(M_4\) chromatic dead end and escape route

Simply enlarging a trivial local fibre from a commutative algebra to `M4` cannot improve the old invariant chromatic frontier. Twirling a globally `PSp(4,3)`-invariant trivial-bundle weighting returns it to the existing three block spectral cones.

The face tower supplies the missing ingredient: objectwise noncommuting transport.

Map the six local filled faces to the six transposition permutation matrices in the four-dimensional tetrahedral representation. These matrices generate the ten-dimensional image of the group algebra of `S4`. Adjoining the null-conic dual sign

\[
D=\operatorname{diag}(1,1,-1,-1)
\]

gives

\[
\boxed{\langle\text{six transpositions},D\rangle=M_4(\mathbb Q)}.
\]

Therefore the new amplitude compiler has:

- six objectwise local matrix tokens per W33 point;
- three antipodal pairs of commuting disjoint transpositions;
- a nontrivial `S3` matching connection on W33 nonedges;
- 2,160 transposition-holonomy complement triangles;
- full `M4` local amplitude reach after adding the conic sign.

This closes both earlier brick walls:

1. scalar phases are too weak;
2. an untwisted full-`M4` fibre twirls back to the old cones.

The resulting bundle is a concrete noncommuting candidate, not yet a certificate for the live 45-block chromatic graph.

---

## 3463 — formal order-three hardware surface

The packet publishes a literal 200-entry eight-mask baseline and compares it exhaustively with the factored Kronecker compiler. It also instantiates the characteristic-three five-channel map three times and proves the source target

\[
J^3=I
\]

over all

\[
3^5=243
\]

valid ternary input states.

The exact source comparison is:

\[
27\cdot25=675\text{ naive symbol entries},
\qquad
8\cdot25=200\text{ literal mask entries}.
\]

The factored engine uses the four entries of one \(2\times2\) primitive rather than either table.

The evidence workflow runs:

- Icarus over all 200 symbol entries and 1,944 mask/state order-three cases;
- Yosys SAT with formal assumptions \(0\leq x_i\leq2\);
- ICE40 synthesis of the factored and literal-table versions;
- all focused Python regressions;
- all three canonical manuscript builds.

No area, timing, or PDF result is promoted until those remote jobs complete.

---

## 3464 — exact tomotope product-code falsifier

The `A2`–conic product code has parameters

\[
[12,6,4]_3.
\]

Its 36 weight-four words give 18 projective supports. Its dual has minimum weight three. Exhausting all

\[
\binom{12}{3}2^3=1760
\]

weight-three ambient vectors and sorting them by dual coset gives the multiplicity histogram

\[
1^{48},\qquad2^{312},\qquad4^{270},\qquad8^1.
\]

Because scalar multiples share one support, the maximum number of projective triples in any dual coset is four. A tomotope requires sixteen triangular face supports. Therefore

\[
\boxed{\text{no dual-product-code coset can realize the sixteen tomotope faces}.}
\]

There is also a group-order obstruction to a faithful realization inside the visible product action:

\[
|S_3\times S_4|=144,
\qquad
|\operatorname{Aut}(\text{tomotope})|=96,
\qquad
96\nmid144.
\]

The proposed direct product-code/tomotope identification is therefore closed negatively.

---

# 3465 BONKERS — the oriented-tetrahedron Reye surface

The failed code-support identification leaves behind a stronger coordinate bridge.

The twelve product coordinates form a \(3\times4\) grid. Interpret the three rows as the three perfect matchings of a tetrahedron and the four columns as its vertices. A matching and a vertex determine the unique matching edge incident with that vertex, oriented away from the chosen vertex. Hence

\[
\boxed{3\times4\cong\{(i,j):i,j\in\{0,1,2,3\},\ i\neq j\}},
\]

the twelve oriented tetrahedron edges.

On these twelve coordinates define sixteen triples:

- four outgoing stars;
- four incoming stars;
- eight directed 3-cycles, two orientations on each three-vertex subset.

Every triple contains three coordinates and every oriented edge lies in four triples. Thus the construction is exactly

\[
\boxed{12_4\,16_3}.
\]

The parity-matched index-two subgroup of `S3 x S4`, of order 72, preserves this star/cycle incidence surface.

This is an explicit Reye-style coordinate model built from the product grid. It does **not** contradict the repository's earlier negative flag search: the archived search proves that the Reye skeleton alone cannot recover the tomotope's four involutions and intersection condition. The missing datum remains the cell/orientation layer of the true 192-flag monodromy.

Thus the final boundary is sharp:

- product-code supports \(\not\to\) tomotope faces;
- product-grid coordinates \(\to\) an exact oriented \(12_4\,16_3\) surface;
- the extra flag/cell cocycle is still required for the tomotope itself.

---

## Published surface

This packet contains:

- `analysis/bt3458_3471_face_tower_brauer_tomotope.py`;
- frozen exact JSON including the full intersection tensor;
- focused pytest regression;
- a generated literal symbol baseline;
- exhaustive RTL testbench;
- formal order-three harness;
- synthesis and PDF evidence workflow;
- shared theorem insert for all three canonical papers;
- public-index source insert.

## External context

The generalized-covering-radius scalar-extension equivalence follows Elimelech–Firer–Schwartz. The next SDP route is aligned with the symmetry-reduced covering-code hierarchy developed by Gijswijt–Polak. GAP/CTblLib and MeatAxe remain independent row-label and composition-series tools; this packet does not replace those checks with guesses. The tomotope boundary follows the distinction in Monson–Pellicer–Williams between symmetry, monodromy, and covering data.
