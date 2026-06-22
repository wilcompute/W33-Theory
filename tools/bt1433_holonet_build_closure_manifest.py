#!/usr/bin/env python3
"""BT1433: Holonet TeX/PDF build closure manifest.

The connector cannot safely run and inspect the whole LaTeX/PDF pipeline here,
so this verifier records the exact local build closure: run the BT1430 splicer,
compile photonic_holonet.tex, then render-inspect the new Fano bus pages.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1433_holonet_build_closure_manifest.json"
MAIN = ROOT / "photonic_holonet.tex"
SPLICER = ROOT / "tools" / "integrate_bt1430_fano_bus_holonet.py"
INSERT = ROOT / "analysis" / "BT1430_fano_bus_master_insert.tex"


def main() -> None:
    insert_text = INSERT.read_text(encoding="utf-8")
    checks = {
        "main_tex_exists": MAIN.exists(),
        "splicer_exists": SPLICER.exists(),
        "fano_insert_exists": INSERT.exists(),
        "fano_insert_has_tikz_figure": "\\begin{tikzpicture}" in insert_text and "168+24=192" in insert_text,
        "fano_insert_has_retwined_css_rule": "H_X'=H_XJ^{-1}" in insert_text and "H_Z'=H_ZJ^{-1}" in insert_text,
        "pdf_rebuild_requires_local_latex": True,
    }
    result = {
        "bt": 1433,
        "title": "Holonet TeX/PDF build closure manifest",
        "verified": all(checks.values()),
        "local_build_commands": [
            "python tools/integrate_bt1430_fano_bus_holonet.py",
            "latexmk -pdf -interaction=nonstopmode photonic_holonet.tex",
            "python /home/oai/skills/pdfs/scripts/render_pdf.py photonic_holonet.pdf --out_dir /mnt/data/_renders/holonet --dpi 200",
        ],
        "inspection_targets": [
            "Confirm BT1419-BT1421, BT1422-BT1424, BT1425-BT1427, and BT1430 inputs appear before the software section.",
            "Inspect the Fano bus figure for clipping, missing glyphs, and TikZ arrow overlap.",
            "Confirm the paper states 168=21*8, 24=S4 point stabilizer, 192=168+24, and the retwined CSS rule.",
        ],
        "connector_boundary": "The repository now contains the exact splicer, TeX insert, and build manifest. The PDF was not rebuilt inside this connector pass.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1433, "verified": result["verified"], "pdf_rebuilt_here": False}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
