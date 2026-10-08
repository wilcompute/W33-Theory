# 2026-10-08 — The 27+13 W33 shell, the two H27 representations, and the C8 Heisenberg-13 radical

**Outcome:** Five user-requested follow-up fronts executed as precisely scoped, reproducible calculations. The strongest *new comparative calculation* is a concrete order-27 subgroup of the characteristic-three reduction of the previously identified 13-dimensional rational Lie radical and an explicit homomorphism from the W33 elation H27 that passes all 729 group multiplication checks. **This is not an identification of the 13 projective polar points with the 13-dimensional Heisenberg Lie algebra.** It also does not identify the regular E6/W33 27-address *representation* with the central-character-locked trinification H27 operator representation. The latter is forbidden without commutant dressing (already established in the repository).

Executable producer: `analysis/w33_20261008_h27_h13_five_frontiers.py`. Frozen calculation data: `data/w33_20261008_h27_h13_five_frontiers.json`. Regression tests: `tests/test_w33_20261008_h27_h13_five_frontiers.py`.

## Attribution and current-repository cross-check

Earlier internal sources **already own**:

- `analysis/THE_27_FOLD_WAY.md` and Passes 369–371: the point-centered **\(1+12+27\)** W33 shell; nonabelian order-27 regular elation H27 acting on 27 opposite points; a machine-verified **equivariant torsor isomorphism to the 27 E6 cubic-surface labels** and the 648-order Clifford normalizer. This is **not new** to this packet.
- `analysis/PASS5102_5109_EXECUTED_OUTCOMES.md` (5105): the state H27 and program \(\mathbf F_3^3\) inside the order-81 unipotent, with detailed subgroup intersection and action. Again previously completed.
- `analysis/2026-09-21_address_operator_h27_roles.md`, `analysis/2026-09-21_e8_matter81_h27_address_operator_compiler.md`: distinction between the **regular/Payne address H27** and **trinification/operator H27** whose center equals \(Z(E_6)\) and acts on the E6 27 as nine copies of a three-dimensional Schrödinger representation. These actions are not linearly intertwined.
- `analysis/PASS11043_COMMUTANT_DRESSING_REGULAR_H27.md`: exact 9D latent module \(A_9=\chi_{00}+\chi_{10}+\chi_{20}+V_\omega+V_{\omega^2}\) converting \(V_\omega\otimes A_9\) into \(\mathrm{Reg}(H_{27})\). A *representation change*, not equality of the original action.
- `analysis/2026-10-08_five_frontiers_deep_jacobi_and_equivariance.md`: newly landed eight-cycle rational Lie algebra \(\mathfrak{sp}(6,\mathbf Q)\ltimes\mathfrak h_{13}(\mathbf Q)\), including an exact 13D Heisenberg radical, six symplectic conjugate pairs and one center.
- Literature external prior: **W(3,q) elation quadrangles**, point polar planes and nonabelian \(q^3\) Heisenberg regular groups for odd \(q\), e.g. [Bamberg's explanatory matrix formula](https://symomega.wordpress.com/2010/07/11/generalised-quadrangles-v-elation-generalised-quadrangles/) and [FinInG/GAP elation generalized quadrangles](https://fossies.org/linux/gap/pkg/fining/doc/chap12_mj.html).

## I. The precise \(40=13+27\) point partition

Take the standard alternating form \(J\) on \(\mathbf F_3^4\),

\[
J=\begin{pmatrix}0&0&0&1\\0&0&1&0\\0&-1&0&0\\-1&0&0&0\end{pmatrix},\quad
p=[1:0:0:0].
\]

Its polar projective plane \(p^\perp=\{[x:y:z:0]\}\cong PG(2,3)\) has \((3^3-1)/(3-1)=13\) points. Outside this plane, every point has a unique affine representative \([x:y:z:1]\) and there are exactly \(3^3=27\) of them. This is the same W33 \(1+12+27\) graph-neighborhood decomposition after separating the anchor \(p\) from the other 12 collinear points.

A concrete point-fixed symplectic unipotent group is

\[
U(a,b,c)=\begin{pmatrix}
1&a&b&c\\ 0&1&0&b\\0&0&1&-a\\0&0&0&1
\end{pmatrix},\quad a,b,c\in\mathbf F_3.
\]

All 27 matrices satisfy \(U^TJU=J\), fix \(p\), preserve the polar plane and act **sharply transitively on the other 27 projective points**. Their law is

\[
U(a,b,c)U(a',b',c')=
U(a+a',b+b',c+c'+ab'-ba')
\]

and \([U(1,0,0),U(0,1,0)]=U(0,0,2)\). The center \(\{U(0,0,c)\}\) fixes the 13 polar-plane points **pointwise** and partitions the affine 27 into **nine 3-point orbits**. (Noncentral elements preserve the polar plane as a set but need not fix its points.) All these assertions are independently enumerated against the committed symplectic W33 40-point geometry.

**Novelty tier:** this matrix model and nine-center-orbit reconstruction are independent reproducibility witnesses for **existing** elation-GQ facts, not claims of discovery.

## II. An actual H27 inside the mod-3 Heisenberg-13 radical

The prior eight-cycle current Lie algebra contains an exact 13-dimensional Heisenberg radical over \(\mathbf Q\):

\[
\mathfrak h_{13}=\langle r_1,\dots,r_6,v_1,\dots,v_6,z\rangle,
\quad [r_i,v_j]=\delta_{ij}z,\quad z\text{ central}.
\]

This consists of **six conjugate pairs plus a single center**. In the exact adapted eight-dimensional matrix basis, \(r_i=E_{0i}\), \(v_i=E_{i7}\), \(z=E_{07}\), \(i=1,\ldots,6\).

Choose the explicitly displayed integral Heisenberg basis and reduce *that chosen lattice* modulo 3. The resulting unipotent group has \(3^{13}=1,594,323\) elements and the expected extraspecial, exponent-three Heisenberg structure. **No statement is made that this integral lattice is the uniquely natural reduction of the original graph-current integer lattice.** For the selected \(r_1,v_1,z\) subalgebra, an order-27 subgroup consists of matrices \(T(a,b,d)\in GL_8(\mathbf F_3)\) with diagonal identity and entries \((0,1)=a\), \((1,7)=b\), \((0,7)=d\). Its law is \(d\mapsto d+d'+ab'\). The explicit isomorphism

\[
\boxed{\Phi:U(a,b,c)\mapsto T(a,b,2c-ab)}
\]

respects **all 729** pairwise products in the two groups, verified exhaustively. This is a genuine, non-numerological **abstract group-level bridge** from the W33 point-elation Heisenberg group to an H27 subgroup of an integral mod-3 form of the local 13D Lie radical.

**Crucial limits:** choosing this symplectic 2-plane in the radical is not canonical; no global W33 \(PSp(4,3)\)-equivariant embedding of all point-centered H27s into one \(\mathfrak h_{13}\) is proved, and the 13 projective points of \(PG(2,3)\) are not 13 basis vectors of the Lie algebra in any exhibited natural geometric representation. The equal numeral **13** therefore remains a possible lead, *not an identification*.

### How the two 27D representations remain different

For the **regular** 27-address action, a nontrivial central element permutes all 27 basis addresses in nine disjoint 3-cycles. Its trace is 0, with central eigenvalue multiplicities

\[
(\mathrm{mult}_1,\mathrm{mult}_\omega,\mathrm{mult}_{\omega^2})=(9,9,9).
\]

For the repository's **trinification E6 operator H27**, the central element is \(\omega I_{27}\), yielding multiplicities \((0,27,0)\). Thus no 27×27 intertwiner exists between the *original representations*. The pre-existing Pass 11043 **resolves the representation-ring mismatch by a nontrivial 9D commutant dressing**; this is not achieved simply by the abstract group isomorphism \(\Phi\) above.

## III. Requested gravitational next step: actual overlapping cycles do not have a common center

Start with the certified induced C8 W33 Levi cycle \([0,40,1,44,4,53,13,41]\). The new program searches the actual 80-vertex, 160-edge Levi graph and finds another induced C8 \([0,42,16,54,25,76,21,43]\) meeting the first in exactly the vertex 0.

Inside each local eight-cycle, the earlier rational Jacobi-algebra center is represented by the embedded rank-one matrix \(C=u s^T\), with \(u\) constant \(+1\) on its eight vertices and \(s\) alternating by bipartition. Embedding both as 80×80 matrices produces two local centers \(C_1,C_2\) satisfying

\[
\boxed{\operatorname{rank}[C_1,C_2]=2},\qquad
\#\{(i,j):[C_1,C_2]_{ij}\neq0\}=126.
\]

Hence the **local** Heisenberg centers are **not global central charges** under overlapping-chart commutators. A global gravity construction must derive a gluing connection/cocycle rather than identify all C8 centers unchanged. This is a strict finite-matrix obstruction in the supplied graph-current ansatz. The full 80-vertex Lie closure, Dirac bracket, continuum, diffeomorphisms and Einstein dynamics remain open.

## IV. Requested photonic next step: discrimination *per launched photon*

The preceding committed compiler built exact nine-disjoint-edge-stage sequences on each 27-port graph, and calculated increasing unitary fidelity at depths 9 to 576. The present producer consumes the **actual committed Trotter-depth output**, not guessed probabilities, to calculate the explicitly marked **screening proxy**

\[
\mathcal P(r)=\eta^{9r}\,[\Delta(r)]^2,
\qquad\eta=0.99
\]

for independently supplied **1% survival loss per layer**. Across the previously tested \(r=1,2,4,8,16,32,64\), this proxy is largest at **36 physical two-port interaction stages** (four nine-layer repetitions), rather than the deepest available circuit. This is a meaningful *cost-versus-accuracy hypothesis* for engineering; it is **not** a true Fisher-information calculation or a valid experimental shot count because \(\Delta\) compares two global maxima that require calibrated port scans, and detector errors/crosstalk are omitted. The selected experiment must define actual input/output ports and a likelihood function before using Chernoff/Hoeffding to quote a real photon budget.

## V. Requested chirality double cover: corrected 320-set pairing

The **previously proved** 320 nontrivial line-character quartic vacua are 160 \((p\in L)\) flags × two conjugate characters. The **projective flag-graph triangles** are 160 line-centered plus 160 point-centered triples. The full \(Sp(4,3)\) center \(-I\) swaps every chiral character pair but fixes every projective triangle, forbidding an equivariant map between those two 320-element G-sets.

This pass isolates the correct candidate source of a lift: the **double cover of the 160 line-centered triangles** by the nontrivial line-character sign associated with the omitted flag. Its total has 320 elements, and \(-I\) swaps sign in every fiber. One can make it equivariant **tautologically by transporting the existing character action**. This merely states the necessary fiber geometry: an *independent* orientation double-cover, projective cocycle and Lorentzian physical chirality are still required to claim a new realization.

## VI. Requested proton-hexality source: center-only H27 fails within a single E6 27

The previous source-derived \(X_3\) remnant needed to complete the supplied \(P_6\) table has \(X_3(Q)=2\) and \(X_3(U^c)=0\) modulo 3. The original trinification **operator H27 center acts as the same scalar \(\omega\) on the entire E6 27**, in particular cannot assign different central charges to two fields both contained in one unchanged E6 27.

This is a **conditional no-go**: if Q and Uc come from the same such 27 representation and the only proposed new \(Z_3\) is that scalar H27 center, it **cannot** equal \(X_3\). Extra gauge factors, different representations, symmetry breaking, geometric equivariance and a true anomaly-checked string-vacuum construction remain legitimate alternate routes. This complements the earlier exclusion of simple \(Y+(B-L)\) and pure Klein-four Wilson-line origins; it does **not** establish that proton hexality itself is impossible.

## VII. Requested physical flavor next step: one explicit free-action polynomial candidate

Pass 11742 **already proved existence of a generic smooth invariant tetraquadric quotient**, but had not fixed a concrete hypersurface polynomial, so numerical Ricci-flat/HYM/harmonic normalization was not executable from that proof alone.

On \((\mathbf P^1)^4\), the Klein-four group is generated by simultaneously \(g:(u_i,v_i)\mapsto(u_i,-v_i)\) and \(h:(u_i,v_i)\mapsto(v_i,u_i)\). In degree \((2,2,2,2)\), the invariant basis consists of **21 orbits of degree-vector monomials**, whose index vectors have an even number of \(uv\) factors and are identified under simultaneous \(d_i\mapsto2-d_i\). The producer picks an explicit **integer coefficient vector** in this basis using a reproducible seed and checks that the resulting polynomial is invariant and nonzero at **all 48 fixed ambient points** of \(g,h,gh\) (16 each). Thus the hypersurface, *if smooth*, avoids nontrivial quotient fixed points.

**Not yet done:** full complex smoothness certification of this specific polynomial, Ricci-flat Kähler metric, HYM connection, harmonic 1-form representatives, zero-mode orthonormalization, physical Yukawa masses, moduli stabilization. This is an **explicit candidate**, not a physical vacuum. The provided certificate and program spell out coefficients, monomial orbit basis and fixed-point evaluation method so the next pass can do an exact smoothness proof rather than start again from existence.

## Physical conclusion and strongest new directions

The new comparison supplies a concrete **group-theoretic embedding from W33's order-27 elation torsor into a chosen symplectic subquotient of the mod-3 Heisenberg-13 radical**, while rigorously preserving the established distinction between address and operator H27. The overlapping C8 calculation shows the opposite obstruction to a naive global gravity gluing: the locally central operators fail to commute when their cycles meet.

These two statements together identify a very specific next issue: construct and classify a **global, equivariant atlas of 13D Heisenberg radicals** over W33 where the order-27 elation subgroup embeddings and local central cocycles transform consistently. Without a natural \(PSp(4,3)\) lift, continuum gravitational action, matter representation and experimental prediction, no Theory-of-Everything theorem is claimed.

### Conservative full-port statistical scan (additional executed certificate)

To avoid treating the maximum over many source/detector ports as a prespecified single Bernoulli experiment, the program also derives an **explicit simultaneous confidence bound**. There are \(2\times27\times26=1404\) offdiagonal probabilities across the two compiled 27-mode devices. At one chosen depth, let \(\Delta>0\) be the ideal-model conditional gap between the two offdiagonal maxima. For **each of the 54 input-port/device configurations**, collect \(n\) independent successful photon detections and estimate all output frequencies. Choosing \(\epsilon=\Delta/4\), Hoeffding plus a union bound over the 1404 individual outcomes gives the sufficient conditional design

\[
n\ge \left\lceil\frac{8\log(2\cdot1404/0.05)}{\Delta^2}\right\rceil.
\]

With at least \(n\) successful observations for every source setting, probability \(\ge0.95\) guarantees all offdiagonal estimates are within \(\epsilon\) of their conditional model values; the estimated difference between the two maxima remains at least \(\Delta/2\). The total detected-sample target is \(54n\). The certificate calculates this at every previously tested Trotter depth and reports \(\lceil54n/0.99^{\mathrm{stages}}\rceil\) as the **expected launches** under an independent uniform loss model. This last expected-launch figure is *not itself a 95%-guaranteed launch budget*: binomial fluctuations in survival would require an additional confidence allowance. This theorem is a valid ideal-model statistical sufficient condition with a fixed, specified gap, **not** a claim of a built photon interferometer, calibrated systematic errors or experimentally achieved discrimination.
