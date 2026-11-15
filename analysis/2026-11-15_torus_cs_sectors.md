# Consistent toroidal gauge sectors and the quiver Chern–Simons obstruction

The [toroidal charge dictionary](2026-11-15_quiver_torus_charge_dictionary.md) identifies the quiver's tritangents with the monomials of the split $E_6$ cubic. In five-dimensional maximal supergravity the invariant tensor on these coordinates appears in the vector Chern–Simons coupling. This makes it possible to test which coordinate sectors close under the gauge equations and which have consistent eleven-dimensional origins. The setting here is classical two-derivative supergravity on the unquotiented torus, keeping only zero modes. [De Wit, Samtleben and Trigiante, maximal five-dimensional supergravity](https://arxiv.org/abs/hep-th/0412173) · [Iqbal, Neitzke and Vafa, toroidal charges and cubic-surface geometry](https://arxiv.org/abs/hep-th/0111068)

## Diagonal torus reflections realize the binary geometry on fields

Reflect any subset of the six torus coordinates. Write their signs as $s_i$ and the orientation sign as $\delta=\prod_i s_i$. For odd orientation reversal, the eleven-dimensional three-form changes sign in addition to its pullback. Equivalently $C_3$ transforms by $\delta R^*C_3$ for a diagonal reflection $R$. The dual field strength transforms by ordinary pullback, since the orientation and the three-form each supply a factor $\delta$. The five-dimensional vector signs are

| Sector | Sign |
|---|---|
| Metric vectors $P_i$ | $s_i$ |
| Three-form vectors $M_{ij}$ | $\delta s_i s_j$ |
| Dual vectors $K_i$ | $\delta s_i$ |

