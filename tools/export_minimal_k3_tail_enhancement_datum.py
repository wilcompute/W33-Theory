#!/usr/bin/env python3
"""Export the exact minimal K3 tail enhancement datum as an artifact."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE_FILE = ROOT / "exploration" / "w33_minimal_k3_tail_enhancement_datum_bridge.py"
OUTPUT_FILE = ROOT / "artifacts" / "minimal_k3_tail_enhancement_datum.json"


def load_bridge_module():
    spec = importlib.util.spec_from_file_location("minimal_tail_bridge", BRIDGE_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload() -> dict[str, object]:
    mod = load_bridge_module()
    summary = mod.build_minimal_k3_tail_enhancement_datum_summary()

    return {
        "kind": "minimal_k3_tail_enhancement_datum",
        "fixed_k3_tail_exactness_channel": summary["fixed_k3_tail_exactness_channel"],
        "current_refined_k3_zero_tail_candidate": summary[
            "current_refined_k3_zero_tail_candidate"
        ],
        "minimal_k3_tail_enhancement_datum": summary[
            "minimal_k3_tail_enhancement_datum"
        ],
        "minimal_k3_tail_enhancement_datum_theorem": summary[
            "minimal_k3_tail_enhancement_datum_theorem"
        ],
        "bridge_verdict": summary["bridge_verdict"],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()