#!/usr/bin/env python3
"""Pass 2840: freeze the execution-codec/M36-cost blueprint release."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "holonet_machine_blueprint.tex"
INSERT = ROOT / "analysis" / "BT2838_BT2840_blueprint_extension_insert.tex"
CODEC = ROOT / "data" / "PART_BT2838_OPTIMAL_EXECUTION_CODEC_results.json"
COST = ROOT / "data" / "PART_BT2839_M36_REPEATED_BRANCH_COST_results.json"
MAGIC = ROOT / "data" / "PART_W33_PASS2797_2799_MAGIC_ORBITS_AND_MONOTONE.json"
OBSERVER = ROOT / "data" / "PART_BT2828_DOUBLE_WORD_DISTANCE4_summary.json"
ROM = ROOT / "rtl" / "w33_pass2827_support_decoder_rom.sv"
MINIMAL_RTL = ROOT / "rtl" / "w33_pass2796_minimal_frame_engine.sv"
RESERVATION = ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2838-2840.json"
PDF = ROOT / "holonet_machine_blueprint.pdf"
LOG = ROOT / "holonet_machine_blueprint.log"
OUT = ROOT / "data" / "PART_BT2840_BLUEPRINT_EXTENSION_results.json"
INPUT = "\\input{analysis/BT2838_BT2840_blueprint_extension_insert}"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate() -> dict[str, bool]:
    tex = TEX.read_text(encoding="utf-8")
    insert = INSERT.read_text(encoding="utf-8")
    codec = load(CODEC)
    cost = load(COST)
    magic = load(MAGIC)
    observer = load(OBSERVER)
    rom = ROM.read_text(encoding="utf-8")
    minimal_rtl = MINIMAL_RTL.read_text(encoding="utf-8")
    reservation = load(RESERVATION)
    log = LOG.read_text(encoding="utf-8", errors="replace") if LOG.is_file() else ""
    return {
        "insert_exactly_once": tex.count(INPUT) == 1,
        "four_magic_classes_in_blueprint": "Clifford classes on the $36$ rays: $[4,8,12,12]$" in tex,
        "four_magic_classes_certificate": magic["pass_2797"]["class_sizes"] == [4, 8, 12, 12],
        "minimal_engine_43_lc_in_blueprint": "Minimal engine: $\\mathbf{43}$ LC" in tex,
        "minimal_engine_rtl_present": "module w33_minimal_frame_engine" in minimal_rtl,
        "deep_48_branch_theorem": "Deep grade: $48$ improving branches, $0<p<2/3$" in tex,
        "support_refinement_theorem": "16{\\to}40{\\to}78{\\to}81" in tex,
        "codec_status": codec["status"] == "COMPLETE_EXACT",
        "codec_all_checks": codec["check_count"] == 7 and all(codec["checks"].values()),
        "codec_seven_bits": codec["optimal_fixed_width_bits"] == 7,
        "codec_transition_payload": codec["transition_table_payload_bits"] == 2268,
        "rom_81_words": rom.count("valid_o = 1'b1") == 81,
        "observer_distance_profile": observer["ordered_pair_distance_profile"] == {"2": 40, "3": 16, "4": 8},
        "observer_52_4_code": observer["coding_consequence"]["trajectory_bits"] == 52 and observer["coding_consequence"]["minimum_distance"] == 4,
        "observer_all_checks": all(observer["checks"].values()),
        "cost_status": cost["status"] == "EXACT_LOCAL_ASYMPTOTIC_AND_NUMERICAL_TRAJECTORIES",
        "cost_all_checks": cost["check_count"] == 6 and all(cost["checks"].values()),
        "cost_exponent": abs(cost["repeated_branch_overhead_exponent"]["value"] - 3.4190225827029095) < 1e-15,
        "cost_boundary": "not an optimized protocol" in cost["claim_boundary"],
        "three_code_text": "Three codes have three different jobs" in insert,
        "reservation_range": reservation["range"] == "2838-2840",
        "pdf_present": PDF.is_file() and PDF.stat().st_size > 100000,
        "log_no_overfull": LOG.is_file() and "Overfull" not in log,
        "log_no_fatal_tex": LOG.is_file() and not any(token in log for token in ("Undefined control sequence", "LaTeX Error", "Emergency stop", "Fatal error")),
    }


def payload(checks: dict[str, bool]) -> dict:
    result = {
        "schema": "w33.pass2840.blueprint_extension_release.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "sha256": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (TEX, INSERT, CODEC, COST, MAGIC, OBSERVER, ROM, MINIMAL_RTL, RESERVATION)
        },
        "boundaries": {
            "seven_bit": "lossless storage optimum, not a placed-area result",
            "eight_bit": "fast selected support telemetry, not the state representation",
            "distance_four": "protected telemetry optimum only in the tested doubled-shortest family",
            "m36_cost": "one repeated branch under iid depolarizing noise, not an optimized factory",
        },
    }
    if PDF.is_file():
        result["pdf"] = {
            "sha256": sha(PDF),
            "bytes": PDF.stat().st_size,
            "log_sha256": sha(LOG) if LOG.is_file() else None,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-frozen", action="store_true")
    args = parser.parse_args()
    checks = evaluate()
    expected = json.dumps(payload(checks), indent=2, sort_keys=True) + "\n"
    if args.verify_frozen:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != expected:
            raise AssertionError("Pass 2840 certificate drift")
    else:
        OUT.write_text(expected, encoding="utf-8")
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise AssertionError(f"Pass 2840 failures: {failed}")
    print(f"PASS {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
