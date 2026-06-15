# BT1128 — Phase-transfer numeric report

BT1128 commits a non-fit numeric reference report for the BT1121 phase-transfer map.

## Parameters

```text
theta = 0.2223
epsilon = 0.1
```

The phase value is the archived Koide-style phase used in the recent W33 ledger.  The small epsilon is only a reservoir-projector perturbation amplitude.

## Reservoir weights

```text
w = (1.0975392940, 0.9321367784, 0.9703239275)
```

If naively interpreted as square-root masses, these give

```text
Q = 0.335
```

which confirms again that the reservoir weights are not the mass vector.

## Phase-transfer Yukawa vector

Using the Koide-radius map

```text
sqrt(y_g) = 1 + sqrt(2) cos(theta + 2*pi*g/3)
```

gives

```text
sqrt(y) = (2.3794139249, 0.0402691168, 0.5803169582)
Q = 0.6666666666666671
```

with numerical error from `2/3` of about

```text
4.44e-16.
```

## Boundary

This is a diagnostic and non-fit reference report.  It does not claim the charged-lepton masses are fitted.
