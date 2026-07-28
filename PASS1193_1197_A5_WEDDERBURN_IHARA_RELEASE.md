# Passes 1193–1197 — A5, Wedderburn, Ihara, and CI Release

## Pass 1193 — Exact A5 intersection bridge

For each 432-point A2-triple orbit, the stabilizer in `W(E6)` is `S5` of order 120. The even-reflection-word kernel has order 25920 and is identified with `PSp(4,3)`. Their intersection has order 60 and element-order distribution

`1^1 2^15 3^20 5^24`,

hence it is `A5`. Therefore the inclusion induces a bijection

`PSp(4,3)/A5 -> W(E6)/S5`,

and both coset spaces have degree 432.

## Pass 1194 — Residual Wedderburn idempotents

The exact residual decomposition is realized in a canonical abstract isotypic basis. It has ten central idempotents, 85 primitive copy idempotents, and 1109 matrix units. The commutant tower is

`1109 -> 1118 -> 1193`

for residual 1952, kernel 2195, and carrier 2240 respectively. The coordinate transport into the original 2240 A2-triple basis remains a separate character-sum/intertwiner problem.

## Pass 1195 — Primitive Ihara census through degree 40

Using the exact Hashimoto factorization

`(x-1)^200 (x+1)^200 product_lambda (x^2-lambda*x+11)^m_lambda`,

all primitive reduced-cycle counts through degree 40 are computed by integer recurrences and Möbius inversion. The short checks are 160 triangles and 1740 unoriented primitive 4-cycles.

## Pass 1196 — Equivariant short-cycle classification

The projective symplectic transvections generate `PSp(4,3)` of order 25920 on the 40 W33 points. Primitive triangles form one orbit of size 160. Primitive 4-cycles split into exactly two orbits:

- 120 line-internal `K4` cycles;
- 1620 generalized-quadrangle apartments.

The honest graph action is `PSp(4,3)`. `W(E6)` is not silently promoted to a second faithful 40-point graph action; a Weyl-equivariant cycle theory requires an explicitly defined phase-lifted carrier.

## Pass 1197 — Mandatory namespace and exact-claim guard

The namespace registry now marks 1188–1192 and 1193–1197 complete. A pull-request/push workflow and pre-commit hook enforce non-overlapping pass reservations, required exact artifacts, result status, corrected Ihara coefficient 11, and the repaired group-extension boundaries.
