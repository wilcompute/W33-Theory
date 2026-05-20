# Part MCXLI: Cross-Branch Gap Normalization Spine

## Claim Boundary

After fetching GitHub `master` at `3c619a82`, the new MCXXXIV-MCXL batch
introduced three adjacent substrate branches:

1. a Yang-Mills spectral-floor branch;
2. a Navier-Stokes substrate-flow branch;
3. a heat-kernel / smooth spectral-action branch.

MCXLI records the exact finite normalization spine that makes those branches
share one executable gap scale. This is a W33 substrate identity packet, not an
external continuum Clay proof by itself.

## Normalization Fix

The Yang-Mills spectral-floor script stated that the charged-sector floor is

```text
m^2 * (3/4) = (11/33)^2 * (3/4) = 1/12.
```

The executable formula was using `V/E = 1/3` rather than `m^2 = (V/E)^2`,
which made the p=2 floor compute as `1/4`. MCXLI corrects the charged-mode
contribution to use `m^2`, aligning the code with the declared floor:

```text
Delta_sub = 1/12.
```

## Cross-Branch Spine

With that correction, the three GitHub branches lock exactly:

```text
Yang-Mills substrate floor        Delta_sub = 1/12
Navier-Stokes enstrophy decay     2 Delta_sub = 1/6
Navier-Stokes vortex barrier      Delta_sub / 2 = 1/24
Heat-kernel spectral gap          lambda_2 = Theta = 10
```

The heat-kernel gap times the Navier-Stokes decay rate recovers the
Kolmogorov/Yang-Mills exponent magnitude:

```text
lambda_2 * (2 Delta_sub) = 10 * (1/6) = 5/3
Delta_YM / q             = 5 / 3
```

So the finite branch identity is

```text
lambda_2 * 2 Delta_sub = Delta_YM / q.
```

This ties the heat-kernel contraction scale, the substrate vorticity decay
scale, and the integer zero-sheet mass-gap midpoint into one exact rational
spine.

## Heat Residual Integer Collapse

The MCXL heat-kernel residual amplitudes are

```text
C4 = 360, C2 = 240, C0 = 10560.
```

Multiplying by the common floor `1/12` gives integers:

```text
C4 * Delta_sub = 30
C2 * Delta_sub = 20
C0 * Delta_sub = 880
```

That is a useful guardrail: the normalized floor is not just positive; it
integrally rescales the heat-kernel error amplitudes.

## Einstein-Hilbert Ratios

The same packet preserves the MCXL smooth-action ratios:

```text
a0/a2 = 55/7
a4/a0 = 3/110
c_EH/Theta = 32
```

These are recorded as companions, not as replacements for the gap spine.

## Artifacts

- Corrected code: `analysis/w33_ym_mass_gap_spectral_floor.py`
- Analysis: `analysis/w33_cross_branch_gap_normalization_spine.py`
- Tests: `tests/test_w33_cross_branch_gap_normalization_spine.py`
- Data: `data/w33_cross_branch_gap_normalization_spine.json`
- Result: `PART_MCXLI_cross_branch_gap_normalization_spine_results.json`
