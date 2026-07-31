# Passes 1390–1394 — Modular, geometric, Fourier, apartment, and integral selector frontiers

## Scope and corrections

This packet continues the exact selector Mackey decomposition of Passes 1380–1384. Two proposed positive statements failed during execution and were retained as corrections:

1. the characteristic-zero Mackey orbit sizes do **not** by themselves derive the bad-characteristic Loewy extensions; what is exact is the projector-localization profile together with the independently exhaustive radical towers;
2. the orbital integral order is **not** contained in the particular split maximal order selected by the frozen rational matrix units. The correct theorem is exact lattice commensurability and discriminant arithmetic.

All calculations use the literal 120-selector permutation action, the frozen 83-orbital algebra, exact rational arithmetic, and the existing hinge-selected 2160-apartment construction.

## Pass 1390 — Modular Mackey localization and Loewy boundary

The fourteen rational primitive central projectors have denominator LCMs

\[
36,18,54,18,54,18,54,54,54,27,54,54,54,108.
\]

Thus their prime support is exactly \(\{2,3\}\). Their direct localization profile in the orbital lattice is

\[
\begin{array}{c|cc}
p&\text{localizable}&\text{collapsed}\\\hline
2&1&13\\
3&0&14\\
5&14&0
\end{array}
\]

The independently exhaustive modular regular-module computations give

\[
\dim J_2^\bullet=(45,16,0),
\qquad
\dim J_3^\bullet=(72,49,27,14,4,0),
\]

while \(J_5=0\). In characteristic five the regular composition-factor census is

\[
1^7,\quad2^4,\quad3^9,\quad4^4,\quad5^5,
\]

so the full split algebra survives:

\[
\mathbb F_5^7\oplus M_2(\mathbb F_5)^2\oplus M_3(\mathbb F_5)^3
\oplus M_4(\mathbb F_5)\oplus M_5(\mathbb F_5).
\]

**Boundary.** The lengths three and six are extension data; they are not inferred from the six characteristic-zero dual-orbit sizes alone.

## Pass 1391 — Intrinsic geometry of the six dual orbits

The complement \(K\cong D_8\times C_2\) has a unique invariant line and a unique invariant complementary plane in the dual \(\mathbb F_3^3\). In the frozen coordinates these are

\[
L=\langle(1,0,1)\rangle,
\qquad
P=\langle(0,1,0),(1,0,2)\rangle.
\]

On \(P\), the unique invariant nondegenerate quadratic form up to scale is

\[
Q_P=\begin{pmatrix}2&0\\0&2\end{pmatrix}.
\]

The six Mackey orbit families are therefore exactly

\[
\begin{array}{c|c|c}
\text{size}&\text{intrinsic class}&\text{little group}\\\hline
1&0&D_8\times C_2\\
2&\text{pure hinge charge}&D_8\\
4&\text{neutral square diagonals}&V_4\\
4&\text{neutral square axes}&V_4\\
8&\text{charged square diagonals}&C_2\\
8&\text{charged square axes}&C_2
\end{array}
\]

This gives a geometric explanation of \(1+2+4+4+8+8=27\) from the exact \(1+2\) complement module.

## Pass 1392 — Exact selector Mackey Fourier transform

For each of the fourteen character projectors, deterministic pivot columns were chosen as a rational basis of its image. Concatenating them gives

\[
U\in GL_{120}(\mathbb Q),
\qquad U^{-1}U=I_{120},
\]

with isotypic block dimensions

\[
1,2,2,4,4,8,8,2,4,12,12,24,32,5.
\]

The forward transform has 3758 nonzero entries, maximum numerator 8, and maximum denominator 54. Its inverse has 1944 nonzero entries, maximum numerator 2, and maximum denominator 3.

The selector adjacency \(A\), shell operator \(D\), and minimum geometric splitter \(S\) are all exactly block diagonal in this basis. The frozen hashes are

```text
U     003cf8fcf294c519be28ead0cf197d4e5f964a83cbd85fee4f560fd138d2e19e
U^-1  9ba063ed7258c50e6f549a3aad02431f60164bda2b0b3bd689f0090836a116a0
A     0ac5d38775cadfd361167027b0ae63e69d0e439f4925119e34edbcf1af544d4e
D     feea2863c86906870f2ca48d6aaf8b96ffe31361d42e871b50fc0c9b84c10447
S     3ec8dfc439abd5bf7cc872f0d521091c3b98a6bb636d198cb83ab23a22e89085
```

