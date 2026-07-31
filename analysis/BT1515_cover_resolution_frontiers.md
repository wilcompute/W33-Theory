# Passes 1511–1515 — Cover resolution frontiers

## Executive result

The sampled “exact covers form an intersecting family” conjecture is false. Its
apparent evidence came from a hidden conditioning: the Pass 1505/1510 DFS fixes
frame `0` before recursion, so every sampled cover contains frame `0` and the
sample is pairwise intersecting by construction.

The global exact family contains literal disjoint covers. More strongly, the
frozen 327-orbit frontier contains a four-cover packing, while the selected
packing leaves a regular residual incidence system with a fractional fifth layer
but no integral fifth layer.

## Pass 1511 — Disjoint-pair correction

Two explicit 60-frame subsets are verified exact covers of the 240 edge columns
and have empty intersection. The canonical cover is in frozen orbit 0; its
partner is in frozen orbit 29.

Thus

\[
  \mathcal C_0\cap\mathcal C_1=\varnothing.
\]

The previous sampled-pair test did not probe this question: all 327 frozen prefix
representatives contain frame 0 because the DFS symmetry break starts with frame
0 already selected.

## Pass 1512 — Every known orbit type has a disjoint partner

Acting with \(\PSp(4,3)\) on all 327 frozen orbit representatives and filtering
against the canonical cover gives:

\[
  13648
\]

distinct disjoint covers. Every one of the 327 orbit types contributes at least
one. Before quotienting by each cover stabilizer, the group action produces
32464 disjoint images.

Per orbit, the number of distinct disjoint covers ranges from 4 to 88, with
median 42. Grouped by stabilizer order, the totals are

\[
  |H|=2:11376,\qquad |H|=4:2116,\qquad |H|=8:156.
\]

## Pass 1513 — Disjointness graph and four-cover packing

Let \(\Gamma_\perp\) be the graph on the 13648 disjoint partners, with adjacency
meaning frame-disjointness. Exact bitset enumeration gives

\[
 |V(\Gamma_\perp)|=13648,
 \qquad |E(\Gamma_\perp)|=188338,
\]

\[
 \#K_3=494,
 \qquad \#K_4=0.
\]

Hence

\[
 \omega(\Gamma_\perp)=3.
\]

Adding the fixed canonical cover gives an explicit packing of four mutually
disjoint exact covers. Inside the certified 327-orbit frontier, no packing that
contains the canonical cover has five members.

The four selected cover stabilizers are

\[
 C_2,\qquad C_2\times C_2,\qquad C_2,\qquad C_2.
\]

## Pass 1514 — Uniform class-45 involution lock

The projective group has 315 involutions, split into conjugacy classes of sizes
45 and 270. Every one of the 228 frozen orbit types with stabilizer \(C_2\) uses
the small class-45 involution. In every case that involution fixes

\[
 84\text{ of the }540\text{ frames}
\]

and exactly

\[
 12\text{ of the }60\text{ frames in the stabilized cover}.
\]

This promotes the earlier one-cover observation to the full C2-stabilized
frontier.

The \(C_2^2\) member of the four-packing contains one class-45 involution with
profile \((84,12)\) and two class-270 involutions with profile \((24,8)\).

## Pass 1515 — Fractional fifth layer, integral obstruction

Deleting the four packing covers leaves 300 frames. Their residual incidence
matrix has 240 edge columns and is exactly

\[
 4\text{-uniform by rows},\qquad 5\text{-regular by columns}.
\]

Therefore the constant row weighting

\[
 x_r=\frac15
\]

is a fractional exact cover:

\[
 M_{\rm res}^{\mathsf T}x=\mathbf 1,
 \qquad \sum_r x_r=60.
\]

However a deterministic exhaustive Algorithm-X search proves that no integral
0–1 exact cover exists. The search closes after 2332 recursive nodes and 18227
forced-row propagations; its complete trace is frozen by SHA-256.

Thus this selected four-packing has an exact integrality gap:

\[
 \text{fractional fifth layer exists},
 \qquad
 \text{integral fifth layer does not}.
\]

## Evidence boundary

The four-packing is globally maximal only with respect to adding a fifth cover to
that specific packing. The clique computation is exhaustive only inside the
frozen 327-orbit frontier. The global packing number over undiscovered orbit
types or different four-packings remains open.
