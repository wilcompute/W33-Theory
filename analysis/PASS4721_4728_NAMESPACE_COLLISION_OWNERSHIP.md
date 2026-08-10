# Pass 4721–4728 namespace collision record

This file records a live namespace collision so the theorem ledger remains auditable.

## First reservation

The support-12 continuation reserved Passes 4721–4728 on `master` in:

- commit `354ba5cac1bac0ceb00cd6729e0dabb85487930d`
- commit timestamp `2026-08-10T15:55:32Z`
- file `analysis/PASS4721_4728_RESERVATION.md`

The executed results currently occupying that namespace are the support-12 involution/square-root-cover and H10-dual-code theorems.

## Later colliding reservation/use

A separate Track-A lane later reserved and then used the same range:

- reservation commit `bc70d9057e41db5844d6223384710e9f3e27a7d8`
- reservation timestamp `2026-08-10T16:06:38Z`
- execution commit `e4a82c9108ef00d1c3d129cc6aea5032bf3bc60f`
- execution timestamp `2026-08-10T16:22:15Z`

Thus the second reservation occurred **11 minutes 6 seconds after** the first reservation.

## Ownership rule

Recent repository collision handling explicitly uses first reservation time to decide ownership. For example, commit `d83ce58c5762ec370ea7755b15dbfe9bdd5be318` states that a lane that reserved 93 seconds later yielded and renumbered, and notes that the timestamp rule is the governing convention.

Accordingly, under the repository's own convention:

\[
\boxed{\text{Passes 4721--4728 belong to the reservation at }354ba5c\ldots}
\]

The later Track-A packet should be renumbered; the earlier support-12 lane is not renumbered here.

## Boundary

This is a namespace/provenance record, not a mathematical theorem. It exists so searches, manuscript inserts, certificates, and future agents do not silently conflate two unrelated pass families while the later packet awaits renumbering.
