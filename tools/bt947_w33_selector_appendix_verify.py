#!/usr/bin/env python3
"""BT947 - verify the E8 selector appendix against w33_paper.tex.

Correct target routing:
  - photonic_holonet.tex is the current main narrative / architecture paper.
  - w33_paper.tex is the heavy-math manuscript.

This helper applies tools/integrate_bt942_selector_appendix_w33.py and then
attempts a two-pass pdflatex build of w33_paper.tex in a full local checkout.
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt947_w33_selector_appendix_verify_manifest.json"


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout_tail": p.stdout[-1200:], "stderr_tail": p.stderr[-1200:]}


def main() -> None:
    records = [call(["python", "tools/integrate_bt942_selector_appendix_w33.py"])]
    latex = shutil.which("pdflatex")
    if latex:
        records.append(call([latex, "-interaction=nonstopmode", "w33_paper.tex"]))
        records.append(call([latex, "-interaction=nonstopmode", "w33_paper.tex"]))
    pdf = ROOT / "w33_paper.pdf"
    result = {
        "theorem": "BT947 w33 selector appendix verification helper",
        "target": "w33_paper.tex",
        "appendix_source": "paper/BT942_e8_selector_appendix.tex",
        "integrator": "tools/integrate_bt942_selector_appendix_w33.py",
        "pdflatex_available": bool(latex),
        "records": records,
        "pdf_exists": pdf.exists(),
        "pdf_sha256": sha256(pdf),
        "routing": "Heavy E8/SNF/symplectic selector math belongs in w33_paper.tex; photonic_holonet.tex remains the narrative/architecture paper.",
        "boundary": "Run this helper in a full local checkout to patch and compile the actual heavy-math manuscript. The connector pass commits the helper and manifest schema."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT947 manifest", OUT)

if __name__ == "__main__":
    main()
