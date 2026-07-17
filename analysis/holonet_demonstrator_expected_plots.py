#!/usr/bin/env python3
"""Generate lab-packet planning artifacts for the Holonet contextuality demonstrator.

This script is intentionally dependency-free. It writes a stable analyzer-map ABI,
an expected-plot SVG, and a compact JSON summary for the single-photon
Witting/KS contextuality protocol.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"


def significance(valid_shots: int, p: float = 0.1) -> float:
    return math.sqrt(valid_shots * p / (1.0 - p))


def polyline(points, x0, y0, w, h, xmax, ymax):
    coords = []
    for x, y in points:
        px = x0 + w * x / xmax
        py = y0 + h * (1.0 - y / ymax)
        coords.append(f"{px:.1f},{py:.1f}")
    return " ".join(coords)


def write_analyzer_map():
    path = DOCS / "holonet_demonstrator_analyzer_map.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["context_id", "basis_slot", "phase_setting"])
        for context_id in range(40):
            for basis_slot in range(4):
                writer.writerow(
                    [context_id, basis_slot, f"witting_{context_id:02d}_{basis_slot}"]
                )
    return path


def write_svg():
    shots = list(range(0, 301, 15))
    sig = [(n, significance(n)) for n in shots]
    satisfied = [(n, 36 + 4 * (1 - math.exp(-n / 80.0))) for n in shots]
    sx = polyline(sig, 70, 40, 700, 260, 300, 6)
    cx = polyline(satisfied, 70, 360, 700, 260, 300, 40)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="700" viewBox="0 0 860 700">
  <style>
    text {{ font-family: Segoe UI, Arial, sans-serif; fill: #eaf4ff; }}
    .muted {{ fill: #9fb1c2; font-size: 13px; }}
    .axis {{ stroke: #32445a; stroke-width: 1; }}
    .grid {{ stroke: #203044; stroke-width: 1; }}
    .curve {{ fill: none; stroke: #66d9ef; stroke-width: 4; }}
    .target {{ stroke: #f4c95d; stroke-width: 2; stroke-dasharray: 8 6; }}
    .kill {{ stroke: #ff6b6b; stroke-width: 2; stroke-dasharray: 8 6; }}
  </style>
  <rect width="860" height="700" fill="#0b1017"/>
  <text x="40" y="28" font-size="22" font-weight="700">Holonet contextuality demonstrator planning surfaces</text>
  <text x="70" y="62" class="muted">Significance for CF=1/10 vs zero</text>
  <line x1="70" y1="300" x2="770" y2="300" class="axis"/>
  <line x1="70" y1="40" x2="70" y2="300" class="axis"/>
  <line x1="70" y1="170" x2="770" y2="170" class="grid"/>
  <line x1="70" y1="{40 + 260 * (1 - 3/6):.1f}" x2="770" y2="{40 + 260 * (1 - 3/6):.1f}" class="target"/>
  <line x1="70" y1="{40 + 260 * (1 - 5/6):.1f}" x2="770" y2="{40 + 260 * (1 - 5/6):.1f}" class="target"/>
  <polyline points="{sx}" class="curve"/>
  <text x="780" y="{40 + 260 * (1 - 3/6):.1f}" class="muted">3 sigma</text>
  <text x="780" y="{40 + 260 * (1 - 5/6):.1f}" class="muted">5 sigma</text>
  <text x="70" y="330" class="muted">valid heralded coincidences</text>
  <text x="70" y="382" class="muted">Satisfied-context budget: kill line S=36, target S=40</text>
  <line x1="70" y1="620" x2="770" y2="620" class="axis"/>
  <line x1="70" y1="360" x2="70" y2="620" class="axis"/>
  <line x1="70" y1="620" x2="770" y2="620" class="kill"/>
  <line x1="70" y1="360" x2="770" y2="360" class="target"/>
  <polyline points="{cx}" class="curve"/>
  <text x="780" y="624" class="muted">S=36 kill</text>
  <text x="780" y="364" class="muted">S=40 target</text>
  <text x="70" y="650" class="muted">This is a planning guide, not measured data. Real certification uses raw JSONL + validators.</text>
</svg>
"""
    path = DOCS / "holonet_demonstrator_expected_plots.svg"
    path.write_text(svg, encoding="utf-8")
    return path


def write_json(analyzer_map, svg):
    path = DATA / "holonet_demonstrator_lab_packet.json"
    payload = {
        "claim": "W(3,3) Witting/KS contextual fraction CF=1/10",
        "noncontextual_bound_S": 36,
        "quantum_target_S": 40,
        "contextual_fraction": 0.1,
        "valid_shots_for_3_sigma": 81,
        "valid_shots_for_5_sigma": 225,
        "analyzer_map": str(analyzer_map.relative_to(ROOT)),
        "expected_plots": str(svg.relative_to(ROOT)),
        "raw_shot_template": "docs/holonet_demonstrator_raw_shot_template.jsonl",
        "required_raw_shot_fields": [
            "shot_id",
            "witting_tetrad",
            "alice_slot",
            "bob_slot",
            "logical_pair_type",
            "transaction_tick",
            "time_bin",
            "detector_id",
            "polarization_setting",
            "tritter_phase_setting",
            "modulator_phase",
            "click_pattern",
            "dark_reference",
            "loss_probe",
            "accepted_flag",
            "witness_class",
        ],
        "basis_local_frame_records_target": 640,
        "validator": "analysis/bt1900_demonstrator_raw_shot_validator.py",
        "estimators": [
            "analysis/bt1901_contextual_fraction_estimator.py",
            "analysis/bt1904_exact_contextual_fraction_estimator.py",
        ],
        "boundary": "planning packet and ABI; physical certification requires real raw JSONL",
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> int:
    DOCS.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    analyzer_map = write_analyzer_map()
    svg = write_svg()
    json_path = write_json(analyzer_map, svg)
    print("Holonet demonstrator lab packet artifacts")
    print(f"  analyzer map  : {analyzer_map.relative_to(ROOT)}")
    print(f"  expected plots: {svg.relative_to(ROOT)}")
    print(f"  summary json  : {json_path.relative_to(ROOT)}")
    print("  status        : PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
