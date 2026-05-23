# Part MCCXII: Poincare Dual Code Law

## Claim Boundary

MCCXII formalizes the dual-surface code packet and keeps distance exactness
explicitly conditional.

## Statement

From the K12 orientable surface:

```text
primal: V=12, E=66, F=44, g=6.
```

Under Poincare duality (swap V and F, keep E):

```text
dual: V'=44, E'=66, F'=12, g'=6.
```

Code packets:

```text
edge code: [72,66,*]_3 with rank(H)=72-66=6,
face code: [50,44,*]_3 with rank(H)=50-44=6.
```

So both packets satisfy:

```text
rank(H)=g=6.
```

Distance closure (conditional):

- edge packet `d=3=q` from MCCXI conditional closure;
- face packet `d=3=q` by declared Poincare-dual distance transfer.

## Honest boundary

Exact `d=3` for the face packet is conditional on the dual-transfer hypothesis
plus MCCXI embedding assumptions.

## Artifacts

- Analysis: `analysis/w33_poincare_dual_code.py`
- Tests: `tests/test_w33_poincare_dual_code.py`
- Result: `PART_MCCXII_POINCARE_DUAL_CODE_results.json`
