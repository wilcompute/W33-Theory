#!/usr/bin/env python3
"""BT1841: generated artifact pack manifest.

Defines the generated artifacts that should be produced by the BT1835-BT1840
runtime/E8 selector continuation. This is a manifest/checker, not an execution
log.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1841_GENERATED_ARTIFACT_PACK_results.json")

EXPECTED_ARTIFACTS = [
    "data/imported_runtime_artifacts/BT1835_raw_artifact_import_summary.json",
    "data/PART_BT1824_EXECUTABLE_PACKET_REPLAY_results.json",
    "data/PART_BT1825_APERTURE_SHOT_TABLE_summary.json",
    "data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE_summary.json",
    "data/PART_BT1837_TETRACODE_QUOTIENT_HUNT_results.json",
    "data/PART_BT1832_TEX_BUILD_CHECK_results.json",
    "data/PART_BT1840_BT930_MATRIX_RECOVERY_AUDIT_results.json",
]

GENERATORS = [
    "python analysis/bt1835_raw_artifact_importer.py",
    "python analysis/bt1824_executable_packet_replay.py",
    "python analysis/bt1825_aperture_shot_table_exporter.py",
    "python analysis/bt1836_e8_selector_aperture_table.py",
    "python analysis/bt1837_tetracode_quotient_hunt.py",
    "python analysis/bt1832_tex_build_check.py",
    "python analysis/bt1840_bt930_matrix_recovery_audit.py",
]


def theorem_summary():
    existence = {p: Path(p).exists() for p in EXPECTED_ARTIFACTS}
    return {
        "theorem": "BT1841 Generated Artifact Pack Manifest",
        "generators": GENERATORS,
        "expected_artifacts": EXPECTED_ARTIFACTS,
        "current_existence_check": existence,
        "pack_pass_condition": "run all generators, then all expected artifacts must exist and their internal checks must pass",
        "honest_scope": "Manifest/checker for generated outputs. It does not itself run the heavy witnesses."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
