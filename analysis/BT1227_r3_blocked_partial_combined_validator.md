# BT1227 -- Combined R3 Blocked/Partial Validator

## Purpose

BT1223 validated the blocked mock sequence. BT1226 introduced the first partial fixture. BT1227 validates both together.

## Result

The combined input set is:

- four BT1220 mock refinement samples;
- one BT1226 partial refinement fixture.

The expected status counts are

\[
\text{blocked}=4,
\qquad
\text{partial}=1,
\qquad
\text{candidate}=0.
\]

The pushed summary matches exactly.

## Interpretation

The R3 evidence pipeline now has an executable two-lane test:

\[
\text{blocked mock data}
\to
\text{partial computed fixture}
\to
\text{no candidate yet}.
\]

Candidate promotion remains disallowed.

## Files

- Code: `analysis/bt1227_r3_blocked_partial_combined_validator.py`
- Result: `data/bt1227_r3_blocked_partial_combined_validator_summary.json`

## Boundary

BT1227 does not create physical R3 evidence. It verifies the validator behavior across blocked and partial fixtures.
