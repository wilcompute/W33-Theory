#!/usr/bin/env python3
"""BT1901 contextual-fraction estimator for the single-photon demonstrator.

Usage:
  python analysis/bt1901_contextual_fraction_estimator.py shots.jsonl

Expected row fields are the BT1900 raw-shot fields.  The estimator reports a dark/loss-corrected
contextual fraction and a normal-approximation compatibility check against target 1/10.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

TARGET = 0.1
DEFAULT_Z = 2.0


def load_rows(path: str) -> list[dict]:
    rows = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def is_click(row: dict) -> bool:
    pattern = str(row.get("click_pattern", "")).strip().lower()
    return pattern not in {"", "0", "none", "no_click", "false"}


def estimate(rows: list[dict], z: float = DEFAULT_Z) -> dict:
    signal_rows = [r for r in rows if r.get("witness_class") == "diagonal_contextual" and not r.get("dark_reference") and not r.get("loss_probe")]
    dark_rows = [r for r in rows if r.get("dark_reference")]
    loss_rows = [r for r in rows if r.get("loss_probe")]

    signal_n = len(signal_rows)
    if signal_n == 0:
        raise SystemExit("BT1901 estimator failed: no diagonal_contextual signal rows")

    signal_clicks = sum(is_click(r) for r in signal_rows)
    dark_rate = (sum(is_click(r) for r in dark_rows) / len(dark_rows)) if dark_rows else 0.0
    loss_rate = (1.0 - sum(is_click(r) for r in loss_rows) / len(loss_rows)) if loss_rows else 0.0

    raw_fraction = signal_clicks / signal_n
    corrected = raw_fraction - dark_rate
    corrected = corrected / max(1e-12, 1.0 - loss_rate)
    corrected = max(0.0, min(1.0, corrected))

    se = math.sqrt(max(TARGET * (1.0 - TARGET), 1e-12) / signal_n)
    lower = TARGET - z * se
    upper = TARGET + z * se
    compatible = lower <= corrected <= upper

    return {
        "target_contextual_fraction": TARGET,
        "signal_rows": signal_n,
        "signal_clicks": signal_clicks,
        "raw_fraction": raw_fraction,
        "dark_rows": len(dark_rows),
        "dark_click_rate": dark_rate,
        "loss_rows": len(loss_rows),
        "loss_rate_estimate": loss_rate,
        "corrected_contextual_fraction": corrected,
        "z_window": z,
        "normal_approx_interval": [lower, upper],
        "compatible_with_one_tenth": compatible,
        "boundary": "Normal-approximation estimator for demonstrator counts; not a final statistical analysis or hardware calibration."
    }


def main(path: str) -> None:
    rows = load_rows(path)
    print(json.dumps(estimate(rows), indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: bt1901_contextual_fraction_estimator.py shots.jsonl")
    main(sys.argv[1])
