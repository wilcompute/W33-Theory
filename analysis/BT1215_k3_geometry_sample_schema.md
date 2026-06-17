# BT1215 -- K3 Geometry Compute-Lane Schema

## Purpose

BT1213 grounded the R3 refinement bridge in the existing BT1127 K3 envelope. BT1215 defines the next compute-lane contract: what a future non-placeholder K3 sample must contain before it can count as R3 evidence.

## Required topology

The schema locks the known K3 invariants:

\[
\chi=24,
\qquad
\sigma=-16,
\qquad
b_2=22,
\qquad
(b_2^+,b_2^-)=(3,19).
\]

## Required blocks

A future sample must contain:

1. `metric_block` -- metric source, volume normalization, and shape quality;
2. `operator_block` -- operator convention, eigenvalue sample, and status;
3. `heat_block` -- coefficients \(A_0,A_2,A_4\);
4. `curvature_block` -- normalized \(|Rm|^2\) target and error;
5. `refinement_block` -- refinement scale \(h\), index, and previous sample link.

## Current status

The pushed artifact is intentionally a schema stub:

```text
claim_status = schema_stub_only
```

It is valid as an interface contract but not as physical R3 evidence.

## Files

- Code: `analysis/bt1215_k3_geometry_sample_schema.py`
- Result: `data/bt1215_k3_geometry_sample_stub_summary.json`

## Boundary

This does not compute a K3 metric. It defines the exact shape of the future computation. A sample graduates only when the placeholder fields are replaced by actual metric/operator/heat/curvature/refinement data.
