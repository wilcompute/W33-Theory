#!/usr/bin/env python3
"""BT1832: Holonet machine TeX build-check witness.

This is a lightweight static build gate for the patched holonet_machine.tex. It
checks that the inserted compiled-runtime-stack result and the aperture honest
boundary are present, and that basic LaTeX delimiters balance. A full PDF build
should still be run in CI or a local TeX environment.
"""
from __future__ import annotations

import json
from pathlib import Path

TEX = Path("holonet_machine.tex")
OUT = Path("data/PART_BT1832_TEX_BUILD_CHECK_results.json")


def theorem_summary():
    text = TEX.read_text(encoding="utf-8")
    checks = {
        "has_compiled_runtime_stack_result": "Compiled defect runtime stack" in text,
        "has_selector_formula": "table}[(p,q)][c(p,q)" in text,
        "has_aperture_honest_boundary": "aperture shot table is a readout scaffold, not data" in text,
        "begin_end_document_balanced": text.count("\\begin{document}") == text.count("\\end{document}") == 1,
        "result_environments_balanced": text.count("\\begin{result}") == text.count("\\end{result}"),
        "honestbox_balanced": text.count("\\begin{honestbox}") == text.count("\\end{honestbox}"),
        "display_math_delimiters_even": text.count("\\[") == text.count("\\]")
    }
    return {
        "theorem": "BT1832 Holonet machine TeX build-check witness",
        "target": str(TEX),
        "checks": checks,
        "all_static_checks_pass": all(checks.values()),
        "honest_scope": "Static TeX sanity check only. It is not a full pdflatex build."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_static_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
