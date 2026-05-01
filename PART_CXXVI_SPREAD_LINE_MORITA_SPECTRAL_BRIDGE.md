# Part CXXVI — Spread-Line Morita Spectral Bridge

**Status:** theorem-grade structural extension  
**Date:** April 29, 2026

Part CXXV isolated the `A2` null plane in the coarse chirality quotient of the complete two-qutrit MUB-frame overlap form. Looking back through the spread algebra and the paper's `1+24+15` W33 decomposition reveals the bigger statement: the spread incidence matrix itself is a rectangular Morita bridge between the 40-line W33 carrier and the 36-spread complete-MUB-frame carrier.

## 1. The incidence matrix

Let

```text
B[line, spread] = 1 iff the W(3,3) line belongs to the spread.
```

Here

```text
40 lines = maximal commuting two-qutrit Pauli contexts,
36 spreads = complete two-qutrit stabilizer MUB frames.
```

Each line lies in exactly 9 spreads, and each spread contains exactly 10 lines. Hence `B` is a `40 x 36` matrix with row sum `9` and column sum `10`.

## 2. Line side

Two W33 lines occur together in a spread exactly when they are disjoint, and then in exactly 3 spreads. Therefore

\[
BB^T = 9I_{40}+3D,
\]

where `D` is the line-disjointness graph.

The line-disjointness graph is

\[
SRG(40,27,18,18),
\]

with spectrum

\[
27^1,\quad 3^{15},\quad (-3)^{24}.
\]

Thus

\[
\operatorname{Spec}(BB^T)=90^1,\quad 18^{15},\quad 0^{24}.
\]

So the line-side carrier decomposes as

\[
40 = 1 + 15 + 24,
\]

and the incidence map kills exactly the `24`-dimensional W33 matter/self-dual block while preserving the common `1+15` block.

## 3. Spread side

The spread Gram matrix is the complete MUB-frame total-overlap matrix:

\[
G := B^T B.
\]

Its diagonal entries are `10`, and its off-diagonal entries are exactly `1` or `4`, according as two complete MUB frames share one basis or four bases.

Let `A_4` be the four-overlap graph on the 36 spreads. Then

\[
G = J_{36}+9I_{36}+3A_4.
\]

The four-overlap graph is

\[
SRG(36,15,6,6),
\]

with spectrum

\[
15^1,\quad 3^{15},\quad (-3)^{20}.
\]

Therefore

\[
\operatorname{Spec}(G)=90^1,\quad 18^{15},\quad 0^{20}.
\]

So the spread-side carrier decomposes as

\[
36 = 1 + 15 + 20,
\]

and the complete MUB-frame total-overlap form has a 20-dimensional exact kernel.

## 4. The Morita bridge theorem

**Theorem CXXVI (Spread-Line Morita Spectral Bridge).** The line-spread incidence matrix

\[
B:\mathbb R^{36}_{\mathrm{spreads}}\longrightarrow \mathbb R^{40}_{\mathrm{lines}}
\]

has rank

\[
\operatorname{rank}B=16=1+15.
\]

It implements the exact correspondence

\[
\boxed{
\mathbb R^{40}_{\mathrm{lines}} = 1\oplus 15\oplus 24,
\qquad
\mathbb R^{36}_{\mathrm{spreads}} = 1\oplus 15\oplus 20,
\qquad
B:\;1\oplus 15\xrightarrow{\sim}1\oplus 15.
}
\]

The `24`-dimensional line-side block is the left null/cokernel block of `B`, and the `20`-dimensional spread-side block is the right null/kernel block of `B`.

Equivalently,

```text
B preserves the common vacuum+gauge spine 1+15,
B kills the 24 line-side block,
B kills the 20 spread-side overlap-null block.
```

## 5. Normalized overlap Hamiltonian

Normalize the spread Gram operator by `18`:

\[
H_{\mathrm{MUB}}=\frac{1}{18}B^TB.
\]

Then

\[
\operatorname{Spec}(H_{\mathrm{MUB}})=5^1,\quad 1^{15},\quad 0^{20}.
\]

This is the cleanest positive-semidefinite MUB-frame Hamiltonian currently visible in the program. It is finite, exact, rank `16`, and its nonzero sector is precisely the common `1+15` Morita spine.

## 6. Meaning

The recent `A2` null plane is the coarse quotient shadow of a much larger statement:

```text
A2 null plane subset 20-dimensional complete-MUB overlap kernel.
```

The 20-dimensional hidden sector is not merely the one-overlap valency. It is the exact kernel of the complete MUB-frame Gram form.

The 24-dimensional W33 sector and the 20-dimensional MUB-frame sector are dual obstructions to the same rectangular incidence bridge. The bridge keeps only the `1+15` common spine, which is why the number `16` keeps reappearing as the surviving spinor/rank channel.

## 7. Paper insertion point

This belongs in the qutrit/MUB spread section immediately after the 36-spread and overlap-count theorem. It should also be cross-referenced from any section discussing the paper's `1+24+15` decomposition, because the spread carrier supplies its complementary `1+15+20` Morita partner.

The accompanying regression tests are in:

```text
tests/test_spread_line_morita_bridge_cxxvi.py
```
