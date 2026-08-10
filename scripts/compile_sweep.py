#!/usr/bin/env python3
"""Compile every standalone manuscript and report which ones cannot build.  Pass 4707.

WHY THIS EXISTS
---------------
`single_photon_universal_computation.tex` could not compile at all.  Line 49 carried
`PASS1150_SHIFTED_ADJACENCY_RETRACTION` inside `\\textbf{}` with bare underscores, which
LaTeX reads as math subscripts -- "Missing $ inserted", build halts, no PDF.  The document
sat in the repository root, linked from the README, with no producible PDF, and nothing
reported it.  It was found by accident while editing an unrelated paragraph.

A repository that ships PDFs needs to know which of its sources still build.  The failure
mode is silent by construction: nobody notices a missing PDF when a stale one is committed
next to it.

WHAT IT DOES
------------
Finds every .tex with a `\\documentclass` (the standalone ones -- `*_body.tex` and the
`manuscripts/tex/part*.tex` fragments are includes and are skipped), compiles each in a
scratch directory so the tree is untouched, and reports pass/fail with the first error line.

    py -3 scripts/compile_sweep.py [--jobs N]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TECTONIC = Path("C:/Users/wiljd/tools/tectonic/tectonic.exe")
# Fontconfig writes "Fontconfig error: Cannot load default config file" to stderr on every
# run in this environment. The first version of this script reported that as the compile
# error for ten manuscripts -- ten false failures, and it would have been the headline.
ERR = re.compile(r"^error: ([^\n]+)", re.M)
NOISE = re.compile(r"Fontconfig|^warning:", re.M)


def standalone_tex():
    """Standalone documents only: *_body.tex and *_sections.tex are includes."""
    out = []
    for p in sorted(ROOT.glob("*.tex")):
        if p.stem.endswith("_body") or p.stem.endswith("_sections"):
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        live = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("%"))
        if "\\documentclass" in live and "\\begin{document}" in live:
            out.append(p)
    return out


def compile_one(p: Path):
    tmp = Path(tempfile.mkdtemp(prefix="sweep_"))
    try:
        # copy the source plus anything it might \input from the root
        shutil.copy2(p, tmp / p.name)
        for extra in list(ROOT.glob("*_body.tex")) + list(ROOT.glob("*.sty")) + \
                list(ROOT.glob("*.bib")) + list(ROOT.glob("*.cls")):
            shutil.copy2(extra, tmp / extra.name)
        for d in ("manuscripts", "figures", "img"):
            src = ROOT / d
            if src.is_dir():
                shutil.copytree(src, tmp / d, dirs_exist_ok=True)
        r = subprocess.run([str(TECTONIC), "-X", "compile", p.name],
                           cwd=tmp, capture_output=True, text=True, timeout=900)
        pdf = tmp / (p.stem + ".pdf")
        ok = r.returncode == 0 and pdf.exists()
        msg = ""
        if not ok:
            clean = "\n".join(l for l in (r.stderr or "").splitlines()
                              if not NOISE.search(l))
            m = ERR.findall(clean)
            msg = next((x for x in m if "halted" not in x), (m[0] if m else "unknown"))
        size = pdf.stat().st_size if pdf.exists() else 0
        return {"file": p.name, "ok": bool(ok), "pdf_bytes": size, "error": msg[:150]}
    except subprocess.TimeoutExpired:
        return {"file": p.name, "ok": False, "pdf_bytes": 0, "error": "TIMEOUT >900s"}
    except Exception as e:
        return {"file": p.name, "ok": False, "pdf_bytes": 0,
                "error": f"{type(e).__name__}: {e}"[:150]}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    if not TECTONIC.exists():
        print(f"  tectonic not found at {TECTONIC}")
        return 1
    files = standalone_tex()
    print(f"  {len(files)} standalone manuscripts (have \\documentclass)\n")
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = list(ex.map(compile_one, files))
    bad = [r for r in results if not r["ok"]]
    for r in sorted(results, key=lambda x: (x["ok"], x["file"])):
        flag = "OK  " if r["ok"] else "FAIL"
        extra = f"{r['pdf_bytes']:>9,d} B" if r["ok"] else r["error"]
        print(f"  {flag} {r['file'][:46]:46s} {extra}")
    print(f"\n  {len(results) - len(bad)}/{len(results)} build, {len(bad)} fail")
    (ROOT / "data" / "w33_compile_sweep.json").write_text(
        json.dumps({"results": results, "failing": len(bad)}, indent=2) + "\n",
        encoding="utf-8")
    print("  wrote data/w33_compile_sweep.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
