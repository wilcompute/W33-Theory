# CE2 / K3 provenance map (Pass5995-6000)

File-level provenance established 2026-08-17. Contents not yet extracted; this
map is the index for the next session's extraction work.

## CE2 genuine evaluator (February L-infinity machinery)

Source commit: `c90fddd4` (2026-02-13, "linfty: add CE2 (l4) prototype, fix
homotopy_jacobi & local CE2 solver").

- `tools/compute_restricted_ce_h3.py` (280 lines) — the restricted CE/H3 evaluator
- `tools/exhaustive_homotopy_check_rationalized_l3.py` (364 lines)
- `tools/build_linfty_firewall_extension.py`
- `tools/compute_S_relation.py`
- `THE_EXACT_MAP.py` (repo root)
- `tests/test_exact_map_line_rep.py`

The genuine anchor-22/23 seed rows must originate here. Next step: read
`compute_restricted_ce_h3.py`, extract the actual evaluator, recompute the
anchor orbits from object data rather than canned counts.

## CE2 false-closure repairs (today)

- `scripts/w33_ce2_global_closure_verify.py` — the false verifier, replaced with
  a fail-closed evidence ledger in commit `69bf9de6`
- Orbit files on master: `w33_ce2_anchor22` (corrected in `fa8885e4`),
  `w33_ce2_anchor24_orbit.py`, `w33_ce2_anchor25_orbit.py`,
  `w33_ce2_anchor26_31_batch.py`, `w33_ce2_anchor32_39_final.py`

## K3 matrix provenance — absence confirmed

- The witness-scan producer: `scripts/w33_k3_curvature_witness_scan.py`
  (62 lines, added in commit `49801227`)
- Code search for `2428` on master: **zero hits**. No frozen 2428x36 matrix
  artifact exists anywhere in the repo.
- Conclusion: the scan's matrix was an ambient allocation, not a loaded object.
  A real K3 witness scan is blocked until a genuine curvature/cochain matrix is
  constructed from the tools/ L-infinity machinery and frozen as a data artifact
  with an explicit coordinate map.

## Status

- CE2 global orbit closure: **OPEN** (evaluator located, extraction pending)
- K3 real-object witness scan: **NOT YET RUN** (no frozen matrix exists to scan)
