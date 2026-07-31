# Passes 1370–1374 — Five exact selector frontiers

## Scope

Let \(X\) be the 120 line-matching selectors of \(W(3,3)\), let \(H\) be a selector stabilizer in \(G=\operatorname{PGSp}(4,3)\), and let

\[
T(x)\subset \mathcal A=\operatorname{End}_{H}(\mathbb Q^X)
\]

be the 79-dimensional Terwilliger and 83-dimensional orbital algebras from Passes 1360–1369. This packet executes all five open fronts from that release.

## Pass 1370 — Literal rational matrix units

For each rational block \(z\mathcal A\cong M_n(\mathbb Q)\), a primitive corner \(e\le z\) is chosen. Exact bases of \(\mathcal Ae\) and \(e\mathcal A\) are dualized under the pairing \(e\mathcal A\times\mathcal Ae\to\mathbb Qe\). The resulting

\[
E_{ij}=u_iw_j
\]

satisfy

\[
E_{ij}E_{k\ell}=\delta_{jk}E_{i\ell},\qquad \sum_iE_{ii}=z
\]

exactly. All

\[
7\cdot1^2+2\cdot2^2+3\cdot3^2+4^2+5^2=83
\]

matrix units are constructed and frozen by fourteen rational-coordinate hashes. The maximum denominator is 108 and maximum absolute numerator is 10.

## Pass 1371 — Selector stabilizer

The order-432 stabilizer has element-order census

\[
1^1\,2^{87}\,3^{26}\,4^{72}\,6^{210}\,12^{36}.
\]

Its normal 3-core is elementary abelian:

\[
O_3(H)\cong C_3^3.
\]

The quotient is \(D_8\times C_2\), an order-16 complement exists, and its faithful action on \(\mathbb F_3^3\) has invariant decomposition \(1+2\). Therefore

\[
\boxed{H\cong C_3^3\rtimes(D_8\times C_2).}
\]

## Pass 1372 — Minimum Schur completion

The defect blocks contain 8 and 16 stabilizer orbitals. All \(8\cdot16=128\) cross-block pairs were tested. Exactly eight complete \(T(x)\) to dimension 83. The minimum support is

\[
\boxed{540},
\]

and the only minimum symmetric pairs are

\[
\boxed{\{18,63\}},\qquad\boxed{\{18,64\}}.
\]

Thus the Pass-1366 splitter is support-minimal and has exactly one equally minimal intrinsic sibling.

## Pass 1373 — Bad characteristics

The integral \(A,D\)-word lattice is not saturated at \(2,3,5\): its generated reductions have dimensions \(42,54,74\), not 79.

For the word-generated Terwilliger reductions,

\[
\dim(J,J^2,J^3)=(22,6,0)\quad(p=2),
\]

\[
\dim(J,J^2,J^3,J^4,J^5,J^6)=(48,36,22,13,4,0)\quad(p=3),
\]

and the 74-dimensional \(p=5\) reduction is semisimple.

The literal 83-dimensional orbital algebra has

\[
(45,16,0)\quad(p=2),
\]

\[
(72,49,27,14,4,0)\quad(p=3),
\]

and is semisimple at \(p=5\). Every terminal regular-module factor is exhaustively checked on all projective vectors; the resulting radicals are verified nilpotent two-sided ideals. Characteristic three is the deepest degeneration on both sides.

## Pass 1374 — Selector–Levi Morita obstruction

The full group has four orbits on the 160 flags times the 120 selectors, of sizes

\[
480,1440,4320,12960,
\]

with bidegrees

\[
(4,3),(12,9),(36,27),(108,81).
\]

Hence the natural equivariant cross-orbital space has dimension four. Its common channels have ranks \(1,24,15,24\), and every channel annihilates the terminal flag idempotent of dimension 81:

\[
\boxed{\operatorname{Hom}_G(\mathbb Q^{120},E_4\mathbb Q^{160})=0.}
\]

The maximum cross-map rank is 40. Therefore the natural selector/flag bimodule is not a Morita bridge to the Levi Steinberg sector. The verified route remains the 2160 rectangle/apartment selector-sheet construction.

## Reproducibility

Ten isolated workers cover the four nonmodular fronts and the six pairs

```text
(full orbital, Terwilliger word-generated) × (2,3,5).
```

Focused certificate tests, per-worker comparison, collision guarding, two-pass manuscript integration, and an independent theorem compilation are included.

Frozen compact certificate SHA-256:

```text
284d9d7f9462a83f0709734d48a3ccf3284da2cb6b5ede159da5c719b84332b9
```

## Boundary

These are finite group, rational-algebra, modular-algebra, and equivariant-bimodule results. No literature-priority, cosmological, Standard-Model, optical-hardware, or laboratory claim is made.
