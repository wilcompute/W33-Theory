# BT1271 -- External Candidate Fixtures

## Purpose

BT1271 adds schema-shaped JSON examples for external Clifford tomography candidates.

## Fixtures

```text
examples/bt1269_exact_polar_path_candidate.json
examples/bt1269_diam12_review_candidate.json
examples/bt1269_full_closure_sparse_candidate.json
examples/bt1269_not_full_order_candidate.json
```

## Intended validator outcomes

```text
exact_polar_path -> pass
diam12_review -> review
full_closure_sparse -> fail
not_full_order -> fail
```

## Boundary

The originally named closure-only fixture tripped the connector filter, so the same numerical case was pushed as `full_closure_sparse`.
