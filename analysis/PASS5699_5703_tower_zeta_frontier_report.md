# Pass5699-5703 frontier report: the W33 Ramanujan tower is an Artin L-function tower

## What is new (not in either lane's recent packets)

1. **Levelwise zeta factorization (Pass5699).** For every balanced 2-lift in the explicit
   tower, spec(child) = spec(parent) u spec(signed parent) to machine precision, so by Bass
   the Ihara zeta factors as zeta_child = zeta_parent * L(u, chi) with
   L(u, chi)^-1 = (1-u^2)^(r-1) det(I - u A_signed + 3u^2 I).  This is the Stark--Terras
   Artin L-function of the Z/2 local system defined by the signing.  The signing is the same
   datum as the Pass5696 determinant-line twist, so the tower L-functions ARE the
   orientation-twisted sector partition functions.

2. **Base closed form.**  Delta_levi(u) = (1-u^2)(1-9u^2)(1+9u^4)^24 (1+3u^2)^30, verified
   against the Bass determinant.  The 24-dimensional +-sqrt(6) eigenspace collapses to the
   quartic factor (1+9u^4)^24 whose roots lie at 45-degree angles on the critical circle.

3. **Tower RH, exact (Pass5701).**  All signed-spectrum L-function poles lie on
   |u| = 1/sqrt(3) (160/160, 320/320, 640/640).  Upgraded from numerics to theorem by exact
   rational LDL certificates that 12I - A_s^2 is positive definite at levels 1-3 (min pivots
   4.82, 4.49, 4.52 as exact Fractions), plus a 60-digit Cholesky certificate for the
   320->640 signing (min pivot 4.52377).  The Sturm 77/80 anomaly is resolved: the zero
   eigenvalue has multiplicity 4 and Sturm counts distinct roots.

4. **Girth-cycle group identity (Pass5700).**  Exact integer arithmetic:
   Tr(A_levi^8) = 193280 = 80*2092 + 25920 = n*M8_tree + |PSp(4,3)|.  The tower excess
   SHRINKS under lifting (25920 -> 25600 -> 25216 -> 24928) while girth stays pinned at 8.
   The 25920 rooted oriented 8-cycles split into TWO PSp(4,3) orbits of 12960 with Z/2
   stabilizers, separated by a symplectic chirality invariant (diagonal common-neighbour
   count 4 vs 0).  The stabilizer involution has cycle structure 1^8 2^16 on the 40 points.

5. **Kesten--McKay equidistribution (Pass5702).**  The new (signed) spectra converge to the
   4-regular tree law with KS distance 0.02102 -> 0.01079 -> 0.00540, an empirical
   2^{-level} law.  Moments match the tree exactly through M6 (girth-forced).  Eigenphase
   spacings sit near GOE, not Poisson.

6. **alpha(W(3,9)) replication (Pass5703).**  Independent construction over F_9 (820
   vertices, 90-regular); greedy+swap plateaus at 46, honestly replicating the barrier below
   the repo's 51 <= alpha <= 80.  Staged GAP TransitiveIdentification script for the Track A
   q=5 settling test included (analysis/PASS5703_Q5_TRANSITIVE_IDENTIFICATION.g).

## Evidence boundary

All statements are finite graph, matrix, zeta-function, or group-action facts verified by
exact integer/rational arithmetic or high-precision numerics with explicit error bounds.
No continuum limit, no physical energy spectrum, no Yang--Mills mass gap, and no all-level
equidistribution theorem is claimed.  The 2^{-level} KS law and the excess-shrinkage trend
are empirical on 3-4 levels.

## Open threads handed forward

- Orbit merger under the full W(E6) duality (Pass5700 open_merger).
- Level-4 (1280-vertex) exact certificate and whether the KS law persists.
- Quantum-graph resonance budget for the photonic paper from the signed eigenphases.
- Weighted/matching-signed independence search on W(3,9) against the 51-barrier.
- Running the staged GAP settling test in the repo's GAP environment.
