"""Fail-closed Monster-word validator for the exact four-parabolic U4(2) target."""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path

EXPECTED_PAIR_ORDERS = [3, 6, 6, 6, 6, 6]
EXPECTED_TRIPLE_ORDERS = [648, 648, 648, 648]
EXPECTED_FULL_ORDER = 25_920


def load_generators(candidate):
    try:
        from mmgroup import MM, MM_from_int
    except Exception as exc:
        raise RuntimeError(f"mmgroup unavailable: {exc}") from exc
    if candidate.get("generator_strings"):
        return [MM(s) for s in candidate["generator_strings"]]
    if candidate.get("generator_integers"):
        return [MM_from_int(int(x)) for x in candidate["generator_integers"]]
    raise ValueError("candidate requires four generator_strings or generator_integers")


def closure_order(generators, cap):
    one = generators[0] ** 0
    seen = {one.as_int(): one}
    queue = [one]
    moves = list(generators) + [g ** -1 for g in generators]
    while queue:
        h = queue.pop()
        for g in moves:
            x = g * h
            key = x.as_int()
            if key not in seen:
                seen[key] = x
                queue.append(x)
                if len(seen) > cap:
                    return len(seen)
    return len(seen)


def validate(candidate):
    errors = []
    if candidate.get("status") != "CANDIDATE":
        return {"status": "PENDING", "promotable": False, "errors": ["no candidate Monster words supplied"]}
    try:
        gens = load_generators(candidate)
    except Exception as exc:
        return {"status": "FAILED", "promotable": False, "errors": [str(exc)]}
    if len(gens) != 4:
        errors.append(f"expected four generators, observed {len(gens)}")
        return {"status": "FAILED", "promotable": False, "errors": errors}
    generator_orders = [int(g.order()) for g in gens]
    pair_orders = [int((gens[i] * gens[j]).order()) for i, j in combinations(range(4), 2)]
    triple_orders = [closure_order([gens[i] for i in triple], 648) for triple in combinations(range(4), 3)]
    full_order = closure_order(gens, 25_920)
    if generator_orders != [3, 3, 3, 3]: errors.append(f"generator orders {generator_orders}")
    if pair_orders != EXPECTED_PAIR_ORDERS: errors.append(f"pair orders {pair_orders}")
    if triple_orders != EXPECTED_TRIPLE_ORDERS: errors.append(f"triple closure orders {triple_orders}")
    if full_order != EXPECTED_FULL_ORDER: errors.append(f"full closure order {full_order}")
    if not candidate.get("class_fusion_artifact_sha256"):
        errors.append("missing independent class-fusion artifact hash")
    return {
        "status": "PASS" if not errors else "FAILED",
        "promotable": not errors,
        "generator_orders": generator_orders,
        "pair_orders": pair_orders,
        "triple_closure_orders": triple_orders,
        "full_closure_order": full_order,
        "errors": errors,
        "boundary": "Abstract closure alone does not certify the documented 5B-type Monster class fusion.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--require-candidate", action="store_true")
    args = parser.parse_args()
    result = validate(json.loads(args.candidate.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2))
    if args.require_candidate and not result["promotable"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
