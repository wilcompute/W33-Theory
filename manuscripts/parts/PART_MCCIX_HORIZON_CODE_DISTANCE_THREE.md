# Part MCCIX: Horizon Code Distance-Three Law

## Claim Boundary

MCCIX establishes a finite upper-bound law for the ternary horizon packet
`[72,66,*]_3`. It does not claim a completed lower-bound kernel proof.

## Statement

For `q=3`, `n=72`, `k=66`, redundancy is `n-k=6`, so `q^{n-k}=3^6=729`.

Hamming sphere-packing for `d=5` (`t=2`) gives:

```text
V2 = 1 + n(q-1) + C(n,2)(q-1)^2
   = 1 + 72*2 + C(72,2)*4
   = 10369 > 729,
```

so `d=5` is impossible.

An explicit triangle-boundary witness model gives a weight-3 nonzero word,
hence `d <= 3`.

Therefore:

```text
d <= 3.
```

## Honest Boundary

The explicit full-kernel proof of `d >= 3` remains open; current status is the
transparent boundary statement from C341 with conjecture `d=q=3` retained.

## Artifacts

- Analysis: `analysis/w33_horizon_code_distance_three.py`
- Tests: `tests/test_w33_horizon_code_distance_three.py`
- Result: `PART_MCCIX_HORIZON_CODE_DISTANCE_THREE_results.json`
