Subject: Exact PMNS fractions in the W(3,3) project

Hi,

The exact PMNS formulas currently promoted at verified status in the repo are the cyclotomic ones:

- `sin^2(theta_12) = 4/13`
- `sin^2(theta_23) = 7/13`
- `sin^2(theta_13) = 2/91`

The implementation is in `analysis/PMNS_CYCLOTOMIC.py`. The route is:

- `q = 3`
- `lambda = q - 1 = 2`
- `mu = q + 1 = 4`
- `Phi_3(q) = q^2 + q + 1 = 13`
- `Phi_6(q) = q^2 - q + 1 = 7`

and then

- `sin^2(theta_12) = mu / Phi_3 = 4/13`
- `sin^2(theta_23) = Phi_6 / Phi_3 = 7/13`
- `sin^2(theta_13) = lambda / (Phi_3 Phi_6) = 2/91`

So the numerators are not post-fit choices:

- `4` is `mu = q + 1`
- `2` is `lambda = q - 1`
- `7` is `Phi_6(3)`

The strongest honest statement is that this is an exact projective/cyclotomic layer tied to the `W(3,3)` parameter set. It is not yet a finished subgroup-chain or direct incidence-theorem derivation from the geometry alone.

The angle-only Jarlskog magnitude from these three angles is

- `J_max ~= 0.03336`

but the physical invariant is still phase-dependent:

- `J = J_max sin(delta)`

So `0.03336` should be read as `J_max`, not as a phase-independent prediction for `J`.

Repro commands:

```powershell
$env:PYTHONUTF8='1'
py -3 .\PMNS_CYCLOTOMIC.py
py -3 -m pytest tests\test_master_derivation.py -k "p20_pmns_theta12 or p21_pmns_theta23 or p22_pmns_theta13" -q
py -3 -m pytest tests\test_tower_generation_rules.py -k "pmns_theta12 or pmns_theta23 or pmns_theta13 or jarlskog_invariant" -q
```

The exact PMNS checks already exist in:

- `tests/test_master_derivation.py`
- `tests/test_tower_generation_rules.py`

For a broader current snapshot of what is verified versus still interpretive, see `docs/march_2026_frontier_note.md`.

Best,

Wil
