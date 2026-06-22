#!/usr/bin/env python3
"""BT1492: canonicalize the 24-state Fano/S4/D4 fiber."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1492_canonical_fano_s4_d4_fiber.json"
ANCHOR_POINT = 1


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def points() -> list[int]:
    return list(range(1, 8))


def fano_lines() -> list[tuple[int, int, int]]:
    seen: set[frozenset[int]] = set()
    lines: list[tuple[int, int, int]] = []
    for a in points():
        for b in points():
            if a >= b:
                continue
            line = frozenset((a, b, a ^ b))
            if len(line) == 3 and line not in seen:
                seen.add(line)
                lines.append(tuple(sorted(line)))
    return sorted(lines)


def apply_columns(cols: tuple[int, int, int], vector: int) -> int:
    out = 0
    for bit, image in enumerate(cols):
        if vector & (1 << bit):
            out ^= image
    return out


def gl32_perms() -> list[tuple[int, ...]]:
    perms: list[tuple[int, ...]] = []
    for c0 in points():
        for c1 in points():
            for c2 in points():
                images = [apply_columns((c0, c1, c2), point) for point in points()]
                if sorted(images) == points():
                    table = [0] * 8
                    for point, image in zip(points(), images):
                        table[point] = image
                    perms.append(tuple(table))
    return sorted(set(perms))


def image_line(
    perm: tuple[int, ...], line: tuple[int, int, int]
) -> tuple[int, int, int]:
    return tuple(sorted(perm[point] for point in line))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] if i else 0 for i in range(8))


def perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(8))
    cur = ident
    for n in range(1, 169):
        cur = compose(p, cur)
        if cur == ident:
            return n
    raise RuntimeError(f"order not found for {p}")


def small_perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    cur = ident
    for n in range(1, 25):
        cur = tuple(p[cur[i]] for i in range(len(p)))
        if cur == ident:
            return n
    raise RuntimeError(f"order not found for {p}")


def action_on_lines(
    perm: tuple[int, ...], line_basis: list[tuple[int, int, int]]
) -> tuple[int, ...]:
    index = {line: i for i, line in enumerate(line_basis)}
    return tuple(index[image_line(perm, line)] for line in line_basis)


def main() -> None:
    bt1422 = load_json("data/bt1422_fano_168_s3_optimizer_bridge.json")
    bt1487 = load_json("data/bt1487_v4_triangle_stabilizer_classifier.json")
    bt1490 = load_json("data/bt1490_fano_e6_commuting_square.json")

    lines = fano_lines()
    through_anchor = sorted(line for line in lines if ANCHOR_POINT in line)
    branch_lines = sorted(line for line in lines if ANCHOR_POINT not in line)
    base_flag_line = through_anchor[0]
    gl = gl32_perms()
    point_stabilizer = [perm for perm in gl if perm[ANCHOR_POINT] == ANCHOR_POINT]
    flag_stabilizer = [
        perm
        for perm in point_stabilizer
        if image_line(perm, base_flag_line) == base_flag_line
    ]
    cosets_by_arm = {
        str(arm_index): [
            list(perm[1:])
            for perm in point_stabilizer
            if image_line(perm, base_flag_line) == line
        ]
        for arm_index, line in enumerate(through_anchor)
    }

    s4_branch_actions = [
        action_on_lines(perm, branch_lines) for perm in point_stabilizer
    ]
    d4_branch_actions = [
        action_on_lines(perm, branch_lines) for perm in flag_stabilizer
    ]
    s4_order_profile = Counter(perm_order(perm) for perm in point_stabilizer)
    d4_order_profile = Counter(perm_order(perm) for perm in flag_stabilizer)
    s4_branch_order_profile = Counter(
        small_perm_order(action) for action in s4_branch_actions
    )
    d4_branch_order_profile = Counter(
        small_perm_order(action) for action in d4_branch_actions
    )

    anchor_profiles = []
    for anchor in points():
        through = sorted(line for line in lines if anchor in line)
        branches = sorted(line for line in lines if anchor not in line)
        base_line = through[0]
        stabilizer = [perm for perm in gl if perm[anchor] == anchor]
        flag = [perm for perm in stabilizer if image_line(perm, base_line) == base_line]
        anchor_profiles.append(
            {
                "anchor": anchor,
                "point_stabilizer": len(stabilizer),
                "flag_stabilizer": len(flag),
                "through_line_count": len(through),
                "branch_line_count": len(branches),
                "branch_action_count": len(
                    {action_on_lines(perm, branches) for perm in stabilizer}
                ),
            }
        )

    bt1487_s4_profile = {
        int(key): value
        for key, value in bt1487["groups"]["triangle_partition_stabilizer"][
            "order_profile"
        ].items()
    }
    bt1487_d4_profile = {
        int(key): value
        for key, value in bt1487["groups"]["d4_square_subgroup"][
            "order_profile"
        ].items()
    }

    checks = {
        "bt1422_fano_bridge_loaded": bt1422["verified"] is True,
        "bt1487_classifier_loaded": bt1487["verified"] is True,
        "bt1490_square_loaded": bt1490["verified"] is True,
        "fano_plane_has_7_points_7_lines": len(points()) == 7 and len(lines) == 7,
        "gl32_order_is_168": len(gl) == bt1422["counts"]["gl32_order"] == 168,
        "anchor_has_three_lines_and_four_branch_lines": len(through_anchor) == 3
        and len(branch_lines) == 4,
        "point_stabilizer_order_24": len(point_stabilizer)
        == bt1422["counts"]["point_stabilizer"]
        == 24,
        "flag_stabilizer_order_8": len(flag_stabilizer)
        == bt1422["counts"]["flag_stabilizer"]
        == 8,
        "point_stabilizer_acts_as_full_s4_on_branch_lines": len(set(s4_branch_actions))
        == 24,
        "flag_stabilizer_acts_as_d4_on_branch_lines": len(set(d4_branch_actions)) == 8,
        "s4_order_profile_matches_bt1487": dict(sorted(s4_branch_order_profile.items()))
        == bt1487_s4_profile,
        "d4_order_profile_matches_bt1487": dict(sorted(d4_branch_order_profile.items()))
        == bt1487_d4_profile,
        "point_stabilizer_splits_as_three_flag_cosets": sorted(
            len(coset) for coset in cosets_by_arm.values()
        )
        == [8, 8, 8],
        "cosets_cover_point_stabilizer": sum(
            len(coset) for coset in cosets_by_arm.values()
        )
        == len(point_stabilizer),
        "all_anchor_choices_have_same_profile": all(
            profile["point_stabilizer"] == 24
            and profile["flag_stabilizer"] == 8
            and profile["through_line_count"] == 3
            and profile["branch_line_count"] == 4
            and profile["branch_action_count"] == 24
            for profile in anchor_profiles
        ),
        "bt1490_shared_fiber_is_canonical_coset_count": bt1490["counts"]["shared_fiber"]
        == len(through_anchor) * len(flag_stabilizer)
        == 24,
    }

    result = {
        "bt": 1492,
        "title": "Canonical Fano S4/D4 24-fiber",
        "verified": all(checks.values()),
        "anchor_point": ANCHOR_POINT,
        "fano_lines": [list(line) for line in lines],
        "canonical_objects": {
            "through_anchor_lines": [list(line) for line in through_anchor],
            "v4_branch_lines_not_through_anchor": [list(line) for line in branch_lines],
            "base_flag_line": list(base_flag_line),
        },
        "groups": {
            "gl32_order": len(gl),
            "point_stabilizer_s4": {
                "order": len(point_stabilizer),
                "order_profile": dict(sorted(s4_order_profile.items())),
                "branch_action_order_profile": dict(
                    sorted(s4_branch_order_profile.items())
                ),
                "elements_as_branch_perms": [
                    list(action) for action in sorted(set(s4_branch_actions))
                ],
            },
            "flag_stabilizer_d4": {
                "order": len(flag_stabilizer),
                "order_profile": dict(sorted(d4_order_profile.items())),
                "branch_action_order_profile": dict(
                    sorted(d4_branch_order_profile.items())
                ),
                "elements_as_branch_perms": [
                    list(action) for action in sorted(set(d4_branch_actions))
                ],
            },
        },
        "canonical_fiber": {
            "identity": "point stabilizer = three anchor-line cosets of the flag stabilizer",
            "factorization": "24 = 3 Fano lines through an anchor point * 8 flag-stabilizer states",
            "cosets_by_anchor_line": cosets_by_arm,
        },
        "anchor_profiles": anchor_profiles,
        "interpretation": (
            "The 24-state fiber is no longer an index convention.  It is the "
            "point stabilizer of the Fano plane, acting as S4 on the four lines "
            "not through the anchor.  Choosing a flag splits it canonically into "
            "three lines through the anchor times an order-8 D4 flag stabilizer."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1492,
                "verified": result["verified"],
                "point_stabilizer": len(point_stabilizer),
                "flag_stabilizer": len(flag_stabilizer),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
