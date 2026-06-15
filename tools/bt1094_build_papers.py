#!/usr/bin/env python3
"""BT1097 paper build handoff.

Runs the latest cumulative integration helper and then tries to compile/check
the W33 preprint and photonic holonet sources.  The script is safe to run repeatedly.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path) -> None:
    print(f"[bt1097] cwd={cwd} :: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd), check=True)


def compile_tex(tex: str, cwd: Path) -> None:
    if shutil.which("latexmk"):
        run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex], cwd)
        return
    engine = shutil.which("pdflatex")
    if not engine:
        raise SystemExit("No latexmk or pdflatex found. Install TeX Live/MacTeX first.")
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex], cwd)
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex], cwd)


def main() -> None:
    run(["python", "tools/bt1097_integrate_all_latest_sections.py"], ROOT)
    compile_tex("w33_preprint.tex", ROOT / "paper")
    compile_tex("photonic_holonet.tex", ROOT)


if __name__ == "__main__":
    main()
