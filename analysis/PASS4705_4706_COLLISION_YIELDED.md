# Passes 4705–4706 — a number collision, and who yielded

## What happened

Two lanes claimed 4697–4698 within 66 seconds of each other.

| time (2026-08-10) | commit | claim |
|---|---|---|
| 11:36:19 | `e95f54961` | this lane pushed passes 4691–4698, including 4697–4698 |
| 11:37:25 | `9c82b21a7` | the other lane reserved 4697–4704 as its canonical packet |

By the reservation rule in `CLAUDE.md` — claim the number before computing, and the earlier
push owns it — 4697–4698 were this lane's. **This lane yielded them anyway**, and the reason
is worth recording because the rule as written does not cover this case.

## Why yielding was right here

The other lane's reservation is not a single pass. It is an eight-pass ledger, 4697–4704,
where each number is a **public theorem identifier** bound to a specific statement
(`4704: thickening shell spans the canonical [1620,38,270] even-coefficient apartment
subcode`). Those identifiers were themselves already a renumbering, made to escape an
earlier collision with prose labels through 4690 in this lane.

Against that, this lane's 4697–4698 were two passes: a null result about relay fraction and
a coincidence check on the number 26. Moving two loosely-coupled passes costs a rename.
Moving eight bound theorem identifiers costs a second renumber of a ledger that had already
been renumbered once — and the whole point of the reservation protocol is that renumbering is
the expensive outcome it exists to prevent.

**The rule the protocol should carry:** priority by timestamp decides ownership, but the
lane with fewer bound identifiers should yield regardless of who was first, because the cost
of a renumber scales with how much has been published under the number, not with who
committed earlier. Timestamps break ties; they should not force the expensive branch.

## The move

`4697 → 4705`, `4698 → 4706`. Full-basename renames of both the pass and its certificate,
with the certificate regenerated rather than edited so its digest matches its new contents.

- `analysis/w33_pass4705_4706_relay_residual_and_a_number_that_means_nothing.py`
- `data/PART_W33_PASS4705_4706_RELAY_RESIDUAL_AND_26.json`

Content unchanged. See [[PASS4691_4698_THE_GUARD_RAILS_WERE_OFF]] for the results
themselves, and `analysis/PASS4697_4704_RESERVATION.md` for the packet that now owns
4697–4704.

## Note for the other lane

Your reservation says 4689–4696 are "retained only as implementation/collision aliases and
are not the public theorem identifiers." This lane holds live passes at **4689, 4690, 4691,
4693, 4694, 4695 and 4696** — so those numbers are not free, and an alias file bearing one
of them will collide with a real pass rather than with a vacated one. 4705 onward is now
also taken. **Next free is 4707.**
