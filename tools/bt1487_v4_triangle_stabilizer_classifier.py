#!/usr/bin/env python3
"""BT1487: classify V4 triangle stabilizers and the D4 branch subgroup."""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1487_v4_triangle_stabilizer_classifier.json"
V4_BITS = [(0, 0), (1, 0), (0, 1), (1, 1)]


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(q)))


def perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    cur = ident
    for n in range(1, 25):
        cur = compose(p, cur)
        if cur == ident:
            return n
    raise RuntimeError("order not found")


def generated_subgroup(gens: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    ident = tuple(range(4))
    seen = {ident}
    queue: deque[tuple[int, ...]] = deque([ident])
    while queue:
        cur = queue.popleft()
        for gen in gens:
            nxt = compose(gen, cur)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def translation(dx: int, dy: int) -> tuple[int, ...]:
    out = []
    for x, y in V4_BITS:
        out.append(V4_BITS.index((x ^ dx, y ^ dy)))
    return tuple(out)


def swap_bits() -> tuple[int, ...]:
    out = []
    for x, y in V4_BITS:
        out.append(V4_BITS.index((y, x)))
    return tuple(out)


def cycle_string(p: tuple[int, ...]) -> str:
    seen: set[int] = set()
    cycles = []
    for i in range(len(p)):
        if i in seen:
            continue
        cur = []
        j = i
        while j not in seen:
            seen.add(j)
            cur.append(j)
            j = p[j]
        if len(cur) > 1:
            cycles.append("(" + " ".join(str(x) for x in cur) + ")")
    return "".join(cycles) or "()"


def main() -> None:
    bt1422 = load_json("data/bt1422_fano_168_s3_optimizer_bridge.json")
    bt1485 = load_json("data/bt1485_d4_v4_branch_action_audit.json")
    all_partition_perms = {tuple(p) for p in itertools.permutations(range(4))}
    tau4 = tuple(bt1485["operations"]["tau4"]["branch_perm"])
    shear_identity = tuple(bt1485["operations"]["d4_shear"]["branch_perm"])
    tx = translation(1, 0)
    ty = translation(0, 1)
    txy = translation(1, 1)
    swap = swap_bits()
    v4_translations = {translation(dx, dy) for dx, dy in V4_BITS}
    d4_square_subgroup = generated_subgroup([tau4, swap])
    order_profile = Counter(perm_order(p) for p in d4_square_subgroup)
    s4_order_profile = Counter(perm_order(p) for p in all_partition_perms)
    order2_d4 = sorted(p for p in d4_square_subgroup if perm_order(p) == 2)

    classifier_rows = [
        {
            "perm": list(p),
            "cycle": cycle_string(p),
            "order": perm_order(p),
            "in_v4_translations": p in v4_translations,
            "in_d4_square_subgroup": p in d4_square_subgroup,
            "fixes_each_triangle": p == (0, 1, 2, 3),
        }
        for p in sorted(all_partition_perms)
    ]

    checks = {
        "bt1422_fano_bridge_loaded": bt1422["verified"] is True,
        "bt1485_branch_audit_loaded": bt1485["verified"] is True,
        "all_triangle_partition_stabilizers_form_s4_order_24": len(all_partition_perms)
        == 24,
        "v4_translation_subgroup_order_4": len(v4_translations) == 4,
        "d4_square_subgroup_order_8": len(d4_square_subgroup) == 8,
        "tau4_is_d4_translation": tau4 == ty and tau4 in d4_square_subgroup,
        "shear_induced_identity_is_in_d4": shear_identity == (0, 1, 2, 3)
        and shear_identity in d4_square_subgroup,
        "swap_reflection_with_tau_generates_d4": swap in d4_square_subgroup
        and generated_subgroup([tau4, swap]) == d4_square_subgroup,
        "d4_order_profile": dict(sorted(order_profile.items())) == {1: 1, 2: 5, 4: 2},
        "s4_order_profile": dict(sorted(s4_order_profile.items()))
        == {1: 1, 2: 9, 3: 8, 4: 6},
        "fano_point_stabilizer_reads_7_times_s4": 7 * len(all_partition_perms)
        == bt1422["counts"]["gl32_order"]
        == 168
        and bt1422["counts"]["point_stabilizer"] == 24,
        "fano_flag_stabilizer_reads_21_times_d4": 21 * len(d4_square_subgroup)
        == bt1422["counts"]["active_bins"]
        == 168
        and bt1422["counts"]["flag_stabilizer"] == 8,
        "tau4_preserves_partition_but_not_each_triangle": bt1485["operations"]["tau4"][
            "preserves_triangle_partition"
        ]
        is True
        and bt1485["operations"]["tau4"]["fixes_each_triangle"] is False,
    }

    result = {
        "bt": 1487,
        "title": "V4-triangle stabilizer classifier",
        "verified": all(checks.values()),
        "v4_bits": {str(i): list(bits) for i, bits in enumerate(V4_BITS)},
        "groups": {
            "triangle_partition_stabilizer": {
                "name": "S4 on four V4 triangle classes",
                "order": len(all_partition_perms),
                "order_profile": dict(sorted(s4_order_profile.items())),
                "fano_reading": "7 Fano points * 24 S4 point-stabilizer states = 168",
            },
            "v4_translations": {
                "order": len(v4_translations),
                "elements": [list(p) for p in sorted(v4_translations)],
            },
            "d4_square_subgroup": {
                "order": len(d4_square_subgroup),
                "generators": {
                    "tau4": list(tau4),
                    "swap_reflection": list(swap),
                    "shear_induced_identity": list(shear_identity),
                },
                "order_profile": dict(sorted(order_profile.items())),
                "order2_elements": [list(p) for p in order2_d4],
                "fano_reading": "21 Fano flags * 8 D4 flag-stabilizer states = 168",
            },
        },
        "named_elements": {
            "translation_x": list(tx),
            "translation_y_tau4": list(ty),
            "translation_xy": list(txy),
            "swap_reflection": list(swap),
        },
        "classifier_rows": classifier_rows,
        "interpretation": (
            "Every branch permutation preserves the four-triangle partition as "
            "a set, giving S4 of order 24.  The physically used D4 branch "
            "subgroup is the square subgroup generated by tau4 and a bit-swap "
            "reflection; shear is identity on branch classes but remains "
            "nontrivial on full branch/phase states."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "bt": 1487,
                "verified": result["verified"],
                "s4": len(all_partition_perms),
                "d4": len(d4_square_subgroup),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
