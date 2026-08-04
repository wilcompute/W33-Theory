# Passes 3376–3389 — Cohomology normal forms, barycentric phase loss, and signed-torus closure

## Status

This packet executes the five requested continuation fronts, two independent high-risk constructions, and several chained consequences after reconciling the parallel Passes 3364–3375 Clebsch–Petersen packet. The exact source verifier reports **9/9 checks passed**. The chromatic boundary remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

No source-level calculation is promoted to a terminal colouring decision, quantum speedup, observed FPGA result, successful PDF, laboratory result, spacetime signature, or physical phase-bit identification.

## 3376–3377 — exact minimum-defect word metric

For one filled triangle with coefficient module

\[
A=\mathbb F_3^5,\qquad |A|=243,
\]

a flat triple has minimum-defect length zero, one, or two. The exact local enumerator is

\[
\boxed{1+726z+58{,}322z^2}.
\]

The 240 filled faces partition the 720 port edges, so the complete flat-space enumerator is

\[
(1+726z+58{,}322z^2)^{240}.
\]

Consequences:

- exact flat-space diameter: **480**;
- exact mean local length under the uniform distribution: \(117370/59049\);
- every flat connection has a deterministic normal form with at most two minimum defects per filled face.

For the quotient by the 220-dimensional coboundary space, exact sphere counting gives

\[
\sum_{j=0}^{388}[z^j](1+726z+58{,}322z^2)^{240}
<3^{2180}
\]

but the same sum through radius 389 is at least \(3^{2180}\). Therefore the minimum-defect Cayley diameter on switching classes satisfies

\[
\boxed{389\leq D_{H^1}\leq480}.
\]

The exact quotient covering radius inside this interval remains open.

## 3378 — cohomological nonseparable chromatic surface

A minimum defect is a nontrivial \(C_3^5\)-valued voltage assignment. Its voltage subgroup is the order-three line \(\langle v\rangle\), not all of \(C_3^5\). The full derived graph therefore has

\[
45\cdot243=10{,}935
\]

vertices but splits into

\[
\boxed{81\text{ connected components of }135\text{ vertices}.}
\]

Each component is 32-regular with 2,160 edges. A minimum defect has nonzero holonomy on exactly 42 of the 5,280 base triangles. Those triangles lift to 9-cycles; the remaining triangles lift threefold. Hence each component has

\[
(5280-42)\cdot3=15{,}714
\]

triangles.

Fourier decomposition across the \(C_3\) fibre gives one untwisted 45-state block and two conjugate magnetic blocks. The exact moments are

\[
\operatorname{tr}A^2=1440,
\qquad
\operatorname{tr}A^3=31{,}680,
\]

for the untwisted block, while each magnetic block has

\[
\operatorname{tr}M^2=1440,
\qquad
\operatorname{tr}M^3=31{,}302.
\]

The deficit

\[
31{,}680-31{,}302=378=42\cdot9
\]

proves that the magnetic weighting is genuinely nonseparable and is not switching-equivalent to the untwisted adjacency. It supplies an exact profile-sensitive candidate surface beyond the separable Hoffman obstruction, but no dual certificate above nine has yet been found.

The 135-vertex count does **not** identify this voltage component with the 135 Hamming-orbit species: the voltage component has degree 32, while the Hamming-orbifold walk has degree 10.

## 3379–3380 — exact Q15 barycentric phase-loss theorem

For

\[
\tau(x_1,x_2,x_3,x_4,x_5)=(-x_4,1-x_3,1-x_2,-x_1,x_5),
\]

the 243 ternary words form 135 orbits: 27 fixed and 108 paired. Under the block-one-hot embedding into \(Q_{15}\), the normalized orbit barycentres take only 108 distinct values. The exact fibre profile is

\[
\boxed{81\text{ singleton barycentres}+27\text{ double barycentres}.}
\]

The barycentre shells are:

- 27 fixed singleton fibres, squared norm 5;
- 54 distance-two singleton fibres, squared norm 4;
- 27 distance-four double fibres, squared norm 3.

For every double fibre, take the coordinatewise missing ternary symbols in the first four blocks. They satisfy

\[
m_4=-m_1,\qquad m_3=1-m_2,
\]

and together with the fifth symbol give one point of \(\mathbb F_3^3\). This missing-symbol map bijects the 27 ambiguous barycentres with the 27 fixed points of \(\tau\).

The two orbit species over an ambiguous barycentre are separated exactly by

\[
\boxed{h=(x_1+x_4)(x_2+x_3-1)\in\{1,2\}.}
\]

This quantity is invariant under \(\tau\), so the 54 ambiguous species form a canonical two-sheeted cover of the fixed affine flat.

