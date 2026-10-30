#!/usr/bin/env python3
"""Copy top z3 candidate artifacts into committed_artifacts and optionally commit/push.

Usage:
  python scripts/_tmp_register_z3_candidate.py --index 1 --commit --push
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

CHECKS = Path.cwd() / "checks"
ART = Path.cwd() / "committed_artifacts"

# safe json dump
try:
    from utils.json_safe import dump_json
except Exception:
    import sys
    from pathlib import Path as _Path

    sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
    from utils.json_safe import dump_json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--index", type=int, default=1, help="Candidate index to register (1-based)"
)
parser.add_argument("--commit", action="store_true", help="Commit artifacts to git")
parser.add_argument(
    "--push",
    action="store_true",
    help="Push commits to origin (subject to safety check)",
)
args = parser.parse_args()

# find latest z3 analysis summary
files = sorted(
    glob.glob(str(CHECKS / "z3_analysis_*" / "summary.json")), key=os.path.getmtime
)
if not files:
    raise FileNotFoundError("No z3_analysis summary found in checks/")
summary = files[-1]
base_dir = Path(summary).parent
with open(summary, "r", encoding="utf-8") as f:
    s = json.load(f)

idx = args.index
cand = s["results"][idx - 1]
# copy NPZ artifact
src_npz = base_dir / Path(cand["artifact"]).name
ts = int(time.time())
npz_name = f"PART_CVII_z3_candidate_{ts}_{idx:02d}.npz"
json_name = f"PART_CVII_z3_candidate_{ts}_{idx:02d}.json"
arti_npz = ART / npz_name
arti_json = ART / json_name
shutil.copy2(src_npz, arti_npz)
# try to attach verification summary if present
ver_files = sorted(
    glob.glob(str(CHECKS / "PART_CVII_z3_verify_*.json")), key=os.path.getmtime
)
ver_meta = None
if ver_files:
    try:
        v = json.loads(open(ver_files[-1], encoding="utf-8").read())
        for r in v.get("results", []):
            if int(r.get("index")) == idx:
                ver_meta = r
                break
    except Exception:
        ver_meta = None

# try to attach conjugacy/centralizer info if present
conj_files = sorted(
    glob.glob(str(CHECKS / "PART_CVII_z3_conjugacy_*.json")), key=os.path.getmtime
)
conj_meta = None
if conj_files:
    try:
        c = json.loads(open(conj_files[-1], encoding="utf-8").read())
        for r in c.get("results", []):
            if int(r.get("index")) == idx:
                conj_meta = r
                break
    except Exception:
        conj_meta = None

meta = {
    "index": idx,
    "source_file": str(summary),
    "vertex_perm": cand["vertex_perm"],
    "counts": cand.get("counts", []),
    "R3_norm": cand.get("R3_norm"),
    "artifact": str(arti_npz.name),
    "notes": "Auto-registered z3 candidate (via _tmp_register_z3_candidate.py)",
    "timestamp": ts,
}
if ver_meta:
    # attach numeric verification fields
    meta.update(
        {
            "P_ranks": ver_meta.get("P_ranks"),
            "P_iderrs": ver_meta.get("P_iderrs"),
            "P_sum_err": ver_meta.get("P_sum_err"),
            "P_cross_norms": ver_meta.get("P_cross_norms"),
            "verified_by": str(ver_files[-1]),
        }
    )

if conj_meta:
    # attach conjugacy/centralizer fields
    meta.update(
        {
            "centralizer_size": conj_meta.get("centralizer_size"),
            "conj_class_size": conj_meta.get("conj_class_size"),
            "conj_summary": str(conj_files[-1]),
        }
    )
# write metadata via safe serializer
dump_json(meta, arti_json, indent=2)
print("Copied NPZ ->", arti_npz)
print("Wrote metadata ->", arti_json)

# optionally commit and push
if args.commit:
    commit_files = [str(arti_npz), str(arti_json)]
    print("Staging for commit:", commit_files)
    add_proc = subprocess.run(
        ["git", "add"] + commit_files,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if add_proc.returncode != 0:
        print("git add failed:", add_proc.stderr)
    else:
        commit_msg = (
            f"Auto-registered z3 candidate {idx} (R3={cand.get('R3_norm'):.2e})"
        )
        cp = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if cp.returncode != 0:
            print("git commit failed:", cp.stderr)
        else:
            print("Committed:", cp.stdout)
            if args.push:
                st = subprocess.run(
                    ["git", "status", "--porcelain"], stdout=subprocess.PIPE, text=True
                ).stdout
                if "README.md" in st or "memory.md" in st:
                    print(
                        "Detected modifications to README.md or memory.md in working tree; skipping push for safety."
                    )
                else:
                    brp = subprocess.run(
                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        stdout=subprocess.PIPE,
                        text=True,
                    )
                    branch = brp.stdout.strip()
                    p = subprocess.run(
                        ["git", "push", "origin", branch],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    if p.returncode != 0:
                        print("git push failed:", p.stderr)
                    else:
                        print("Pushed to origin:", p.stdout)

print("Done")
