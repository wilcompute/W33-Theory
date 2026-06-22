#!/usr/bin/env python3
"""BT1494: restore root-level legacy artifacts for the photonic-qec gate."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "manuscripts" / "parts"
OUT = ROOT / "data" / "bt1494_photonic_qec_release_lock_repair.json"

REQUIRED_ARTIFACTS = [
    "PART_CCCXCVI_photonic_life_runtime_architecture_results.json",
    "PART_CCCCII_w33_css_topological_code_results.json",
    "PART_CCCCIII_w33_css_distance_results.json",
    "PART_CCCCIV_w33_css_steane_lift_results.json",
    "PART_CCCCIV_w33_distance_amplification_results.json",
    "PART_CCCCIX_line_star_rank_correction_results.json",
    "PART_CCCCV_protected_toe_kernel_results.json",
    "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json",
    "PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER.md",
    "PART_CCCCXIX_photonic_harmonic_tqc_synthesis_results.json",
    "PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json",
    "PART_CCCCXVI_protection_selection_ledger_results.json",
    "PART_CCCCXVII_qec_ouroboros_stabilizer_loop_results.json",
    "PART_CCCCXVII_QEC_OUROBOROS_STABILIZER_LOOP.md",
    "PART_CCCCXVIII_photonic_harmonic_tqc_bus_results.json",
    "PART_CCCCXVIII_PHOTONIC_HARMONIC_TQC_BUS.md",
    "PART_CCCCXXV_theta_u5_stabilizer_completion_results.json",
    "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json",
    "PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.md",
    "PART_CCCCXXX_cyclic_cayley_obstruction_results.json",
    "PART_CCCCXXX_CYCLIC_CAYLEY_OBSTRUCTION.md",
    "PART_CCCXII_EQUITABLE_PARTITION_BRIDGE.md",
    "PART_DCCCLXXII_W33_FOR_EVERYONE_QEC_OUROBOROS_BRIDGE.md",
    "PART_DCCXVI_AXIS_SYNDROME_SELECTOR_CODEC_BRIDGE.md",
    "PART_DCLXV_HOLONOMY_SCREEN_UNIVERSALITY_BRIDGE.md",
    "PART_DCLXVI_HOLONOMY_SCREEN_OPERATOR_BRIDGE.md",
    "PART_DCMI_SUB_DISTINCTION_BOUNDARY_AUDIT.md",
    "PART_DCMII_projective_screen_bulk_qec_bridge_results.json",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def copy_artifact(name: str) -> dict[str, Any]:
    src = PARTS / name
    dst = ROOT / name
    if not src.exists():
        return {"name": name, "source": str(src), "copied": False, "missing": True}
    before = dst.read_bytes() if dst.exists() else None
    shutil.copyfile(src, dst)
    after = dst.read_bytes()
    return {
        "name": name,
        "source": str(src.relative_to(ROOT)),
        "target": name,
        "copied": before != after,
        "missing": False,
        "bytes": len(after),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def regenerate_live_artifacts() -> dict[str, Any]:
    regenerated: dict[str, Any] = {}

    ccccvi = load_module(
        "bt1494_ccccvi",
        ROOT / "exploration" / "PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER.py",
    ).build_results()
    write_json(
        ROOT / "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json", ccccvi
    )
    regenerated["PART_CCCCVI"] = {
        "verified": ccccvi["verified"],
        "checks_passed": ccccvi["checks_passed"],
        "checks_total": ccccvi["checks_total"],
    }

    ccccxviii = load_module(
        "bt1494_ccccxviii",
        ROOT / "exploration" / "PART_CCCCXVIII_PHOTONIC_HARMONIC_TQC_BUS.py",
    ).build_results()
    write_json(
        ROOT / "PART_CCCCXVIII_photonic_harmonic_tqc_bus_results.json", ccccxviii
    )
    regenerated["PART_CCCCXVIII"] = {
        "verified": ccccxviii["verified"],
        "checks_passed": ccccxviii["checks_passed"],
        "checks_total": ccccxviii["checks_total"],
    }

    ccccxxvi = load_module(
        "bt1494_ccccxxvi",
        ROOT / "exploration" / "PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.py",
    ).build_results()
    write_json(
        ROOT / "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json", ccccxxvi
    )
    regenerated["PART_CCCCXXVI"] = {
        "verified": ccccxxvi["verified"],
        "checks_passed": ccccxxvi["checks_passed"],
        "checks_total": ccccxxvi["checks_total"],
    }

    dcmii_module = load_module(
        "bt1494_dcmii", ROOT / "verify_dcmii_projective_screen_bulk_qec_bridge.py"
    )
    dcmii_payload = dcmii_module.build_bridge()
    dcmii_module.write_bridge()
    regenerated["PART_DCMII"] = {
        "verified": dcmii_payload["summary"]["all_identities_hold"],
        "anchors_present": all(dcmii_payload["anchors"].values()),
    }

    return regenerated


def main() -> None:
    copy_results = [copy_artifact(name) for name in REQUIRED_ARTIFACTS]
    regenerated = regenerate_live_artifacts()
    missing_after = [name for name in REQUIRED_ARTIFACTS if not (ROOT / name).exists()]
    json_artifacts = [
        name for name in REQUIRED_ARTIFACTS if name.endswith("_results.json")
    ]
    loaded_json = {
        name: json.loads((ROOT / name).read_text(encoding="utf-8"))
        for name in json_artifacts
    }
    verified_json = {}
    for name, payload in loaded_json.items():
        if payload.get("verified") is True:
            verified_json[name] = True
        elif isinstance(payload.get("status"), str):
            verified_json[name] = payload["status"].startswith("VERIFIED")
        else:
            verified_json[name] = False

    checks = {
        "all_required_sources_exist": all(not row["missing"] for row in copy_results),
        "all_required_root_targets_exist": not missing_after,
        "live_generators_regenerated": all(
            value.get("verified") is True for value in regenerated.values()
        ),
        "ccccvi_current": regenerated["PART_CCCCVI"]["checks_passed"]
        == regenerated["PART_CCCCVI"]["checks_total"]
        >= 31,
        "ccccxviii_current": regenerated["PART_CCCCXVIII"]["checks_passed"]
        == regenerated["PART_CCCCXVIII"]["checks_total"]
        == 36,
        "ccccxxvi_current": regenerated["PART_CCCCXXVI"]["checks_passed"]
        == regenerated["PART_CCCCXXVI"]["checks_total"]
        == 29,
        "dcmii_anchors_present": regenerated["PART_DCMII"]["anchors_present"] is True,
        "json_artifacts_load": all(
            isinstance(payload, dict) for payload in loaded_json.values()
        ),
        "key_json_artifacts_verified": all(
            verified_json[name]
            for name in [
                "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json",
                "PART_CCCCXVIII_photonic_harmonic_tqc_bus_results.json",
                "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json",
            ]
        ),
    }

    result = {
        "bt": 1494,
        "title": "Photonic-QEC legacy artifact release-lock repair",
        "verified": all(checks.values()),
        "required_artifacts": REQUIRED_ARTIFACTS,
        "copied": copy_results,
        "regenerated": regenerated,
        "missing_after": missing_after,
        "verified_json": verified_json,
        "interpretation": (
            "The broad photonic-qec gate expected legacy PART artifacts at the "
            "repo root, while the preserved copies lived under manuscripts/parts. "
            "BT1494 restores those root release-lock targets and regenerates the "
            "live scheduler, harmonic bus, fusion splice, and DCMII bridge JSONs."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1494,
                "verified": result["verified"],
                "required_artifacts": len(REQUIRED_ARTIFACTS),
                "missing_after": len(missing_after),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
