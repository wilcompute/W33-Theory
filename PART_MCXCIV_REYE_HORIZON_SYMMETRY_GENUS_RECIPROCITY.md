# Part MCXCIV: Reye Horizon Symmetry-Genus Reciprocity Lock

## Claim Boundary

MCXCIV is a finite reciprocity theorem linking horizon code, topology, and
symmetry on the MCXCII-MCXCIII Reye spine. It does not claim continuum
dynamics.

## Statement

From MCXCII:

```text
genus g = 6,
payload k = 66,
parity r = 6,
total n = 72,
so n = k + r = 66 + 6.
```

From MCXCIII:

```text
|Aut(Reye)| = 576,
|Aut(Tomotope)| = 96,
|Aut(Reye)|/|Aut(T)| = 6.
```

Hence the reciprocity lock:

```text
|Aut(Reye)|/|Aut(T)| = g = r = 6,
|Aut(Reye)| = g*|Aut(T)| = r*|Aut(T)|,
n = k + g = k + r = 72.
```

## Reading

The same integer `6` is simultaneously topological genus, code redundancy, and
symmetry-lift ratio from tomotope to Reye. So the horizon redundancy is not an
ad hoc add-on; it is the exact lift factor of the common spine symmetry.

## Artifacts

- Analysis: `analysis/w33_reye_horizon_symmetry_genus_reciprocity.py`
- Tests: `tests/test_w33_reye_horizon_symmetry_genus_reciprocity.py`
- Result: `PART_MCXCIV_REYE_HORIZON_SYMMETRY_GENUS_RECIPROCITY_results.json`