## 3381 — equivariant minimum-defect presentation

For scalar coefficients the three omitted-edge support vectors on each filled face span its two-dimensional flat plane and satisfy one relation. Globally:

\[
0\longrightarrow\mathbb F_3[240\text{ faces}]
\longrightarrow\mathbb F_3[720\text{ supports}]
\longrightarrow Z^1\longrightarrow H^1\longrightarrow0.
\]

The ranks are

\[
720-240=480,
\qquad
480-44=436.
\]

This is a canonical \(PSp(4,3)\)-equivariant permutation-module presentation. Tensoring by the five-dimensional coefficient label gives

\[
3600\text{ generator coordinates},\quad
1200\text{ local relations},\quad
220\text{ coboundary relations},
\]

and therefore

\[
\boxed{3600-1200-220=2180}.
\]

Thus the complete logical gauge sector is generated by minimum defects with 1,420 independent relations. This is the exact module-level answer presently available; a full irreducible character decomposition of the 720-support module remains a separate computation.

## 3382 — generated publication manifest

The three canonical manuscripts previously duplicated the same growing list of current-frontier inserts. The packet replaces those repeated tails with one ordered manifest:

`analysis/W33_CURRENT_FRONTIER_MANIFEST.tex`.

The authoritative JSON manifest checks order, uniqueness, file existence, wrapper reachability, body reachability, and public-index identifiers. The parallel Passes 3364–3375 insert is preserved in the same manifest before this packet's insert. Historical manuscript ledgers remain unchanged.

## 3383 BONKERS — the 81-by-135 voltage constellation

The minimum defect naturally creates an \(81\times135\) constellation:

\[
10{,}935=81\cdot135.
\]

The factor 81 is not inserted numerologically: it is the quotient \(|\mathbb F_3^5|/|\langle v\rangle|=243/3\), while 135 is the connected component size \(45\cdot3\). This produces 81 isomorphic components carrying conjugate magnetic character blocks.

The tempting identification with the 81 logical code coordinates and 135 Hamming-orbit species is explicitly rejected without an equivariant crosswalk. Degree and local moment tests already distinguish the voltage component from the Hamming quotient.

## 3384 BONKERS — hidden signed ternary torus

Barycentric aggregation is strongly lumpable for the weighted 135-state Hamming-orbifold walk. The exact operator decomposes as

\[
\boxed{W_{135}\cong B_{108}\oplus D_{27}}.
\]

The barycentric block has spectrum

\[
10^1,\;7^6,\;4^{18},\;1^{32},\;(-2)^{33},\;(-5)^{18}.
\]

Orienting the 27 double fibres by \(h=1\) versus \(h=2\) identifies the lost sector with a signed Cayley operator on the fixed flat \(\mathbb F_3^3\):

\[
\boxed{D_{27}=C_3^{(3)}-C_3^{(1)}-C_3^{(2)}}.
\]

Its edge weights are +1 on \(\pm e_3\) and -1 on \(\pm e_1,\pm e_2\). Its exact spectrum is

\[
4^4,\;1^{12},\;(-2)^9,\;(-5)^2.
\]

This is an exact finite signed-torus theorem. The \((--+)\) sign pattern is not promoted to a physical spacetime metric.

## 3385 — chained three-shell compression

The 108-state barycentric walk itself has an equitable three-shell quotient on the fixed, distance-two, and ambiguous barycentre shells:

\[
\boxed{
\begin{pmatrix}
2&8&0\\
2&4&4\\
0&4&6
\end{pmatrix}}
\]

with shell sizes \((27,54,27)\), stationary masses \((27,108,108)\), and spectrum \((10,4,-2)\). The complete chain is therefore

\[
243\longrightarrow135\longrightarrow108\longrightarrow3,
\]

while the 27-dimensional signed torus records precisely what the 135-to-108 barycentric map discards.

## Literature cross-checks

The exact barycentric lumping is consistent with recent work on when equitable Markov aggregation commutes with Szegedy quantization. The cohomological magnetic surface belongs to the broader Hermitian weighted-adjacency framework used for spectral chromatic bounds. Voltage assignments are naturally homological objects, and connectedness of a derived cover is controlled by the generated voltage subgroup. These references motivate the constructions; every numerical and finite statement above is independently regenerated from repository source.

## Reproduction

```bash
python analysis/bt3376_3389_cohomology_tau_frontier.py --json /tmp/results.json
cmp /tmp/results.json data/PART_BT3376_BT3389_COHOMOLOGY_TAU_results.json
python tools/integrate_bt3376_bt3389.py
python tools/audit_w33_current_frontier.py
python -m pytest -q tests/test_bt3376_3389_cohomology_tau_frontier.py
```
