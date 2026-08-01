# Passes 1882–1886 — decoder correction, complete primal enumerator, two-adic clock order, exceptional-$S_6$ carrier maps, and the geometric $C_4$ fold

## Executive result

All five requested fronts were executed. Four close as exact finite theorems. The decoder front instead exposes and corrects a real globalization error in Passes 1847/1857: a fixed-coordinate syndrome chart cannot determine global syndrome multiplicity. Consequently the published number

\[
2{,}993{,}248{,}416
\]

is a certified **upper bound**, not an exact fifth-order unique-minimum coefficient. The exact sixth-order equal-syndrome edge count remains valid, but the sixth-order singleton coefficient remains open.

The aggregate certificate verifies **42/42** checks. Its SHA-256 is

```text
4a9611b3cd9463307efd12678be2792fd63da77b750e1dd4755bf9bad6fc8f1c
```

---

## Pass 1882 — fixed-coordinate charts do not globalize syndrome multiplicity

Let $e,f$ be weight-five errors with equal syndrome. Their symmetric difference is a codeword of even weight $w$, and

\[
|\operatorname{supp}(e)\cap\operatorname{supp}(f)|=5-\frac w2.
\]

Therefore this collision pair appears in exactly $5-w/2$ of the 240 fixed-coordinate charts. In particular, every pair arising from a weight-ten codeword is disjoint and appears in **zero** charts.

The exact Pass-1847 collision terms are

\[
\begin{array}{c|rrrr}
w&4&6&8&10\\ \hline
E_5(w)&3{,}503{,}962{,}800&2{,}617{,}056{,}000&3{,}444{,}260{,}400&2{,}207{,}943{,}360.
\end{array}
\]

Thus $2{,}207{,}943{,}360$ disjoint equal-syndrome pairs are invisible in every coordinate chart. The chart singleton identity

\[
240\cdot62{,}359{,}342
=5\cdot2{,}993{,}248{,}416
\]

counts singleton incidences **inside the charts**; it does not prove that those errors remain singleton after disjoint partners are included globally.

What remains exact at weight five is

\[
\binom{240}{5}=6{,}363{,}048{,}048,
\]

with

\[
84{,}201{,}264
\]

errors lying in lower odd shadows and

\[
6{,}278{,}846{,}784
\]

errors having minimum weight five. The corrected conclusion is

\[
\boxed{U_5\le2{,}993{,}248{,}416},
\]

where $U_5$ is the global unique-minimum count.

At weight six the exact equal-syndrome collision edge count remains

\[
\boxed{E_6=1{,}724{,}138{,}884{,}380}.
\]

But an edge count does not determine singleton components. For example, three doubleton classes and the distribution “three singletons plus one tripleton” both contain six errors and three collision edges, while their singleton counts are zero and three. Therefore neither the univariate enumerator nor $E_6$ determines the sixth-order decoder coefficient.

**Boundary.** Exact $U_5$ and $U_6$ require a global syndrome-component enumeration with lower-shadow removal. No fixed-coordinate or moment-only shortcut is valid.

---

## Pass 1883 — complete primal enumerator and exact shell strength

The complete dual histogram from Pass 1876 was transformed through the binary MacWilliams identity. This gives the full weight enumerator of the primal

\[
[240,195,4]
\]

code. It sums to $2^{195}$, every odd coefficient vanishes, and complement symmetry holds:

\[
A_w=A_{240-w}.
\]

The first nonzero coefficients are

\[
\begin{aligned}
A_4&=540,\\
A_6&=9{,}600,\\
A_8&=424{,}170,\\
A_{10}&=17{,}523{,}360,\\
A_{12}&=891{,}792{,}940,\\
A_{14}&=54{,}326{,}090{,}880,\\
A_{16}&=3{,}770{,}230{,}198{,}995.
\end{aligned}
\]

The complete coefficient table is frozen in
`data/w33_pass1883_full_primal_weight_enumerator.json`.

Edge transitivity makes every nonempty support shell a $1$-design. For the first three newly closed shells,

\[
\lambda_1(12)=44{,}589{,}647,
\qquad
\lambda_1(14)=3{,}169{,}021{,}968,
\qquad
\lambda_1(16)=251{,}348{,}679{,}933.
\]

The required pair multiplicities are

\[
\lambda_2(12)=\frac{490{,}486{,}117}{239},
\]

\[
\lambda_2(14)=\frac{41{,}197{,}285{,}584}{239},
\]

and

\[
\lambda_2(16)=\frac{3{,}770{,}230{,}198{,}995}{239}.
\]

All are nonintegral. Hence

\[
\boxed{\text{the weight-12, 14, and 16 shells are exactly 1-designs, not 2-designs}.}
\]

---

## Pass 1884 — the integral clock order is defective only at two

Let $C$ denote the balanced clock operator and set

\[
f(x)=(x-2)(x+2)(x^2+4)(x^4+16).
\]

Then

\[
\mathbb Q[C]
\cong
\mathbb Q\times\mathbb Q\times\mathbb Q(i)\times\mathbb Q(\zeta_8).
\]

The power order has discriminant

\[
\operatorname{disc}\mathbb Z[C]=-2^{80},
\]

while its normalization is

