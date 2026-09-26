#!/usr/bin/env python3
"""Pass 10963 exact stabilizer generator/witness certificate."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10963_exact_stabilizer_generators.json"

_spec = importlib.util.spec_from_file_location(
    "p55", ROOT / "analysis/w33_pass10955_d4_halfspin_clock_bridge.py")
P55 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P55)

jd = json.loads(
    (ROOT / "data/w33_pass10959_doubled_albert_gl23_intertwiner.json")
    .read_text(encoding="utf-8"))
J = sp.Matrix([[sp.sympify(x) for x in row] for row in jd["intertwiner_J"]])
Ji = J.inv()
gd = json.loads(
    (ROOT / "data/w33_pass10961_albert_clifford9_gammas.json")
    .read_text(encoding="utf-8"))
g9 = [
    sp.Matrix([[sp.Rational(x) for x in row] for row in M])
    for M in gd["gamma9"]
]
I16 = sp.eye(16)
Z16 = sp.zeros(16)
V = [
    sp.Matrix.vstack(
        sp.Matrix.hstack(Z16, x),
        sp.Matrix.hstack(x, Z16),
    )
    for x in g9
]
G10 = sp.diag(I16, -I16)
V.append(G10)
MIX = [G10 * V[i] for i in range(9)]
P19 = V + MIX
def r32(m):
    r = sp.Matrix(P55.signed_matrix(m).tolist())
    return sp.diag(*([r] * 8))


def action(m):
    return sp.simplify(J * r32(m) * Ji)


def reconstruct_v(y):
    coeffs = [sp.simplify((x * y).trace() / 32) for x in V]
    return sum((c * x for c, x in zip(coeffs, V)), sp.zeros(32))


def reconstruct_19(y):
    out = reconstruct_v(y)
    coeffs = [sp.simplify(-(x * y).trace() / 32) for x in MIX]
    return out + sum(
        (c * x for c, x in zip(coeffs, MIX)), sp.zeros(32))
def checks(m):
    r = action(m)
    ri = r.inv()
    v_ok = []
    p_ok = []
    for x in V:
        y = sp.simplify(r * x * ri)
        v_ok.append(sp.simplify(y - reconstruct_v(y)) == sp.zeros(32))
        p_ok.append(sp.simplify(y - reconstruct_19(y)) == sp.zeros(32))
    for x in MIX:
        y = sp.simplify(r * x * ri)
        p_ok.append(sp.simplify(y - reconstruct_19(y)) == sp.zeros(32))
    return v_ok, p_ok


def main():
    b = ((1, 0), (1, 2))
    outsider = ((1, 1), (0, 1))
    bv, bp = checks(b)
    tv, tp = checks(outsider)
    assert all(bv) and all(bp)
    assert not any(tv) and not any(tp)
    out = {
        "schema": "w33.pass10963.exact-stabilizer-generators.v1",
        "field": "Q(i,sqrt(2))",
        "involution_b": [list(r) for r in b],
        "b_preserves_all_10_vectors": all(bv),
        "b_preserves_all_19_packet_generators": all(bp),
        "outsider_order3": [list(r) for r in outsider],
        "outsider_preserves_vector_generators": sum(tv),
        "outsider_preserves_packet_generators": sum(tp),
        "exact_zero_tests": True,
        "reading": (
            "b is an exact packet stabilizer; the order-3 witness lies "
            "outside both packet stabilizers"
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
