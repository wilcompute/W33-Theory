# BREAKTHROUGH: BT1604–BT1606 — Physical Calibration + Decoder + Fault-Path ABI

## Summary

This batch closes the physical-layer gap between the abstract finite universal ABI (BT1603) and a real bench run:

| BT | Title | Core Contribution |
|----|-------|-------------------|
| BT1604 | Physical Calibration ABI | Converts BT1601 loss/dark placeholders into bench-data schema with 95% CI gates |
| BT1605 | Detector-Bin Decoder | Inverse map: Fano bin click → Witting role + rail + Hesse residue + CSS row |
| BT1606 | Fault-Path Theorem | Extends BT1603 to retry/failure ABI with Pauli-frame recovery |

## BT1604 — Physical Calibration ABI

- **ThresholdBank**: four metrics — loss fraction, dark-count rate (Hz), detector efficiency, timing jitter (ps).
- **CalibrationRecord**: per-(bin, rail) CI record with `PASS | WARN | FAIL` gates.
- **CalibrationABI**: ingests raw samples, groups by `(bin_id, rail)`, computes 95% CI, applies gate logic.
- **Coverage**: all 168 Fano bins × 2 rails = 336 calibration records per run.
- **Usage profile preserved**: BT1602's 80-bin×9-use + 88-bin×10-use = 1600-frame profile baked into synthetic test.

## BT1605 — Detector-Bin Decoder

- **Fano geometry**: PG(2,2) — 7 points, 7 lines, tiled across 24 orbits → 168 bins.
- **Decode fields**: `bin_id → orbit, fano_point, witting_role, rail, hesse_residue, css_syndrome_row, fano_lines`.
- **Inverse lookup**: filter table by any combination of `role / rail / hesse_residue / css_row`.
- **ClickPattern → DecodedFrame**: dominant role, Hesse vote (mod 3), 7-bit CSS syndrome, validity flag.
- **Verification**: all 168 bins decoded; all 7 CSS rows covered; H-rail source bins = 12 (= 24/2).

## BT1606 — Fault-Path Theorem

- **Fault taxonomy**: 6 fault types across soft/hard severity with per-type retry budgets.
- **RetrySchedule**: overridable per bench run; defaults: missed/dark click ×3, Hesse ×2, T-inject ×1, CSS ×2.
- **PauliFrameTracker**: 7-bit syndrome vector → correction operator (I/X/Z/Y) via Fano-line lookup.
- **FaultPathABI.run_batch(1600)**: simulates all 1600 Witting frames with realistic fault probabilities.
- **Outcomes**: `PASS | CORRECTED | ABORTED` — pass rate >95% under default fault profile.

## Verification Status

```
BT1604 calibration ABI      : OK  (168 bins × 2 rails = 336 records evaluated)
BT1605 decoder              : OK  (all 168 bins decoded; 7 CSS rows covered)
BT1606 fault-path theorem   : OK  (1600 frames; pass_rate ≥ 0.95 under default profile)
```

## Next Steps (Generated)

See `COMMIT_ANALYSIS_BT1583_BT1606.md` for the full two-day commit review and top-3 outside-the-box next moves.
