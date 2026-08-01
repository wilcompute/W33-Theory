# Passes 1872–1876 — cyclotomic boundary, Tutte–Coxeter lift, separator projector, directed uniqueness, and exact \(A_{12}\)

## Executive result

All five requested continuation fronts were executed. Four close as exact finite theorems. The decoder front closes the previously missing coefficient

\[
\boxed{A_{12}=891{,}792{,}940}
\]

and therefore the complete weight-six equal-syndrome pair count, while preserving the distinct open problem of deduplicating those pairs into the sixth-order unique-minimum decoding coefficient.

The aggregate light verifier proves **19/19** checks. The exact dual enumerator has its own **8/8** fail-closed certificate. The exhaustive calculation enumerates all \(2^{45}\) words of the dual code through a deterministic \(30+15\) separator contraction.

---

## Pass 1872 — the clock is cyclotomic only after inverting two

Let

\[
\Lambda=\operatorname{im}_{\mathbb Z}(T)\cap\mathbf1^\perp.
\]

It is a rank-nine integral lattice with Euclidean discriminant

\[
\boxed{\det(\Lambda^{\mathsf T}\Lambda)=2560=2^9\cdot5.}
\]

If \(C\) denotes the integral matrix of \(T\) on \(\Lambda\), then

\[
\chi_C(x)=(x-2)(x+2)^2(x^2+4)(x^4+16).
\]

Thus over \(\mathbb Q\), and equivalently after inverting \(2\), the balanced clock decomposes as

\[
\mathbb Q[x]/(x-2)
\oplus2\,\mathbb Q[x]/(x+2)
\oplus\mathbb Q[x]/(x^2+4)
\oplus\mathbb Q[x]/(x^4+16).
\]

The normalized operator \(C/2\) is not integral; its reduction obstruction has binary rank four. More sharply,

\[
\operatorname{SNF}(C+2I)_{\ne0}=(1,1,1,1,4,4,4),
\]

so

\[
\boxed{\Lambda/(C+2I)\Lambda\cong\mathbb Z^2\oplus(\mathbb Z/4)^3.}
\]

Therefore the eight-dimensional regular \(C_8\) packet plus an additional sign direction exists rationally, but there is no honest global integral \(\mathbb Z[\zeta_8]\)-lattice decomposition. The doubled \(-2\) eigenspace also prevents a canonical choice of the “extra” sign line.

---

## Pass 1873 — the 30-vertex lift is the Tutte–Coxeter graph

Form the bipartite Levi adjacency

\[
A_{\mathrm{TC}}=
\begin{pmatrix}
0&D^{\mathsf T}\\
D&0
\end{pmatrix}.
\]

The exact graph census is

\[
|V|=30,\qquad |E|=45,\qquad k=3,\qquad g=8,\qquad\operatorname{diam}=4,
\]

with distance distribution

\[
1,3,6,12,8
\]

and intersection array

\[
\boxed{\{3,2,2,2;1,1,1,3\}.}
\]

This is the Tutte–Coxeter graph, the incidence graph of the doily \(W(2)\). Conjugating the syntheme half by the exceptional identification changes the off-diagonal blocks exactly to

\[
\begin{pmatrix}
0&T^{\mathsf T}\\
T&0
\end{pmatrix}.
\]

Its adjacency polynomial is

\[
\boxed{x^{10}(x-3)(x+3)(x-2)^9(x+2)^9.}
\]

For the 90-state Hashimoto operator \(B\),

\[
\boxed{
\chi_B(x)=
(x-2)(x+2)(x-1)^{16}(x+1)^{16}
(x^2+2)^{10}(x^2-2x+2)^9(x^2+2x+2)^9.
}
\]

The first primitive unoriented reduced-cycle counts are

\[
N_8=90,\quad N_{10}=72,\quad N_{12}=300,
\quad N_{14}=1080,\quad N_{16}=4500.
\]

---

## Pass 1874 — exact separator projector and full-group obstruction

Set \(G=T^{\mathsf T}T\). The exact rank-nine rational projector is

\[
\boxed{E_9=\frac{G(9I-G)}{20}.}
\]

