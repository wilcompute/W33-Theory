#!/usr/bin/env python3
"""Export the fixed-base Payne-to-cubic local 27/45 dictionary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_burkhardt_moduli_realization.py"
OUTPUT_FILE = ROOT / "artifacts" / "payne_cubic_local_dictionary.json"


def load_burkhardt_module():
    spec = importlib.util.spec_from_file_location("burkhardt_test_module", TEST_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload() -> dict[str, object]:
    mod = load_burkhardt_module()
    witness = mod.explicit_payne_to_cubic_local_dictionary()
    inverse_labels = {
        line: label for label, line in witness["record"]["classical_labels"].items()
    }

    type1_images = set(witness["type1_images"])
    type2_images = set(witness["type2_images"])
    mixed_30 = witness["mixed_30"]
    c_only_15 = witness["c_only_15"]

    return {
        "kind": "payne_cubic_local_dictionary",
        "base_point_index": 0,
        "reference_double_six_index": 0,
        "point_mapping_rows": [
            {
                "payne_point_index": source,
                "cubic_line_index": target,
                "cubic_label": inverse_labels[target],
            }
            for source, target in sorted(witness["point_mapping"].items())
        ],
        "type1_tritangents": witness["type1_planes"],
        "type2_tritangents": witness["type2_planes"],
        "split_summary": {
            "type1_total": 36,
            "type2_total": 9,
            "type1_mixed": sum(triangle in mixed_30 for triangle in type1_images),
            "type1_c_only": sum(triangle in c_only_15 for triangle in type1_images),
            "type2_mixed": sum(triangle in mixed_30 for triangle in type2_images),
            "type2_c_only": sum(triangle in c_only_15 for triangle in type2_images),
        },
        "hyperbolic_nine_shape": {
            "mixed_index_triangles": [[1, 2, 6], [3, 4, 5]],
            "c_only_matchings": [
                [[1, 4], [2, 3], [5, 6]],
                [[1, 3], [2, 5], [4, 6]],
                [[1, 5], [2, 4], [3, 6]],
            ],
        },
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()