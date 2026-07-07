#!/usr/bin/env python3
"""BT1835: raw uploaded-artifact importer.

Copies the uploaded JSON artifacts into data/imported_runtime_artifacts/raw when
run in an environment that has the upload directory available. The large JSONL
trace is recorded by checksum/line count by default; pass --include-trace to copy
it too.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ARTIFACTS = [
    ("bt950_snf_transform_e8_extractor.json", "dd1d3e2cc04e8461df5c8c18cc8a218ce2bc48282de8bdc0ae1d4b56a15750ab", True),
    ("bt951_exact_support_minimal_selector.json", "f7d835ac1f006448a8c1a87a57d9be6cdfa456827f5d3d9f4b9fdb7a3182c6d6", True),
    ("bt953_support60_orbit_classifier.json", "7af986c918669c1bb3f3e14abdb9d8ea6787962d1efe0f7e831ffd813f0f01e3", True),
    ("bt954_metric_selector_among_support60.json", "845dbb27d85d86ddbdb7255a9f6b47e3faa6a2d6d891b4e3aab9ba67cdb0373f", True),
    ("bt1494_photonic_qec_release_lock_repair.json", "7382c1996f4d8ecbf1d19f3efa5e6a5a6e15906c081d8b260930d3b063cb8629", True),
    ("w33_defect_aware_placement.json", "8aa55e46b3f467acd5cf3714febb5ed2290397a12b5daf3badaefc6effd649e4", True),
    ("w33_defect_walk_telemetry.json", "8846add70a47a2c5524be7d09b538d02d78767bd33dfd21fc450598bc405bb19", True),
    ("w33_packet_vm_kernel.json", "d1143bcca6e649b2b721a3c3192fee87dbca1ef0ccc15a6ca9f28a7c80795b2f", True),
    ("w33_interrupt_controller.json", "62213108e6a1ffe8771a87b8ea4dd0f5a4329d164f96776fee07e3fb14591eea", True),
    ("w33_defect_walk_trace.jsonl", "cd39ba85960d6b7d9001eea0fcfd0ce224eb15f87ef0f1c5f12812d133fecf9c", False),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def import_artifacts(src: Path, dst: Path, include_trace: bool = False):
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    missing = []
    for name, expected, copy_default in ARTIFACTS:
        source = src / name
        if not source.exists():
            missing.append(name)
            continue
        got = sha256(source)
        if got != expected:
            raise ValueError(f"checksum mismatch for {name}: {got} != {expected}")
        should_copy = copy_default or include_trace
        if should_copy:
            shutil.copyfile(source, dst / name)
        copied.append({"name": name, "sha256": got, "bytes": source.stat().st_size, "copied": should_copy})
    return {"copied": copied, "missing": missing, "all_present": not missing}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="/mnt/data")
    ap.add_argument("--dst", default="data/imported_runtime_artifacts/raw")
    ap.add_argument("--include-trace", action="store_true")
    args = ap.parse_args()
    summary = import_artifacts(Path(args.src), Path(args.dst), args.include_trace)
    out = Path("data/imported_runtime_artifacts/BT1835_raw_artifact_import_summary.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
