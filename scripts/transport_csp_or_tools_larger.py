"""Improved OR-Tools CP-SAT runner for the transport CSP with configurable limits.

This script mirrors `transport_csp_real.py` but exposes command-line
parameters for time limit, workers, and a symmetry-breaking seed. It will
attempt to use OR-Tools if installed; otherwise it will print guidance for
running the CNF export instead.

Usage (local):
  python scripts/transport_csp_or_tools_larger.py --time_limit 300 --workers 16 --seed 0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def compute_branch_perm_if_consistent(perm: Tuple[int, ...], n_cells: int, per_cell: int) -> Optional[Tuple[int, ...]]:
    if len(perm) != n_cells * per_cell:
        return None
    f0 = tuple(perm[j] % per_cell for j in range(per_cell))
    for cell in range(n_cells):
        fc = tuple(perm[cell * per_cell + j] % per_cell for j in range(per_cell))
        if fc != f0:
            return None
    return f0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_limit", type=float, default=30.0, help="seconds")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0, help="symmetry-breaking seed for rep0")
    args = parser.parse_args()

    try:
        from scripts.w33_h4_orbital_no_go import compute_quadrangle_adjacent_transport_packet_action_data
    except Exception as exc:
        print(json.dumps({"status": "missing_repo_function", "error": str(exc)}))
        return

    try:
        data = compute_quadrangle_adjacent_transport_packet_action_data()
    except Exception as exc:
        print(json.dumps({"status": "compute_failed", "error": str(exc)}))
        return

    packet_cycles = data.get("packet_cycles") or []
    packet_image = list(data.get("packet_image") or [])
    if not packet_cycles:
        print(json.dumps({"status": "no_packet_cycles_found", "n": 0}))
        return

    n = len(packet_cycles)
    per_cell = 3
    if n % per_cell != 0:
        for d in [2, 3, 4, 5]:
            if n % d == 0:
                per_cell = d
                break
    n_cells = n // per_cell

    group_raw = [tuple(p) for p in packet_image]
    group_map = []
    for perm in group_raw:
        branch = compute_branch_perm_if_consistent(perm, n_cells, per_cell)
        group_map.append((perm, branch))

    try:
        from ortools.sat.python import cp_model  # type: ignore
    except Exception as exc:
        msg = {
            "status": "ortools_missing",
            "error": str(exc),
            "note": "Install ortools or use the CNF exporter: scripts/transport_csp_cnf_export.py",
        }
        print(json.dumps(msg, indent=2))
        return

    # build CP-SAT model
    model = cp_model.CpModel()
    bvars = [[model.NewBoolVar(f"b_{i}_{b}") for b in range(per_cell)] for i in range(n)]
    for i in range(n):
        model.Add(sum(bvars[i]) == 1)

    cell_indices = [[cell * per_cell + j for j in range(per_cell)] for cell in range(n_cells)]
    for cell in range(n_cells):
        for b in range(per_cell):
            model.Add(sum(bvars[idx][b] for idx in cell_indices[cell]) == 1)

    for perm, branch in group_map:
        for i in range(n):
            for b in range(per_cell):
                if branch is None:
                    model.Add(bvars[perm[i]][b] == 1).OnlyEnforceIf(bvars[i][b])
                else:
                    model.Add(bvars[perm[i]][branch[b]] == 1).OnlyEnforceIf(bvars[i][b])

    # symmetry-breaking seed: fix rep0
    rep0 = 0
    seed = args.seed % per_cell
    model.Add(bvars[rep0][seed] == 1)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(args.time_limit)
    solver.parameters.num_search_workers = int(args.workers)
    solver.parameters.random_seed = 12345

    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = {i: next(b for b in range(per_cell) if solver.BooleanValue(bvars[i][b])) for i in range(n)}
        out = {"status": "found_or_tools", "n_quadrangles": n, "assignment": sol}
    else:
        out = {"status": "no_solution_or_timeout", "solver_status": int(status)}

    out_path = Path("data") / f"transport_csp_or_tools_seed{seed}.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
