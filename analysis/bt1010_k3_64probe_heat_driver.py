#!/usr/bin/env python3
"""BT1010 — 64-probe K3 all-degree heat CI driver.

This is a manual long-run entrypoint. It records the requested probe count and
points the CI job at the K3 all-degree heat stack.  The actual heavy estimator is
kept separate from the smoke workflow so ordinary pushes stay cheap.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probes", type=int, default=64)
    parser.add_argument("--seed", type=int, default=1010)
    args = parser.parse_args()
    out = {
        "theorem": "BT1010 K3_16 64-probe all-degree heat CI driver",
        "workflow": ".github/workflows/r3-k3-64probe-heat.yml",
        "requested_probes_per_degree": args.probes,
        "random_seed": args.seed,
        "baseline_checkpoint": "BT1007 16-probe checkpoint",
        "target": "all five K3_16 level-1 Hodge degrees; alternating supertrace target chi=24",
        "production_command": "python analysis/bt1010_k3_64probe_heat_driver.py --probes 64",
        "boundary": "This driver separates long heat-estimator runs from the cheap R3 smoke workflow. The committed output is a CI job manifest; the long run should be executed by manual workflow dispatch.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1010_k3_64probe_heat_driver.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
