# Part DCCXII — Klitzing Partial-Sheet Operation Commutation

This part adds the missing symmetric operation ladder for Klitzing's tomotope partial sheets.

## What was already exact

From the promoted bridge data:

- seed sheet law: `partial_a = 2 * partial_b`, with packets
  - `partial_a = (8,24,32,8,8)`
  - `partial_b = (4,12,16,4,4)`
- direct operation ladder on `mod_b`:
  - `12 -> 24 -> 48 -> 96` for
    `rectified -> truncated -> maximal expanded -> omnitruncated`

## New explicit lift

The module `w33_tomotope_klitzing_partial_operation_commutation.py` adds the unique sheet-lifted operation ladder:

- `partial_a`: `24 -> 48 -> 96 -> 192`

and verifies stagewise commutation of:

- `S(x)=2x` (sheet map),
- `O(x)=2x` (next operation step in this ladder),

so `S∘O = O∘S` at every stage.

## Scope guardrail

This repository currently encodes direct row strings for `mod_b` operations. The `partial_a` operation ladder here is marked as inferred from the exact seed sheet law plus the direct `mod_b` ladder, not from separately transcribed `mod_a` operation rows.

## Artifact

- Script: `exploration/w33_tomotope_klitzing_partial_operation_commutation.py`
- Test: `tests/test_w33_tomotope_klitzing_partial_operation_commutation.py`
- Output: `data/w33_tomotope_klitzing_partial_operation_commutation_summary.json`
