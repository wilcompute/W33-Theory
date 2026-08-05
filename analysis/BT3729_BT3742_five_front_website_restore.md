# Passes 3729–3742 — Five-front closure and exact website restoration

## Website restoration

The long-form public website was not reconstructed from fragments. `docs/index.html` was restored byte-for-byte from blob

`41a8d733f42da18282fa276f5d2fa82bac7516f6`

at commit `df5c52314bf4c8c4b0d7a1b1f0afb66d872bdfb6`, the parent immediately before commit `413ed869b1ae82446df3583e43c3f9bcb365a18c` replaced it with 86 added lines and 28,865 deleted lines.

The compact architecture landing page that was present immediately before restoration is preserved byte-for-byte at

`docs/source-derived-architecture-landing-2026-08-05.html`

with blob

`94e90827ec73fc20e632fba5519fed2d109846d6`.

## 1. Cubic transversal: 106 ≤ τ ≤ 178

Let `T` be the 240×5,040 incidence matrix of the cubic dependency deck and let `D=TT^T-63I`.  For a transversal indicator `x` of size `m`, write `h_t` for the number of selected faces in dependency triple `t` and

`P = sum_t binom(h_t,2) = (1/2)x^T D x`.

The weighted pair operator is 126-regular with minimum eigenvalue −18, so

`P >= (3/10)m^2 - 9m`.

Because every hit count belongs to `{1,2,3}`,

`P <= (3/2)(63m-5040)`.

Combining them gives

`(m-105)(m-240) <= 0`.

At `m=105`, both real bounds meet at `4725/2`, while `P` is integral.  Therefore

`τ >= 106`.

An explicit 62-face cubic cap contains no dependency triple.  Its complement is a 178-face transversal with hit profile

`1^844 2^2218 3^1978`,

so

`106 <= τ <= 178`.

This is a new cubic-deck interval, not the 720-coordinate covering-radius interval, which remains `389 <= R <= 435`.

## 2. Arbitrary Hermitian weighted-Hoffman closure

The 45-anchor graph is `SRG(45,32,22,24)`. Its ordinary Hoffman bound gives independence number at most five, and the 27 five-point lines attain five.  Each point belongs to three lines, hence these lines weighted by `1/3` give fractional chromatic number nine.

The ordinary weighted matrix `A45 tensor I4` attains ratio nine.  The generalized weighted-Hoffman optimum over arbitrary edge-supported Hermitian matrices is bounded by the vector chromatic number; conversely ordinary Hoffman bounds the vector chromatic number from below.  Thus

`chi_v = chi_f = 9`

and the arbitrary signed real or complex-Hermitian generalized Hoffman optimum is exactly nine.  This uses the weighted-adjacency framework of Wocjan–Janzing–Beth (`arXiv:cs/0112023`) and the vector-chromatic characterization discussed by Wocjan–Elphick–Anekstein (`arXiv:1812.02613`).

This closes the spectral-weight family, not the actual colouring problem: `10 <= chi(H) <= 11` remains live.

## 3. Complete rank-four tomotope census

The edge–face layer admits twelve vertex assignments after fixing the first edge label.  They split into three vertex-structure orbits.  Pairing those three structures with the three corrected eight-cell covers gives a 3×3 completion square.

All nine structures have

`f = (4,12,16,8)`, 192 flags, every diamond interval of size two, and a connected flag graph.

The automorphism-order matrix is

```
96   96  192
192  96   96
96  192   96
```

Six entries have automorphism order 96, order census `1^1 2^27 3^32 4^36`, and two flag orbits of size 96.  These are tomotope completions.

The three matched entries have automorphism order 192, order census `1^1 2^43 3^32 4^84 6^32`, and one flag orbit of size 192.  They realize the non-split central lift already isolated in Passes 3670–3686.

## 4. The 159-module filtration

The characteristic-three complement has filtration

`159 > 44 > 14 > 0`,

with successive dimensions `115 | 30 | 14`.

The bottom 14-space generates the full algebra `M14(F3)`, so it is absolutely irreducible.

The middle 30-space contains a direct semisimple socle of dimensions `1+5+10`; the generated matrix algebras have dimensions `1,25,100`.  Its 14-dimensional head generates `M14(F3)`.  The full 30-module has scalar endomorphism ring, so the extension is non-split:

`0 -> 1+5+10 -> M30 -> 14 -> 0`.

The top 115-quotient has a two-dimensional fixed socle and one trivial head.  Its remaining composition factors are deliberately left unlabeled.

## 5. Gewirtz rounding no-go

The weighted W33–Clebsch bridge has order 56, entry alphabet

`{-13,-6,8,15,50,71}`

and spectrum

`560^1 112^35 (-224)^20`.

The complete full-orbit binary rounding family has five binary choices: W33 adjacency, W33 nonadjacency, cross block, Clebsch adjacency, and Clebsch distance-two relation.  All `2^5=32` choices were exhausted.

None is 10-regular and none satisfies

`A^2 = 8I - 2A + 2J`,

the `SRG(56,10,0,2)` identity.  In particular, any rounding retaining induced W33 is impossible because W33 already has internal degree 12.

This closes fully equivariant orbitwise rounding.  Asymmetric switching and non-equivariant rounding remain open.

## BONKERS 1 — the tomotope completion square

The three vertex structures and three cell covers form a 3×3 binary geometry: six entries are the two-orbit order-96 tomotope, while a perfect matching of three entries lifts to a regular order-192 central extension.  The exceptional pattern is literally a permutation matrix.

## BONKERS 2 — a free 62-cap torsor

The explicit cubic 62-cap has trivial stabilizer in `U4(2)` and therefore a free orbit of size 25,920.  This produces 25,920 distinct cap witnesses.  The cap is not claimed maximum.

## Frozen certificate

Semantic SHA-256:

`c6e5e73fb5a18d9add4c1643d52df31413280b0e5cd157294ca686f8df32a299`

## Evidence firewall

No exact cubic-transversal endpoint, ten-colour decision, unresolved top-115 composition label, asymmetric Gewirtz rounding, remote CI/PDF result, hardware result, laboratory result, or physical interpretation is asserted without executed evidence.
