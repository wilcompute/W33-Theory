# Pass 4969 — outer extension on the W33 point module

**Date:** 2026-08-12  
**Status:** SUPERSEDED/HARDENED by Pass4985.

For the W33 adjacency matrix

`Spec(A) = {12^1, 2^24, (-4)^15}`.

The 40-point real permutation module therefore splits as `1 + 24 + 15`.

## Exact correction

Every graph automorphism `P` satisfies `PA=AP`. Consequently it preserves each eigenspace belonging to a distinct adjacency eigenvalue. In particular, an outer graph automorphism **cannot interchange the 24- and 15-dimensional eigenspaces**. The earlier wording claiming that the outer involution interchanged them is false.

Pass4966 gives an explicit multiplier-minus-one similitude extending the PSp action from order 25,920 to a PGSp action of order 51,840. It acts *within* the 24- and 15-dimensional packets while reversing the oriented Witting/Pancharatnam phase character.

## Physics boundary

The finite quotient character `PGSp/PSp ~= C2` is an exact group-theoretic sign. It is **not automatically spacetime CPT, CP, or parity**. The previous sentence equating the outer involution with CPT is withdrawn.

The numerical identities `24=2k` and `24-15=9=q^2` remain arithmetic observations; any particle-physics interpretation requires an independent representation/mechanism.

Cross-references: `data/PART_W33_PASS4966_WITTING_PHASE_OUTER_CHARACTER.json`, `data/PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json`.
