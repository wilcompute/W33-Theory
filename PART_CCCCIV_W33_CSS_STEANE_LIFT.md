# Part CCCCIV: W33 CSS Steane-Lift Protection Stack

**Status:** verified finite protection architecture for the W33 CSS topological code.

## Result

Parts CCCCII-CCCCIII prove the base W33 edge-qubit CSS code:

```text
[[240,81,3]]
```

That core has the right logical carrier, but distance `3` is low.  CCCCIV closes that honesty boundary at the architecture level by concatenating the W33 core with the Steane code:

```text
[[7,1,3]]
```

The length `7` is the W33 packet number `Phi6 = q^2 - q + 1`.

## Lift Table

| Lift level | Code parameters | Correctable weight |
|---:|---:|---:|
| 0 | `[[240,81,3]]` | `1` |
| 1 | `[[1680,81,>=9]]` | `4 = mu` |
| 2 | `[[11760,81,>=27]]` | `13` |
| 3 | `[[82320,81,>=81]]` | `40 = v` |

The third lift is the closure point:

```text
distance lower bound = 81 = q^4 = H1
correctable weight   = 40 = |W(3,3) vertices|
```

## Theorem

Concatenating the W33 CSS core `[[240,81,3]]` with `L` levels of the Steane `[[7,1,3]]` code gives

```text
[[240 * 7^L, 81, >= 3^(L+1)]]
```

For `L = 3`, this is `[[82320,81,>=81]]`.

## Boundary

This is a parameter and distance-lower-bound theorem, not a threshold simulation or an optimized hardware layout. It gives the finite protection stack that the photonic/topological runtime can compile before physical noise calibration.

Artifacts:

- Script: `exploration/PART_CCCCIV_W33_CSS_STEANE_LIFT.py`
- Results: `PART_CCCCIV_w33_css_steane_lift_results.json`
- Tests: `tests/test_w33_css_steane_lift_cccciv.py`
