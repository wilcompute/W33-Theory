# Pass 12088: the CKM phase is not a cube-root clock phase (negative)

Claude track. Builds on 12005, 12080 and 12082.

## Test

The 12005 quark model with an equal-magnitude Barr row whose phases are multiples of pi/3. That leaves 4 parameters for
6 observables, so the test is overdetermined.

## Results

| Fit | Parameters | Best residual |
|---|---|---|
| control: continuous phases | 6 | exact; phases 0.62 and 5.62 in units of pi/3 |
| quantised phases, all 36 (k, l) | 4 | 0.053, at (0, 5) |
| baseline: 36 random fixed phase pairs | 4 | 0.021, then 0.047 (median 0.52) |

## Conclusion

Quantised pi/3 phases fit no better than random ones. In this model the CP phase is not a clock phase.

Producer: `analysis/w33_pass12088_the_ckm_phase_is_not_a_clock_phase.py`. Search drivers:
`analysis/search_drivers_12088/`.
