#!/usr/bin/env python3
"""BT578: lightweight build harness for paper/w33_preprint.tex.

Default behavior runs static checks only.  With --compile, the harness tries to
call latexmk first, then pdflatex if available.  This keeps CI/repo use safe on
machines without a TeX toolchain while still making a local PDF build one command.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper" / "w33_preprint.tex"
CHECKER = ROOT / "analysis" / "bt574_latex_sanity_verifier.py"


def run(cmd, cwd=ROOT):
    print("$", " ".join(str(x) for x in cmd))
    return subprocess.run(cmd, cwd=cwd, text=True)


def static_check():
    if not TEX.exists():
        print(f"missing target: {TEX}", file=sys.stderr)
        return 2
    if CHECKER.exists():
        rc = run([sys.executable, str(CHECKER)]).returncode
        if rc != 0:
            return rc
    text = TEX.read_text(encoding="utf-8")
    required = [
        "\\documentclass",
        "\\begin{document}",
        "\\end{document}",
        "Symmetry, Phase, and Cubic Leakage",
    ]
    missing = [x for x in required if x not in text]
    if missing:
        print("missing required tokens:", missing, file=sys.stderr)
        return 3
    print("static checks passed")
    return 0


def compile_pdf():
    if shutil.which("latexmk"):
        return run(["latexmk", "-pdf", "-interaction=nonstopmode", "w33_preprint.tex"], cwd=TEX.parent).returncode
    if shutil.which("pdflatex"):
        rc = run(["pdflatex", "-interaction=nonstopmode", "w33_preprint.tex"], cwd=TEX.parent).returncode
        if rc == 0:
            rc = run(["pdflatex", "-interaction=nonstopmode", "w33_preprint.tex"], cwd=TEX.parent).returncode
        return rc
    print("No TeX compiler found. Install latexmk or pdflatex, then rerun with --compile.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true", help="attempt PDF compilation after static checks")
    args = ap.parse_args()
    rc = static_check()
    if rc != 0:
        return rc
    if args.compile:
        return compile_pdf()
    print("Static-only mode complete. Use --compile to attempt local PDF build.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
