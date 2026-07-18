# Release milestones — criteria, not momentum

*Releases fire when gates close, not when a round feels productive. Gates may
be overtaken by results (one already was); when that happens, replace the gate
and say so.*

## v1.0-selection-layer-closed — shipped

The selection layer closed in the negative (chirality no-go, torsor theorem,
attributions corrected); self-verifying claims ledger; failure taxonomy.

## v1.1-cover-law-and-audit — shipped

The cover law proved for all odd q; sections classified (= characters);
nesting tower law; PDS certified; third stream's Pass 399 audited GOOD;
executable batch intake; both papers compile.

## v1.2 — ONE GATE OPEN

1. **Polhill full-table check — OPEN.** Read the tables of arXiv:2306.00140
   (not just the abstract) and record whether `(27,10,1,5)` — or the tower
   family — appears. Either outcome closes the novelty question of
   `papers/heisenberg_pds_note.tex`.
2. **The 2-part tower question — CLOSED by Pass 434.** Exact unit-pivot Smith
   elimination gives

   \[
   K_{7,(2)}\cong(\mathbb Z/2)^{42}\oplus(\mathbb Z/16)^{126}.
   \]

   Independent `GF(9)` and prime `q=11` certificates also match the same
   spectral-pairing law, while the `Z/9Z` control fails it. The general
   odd-prime-power formula remains conjectural, but the release gate was the
   q=7 decision and is now closed.
3. **Batch 415–429 resolved — CLOSED.** Commit `2b83623f866c22df42232630248792be3e2a7309`
   merged the complete fifteen-frontier release, all three regression suites,
   schema validation, exact batch audit, permanent workflow, and green claims
   ledger. Commit `822739b1224418b76159dc38b6857600d75aff97`
   subsequently merged the portable certificate hardening.

## Deferred beyond v1.2 (named, not gating)

- Integral proof of the Pass 434 2-adic Smith pairing law for every odd prime
  power.
- m=6 Coxeter–Todd rung of the QR tower (GAP; handoff `data/m6_handoff_k12.json`).
- exp-3/exp-9 vs ordinary/twisted Frobenius–Schur correspondence.
- q=25/27 Smith middle layers (third stream's queue).
- Papers-build CI step (waiting on the other stream's workflow staging).
