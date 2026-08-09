# Part MCLXXXIV: Q4-Tomotope Index Staircase Law

## Claim Boundary

MCLXXXIV is a finite incidence/index factorization theorem extending MCLXXXIII.
It does not claim a continuum field equation.

## Statement

Using MCLXXXII-MCLXXXIII packets:

```text
m0 = 48   (antipodal quotient / medial incidences),
m1 = 96   (Q4 face-edge incidences),
m2 = 192  (tomotope flags),
m3 = 384  (flag doubler),
M  = 18432 (tomotope monodromy).
```

The first lock is an exact doubling staircase:

```text
48 -> 96 -> 192 -> 384,
```

each step multiplying by 2.

The second lock is area invariance:

```text
M = m0*m3 = m1*m2,
```

equivalently

```text
18432 = 48*384 = 96*192.
```

So monodromy is the same rectangle area whether you split through the outer
quotient/flag-doubler pair or the inner incidence/flag pair.

## Artifacts

- Analysis: `analysis/w33_q4_tomotope_index_staircase.py`
- Tests: `tests/test_w33_q4_tomotope_index_staircase.py`
- Result: `PART_MCLXXXIV_Q4_TOMOTOPE_INDEX_STAIRCASE_results.json`
