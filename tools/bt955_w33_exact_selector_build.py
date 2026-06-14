#!/usr/bin/env python3
"""BT955 - integrate exact selector theorem into w33_paper.tex and build.

Runs the corrected W33 integrations:
  1. BT942 appendix into w33_paper.tex.
  2. BT952 exact support-60 theorem into w33_paper.tex.
Then attempts a two-pass pdflatex build when run in a full local checkout.
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt955_w33_exact_selector_build_manifest.json"


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout_tail": p.stdout[-1200:], "stderr_tail": p.stderr[-1200:]}


def main() -> None:
    records = []
    records.append(call(["python", "tools/integrate_bt942_selector_appendix_w33.py"]))
    records.append(call(["python", "tools/integrate_bt952_exact_selector_w33.py"]))
    latex = shutil.which("pdflatex")
    if latex:
        records.append(call([latex, "-interaction=nonstopmode", "w33_paper.tex"]))
        records.append(call([latex, "-interaction=nonstopmode", "w33_paper.tex"]))
    pdf = ROOT / "w33_paper.pdf"
    result = {
        "theorem": "BT955 w33 exact selector build helper",
        "target": "w33_paper.tex",
        "integrators": ["tools/integrate_bt942_selector_appendix_w33.py", "tools/integrate_bt952_exact_selector_w33.py"],
        "pdflatex_available": bool(latex),
        "records": records,
        "pdf_exists": pdf.exists(),
        "pdf_sha256": sha256(pdf),
        "status_boundary": "Run in a full local checkout to patch and compile the actual heavy-math manuscript. The connector pass commits the helper and a manifest template, not a root-source overwrite."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT955 wrote", OUT)

if __name__ == "__main__":
    main()
