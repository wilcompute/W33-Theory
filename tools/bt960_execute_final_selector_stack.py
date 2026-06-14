#!/usr/bin/env python3
"""BT970 - execute the final selector paper stack in a full checkout.

This updates the BT960 production wrapper so the BT967 selector-rail theorem and
Holonet pointer are included in the final paper-stack build path.
"""
from __future__ import annotations
import hashlib, json, shutil, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt970_final_selector_stack_execution_manifest.json"

INTEGRATORS = [
    "tools/integrate_bt942_selector_appendix_w33.py",
    "tools/integrate_bt952_exact_selector_w33.py",
    "tools/integrate_bt957_final_selector_w33.py",
    "tools/integrate_bt967_selector_rails_w33.py",
    "tools/integrate_bt949_holonet_w33_crossref.py",
    "tools/integrate_bt958_holonet_final_selector_pointer.py",
    "tools/integrate_bt967_holonet_selector_rails.py",
]
PAPERS = ["w33_paper.tex", "photonic_holonet.tex"]


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(cmd: list[str]) -> dict:
    started = time.time()
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {
        "cmd": cmd,
        "returncode": p.returncode,
        "elapsed_seconds": round(time.time() - started, 3),
        "stdout_tail": p.stdout[-1600:],
        "stderr_tail": p.stderr[-1600:],
    }


def main() -> None:
    records = [call(["python", script]) for script in INTEGRATORS]
    latex = shutil.which("pdflatex")
    if latex:
        for paper in PAPERS:
            records.append(call([latex, "-interaction=nonstopmode", paper]))
            records.append(call([latex, "-interaction=nonstopmode", paper]))
    result = {
        "theorem": "BT970 final selector and rail theorem paper-stack execution manifest",
        "integrators": INTEGRATORS,
        "papers": PAPERS,
        "pdflatex_available": bool(latex),
        "records": records,
        "pdf_hashes": {
            "w33_paper.pdf": sha256(ROOT / "w33_paper.pdf"),
            "photonic_holonet.pdf": sha256(ROOT / "photonic_holonet.pdf"),
        },
        "source_hashes": {
            "w33_paper.tex": sha256(ROOT / "w33_paper.tex"),
            "photonic_holonet.tex": sha256(ROOT / "photonic_holonet.tex"),
        },
        "final_selector": "[(3,68),(4,42),(38,65),(90,144)]",
        "selector_rail_payload": "BT967 selector rail theorem included",
        "boundary": "Run this wrapper in a full local checkout. The connector commit provides the production execution script and manifest schema.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT970 wrote", OUT)

if __name__ == "__main__":
    main()
