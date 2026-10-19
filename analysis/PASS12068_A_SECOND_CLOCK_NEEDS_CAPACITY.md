# Pass 12068: a tick capacity condenses a whole context, not a pair

Claude track. Builds on 12055 and 12061.

## Model

The model is V_T = F_T(φ) + g Σφ² at fixed Σφ = 1, i.e. 12055 plus a tick-capacity cost.

## Exact spectra

Compatible ticks on one context share one joint eigenvector (a stabiliser state). Their uniform-weight spectra are:

| Ticks n | Spectrum |
|---|---|
| 1 | {0³, 1⁶} |
| 2 | {0, (½)⁴, 1⁴} |
| 3 | {0, (⅔)⁶, 1²} |
| 4 | {0, (¾)⁸} |

## Threshold

An n-set beats the single tick when g > g_n = n/(n−1) (F_n − F_1). For the full context, with y = e^(−β/4):

g₄ = (4/3) T log[(3 + 6y⁴)/(1 + 8y³)] > 0,

because 3 + 6y⁴ − 1 − 8y³ = 2(1−y)²(1+2y+3y²).

## Results

1. **The first condensate after a single tick is the full context.** On T ∈ [0.05, 2], g₄ < g₃ < g₂, and g₄ is also
   below the far-pair and uniform thresholds. So a capacity cost jumps from one tick straight to a whole context, never
   to a pair.
2. **The context phase is a window g₄ < g < g_u:**
   - T = 0.2: [0.251, 1.083];
   - T = 1: [0.114, 0.139].

   Inside the window, uniform weights are optimal within the 4-set, and the context beats every structured candidate.
   Above it, the condensate spreads.
3. **The multistart is a record, not a proof.** The frozen 40-start run (`search_drivers_12068/capacity.out`) can stall
   in a 3-tick set (0.0775 against the context's 0.0544 at T = 0.2, g = 0.356).

## Reading

Positive tick generators with a finite capacity choose a measurement context, i.e. a stabiliser state. That is the same
object that signed Pauli fields chose in 12055.

## Caution for 12060–12061

Those passes read clock pairs as tick pairs. But the 12055 Clifford ticks match the 120 clock involutions only in
number. Under linear Sp(4,3), the label-0 tick at x is fixed by the whole point stabiliser, not by the clock group. So
rest-frame statements for tick condensates wait on an explicit tick-to-clock map, which is **open**. The group-theoretic
results of 12060 (clock groups, mirror frames) are unaffected.

## Certificates

- Producer: `analysis/w33_pass12068_a_second_clock_needs_capacity.py`.
- Drivers: `analysis/search_drivers_12068/`.
