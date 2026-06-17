# BT1278 -- External Protocol CI Integration

## Purpose

BT1278 wires the BT1276 external-candidate protocol paper section into CI through a safe companion integrator.

## New helper

```text
tools/integrate_bt1276_external_protocol_insert.py
```

The helper materializes:

```text
analysis/BT1276_external_candidate_protocol_paper_section.tex
  -> paper/sections/sec_bt1276_external_candidate_protocol.tex
```

and idempotently inserts the BT1276 paper section line into the preprint.

## CI update

The paper-materialization step now runs:

```text
python tools/integrate_bt1236_insert.py
python tools/integrate_bt1261_ladder_insert.py
python tools/integrate_bt1267_score_vector_insert.py
python tools/integrate_bt1276_external_protocol_insert.py
python analysis/bt1239_bt1236_integration_sanity.py
```

## Boundary

This follows the safe companion-integrator route already used for BT1261 and BT1267.
