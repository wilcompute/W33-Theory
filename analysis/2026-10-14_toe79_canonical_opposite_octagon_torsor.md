# TOE79 — Canonical GQ(3,3) antipode map: 27 opposite points = 27 native octagons

**14 October 2026.** Exact W33 geometric construction, explicit full symplectic group orbit and finite incidence theorem. This is a genuine canonical address-space bridge; it is **not** a physical Theory of Everything.

## The formerly missing canonical identification

TOE77–78 established that two native theta-graph chords lie in exactly 27 common W33 Levi eight-cycles, with a regular normal extraspecial Heisenberg \(H_{27}\) acting on those cycles, and that a unique invariant \(\mathrm{SRG}(27,10,1,5)\) graph recovers the E6 cubic-surface 27-line incidence.

The **original theta-chord edge indices are 5 and 6**. They are both incident to the **same W33 projective point, indexed 1**, and to two of its four isotropic lines. This is the key underlying reason that the unordered flag-edge pair has a \(\mathrm{PGSp}(4,3)\) orbit of exactly **240**, not a coincidence with W33's 240 ordinary collinearity edges:
\[
\boxed{40\;\text{W33 points}\times\binom{4}{2}\;\text{incident line pairs}=240}.
\]

Choose *any* W33 point \(p\), and *any* unordered pair of distinct native Levi incidence edges \(\{e_1,e_2\}\) through it. The point \(p\) has 12 collinear neighbors and exactly **27 noncollinear points** \(q\). In the generalized quadrangle \(GQ(3,3)\), for each line through \(p\) and each point \(q\) not on that line, exactly one point of that line is collinear with \(q\). Consequently, for every **noncollinear** \(q\), the chosen pair of initial lines determines exactly one shortest eight-step cycle
\[
p\to L_1\to r_1\to M_1\to q\to M_2\to r_2\to L_2\to p.
\]

Conversely, every Levi eight-cycle containing both \(e_1,e_2\) has a **unique antipodal point** \(q\) at graph distance four along that cycle, and \(q\) is necessarily noncollinear with \(p\) because the generalized-quadrangle Levi graph has girth eight. Thus for **every** \((p,\{e_1,e_2\})\) there is a **canonical bijection**
\[
\boxed{\{\text{27 octagons through both }e_1,e_2\}
\longleftrightarrow
\{\text{27 W33 points noncollinear with }p\}}
\]
with no choice of labels, no H27 generator gauge, and no reference to a cubic-surface frame numbering.

The proof is equivariant under the native symplectic automorphism group because every automorphism preserves eight-cycles, the two incident edges, the marked root \(p\) and the opposite vertex \(q\).

## All 6480 decorated octagons form one homogeneous orbit

The exact source enumerates all **1620** undirected octagons in the native 80-vertex Levi graph and, for **each of their four point-vertices**, recovers its pair of incident cycle edges and the opposite point. An exhaustive map then confirms:

- **40** base W33 points.
- **6** unordered pairs of four flags at each point.
- **27** unique antpodal octagons per such pair; the antipodes exhaust *exactly* the full noncollinear 27-point shell.
- **240** marked \((p,\{e_1,e_2\})\) flags-pair objects.
- **6480** marked \((p,\{e_1,e_2\},q)\) objects, exactly equal to \(1620\times4\).

Moreover, by applying the **actual native symplectic transvection and similitude generators**, the program constructs one orbit of size **6480** on these decorated configurations. This confirms the homogeneous space
\[
\boxed{\mathrm{PGSp}(4,3)/D_8,\qquad 51840/8=6480}
\]
with the complete concrete stabilizer chain
\[
\begin{array}{c|r|r}
\text{fixed geometric data}&\text{orbit size}&\text{stabilizer order}\\ \hline
\text{none}&1&51840\\
p&40&1296\\
p\text{ and unordered flag pair}&40\cdot6=240&216\\
p,\text{ pair, antipode }q&40\cdot6\cdot27=6480&8.
\end{array}
\]

The order-216 stabilizer is exactly the \(H_{27}\rtimes D_8\) subgroup identified by the preceding native group-law certificate; its \(H_{27}\) acts regularly on the noncollinear opposite-point shell. The **point stabilizer** has order \(1296=27\cdot48\), naturally matching the project's H27 affine normalizer, and its **pair stabilizer** has index six, reflecting the six unordered choices of two of four incident isotropic lines. The D8 complement is the 2-set stabilizer subgroup, not a Q8 Clifford complement.

This is a **canonical geometric** way to connect the TOE77–78 27-octagon cubic-surface structure to the previously established Payne \(H_{27}\) on W33's opposite shell. It eliminates a pure numerical-coincidence concern and gives a coherent address-space route into the cubic-surface 27-line graph and 45 tritangents, previously verified by an independent quadratic \(F_2^6\) construction. The **operator H27** in E6 trinification remains a separate, center-scalar 3D Schrödinger representation requiring its own intertwiner.

## Why the 6480 count is interesting but not yet physics

The project already contains other 6480-dimensional cochain bookkeeping and 27/40/216/1296 structures. This construction derives **6480 as an actual native incidence homogeneous space**, not merely an observed matching number. However, *an equality of dimensions does not provide a canonical chain map*, fermionic Hilbert space, action functional, anomalies, or experimental observable. Connecting any 6480-entry cochain model to these rooted eight-cycles would require an explicit boundary/coboundary intertwiner with preserved degree and group action.

## Reproducibility and boundary

- Source: \`analysis/w33_20261014_toe79_canonical_antipode_octagon.py\`
- Test: \`tests/test_w33_20261014_toe79_canonical_antipode_octagon.py\`
- CI: \`.github/workflows/w33_toe79_antipode_octagon.yml\`
- JSON: \`data/w33_20261014_toe79_canonical_antipode_octagon.json\` regenerated in workflow artifacts.

The map and complete generator orbit are exact finite combinatorics. **No physical particle spectrum, all-80-site interacting gauge vacuum, 4D chiral spin structure, or classical Riemann-hypothesis proof is established.**

## Five independent next experiments

1. Verify a completely explicit **equivariant graph isomorphism** from the canonical 27 noncollinear points to the native 27-octagon tritangent graph, and compare it with the project's previous Payne-H27/cubic-surface frame map, recording stabilizer gauges.
2. Determine the complete native **six-dimensional orbital adjacency algebra**, its exact structure constants and the \(1+4+4+6+6+6\) decomposition of the 27 address space, especially the six-dimensional E6 root-reflection sector.
3. Build and independently calibrate an **80-mode photonic interferometer** showing the exterior-driven 120°→π flux migration and null controls on generic three-arm and rewired W33-equivalent graphs.
4. Test whether the group-equivariant rooted-octagon \(6480\)-space admits a nontrivial, degree-preserving **map to the separate Čech/cohomology ledger**, rather than equating dimensions.
5. Develop an actual **local 4D spinor/gauge dynamics** coupling H27 address translations to the ternary trinification operator H27, including antiunitary center inversion, anomalies and stable spectral gaps.
