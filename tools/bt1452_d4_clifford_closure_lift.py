#!/usr/bin/env python3
"""BT1452: test the Szilassi/Fano closure lift against the D4 shear layer."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1452_d4_clifford_closure_lift.json"

STATES = [(branch, phase) for branch in range(4) for phase in range(3)]
INDEX = {s: i for i, s in enumerate(STATES)}


def perm_from_fn(fn):
    return tuple(INDEX[fn(s)] for s in STATES)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def order(p):
    ident = tuple(range(len(p)))
    cur = ident
    for n in range(1, 100):
        cur = compose(p, cur)
        if cur == ident:
            return n
    raise RuntimeError("order not found")


def closure_tau(state):
    branch, phase = state
    # tau_4 swaps the two sides of each closure pair; branch encodes side/orientation.
    return branch ^ 2, phase


def d4_shear(state):
    branch, phase = state
    return branch, (phase + branch) % 3


def generated_group(gens):
    group = {tuple(range(len(STATES)))}
    changed = True
    while changed:
        changed = False
        for a in list(group):
            for g in gens:
                for h in (compose(g, a), compose(a, g)):
                    if h not in group:
                        group.add(h)
                        changed = True
    return group


def main() -> None:
    tau = perm_from_fn(closure_tau)
    shear = perm_from_fn(d4_shear)
    comm = compose(tau, shear) == compose(shear, tau)
    conjugate = compose(compose(tau, shear), inv(tau))
    group = generated_group([tau, shear])
    order_profile = {str(o): sum(1 for g in group if order(g) == o) for o in sorted({order(g) for g in group})}
    checks = {
        "state_space_is_12": len(STATES) == 12,
        "tau_order_2": order(tau) == 2,
        "d4_shear_order_3": order(shear) == 3,
        "tau_and_shear_do_not_bare_commute": not comm,
        "tau_conjugate_shear_still_order_3": order(conjugate) == 3,
        "closure_shear_generated_group_size_18": len(group) == 18,
        "group_order_profile_expected": order_profile == {"1": 1, "2": 3, "3": 8, "6": 6},
    }
    result = {
        "bt": 1452,
        "title": "D4 Clifford closure lift",
        "verified": all(checks.values()),
        "state_model": "12 closure states = 4 side/orientation branches x 3 opposite-pair phases",
        "tau4_action": "branch -> branch xor 2, phase fixed",
        "d4_shear_action": "(branch, phase) -> (branch, phase + branch mod 3)",
        "commutation": {"bare_commutes": comm, "interpretation": "tau_4 is compatible only as a retwined/conjugating frame action, not as a bare commuting symmetry of the D4 shear."},
        "generated_group": {"size": len(group), "order_profile": order_profile},
        "conjugate_shear_order": order(conjugate),
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1452, "verified": result["verified"], "group_size": len(group), "commutes": comm}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
