#!/usr/bin/env python3
"""BT1515: first exact gauge-cocycle law for decorated residual triples.

For a chosen automorphism g and gauge labels U_l on lines, residuals transform by
conjugated transport:

    rho'_{g l, g m} = U_{g m}^{-1} T_{g l,g m} U_{g l}

This script records the algebraic law and verifies its group-action shape on the
finite S3 residual keys.  It is a cocycle schema; applying it to all Aut(W33)
generators needs the true transported gauge labels for each automorphism.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1515_gauge_cocycle_residual_action.json"
MD = ROOT / "analysis" / "BT1515_gauge_cocycle_residual_action.md"

S3 = list(itertools.permutations(range(3)))
IDENT = (0, 1, 2)


def compose(p: tuple[int, int, int], q: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(p[i] for i in q)  # p after q


def inv(p: tuple[int, int, int]) -> tuple[int, int, int]:
    out = [0, 0, 0]
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def act(left_gauge: tuple[int, int, int], right_gauge: tuple[int, int, int], residual: tuple[int, int, int]) -> tuple[int, int, int]:
    return compose(inv(right_gauge), compose(residual, left_gauge))


def main() -> None:
    closure_ok = all(act(a, b, r) in S3 for a in S3 for b in S3 for r in S3)
    identity_ok = all(act(IDENT, IDENT, r) == r for r in S3)
    inverse_ok = all(act(inv(a), inv(b), act(a, b, r)) == r for a in S3 for b in S3 for r in S3)
    # Associativity of gauge-change composition: applying (a,b) then (c,d) equals applying composed gauges.
    assoc_failures = []
    for a in S3:
        for b in S3:
            for c in S3:
                for d in S3:
                    for r in S3:
                        left_then = act(c, d, act(a, b, r))
                        combined = act(compose(a, c), compose(b, d), r)
                        if left_then != combined:
                            assoc_failures.append({"a": a, "b": b, "c": c, "d": d, "r": r})
                            break
                    if assoc_failures:
                        break
                if assoc_failures:
                    break
            if assoc_failures:
                break
        if assoc_failures:
            break
    orbit_sizes = sorted({len({act(a, b, r) for a in S3 for b in S3}) for r in S3})
    checks = {
        "s3_size_6": len(S3) == 6,
        "closure_ok": closure_ok,
        "identity_ok": identity_ok,
        "inverse_ok": inverse_ok,
        "associativity_ok": not assoc_failures,
        "all_residual_keys_mutually_reachable_under_free_gauge": orbit_sizes == [6],
    }
    result = {
        "bt": 1515,
        "title": "Gauge-cocycle residual action",
        "verified": all(checks.values()),
        "law": "rho'_(g l,g m)=U_(g m)^(-1) T_(g l,g m) U_(g l), equivalently rho -> R^{-1} rho L on S3 residual keys",
        "finite_key_space": {"S3_size": len(S3), "identity": list(IDENT)},
        "orbit_sizes_under_free_left_right_gauge": orbit_sizes,
        "interpretation": "The residual key transforms by a left/right S3 gauge cocycle. This supplies the algebraic missing law needed before decorated Aut(W33) orbit tests can be exact.",
        "honesty_boundary": "This verifies the residual-key algebra, not the full Aut(W33) transported gauge labels. The decorated orbit computation still needs those labels for each generator.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1515 Gauge-Cocycle Residual Action\n\n"
        "Residual keys transform by `rho -> R^{-1} rho L` for right and left line gauges.  The finite S3 key-space action is closed, has identity/inverse laws, and composes associatively.\n\n"
        "This is the algebraic cocycle law; the full decorated Aut(W33) orbit test still needs transported gauge labels for each automorphism generator.\n",
        encoding="utf-8",
    )
    print(json.dumps({"bt": 1515, "verified": result["verified"], "orbit_sizes": orbit_sizes}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
