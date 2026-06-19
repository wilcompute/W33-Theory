#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WF = ROOT / ".github" / "workflows" / "paper-build.yml"
PRE = ROOT / "paper" / "w33_preprint.tex"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1300_paper_build_handshake_summary.json")
    ns = ap.parse_args()
    wf_text = WF.read_text(encoding="utf-8") if WF.exists() else ""
    checks = {
        "workflow_exists": WF.exists(),
        "preprint_exists": PRE.exists(),
        "paper_trigger": "paper/**" in wf_text,
        "paper_workdir": "/paper" in wf_text,
        "pdflatex_preprint": "w33_preprint.tex" in wf_text,
        "artifact_pdf": "paper/w33_preprint.pdf" in wf_text,
        "manual_dispatch": "workflow_dispatch" in wf_text
    }
    result = {
        "bt": 1300,
        "verified": all(checks.values()),
        "checks": checks,
        "workflow": ".github/workflows/paper-build.yml",
        "preprint": "paper/w33_preprint.tex",
        "artifact": "paper/w33_preprint.pdf"
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1300, "verified": result["verified"], "out": str(ns.out)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
