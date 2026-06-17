# BT1266 -- Tomography Candidate Validator

## Purpose

BT1266 turns the BT1264 score vector into an operational pass/review/fail validator.

## Gates

```text
closure51840
diameter14
polar_path_P4P4
unique_all_channel_endpoint
labelled_nonzero_spread
```

## Bands

```text
pass   = all five gates true
review = full closure plus at least one additional gate, but not all gates
fail   = missing closure or score below review threshold
```

## Demo outcomes

```text
exact_polar_path:         pass,   5/5
wrong_full_order_diam12:  review, 2/5
fast_full_order_diam10_A: review, 2/5
closure_only:             fail,   1/5
not_full_order:           fail,   0/5
```

## Consequence

The ladder is now executable as a validator.  Closure-only no longer gets promoted; wrong full-order regimes are review-only; only the diameter-14 polar path target passes.

## Files

- Code: `analysis/bt1266_tomography_candidate_validator.py`
- Result: `data/bt1266_tomography_candidate_validator_summary.json`
