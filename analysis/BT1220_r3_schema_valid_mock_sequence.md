# BT1220 -- R3 Schema-Valid Mock Refinement Sequence

## Purpose

BT1215 defined the K3 geometry sample schema. BT1220 creates the first sequence of samples shaped like that schema with non-null refinement data.

The point is not to fake R3. The point is to exercise the pipeline while refusing promotion until real metric/operator data exist.

## Sequence

The refinement indices are

\[
n=8,16,32,64,
\qquad h=1/n.
\]

Each sample includes:

- K3 topology \(\chi=24,\sigma=-16,b_2=22,(b_2^+,b_2^-)=(3,19)\),
- non-null refinement \(h\),
- improving shape quality,
- mock eigenvalue arrays,
- mock heat coefficients,
- decreasing curvature error.

## Monotone witnesses

The sequence passes:

\[
h\downarrow,
\qquad
\text{shape quality}\uparrow,
\qquad
A_2^{\rm mock}\downarrow0,
\]

\[
A_4^{\rm mock}\downarrow24,
\qquad
\epsilon_{\rm curv}\downarrow0.
\]

## Promotion refusal

Despite passing schema and monotone checks, the sequence has

```text
claim_status = mock_sequence_only
```

and promotion is explicitly blocked because the metric and operator blocks are mock-labeled.

## Files

- Code: `analysis/bt1220_r3_schema_valid_mock_sequence.py`
- Result: `data/bt1220_r3_schema_valid_mock_sequence_summary.json`

## Boundary

BT1220 is not R3 evidence. It is a pipeline exercise and guardrail: it proves the repository can carry refinement samples without confusing mock samples for physical samples.
