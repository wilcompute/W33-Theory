#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BADGE = ROOT / "data" / "bt1295_v1_release_readiness_badge.json"
SUMMARY = ROOT / "data" / "bt1291_release_packet_verification_summary.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    badge = load(BADGE)
    summary = load(SUMMARY)
    checks = {
        "badge_ready": badge.get("ready") is True,
        "badge_release_target": badge.get("release_target") == "v1.0.0",
        "badge_strict_target": badge.get("strict_target") == "diam14_polar_path",
        "badge_expected_score": badge.get("expected_outputs", {}).get("strict_score_out_of_5") == 5,
        "badge_expected_bands": badge.get("expected_outputs", {}).get("candidate_bands") == {"pass": 1, "review": 1, "fail": 2},
        "release_summary_verified": summary.get("verified") is True,
        "release_summary_target": summary.get("strict_target") == badge.get("strict_target"),
    }
    return {
        "bt": 1296,
        "title": "Release readiness badge verifier",
        "verified": all(checks.values()),
        "checks": checks,
        "badge": str(BADGE.relative_to(ROOT)),
        "release_summary": str(SUMMARY.relative_to(ROOT))
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1296_readiness_badge_verification_summary.json")
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1296, "verified": result["verified"], "out": str(ns.out)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
