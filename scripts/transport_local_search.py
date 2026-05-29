"""Local-search/seeded solver for the transport CSP.

This lightweight, dependency-free script attempts to find a full assignment by
working on orbit representatives and propagating equivariance constraints.
It uses a simple greedy / simulated-annealing style local search and can be
used to quickly explore promising algebraic seeds produced by
`transport_algebraic_seeder.py` before dispatching heavy SAT/CP jobs.

Usage (run inside repo venv):
  python scripts/transport_local_search.py --max-iters 20000 --seed-file data/transport_algebraic_seed.json

If it finds a zero-conflict assignment it writes `data/transport_local_search_result.json`
and can optionally call the repo verifier to produce the official certificate.
"""
from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_packet_data():
    try:
        from scripts.w33_h4_orbital_no_go import compute_quadrangle_adjacent_transport_packet_action_data
    except Exception as exc:
        raise RuntimeError(f"required repo function missing: {exc}")
    data = compute_quadrangle_adjacent_transport_packet_action_data()
    packet_cycles = data.get("packet_cycles") or []
    packet_image = list(data.get("packet_image") or [])
    return packet_cycles, packet_image


def compute_branch_perm_if_consistent(perm: Tuple[int, ...], n_cells: int, per_cell: int) -> Optional[Tuple[int, ...]]:
    if len(perm) != n_cells * per_cell:
        return None
    f0 = tuple(perm[j] % per_cell for j in range(per_cell))
    for cell in range(n_cells):
        fc = tuple(perm[cell * per_cell + j] % per_cell for j in range(per_cell))
        if fc != f0:
            return None
    return f0


def build_orbit_reps(packet_image: List[Tuple[int, ...]], n: int) -> List[List[int]]:
    group_raw = [tuple(p) for p in packet_image]
    indices = list(range(n))
    visited = set()
    orbits: List[List[int]] = []
    for i in indices:
        if i in visited:
            continue
        orbit = set()
        stack = [i]
        while stack:
            cur = stack.pop()
            if cur in orbit:
                continue
            orbit.add(cur)
            for perm in group_raw:
                nxt = perm[cur]
                if nxt not in orbit:
                    stack.append(nxt)
        for v in orbit:
            visited.add(v)
        orbits.append(sorted(orbit))
    return orbits


def propagate_from_rep_assign(rep_assign: Dict[int, int], orbits: List[List[int]], group_raw: List[Tuple[int, ...]], group_map: List[Tuple[Tuple[int, ...], Optional[Tuple[int, ...]]]], per_cell: int) -> Tuple[Dict[int, int], int]:
    """Propagate representative assignments across group_map and compute conflicts.

    Returns (assignment_map, conflict_count). assignment_map maps each index->label.
    """
    assignment: Dict[int, int] = {}
    # initialize with rep assignments and propagate
    queue: List[Tuple[int, int]] = []
    for rep, val in rep_assign.items():
        queue.append((rep, val))
    while queue:
        idx, val = queue.pop()
        if idx in assignment:
            if assignment[idx] != val:
                # conflict during propagation
                return assignment, 1_000_000
            continue
        assignment[idx] = val
        # apply all group_map actions to propagate
        for perm, branch in group_map:
            img = perm[idx]
            if branch is None:
                img_val = val
            else:
                img_val = branch[val]
            if img in assignment and assignment[img] != img_val:
                return assignment, 1_000_000
            if img not in assignment:
                queue.append((img, img_val))

    # now compute per-cell conflicts: each cell indices should have unique labels
    n = len(sum(orbits, []))
    # but we can compute n_cells from maximum index and per_cell
    n_cells = (max(assignment.keys()) + 1) // per_cell if assignment else 0
    conflicts = 0
    # build per-cell mapping
    cell_map: Dict[int, Dict[int, List[int]]] = {}
    for idx, lbl in assignment.items():
        cell = idx // per_cell
        cell_map.setdefault(cell, {}).setdefault(lbl, []).append(idx)
    for cell, labels in cell_map.items():
        for lbl, lst in labels.items():
            if len(lst) > 1:
                conflicts += (len(lst) - 1)

    return assignment, conflicts


