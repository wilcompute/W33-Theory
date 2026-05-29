"""Prototype symmetry-reduced CSP for a toy Heisenberg packet selector.

This script builds a small toy model of the 27-quadrangle Heisenberg packet
organized as 9 cells × 3 completions per cell. It generates a small symmetry
group (cell-local rotations + a global reflection) with corresponding actions
on the quadrangle indices and on the 3 branch labels, and then searches for a
global assignment (one branch per quadrangle) that is equivariant under the
group action and satisfies a mild local distinctness constraint (each cell's
three completions receive distinct branch labels).

This is a prototype meant to exercise symmetry-reduced CSP techniques used in
the repo's transport/holonomy search pipeline. It is intentionally small and
dependency-free.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple, Dict, Optional


def compose_perm(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    """Return composition a ∘ b (apply b, then a)."""
    return tuple(a[b[i]] for i in range(len(b)))


def compose_branch(a: Tuple[int, ...], b: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(b)))


def invert_perm(p: Tuple[int, ...]) -> Tuple[int, ...]:
    inv = [0] * len(p)
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


class GroupElement:
    def __init__(self, perm: Tuple[int, ...], branch: Tuple[int, ...]):
        self.perm = perm
        self.branch = branch

    def compose(self, other: "GroupElement") -> "GroupElement":
        return GroupElement(compose_perm(self.perm, other.perm), compose_branch(self.branch, other.branch))

    def __repr__(self) -> str:  # pragma: no cover - debug
        return f"GE(perm={self.perm[:8]}..., branch={self.branch})"


def build_toy_group() -> List[GroupElement]:
    # 9 cells, each with 3 completions -> 27 quadrangles
    n_cells = 9
    per_cell = 3
    n = n_cells * per_cell

    # identity
    identity = tuple(range(n))

    # generator 1: rotate each cell's three completions (cycle (0 1 2) inside each cell)
    rot = list(range(n))
    for cell in range(n_cells):
        base = cell * per_cell
        rot[base + 0] = base + 1
        rot[base + 1] = base + 2
        rot[base + 2] = base + 0
    rot = tuple(rot)

    # branch action for rot: 3-cycle on branch labels
    branch_rot = (1, 2, 0)

    # generator 2: global reflection reversing cell order (0<->8,1<->7, ...)
    reflect_cells = list(range(n))
    for cell in range(n_cells):
        tgt = n_cells - 1 - cell
        for j in range(per_cell):
            reflect_cells[cell * per_cell + j] = tgt * per_cell + j
    reflect_cells = tuple(reflect_cells)

    # branch action for reflection: swap branches 1 and 2 (transposition)
    branch_reflect = (0, 2, 1)

    # include identity and generators
    gens = [GroupElement(identity, (0, 1, 2)), GroupElement(rot, branch_rot), GroupElement(reflect_cells, branch_reflect)]

    # close the group
    closure = { (g.perm, g.branch) for g in gens }
    changed = True
    while changed:
        changed = False
        for a_perm, a_branch in list(closure):
            for b_perm, b_branch in list(closure):
                a = GroupElement(a_perm, a_branch)
                b = GroupElement(b_perm, b_branch)
                c = a.compose(b)
                key = (c.perm, c.branch)
                if key not in closure:
                    closure.add(key)
                    changed = True

    group = [GroupElement(p, b) for p, b in closure]
    return group


def compute_orbits(n: int, group: List[GroupElement]) -> List[List[int]]:
    seen = [False] * n
    orbits = []
    perms = [g.perm for g in group]
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
            for p in perms:
                y = p[x]
                if y not in orb:
                    stack.append(y)
        for v in orb:
            seen[v] = True
        orbits.append(sorted(orb))
    return orbits


def search_selector(n_cells: int = 9, per_cell: int = 3) -> Optional[Dict[int, int]]:
    n = n_cells * per_cell
    group = build_toy_group()
    orbits = compute_orbits(n, group)
    # representative indices
    reps = [orbit[0] for orbit in orbits]

    # precompute mapping functions: for each group element, where does rep go and how branch perm acts
    group_map = []
    for g in group:
        group_map.append((g.perm, g.branch))

    # cell structure
    cell_indices = [[cell * per_cell + j for j in range(per_cell)] for cell in range(n_cells)]

    assignment: Dict[int, int] = {}

    def propagate(rep: int, val: int) -> bool:
        # assign rep=val and propagate to entire orbit via group_map
        stack = [(rep, val)]
        while stack:
            i, v = stack.pop()
            if i in assignment:
                if assignment[i] != v:
                    return False
                continue
            assignment[i] = v
            # enforce cell-level distinctness early: if a full cell assigned and duplicates
            cell = i // per_cell
            assigned_vals = [assignment.get(idx) for idx in cell_indices[cell]]
            if all(x is not None for x in assigned_vals) and len(set(assigned_vals)) != per_cell:
                return False
            # propagate via group elements
            for perm, branch in group_map:
                j = perm[i]
                vj = branch[v]
                if j in assignment:
                    if assignment[j] != vj:
                        return False
                else:
                    stack.append((j, vj))
        return True

    def backtrack(idx: int) -> Optional[Dict[int, int]]:
        if idx >= len(reps):
            return dict(assignment)
        rep = reps[idx]
        if rep in assignment:
            return backtrack(idx + 1)
        for v in range(per_cell):
            # snapshot
            snapshot = dict(assignment)
            ok = propagate(rep, v)
            if ok:
                res = backtrack(idx + 1)
                if res is not None:
                    return res
            # restore
            assignment.clear()
            assignment.update(snapshot)
        return None

    res = backtrack(0)
    return res


def main() -> None:
    n_cells = 9
    per_cell = 3
    result = search_selector(n_cells=n_cells, per_cell=per_cell)
    out = {
        "status": "found" if result else "none",
        "n_cells": n_cells,
        "per_cell": per_cell,
        "assignment_count": len(result) if result else 0,
        "assignment": result,
    }
    out_path = Path("data") / "transport_csp_prototype_result.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
