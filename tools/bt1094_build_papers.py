#!/usr/bin/env python3
"""BT1100 paper build handoff.

Runs the no-network sanity check, then the latest cumulative integration helper,
and finally tries to compile/check the W33 preprint and photonic holonet sources.
The script is safe to run repeatedly.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], cwd: Path) -> None:
    print(f"[bt1100] cwd={cwd} :: {' '.join(cmd)}")
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
    run(["python", "tools/bt1100_tex_path_sanity.py"], ROOT)
    run(["python", "tools/bt1100_integrate_all_latest_sections.py"], ROOT)
    compile_tex("w33_preprint.tex", ROOT / "paper")
    compile_tex("photonic_holonet.tex", ROOT)


if __name__ == "__main__":
    main()
