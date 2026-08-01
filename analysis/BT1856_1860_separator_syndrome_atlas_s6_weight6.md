# Passes 1856–1860 — residual contraction, syndrome orbits, literal ATLAS tuple reconciliation, exceptional S6 intertwiner, and weight-six frontier

## Executive result

The aggregate certificate SHA-256 is

```text
c409b43e3e658ba273fa440e59a479a7d60d8636c3ae33fcae409180b15facca
```

The packet closes three fronts exactly and two to explicit proof boundaries.

1. The 15-duad residual tensor contracts exactly into 156 natural S6 orbits. All fifteen pair-transfer tensors have binary rank 7, all twenty phase tensors have rank 2, and the rowspace binomial moments are exact through order 11. The remaining six-fiber contraction has a certified separator-first induced width of 40, so the complete weight enumerator is not claimed.
2. The complete odd lower-syndrome set contains 1,892,792 syndromes in exactly 110 PSp(4,3)-orbits: one weight-one orbit and 109 weight-three orbits. Combined with the exact fixed-coordinate weight-five multiplicity sort, this is a fail-closed symmetry-compressed lower-shadow decoder.
3. The independently owned Pass 1855 packet retrieved and froze the official ATLAS 40a generator payloads and proves a unique simultaneous conjugator to the project standard pair. Pass 1858 reconciles that literal byte-level result, including both payload hashes and the conjugator hash.
4. The W33 duad-to-syntheme map is promoted to an explicit unimodular 15x15 integer matrix P with det(P)=-1. It intertwines the natural duad action with the outer-twisted syntheme action, maps each adjacent transposition to a triple transposition, and generates the full S6 image.
5. A deterministic 500,000,000-node weight-twelve proof search certifies A12 >= 5,323,560. Consequently the weight-six equal-syndrome collision count is
   E6 = 1,312,130,546,100 + 462 A12
   and is at least 1,314,590,030,820. A12 and the sixth-order unique-minimum coefficient remain open.

## Pass 1856 — exact residual contraction frontier

With the six fiber variables set aside, the fifteen residual duads form a dimension-15 subcode. Its complete 32,768-word weight enumerator is frozen. The natural S6 action reduces those assignments to exactly 156 orbits. Restriction ranks are 15 for the residual sector and 30 for the fiber sector. Every pair tensor has rank 7; every triple-phase tensor has rank 2.

MacWilliams differentiation using A4=540, A6=9,600, A8=424,170, and A10=17,523,360 gives every global binomial moment sum_w A_w binom(w,r) through r=11. The exact residual and local contractions therefore close, but the six-fiber phase-coupled contraction does not.

## Pass 1857 — lower odd syndrome orbit atlas

All 240 weight-one errors and all 2,275,280 weight-three errors were grouped by their 45-bit syndrome. There are 1,892,792 distinct lower odd syndromes. Exact BFS under the five certified octet permutations yields 110 orbits. One orbit has minimum weight one and 109 have minimum weight three; the orbit data collapse to 27 multiplicity/weight types.

The exact weight-five partition from Pass 1847 is retained:

6363048048 = 84201264 + 2993248416 + 3285598368,

for lower-shadowed, unique-minimum, and ambiguous-minimum errors. The lower-shadow decoder is orbit-complete; a full orbit decomposition of all minimum-weight-five syndromes remains open.

## Pass 1858 — literal official tuple reconciliation

During this release, the independently owned Pass 1855 worker successfully retrieved and froze the official ATLAS 40a GAP generator pair.  The two payload hashes are

`ee9c5dbc42a452acfef5d988ba2c09d96e5bc4ae99de63bb24586933286db1f2`

and

`cb97373668ca18afc16fcc22d1b231bbe73922ad3c6164e4b18d5e729a32b894`.

The unique simultaneous conjugator to the project standard pair has SHA-256

`c269967dfc4a94fe69aba300a86db9dbc7606a44914f2be922a79f1c8b7bc2a4`.

Literal checks hold for both generators; the official pair has orders $2$ and $9$, product order $10$, generated group order $51{,}840$, and point suborbits $1,12,27$.  Pass 1858 independently reconciles the source schema, certificate hash, payload hashes, standard-generator conditions, and unique conjugator.  The boundary is only that this identifies the official ATLAS 40a pair, not unrelated representations or alternative standard pairs.

## Pass 1859 — integral exceptional-S6 intertwiner

Order the fifteen duads lexicographically and the fifteen synthemes canonically. The W33 map is the permutation

(8,12,4,0,10,3,2,9,14,11,7,1,13,6,5).

Its permutation matrix P has rank 15 and determinant -1. For all five adjacent transpositions s_i,

P rho_duad(s_i) = rho_syntheme(alpha(s_i)) P.

Every alpha(s_i) is a triple transposition, the Coxeter relations hold exactly, and the images generate all 720 elements. This is a literal integral realization of the exceptional outer automorphism of S6.

## Pass 1860 — weight-six proof frontier

The exact weight-six population is C(240,6)=249,219,381,880. Equal-syndrome pairs differ by a codeword of weight 4,6,8,10, or 12. The known contribution is

204105833100 + 202385664000 + 397812076200 + 507826972800
= 1312130546100,

and the missing term is 462 A12.

The capped exact DFS visits 500,000,000 nodes and finds 266,178 valid weight-twelve supports through coordinate zero. Coordinate transitivity gives

A12 >= 20*266178 = 5323560.

Thus E6 >= 1314590030820. Since the A12 search is incomplete and lower-shadow incidences are not deduplicated, no sixth-order BSC success coefficient is promoted.
