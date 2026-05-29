"""Solver harness: export CNF, solve with pysat (if available), verify assignment.

This helper automates the common loop: export CNF for a chosen seed, run a SAT
solver via python-sat (pysat) when available, and post-process the model into
the repo's assignment JSON shape, then run the verification wrapper.

Run locally inside the repo venv:

  python scripts/transport_solve_harness.py --seed 0 --mode pysat

Modes:
  cnf   - only export CNF and exit
  pysat - export CNF then solve with pysat (if installed)
  or    - run OR-Tools runner (delegates to transport_csp_or_tools_larger)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]


def run_command(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return proc.returncode, out, err


def export_cnf(seed: int) -> Path:
    out = ROOT / "data" / f"transport_seed{seed}.cnf"
    cmd = [sys.executable, str(ROOT / "scripts" / "transport_csp_cnf_export.py"), "--out", str(out), "--seeds", str(seed)]
    rc, out, err = run_command(cmd)
    if rc != 0:
        raise RuntimeError(f"CNF exporter failed: rc={rc}\nstdout={out}\nstderr={err}")
    # exporter writes file named transport_seed{seed}_seed{seed}.cnf
    cnf_file = out = ROOT / "data" / f"{out.stem}_seed{seed}.cnf"
    # ensure file exists
    if not cnf_file.exists():
        # try alternate name
        alt = ROOT / "data" / f"transport_seed{seed}_seed{seed}.cnf"
        if alt.exists():
            cnf_file = alt
        else:
            raise FileNotFoundError(f"Expected CNF file not found for seed {seed}")
    return cnf_file


def solve_with_pysat(cnf_path: Path, timeout: Optional[int] = None) -> Optional[dict]:
    try:
        from pysat.formula import CNF
        from pysat.solvers import Solver
    except Exception as exc:
        print(json.dumps({"status": "pysat_missing", "error": str(exc)}))
        return None

    f = CNF(from_file=str(cnf_path))
    with Solver(name="glucose4") as s:
        s.append_formula(f.clauses)
        ok = s.solve()
        if not ok:
            print(json.dumps({"status": "unsat_or_unknown"}))
            return None
        model = s.get_model()

    # read varmap from comment line in CNF (second line expected)
    with open(cnf_path, "r", encoding="utf-8") as fh:
        lines = [next(fh) for _ in range(3)]
    varmap = None
    for line in lines:
        if line.startswith("c varmap:"):
            varmap = json.loads(line.split("c varmap:", 1)[1].strip())
            break
    if varmap is None:
        raise RuntimeError("varmap comment not found in CNF file")

    assignment = {}
    for lit in model:
        if lit > 0:
            key = str(lit)
            if key in varmap:
                idx, b = varmap[key]
                assignment[int(idx)] = int(b)
    return assignment


def run_or_tools(seed: int, time_limit: int = 300, workers: int = 8) -> Path:
    cmd = [sys.executable, str(ROOT / "scripts" / "transport_csp_or_tools_larger.py"),
           "--time_limit", str(time_limit), "--workers", str(workers), "--seed", str(seed)]
    rc, out, err = run_command(cmd)
    if rc != 0:
        raise RuntimeError(f"OR-Tools runner failed: rc={rc}\nstdout={out}\nstderr={err}")
    # output file produced: data/transport_csp_or_tools_seed{seed}.json
    out_path = ROOT / "data" / f"transport_csp_or_tools_seed{seed}.json"
    if not out_path.exists():
        # try alternate
        alt = ROOT / "data" / f"transport_csp_or_tools_seed{seed}.json"
        if not alt.exists():
            raise FileNotFoundError("Expected OR-Tools output not found")
    return out_path


def verify_result(result_path: Path) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / "transport_result_verify.py"), str(result_path)]
    rc, out, err = run_command(cmd)
    if rc != 0:
        print(f"verification failed: rc={rc}\n{err}")
    else:
        print(out)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--mode", choices=["cnf", "pysat", "or"], default="pysat")
    parser.add_argument("--time_limit", type=int, default=300)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    seed = args.seed
    if args.mode == "cnf":
        cnf = export_cnf(seed)
        print(json.dumps({"status": "cnf_exported", "cnf": str(cnf)}))
        return

    if args.mode == "or":
        out_path = run_or_tools(seed, time_limit=args.time_limit, workers=args.workers)
        verify_result(out_path)
        return

    # default pysat flow
    cnf = export_cnf(seed)
    assignment = solve_with_pysat(cnf)
    if assignment is None:
        print(json.dumps({"status": "no_assignment"}))
        return
    # write result file and verify
    res_path = ROOT / "data" / f"transport_csp_pysat_seed{seed}.json"
    res = {"status": "found_pysat", "assignment": assignment}
    res_path.write_text(json.dumps(res, indent=2))
    verify_result(res_path)


if __name__ == "__main__":
    main()
