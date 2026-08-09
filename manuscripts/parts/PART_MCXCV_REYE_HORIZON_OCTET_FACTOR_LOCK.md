# Part MCXCV: Reye Horizon Octet-Factor Lock

## Claim Boundary

MCXCV is a finite combinatorial factor law extending MCXCII-MCXCIV with the
tomotope cell packet from MCLXXXVI. It does not claim continuum dynamics.

## Statement

Use these verified packets:

```text
C = 8   (tomotope cells),
N = 72  (horizon code total),
P = 12  (Reye points),
g = 6   (genus/parity),
A_R = 576 (Reye automorphism order),
A_T = 96  (tomotope automorphism order).
```

Then the octet-factor lock is:

```text
A_R = C*N = C*P*g = 8*72 = 8*12*6 = 576,
A_T = P*C = 12*8 = 96,
N = P*g = 12*6 = 72.
```

Derived integer densities:

```text
N/C = 9   symbols per cell,
A_R/N = 8 symmetry units per horizon symbol.
```

## Reading

The tomotope cell octet is not an isolated number: it is the exact lift factor
from horizon volume to Reye symmetry volume.

## Artifacts

- Analysis: `analysis/w33_reye_horizon_octet_factor_lock.py`
- Tests: `tests/test_w33_reye_horizon_octet_factor_lock.py`
- Result: `PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json`
