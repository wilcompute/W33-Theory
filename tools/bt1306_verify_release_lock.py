#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data" / "bt1303_v1_release_source_of_truth_index.json"


def rel_exists(path: str) -> bool:
    return (ROOT / path).exists()


def collect(index: dict) -> list[str]:
    paths: list[str] = []
    paths.append(index["root_pointer"])
    paths.extend(index["human_entrypoints"])
    paths.extend(index["machine_entrypoints"])
    paths.append(index["runner"])
    paths.extend(index["verifiers"])
    paths.extend(index["workflows"])
    paths.append(index["paper"]["source"])
    paths.append(index["paper"]["workflow"])
    rp = index["recovery_packet"]
    paths.extend([rp["strict_certificate"], rp["candidate_schema"], rp["batch_summary"]])
    return sorted(set(paths))


def build() -> dict:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    paths = collect(index)
    missing = [p for p in paths if not rel_exists(p)]
    checks = {
        "index_exists": INDEX.exists(),
        "index_ready": index.get("ready") is True,
        "release_target_v1": index.get("release_target") == "v1.0.0",
        "strict_target": index.get("recovery_packet", {}).get("strict_target") == "diam14_polar_path",
        "all_paths_exist": not missing,
    }
    return {
        "bt": 1306,
        "verified": all(checks.values()),
        "checks": checks,
        "path_count": len(paths),
        "missing": missing,
        "index": "data/bt1303_v1_release_source_of_truth_index.json",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1306_release_lock_summary.json")
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1306, "verified": result["verified"], "path_count": result["path_count"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
