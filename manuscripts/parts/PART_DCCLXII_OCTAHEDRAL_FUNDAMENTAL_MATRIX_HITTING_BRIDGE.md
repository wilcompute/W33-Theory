# Part DCCLXII — Octahedral Fundamental-Matrix / Hitting Bridge

## Why this part exists

DCCLIV gave exact hitting times by direct linear solves. DCCLXI gave renewal structure. This part adds the canonical ergodic-chain fundamental matrix representation that unifies hitting data and Kemeny invariants.

## Exact fundamental matrix

For transition matrix `P` and uniform stationary projector `Pi = 1 pi^T`, define

```text
Z = (I - P + Pi)^(-1).
```

The verifier proves exact inversion identity and then recovers all hitting times by

```text
H_ij = (Z_jj - Z_ij)/pi_j.
```

This matches both direct hitting solves and the previous DCCLIV hitting matrix.

## Exact consequences

The verifier confirms:

- adjacent hitting times are exactly `5`,
- antipodal hitting times are exactly `6`,
- Kemeny row sums are independent of start state,
- exact Kemeny value:

  ```text
  K = 13/3,
  ```

- trace identity:

  ```text
  K = trace(Z) - 1.
  ```

So transport times, recurrence invariants, and resolvent-like matrix structure are now in one exact formula layer.

## Meaning

The closure random-walk chain now has:

- explicit hitting-time equations,
- explicit first-return renewal equations,
- and explicit fundamental-matrix representation linking both.

This is the cleanest exact finite resolvent-hitting bridge so far.

## Exact vs conditional

- **Exact:** all octahedral hitting and Kemeny data are reproduced by `Z=(I-P+Pi)^(-1)`.
- **Conditional:** continuum resolvent/hitting interpretation still requires a scaling limit.

## Executable artifact

- Verifier: `verify_dcclxii_octahedral_fundamental_matrix_hitting_bridge.py`
- Tests: `tests/test_dcclxii_octahedral_fundamental_matrix_hitting_bridge.py`
- Data: `data/dcclxii_octahedral_fundamental_matrix_hitting_bridge.json`
