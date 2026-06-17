# BT1232 -- Unified R3 Evidence Gate

## Purpose

BT1215 defined the K3 geometry sample schema. BT1227 exercised blocked and partial samples. BT1229 added the near-candidate boundary: numerical fields can be present while independent certification is still absent.

BT1232 merges those lanes into one fail-closed gate.

## Lanes

The gate recognizes five mutually exclusive lanes:

1. `schema_stub`
2. `blocked`
3. `partial`
4. `near_candidate`
5. `candidate`

## Promotion rule

A sample is promoted to `candidate` only if:

\[
\boxed{\text{all numerical fields are present}}
\]

and

\[
\boxed{\text{independent metric certification}=\texttt{true}}
\]

and

\[
\boxed{\text{independent operator certification}=\texttt{true}.}
\]

Thus BT1229-style near-candidates are explicitly blocked from evidence status.

## Demo result

The pushed demo fixture has one sample in each lane:

\[
\boxed{1,1,1,1,1}
\]

for

\[
\text{schema-stub},\text{ blocked},\text{ partial},\text{ near-candidate},\text{ candidate}.
\]

The near-candidate is not promoted, while the certified candidate is promoted.

## Boundary

This is an evidence gate and validator. It does not compute a K3 metric. It prevents future K3/R3 artifacts from being promoted unless the independent certification fields are explicitly true.

## Files

- Code: `analysis/bt1232_r3_evidence_gate.py`
- Result: `data/bt1232_r3_gate_summary.json`
