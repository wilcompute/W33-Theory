#!/usr/bin/env python3
"""BT979 - local build attempt probe.

Records whether the current runtime can perform the direct final paper build.
A full build requires a real checkout plus pdflatex.  This script is meant to be
run from a checkout; it records tool availability and, when possible, runs the
BT974 direct build script.
"""
from __future__ import annotations
import json, shutil, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt979_local_build_attempt_manifest.json"


def call(cmd):
    t = time.time()
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return {"cmd": cmd, "returncode": p.returncode, "elapsed_seconds": round(time.time()-t, 3), "stdout_tail": p.stdout[-1200:], "stderr_tail": p.stderr[-1200:]}


def main():
    script = ROOT / "tools/bt974_direct_final_paper_build.sh"
    result = {
        "theorem": "BT979 local final paper build attempt probe",
        "cwd": str(ROOT),
        "has_git": shutil.which("git") is not None,
        "has_pdflatex": shutil.which("pdflatex") is not None,
        "has_bt974_script": script.exists(),
        "records": [],
        "boundary": "Run from a full checkout with network/TeX access. This probe records whether the build can run in that environment."
    }
    if script.exists() and shutil.which("pdflatex"):
        result["records"].append(call(["bash", str(script)]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT979 wrote", OUT)

if __name__ == "__main__":
    main()
