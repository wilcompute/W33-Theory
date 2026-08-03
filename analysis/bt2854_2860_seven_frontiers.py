#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from itertools import product

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from bt2854_2860_common import encode_affine, decode_affine
from bt2854_polarization_groupoid import pass2854
from bt2855_boolean_harmonic_terwilliger import pass2855
from bt2856_codec_silicon_comparison import pass2856
from bt2857_selector_tomotope_fusion import pass2857
from bt2858_quantum_support_coarse_graining import pass2858
from bt2859_q_hadamard_butterfly import pass2859
from bt2860_support_green_first_passage import pass2860

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data"


def build_all() -> dict:
    packets = [pass2854(), pass2855(), pass2856(), pass2857(), pass2858(), pass2859(), pass2860()]
    total = sum(p["check_count"] for p in packets)
    aggregate_checks = {
        "seven_packets": len(packets) == 7,
        "all_packets_complete_or_bounded": all("COMPLETE" in p["status"] for p in packets),
        "all_checks_pass": all(all(bool(v) for v in p["checks"].values()) for p in packets),
        "total_exact_checks": total == 68,
        "pass_range_2854_2860": [int(p["schema"].split("pass")[1].split(".")[0]) for p in packets] == list(range(2854, 2861)),
    }
    assert all(aggregate_checks.values()), (total, aggregate_checks)
    return {
        "schema": "w33.pass2854_2860.seven_frontiers.v1",
        "status": "COMPLETE_68_EXACT_CHECKS_NEW_CODEC_PNR_PENDING",
        "canonical_pass_range": "2854-2860",
        "headline": "The support program closes at three deeper levels: S4 is a polarization groupoid rather than a fixed-form symmetry; the shell is a punctured Boolean/Terwilliger module and q-Hadamard transform; deterministic and noisy quantum coarse-grainings are classified exactly; and the complete Green function is closed.",
        "packets": packets,
        "total_exact_checks": total,
        "checks": aggregate_checks,
        "check_count": len(aggregate_checks),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verify-frozen", action="store_true")
    args = parser.parse_args()
    result = build_all()
    names = {
        "2854": "PART_BT2854_POLARIZATION_GROUPOID_results.json",
        "2855": "PART_BT2855_BOOLEAN_HARMONIC_TERWILLIGER_results.json",
        "2856": "PART_BT2856_CODEC_SILICON_COMPARISON_results.json",
        "2857": "PART_BT2857_SELECTOR_TOMOTOPE_FUSION_results.json",
        "2858": "PART_BT2858_QUANTUM_SUPPORT_COARSE_GRAINING_results.json",
        "2859": "PART_BT2859_Q_HADAMARD_BUTTERFLY_results.json",
        "2860": "PART_BT2860_SUPPORT_GREEN_FIRST_PASSAGE_results.json",
    }
    rendered = {}
    for packet in result["packets"]:
        passnum = packet["schema"].split("pass")[1].split(".")[0]
        rendered[OUTDIR / names[passnum]] = json.dumps(packet, indent=2, sort_keys=True) + "\n"
    aggregate_path = OUTDIR / "PART_BT2854_BT2860_SEVEN_FRONTIERS_results.json"
    rendered[aggregate_path] = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    if args.write:
        OUTDIR.mkdir(exist_ok=True)
        for path, text in rendered.items():
            path.write_text(text, encoding="utf-8")
    if args.verify_frozen:
        expected = rendered[aggregate_path]
        if aggregate_path.read_text(encoding="utf-8") != expected:
            raise SystemExit(f"frozen certificate drift: {aggregate_path}")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
