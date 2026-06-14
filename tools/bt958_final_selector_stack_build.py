#!/usr/bin/env python3
"""BT958 - final selector theorem stack build helper.

Applies the corrected W33/Holonet routing after BT957:
  - w33_paper.tex receives BT942, BT952, and BT957 theorem inserts.
  - photonic_holonet.tex receives a concise pointer to the final selector theorem.
Then attempts a two-pass pdflatex build of w33_paper.tex and photonic_holonet.tex
when run in a full checkout.
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt958_final_selector_stack_build_manifest.json"


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout_tail": p.stdout[-1200:], "stderr_tail": p.stderr[-1200:]}


def main() -> None:
    records = []
    for script in [
        "tools/integrate_bt942_selector_appendix_w33.py",
        "tools/integrate_bt952_exact_selector_w33.py",
        "tools/integrate_bt957_final_selector_w33.py",
        "tools/integrate_bt949_holonet_w33_crossref.py",
    ]:
        records.append(call(["python", script]))
    latex = shutil.which("pdflatex")
    if latex:
        for tex in ["w33_paper.tex", "photonic_holonet.tex"]:
            records.append(call([latex, "-interaction=nonstopmode", tex]))
            records.append(call([latex, "-interaction=nonstopmode", tex]))
    result = {
        "theorem": "BT958 final selector stack build helper",
        "w33_target": "w33_paper.tex",
        "holonet_target": "photonic_holonet.tex",
        "integrators": [
            "tools/integrate_bt942_selector_appendix_w33.py",
            "tools/integrate_bt952_exact_selector_w33.py",
            "tools/integrate_bt957_final_selector_w33.py",
            "tools/integrate_bt949_holonet_w33_crossref.py"
        ],
        "pdflatex_available": bool(latex),
        "records": records,
        "w33_pdf_sha256": sha256(ROOT / "w33_paper.pdf"),
        "holonet_pdf_sha256": sha256(ROOT / "photonic_holonet.pdf"),
        "final_selector": "[(3,68),(4,42),(38,65),(90,144)]",
        "boundary": "Run in a full checkout to patch and build both papers. The connector pass commits the build helper and theorem pointer, not root-source overwrites."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT958 wrote", OUT)

if __name__ == "__main__":
    main()
