#!/usr/bin/env python3
"""BT943 - A2-plane Weyl lift attempt for the tetracode E8 selector.

BT940 separated the tetracode monomial group into an S4 block quotient and a
scalar/A2-plane component that is invisible on the mod-2 chain shadow unless an
A2-plane lift is chosen.  BT943 constructs the explicit A2 Weyl generators in
simple-root coordinates and records their mod-2 action.

Result: each A2 plane has Weyl group W(A2)=S3, which reduces mod 2 to GL(2,2).
These local Weyl actions are valid on tetracode metric coordinates.  The part
that is canonical on H is the induced GL(2,2) block action after choosing the
BT930 tetracode gauge; a chain-complex action on representatives still needs a
chosen lift from H classes to integral A2 roots.
"""
from __future__ import annotations
import json
from itertools import product
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt943_a2_plane_weyl_lift.json"

A2_GRAM = np.array([[2, -1], [-1, 2]], dtype=int)
S1 = np.array([[-1, 1], [0, 1]], dtype=int)   # reflection in alpha_1
S2 = np.array([[1, 0], [1, -1]], dtype=int)   # reflection in alpha_2


def mat_tuple(M):
    return tuple(int(x) for x in M.reshape(-1))


def closure(gens, mod=None):
    I = np.eye(gens[0].shape[0], dtype=int)
    seen = {mat_tuple(I): I}
    frontier = [I]
    while frontier:
        A = frontier.pop()
        for G in gens:
            B = A @ G
            if mod is not None:
                B %= mod
            key = mat_tuple(B)
            if key not in seen:
                seen[key] = B.copy()
                frontier.append(B.copy())
    return list(seen.values())


def main() -> None:
    W_int = closure([S1, S2])
    W_mod2 = closure([S1 % 2, S2 % 2], mod=2)
    preserves_integral = all(np.array_equal(M.T @ A2_GRAM @ M, A2_GRAM) for M in W_int)
    J = np.array([[0, 1], [1, 0]], dtype=int)
    preserves_mod2 = all(np.array_equal((M.T @ (A2_GRAM % 2) @ M) % 2, A2_GRAM % 2) for M in W_mod2)
    # Four independent planes would give S3^4 locally; the tetracode monomial
    # group constrains this through the code-glue condition.
    result = {
        "theorem": "BT943 A2-plane Weyl lift attempt",
        "A2_gram": A2_GRAM.tolist(),
        "simple_reflections": {"s1": S1.tolist(), "s2": S2.tolist()},
        "integral_WA2_order": len(W_int),
        "integral_WA2_preserves_gram": bool(preserves_integral),
        "mod2_WA2_order": len(W_mod2),
        "mod2_WA2_matrices": [M.astype(int).tolist() for M in W_mod2],
        "mod2_WA2_preserves_A2_form": bool(preserves_mod2),
        "four_plane_local_order": 6**4,
        "tetracode_monomial_order_from_BT940": 48,
        "survives_to_chain_H": "After choosing the BT930 tetracode gauge, the local A2 Weyl generators reduce to GL(2,2) actions on each 2-coordinate plane. They act on H as gauge-dependent block operations; they are not yet canonical chain-complex maps on representatives.",
        "exact_boundary": "BT943 constructs the A2-plane Weyl lift in tetracode metric coordinates. It does not prove that all local Weyl choices preserve the ternary tetracode glue or define canonical chain-complex automorphisms.",
        "next_test": "Intersect the four-plane W(A2)^4 action with the tetracode code-glue stabilizer and then transport that stabilizer through BT930 to H.",
        "checks": {"T1_integral_WA2_order_6": len(W_int)==6, "T2_integral_gram_preserved": bool(preserves_integral), "T3_mod2_GL22_order_6": len(W_mod2)==6, "T4_four_plane_local_order_recorded": 6**4==1296, "T5_chain_canonicality_not_overclaimed": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT943 wrote", OUT)

if __name__ == "__main__":
    main()
