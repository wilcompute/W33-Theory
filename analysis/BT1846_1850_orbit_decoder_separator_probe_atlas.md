# Passes 1846–1850 — two signature no-lift orbits, exact weight-five decoding, the duad–syntheme transfer algebra, probe fusion, and the official-tuple boundary

## Executive result

The five continuation fronts are closed to their exact evidence boundaries.

1. The independently owned Passes 1841–1845 packet is reconciled: two distinct inner signature-resolution orbits of sizes 2,880 and 25,920 are certified, and both have exact frame-level no-lift proofs. Thus at least 28,800 signature resolutions exist, but neither certified orbit produces a nine-cover resolution. The binary orbit census remains incomplete.
2. The low-weight binary frame-code enumerator is exact through weight ten:
   \[A_4=540,\quad A_6=9,600,\quad A_8=424,170,\quad A_{10}=17,523,360.\]
   Sorting all fixed-coordinate weight-five syndromes gives the exact global partition
   \[6,363,048,048=84,201,264+2,993,248,416+3,285,598,368,\]
   into lower-shadowed, unique-minimum, and ambiguous-minimum errors. The fifth-order BSC success term is
   \[\boxed{2,993,248,416\,p^5(1-p)^{235}}.\]
3. The six-fiber plus duad separator carries the exact check algebra
   \[\boxed{240=20+15\cdot12+20\cdot2}.\]
   The residual checks are the 20 triangles of \(K_6\), the 15 fiber pairs map bijectively to the 15 synthemes, and the 20 fiber triples each carry two phase checks. This is the classical duad–syntheme model of the exceptional outer automorphism of \(S_6\).
4. The four geometric outer probes fuse exactly to ATLAS classes \(2D,4C,6H,8A\). Their centralizers are \(96,96,36,8\), and their literal shortest words in the project standard pair have lengths \(18,12,16,17\).
5. The official-tuple conjugacy algorithm is implemented and passes an exact synthetic relabelling test. The official ATLAS `.g1/.g2` endpoints were inaccessible from this execution environment, so the byte-level official conjugacy claim is correctly withheld.

## Pass 1846 — reconciliation of the parallel signature-orbit packet

The parallel packet has aggregate certificate SHA-256

```text
74fe918ebe6f2609e678363e4602a68ffb186e0571f1b5817757035828471063
```

It certifies two inner solution orbits:

- size 2,880, stabilizer \(C_3\times C_3\), type multiset `6T128+3T96`, exact no-lift;
- size 25,920, trivial stabilizer, type multiset `3T128+2T120+2T104+2T96`, exact no-lift.

The first witness has three 3-point stabilizer orbits and an intrinsic \(2K_3/K_{3,3}\) Gram geometry. The second orbit is free. The canonical outer involution stabilizes both known inner orbits. This is a rigorous lower bound of 28,800 signature-level solutions, not a complete census and not global nine-cover UNSAT.

## Pass 1847 — exact low-weight enumerator and decoder coefficient

A parity-guided DFS on the 45-check hypergraph fixes one coordinate and uses coordinate transitivity. It reconstructs

\[
A_4=540,\quad A_6=9600,\quad A_8=424170,\quad A_{10}=17523360.
\]

The complete weight-five collision-edge count is

\[
11,773,222,560,
\]

with contributions

\[
3,503,962,800+2,617,056,000+3,444,260,400+2,207,943,360
\]

from weights 4, 6, 8, and 10.

All

\[
\binom{239}{4}=132,563,501
\]

weight-five errors containing coordinate zero are enumerated and sorted by syndrome. Since every check column has odd weight, syndrome parity equals error parity; only weights one and three can undercut weight five. The fixed-coordinate partition is

\[
132,563,501=1,754,193+62,359,342+68,449,966.
\]

Globalizing by \(240/5=48\) gives

\[
\boxed{6,363,048,048=84,201,264+2,993,248,416+3,285,598,368}.
\]

The exact success polynomial through weight five is

\[
\begin{aligned}
&(1-p)^{240}+240p(1-p)^{239}+25440p^2(1-p)^{238}\\
&\quad+1576000p^3(1-p)^{237}+63416280p^4(1-p)^{236}\\
&\quad+2993248416p^5(1-p)^{235}.
\end{aligned}
\]

No asymptotic threshold is inferred from this truncated polynomial.

## Pass 1848 — the duad–syntheme transfer algebra

Relative to one maximum six-line packing, the 240 checks split into:

- 20 residual checks, exactly the \(\binom63=20\) triangles of \(K_6\) on the 15 residual duads;
- 180 pair-transfer checks, twelve for each of the 15 fiber pairs;
- 40 phase checks, two for each of the 20 fiber triples.

For each fiber pair, the three residual duads absent from its twelve transfer checks form a perfect matching of the six labels. All fifteen perfect matchings occur exactly once. The resulting duad-to-syntheme map is a concrete exceptional outer automorphism of \(S_6\).

Boundary: the transfer tensors are exact, but their complete contraction across the middle layer remains open.

## Pass 1849 — stable outer-probe fusion

The geometric probes are fused by literal conjugacy to official ATLAS class-representative words evaluated in the project standard pair:

| probe fingerprint | class | centralizer | shortest project word length |
|---|---:|---:|---:|
| \((2;8,6,16,7)\) | \(2D\) | 96 | 18 |
| \((4;0,4,6,3)\) | \(4C\) | 96 | 12 |
| \((6;0,1,3,3)\) | \(6H\) | 36 | 16 |
| \((8;2,0,0,1)\) | \(8A\) | 8 | 17 |

The compact words are frozen in the certificate and evaluate literally to the canonical permutations.

## Pass 1850 — official-tuple bridge boundary

The official ATLAS representation page identifies the 40-point representation and the `.g1/.g2` GAP payloads. The worker parses cycle notation and solves

\[
hc_0=ch,\qquad hd_0=dh
\]

by propagating each of forty possible images of a base point. A deterministic synthetic relabelling produces exactly one conjugator and passes literal checks for both generators.

During this execution the primary-source payload endpoints returned cache misses and the isolated container had no network name resolution. The code and URLs are frozen, but no byte-level official conjugacy result is fabricated.

## Verification

The aggregate certificate is fail-closed. Focused local regression passes 2/2. The exact fixed-coordinate syndrome sorter reruns in approximately twelve seconds and uses about one gigabyte of memory. The heavier low-weight DFS also reproduced all four enumerator coefficients locally; CI keeps that worker available behind the explicit heavy-worker flag.
