#!/usr/bin/env python3
"""Orchestrate verification for both canonical forbid rules (lex_min, max_stab).

Steps:
 - compute canonical representative for `cands` under full Aut(W33) action using
   functions from `forbid_full_aut_orbit_analysis.py` (induced perms on 27).
 - for each canonical forbid, run anchored CP-SAT (via `run_anchor_and_archive.py`)
   and then generate GF(2) certificates.
 - write an aggregated summary JSON + markdown report.

Usage: python tools/run_both_canonical_forbids.py --cands 0-18-25,0-20-23 --time 300 --w-list 0,4
"""

from __future__ import annotations

import argparse
import json
import subprocess

# Ensure repository root is on sys.path so `import tools.*` works when running as a
# top-level script (this allows running the script directly via `python tools/...`).
import sys
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
REPORTS = ROOT / "reports"
ART.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

# Import helpers from our orbit analysis module
# Prefer full Aut(W33) analysis (requires networkx), but fall back to the
# AGL(2,3)×Z3 orbit analysis if that dependency is missing.
try:
    from tools.forbid_full_aut_orbit_analysis import (
        build_schlafli_mapping,
    )
    from tools.forbid_full_aut_orbit_analysis import (
        compute_canonical_for_pick as compute_canonical_full,
    )
    from tools.forbid_full_aut_orbit_analysis import (
        induce_27_action,
        triad_orbit,
    )

    def compute_canonical_for_pick(cands, pick):
        # Use the full-aut computation when available
        return compute_canonical_full(cands, pick)

    has_full_aut = True
except Exception:
    import subprocess

    has_full_aut = False

    def compute_canonical_for_pick(cands, pick):
        # Use AGL×Z3 orbit analysis script to produce an intersection; pick deterministically.
        # This is a fallback when the full-group tools (networkx etc.) are unavailable.
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "forbid_orbit_analysis.py"),
            ],
            check=True,
        )
        j = json.loads((ART / "forbid_orbit_analysis.json").read_text(encoding="utf-8"))
        inter = j.get("intersection", [])
        if not inter:
            # fallback to union of candidate orbits
            cand_orbits = j.get("cand_orbits", {}).values()
            union = set()
            for v in cand_orbits:
                union.update(v)
            inter = sorted(list(union))
        if not inter:
            return None
        if pick == "lex_min":
            return tuple(sorted(inter)[0])
        elif pick == "max_stab":
            # Fallback deterministic choice: pick triad with smallest sum-of-elements
            return tuple(min(inter, key=lambda t: sum(t)))
        else:
            return tuple(sorted(inter)[0])


# compute_canonical_for_pick is defined above and will use the full-aut method when available
# or the AGL(2,3) fallback when not. Keeping a single definition avoids accidental redefinition.


def run_anchor_and_archive(forbid_str: str, time: int, w_list: str, workers: int):
    cmd = [
        sys.executable,
        str(ROOT / "tools" / "run_anchor_and_archive.py"),
        "--forbid",
        forbid_str,
        "--time",
        str(time),
        "--w-list",
        w_list,
        "--workers",
        str(workers),
    ]
    print("Running anchored CP-SAT for forbid:", forbid_str)
    subprocess.run(cmd, check=True)


def run_generate_gf2_cert():
    cmd = [sys.executable, str(ROOT / "tools" / "generate_gf2_certificate.py")]
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cands", type=str, default="0-18-25,0-20-23")
    parser.add_argument("--time", type=int, default=300)
    parser.add_argument("--w-list", type=str, default="0,4,5,6,7,8,9,10,11,12,13,14,15")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=REPORTS,
        help="Directory to write markdown reports (defaults to repo reports/).",
    )
    parser.add_argument(
        "--pick1", type=str, default="lex_min", choices=["lex_min", "max_stab"]
    )
    parser.add_argument(
        "--pick2", type=str, default="max_stab", choices=["lex_min", "max_stab"]
    )
    args = parser.parse_args()

    cands = [tuple(sorted(int(x) for x in s.split("-"))) for s in args.cands.split(",")]

    # compute canonical picks
    canonical1 = compute_canonical_for_pick(cands, args.pick1)
    canonical2 = compute_canonical_for_pick(cands, args.pick2)

    forbids = []
    for name, tri in [(args.pick1, canonical1), (args.pick2, canonical2)]:
        if tri is None:
            print(f"Warning: no canonical representative found for pick {name}")
            continue
        forbids.append((name, tri))

    summary = {"forbids": []}

    reports_dir = Path(args.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    for name, tri in forbids:
        forbid_str = "-".join(map(str, tri))
        try:
            cmd = [
                sys.executable,
                str(ROOT / "tools" / "run_anchor_and_archive.py"),
                "--forbid",
                forbid_str,
                "--time",
                str(args.time),
                "--w-list",
                args.w_list,
                "--workers",
                str(args.workers),
                "--reports-dir",
                str(reports_dir),
            ]
            print("Running anchored CP-SAT for forbid:", forbid_str)
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Anchored run failed for forbid {forbid_str}:", e)

        # generate GF(2) certificates (will write synthetic if no unsat cores exist)
        try:
            run_generate_gf2_cert()
        except subprocess.CalledProcessError as e:
            print("GF(2) certificate generation failed:", e)

        # collect artifacts
        anchor_summary = (
            ART / f"anchor_core_cpsat_summary_forbid_{forbid_str.replace(',','_')}.json"
        )
        gf2 = ART / "gf2_certificates.json"
        rep = {
            "pick": name,
            "forbid": forbid_str,
            "anchor_summary_exists": anchor_summary.exists(),
            "gf2_exists": gf2.exists(),
        }
        if anchor_summary.exists():
            try:
                rep["anchor_summary"] = json.loads(
                    anchor_summary.read_text(encoding="utf-8")
                )
            except Exception:
                rep["anchor_summary"] = "corrupt"
        if gf2.exists():
            try:
                rep["gf2_certs"] = json.loads(gf2.read_text(encoding="utf-8"))
            except Exception:
                rep["gf2_certs"] = "corrupt"

        summary["forbids"].append(rep)

    outpath = ART / "canonical_forbid_verification_summary.json"
    outpath.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # human report
    lines = ["# Canonical forbid verification summary", ""]
    for r in summary["forbids"]:
        lines.append(f"- pick: {r['pick']}, forbid: {r['forbid']}")
        lines.append(f"  - anchor_summary_exists: {r['anchor_summary_exists']}")
        lines.append(f"  - gf2_exists: {r['gf2_exists']}")
    (reports_dir / "canonical_forbid_verification_summary.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(
        "Wrote summary artifacts/canonical_forbid_verification_summary.json and report"
    )


if __name__ == "__main__":
    main()
