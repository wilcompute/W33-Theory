#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load(path: str):
    return json.loads(text(path))


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def build():
    zenodo = load(".zenodo.json") if exists(".zenodo.json") else {}
    cert = load("data/bt1275_strict_polar_path_recovery_certificate.json") if exists("data/bt1275_strict_polar_path_recovery_certificate.json") else {}
    vsummary = load("data/bt1281_recovery_certificate_verification_summary.json") if exists("data/bt1281_recovery_certificate_verification_summary.json") else {}
    rmanifest = load("data/bt1287_recovery_packet_release_manifest.json") if exists("data/bt1287_recovery_packet_release_manifest.json") else {}
    checks = {
        "zenodo_json_exists": exists(".zenodo.json"),
        "zenodo_license_cc_by": zenodo.get("license") == "CC-BY-4.0",
        "paper_build_workflow_exists": exists(".github/workflows/paper-build.yml"),
        "release_instructions_exist": exists("analysis/BT1259_v1_release_instructions.md"),
        "release_addendum_exists": exists("analysis/BT1290_v1_release_recovery_packet_addendum.md"),
        "readme_points_to_packet": all(s in text("README.md") for s in ["docs/recovery_packet_landing.md", "data/bt1279_recovery_packet_index.json", "data/bt1275_strict_polar_path_recovery_certificate.json"]),
        "recovery_workflow_exists": exists(".github/workflows/recovery-packet.yml"),
        "packet_index_exists": exists("data/bt1279_recovery_packet_index.json"),
        "strict_certificate_exists": exists("data/bt1275_strict_polar_path_recovery_certificate.json"),
        "strict_certificate_target": cert.get("target") == "diam14_polar_path",
        "strict_certificate_score": cert.get("score_vector", {}).get("strict_score_out_of_5") == 5,
        "certificate_verification_true": vsummary.get("verified") is True,
        "release_manifest_exists": exists("data/bt1287_recovery_packet_release_manifest.json"),
        "release_manifest_v1": rmanifest.get("release_target") == "v1.0.0",
    }
    return {
        "bt": 1291,
        "title": "Unified v1 release packet verifier",
        "verified": all(checks.values()),
        "checks": checks,
        "release_target": "v1.0.0",
        "strict_target": "diam14_polar_path"
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1291_release_packet_verification_summary.json")
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1291, "verified": result["verified"], "out": str(ns.out)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
