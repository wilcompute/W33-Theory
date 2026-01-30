# GBS TDA Follow-up Results (summary)

**Date:** 2026-01-29
**Branch:** photonic/threshold-sweeps

## Per-point follow-up (η=1.0)

- modes=6: js=0.1151 (95% CI [0.1103, 0.1279]), H1 features=119, shots=2000
- modes=5: js=0.04235 (95% CI [0.03912, 0.05014]), H1 features=45, shots=2000
- modes=4: js=0.04266 (95% CI [0.03821, 0.04902]), H1 features=17, shots=2000

## Notes

- The `modes=6` point shows markedly elevated JS and H1 feature counts versus modes 4–5, consistent with exploratory grid signals.
- Summary JSON and PNG saved in `bundles/v23_toe_finish/v23/`:
  - `gbs_threshold_tda_followup_summary.json`
  - `gbs_threshold_tda_followup_summary.png`
  - Correlation summary updated: `gbs_tda_correlation_summary.json`, `gbs_tda_w_vs_js_correlation.png`

## Next steps

- Integrate these figures into the main notebook and PR notes.
- Run robustness checks for loss and alternative encodings (threshold vs photon-number).
