#!/usr/bin/env python3
"""BT905 - one-command Holonet profile CI guard.

Runs the Holonet profile correction stack as a local CI guard:
  1. apply BT903 root patch runner (which calls BT899 integrator + guard),
  2. run BT901 profile-basis search,
  3. run BT904 constrained profile solver,
  4. run BT902 cross-index generator,
  5. optionally compile photonic_holonet.tex with --compile.
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
    ap.add_argument("--compile",action="store_true",help="include pdflatex compilation through BT903")
    args=ap.parse_args()
    steps=[]
    bt903=[sys.executable,"tools/apply_bt903_holonet_root_patch.py"]
    if args.compile: bt903.append("--compile")
    for cmd in [bt903,[sys.executable,"analysis/bt901_s3_profile_basis_search.py"],[sys.executable,"analysis/bt904_constrained_profile_solver.py"],[sys.executable,"analysis/bt902_holonet_profile_cross_index.py"]]:
        steps.append(run(cmd))
        if steps[-1]["returncode"]!=0:
            OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps({"status":"failed","failed_step":steps[-1],"steps":steps},indent=2))
            raise SystemExit(json.dumps(steps[-1],indent=2))
    compile_possible=shutil.which("pdflatex") is not None
    result={
        "theorem":"BT905 Holonet profile CI guard",
        "target":"photonic_holonet.tex",
        "one_command":"python tools/run_bt905_holonet_profile_ci.py --compile",
        "compile_requested":args.compile,
        "pdflatex_available":compile_possible,
        "steps":steps,
        "guard_conclusion":"BT905 ties together root Holonet patching, static document identity guard, S3 profile equivariance, constrained 9x9 numerical scaffold, and cross-index regeneration.",
        "checks":{"T1_BT903_patch_runner_passed":True,"T2_BT901_profile_basis_passed":True,"T3_BT904_constrained_solver_passed":True,"T4_BT902_cross_index_regenerated":True,"T5_one_command_CI_available":True}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2))
    print("BT905 Holonet profile CI passed; wrote",OUT)
if __name__=="__main__": main()
