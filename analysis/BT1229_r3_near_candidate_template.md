# BT1229 -- R3 Near-Candidate Template

## Purpose

BT1226 created the partial lane. BT1229 creates a near-green template: all numerical fields are present, but independent certification is absent.

## Sample

The sample is

```text
k3_near_candidate_n64_template_v1
```

with

\[
h=0.015625,
\qquad
\text{shape quality}=0.996875.
\]

It includes nonempty operator data, non-null heat coefficients, and non-null curvature error.

## Failure mode

Candidate promotion is blocked because the independent metric and operator certifications are both false.

So the sample is numerically complete but not evidence-complete.

## Why this matters

This closes the near-green loophole. A future R3 sample cannot be promoted just because all numerical fields are filled. It also needs independent provenance and certification.

## Files

- Code: `analysis/bt1229_r3_near_candidate_template.py`
- Result: `data/bt1229_r3_near_candidate_template_summary.json`

## Boundary

BT1229 is not a physical R3 sample. It is a guardrail template for samples that look complete but still lack certification.
