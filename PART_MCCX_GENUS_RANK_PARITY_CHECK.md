# Part MCCX: Genus-Rank Parity-Check Law

## Claim Boundary

MCCX is a finite code/topology identification theorem for the established
horizon packet. It does not claim universality for all code families.

## Statement

For the ternary horizon packet:

```text
[n,k]_3 = [72,66]_3,
rank(H)=n-k=6.
```

Using established geometry/packet constants:

```text
g = 6,
k_val = 12,
N_M = 36,
q = 3,
```

one has the exact lock:

```text
rank(H)=n-k=72-66=6=g=k_val/2=N_M/(2q).
```

So parity-check rank equals genus, and the same value appears in two equivalent
structural normalizations.

## Artifacts

- Analysis: `analysis/w33_genus_rank_parity_check.py`
- Tests: `tests/test_w33_genus_rank_parity_check.py`
- Result: `PART_MCCX_GENUS_RANK_PARITY_CHECK_results.json`
