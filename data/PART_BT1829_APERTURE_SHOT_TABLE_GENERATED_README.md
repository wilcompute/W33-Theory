# BT1829 — Generated Aperture CSV Artifact Note

BT1825 introduced the exporter for the full aperture shot table:

```bash
python analysis/bt1825_aperture_shot_table_exporter.py
```

Expected generated artifacts:

- `data/PART_BT1825_APERTURE_SHOT_TABLE.csv`
- `data/PART_BT1825_APERTURE_SHOT_TABLE_summary.json`

Expected table shape:

| field | value |
|---|---:|
| centers | 40 |
| phase rows per center | 9 |
| apertures per phase row | 4 |
| total rows | 1440 |

The uploaded BT1820/BT1825 chain gives this as a physical readout skeleton, not measured data. Observed-shot columns remain blank until a physical or simulated readout fills them.

Honest boundary: this commit records the generated-artifact path and required row count. The full 1440-row CSV is produced by running the exporter in the repo environment.
