#!/usr/bin/env python3
"""
Run the SageMath (Docker-backed) cross-checks and write a small closeout bundle.

This complements `tools/toe_algebra_closeout.py` (pure Python).

Run:
  python tools/toe_sage_closeout.py

Outputs:
  - artifacts/toe_sage_closeout.json
  - artifacts/toe_sage_closeout.md
  - artifacts/sage_runs/*.log
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
RUNS = ART / "sage_runs"


def _run(cmd: List[str], *, log_path: Path, env: Dict[str, str]) -> Dict[str, object]:
    t0 = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    dt = time.time() - t0
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(proc.stdout, encoding="utf-8")
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "seconds": dt,
        "log": log_path.relative_to(ROOT).as_posix(),
    }


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)

    # Force Docker-backed Sage for reproducibility (works even if micromamba exists but has no `sage` env).
    env = os.environ.copy()
    env["SAGE_DOCKER_IMAGE"] = "sagemath/sagemath:latest"

    checks = [
        {
            "name": "sage_verify_w33_sp4_we6",
            "script": "tools/sage_verify_w33_sp4_we6.sage",
            "out_json": "artifacts/sage_verify_w33_sp4_we6.json",
        },
        {
            "name": "sage_verify_e8_trinification_closeout",
            "script": "tools/sage_verify_e8_trinification_closeout.sage",
            "out_json": "artifacts/sage_verify_e8_trinification_closeout.json",
        },
    ]

    run_meta: Dict[str, object] = {
        "status": "ok",
        "runs": {},
        "artifacts": {},
        "checks": {},
    }

    for item in checks:
        name = item["name"]
        log = RUNS / f"{name}.log"
        meta = _run(["./run_sage.sh", item["script"]], log_path=log, env=env)
        run_meta["runs"][name] = meta
        run_meta["artifacts"][name] = item["out_json"]
        if meta["returncode"] != 0:
            run_meta["status"] = "fail"

        out_path = ROOT / item["out_json"]
        if out_path.exists():
            try:
                out = json.loads(out_path.read_text(encoding="utf-8"))
                run_meta["checks"][name] = {"status": out.get("status")}
                if out.get("status") != "ok":
                    run_meta["status"] = "fail"
            except Exception as e:
                run_meta["checks"][name] = {"status": "unreadable", "error": str(e)}
                run_meta["status"] = "fail"
        else:
            run_meta["checks"][name] = {"status": "missing"}
            run_meta["status"] = "fail"

    out_json = ART / "toe_sage_closeout.json"
    out_md = ART / "toe_sage_closeout.md"
    out_json.write_text(
        json.dumps(run_meta, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    md_lines: List[str] = []
    md_lines.append("# TOE Sage closeout\n")
    md_lines.append(f"- status: `{run_meta['status']}`")
    md_lines.append("- runner: `tools/toe_sage_closeout.py`")
    md_lines.append("- backend: `docker (sagemath/sagemath:latest)`\n")
    md_lines.append("## Checks\n")
    for item in checks:
        name = item["name"]
        md_lines.append(
            f"- {name}: `{run_meta['checks'][name]['status']}` (log: `{run_meta['runs'][name]['log']}`)"
        )
    md_lines.append(f"\n- JSON: `{out_json.relative_to(ROOT).as_posix()}`")
    out_md.write_text("\n".join(md_lines).rstrip() + "\n", encoding="utf-8")

    print(out_md.read_text(encoding="utf-8"))
    if run_meta["status"] != "ok":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
