#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1331_master_synthesis_certificate.json")
    ns = ap.parse_args()
    audit = load("data/bt1327_q4_diamond_audit.json")
    epoch = load("data/bt1328_epoch_repair.json")
    bt1326 = (ROOT / "proofs" / "BT1326_w33_holonet_master_synthesis.md").read_text(encoding="utf-8")
    clauses = [
        {"name": "q4_number_table", "class": "exact_arithmetic", "status": "verified_with_one_repaired_epoch", "evidence": "data/bt1327_q4_diamond_audit.json"},
        {"name": "rolling_epoch_10980", "class": "exact_arithmetic", "status": "verified", "evidence": "data/bt1328_epoch_repair.json"},
        {"name": "spinor_cohomology", "class": "structural_theorem", "status": "proof_note_present", "evidence": "proofs/BT1323_global_section_spinor_cohomology.md"},
        {"name": "photonic_mode_encoding", "class": "constructive_design", "status": "proof_note_present", "evidence": "proofs/BT1324_photonic_mode_encoding.md"},
        {"name": "fault_tolerance_threshold", "class": "simulation_required", "status": "claimed_not_independently_certified_here", "evidence": "proofs/BT1325_fault_tolerance_threshold.md"},
        {"name": "physical_chip_footprint", "class": "experimental_assumption", "status": "requires_layout_and_foundry_model", "evidence": "proofs/BT1324_photonic_mode_encoding.md"}
    ]
    checks = {
        "bt1326_source_exists": exists("proofs/BT1326_w33_holonet_master_synthesis.md"),
        "bt1321_source_exists": exists("proofs/BT1321_holonet_q3_atlas_bridge.md"),
        "bt1327_audit_exists": exists("data/bt1327_q4_diamond_audit.json"),
        "bt1328_epoch_repair_verified": epoch.get("verified") is True,
        "bt1327_only_epoch_lcm_failed": audit.get("failed") == ["epoch_lcm_10980"],
        "bt1326_mentions_rolling_epoch": "rolling chart-phase closure" in bt1326,
        "bt1326_no_false_epoch_lcm": "lcm(3660, 1620)" not in bt1326,
    }
    result = {
        "bt": 1331,
        "title": "BT1326 master synthesis certificate",
        "verified": all(checks.values()),
        "checks": checks,
        "clauses": clauses,
        "verdict": "BT1326 is certificate-backed for exact arithmetic and corrected epoch wording; threshold and chip-footprint claims remain separately certifiable engineering/simulation gates."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1331, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
