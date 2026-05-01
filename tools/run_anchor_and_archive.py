#!/usr/bin/env python3
"""Wrapper: run `anchor_core_and_maximize_cpsat.py` with a given forbid, then archive results.

Usage: python tools/run_anchor_and_archive.py --forbid 0-18-25 --time 300

It will:
 - run tools/anchor_core_and_maximize_cpsat.py with the provided forbid and time
 - copy artifacts/anchor_core_cpsat_summary.json to artifacts/anchor_core_cpsat_summary_forbid_<forbid>.json
 - write anchor-forbid reports summarizing per-W status
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
REPORTS = ROOT / "reports"

parser = argparse.ArgumentParser()
parser.add_argument(
    "--forbid",
    type=str,
    required=False,
    default=None,
    help="Comma-separated E6 triads like '0-18-25' to forbid; if omitted, uses config/canonical_forbid.json",
)
parser.add_argument("--time", type=int, default=300)
parser.add_argument("--w-list", type=str, default="0,4,5,6,7,8,9,10,11,12,13,14,15")
parser.add_argument("--workers", type=int, default=4)
parser.add_argument(
    "--reports-dir",
    type=Path,
    default=REPORTS,
    help="Directory to write anchor-forbid reports (defaults to repo reports/).",
)
args = parser.parse_args()

# Resolve forbid: prefer explicit argument, otherwise fall back to config file
forbid = args.forbid
if forbid is None:
    cfg = ROOT / "config" / "canonical_forbid.json"
    if cfg.exists():
        try:
            cfgj = json.loads(cfg.read_text(encoding="utf-8"))
            cf = cfgj.get("canonical_forbid")
            if cf and isinstance(cf, (list, tuple)) and len(cf) == 3:
                forbid = "-".join(map(str, cf))
                print(f"No --forbid given; using canonical forbid from {cfg}: {forbid}")
            else:
                raise RuntimeError(
                    "config/canonical_forbid.json missing 'canonical_forbid' entry or invalid"
                )
        except Exception as e:
            raise RuntimeError(f"Failed to read canonical forbid config: {e}")
    else:
        raise RuntimeError(
            "No --forbid provided and config/canonical_forbid.json not found"
        )
# run anchored script
cmd = [
    sys.executable,
    str(ROOT / "tools" / "anchor_core_and_maximize_cpsat.py"),
    "--forbid",
    forbid,
    "--time",
    str(args.time),
    "--w-list",
    args.w_list,
    "--workers",
    str(args.workers),
]
print("Running:", " ".join(cmd))
proc = subprocess.run(cmd)
if proc.returncode != 0:
    print("Anchor run failed with returncode", proc.returncode)

# archive summary
src = ART / "anchor_core_cpsat_summary.json"
dst = ART / f"anchor_core_cpsat_summary_forbid_{forbid.replace(',','_')}.json"
shutil.copyfile(src, dst)
print("Copied summary to", dst)

# read summary and write reports
data = json.loads(src.read_text(encoding="utf-8"))
reports_dir = Path(args.reports_dir)
reports_dir.mkdir(parents=True, exist_ok=True)
md = reports_dir / f"anchor_forbid_{forbid.replace(',','_')}.md"
js = reports_dir / f"anchor_forbid_{forbid.replace(',','_')}.json"
lines = [f"# Anchor CP-SAT summary (forbid: {forbid})", ""]
for e in data:
    lines.append(
        f"- W={e.get('W_idx')}: status={e.get('status')}, matched={e.get('matched')}"
    )
md.write_text("\n".join(lines), encoding="utf-8")
js.write_text(json.dumps(data, indent=2), encoding="utf-8")
print("Wrote reports:", md, js)
