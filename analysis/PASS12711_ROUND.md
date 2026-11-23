# Pass 12711 (exploration): when does ternary actually beat binary? Above a noise threshold (swing-to-noise ≈ 9), and only when cost scales with the number of levels; for neural-network weights ternary wins by sparsity, not by bits

Claude track, a self-directed exploration requested by the user. It is not physics and not a theory-of-everything claim.
- Script: `explore_pass12711_ternary_noise.py` (≈6 s).
- Certificate: `data/explore_pass12711_ternary_noise.json`.
- Tests: `tests/test_toe_pass12711.py`, 3 tests passing.
- Related: the `ternary_radix_simplex_note.py` of Pass 12708.

**The claim tested:** "base 3 is optimal because 3 is the integer closest to e". This is exact only when digits are noiseless and a digit costs in proportion to its number of states r, so that log₂r/r peaks at e. Both assumptions were relaxed here.

## (1) Noisy radix economy
**Setup:**
- r equally spaced levels in a fixed voltage swing.
- Gaussian noise σ, with SNR = swing/σ.
- Equiprobable symbols.
- The mutual information I_r(SNR) was computed numerically.

| SNR | bits/symbol r = 2 / 3 / 4 | bits per unit cost (cost ∝ r) |
|---|---|---|
| 2 | 0.48 / 0.37 / 0.32 | **0.24** / 0.12 / 0.08 |
| 4 | 0.91 / 0.89 / 0.82 | **0.46** / 0.30 / 0.20 |
| 8 | 1.00 / 1.47 / 1.52 | **0.50** / 0.49 / 0.38 |
| 32 | 1.00 / 1.58 / 2.00 | 0.50 / **0.53** / 0.50 |

- **Below SNR ≈ 9, binary wins.** Ternary is optimal from SNR ≈ 8.9 upward, for every higher SNR, under cost ∝ r.
- **At high SNR, base 2 and base 4 tie exactly.** Both give log₂r/r = 0.5, and base 3 beats them by 5.6%.

**A more realistic cost**, 1 + c(r − 1): a fixed device cost plus a cost per extra level.

| c (cost of an extra level, relative to the device) | optimal r at SNR 3 / 10 / 32 / 100+ |
|---|---|
| 0.1 | 2 / 4 / 7 / 8 |
| 0.3 | 2 / 3 / 5 / 5 |
| 1.0 | 2 / 3 / 3 / 3 |

- **Ternary is the optimum only when an extra level costs about as much as a whole device.** That is the classic radix-economy assumption.
- **When devices dominate the cost, more levels win at high SNR.** Multi-level flash memory (QLC, 16 levels) is this case.
- **Binary dominates real logic** because noise margins are expensive: CMOS logic effectively operates in the "binary wins" regime.

## (2) Ternary neural-network weights
Gaussian weights, with optimal (Lloyd–Max) scalar quantisers:

| r | distortion D/σ² | levels | entropy (bits) | quality per fixed-length bit | quality per entropy-coded bit |
|---|---|---|---|---|---|
| 2 | 0.3634 | ±0.80 | 1.000 | 4.40 dB | 4.40 dB |
| **3** | **0.1902** | 0, ±1.22 | 1.536 | 4.55 dB | 4.69 dB |
| 4 | 0.1175 | ±0.45, ±1.51 | 1.911 | 4.65 dB | 4.87 dB |
| 8 | 0.0345 | — | 2.825 | 4.87 dB | 5.17 dB |

- **Per bit stored, ternary is only 0.15–0.3 dB better than binary**, and more levels keep improving.
- **Ternary's real advantage is structural.** About 46% of the weights land exactly on 0, and those multiplications are skipped. The rest are ±1, so multiply-accumulate becomes signed addition.
- **This is why ternary networks (e.g. BitNet b1.58) are attractive:** for compute and energy, not for information per bit.

## Takeaway
The "closest to e" argument is a real but narrow optimum. It holds when:
- noise is low (SNR ≳ 9);
- the cost of a digit scales with its number of states.

In practice:
- **Logic hardware:** binary is optimal, because noise margins are expensive.
- **Storage:** many levels are optimal.
- **Neural-network weights:** ternary is optimal, because zero is free.
