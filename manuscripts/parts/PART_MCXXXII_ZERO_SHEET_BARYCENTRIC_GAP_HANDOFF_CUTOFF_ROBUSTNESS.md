# Part MCXXXII: Zero-Sheet Barycentric Gap-Handoff Cutoff Robustness

## Claim Boundary

This part is a finite cutoff-robustness theorem for the zero-sheet barycentric
gap-handoff cascade. It checks the same sampled ladder as MCXXXI at three
increasing prime cutoffs:

```text
X = 10^3, 10^4, 10^5
```

with `s = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0` and `subintervals = 40`.

## Statement

Across all three cutoffs:

1. the shared resonance remains exactly `s = 2.0`;
2. the handoff cascade remains detected;
3. the secondary gap sequence remains

```text
third_derivative_to_wall, third_derivative_to_wall, third_derivative_to_wall,
softening_to_order, softening_to_order, softening_to_order;
```

1. the wall-gap rank sequence remains

```text
2, 2, 2, 3, 4, 4;
```

1. the dominant wall-mass recipient remains `softening_to_order`;
1. the softening-to-order gap receives a strict majority of the wall transfer;
1. the wall-gap drop and the secondary crossing location vary only by tiny cutoff
   deviations.

So the MCXXXI handoff cascade is not a one-off finite artifact of a single prime
cutoff: its rank cascade and mass-transfer picture persist uniformly along the
sampled cutoff ladder.

## Numerical profile

- reference wall-gap drop at `10^5`:
  `0.38305552720929903`
- maximum wall-gap-drop deviation across the cutoff ladder:
  `< 1e-9`
- reference secondary crossing at `10^5`:
  `1.7384967374464677`
- maximum secondary-crossing deviation across the cutoff ladder:
  `< 1e-5`

## Interpretation

MCXXXI showed a finite inward handoff of gap rank at one cutoff. MCXXXII shows
that this is stable under increasing prime cutoff: the same resonance point,
the same ranked cascade, and the same dominant transfer recipient survive.

This is still a finite sampled theorem — a robustness profile, not an infinite
limit statement.

## Artifacts

- Code: `w33/cyclotomic.py`
- Analysis: `analysis/w33_zero_sheet_barycentric_gap_handoff_cutoff_profile.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_zero_sheet_barycentric_gap_handoff_cutoff_profile.json`
- Result: `PART_MCXXXII_zero_sheet_barycentric_gap_handoff_cutoff_robustness_results.json`