Its integral numerator \(Q=G(9I-G)\) satisfies

\[
Q^2=20Q,\qquad \operatorname{rank}Q=9,
\]

and has nonzero Smith invariants

\[
\boxed{1,5,5,5,10,20,20,20,20.}
\]

The six-dimensional kernel is exactly the trivial line plus the five-dimensional vertex-potential gauge. Hence the separator representation decomposes as

\[
\boxed{\mathbb Q^{15}=\mathbf1\oplus V_5\oplus V_9,}
\]

with \(V_9\) occurring once, and

\[
GQ=4Q.
\]

This is the positive occurrence sought by the carrier search. The exact \(W(E_6)\) character-degree list contains no degree nine, so a nine-dimensional irreducible cannot embed equivariantly into a full \(W(E_6)\)-carrier. The clock exists after restriction to the exceptional \(S_6\) separator, not as a full-group irreducible sector.

---

## Pass 1875 — normality correction, automorphism group, and uniqueness

A correction to Passes 1867–1871 is required:

\[
\boxed{TT^{\mathsf T}=T^{\mathsf T}T.}
\]

Thus \(T\) is **normal but nonsymmetric**, not nonnormal. Consequently \(T/2\) is exactly orthogonal on the balanced rank-nine image. This remains compatible with Pass 1866: the construction is outer-twisted and does not provide a \(W(E_6)\)-invariant complex structure on a full-group irreducible.

The directed \(15\)-vertex graph of \(T\) is strongly connected, has directed diameter three, and has full directed automorphism group

\[
\boxed{\operatorname{Aut}_{\rightarrow}(T)\cong C_4.}
\]

Its vertex orbits have sizes

\[
4,4,4,2,1,
\]

and its ordered-pair orbital rank is \(59\). The orbital matrices close under multiplication, giving the exact coherent configuration of the directed graph.

The exceptional twisted Hom-space has dimension two. With basis \(T,J-T\), every twisted-equivariant row-sum-three candidate is

\[
X(c)=(1-5c)T+cJ.
\]

The Gram equation

\[
X(c)^{\mathsf T}X(c)=T^{\mathsf T}T
\]

has precisely

\[
c=0,\qquad c=\frac25.
\]

The second solution \(2J/5-T\) is nonintegral. Therefore

\[
\boxed{T\text{ is the unique integral, and unique }0/1,
\text{ twisted-equivariant row-sum-three solution with its Gram matrix}.}
\]

---

## Pass 1876 — complete dual enumerator and exact \(A_{12}\)

The canonical \(45\)-generator dual code splits into the rank-30 fiber subcode and rank-15 residual-duad subcode. The stabilizer of the canonical six-line pack has order \(720\) and induces the full order-\(720\) action on the residual sector. The \(2^{15}\) residual assignments collapse into exactly \(156\) orbits.

A chunkable Gray-code C++ worker expands each residual orbit over all \(2^{30}\) fiber assignments. The merged histogram contains exactly

\[
\boxed{2^{45}=35{,}184{,}372{,}088{,}832}
\]

dual words and is symmetric under \(w\leftrightarrow240-w\). Exact MacWilliams transform reproduces

\[
A_4=540,\quad A_6=9600,\quad A_8=424170,
\quad A_{10}=17{,}523{,}360
\]

and closes the missing coefficient:

\[
\boxed{A_{12}=891{,}792{,}940.}
\]

Coordinate transitivity gives the exact fixed-coordinate count

\[
\boxed{A_{12}^{(0)}=44{,}589{,}647.}
\]

Therefore the weight-six equal-syndrome pair count is

\[
\boxed{
E_6=1{,}312{,}130{,}546{,}100+462A_{12}
=1{,}724{,}138{,}884{,}380.
}
\]

The prior Pass-1860 value \(A_{12}\ge5{,}323{,}560\) is superseded by this exact count.

### Decoder boundary

The total collision count is not the sixth-order unique-minimum success coefficient. A syndrome can participate in multiple collision edges, and lower-weight shadows must be removed before unique and ambiguous minima are counted. No BSC coefficient is promoted until that orbitwise deduplication is complete.
