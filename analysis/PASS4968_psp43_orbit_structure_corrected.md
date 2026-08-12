# Pass 4968 — PSp(4,3) orbit structure on 40 vertices

**Date:** 2026-08-12  
**Status:** SUPERSEDED/HARDENED by Pass4985 after the original srg(33) correction.

The valid finite statement is:

- `W(3,3) = srg(40,12,2,4)` on 40 projective points of `F_3^4`.
- The symplectic subgroup `PSp(4,3)` has order 25,920 and is transitive on the 40 points and 240 graph edges.
- A point stabilizer inside this subgroup has order `25920/40 = 648`.
- Its two graph-distance shells have sizes 12 neighbors and 27 nonneighbors.
- Pass4966 exhibits an explicit multiplier-minus-one similitude that doubles this action to a 51,840-element `PGSp(4,3)` extension.

Two claims from the earlier version are withdrawn by Pass4985:

1. `PSp(4,3)` should not have been presented as the entire index-two-extended symmetry; the explicit PGSp extension is already present in the repo.
2. The 27 nonneighbors of a fixed W33 point are simply 27 points of the same 40-point carrier. The asserted identification with "the 27 lines of PG(3,3) not through the fixed point" was unsupported and is withdrawn.

No physical braid/TQC interpretation follows merely from the numerical stabilizer order 648.

Cross-references: `data/PART_W33_PASS4966_WITTING_PHASE_OUTER_CHARACTER.json`, `data/PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json`.