**Boundary.** This is a canonical deterministic isotypic transform; bases inside repeated copies remain a rational gauge.

## Pass 1393 — Hinge-selected selector/apartment Steinberg bridge

The BT713 hinge sheet with mask `1110` and residual channel zero gives a boundaryless

\[
2160\times160
\]

apartment matrix of rank \(81\), hence the complete Levi cycle/Steinberg sector.

Each centered rectangle is incident with the unique matching selector on each of its two carrier lines. This gives degree two per rectangle and degree 36 per selector. Composing the incidence with the signed apartment rows and the two binary side/edge characters produces four natural \(120\times160\) maps. All four are boundaryless and all four have rank

\[
\boxed{81}.
\]

Their hashes are

```text
side0_edge0  38a9e954ca2c19e5a7f62ea9ddf2a61ab65c2243f5bd476144c619a2a7a61feb
side0_edge1  653d7d55f029e0d68f0d1fd6bbb94fe3331f0fa0e061f533c6752420040524a2
side1_edge0  af47f847179551a8c0915040e100a2a3b1c9831d0b7655861ff898e2cacbdbfe
side1_edge1  4cee7c51c1222c41c8c95d781e8176de1d2cf89112d442bcdfa5da2785ea50b4
```

Moreover, projecting the source through each of the fourteen Mackey projectors shows that every source isotypic sector survives with its full source dimension:

\[
1,2,2,4,4,8,8,2,4,12,12,24,32,5.
\]

These images overlap inside the common 81-dimensional target.

**Boundary.** The hinge and parity characters break full \(G\)-equivariance. Therefore this does not contradict

\[
\operatorname{Hom}_G(\mathbb Q^{120},E_4\mathbb Q^{160})=0.
\]

It is a gauge-fixed, rank-complete selector-to-Steinberg bridge, not a \(G\)-equivariant Morita equivalence.

## Pass 1394 — Integral orbital-order commensurability

Let \(O\) be the \(\mathbb Z\)-span of the 83 stabilizer orbitals and let

\[
M=\mathbb Z^7\oplus M_2(\mathbb Z)^2\oplus M_3(\mathbb Z)^3
\oplus M_4(\mathbb Z)\oplus M_5(\mathbb Z)
\]

be the split order selected by the frozen rational matrix units. Exact Smith arithmetic proves

\[
O\not\subset M,
\qquad
M\not\subset O.
\]

Their rational Smith-factor census is

\[
1^{21},\quad(1/2)^2,\quad3^{22},\quad9^6,
\quad18^{17},\quad54^9,\quad108^6.
\]

Writing \(L=O\cap M\),

\[
[M:L]=2^{38}3^{113},
\qquad
[O:L]=2^2.
\]

Equivalently, for the lattice sum \(O+M\),

\[
[O+M:O]=2^{38}3^{113},
\qquad
[O+M:M]=4.
\]

The bidirectional levels are

\[
2O\subset M,
\qquad
108M\subset O.
\]

The exact reduced-trace discriminant of \(O\) is

\[
\boxed{\operatorname{disc}(O)=2^{72}3^{226}}.
\]

Thus the orbital order is nonmaximal at 2 and 3 but passes the discriminant maximality test at 5, matching the characteristic-five semisimple reduction.

**Boundary.** Since the selected \(M\) does not contain \(O\), no conductor \(O\subset M\) is claimed. Constructing a conjugate maximal overorder containing \(O\) remains open.

## Reproducibility

Worker SHA-256 values:

```text
1390  4e41c2deb45231021530090f81ae7fba26a0dc8b54d58b198e9986f1bd051a64
1391  8ea57134011b39400aca5a169b2e5de2d4a1bfe1381005aeb9c447ef21457961
1392  39c19f72a725fe9921e47efc2ab3444892926b74800622fada83900ad4673208
1393  cff9adba6a40000ae333b10d57a135166af7057fdb564b711c05c0a4ba186ff4
1394  31e56730fb6841ad9a3c4e033e733a5e2ac97aac69d236efeb130b182da7a23f
```

The implementation is split into transparent source fragments and can be run as five isolated workers or one serial exact job. No floating eigensolver, database character table, particle assignment, hardware realization, or experimental claim is used.
