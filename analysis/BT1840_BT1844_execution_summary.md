# BT1840-BT1844 Execution Summary

## BT1840

Repo search found `analysis/bt956_tetracode_metric_selector_matrix.py`, which stores the recovered BT930 chain-to-tetracode matrix. The tetracode metric independently selects minimizer 2, agreeing with BT954's vertex metric. The remaining open problem is no longer matrix recovery; it is the full tetracode stabilizer/group-action quotient.

## BT1841

Added the generated artifact pack manifest for the BT1835-BT1840 runtime/E8 selector continuation. It lists the generator commands and expected output JSON artifacts.

## BT1842

Added the E8-labelled compiled trace schema. A materialized relocation row should carry the base walk fields, the BT1823 `compiled_phase`, and the BT954/BT956 metric-winner-2 selector pair.

## BT1843

Added the aperture-to-shot protocol. The protocol has 1440 settings, 100 nominal shots per setting, four detector channels balanced at 360 rows each, and blank observed columns until data exists.

## BT1844

Added theorem-ledger promotion rows for BT1835-BT1843. The promotion rule is precise: BT956 recovers the matrix and agrees on winner 2, but the full tetracode quotient is not closed until the explicit action is computed.

## Honest boundary

No full CI or physical run was executed in this connector pass. Generated CSV/JSON/JSONL payloads are produced by the committed generators/manifests in the repo environment.
