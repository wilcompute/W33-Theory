"""Verify a SAT/CP/assignment result using the repo's verification bridges.

This script reads a JSON result file produced by the CSP runners (assignment map)
and attempts to run the canonical K3/mixed-plane nilpotent holonomy bridge
and the packet-level audits to validate whether a proposed selector actually
activates the expected holonomy and arithmetic tail.

Run locally after a solver produces `data/transport_csp_*.json` or a CNF solver
produces an interpretation mapping.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("result", nargs="?", default="data/transport_csp_real_result.json")
    args = parser.parse_args()

    path = Path(args.result)
    if not path.exists():
        print(json.dumps({"status": "missing_result_file", "path": str(path)}))
        return

    result = json.loads(path.read_text(encoding="utf-8"))
    assignment = result.get("assignment")
    if not assignment:
        print(json.dumps({"status": "no_assignment_in_result", "result": result}, indent=2))
        return

    out = {"status": "verification_attempt", "input_result": str(path)}

    # Try to run the K3 mixed-plane nilpotent holonomy bridge summary
    try:
        from exploration.w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (
            build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
        )

        bridge = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()
        out["k3_mixed_plane_bridge"] = bridge.get("theorem") or bridge.get("bridge_verdict") or bridge
    except Exception as exc:  # pragma: no cover - environment dependent
        out["k3_mixed_plane_bridge_error"] = str(exc)

    # Try packet-level audit
    try:
        from scripts.w33_h4_s3_selector_holonomy_audit import analyze_assignment_if_possible  # type: ignore

        audit = analyze_assignment_if_possible(assignment)
        out["packet_assignment_audit"] = audit
    except Exception as exc:
        out["packet_assignment_audit_error"] = str(exc)

    # Write certificate file
    cert_path = Path("data") / f"transport_verification_{path.stem}.json"
    cert_path.parent.mkdir(exist_ok=True)
    cert_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
