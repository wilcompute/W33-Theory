#!/usr/bin/env python3
"""
Auto-ingest a ChatGPT bundle: run backbone/coset map, trihedron builder, diagnostics,
perform fast repairs (rebuild root dict from bundle export), and optionally commit/push
results to a branch and create a PR.

Usage:
  py -3 tools/auto_ingest_bundle.py --bundle-dir <path> [--out-dir artifacts/bundles/<name>] [--threshold 0.05] [--push]

Notes:
 - Designed to be run by `tools/watch_chatgpt52.py` or manually on a bundle dir.
 - Uses existing tools in `tools/` (toe_backbone_coset_coupling_map.py, build_trihedron_tritangent_bundle.py, toe_root_operator_dictionary.py, diagnose_v3p52_root_recovery.py).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"


def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> int:
    print("Running:", " ".join(cmd))
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd
    )
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print("STDERR:", proc.stderr)
    return proc.returncode


def measure_mean_rel(out_json_path: Path) -> Optional[float]:
    if not out_json_path.exists():
        return None
    j = json.loads(out_json_path.read_text(encoding="utf-8"))
    vals = [
        c.get("backbone_coset", {}).get("rel_resid")
        for c in j.get("couplings", [])
        if c.get("backbone_coset")
    ]
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def find_coupling_jsons(bundle_dir: Path) -> List[Path]:
    res = list(bundle_dir.glob("toe_coupling_strengths_*.json"))
    # Fallback: any json that looks like coupling strengths
    if not res:
        for p in bundle_dir.rglob("*.json"):
            if p.name.lower().startswith("toe_coupling_strengths"):
                res.append(p)
    return sorted(res)


def has_cubic_csvs(bundle_dir: Path) -> bool:
    # Heuristic: if there are files with 'h27', 'trihedron', 'tritangent' in name
    for p in bundle_dir.rglob("*"):
        if p.is_file():
            name = p.name.lower()
            if any(
                x in name
                for x in ["h27", "schlafli", "trihedron", "tritangent", "missing_9"]
            ):
                return True
    return False


def process_bundle(
    bundle_dir: Path,
    out_dir: Path,
    threshold: float = 0.05,
    extended_repair: bool = False,
    push: bool = False,
    dry_run: bool = False,
    no_we6: bool = False,
):
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle_name = bundle_dir.name
    report: Dict[str, object] = {
        "bundle": str(bundle_dir),
        "bundle_name": bundle_name,
        "ts": datetime.utcnow().isoformat() + "Z",
        "actions": [],
    }

    coupling_jsons = find_coupling_jsons(bundle_dir)
    if not coupling_jsons:
        report["note"] = "No coupling JSON found in bundle"
        (out_dir / "ingest_status.json").write_text(
            json.dumps(report, indent=2), encoding="utf-8"
        )
        print("No coupling JSON found; nothing to do.")
        return report

    # For each coupling json, run backbone/coset map
    for cj in coupling_jsons:
        short = cj.stem
        out_json = out_dir / f"{short}_backbone_coset_map.json"
        out_md = out_dir / f"{short}_backbone_coset_map.md"

        rc = run_cmd(
            [
                sys.executable,
                "tools/toe_backbone_coset_coupling_map.py",
                "--in-json",
                str(cj),
                "--out-json",
                str(out_json),
                "--out-md",
                str(out_md),
            ]
        )
        report["actions"].append(
            {"step": "initial_decompose", "file": str(cj), "rc": int(rc)}
        )

        mean_rel = measure_mean_rel(out_json)
        report["initial_mean_rel"] = mean_rel
        print(f"Initial mean rel_resid for {cj.name}: {mean_rel}")

        if mean_rel is None:
            continue

        if mean_rel <= threshold:
            report["status"] = "ok"
            report["note"] = (
                f"mean_rel_resid {mean_rel} <= threshold {threshold}: no repair required"
            )
            continue

        # Attempt fast repair: if bundle contains e6_basis_export, run toe_root_operator_dictionary with export dir
        export_dir = None
        # Common export dir names
        for cand in ["e6_basis_export", "e6_basis_export_full"]:
            candp = bundle_dir / cand
            if candp.exists():
                export_dir = candp
                break
        if export_dir is not None:
            report["found_export_dir"] = str(export_dir)
            print("Attempting fast repair: regenerating root dict from bundle export")
            rc2 = run_cmd(
                [
                    sys.executable,
                    "tools/toe_root_operator_dictionary.py",
                    "--export-dir",
                    str(export_dir),
                ]
            )
            report["actions"].append(
                {
                    "step": "rebuild_root_dict_from_export",
                    "export_dir": str(export_dir),
                    "rc": int(rc2),
                }
            )
            # Re-run decomposition
            rc3 = run_cmd(
                [
                    sys.executable,
                    "tools/toe_backbone_coset_coupling_map.py",
                    "--in-json",
                    str(cj),
                    "--out-json",
                    str(out_json),
                    "--out-md",
                    str(out_md),
                ]
            )
            report["actions"].append({"step": "post_rebuild_decompose", "rc": int(rc3)})
            mean_rel_after = measure_mean_rel(out_json)
            report["mean_rel_after_rebuild"] = mean_rel_after
            print(f"Mean rel_resid after rebuild: {mean_rel_after}")
            if mean_rel_after is not None and mean_rel_after <= threshold:
                report["status"] = "repaired"
                report["note"] = (
                    f"mean_rel_resid improved to {mean_rel_after} <= threshold"
                )
                continue

        # If still bad and extended_repair requested, run diagnostic seed sweep (works for v3p52 case)
        if extended_repair and "v3p52" in bundle_name.lower():
            print("Running seed sweep diagnostics (extended repair)")
            rc4 = run_cmd(
                [
                    sys.executable,
                    "tools/diagnose_v3p52_root_recovery.py",
                    "--seeds",
                    "0",
                    "1",
                    "2",
                    "3",
                    "4",
                    "--export-dir",
                    str(export_dir) if export_dir is not None else "",
                ]
            )
            report["actions"].append({"step": "diagnose_seed_sweep", "rc": int(rc4)})
            diag = ART / "toe_root_operator_diagnostics_v3p52.json"
            if diag.exists():
                dj = json.loads(diag.read_text(encoding="utf-8"))
                best = min(
                    (
                        r
                        for r in dj.get("results", [])
                        if r.get("mean_rel_resid") is not None
                    ),
                    key=lambda x: float(x["mean_rel_resid"]),
                )
                report["diagnose_best"] = best
                # rebuild root dict with best seed
                seed = int(best["seed"])
                rc5 = run_cmd(
                    [
                        sys.executable,
                        "tools/toe_root_operator_dictionary.py",
                        "--seed",
                        str(seed),
                        "--export-dir",
                        str(export_dir) if export_dir is not None else "",
                    ]
                )
                report["actions"].append(
                    {"step": "rebuild_with_best_seed", "seed": seed, "rc": int(rc5)}
                )
                rc6 = run_cmd(
                    [
                        sys.executable,
                        "tools/toe_backbone_coset_coupling_map.py",
                        "--in-json",
                        str(cj),
                        "--out-json",
                        str(out_json),
                        "--out-md",
                        str(out_md),
                    ]
                )
                report["actions"].append(
                    {"step": "post_seed_rebuild_decompose", "rc": int(rc6)}
                )
                mean_rel_after2 = measure_mean_rel(out_json)
                report["mean_rel_after_seed_rebuild"] = mean_rel_after2
                print(f"Mean rel_resid after best-seed rebuild: {mean_rel_after2}")
                if mean_rel_after2 is not None and mean_rel_after2 <= threshold:
                    report["status"] = "repaired_seed_sweep"
                    continue

        # Try global assignment repair if extended_repair is enabled
        if extended_repair:
            print(
                "Attempting global assignment repair on output_root vectors (extended_repair)"
            )
            fixed_couplings = out_dir / f"{short}_couplings_global_assigned.json"
            rc_gm = run_cmd(
                [
                    sys.executable,
                    "tools/global_match_repair.py",
                    "--couplings",
                    str(cj),
                    "--out",
                    str(fixed_couplings),
                    "--root-npy",
                    str(ART / "toe_root_operator_dictionary.npy"),
                ]
            )
            report["actions"].append(
                {"step": "global_match", "rc": int(rc_gm), "out": str(fixed_couplings)}
            )
            # Re-run decomposition using fixed couplings file
            rc_gm2 = run_cmd(
                [
                    sys.executable,
                    "tools/toe_backbone_coset_coupling_map.py",
                    "--in-json",
                    str(fixed_couplings),
                    "--out-json",
                    str(out_json),
                    "--out-md",
                    str(out_md),
                ]
            )
            report["actions"].append(
                {"step": "post_global_match_decompose", "rc": int(rc_gm2)}
            )
            mean_rel_after3 = measure_mean_rel(out_json)
            report["mean_rel_after_global_match"] = mean_rel_after3
            print(f"Mean rel_resid after global match: {mean_rel_after3}")
            if mean_rel_after3 is not None and mean_rel_after3 <= threshold:
                report["status"] = "repaired_global_match"
                continue

        # If still unresolved, mark as needs_manual
        report["status"] = "needs_manual_revision"
        report["note"] = (
            f"mean_rel_resid {mean_rel} > threshold {threshold} after automatic attempts"
        )

    # If bundle contains cubic CSVs, run trihedron tool
    if has_cubic_csvs(bundle_dir):
        tri_out = out_dir / "trihedron"
        tri_out.mkdir(parents=True, exist_ok=True)
        args = [
            sys.executable,
            "tools/build_trihedron_tritangent_bundle.py",
            "--bundle-dir",
            str(bundle_dir),
            "--out-dir",
            str(tri_out),
        ]
        if no_we6:
            args.append("--no-we6")
        rc_tri = run_cmd(args)
        report["actions"].append(
            {"step": "trihedron_build", "rc": int(rc_tri), "out_dir": str(tri_out)}
        )

        # If trihedron output contains missing planes, attempt to reconstruct them
        try:
            tri_json = tri_out / "tritangent_planes.json"
            if tri_json.exists():
                tj = json.loads(tri_json.read_text(encoding="utf-8"))
                missing_flag = any(p.get("missing") for p in tj.get("planes", []))
                if missing_flag:
                    print(
                        "Detected missing tritangent planes; attempting reconstruct via CP-SAT solver"
                    )
                    rc_solver = run_cmd(
                        [
                            sys.executable,
                            "tools/solve_missing_tritangents.py",
                            "--bundle-dir",
                            str(bundle_dir),
                            "--trihedron-dir",
                            str(tri_out),
                        ]
                    )
                    report["actions"].append(
                        {"step": "solve_missing_tritangents", "rc": int(rc_solver)}
                    )
        except Exception as e:
            print("Warning: failed to check/solve missing tritangent planes:", e)

    # Write report files
    (out_dir / "ingest_status.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    md_lines = [f"# Auto-ingest report: {bundle_name}", ""]
    md_lines.append(f"- initial_mean_rel: `{report.get('initial_mean_rel')}`")
    md_lines.append(f"- status: `{report.get('status')}`")
    md_lines.append("")
    (out_dir / "ingest_report.md").write_text("\n".join(md_lines), encoding="utf-8")

    # Also write a small tracked summary into `docs/reports/auto_ingest/` so PRs can include
    # a compact representation even though `artifacts/` is git-ignored.
    repo_reports = ROOT / "reports" / "auto_ingest"
    repo_reports.mkdir(parents=True, exist_ok=True)
    repo_md = repo_reports / f"{bundle_name}_ingest_report.md"
    repo_status = repo_reports / f"{bundle_name}_ingest_status.json"
    repo_md_lines = [
        f"# Auto-ingest summary: {bundle_name}",
        "",
        f"- initial_mean_rel: `{report.get('initial_mean_rel')}`",
        f"- status: `{report.get('status')}`",
        "",
        f"- artifact_dir: `{out_dir}`",
    ]
    repo_md.write_text("\n".join(repo_md_lines), encoding="utf-8")
    repo_status.write_text(
        json.dumps(
            {
                "bundle": str(bundle_dir),
                "status": report.get("status"),
                "initial_mean_rel": report.get("initial_mean_rel"),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Commit & push if requested
    if push and not dry_run:
        branch = f"auto/repaired-{bundle_name}-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
        print(f"Creating git branch: {branch}")
        run_cmd(["git", "checkout", "-b", branch])
        # Add only artifacts for bundle and any relevant top-level artifacts
        run_cmd(["git", "add", str(out_dir)])
        # Also add any updated toe_root_operator_dictionary files
        run_cmd(["git", "add", str(ART / "toe_root_operator_dictionary.json")])
        run_cmd(["git", "add", str(ART / "toe_root_operator_dictionary.npy")])
        commit_msg = (
            f"Auto-ingest: processed {bundle_name} (status={report.get('status')})"
        )
        rc_commit = run_cmd(["git", "commit", "-m", commit_msg])
        report["git_commit_rc"] = int(rc_commit)
        if rc_commit == 0:
            rc_push = run_cmd(["git", "push", "-u", "origin", branch])
            report["git_push_rc"] = int(rc_push)
            # Try to create PR via gh CLI (best effort)
            try:
                rc_pr = run_cmd(
                    [
                        "gh",
                        "pr",
                        "create",
                        "--title",
                        f"Auto repair: {bundle_name}",
                        "--body",
                        str(out_dir / "ingest_report.md"),
                    ]
                )
                report["gh_pr_rc"] = int(rc_pr)
            except Exception as e:
                print(
                    "gh CLI not available or failed to create PR; you can create a PR from branch:",
                    branch,
                )
                report["gh_pr_rc"] = None
        else:
            print("No changes to commit, skipping push")

    print("Wrote report to", out_dir / "ingest_status.json")
    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bundle-dir", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, default=None)
    p.add_argument("--threshold", type=float, default=0.05)
    p.add_argument("--extended-repair", action="store_true")
    p.add_argument("--push", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--no-we6", action="store_true")
    args = p.parse_args()

    bundle_dir = args.bundle_dir
    if args.out_dir is None:
        out_dir = ART / "bundles" / bundle_dir.name
    else:
        out_dir = args.out_dir

    rpt = process_bundle(
        bundle_dir=bundle_dir,
        out_dir=out_dir,
        threshold=args.threshold,
        extended_repair=args.extended_repair,
        push=args.push,
        dry_run=args.dry_run,
        no_we6=args.no_we6,
    )
    print(json.dumps(rpt, indent=2))


if __name__ == "__main__":
    main()
