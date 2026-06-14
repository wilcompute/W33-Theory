#!/usr/bin/env python3
"""BT945 selector appendix verification helper.

Applies the BT942 appendix insertion script and, when pdflatex is available in a
local checkout, builds W36_PAPER.tex twice.  The helper writes a manifest with
return codes and hashes.
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt945_selector_appendix_verify_manifest.json"


def file_hash(path: Path):
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout_tail": p.stdout[-1000:], "stderr_tail": p.stderr[-1000:]}


def main():
    records = [call(["python", "tools/integrate_bt942_selector_appendix.py"])]
    latex = shutil.which("pdflatex")
    if latex:
        records.append(call([latex, "-interaction=nonstopmode", "W36_PAPER.tex"]))
        records.append(call([latex, "-interaction=nonstopmode", "W36_PAPER.tex"]))
    pdf = ROOT / "W36_PAPER.pdf"
    result = {
        "theorem": "BT945 selector appendix verification helper",
        "target": "W36_PAPER.tex",
        "appendix_source": "paper/BT942_e8_selector_appendix.tex",
        "pdflatex_available": bool(latex),
        "records": records,
        "pdf_exists": pdf.exists(),
        "pdf_sha256": file_hash(pdf),
        "boundary": "Use this helper in a full local checkout. The chat execution also verified the appendix as a standalone one-page TeX/PDF syntax check."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT945 manifest", OUT)

if __name__ == "__main__":
    main()
