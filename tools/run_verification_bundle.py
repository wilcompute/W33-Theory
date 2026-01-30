#!/usr/bin/env python3
"""Run the minimal verification suite and package outputs.

Creates a timestamped bundle under verification_bundle/ with:
- command logs
- copied artifacts
- hash manifest
- summary.json
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = ROOT / "verification_bundle"

NON_PANDAS = [
    ["python3", "w33_baseline_audit.py"],
    ["python3", "w33_baseline_audit_suite.py"],
    ["python3", "tools/e6_we6_orbit_refined.py"],
    ["python3", "tools/explicit_bijection_decomposition.py"],
]

PANDAS_SCRIPTS = [
    ["python", "-X", "utf8", "src/color_singlet_test.py"],
    ["python", "-X", "utf8", "src/z4_analysis.py"],
    ["python", "-X", "utf8", "src/final_v23_analysis.py"],
]

ARTIFACTS = [
    ROOT / "artifacts" / "e6_we6_orbit_refined.json",
    ROOT / "artifacts" / "explicit_bijection_decomposition.json",
    ROOT / "artifacts" / "explicit_bijection_refined.json",
    ROOT / "artifacts" / "final_summary_table.json",
    ROOT / "artifacts" / "final_summary_table.md",
    ROOT / "artifacts" / "verification_digest.json",
    ROOT / "artifacts" / "verification_digest.md",
]

CLAUDE_DATA = [
    ROOT / "claude_workspace" / "data" / "w33_baseline_audit_results.json",
    ROOT / "claude_workspace" / "data" / "w33_baseline_audit_top.csv",
    ROOT / "claude_workspace" / "data" / "w33_baseline_suite_results.json",
]


def pick_pandas_python() -> str:
    # Prefer env override
    env_py = os.environ.get("W33_PY")
    if env_py and Path(env_py).exists():
        return env_py

    candidates = [
        ROOT / ".venv_toe" / "bin" / "python",
        Path("/tmp/venv_toe/bin/python"),
        ROOT / ".venv" / "bin" / "python",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # fallback to python3
    return "python3"


def run_cmd(cmd, out_path: Path) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    out_path.write_text(
        f"$ {' '.join(cmd)}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n",
        encoding="utf-8",
    )
    return {"cmd": cmd, "returncode": proc.returncode}


def copy_if_exists(src: Path, dst_dir: Path) -> list:
    copied = []
    if src.exists():
        dst = dst_dir / src.name
        shutil.copy2(src, dst)
        copied.append(dst)
    return copied


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle = BUNDLE_ROOT / f"verify_{ts}"
    bundle.mkdir(parents=True, exist_ok=True)

    logs_dir = bundle / "logs"
    logs_dir.mkdir(exist_ok=True)

    summary = {
        "timestamp": ts,
        "runs": [],
        "pandas_python": pick_pandas_python(),
    }

    # Run non-pandas scripts with python3
    for i, cmd in enumerate(NON_PANDAS):
        log_path = logs_dir / f"run_{i+1:02d}_non_pandas.log"
        summary["runs"].append(run_cmd(cmd, log_path))

    # Run pandas scripts with selected python
    pandas_py = pick_pandas_python()
    for j, cmd in enumerate(PANDAS_SCRIPTS):
        cmd2 = cmd.copy()
        cmd2[0] = pandas_py
        log_path = logs_dir / f"run_{len(NON_PANDAS)+j+1:02d}_pandas.log"
        summary["runs"].append(run_cmd(cmd2, log_path))

    # Copy artifacts
    copied = []
    artifacts_dir = bundle / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    for p in ARTIFACTS:
        copied += copy_if_exists(p, artifacts_dir)

    data_dir = bundle / "data"
    data_dir.mkdir(exist_ok=True)
    for p in CLAUDE_DATA:
        copied += copy_if_exists(p, data_dir)

    # Hash manifest
    manifest = []
    for path in sorted(copied):
        manifest.append(
            {"file": str(path.relative_to(bundle)), "sha256": sha256_file(path)}
        )

    (bundle / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    (bundle / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"Bundle created: {bundle}")


if __name__ == "__main__":
    main()
