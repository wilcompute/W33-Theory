# Pass 467 measured blind-run handoff

This directory is a fail-closed acquisition contract for the frozen Pass 451 field-versus-ring classifier.

1. Copy `measurement_manifest_template.json` to `measured_manifest.json`, fill every acquisition field, and set `measured` to `true` only after real data collection.
2. Replace `calibration_matrix_template.csv` with `measured_calibration_matrix.csv`. Each row is an exact integer linear transfer map with its own positive denominator.
3. Write label-free counts to `measured_sealed_observations.csv`. Do not include any truth-like column. Each sample has a SHA256 commitment and sixteen counts.
4. Run:

```bash
python analysis/w33_pass467_hardware_blind_runner.py \
  --manifest hardware/pass467/measured_manifest.json \
  --calibration hardware/pass467/measured_calibration_matrix.csv \
  --sealed hardware/pass467/measured_sealed_observations.csv \
  --predictions hardware/pass467/measured_predictions.json
```

5. Only after predictions are frozen, create a reveal matching `reveal_template.json` and rerun with `--reveal` to score the endpoint.

The classifier, 1% abstention threshold, and balanced-accuracy endpoint are frozen. A measured run may replace only the transfer calibration and observations.
