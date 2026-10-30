#!/usr/bin/env python3
"""Sweep phase-correction workflow across bundle directories.

This script discovers bundle roots by looking for the canonical input CSV:
`qutrit_MUB_state_vectors_for_N12_vertices.csv`.

For each compatible bundle, it:
1. Ensures Clifford and Sp(2,3) analysis artifacts exist (builds them if needed).
2. Runs `tools/phase_correct_mubs.py --write-holonomy-gauge`.
3. Reads `parallelogram_holonomy_vs_bargmann.json` and records match stats.

Outputs:
  - JSON summary (default: docs/reports/phase_correction_sweep_summary.json)
  - Markdown summary (default: docs/reports/phase_correction_sweep_summary.md)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_BUNDLE_FILES = (
    "H27_vertices_as_F3_cube_xy_t.csv",
    "missing_planes_as_phase_space_points.csv",
    "N12_vertices_as_affine_lines.csv",
    "qutrit_MUB_state_vectors_for_N12_vertices.csv",
)

DEFAULT_SEARCH_ROOTS = ("artifacts/bundles", "analysis")


def _run_checked(cmd: list[str]) -> None:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + "\nstdout:\n"
            + proc.stdout
            + "\nstderr:\n"
            + proc.stderr
        )


def discover_bundle_dirs(search_roots: Iterable[Path]) -> list[Path]:
    candidates: set[Path] = set()
    for root in search_roots:
        if not root.exists():
            continue
        for csv_path in root.rglob("qutrit_MUB_state_vectors_for_N12_vertices.csv"):
            candidates.add(csv_path.parent.resolve())
    return sorted(candidates)


def is_compatible_bundle(bundle_dir: Path) -> tuple[bool, list[str]]:
    missing = [
        name for name in REQUIRED_BUNDLE_FILES if not (bundle_dir / name).exists()
    ]
    return (len(missing) == 0, missing)


def ensure_analysis_inputs(bundle_dir: Path, out_dir: Path, python_exe: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    clifford_json = out_dir / "clifford_lift_on_H27_and_N12.json"
    sp23_json = out_dir / "sp23_action_on_H27_and_N12.json"

    if not clifford_json.exists():
        _run_checked(
            [
                python_exe,
                "tools/build_qutrit_clifford_lift.py",
                "--bundle-dir",
                str(bundle_dir),
                "--out-dir",
                str(out_dir),
            ]
        )

    if not sp23_json.exists():
        _run_checked(
            [
                python_exe,
                "tools/compare_sp23_clifford_and_bargmann.py",
                "--bundle-dir",
                str(bundle_dir),
                "--out-dir",
                str(out_dir),
            ]
        )


def read_match_stats(out_dir: Path) -> tuple[int | None, int | None]:
    stats_path = out_dir / "parallelogram_holonomy_vs_bargmann.json"
    if not stats_path.exists():
        return (None, None)
    payload = json.loads(stats_path.read_text(encoding="utf-8"))
    matches = payload.get("matches")
    total = payload.get("total_parallelograms")
    if isinstance(matches, int) and isinstance(total, int):
        return (matches, total)
    return (None, None)


def run_bundle(bundle_dir: Path, out_dir: Path, python_exe: str) -> dict[str, object]:
    result: dict[str, object] = {
        "bundle_dir": str(bundle_dir),
        "out_dir": str(out_dir),
        "status": "ok",
        "notes": [],
    }
    compatible, missing = is_compatible_bundle(bundle_dir)
    if not compatible:
        result["status"] = "skipped_incompatible"
        result["notes"] = [f"Missing required files: {', '.join(missing)}"]
        result["matches"] = None
        result["total"] = None
        return result

    try:
        ensure_analysis_inputs(bundle_dir, out_dir, python_exe)
        _run_checked(
            [
                python_exe,
                "tools/phase_correct_mubs.py",
                "--bundle-dir",
                str(bundle_dir),
                "--out-dir",
                str(out_dir),
                "--write-holonomy-gauge",
            ]
        )
        matches, total = read_match_stats(out_dir)
        result["matches"] = matches
        result["total"] = total
    except Exception as exc:
        result["status"] = "error"
        result["notes"] = [str(exc)]
        result["matches"] = None
        result["total"] = None
    return result


def build_markdown_summary(summary: dict[str, object]) -> str:
    lines = []
    lines.append("# Phase correction bundle sweep")
    lines.append("")
    lines.append(f"- Generated UTC: `{summary['generated_at_utc']}`")
    lines.append(f"- Python: `{summary['python_executable']}`")
    lines.append(f"- Bundles discovered: `{summary['bundles_total']}`")
    lines.append(f"- Success: `{summary['bundles_succeeded']}`")
    lines.append(f"- Failed/skipped: `{summary['bundles_failed_or_skipped']}`")
    lines.append("")
    lines.append("| Bundle | Status | Matches | Total | Notes |")
    lines.append("|---|---|---:|---:|---|")
    for row in summary["results"]:
        notes = "; ".join(row.get("notes", []))
        lines.append(
            f"| `{row['bundle_dir']}` | `{row['status']}` | {row.get('matches')} | {row.get('total')} | {notes} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bundle-dir",
        action="append",
        type=Path,
        default=[],
        help="Explicit bundle dir to process (repeatable).",
    )
    parser.add_argument(
        "--search-root",
        action="append",
        type=Path,
        default=[],
        help="Root to scan for bundle dirs (repeatable).",
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("docs/reports/phase_correction_sweep_summary.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("docs/reports/phase_correction_sweep_summary.md"),
    )
    parser.add_argument(
        "--python-exe",
        default=sys.executable,
        help="Python executable used to run helper scripts.",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit with non-zero code if any bundle errors.",
    )
    args = parser.parse_args()

    search_roots = [ROOT / p for p in args.search_root] if args.search_root else []
    if not search_roots:
        search_roots = [ROOT / p for p in DEFAULT_SEARCH_ROOTS]

    explicit = [
        p.resolve() if p.is_absolute() else (ROOT / p).resolve()
        for p in args.bundle_dir
    ]
    discovered = discover_bundle_dirs(search_roots)
    bundle_dirs = sorted({*explicit, *discovered})

    results = []
    had_error = False
    for bundle in bundle_dirs:
        out_dir = bundle / "analysis"
        row = run_bundle(bundle, out_dir, args.python_exe)
        if row["status"] == "error":
            had_error = True
        results.append(row)

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_executable": args.python_exe,
        "bundles_total": len(results),
        "bundles_succeeded": sum(1 for r in results if r["status"] == "ok"),
        "bundles_failed_or_skipped": sum(1 for r in results if r["status"] != "ok"),
        "results": results,
    }

    out_json = args.out_json if args.out_json.is_absolute() else ROOT / args.out_json
    out_md = args.out_md if args.out_md.is_absolute() else ROOT / args.out_md
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    out_md.write_text(build_markdown_summary(summary), encoding="utf-8")

    print(f"Wrote {out_json}")
    print(f"Wrote {out_md}")

    if args.fail_on_error and had_error:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
