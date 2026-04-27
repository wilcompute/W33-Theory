#!/usr/bin/env python3
"""Export the fixed-base Payne-to-qutrit local 27/45 dictionary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_burkhardt_moduli_realization.py"
OUTPUT_FILE = ROOT / "artifacts" / "payne_qutrit_local_dictionary.json"


def load_burkhardt_module():
    spec = importlib.util.spec_from_file_location("burkhardt_test_module", TEST_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload() -> dict[str, object]:
    mod = load_burkhardt_module()
    witness = mod.explicit_payne_to_qutrit_local_dictionary()
    qutrit_shell = witness["qutrit_shell"]

    return {
        "kind": "payne_qutrit_local_dictionary",
        "base_point_index": 0,
        "point_mapping_rows": [
            {
                "payne_point_index": source,
                "h27_point_index": target,
                "h27_vertex": qutrit_shell["h27_vertices"][target],
                "heisenberg_xyz": list(qutrit_shell["vertex_to_xyz"][target]),
            }
            for source, target in sorted(witness["point_mapping"].items())
        ],
        "ordinary_36_triangles": [
            {
                "indices": list(triangle),
                "h27_vertices": [qutrit_shell["h27_vertices"][index] for index in triangle],
                "heisenberg_xyz": [list(qutrit_shell["vertex_to_xyz"][index]) for index in triangle],
            }
            for triangle in witness["type1_images"]
        ],
        "hyperbolic_9_fibers": [
            {
                "indices": list(fiber),
                "h27_vertices": [qutrit_shell["h27_vertices"][index] for index in fiber],
                "heisenberg_xyz": [list(qutrit_shell["vertex_to_xyz"][index]) for index in fiber],
            }
            for fiber in witness["type2_images"]
        ],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()