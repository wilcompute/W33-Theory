#!/usr/bin/env python3
"""BT905/BT916 - one-command Holonet profile CI guard.

Runs the Holonet profile correction stack as a local CI guard:
  1. apply BT903 root patch runner without compiling,
  2. apply BT914 dictionary/profile row patch,
  3. run BT901/BT904/BT902 profile witnesses,
  4. optionally compile photonic_holonet.tex with --compile after every patch.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_BT905_HOLONET_PROFILE_CI_results.json"


def run(cmd:list[str])->dict:
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    return {"cmd":cmd,"returncode":p.returncode,"stdout_tail":p.stdout[-1600:],"stderr_tail":p.stderr[-1600:]}


def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--compile",action="store_true",help="compile after BT903+BT914 patches and witness regeneration")
    args=ap.parse_args()
    steps=[]
    commands=[
        [sys.executable,"tools/apply_bt903_holonet_root_patch.py"],
        [sys.executable,"tools/integrate_bt914_holonet_dictionary_row.py"],
        [sys.executable,"analysis/bt901_s3_profile_basis_search.py"],
        [sys.executable,"analysis/bt904_constrained_profile_solver.py"],
        [sys.executable,"analysis/bt902_holonet_profile_cross_index.py"],
    ]
    if args.compile:
        commands += [["pdflatex","-interaction=nonstopmode","photonic_holonet.tex"],["pdflatex","-interaction=nonstopmode","photonic_holonet.tex"]]
    for cmd in commands:
        steps.append(run(cmd))
        if steps[-1]["returncode"]!=0:
            OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps({"status":"failed","failed_step":steps[-1],"steps":steps},indent=2))
            raise SystemExit(json.dumps(steps[-1],indent=2))
    compile_possible=shutil.which("pdflatex") is not None
    result={
        "theorem":"BT905/BT916 Holonet profile CI guard",
        "target":"photonic_holonet.tex",
        "one_command":"python tools/run_bt905_holonet_profile_ci.py --compile",
        "compile_requested":args.compile,
        "pdflatex_available":compile_possible,
        "steps":steps,
        "guard_conclusion":"BT916 extends BT905 so the release path applies BT914 dictionary/profile row before any compile/hash step.",
        "checks":{"T1_BT903_patch_runner_passed":True,"T2_BT914_dictionary_patch_passed":True,"T3_BT901_profile_basis_passed":True,"T4_BT904_constrained_solver_passed":True,"T5_BT902_cross_index_regenerated":True}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2))
    print("BT905/BT916 Holonet profile CI passed; wrote",OUT)
if __name__=="__main__": main()
