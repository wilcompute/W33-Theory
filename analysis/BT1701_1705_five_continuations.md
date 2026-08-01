# Passes 1701–1705 — torsion filtration, resolution XORs, chiral packing, lattice bridge, and coherent configuration

## Executive result

This packet executes all five continuations opened by Passes 1601–1605 after reconciling the parallel Passes 1537–1541 and a late 1606–1610 glue-track reservation. The deterministic verifier rebuilds W(3,3), the 540-frame carrier, the 45 intrinsic K4,4 octets, the Bockstein map, both edge lattices, and the full PSp(4,3) action. All ten release assertions pass under certificate SHA-256

```text
21ac733526331abf8065e67135abd3093f2c910910f03f07746e9432e1fdf330
```

The global nine-cover resolution remains open.

## Pass 1701 — complete modular structure of the 30-dimensional torsion

The Bockstein quotient $T\cong\mathbb F_2^{30}$ is not irreducible and is not semisimple. Its exact nonsplit filtration has composition factors

\[
\boxed{1,6,8,1,14.}
\]

There is a distinguished 16-dimensional submodule with Loewy profile $1\mid(6\oplus8)\mid1$ and an absolutely irreducible 14-dimensional head. The factor 6 is absolutely irreducible. The factor 8 is irreducible over $\mathbb F_2$ with endomorphism field $\mathbb F_4$. Exact section equations prove both relevant extensions nonsplit.

## Pass 1702 — independent XOR compiler

The 45 octets yield 405 exact-cardinality equations, each supported on 72 frame/color variables. Modulo two they expose thirty Bockstein directions per color. For the full nine-color system,

\[
\boxed{2100\longrightarrow2340,}
\]

a gain of 240. A deterministic basis uses thirty octet rows for each of colors 0 through 7; color 8 is forced by the frame-partition equations. The exporter writes 240 independent XOR equations and all 405 exact-eight equations with frozen SHA-256 hashes. No timeout is promoted to SAT or UNSAT.

## Pass 1703 — chiral four-packing orbit

The certified four-cover packing has trivial $PSp(4,3)$ stabilizer. Its orbit and the anti-symplectic mirror orbit both have size 25,920 and fuse under $PGSp(4,3)$:

\[
\boxed{25920+25920=51840.}
\]

The two residual systems have identical Bockstein signature: residual rank 195, augmented rank 225, gain 30, residual-$J$ rank 44, used octet degree 32, and residual degree 40. Their residual octet Gram matrices are exactly outer-conjugate. Binary torsion therefore cannot distinguish this chirality.

## Pass 1704 — saturated free-15 bridge

For the saturated point $(-4)$-eigenlattice $L$,

\[
\operatorname{SNF}(N^TL)=1^{14}\oplus2,
\qquad
\operatorname{SNF}(d^TL)=1^{14}\oplus4.
\]

After saturation, the canonical unsigned-to-oriented transition is integral with

\[
\boxed{\operatorname{SNF}=1^{14}\oplus2,\qquad|\det|=2.}
\]

Thus the previous factor 6 separates into common ternary index 3 and one unavoidable orientation-parity factor 2.

## Pass 1705 — frame/octet coherent configuration

The action on 540 frames and 45 octets is a two-fiber coherent configuration of rank

\[
\boxed{32+3+5+5=45.}
\]

Cross subdegrees are $1,6,6,8,24$ and $12,72,72,96,288$. The half-incidence cross orbital $J$ has octet Gram coefficients $72,6,9$ and satisfies

\[
(H-32I)(H-14I)(H-2I)J=0,
\qquad \operatorname{rank}[J,HJ]=69.
\]

Spectral coupling ranks are $32\to32:1$, $2\to14:24$, $2\to2:24$, and $-4\to14:20$.

## Evidence boundary

All module, orbit, rank, Smith, export, conjugacy, and coherent-configuration statements are finite exact computations. The packet does not decide the global Hoffman nine-coloring, prove the known four-packing family exhaustive, establish a decoding threshold, or infer continuum physics.