def conflict_score_full(assignment: Dict[int, int], n: int, per_cell: int, group_map: List[Tuple[Tuple[int, ...], Optional[Tuple[int, ...]]]]) -> int:
    # count per-cell duplicates
    n_cells = n // per_cell
    score = 0
    for cell in range(n_cells):
        counts = {}
        for j in range(per_cell):
            idx = cell * per_cell + j
            lbl = assignment.get(idx, None)
            if lbl is None:
                score += 1  # missing assignment penalized
                continue
            counts[lbl] = counts.get(lbl, 0) + 1
        for v in counts.values():
            if v > 1:
                score += (v - 1)
    # equivariance violations
    for perm, branch in group_map:
        for i in range(n):
            a = assignment.get(i, None)
            b = assignment.get(perm[i], None)
            if a is None or b is None:
                continue
            if branch is None:
                if a != b:
                    score += 1
            else:
                if b != branch[a]:
                    score += 1
    return score


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-iters", type=int, default=20000)
    parser.add_argument("--seed-file", default=None, help="Optional JSON seed mapping index->label to initialize reps")
    parser.add_argument("--per-cell", type=int, default=3)
    parser.add_argument("--try-count", type=int, default=8, help="Number of independent random restarts")
    parser.add_argument("--verify", action="store_true", help="Run repo verifier on any found assignment")
    args = parser.parse_args()

    packet_cycles, packet_image = load_packet_data()
    if not packet_cycles:
        print(json.dumps({"status": "no_packet_cycles_found"}))
        return
    n = len(packet_cycles)
    per_cell = int(args.per_cell)
    n_cells = n // per_cell

    # build group_map
    group_raw = [tuple(p) for p in packet_image]
    group_map: List[Tuple[Tuple[int, ...], Optional[Tuple[int, ...]]]] = []
    for perm in group_raw:
        branch = compute_branch_perm_if_consistent(perm, n_cells, per_cell)
        group_map.append((perm, branch))

    # build orbit reps
    orbits = build_orbit_reps(packet_image, n)
    reps = [min(orbit) for orbit in orbits]

    # optional seed file
    seed_assign: Dict[int, int] = {}
    if args.seed_file:
        p = Path(args.seed_file)
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "assignment" in data:
                seed_assign = {int(k): int(v) for k, v in data["assignment"].items()}
            else:
                seed_assign = {int(k): int(v) for k, v in data.items()}

    best_global = None
    best_score = 10**9
    for attempt in range(args.try_count):
        # initialize rep assignment: use seed where available; otherwise assign each rep randomly
        rep_assign: Dict[int, int] = {}
        for rep in reps:
            if rep in seed_assign:
                rep_assign[rep] = seed_assign[rep]
            else:
                rep_assign[rep] = random.randrange(per_cell)

        # initial propagation and scoring
        assignment, conflicts = propagate_from_rep_assign(rep_assign, orbits, group_raw, group_map, per_cell)
        if conflicts >= 1_000_000:
            score = 10**9
        else:
            score = conflict_score_full(assignment, n, per_cell, group_map)

        T0 = 1.0
        for it in range(args.max_iters):
            if score == 0:
                best_global = assignment
                best_score = 0
                break
            # pick random rep to modify (not fixed seed)
            rep = random.choice([r for r in reps if r not in seed_assign])
            current_val = rep_assign[rep]
            cand_vals = [v for v in range(per_cell) if v != current_val]
            if not cand_vals:
                continue
            new_val = random.choice(cand_vals)
            rep_assign_candidate = dict(rep_assign)
            rep_assign_candidate[rep] = new_val
            assignment_cand, conflicts_cand = propagate_from_rep_assign(rep_assign_candidate, orbits, group_raw, group_map, per_cell)
            if conflicts_cand >= 1_000_000:
                cand_score = 10**9
            else:
                cand_score = conflict_score_full(assignment_cand, n, per_cell, group_map)
            # accept if better or by simulated annealing probability
            if cand_score <= score or random.random() < 0.001:
                rep_assign = rep_assign_candidate
                assignment = assignment_cand
                score = cand_score
                if score < best_score:
                    best_score = score
                    best_global = dict(assignment)
            # very small temperature schedule not to get stuck
            T0 *= 0.9999

        if best_score == 0:
            break

    out_path = ROOT / "data" / "transport_local_search_result.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if best_global is None:
        res = {"status": "no_solution_found", "best_score": best_score}
        out_path.write_text(json.dumps(res, indent=2))
        print(json.dumps(res))
        return

    res = {"status": "found_candidate", "assignment": best_global, "score": best_score}
    out_path.write_text(json.dumps(res, indent=2))
    print(json.dumps(res))

    if args.verify:
        cmd = [sys.executable, str(ROOT / "scripts" / "transport_result_verify.py"), str(out_path)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        out, err = proc.communicate()
        if proc.returncode != 0:
            print("Verifier failed:\n", err)
        else:
            print(out)


if __name__ == "__main__":
    main()
