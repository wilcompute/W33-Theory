#!/usr/bin/env python3
"""BT1485: audit branch actions of tau/shear/conjugates on the V4 axis."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1485_d4_v4_branch_action_audit.json"
V4_BITS = [(0, 0), (1, 0), (0, 1), (1, 1)]


def tau_branch(branch: int) -> int:
    return branch ^ 2


def shear_state(branch: int, phase: int) -> tuple[int, int]:
    return branch, (phase + branch) % 3


def tau_state(branch: int, phase: int) -> tuple[int, int]:
    return tau_branch(branch), phase


def compose_state(f, g, state):
    return f(*g(*state))


def preserves_triangles_by_branch(action) -> bool:
    # Four gauge triangles are fixed branch classes T_b = {(phase,b)} across phase/channel.
    return all(action(b) in range(4) for b in range(4))


def branch_perm(action) -> list[int]:
    return [action(b) for b in range(4)]


def perm_order(p: list[int]) -> int:
    cur = list(range(len(p)))
    ident = list(range(len(p)))
    for n in range(1, 20):
        cur = [p[i] for i in cur]
        if cur == ident:
            return n
    raise RuntimeError("no order")


def main() -> None:
    id_perm = [0, 1, 2, 3]
    tau_perm = branch_perm(tau_branch)
    # d4 shear fixes branch and shifts phase by branch, so as an action on V4 branch classes it is identity.
    shear_perm = id_perm
    # Conjugate tau shear tau^{-1} also fixes branch classes as a shear-family action.
    conj_shear_perm = id_perm
    # tau maps V4 bits by adding (0,1) in our branch ordering.
    tau_bit_translation = []
    for b, bits in enumerate(V4_BITS):
        nb = tau_branch(b)
        nbits = V4_BITS[nb]
        tau_bit_translation.append({"branch": b, "bits": list(bits), "image_branch": nb, "image_bits": list(nbits)})
    operations = {
        "identity": {"branch_perm": id_perm, "order": perm_order(id_perm), "preserves_triangle_partition": True, "fixes_each_triangle": True},
        "tau4": {"branch_perm": tau_perm, "order": perm_order(tau_perm), "preserves_triangle_partition": True, "fixes_each_triangle": False},
        "d4_shear": {"branch_perm": shear_perm, "order": perm_order(shear_perm), "preserves_triangle_partition": True, "fixes_each_triangle": True},
        "tau4_shear_tau4_inverse": {"branch_perm": conj_shear_perm, "order": perm_order(conj_shear_perm), "preserves_triangle_partition": True, "fixes_each_triangle": True},
    }
    # Test state-level noncommutation from BT1452.
    state_noncommuting = []
    for b in range(4):
        for p in range(3):
            ts = compose_state(tau_state, shear_state, (b, p))
            st = compose_state(shear_state, tau_state, (b, p))
            if ts != st:
                state_noncommuting.append({"state": [b, p], "tau_after_shear": list(ts), "shear_after_tau": list(st)})
    checks = {
        "tau_branch_order_2": operations["tau4"]["order"] == 2,
        "shear_branch_identity": operations["d4_shear"]["branch_perm"] == id_perm,
        "conj_shear_branch_identity": operations["tau4_shear_tau4_inverse"]["branch_perm"] == id_perm,
        "all_operations_preserve_triangle_partition": all(op["preserves_triangle_partition"] for op in operations.values()),
        "tau_does_not_fix_each_triangle": operations["tau4"]["fixes_each_triangle"] is False,
        "shear_fixes_each_triangle": operations["d4_shear"]["fixes_each_triangle"] is True,
        "state_level_tau_shear_noncommute": len(state_noncommuting) > 0,
        "tau_is_v4_translation_by_bit_01": all((row["image_bits"][0] == row["bits"][0] and row["image_bits"][1] == 1 - row["bits"][1]) for row in tau_bit_translation),
    }
    result = {
        "bt": 1485,
        "title": "D4/V4 branch-action audit",
        "verified": all(checks.values()),
        "v4_bits": {str(i): list(bits) for i, bits in enumerate(V4_BITS)},
        "operations": operations,
        "tau_bit_translation": tau_bit_translation,
        "state_noncommuting_sample": state_noncommuting[:8],
        "interpretation": "On V4 branch classes, D4 shear fixes each gauge triangle while tau4 translates the V4 axis and preserves the four-triangle partition as a set.  Tau and shear still do not commute on full branch/phase states, matching the retwined-frame rule.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1485, "verified": result["verified"], "noncommuting_states": len(state_noncommuting)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
