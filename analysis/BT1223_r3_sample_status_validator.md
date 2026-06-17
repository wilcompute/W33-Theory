# BT1223 -- R3 Sample Status Validator

## Purpose

BT1220 showed that the R3 pipeline can carry schema-shaped refinement sequences without treating test data as physical evidence. BT1223 makes that rule executable.

## Status levels

The validator uses three levels:

- `blocked`: sample contains test labels, placeholder labels, missing fields, or noncomputed fields;
- `partial`: sample is schema-valid with some computed data but is still not enough for evidence status;
- `candidate`: sample has all required metric, operator, heat, and refinement fields and has no blocking labels.

## Result on BT1220

The BT1220 sequence has four refinement samples with

\[
n=8,16,32,64.
\]

All four are classified as `blocked` because their metric and operator fields are test-labeled and the claim status prevents evidence promotion.

## Candidate rule

A sample can become a candidate only if it has:

- no blocking labels in metric, operator, or status fields;
- nonempty operator data;
- non-null refinement scale \(h\);
- non-null \(A_4\);
- non-blocking claim status.

## Files

- Code: `analysis/bt1223_r3_sample_status_validator.py`
- Result: `data/bt1223_r3_sample_status_validator_summary.json`

## Boundary

BT1223 does not create physical R3 evidence. It prevents premature promotion and gives the repo a clean path from test data to partial data to future candidate data.
