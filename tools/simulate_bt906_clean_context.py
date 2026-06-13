#!/usr/bin/env python3
"""BT906 - simulate a clean checkout for the Holonet profile CI.

This makes a temporary clean workspace containing only the root Holonet source
and the BT899/BT903/BT905/BT901/BT904/BT902 scripts, then runs the one-command
CI guard. It is a clean-context simulation for environments where a network
git clone is unavailable.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILES=[
    "photonic_holonet.tex",
    "tools/integrate_bt897_bt899_photonic_holonet_patch.py",
    "tools/apply_bt903_holonet_root_patch.py",
    "tools/run_bt905_holonet_profile_ci.py",
    "analysis/bt899_photonic_holonet_static_guard.py",
    "analysis/bt901_s3_profile_basis_search.py",
    "analysis/bt902_holonet_profile_cross_index.py",
    "analysis/bt904_constrained_profile_solver.py",
]

def run(cmd:list[str], cwd:Path)->dict:
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    return {"cmd":cmd,"returncode":p.returncode,"stdout_tail":p.stdout[-1600:],"stderr_tail":p.stderr[-1600:]}

def sha(path:Path)->str|None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--compile",action="store_true")
    ap.add_argument("--keep",action="store_true")
    args=ap.parse_args()
    tmp=Path(tempfile.mkdtemp(prefix="bt906_clean_"))
    try:
        for rel in FILES:
            src=ROOT/rel; dst=tmp/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        cmd=[sys.executable,"tools/run_bt905_holonet_profile_ci.py"] + (["--compile"] if args.compile else [])
        step=run(cmd,tmp)
        ok=step["returncode"]==0
        pdf=tmp/"photonic_holonet.pdf"
        tex=tmp/"photonic_holonet.tex"
        result={
            "theorem":"BT906 clean-context BT905 run",
            "workspace":str(tmp),
            "status":"passed" if ok else "failed",
            "command":" ".join(cmd),
            "step":step,
            "pdf_exists":pdf.exists(),
            "pdf_sha256":sha(pdf),
            "tex_sha256":sha(tex),
            "tex_patch_present": all(s in tex.read_text(encoding="utf-8") for s in ["BT893--BT898","shifted reflection","3/\\sqrt{178}","Yukawa reflection/profile layer"]),
        }
        out=ROOT/"data/PART_BT906_CLEAN_CONTEXT_BT905_RUN_results.json"
        out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2),encoding="utf-8")
        if not ok: raise SystemExit(json.dumps(result,indent=2))
        print("BT906 clean-context simulation passed; wrote",out)
    finally:
        if not args.keep:
            shutil.rmtree(tmp,ignore_errors=True)
if __name__=="__main__": main()
