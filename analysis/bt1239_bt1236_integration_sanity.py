#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "analysis" / "BT1236_minimal_clifford_tomography_insert.tex"
DST = ROOT / "paper" / "sections" / "sec_bt1236_minimal_clifford_word_metric.tex"
PRE = ROOT / "paper" / "w33_preprint.tex"
INTEGRATOR = ROOT / "tools" / "integrate_bt1236_insert.py"
INPUT = r"\input{sections/sec_bt1236_minimal_clifford_word_metric}"
REQUIRED_SNIPPETS = [
    "|Sp(4,3)|=51840",
    "m_{\\min}=4",
    "operatorname{diam}=14",
    "|B_4|=534",
]


def build():
    src_text = SRC.read_text(encoding="utf-8") if SRC.exists() else ""
    pre_text = PRE.read_text(encoding="utf-8") if PRE.exists() else ""
    dst_text = DST.read_text(encoding="utf-8") if DST.exists() else ""
    input_count = pre_text.count(INPUT)
    result = {
        "bt": 1239,
        "title": "BT1236 integration sanity",
        "source_insert_exists": SRC.exists(),
        "integrator_exists": INTEGRATOR.exists(),
        "paper_section_exists": DST.exists(),
        "preprint_exists": PRE.exists(),
        "preprint_input_count": input_count,
        "required_snippets_present_in_source": {s: (s in src_text) for s in REQUIRED_SNIPPETS},
        "paper_section_matches_source": (DST.exists() and src_text == dst_text),
        "input_duplicate_free": input_count <= 1,
    }
    if not result["source_insert_exists"] or not result["integrator_exists"]:
        status = "missing_prerequisite"
    elif input_count > 1:
        status = "duplicate_input_error"
    elif DST.exists() and input_count == 1 and src_text == dst_text:
        status = "integrated"
    else:
        status = "ready_to_integrate"
    result["status"] = status
    result["run_command"] = "python tools/integrate_bt1236_insert.py"
    result["pass"] = status in ["integrated", "ready_to_integrate"] and all(result["required_snippets_present_in_source"].values())
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1239_bt1236_integration_sanity_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1239, "status": result["status"], "pass": result["pass"], "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
