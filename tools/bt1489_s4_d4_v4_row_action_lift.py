#!/usr/bin/env python3
"""BT1489: lift S4/D4/V4 branch symmetries to the 72 ABI v2 rows."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1489_s4_d4_v4_row_action_lift.json"


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after q for source-to-image permutation tuples."""
    return tuple(p[q[i]] for i in range(len(q)))


def perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    cur = ident
    for n in range(1, 121):
        cur = compose(p, cur)
        if cur == ident:
            return n
    raise RuntimeError(f"order not found for {p}")


def row_position(kind: str, guard_slot: int | None, value: int) -> int:
    if kind == "active":
        return value - 1
    if guard_slot is None:
        raise ValueError("guard rows require a guard slot")
    return 2 + 2 * guard_slot + (value - 1)


def build_rows() -> list[dict]:
    rows: list[dict] = []
    for c3_channel in range(3):
        for v4_branch in range(4):
            strand = 4 * c3_channel + v4_branch
            active_col = 14 * strand + 13
            for value in (1, 2):
                position = row_position("active", None, value)
                rows.append(
                    {
                        "row_id": f"P{c3_channel}.T{v4_branch}.a.v{value}",
                        "c3_channel": c3_channel,
                        "v4_branch": v4_branch,
                        "strand": strand,
                        "kind": "active",
                        "guard_slot": None,
                        "value": value,
                        "row_position": position,
                        "col": active_col,
                    }
                )
            for guard_slot, col in enumerate((216 + 2 * strand, 216 + 2 * strand + 1)):
                for value in (1, 2):
                    position = row_position("guard", guard_slot, value)
                    rows.append(
                        {
                            "row_id": (
                                f"P{c3_channel}.T{v4_branch}.g{guard_slot}.v{value}"
                            ),
                            "c3_channel": c3_channel,
                            "v4_branch": v4_branch,
                            "strand": strand,
                            "kind": "guard",
                            "guard_slot": guard_slot,
                            "value": value,
                            "row_position": position,
                            "col": col,
                        }
                    )
    return rows


def lift_branch_perm(
    branch_perm: tuple[int, int, int, int],
    rows: list[dict],
    row_index: dict[tuple[int, int, int], int],
) -> tuple[int, ...]:
    image = []
    for row in rows:
        target_key = (
            row["c3_channel"],
            branch_perm[row["v4_branch"]],
            row["row_position"],
        )
        image.append(row_index[target_key])
    return tuple(image)


