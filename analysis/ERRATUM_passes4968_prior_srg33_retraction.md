# ERRATUM — srg(33) retraction and Pass4985 cascade audit

**Date:** 2026-08-12  
**Severity:** MAJOR  
**Status:** FORMALLY RETRACTED / HARDENED

The prior `srg(33,8,2,2)` W33 story remains retracted. `W33` means `W(3,3)` and its point graph is
` srg(40,12,2,4)` with spectrum `12^1,2^24,(-4)^15`.

Pass4985 found additional errors in the first "corrected" Pass4968--4972 packet and supersedes them:

- PSp(4,3), order 25,920, is the symplectic index-two subgroup; Pass4966 already exhibits a multiplier-minus-one similitude giving a 51,840-element PGSp extension.
- The 27 nonneighbors of a W33 point were incorrectly identified with 27 PG(3,3) lines; that identification is withdrawn.
- A graph automorphism commutes with adjacency, so it cannot interchange the distinct 24- and 15-dimensional eigenspaces. The old CPT identification is also withdrawn.
- The Ihara roots are `(1 +- i sqrt(10))/11` and `(-2 +- i sqrt(7))/11`; the previous sqrt(43)/sqrt(107) fields and their class-number interpretation were arithmetic errors.
- The exact W33 critical group is `(Z/10)^8 (+) Z/40 (+) (Z/160)^14`, as already frozen by Pass88. Its order `2^81*5^23` survives; the old ad-hoc invariant-factor/hypercharge paragraph does not.

What remains valid from the collision repair: 40 vertices, SRG parameters `(40,12,2,4)`, spectrum `12,2,-4`, Ramanujan inequality, the retraction of the Fano-deletion/srg33 tower, and the 240-edge count.

Canonical audit certificate: `data/PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json`.
