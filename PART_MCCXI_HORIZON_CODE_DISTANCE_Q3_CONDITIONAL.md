# Part MCCXI: Conditional Horizon Code Distance q=3 Law

## Claim Boundary

MCCXI separates constructive facts from embedding-level assumptions.

## Constructive layer (explicit)

- The explicit full F3 horizon parity matrix has rank `6` and no zero columns.
- MCCIX already gives the upper-bound packet `d <= 3`.
- Triangle witness model gives weight `3` support.

So the constructive side locks:

```text
d <= 3.
```

## Conditional exactness (C346c)

Under the declared embedding hypotheses:

1. minimal symmetric K12 embedding;
2. no proportional edge columns under that embedding,

the model excludes weight-1/2 nonzero codewords while retaining a weight-3
construction, giving:

```text
d = 3 = q.
```

## Honest boundary

The exact equality is conditional; a fully constructive lower-bound certificate
(`d >= 3`) independent of embedding hypotheses remains open.

## Artifacts

- Analysis: `analysis/w33_horizon_code_distance_q3_conditional.py`
- Tests: `tests/test_w33_horizon_code_distance_q3_conditional.py`
- Result: `PART_MCCXI_HORIZON_CODE_DISTANCE_Q3_CONDITIONAL_results.json`
