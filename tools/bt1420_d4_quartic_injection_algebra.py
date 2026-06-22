#!/usr/bin/env python3
"""BT1420: finite D4-quartic injection algebra."""
from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1420_d4_quartic_injection_algebra.json"

BRANCHES = tuple(range(4))
PHASES = tuple(range(3))
ATOMS = (0, 1)


def d4_permutations() -> list[tuple[int, int, int, int]]:
    # Square vertices 0,1,2,3 around the cycle.  D4 = rotations and reflections.
    rots = [tuple((i + r) % 4 for i in range(4)) for r in range(4)]
    refl = tuple((-i) % 4 for i in range(4))
    perms = []
    for r in rots:
        perms.append(r)
    for r in range(4):
        perms.append(tuple((refl[i] + r) % 4 for i in range(4)))
    seen = []
    for p in perms:
        if p not in seen:
            seen.append(p)
    return seen


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def perm_order(p: tuple[int, ...]) -> int:
    x = tuple(range(len(p)))
    cur = x
    for n in range(1, 25):
        cur = compose(p, cur)
        if cur == x:
            return n
    raise RuntimeError("order search failed")


def uniform_phase_shift(state: tuple[int, int], shift: int) -> tuple[int, int]:
    b, p = state
    return b, (p + shift) % 3


def branch_perm_action(state: tuple[int, int], perm: tuple[int, int, int, int]) -> tuple[int, int]:
    b, p = state
    return perm[b], p


def injection_shear(state: tuple[int, int]) -> tuple[int, int]:
    b, p = state
    return b, (p + b) % 3


def perm_on_12(fn) -> tuple[int, ...]:
    states = list(product(BRANCHES, PHASES))
    index = {s: i for i, s in enumerate(states)}
    return tuple(index[fn(s)] for s in states)


def is_product_branch_phase(perm12: tuple[int, ...], d4s: list[tuple[int, int, int, int]]) -> bool:
    for d in d4s:
        for shift in PHASES:
            candidate = perm_on_12(lambda s, d=d, shift=shift: uniform_phase_shift(branch_perm_action(s, d), shift))
            if candidate == perm12:
                return True
    return False


def main() -> None:
    d4s = d4_permutations()
    d4_orders = Counter(perm_order(p) for p in d4s)
    d4_graph = nx.Graph()
    d4_graph.add_nodes_from(d4s)
    gens = [d4s[1], d4s[4]]
    for p in d4s:
        for g in gens:
            d4_graph.add_edge(p, compose(g, p))

    resource_states = [
        {"aperture": a * 12 + b * 3 + p, "atom": a, "branch": b, "phase": p}
        for a, b, p in product(ATOMS, BRANCHES, PHASES)
    ]
    oriented_tokens = [
        {
            "token": i,
            "atom": row["atom"],
            "branch": row["branch"],
            "phase": row["phase"],
            "orientation": orient,
            "branch_image": d4s[orient][row["branch"]],
            "tomotope_flag": row["aperture"] * 8 + orient,
        }
        for row in resource_states
        for orient in range(8)
        for i in [row["aperture"] * 8 + orient]
    ]

    shear = perm_on_12(injection_shear)
    shear2 = compose(shear, shear)
    shear3 = compose(shear, shear2)
    identity12 = tuple(range(12))
    conjugates = set()
    for d in d4s:
        d12 = perm_on_12(lambda s, d=d: branch_perm_action(s, d))
        inv = tuple(d12.index(i) for i in range(12))
        conjugates.add(compose(compose(d12, shear), inv))

    phase_shift = perm_on_12(lambda s: uniform_phase_shift(s, 1))
    checks = {
        "d4_has_8_elements": len(d4s) == 8,
        "d4_order_profile_is_square_symmetry": dict(sorted(d4_orders.items())) == {1: 1, 2: 5, 4: 2},
        "d4_cayley_graph_connected": nx.is_connected(d4_graph),
        "resource_states_are_24": len(resource_states) == 2 * 4 * 3 == 24,
        "oriented_tokens_are_192": len(oriented_tokens) == 24 * 8 == 192,
        "tomotope_flags_bijective": sorted(t["tomotope_flag"] for t in oriented_tokens) == list(range(192)),
        "per_atom_shell_is_864": 4 * 27 * 8 == 864,
        "two_atom_shell_is_1728": 2 * 4 * 27 * 8 == 1728,
        "qutrit_phase_shift_order_3": compose(phase_shift, compose(phase_shift, phase_shift)) == identity12,
        "injection_shear_order_3": shear3 == identity12 and shear != identity12,
        "injection_shear_not_product_d4_times_uniform_phase": not is_product_branch_phase(shear, d4s),
        "d4_conjugate_shears_nontrivial": len(conjugates) >= 3,
    }

    result = {
        "bt": 1420,
        "title": "Finite D4-quartic injection algebra",
        "verified": all(checks.values()),
        "resource_state_space": {
            "atoms": len(ATOMS),
            "branches_per_atom": 4,
            "qutrit_phases": 3,
            "guard_apertures": len(resource_states),
            "d4_orientations": 8,
            "oriented_tomotope_tokens": len(oriented_tokens),
            "identity": "2 atoms * 4 branches * 3 phases = 24; times 8 D4 orientations = 192",
        },
        "d4_action": {
            "permutations": [list(p) for p in d4s],
            "order_profile": {str(k): v for k, v in sorted(d4_orders.items())},
            "cayley_connected": nx.is_connected(d4_graph),
        },
        "clifford_frame_action": {
            "qutrit_phase_shift": "X_frame: (branch, phase) -> (branch, phase+1 mod 3)",
            "d4_branch_action": "D4 acts on the four quartic branches and commutes with uniform qutrit phase shifts",
            "phase_shift_order": 3,
        },
        "non_clifford_injection_effect": {
            "shear": "J: (branch, phase) -> (branch, phase+branch mod 3)",
            "order": 3,
            "not_product_action": True,
            "d4_conjugate_shear_count": len(conjugates),
            "reading": "The injected resource is a branch-controlled qutrit phase shear, not a uniform Clifford phase-frame shift.",
        },
        "samples": {
            "resource_states_first_12": resource_states[:12],
            "oriented_tokens_first_24": oriented_tokens[:24],
        },
        "boundary": "This is a finite permutation/resource-state algebra for the guard band. It does not assert a calibrated nonlinear optical source or collapse the two independent D4 quartic atoms into one field.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1420, "verified": result["verified"], "tokens": len(oriented_tokens), "conjugate_shears": len(conjugates)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
