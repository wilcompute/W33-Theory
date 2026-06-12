#!/usr/bin/env python3
"""BT775 — PG(3,2) equivariance obstruction verifier.

BT772 gave a PG(3,2)-labeled coordinate frame for the 15-sector by reducing
W33 point coordinates F_3^4 -> F_2^4.  This verifier tests the stronger
question: is that labeling equivariant for the full W33 automorphism group
Sp(4,3)?

Answer: no.  A single symplectic transvection already gives a counterexample.
So the PG(3,2) labels are a canonical coordinate gauge for the 15-sector, not
a full Sp(4,3)-equivariant quotient.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from bt766_intrinsic_k44_octet_quotient import build_w33

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT775_PG32_EQUIVARIANCE_OBSTRUCTION_summary.json"
MOD = 3
J = np.array(
    [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]], dtype=int
) % MOD


def norm(v):
    v = tuple(int(x) % MOD for x in v)
    for x in v:
        if x % MOD:
            s = 1 if x % MOD == 1 else 2
            return tuple((s * y) % MOD for y in v)
    raise ValueError("zero vector")


def apply_matrix(M, p):
    return norm(tuple((M @ np.array(p, dtype=int)) % MOD))


def transvection(v, s=1):
    """Symplectic transvection x |-> x + s*<x,v>*v for column vectors."""
    vv = np.array(v, dtype=int).reshape(4, 1)
    Jv = (J @ vv) % MOD
    return (np.eye(4, dtype=int) + s * (vv @ Jv.T)) % MOD


def pg_label(p):
    return tuple(int(x) % 2 for x in p)


def is_label_equivariant(M, pts, idx):
    labels = [pg_label(p) for p in pts]
    induced = {}
    for pid, p in enumerate(pts):
        source = labels[pid]
        target = labels[idx[apply_matrix(M, p)]]
        if source in induced and induced[source] != target:
            return False, {
                "source_label": list(source),
                "first_target_label": list(induced[source]),
                "second_point": list(p),
                "second_target_point": list(apply_matrix(M, p)),
                "second_target_label": list(target),
            }
        induced[source] = target
    return len(induced) == 15 and len(set(induced.values())) == 15, induced


def main():
    pts, lines, idx, G, point_lines = build_w33()

    # The smallest visible obstruction: transvection along the projective point e4.
    v = (0, 0, 0, 1)
    T = transvection(v, 1)
    symplectic_ok = np.array_equal((T.T @ J @ T) % MOD, J)
    point_perm_ok = sorted(apply_matrix(T, p) for p in pts) == sorted(pts)
    equivariant, witness = is_label_equivariant(T, pts, idx)

    # Sanity: identity is equivariant, so failure is not a bug in the test.
    identity_ok, _ = is_label_equivariant(np.eye(4, dtype=int), pts, idx)

    checks = {
        "identity_is_equivariant": identity_ok,
        "counterexample_matrix_is_symplectic": bool(symplectic_ok),
        "counterexample_permutes_W33_projective_points": bool(point_perm_ok),
        "counterexample_breaks_mod2_label_equivariance": equivariant is False,
    }

    result = {
        "theorem": "BT775 PG(3,2) Equivariance Obstruction Theorem",
        "question": "Do the BT772 mod-2 PG(3,2) labels define a full Sp(4,3)-equivariant quotient?",
        "answer": "No: full equivariance is falsified by a symplectic transvection.",
        "counterexample": {
            "transvection_vector": list(v),
            "matrix_mod_3": T.astype(int).tolist(),
            "witness": witness,
        },
        "interpretation": "The PG(3,2) labels are a useful coordinate gauge for the 15-sector, not a full W33 automorphism quotient. The obstruction is structural and should be tracked rather than hidden.",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This falsifies full Sp(4,3)-equivariance only. It does not classify the subgroup preserving the PG(3,2) labels."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
