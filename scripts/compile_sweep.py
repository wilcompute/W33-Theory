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


INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")


def standalone_tex():
    r"""Root .tex files that nothing else \input.

    THE FIRST TWO VERSIONS OF THIS FUNCTION BOTH SKIPPED THE THREE MAIN MANUSCRIPTS.
    They looked for \documentclass and \begin{document} in the file itself, and excluded
    *_body.tex as "obviously an include". That is backwards here: holonet_machine_blueprint,
    photonic_holonet and w33_paper are WRAPPERS -- they set up macros and \input a body, and
    the body is where \documentclass lives. So the wrapper failed the content test, the body
    failed the name test, and the repository's three largest documents were swept by nothing
    while the sweep reported 20/20 and was wired into CI.

    NEITHER TEST ALONE IS ENOUGH, and the third version learned that too. "Not included by
    anything" alone sweeps in orphan fragments -- section2_uniqueness.tex, the supplements,
    the inserts -- which open with \section and were never documents. "Has \documentclass"
    alone misses the wrappers. A standalone document is a file that nothing includes AND
    from which a \documentclass is reachable, in itself or through its include chain.
    """
    roots = sorted(ROOT.glob("*.tex"))

    def live_text(p):
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""
        return "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("%"))

    included = set()
    for p in roots:
        for tgt in INPUT_RE.findall(live_text(p)):
            name = tgt.split("/")[-1]
            included.add(name if name.endswith(".tex") else name + ".tex")

    def reaches_documentclass(p, depth=0):
        if depth > 4:
            return False
        t = live_text(p)
        if "\\documentclass" in t:
            return True
        for tgt in INPUT_RE.findall(t):
            name = tgt.split("/")[-1]
            name = name if name.endswith(".tex") else name + ".tex"
            child = ROOT / name
            if child.is_file() and reaches_documentclass(child, depth + 1):
                return True
        return False

    return [p for p in roots
            if p.name not in included and reaches_documentclass(p)]


def compile_one(p: Path):
    # Compile IN THE REPO ROOT with --outdir, not in a copied tree.
    #
    # The first version copied the source into a scratch directory along with a guessed list
    # of dependencies, and guessed wrong: it did not copy analysis/*.tex or root *.png, so
    # three manuscripts were reported as missing files that are present and tracked. Between
    # that and the Fontconfig noise, this script produced false failures twice before it
    # produced a true one. Relative \input and \includegraphics paths are resolved against
    # the source's directory, so the only way to be sure they resolve is to be there.
    tmp = Path(tempfile.mkdtemp(prefix="sweep_"))
    try:
        r = subprocess.run([str(TECTONIC), "-X", "compile", p.name,
                            "--outdir", str(tmp)],
                           cwd=ROOT, capture_output=True, text=True, timeout=900)
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
