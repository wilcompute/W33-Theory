# BT1370--BT1372 -- Counterconnection, Address Table, and Three-Epoch Scheduler Lift

## Summary

This packet continues BT1367--BT1369:

1. BT1370 separates phase-only correction from full `S3` correction.
2. BT1371 turns the Q6/tomotope equivariance certificate into an explicit
   192-row address table.
3. BT1372 upgrades the scheduler from a quotient count to explicit Steinberg
   basis labels, with an honest one-epoch obstruction and a three-epoch cure.

## BT1370 -- Counterconnection

BT1367 measured non-flat `S3` holonomy on skew-line quadrangles.  BT1370 tests
the correction hierarchy.

Phase-only `C3` twists cannot flatten the connection: `29160` quadrangles have
odd/transposition holonomy, and `C3` twists preserve parity.

A full `S3` edge counterconnection does flatten it.  In the BT1367 spanning
tree gauge, the edge residual profile is:

```text
identity:       160
transposition:  300
3-cycle:         80
```

Multiplying each residual by its inverse kills every edge residual and hence
every quadrangle holonomy.  The curvature is therefore not a pure qutrit phase
defect; it needs the mirror/transposition half of `S3`.

## BT1371 -- Explicit Q6/Tomotope Address Table

BT1368 proved that a Q6 edge subgroup and `Aut(tomotope)` are isomorphic
actions on two regular 96-point orbits.  BT1371 asks GAP for an explicit
isomorphism and builds the resulting address table:

```text
192 tomotope flags <-> 192 Q6 edges
```

The verifier checks equivariance for all 96 group elements and all 192 flags.
The table depends on the selected GAP isomorphism and basepoints, but any
choice is conjugate and preserves the same runtime address structure.

## BT1372 -- Three-Epoch Steinberg Basis Scheduler

BT1369 gave:

```text
2160 = 135 * 16 = 27 * 80
```

That is a perfect one-epoch scheduler for the 27 matter coordinates, but it is
not uniform on the full 81-dimensional Steinberg basis:

```text
2160 = 81 * 26 + 54
```

So one epoch cannot be the generation-commuting basis action.

The fix is the native ternary time cover:

```text
3 * 2160 = 6480 = 81 * 80
```

BT1372 uses the explicit rule

```text
generation = (local_slot + matter_state + epoch) mod 3
```

Across three epochs, every Steinberg basis label receives exactly 80 slots,
every generation receives 2160 slots, and epoch advance commutes with the
generation cycle.  The scheduler is therefore quotient-level in one epoch and
full-basis-level over the natural `q=3` time cover.

## Verification

```bash
python3 analysis/bt1370_s3_counterconnection_phase_holonomy_correction.py
python3 analysis/bt1371_q6_tomotope_explicit_orbit_address_table.py
python3 analysis/bt1372_three_epoch_steinberg_basis_scheduler_lift.py
python3 tests/test_bt1370_bt1372_counterconnection_address_scheduler_lifts.py
python3 -m py_compile analysis/bt1370_s3_counterconnection_phase_holonomy_correction.py analysis/bt1371_q6_tomotope_explicit_orbit_address_table.py analysis/bt1372_three_epoch_steinberg_basis_scheduler_lift.py tests/test_bt1370_bt1372_counterconnection_address_scheduler_lifts.py
python3 -m json.tool data/bt1370_s3_counterconnection_phase_holonomy_correction.json
python3 -m json.tool data/bt1371_q6_tomotope_explicit_orbit_address_table.json
python3 -m json.tool data/bt1372_three_epoch_steinberg_basis_scheduler_lift.json
```
