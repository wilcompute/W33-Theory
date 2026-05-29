"""Real CSP prototype using repo packet data (symmetry-reduced).

Attempts to import packet data generators from the repo (H4 orbital code).
If available, builds group actions and searches for an equivariant S3-style
selector using the same orbit-rep propagation strategy as the toy prototype.

Falls back gracefully and prints diagnostics if the repo functions or heavy
dependencies are unavailable in the environment where this script is run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def compute_branch_perm_if_consistent(perm: Tuple[int, ...], n_cells: int, per_cell: int) -> Optional[Tuple[int, ...]]:
    # For a global branch permutation to exist, the local mapping (image%per_cell)
    # must be the same for every cell. Check that property and return the branch
    # permutation on labels 0..per_cell-1 if consistent.
    n = n_cells * per_cell
    if len(perm) != n:
        return None
    # compute mapping on cell 0
    f0 = tuple(perm[j] % per_cell for j in range(per_cell))
    for cell in range(n_cells):
        fc = tuple(perm[cell * per_cell + j] % per_cell for j in range(per_cell))
        if fc != f0:
            return None
    return f0


def compute_orbits(n: int, group_perms: List[Tuple[int, ...]]) -> List[List[int]]:
    seen = [False] * n
    orbits: List[List[int]] = []
    for i in range(n):
        if seen[i]:
            continue
        stack = [i]
        orb = set()
        while stack:
            x = stack.pop()
            if x in orb:
                continue
            orb.add(x)
            for p in group_perms:
                y = p[x]
                if y not in orb:
                    stack.append(y)
        for v in orb:
            seen[v] = True
        orbits.append(sorted(orb))
    return orbits


def search_selector_from_group(packet_cycles: List[Tuple[int, ...]], group_raw: List[Tuple[int, ...]], per_cell: int = 3) -> Optional[Dict[int, int]]:
    n = len(packet_cycles)
    # try to factor into cells
    if per_cell <= 0:
        per_cell = 3
    if n % per_cell != 0:
        # try to find a small divisor
        for d in [2, 3, 4, 5]:
            if n % d == 0:
                per_cell = d
                break
    n_cells = n // per_cell

    # compute branch perms when possible
    group_map: List[Tuple[Tuple[int, ...], Optional[Tuple[int, ...]]]] = []
    for perm in group_raw:
        branch = compute_branch_perm_if_consistent(perm, n_cells, per_cell)
        group_map.append((perm, branch))

    # build orbits using only permutation action
    group_perms = [perm for perm, _ in group_map]
    orbits = compute_orbits(n, group_perms)
    reps = [orb[0] for orb in orbits]

    cell_indices = [[cell * per_cell + j for j in range(per_cell)] for cell in range(n_cells)]

    assignment: Dict[int, int] = {}

    def propagate(i: int, v: int) -> bool:
        stack = [(i, v)]
        while stack:
            idx, val = stack.pop()
            if idx in assignment:
                if assignment[idx] != val:
                    return False
                continue
            assignment[idx] = val
            # local distinctness per cell
            cell = idx // per_cell
            assigned_vals = [assignment.get(ii) for ii in cell_indices[cell]]
            if all(x is not None for x in assigned_vals) and len(set(assigned_vals)) != per_cell:
                return False
            # propagate via group_map
            for perm, branch in group_map:
                j = perm[idx]
                if branch is None:
                    # require exact equality if no branch action available
                    vj = val
                else:
                    vj = branch[val]
                if j in assignment:
                    if assignment[j] != vj:
                        return False
                else:
                    stack.append((j, vj))
        return True

    def backtrack(pos: int) -> Optional[Dict[int, int]]:
        if pos >= len(reps):
            return dict(assignment)
        rep = reps[pos]
        if rep in assignment:
            return backtrack(pos + 1)
        for v in range(per_cell):
            snapshot = dict(assignment)
            ok = propagate(rep, v)
            if ok:
                res = backtrack(pos + 1)
                if res is not None:
                    return res
            assignment.clear()
            assignment.update(snapshot)
        return None

    return backtrack(0)


def main() -> None:
    out_path = Path("data") / "transport_csp_real_result.json"
    out_path.parent.mkdir(exist_ok=True)

    try:
        from scripts.w33_h4_orbital_no_go import compute_quadrangle_adjacent_transport_packet_action_data
    except Exception as exc:  # pragma: no cover - environment dependent
        msg = {
            "status": "missing_repo_function",
            "error": str(exc),
            "note": "Could not import required packet builder from scripts; run this locally inside the repo venv.",
        }
        out_path.write_text(json.dumps(msg, indent=2))
        print(json.dumps(msg, indent=2))
        return

    try:
        data = compute_quadrangle_adjacent_transport_packet_action_data()
    except Exception as exc:  # pragma: no cover - environment dependent
        msg = {"status": "compute_failed", "error": str(exc)}
        out_path.write_text(json.dumps(msg, indent=2))
        print(json.dumps(msg, indent=2))
        return

    packet_cycles = data.get("packet_cycles") or []
    packet_image = data.get("packet_image") or set()
    packet_image_list = [tuple(p) for p in packet_image]

    n = len(packet_cycles)
    if n == 0:
        msg = {"status": "no_packet_cycles_found", "n": n}
        out_path.write_text(json.dumps(msg, indent=2))
        print(json.dumps(msg, indent=2))
        return

    # try OR-Tools CP-SAT solver if available (symmetry-reduced encoding)
    try:
        from ortools.sat.python import cp_model  # type: ignore

        per_cell = 3
        if n % per_cell != 0:
            for d in [2, 3, 4, 5]:
                if n % d == 0:
                    per_cell = d
                    break
        n_cells = n // per_cell

        # build group_map for branch-aware elements
        group_raw = [tuple(p) for p in packet_image_list]
        group_map = []
        for perm in group_raw:
            branch = compute_branch_perm_if_consistent(perm, n_cells, per_cell)
            if branch is not None:
                group_map.append((perm, branch))

        # CP-SAT model
        model = cp_model.CpModel()
        # boolean indicators b[i][b] <=> x[i] == b
        bvars = [[model.NewBoolVar(f"b_{i}_{b}") for b in range(per_cell)] for i in range(n)]
        for i in range(n):
            model.Add(sum(bvars[i]) == 1)

        # per-cell: each label used exactly once (permutation)
        cell_indices = [[cell * per_cell + j for j in range(per_cell)] for cell in range(n_cells)]
        for cell in range(n_cells):
            for b in range(per_cell):
                model.Add(sum(bvars[idx][b] for idx in cell_indices[cell]) == 1)

        # equivariance constraints for each group_map element
        for perm, branch in group_map:
            for i in range(n):
                for b in range(per_cell):
                    # If bvars[i][b] then bvars[perm[i]][branch[b]] must hold
                    model.Add(bvars[perm[i]][branch[b]] == 1).OnlyEnforceIf(bvars[i][b])

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0
        solver.parameters.num_search_workers = 8
        status = solver.Solve(model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            sol = {}
            for i in range(n):
                for b in range(per_cell):
                    if solver.BooleanValue(bvars[i][b]):
                        sol[i] = b
                        break
            out = {"status": "found_or_tools", "n_quadrangles": n, "assignment": sol}
            out_path.write_text(json.dumps(out, indent=2))
            print(json.dumps(out, indent=2))
            return
        else:
            print("OR-Tools found no solution (or timed out); falling back to backtracking")
    except Exception:
        # ortools not available or failed; fall back
        pass

    # fallback symmetry-reduced backtracking search
    sol = search_selector_from_group(packet_cycles, packet_image_list, per_cell=3)
    out = {
        "status": "found_backtrack" if sol else "none",
        "n_quadrangles": n,
        "assignment_size": len(sol) if sol else 0,
        "assignment": sol,
    }
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
