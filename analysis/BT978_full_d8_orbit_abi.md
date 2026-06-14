# BT978 — Full-D8-compatible orbit ABI

BT975 showed that no fixed 2+2 lane partition survives the full transitive D8 action. BT978 therefore defines an orbit-valued ABI.

## Result

```text
lane_orbit = all four lanes
full_D8_covariant = true
```

Each role has all four lanes as its D8 orbit. Full D8 covariance is recovered only when roles are transported as tags on a four-lane orbit.

## Tradeoff

A fixed light/cache 2+2 split is V4-level. Full D8 covariance requires abandoning fixed lane families or replacing them by moving tags.

## Witness

```text
analysis/bt978_full_d8_orbit_abi.py
data/bt978_full_d8_orbit_abi_summary.json
```
