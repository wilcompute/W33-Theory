# Release milestones — criteria, not momentum

*Releases fire when gates close, not when a round feels productive. Gates may
be overtaken by results; when that happens, replace or close the gate and say
so.*

## v1.0-selection-layer-closed — shipped

The selection layer closed in the negative (chirality no-go, torsor theorem,
attributions corrected); self-verifying claims ledger; failure taxonomy.

## v1.1-cover-law-and-audit — shipped

The cover law proved for all odd q; sections classified (= characters);
nesting tower law; PDS certified; third stream's Pass 399 audited GOOD;
executable batch intake; both papers compile.

## v1.2 — OPEN. Remaining gates:

1. **Polhill full-table check.** Read the tables of arXiv:2306.00140 (not just
   the abstract) and record whether `(27,10,1,5)` — or the tower family —
   appears. Either outcome closes the novelty question of
   `papers/heisenberg_pds_note.tex`.
2. **The 2-part tower question.** The q=7 2-adic sandpile shape (343×343,
   unit-pivot elimination mod `2^k`) decides whether the 2-layer profile follows
   a tower law. This gate replaced "the tower nonabelian theorem", which closed
   during Pass 433 by the two-line character argument for every odd q.

### Closed during the v1.2 cycle

- [x] **Batch 415–429 resolved.** PRs #120 and #125 merged the readable
      scientific tree; PR #126 hardened cross-runner certificate portability.
      All fifteen witnesses, all three regression suites, schema validation,
      exact batch audit, and claims ledger passed. See
      `BATCH_415_429_INTAKE_FINDINGS.md`.
- [x] **q=25/q=27 characteristic Smith middle layers.** Pass 425 closed the
      formerly deferred characteristic-primary layers. Prime-to-characteristic
      extension-field components remain a separate problem.

## Deferred beyond v1.2 (named, not gating)

- m=6 Coxeter–Todd rung of the QR tower (GAP; handoff
  `data/m6_handoff_k12.json`).
- exp-3/exp-9 vs ordinary/twisted Frobenius–Schur correspondence.
- Prime-to-characteristic critical-group components for odd prime powers.
- Papers-build CI step (waiting on the other stream's workflow staging).