The scalar signs are $s_i s_j$ on the internal metric, $\delta s_i s_j s_k$ on the internal three-form, and $\delta$ on the scalar dual to the external three-form. The Pfaffian and each mixed monomial are invariant under every reflection. The torus zero-mode equations are equivariant, so retaining the fields fixed by a subgroup is a consistent bosonic truncation. This argument retains the corresponding metric and scalar fields and introduces no boundary or quotient sectors. [Freed and Hopkins, M-theory parity](https://arxiv.org/abs/1908.09916)

Use $\mathbb F_2^6$ to label the sign characters. Momentum, M2, and M5 vectors have characters of Hamming weights one, four, and five respectively. These are precisely the nonzero singular vectors of $q(x)=\sum_{i<j}x_ix_j$, the binary elliptic quadric $Q^-(5,2)$. The tritangents are exactly the triples of distinct vector characters that sum to zero. The scalar characters have weights two, three, and six, together with six trivial characters from the metric diagonal. Thus **each nonzero character of the six torus reflections occurs exactly once** on the combined vectors and scalars. This realizes the finite charge geometry directly on reduction fields. The abstract 27-point geometry and its 63 geometric hyperplanes are known. [Saniga, Lévay, Pracna and Vrana, Veldkamp space of $GQ(2,4)$](https://arxiv.org/abs/0903.0715)

An $r$-dimensional subgroup retains $2^{6-r}-1$ components carrying nonzero characters of the full group, and six neutral scalars. Since all nonzero characters occur, different subgroups give different combined vector–scalar sectors. The 2,825 subgroups give 1,949 distinct vector supports. In particular the 120 sectors with nine vectors have 12 scalars, the 27 sectors with 11 vectors have 26 scalars, and the 36 sectors with 15 vectors have 22 scalars.

## The spinor lift selects the STU sectors

With periodic spin structure on the flat torus, a coordinate reflection lifts on constant eleven-dimensional spinors by the product of the spatial gamma matrices for its reflected directions, up to a central sign. A reflection of weight $k$ has lift square $(-1)^{k(k-1)/2}=(-1)^{q(r)}$ for reflection vector $r$. The commutator of two lifts is the polarization of this same sign. Thus a subgroup admits common invariant supercharges only when $q$ vanishes on it. On a totally singular subgroup the generators have commuting order-two lifts. Choosing their signs gives simultaneous eigenspaces of equal dimension, since every nonidentity gamma monomial has zero trace. An $r$-dimensional totally singular subgroup preserves $32/2^r$ real constant supercharges.

The minus-type quadratic space has Witt index two. The verifier finds 27 rank-one projections preserving 16 supercharges, each with 11 vectors and 26 scalars. It finds 45 rank-two projections preserving eight supercharges, each with three vectors, 18 scalars, and a single tritangent cubic. For example, reflecting $1234$ and $1256$ keeps the three M2 directions $12,34,56$. Their Pfaffian restriction is the STU product. In five-dimensional $\mathcal N=2$ counting this is the gravity multiplet, two vector multiplets, and four hypermultiplets. Higher-rank or nonsingular reflection groups contain an element whose lift squares to minus one. In particular the two triple reflections isolating the nine-vector determinant sector give a consistent bosonic sector with no constant invariant supercharges.

## The maximal coordinate supports for vanishing discarded Chern–Simons sources

At a diagonal torus background a discarded vector has a Chern–Simons source $d_{Iab}F^a\wedge F^b$ if $a,b$ are retained and the corresponding tritangent contains the discarded coordinate $I$. For a coordinate truncation allowing arbitrary retained field strengths at that background, source cancellation requires that the third coordinate be kept whenever two coordinates of a tritangent are kept. The verifier takes the closure under this rule. It generates every closed subset by starting at the empty set and repeatedly adding one coordinate and closing. Any closed set can be reached by adding its own coordinates, since closure never exits a closed superset.

Of the 3,668 closed subsets, the following are the maximal proper ones. Every other proper closed set is contained in at least one of them.

| Vectors | Maximal supports | Representative | Restricted cubic |
|---|---:|---|---|
| 6 | 72 | Six skew exceptional lines, giving the six momenta | Zero |
| 11 | 27 | One reflected circle, giving five momenta, five crossing M2 charges, and one M5 charge | One distinguished charge times a split quadratic |
| 15 | 36 | Total torus inversion, giving all 15 M2 charges | Pfaffian |

The verifier matches each class to one Weyl orbit. The 11- and 15-vector supports are the 63 single-reflection fixed sets. The six-momentum representative lifts by setting the three-form to zero in eleven dimensions, which leaves vacuum gravity and its full torus metric sector. The ungauged $E_{6(6)}$ symmetry transports this representative to its Weyl images in the classical five-dimensional theory. The single-circle reflection has the field content of five-dimensional half-maximal supergravity with five vector multiplets. The exhaustive claim concerns coordinate Chern–Simons closure. It does not classify non-coordinate truncations or guarantee that every smaller closed support has a compatible scalar sector. [Schön and Weidner, five-dimensional half-maximal supergravity](https://arxiv.org/abs/hep-th/0602024)

## The determinant sector and why two quiver blocks source the third

For a split $T^6=T^3_U\times T^3_V$, impose both reflections that reverse precisely one triple, each with the accompanying three-form parity. The common even sector consists of the external metric, two symmetric internal $3\times3$ metric blocks $G_U,G_V$, and the nine vectors $A_{i\alpha}$ from $C_{\mu i\alpha}$. It retains no internal three-form or dual scalar. All other bosonic fields have an odd character under at least one reflection. The verifier identifies the 120 such rank-nine vector supports with precisely the 120 distinct determinant blocks of the 40 quiver charts.

The reduction gives a positive gauge kinetic matrix directly. With internal volume $\nu=\sqrt{\det G_U\det G_V}$, use $ds^2_{11}=\nu^{-2/3}ds^2_5+ds^2_{6}$ in five-dimensional Einstein frame. The eleven-dimensional measure contributes $\nu^{-2/3}$ and raising the two external field-strength indices contributes $\nu^{4/3}$. The kinetic coefficient is proportional to $\nu^{2/3}(G_U^{-1})^{ij}(G_V^{-1})^{\alpha\beta}$. The internal forms in $C_3\wedge G_4\wedge G_4$ are three crossing two-forms. Their wedge gives the tensor $\epsilon_{ijk}\epsilon_{\alpha\beta\gamma}$ up to the common orientation sign. Its cubic is the determinant of the crossing M2 matrix, which is the term of degree three in the [charge cut expansion](2026-11-15_quiver_torus_charge_dictionary.md).

The other part of the full cubic has a direct reduction origin as well. Write the Kaluza–Klein one-forms as $\eta^i=dy^i+P^i$ and $G^i=dP^i$. At zero internal three-form scalars the coefficient of $\eta^i$ in $dC_3$ is $H_i=dB_i+\sum_j A_{ij}\wedge G^j$, with $A_{ij}=-A_{ji}$ and $F_{ij}=dA_{ij}$. Its Bianchi identity is $dH_i=\sum_j F_{ij}\wedge G^j$. Dualization by a one-form $K^i$ paired with this identity produces the Chern–Simons term $-\sum_{ij}K^i\wedge F_{ij}\wedge G^j$. Grouping the two orientations of each M2 pair gives the alternating $M2$–momentum–$M5$ tensor in the toroidal cubic, with the choice of orientation for the dual vectors. Evaluating at these scalar values identifies the tensor and does not freeze the scalar equations of the full theory.

The quiver support corresponds instead to the degree-one response in the crossing M2 coordinates, or the mixed trace in the three determinant blocks. If two blocks are retained and the third is discarded, every field in the discarded block has three independent mixed Chern–Simons sources from the retained blocks. This holds for all 40 charts and all three choices of discarded block. One can excite a single such source by choosing the two contributing field strengths with nonzero wedge product. The mixed trace therefore gives a coupling among sectors of the full theory.

There is also a separate positivity obstruction for treating the trace-only polynomial as a five-dimensional $\mathcal N=2$ vector prepotential. It is linear in each nine-coordinate block when the other two are fixed. At any point with positive polynomial value there is an at least eight-dimensional space of nonzero variations in one block that annihilate its first derivative. The second derivative also vanishes on these variations. They are tangent to the constant-volume surface and have zero norm in the very-special metric proportional to $-\mathrm{Hess}\log N$. That metric cannot be positive definite, and the argument permits arbitrary coefficients on the mixed support. The actual bosonic determinant sector has the positive metric-block kinetic term above. [Very-special real geometry and gauge kinetic metrics](https://doi.org/10.1103/PhysRevD.104.106016)

Replay with NetworkX and SymPy.

    python -B analysis/toe_20261115_torus_cs_sectors.py

The [certificate](../data/toe_20261115_torus_cs_sectors.json) gives the closure census, the field counts, the maximal Weyl representatives, and the source multiplicities. A microscopic relation between the toroidal truncations and the four-dimensional del Pezzo probe remains open.
