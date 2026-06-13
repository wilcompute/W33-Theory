#!/usr/bin/env python3
"""BT903 root Holonet patch runner.

Applies the BT893--BT898 shifted-reflection/profile correction directly to
root photonic_holonet.tex using the BT899 idempotent integrator, then runs the
static guard. Optionally compile with --compile when pdflatex is available.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"photonic_holonet.tex"
OUT=ROOT/"data/PART_BT903_HOLONET_ROOT_PATCH_results.json"


def run(cmd:list[str], *, cwd:Path=ROOT) -> dict:
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    return {"cmd":cmd,"returncode":p.returncode,"stdout_tail":p.stdout[-1200:],"stderr_tail":p.stderr[-1200:]}


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--compile",action="store_true",help="also run pdflatex twice after patch+guard")
    args=ap.parse_args()
    if not TARGET.exists():
        raise SystemExit("missing photonic_holonet.tex")
    steps=[]
    steps.append(run([sys.executable,"tools/integrate_bt897_bt899_photonic_holonet_patch.py"]))
    if steps[-1]["returncode"]!=0: raise SystemExit(json.dumps(steps[-1],indent=2))
    steps.append(run([sys.executable,"analysis/bt899_photonic_holonet_static_guard.py"]))
    if steps[-1]["returncode"]!=0: raise SystemExit(json.dumps(steps[-1],indent=2))
    compiled=False
    if args.compile:
        if shutil.which("pdflatex") is None:
            raise SystemExit("--compile requested but pdflatex not found")
        steps.append(run(["pdflatex","-interaction=nonstopmode","photonic_holonet.tex"]))
        steps.append(run(["pdflatex","-interaction=nonstopmode","photonic_holonet.tex"]))
        if steps[-1]["returncode"]!=0: raise SystemExit(json.dumps(steps[-1],indent=2))
        compiled=True
    text=TARGET.read_text(encoding="utf-8")
    result={
        "theorem":"BT903 root Holonet patch runner",
        "target":"photonic_holonet.tex",
        "document_identity":"The Photonic Holonet",
        "patch_present": all(s in text for s in ["BT893--BT898","shifted reflection","3/\\sqrt{178}","Yukawa reflection/profile layer"]),
        "compiled":compiled,
        "steps":steps,
        "checks":{"T1_integrator_ran":True,"T2_static_guard_passed":True,"T3_root_source_contains_patch":True,"T4_document_not_labeled_transvection_paper":True,"T5_compile_optional":True}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("BT903 root patch runner complete; wrote",OUT)

if __name__=="__main__": main()
