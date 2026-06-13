#!/usr/bin/env python3
"""BT908 - Photonic Holonet PDF release artifact protocol.

Builds a release-grade PDF manifest. By default it runs the BT905 CI with
--compile, then hashes photonic_holonet.tex and photonic_holonet.pdf, checks
that the PDF is not older than the TeX source, and records page count.
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEX=ROOT/"photonic_holonet.tex"
PDF=ROOT/"photonic_holonet.pdf"
OUT=ROOT/"data/PART_BT908_HOLONET_PDF_RELEASE_PROTOCOL_results.json"
DIST=ROOT/"dist/photonic_holonet_release_manifest.json"

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def page_count(path:Path)->int:
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        return -1

def run(cmd:list[str])->dict:
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    return {"cmd":cmd,"returncode":p.returncode,"stdout_tail":p.stdout[-1600:],"stderr_tail":p.stderr[-1600:]}

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--skip-build",action="store_true",help="do not run BT905 --compile before hashing")
    args=ap.parse_args()
    steps=[]
    if not args.skip_build:
        steps.append(run([sys.executable,"tools/run_bt905_holonet_profile_ci.py","--compile"]))
        if steps[-1]["returncode"]!=0: raise SystemExit(json.dumps(steps[-1],indent=2))
    if not TEX.exists() or not PDF.exists():
        raise SystemExit("missing photonic_holonet.tex or photonic_holonet.pdf")
    stale=PDF.stat().st_mtime < TEX.stat().st_mtime
    if stale:
        raise SystemExit("stale PDF: photonic_holonet.pdf older than photonic_holonet.tex")
    result={
        "theorem":"BT908 Holonet PDF release artifact protocol",
        "timestamp_utc":dt.datetime.utcnow().isoformat(timespec="seconds")+"Z",
        "target_tex":"photonic_holonet.tex",
        "target_pdf":"photonic_holonet.pdf",
        "build_steps":steps,
        "pdf_sha256":sha(PDF),
        "tex_sha256":sha(TEX),
        "pdf_size_bytes":PDF.stat().st_size,
        "page_count":page_count(PDF),
        "stale_pdf_guard":"passed: PDF mtime >= TeX mtime",
        "checks":{"T1_pdf_exists":True,"T2_tex_exists":True,"T3_pdf_not_stale":True,"T4_sha256_recorded":True,"T5_page_count_recorded":True}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding="utf-8")
    DIST.parent.mkdir(parents=True,exist_ok=True); DIST.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("BT908 release manifest written",OUT,"and",DIST)
if __name__=="__main__": main()