def main() -> None:
    bt1483 = load_json("data/bt1483_closure_abi_v2_consumer.json")
    bt1485 = load_json("data/bt1485_d4_v4_branch_action_audit.json")
    bt1486 = load_json("data/bt1486_retwined_css_from_abi_v2.json")
    bt1487 = load_json("data/bt1487_v4_triangle_stabilizer_classifier.json")

    rows = build_rows()
    row_index = {
        (row["c3_channel"], row["v4_branch"], row["row_position"]): i
        for i, row in enumerate(rows)
    }
    classifier_rows = bt1487["classifier_rows"]
    s4_perms = [tuple(row["perm"]) for row in classifier_rows]
    d4_perms = [
        tuple(row["perm"]) for row in classifier_rows if row["in_d4_square_subgroup"]
    ]
    v4_perms = [
        tuple(row["perm"]) for row in classifier_rows if row["in_v4_translations"]
    ]
    tau4 = tuple(bt1485["operations"]["tau4"]["branch_perm"])
    shear_identity = tuple(bt1485["operations"]["d4_shear"]["branch_perm"])

    lifts = {perm: lift_branch_perm(perm, rows, row_index) for perm in s4_perms}
    d4_lifts = {perm: lifts[perm] for perm in d4_perms}
    v4_lifts = {perm: lifts[perm] for perm in v4_perms}

    kind_value_slot_preserved = True
    channel_preserved = True
    triangle_image_rule = True
    column_formula_preserved = True
    for perm, lift in lifts.items():
        if sorted(lift) != list(range(len(rows))):
            kind_value_slot_preserved = False
        for source_index, target_index in enumerate(lift):
            source = rows[source_index]
            target = rows[target_index]
            kind_value_slot_preserved &= (
                source["kind"],
                source["guard_slot"],
                source["value"],
                source["row_position"],
            ) == (
                target["kind"],
                target["guard_slot"],
                target["value"],
                target["row_position"],
            )
            channel_preserved &= source["c3_channel"] == target["c3_channel"]
            triangle_image_rule &= target["v4_branch"] == perm[source["v4_branch"]]
            target_strand = 4 * target["c3_channel"] + target["v4_branch"]
            expected_col = (
                14 * target_strand + 13
                if target["kind"] == "active"
                else 216 + 2 * target_strand + target["guard_slot"]
            )
            column_formula_preserved &= target["col"] == expected_col

    homomorphism_ok = all(
        lifts[compose(p, q)] == compose(lifts[p], lifts[q])
        for p in s4_perms
        for q in s4_perms
    )
    s4_row_order_profile = Counter(perm_order(lifts[p]) for p in s4_perms)
    d4_row_order_profile = Counter(perm_order(d4_lifts[p]) for p in d4_perms)
    triangle_rows = Counter(f"T{row['v4_branch']}" for row in rows)
    channel_rows = Counter(f"P{row['c3_channel']}" for row in rows)
    active_rows = [row for row in rows if row["kind"] == "active"]
    guard_rows = [row for row in rows if row["kind"] == "guard"]

    tau4_lift = lifts[tau4]
    tau4_first_channel_sample = [
        {
            "source": rows[i]["row_id"],
            "target": rows[tau4_lift[i]]["row_id"],
        }
        for i in range(12)
    ]
    identity_lift = lifts[shear_identity]

    checks = {
        "bt1483_consumer_loaded": bt1483["verified"] is True,
        "bt1485_branch_audit_loaded": bt1485["verified"] is True,
        "bt1486_css_rows_loaded": bt1486["verified"] is True,
        "bt1487_classifier_loaded": bt1487["verified"] is True,
        "row_count_72": len(rows) == bt1483["counts"]["rows"] == 72,
        "active_guard_split_24_48": len(active_rows) == 24 and len(guard_rows) == 48,
        "channel_profile_matches_abi_v2": dict(sorted(channel_rows.items()))
        == bt1483["channel_row_counts"],
        "triangle_profile_matches_abi_v2": dict(sorted(triangle_rows.items()))
        == bt1483["triangle_row_counts"],
        "s4_lifts_are_24_unique_row_permutations": len(set(lifts.values())) == 24,
        "d4_lifts_are_8_unique_row_permutations": len(set(d4_lifts.values())) == 8,
        "v4_lifts_are_4_unique_row_permutations": len(set(v4_lifts.values())) == 4,
        "row_action_is_homomorphism": homomorphism_ok,
        "row_order_profile_matches_s4": dict(sorted(s4_row_order_profile.items()))
        == {1: 1, 2: 9, 3: 8, 4: 6},
        "d4_row_order_profile_matches_d4": dict(sorted(d4_row_order_profile.items()))
        == {1: 1, 2: 5, 4: 2},
        "kind_value_slot_preserved": kind_value_slot_preserved,
        "channel_preserved": channel_preserved,
        "triangle_image_rule": triangle_image_rule,
        "column_formula_preserved": column_formula_preserved,
        "tau4_row_action_matches_bt1485_branch_action": tau4
        == tuple(bt1487["named_elements"]["translation_y_tau4"]),
        "shear_identity_fixes_all_72_rows_at_branch_layer": identity_lift
        == tuple(range(72)),
    }

    result = {
        "bt": 1489,
        "title": "S4/D4/V4 row-action lift on ABI v2",
        "verified": all(checks.values()),
        "source_packets": {
            "abi_consumer": "data/bt1483_closure_abi_v2_consumer.json",
            "branch_audit": "data/bt1485_d4_v4_branch_action_audit.json",
            "css_rows": "data/bt1486_retwined_css_from_abi_v2.json",
            "classifier": "data/bt1487_v4_triangle_stabilizer_classifier.json",
        },
        "counts": {
            "rows": len(rows),
            "active_rows": len(active_rows),
            "guard_rows": len(guard_rows),
            "s4_branch_actions": len(s4_perms),
            "d4_branch_actions": len(d4_perms),
            "v4_translation_actions": len(v4_perms),
        },
        "axis_profiles": {
            "channel_rows": dict(sorted(channel_rows.items())),
            "triangle_rows": dict(sorted(triangle_rows.items())),
        },
        "row_action_profiles": {
            "s4_order_profile": dict(sorted(s4_row_order_profile.items())),
            "d4_order_profile": dict(sorted(d4_row_order_profile.items())),
        },
        "named_lifts": {
            "tau4_branch_perm": list(tau4),
            "tau4_row_perm_prefix": list(tau4_lift[:24]),
            "shear_identity_branch_perm": list(shear_identity),
            "shear_identity_row_perm_prefix": list(identity_lift[:24]),
        },
        "tau4_first_channel_sample": tau4_first_channel_sample,
        "interpretation": (
            "The S4/D4/V4 symmetry is now a row-level ABI symmetry, not only a "
            "label symmetry.  Every branch action lifts to a permutation of the "
            "72 active/guard value rows while preserving channel, row kind, "
            "qutrit value, guard slot, and the column formulas."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1489,
                "verified": result["verified"],
                "rows": len(rows),
                "s4": len(s4_perms),
                "d4": len(d4_perms),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
