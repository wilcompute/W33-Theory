# Passes 6541–6544 — Full doily Veldkamp space from the quadratic-evaluation code

## Status

**PASS — exact finite binary geometry/coding theorem.** This packet extends Passes 6533–6540 from the 31 Veldkamp points to all 155 Veldkamp lines.

## Pass 6541 — projectivization is the whole Veldkamp space

The Pass6533 code has dimension five over \(\mathbb F_2\). Therefore its 31 nonzero words are the points of
\[
\boxed{PG(4,2)}.
\]
Every projective line is a triple
\[
\boxed{\{u,v,u+v\}},
\]
and exhaustive deduplication gives exactly
\[
\boxed{155}
\]
such triples. This matches the complete line count of the doily Veldkamp space, not merely its point count.

## Pass 6542 — the five Veldkamp line types are recovered exactly

For each code line \(\{u,v,u+v\}\), take the common zero-set core of its three hyperplane words and classify it using the doily line geometry already reconstructed by \(C^\perp\). The exact census is
\[
\boxed{15+15+60+20+45=155},
\]
namely:

- 15 single-point cores, with hyperplane-weight composition \((8,10,10)\);
- 15 collinear-triple cores, with composition \((8,8,8)\);
- 60 unicentric-triad cores, with composition \((6,8,10)\);
- 20 tricentric-triad cores, with composition \((8,8,8)\);
- 45 pentad cores, with composition \((6,6,8)\).

This exactly reproduces the five-type Veldkamp-line census of Saniga--Planat--Pracna--Havlicek.

## Pass 6543 — the dual resolves the only weight-composition ambiguity

Weight composition alone gives 35 all-perp lines of type \((8,8,8)\). The minimum supports of \(C^\perp\) split them canonically:
\[
\boxed{35=15_{\rm collinear}+20_{\rm tricentric}}.
\]
The 15 cores that are minimum dual supports are exactly the doily lines; the remaining 20 three-point cores are tricentric triads. Thus the dual code is essential to the *line-level* reconstruction of the Veldkamp geometry.

## Pass 6544 — hyperplane fusion laws

Because the 15 weight-eight words are the nonzero simplex subcode and the 16 quadratic words form its other coset, the projective-line addition laws are exact:
\[
\boxed{6+6\to8\quad(45\text{ pairs})},
\]
\[
\boxed{10+10\to8\quad(15\text{ pairs})},
\]
\[
\boxed{6+10\to8\quad(60\text{ pairs})},
\]
\[
\boxed{8+8\to8\quad(105\text{ pairs})}.
\]
So every pair of quadratic hyperplanes adds to a perp word, while the perp words close among themselves. The line types are then determined by the plus/minus quadratic species together with the common-core geometry.

## Prior-art and scope boundary

The abstract result \(\mathcal V(W(2))\cong PG(4,2)\), including the 31 hyperplanes and 155 lines with five core types, is established prior art (arXiv:0704.0495). This packet makes no novelty claim for that classification. The repo-level advance is that the explicit Pass6533 quadratic-evaluation code and its dual reconstruct the *entire* incidence space and its five line types by executable linear-code operations.

Everything here remains finite binary geometry/coding. No physical or continuum inference follows without an additional explicit map.