\[
\mathcal O_{\max}
=
\mathbb Z\times\mathbb Z\times\mathbb Z[i]\times\mathbb Z[\zeta_8]
\]

with discriminant $-2^{10}$. Therefore

\[
\boxed{[\mathcal O_{\max}:\mathbb Z[C]]=2^{35}}.
\]

The exact quotient Smith invariants are

\[
1,2,4,8,32,64,256,1024,
\]

so

\[
\mathcal O_{\max}/\mathbb Z[C]
\cong
\mathbb Z/2\oplus\mathbb Z/4\oplus\mathbb Z/8\oplus
\mathbb Z/32\oplus\mathbb Z/64\oplus\mathbb Z/256\oplus\mathbb Z/1024.
\]

The conductor is

\[
\boxed{
\mathfrak f=
1024\mathbb Z\times1024\mathbb Z\times512\mathbb Z[i]
\times256\mathbb Z[\zeta_8].
}
\]

The four primitive CRT idempotents require denominators

\[
2^{10},\quad2^{10},\quad2^8,\quad2^5.
\]

Thus every obstruction to the integral cyclotomic splitting is two-adic; away from $2$, the power order is already maximal.

---

## Pass 1885 — exceptional-$S_6$ branching and literal carrier maps

The setwise stabilizer of the canonical six 5-point fibers has order $720$ and induces the full $S_6$ action on the fibers. Restricting the five signed-edge sectors gives

\[
\begin{aligned}
15&\downarrow S_6=[3,1,1,1]+[2,1,1,1,1],\\
24&\downarrow S_6=[4,2]+[4,1,1]+[2,2,2],\\
30&\downarrow S_6=[3,1,1,1]+[2,2,2]+[2,2,1,1]+[2,1,1,1,1]+[1^6],\\
81&\downarrow S_6=[4,1,1]+2[3,2,1]+2[3,1,1,1]+[2,2,2]+[2,2,1,1]+[2,1,1,1,1],\\
90&\downarrow S_6=[4,2]+2[4,1,1]+2[3,2,1]+2[3,1,1,1]+[2,2,1,1].
\end{aligned}
\]

The natural separator constituent is the nine-dimensional Specht module

\[
V_9=[4,2].
\]

Its multiplicities are

\[
\boxed{(m_{15},m_{24},m_{30},m_{81},m_{90})=(0,1,0,0,1).}
\]

The sign-twisted nine-dimensional module $[2,2,1,1]$ occurs with multiplicities

\[
(0,0,1,1,1).
\]

Two explicit intertwiners were constructed by Reynolds averaging and exact spectral projection:

\[
A_{24}=N_{24}/2,
\qquad
A_{90}=N_{90}/2,
\]

where $N_{24},N_{90}\in\{-1,0,1\}^{240\times15}$ each have rank nine and entry counts

\[
720(-1)+2160(0)+720(+1).
\]

They satisfy all $720$ intertwining equations and

\[
N_{24}^{\mathsf T}N_{24}
=N_{90}^{\mathsf T}N_{90}
=4E_{9,\mathrm{num}},
\]

\[
\boxed{N_{24}^{\mathsf T}N_{90}=0.}
\]

The two image copies of $V_9$ are therefore isometric and orthogonal. The denominator $2$ is genuine: the primitive integer numerators are ternary, while the equivariant maps themselves are half-integral.

This is an occurrence and transport theorem, not a phase theorem. In particular the odd $81$-sector remains parity-obstructed and contains only the sign-twisted nine-dimensional constituent.

---

## Pass 1886 — the directed clock is a five-vertex $C_4$ voltage orbifold

The complete directed automorphism group of the transfer graph is

\[
\boxed{\operatorname{Aut}_{\rightarrow}(T)=\operatorname{Fix}(\alpha)\cong C_4,}
\]

where $\alpha$ is the exceptional outer automorphism of $S_6$. A generator is

\[
(0\ 1\ 4\ 5)(2\ 3).
\]

Its five duad orbits are

\[
\begin{array}{c|l}
A&(01),(14),(45),(05)\\
B&(02),(13),(24),(35)\\
C&(03),(12),(34),(25)\\
D&(04),(15)\\
E&(23),
\end{array}
\]

with sizes

\[
\boxed{4+4+4+2+1}.
\]

The stabilizers are respectively

\[
1,1,1,C_2,C_4.
\]

The unique loop lies at the fixed duad

\[
\boxed{\{2,3\}}.
\]

A five-vertex graph-of-groups voltage table reconstructs all 45 directed arcs. The graph remains strongly connected, cubic, and of directed diameter three. Hence the residual $C_4$ is not an accidental graph symmetry: it is exactly the fixed subgroup of the exceptional outer automorphism and is the surviving symmetry of the one-part fold

\[
T=P^{\mathsf T}D
\]

of the Tutte–Coxeter Levi graph.

**Boundary.** Voltage offsets are finite graph phases. They do not define physical time, optical phase, or a Hamiltonian evolution.

---

## Verification ledger

- Pass 1882: 9/9 checks, with an explicit proof boundary.
- Pass 1883: 9/9 checks.
- Pass 1884: 6/6 checks.
- Pass 1885: 10/10 checks, including 720 literal equivariance identities.
- Pass 1886: 8/8 checks.
- Aggregate: 42/42 checks.
