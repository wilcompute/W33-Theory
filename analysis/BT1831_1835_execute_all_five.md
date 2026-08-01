# Passes 1831--1835: Five Exact Resolution Fronts

## Summary

This packet executes the five continuations selected after the complete 3,547,800-cover census. It separates three levels that must not be conflated:

1. exact covers of the 540-frame carrier;
2. their 45-coordinate nonlinear octet signatures;
3. full nine-colour resolutions.

The central result is a sharp separation theorem. The nonlinear signature polytope has an exact nine-layer integer point, but the first symmetry orbit found has no lift to nine pairwise-disjoint frame covers. At the same time, the disjoint-pair relation is now completely classified over all 327 exact-cover orbit types.

## Pass 1831 -- Nine-signature polytope

Let `T` be the complete set of 720 globally realizable nonlinear cover signatures. Every `t in T` satisfies

\[
(A_{45}+4I)t=48\mathbf 1,
\qquad
\sum_o t_o=60.
\]

The integer signature-resolution equations are

\[
\sum_{t\in T} y_t=9,
\qquad
\sum_{t\in T}y_t t=12\mathbf 1,
\qquad y_t\in\mathbb Z_{\ge0}.
\]

An exact witness exists with nine distinct signatures. Its class composition is

\[
6T_{128}+3T_{96}.
\]

The nine vectors have pairwise inner products

\[
70^9,\qquad 74^6,\qquad 78^{21},
\]

and setwise stabilizer order 9 in `PSp(4,3)`. Hence this witness lies in a signature-resolution orbit of size

\[
25920/9=2880.
\]

The 46 displayed equations have rational rank 21, because the 45 coordinate equations live in the uniform line plus the 20-dimensional `-4` constituent. The real affine solution space in 720 variables therefore has dimension 699.

**Boundary.** This proves only that the nonlinear 45-coordinate quotient admits nine-layer integer points. It does not by itself produce nine disjoint exact covers.

## Pass 1832 -- Complete cover-orbit pair classification

For every one of the 327 `PSp(4,3)` exact-cover orbit representatives, every cover in every target orbit was reconstructed from the full 25,920-element action. The resulting matrix

\[
D_{ij}=\#\{C\in\mathcal O_j:C\cap C_i=\varnothing\}
\]

is exact and satisfies the double-counting identity

\[
|\mathcal O_i|D_{ij}=|\mathcal O_j|D_{ji}.
\]

Results:

- ordered orbit-type cells: `327^2 = 106,929`;
- compatible ordered cells: `106,761`;
- incompatible ordered cells: `168`;
- incompatible unordered orbit-type pairs: `89`;
- self-compatible orbit types: `317`;
- self-incompatible orbit types: `10`;
- compatible orbit-type degree range: `311..327`;
- disjoint covers per representative: `9,232..18,754`;
- global ordered disjoint cover pairs: `46,552,553,280`;
- global unordered disjoint cover pairs: `23,276,276,640`.

All orbit types still have at least one disjoint partner. The only signature-class blocks containing incompatibilities are those involving the `T_{96}` class or the small internal exceptions in `T_{128}`.

**Boundary.** This closes the complete pair layer. A global classification of simultaneous triple and quadruple packing orbits still requires a double-coset recursion beyond pair compatibility.

## Pass 1833 -- Representation derivation of the four signature classes

The octet graph is

\[
\operatorname{SRG}(45,32,22,24),
\]

with spectrum

\[
32^1\oplus2^{24}\oplus(-4)^{20}.
\]

For every signature there is a unique anchor octet. The anchor stabilizer has order

\[
25920/45=576.
\]

Its twelve non-neighbours form three independent four-cells, i.e. `K_{4,4,4}`. The induced action on the three cells is onto `S_3`, with kernel order 96:

\[
1\to K_{96}\to G_o\to S_3\to1.
\]

The sixteen signatures above one anchor are exactly the permutations of four cell-value patterns:

| cell pattern | local orbit | `S_3` stabilizer | global orbit | global stabilizer |
|---|---:|---:|---:|---:|
| `(0,2,4)` | 6 | 1 | 270 | 96 |
| `(0,3,3)` | 3 | 2 | 135 | 192 |
| `(1,2,3)` | 6 | 1 | 270 | 96 |
| `(2,2,2)` | 1 | 6 | 45 | 576 |

Thus the four global signature orbit sizes

\[
270,135,270,45
\]

are derived directly from the anchor `S_3` quotient, rather than inferred from the exhaustive census.

## Pass 1834 -- Outer fusion and chirality audit

The canonical multiplier-minus-one outer involution fixes seven octets and swaps nineteen octet pairs. On the 720 signatures it preserves all four nonlinear classes and has fixed-point counts

\[
(6,9,6,7),
\]

leaving 28 signatures fixed and exchanging 346 pairs.

On the 327 inner exact-cover orbits it fixes only five and exchanges 161 pairs. By signature class, the fixed-orbit counts are

\[
(0,2,0,3).
\]

The full 327-by-327 disjointness matrix is invariant under this outer permutation. Therefore outer chirality is visible at the cover-orbit level even though the four nonlinear signature classes themselves are not fused: their norms and anchor-cell patterns already distinguish them.

## Pass 1835 -- Proof-producing lift obstruction

The Pass-1831 witness contains six `T_{128}` signatures and three `T_{96}` signatures. Using the complete 327-orbit cover census, the exact candidate cover counts for its nine colours are

\[
(11664,11664,2808,11664,2808,2808,11664,11664,11664).
\]

A deterministic nine-partite exact-cover search tests all possible choices, dynamically selecting the colour with the fewest currently disjoint candidates. It closes after

\[
4421\text{ nodes},\qquad4188\text{ dead ends},
\]

with trace hash

```text
c9cb284a87c2191d
```

and returns `UNSAT` for this fixed signature system. The candidate binary regenerates identically with SHA-256

```text
36742beb39510a916578e20aa50dd089b7f6d5231856e3658562efb354a17387
```

Therefore none of the 2,880 symmetry-equivalent nine-signature solutions in this orbit lifts to a Hoffman resolution.

**Critical boundary.** This is not a global nine-cover impossibility proof. Other integer points of the nonlinear signature polytope may lie in other `PSp(4,3)` orbits and may have different lift behaviour.

## Evidence stack

The release includes:

- deterministic Python verifier and frozen aggregate certificate;
- exact C++ cover-orbit pair worker;
- exact C++ outer orbit-fusion worker;
- exact C++ nine-signature lift worker;
- focused regression and fail-closed CI;
- a shared manuscript insert promoted into both `w33_paper.tex` and `photonic_holonet.tex`.
