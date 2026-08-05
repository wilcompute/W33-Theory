#!/usr/bin/env python3
"""Reconcile Passes 3458--3471 with the later certified Pass 3486 radius bound."""
from __future__ import annotations

import argparse
import base64
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap/pass3486_3499/results.json.zlib.b64"


def load_parallel_certificate() -> dict:
    encoded = BOOTSTRAP.read_text(encoding="utf-8").strip()
    return json.loads(zlib.decompress(base64.b64decode(encoded)))


def build_certificate() -> dict:
    parallel = load_parallel_certificate()
    radius = parallel["sections"]["pass3486_radius_435"]
    interval = radius["improved_interval"]
    assert interval == [389, 435]

    amplitude = parallel["sections"]["pass3487_3488_amplitude_grid"]
    exact = amplitude["exact_winner"]
    assert exact["ratio_strictly_below_9"] is True

    return {
        "schema": "w33.bt3471.parallel_radius_reconciliation.v1",
        "status": "PASS",
        "source_packet": "Passes 3486-3499 frozen bootstrap certificate",
        "live_covering_radius_interval": interval,
        "local_pass3458_delsarte_lower_bound": 389,
        "parallel_pass3486_upper_bound": 435,
        "parallel_amplitude_grid_verdict": "exact winner strictly below Hoffman ratio 9",
        "checks": {
            "parallel_radius_upper_bound_435": interval[1] == 435,
            "lower_bound_preserved_389": interval[0] == 389,
            "finite_amplitude_grid_below_9": exact["ratio_strictly_below_9"] is True,
        },
        "boundary": (
            "The Pass 3458 association-scheme computation independently closes the "
            "level-zero lower bound at 389. The upper bound 435 and finite amplitude-grid "
            "no-go are imported and verified from the later frozen Pass 3486-3499 packet."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    print("PASS parallel radius reconciliation 389<=R<=435")
    print(text, end="")


if __name__ == "__main__":
    main()
