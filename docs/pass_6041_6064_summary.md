# Pass 6041–6064 Summary — CORRECTED BY PASS6137–6144

The historical packet claimed full CE2 anchor-23 orbit closure. That claim is
withdrawn.

## What survives

Five anchor-23 seed rows remain available as historical input data in
`scripts/w33_ce2_anchor23_full_orbit.py`.

## Why closure was not established

The historical producer did not construct the W(3,3) automorphism action, did
not enumerate orbit rows, and did not evaluate a CE2 object on that orbit. It
classified the five seed rows by coefficient family and then declared family
counts

- transport_line = 24,
- overlap_phase = 12,
- transport_gauge = 6,
- diagonal_source = 6,
- reflected_transport = 0,

without producing those rows.

Therefore the corrected status is:

**Anchor 23: OPEN beyond five seed rows.**

Canonical correction:

- `analysis/PASS6137_6144_ce2_k3_evidence_repair.md`
- `data/PART_W33_PASS6137_6144_CE2_K3_EVIDENCE_REPAIR.json`

The historical version remains recoverable at commit
`85a72c8a8974a3491187d033a66211e8f20ad93c`.
