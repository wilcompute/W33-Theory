#!/usr/bin/env python3
"""Fail-closed Monster U4(2) candidate verifier for Passes 3694-3700.

Candidate JSON schema:
{
  "generators": ["<MM word>", "<MM word>", "<MM word>", "<MM word>"]
}

Without four explicit serialized Monster words this emits PENDING only with
--allow-empty, or fails. With a candidate it closes the subgroup using
mmgroup's canonical integer encoding and checks the exact abstract signature.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import argparse
import json
from pathlib import Path

TARGET_ORDER = 25_920
TARGET_ELEMENT_ORDERS = {1: 1, 2: 315, 3: 800, 4: 3780, 5: 5184, 6: 5760, 9: 5760, 12: 4320}
TARGET_PAIR_ORDERS = [3, 6, 6, 6, 6, 6]
TARGET_TRIPLE_ORDERS = [648, 648, 648, 648]


def pending_record(candidate: Path) -> dict[str, object]:
    return {
        "schema": "w33.mmgroup_u42_candidate.v1",
        "status": "PENDING_EXPLICIT_MONSTER_WORDS",
        "candidate_path": str(candidate),
        "promoted": False,
    }


def close_subgroup(gens, MM_from_int, cap: int = TARGET_ORDER):
    one = gens[0] ** 0
    moves = gens + [g ** -1 for g in gens]
    seen = {one.as_int(): one}
    queue = deque([one])
    while queue:
        h = queue.popleft()
        for g in moves:
            x = g * h
            key = x.as_int()
            if key not in seen:
                if len(seen) >= cap:
                    raise RuntimeError(f"candidate closure exceeds cap {cap}")
                y = MM_from_int(key)
                if y.as_int() != key:
                    raise RuntimeError("mmgroup integer round-trip failed")
                seen[key] = y
                queue.append(y)
    return tuple(seen.values())


def subgroup_order(gens, MM_from_int, cap: int = TARGET_ORDER) -> int:
    return len(close_subgroup(list(gens), MM_from_int, cap=cap))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--allow-empty", action="store_true")
    args = ap.parse_args()

    if not args.candidate.exists():
        if not args.allow_empty:
            raise SystemExit("candidate JSON missing: refusing to claim a Monster embedding")
        result = pending_record(args.candidate)
    else:
        raw = json.loads(args.candidate.read_text(encoding="utf-8"))
        words = raw.get("generators", [])
        if len(words) != 4 or not all(isinstance(w, str) and w.strip() for w in words):
            raise SystemExit("candidate must contain exactly four nonempty serialized MM words")
        from mmgroup import MM, MM_from_int

        gens = [MM(w) for w in words]
        generator_orders = [int(g.order()) for g in gens]
        pair_orders = sorted(int((gens[i] * gens[j]).order()) for i, j in combinations(range(4), 2))
        triple_orders = sorted(subgroup_order([gens[j] for j in range(4) if j != i], MM_from_int, cap=TARGET_ORDER) for i in range(4))
        group = close_subgroup(gens, MM_from_int)
        census = dict(sorted(Counter(int(g.order()) for g in group).items()))
        fingerprints = []
        for g in gens:
            entry = {"order": int(g.order()), "as_int": str(g.as_int())}
            try:
                entry["chi_powers"] = list(map(int, g.chi_powers()))
            except Exception as exc:
                entry["chi_powers_error"] = repr(exc)
            fingerprints.append(entry)
        checks = {
            "four_generator_orders_3": generator_orders == [3, 3, 3, 3],
            "pair_orders_3_6x5": pair_orders == TARGET_PAIR_ORDERS,
            "triple_orders_648": triple_orders == TARGET_TRIPLE_ORDERS,
            "closure_order_25920": len(group) == TARGET_ORDER,
            "element_order_census": census == TARGET_ELEMENT_ORDERS,
        }
        result = {
            "schema": "w33.mmgroup_u42_candidate.v1",
            "status": "PASS_CONCRETE_MONSTER_U42_WORDS" if all(checks.values()) else "FAIL_CANDIDATE_SIGNATURE",
            "checks": checks,
            "generator_words": words,
            "generator_fingerprints": fingerprints,
            "generator_orders": generator_orders,
            "pair_orders": pair_orders,
            "triple_closure_orders": triple_orders,
            "closure_order": len(group),
            "element_order_census": census,
            "promoted": all(checks.values()),
        }
        if not all(checks.values()):
            raise SystemExit(json.dumps(result, indent=2, sort_keys=True))

    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
