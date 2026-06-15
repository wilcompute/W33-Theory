# BT1121 — Phase-transfer Yukawa test

BT1121 implements the BT1118 phase-transfer route as a diagnostic script.

## Rejected map

The naive map

```text
sqrt(m_g) proportional to reservoir weight w_g
```

fails exact Koide in the positive small-perturbation regime.

## Phase-transfer map

Use the reservoir only for phase/order data:

```text
w_g = 1 + epsilon cos(theta + 2*pi*g/3).
```

Then define the square-root Yukawa vector by the Koide-radius map:

```text
sqrt(y_g) = A * (1 + sqrt(2) cos(theta + 2*pi*g/3)).
```

This gives exact Koide ratio for any phase `theta` as long as the vector is interpreted as the phase-spaced Koide square-root vector.

## Script

```text
tools/bt1121_phase_transfer_yukawa_test.py
```

The script reports:

```text
reservoir_weights
reservoir_Q_if_naive_mass_map
yukawa_sqrt_vector_phase_transfer
yukawa_Q
koide_error
```

## Boundary

This is not a charged-lepton fit.  It is a diagnostic proving that the phase-transfer route avoids the BT1113 obstruction while keeping the reservoir generation phase testable.
