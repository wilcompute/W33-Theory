"""W(3,3) BREAKTHROUGH 275: folded Gray selector transport.

BT274 proved that the corrected BT176 Gray projection chooses selector 7 from
the BT273 phase atlas.  BT275 strengthens this from a prefix match to a full
transport law.

The BT176 even projection has two-step reflected-Gray word

    [3, 5, 3, 9, 3, 5, 3, 9] = [3,5,3,9]^2.

Take each BT273 q! selector cycle, insert the fixed caps 0 and 15, and allow a
single tail reversal at the 15 cap.  Among every selector, orientation,
rotation, split, and tail mode, exactly two descriptions recover that exact
reflected-Gray word:

    selector 7 forward, split 4|2, tail reversed;
    selector 6 reversed, split 4|2, tail reversed.

These are the same base-14 inverse clock pair.  Therefore the Gray clock is not
merely compatible with the selector atlas: it is the unique folded q!-cycle
transport of the selected base-14 phase.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_273_selector_phase_clock_atlas import (  # noqa: E402
    Q,
    LAMBDA,
    selector_phase_clock_atlas_packet,
)
from analysis.w33_BREAKTHROUGH_274_gray_projection_selector_phase_lock import (  # noqa: E402
    gray_projection_selector_phase_lock_packet,
)


ALL_ONES = 15


def hamming_weight(value: int) -> int:
    return bin(value).count("1")


def cyclic_steps(cycle: list[int]) -> list[int]:
    return [cycle[index] ^ cycle[(index + 1) % len(cycle)] for index in range(len(cycle))]


def rotations(cycle: list[int]) -> list[tuple[int, list[int]]]:
    return [(index, cycle[index:] + cycle[:index]) for index in range(len(cycle))]


def cap_splice_rows() -> list[dict]:
    bt273 = selector_phase_clock_atlas_packet()
    rows = []
    for selector in bt273["selector_rows"]:
        for orientation, cycle in (
            ("atlas_forward", selector["moving_cycle"]),
            ("atlas_reverse", list(reversed(selector["moving_cycle"]))),
        ):
            for rotation_index, rotated in rotations(cycle):
                for split_index in range(1, len(rotated)):
                    head = rotated[:split_index]
                    tail = rotated[split_index:]
                    for tail_mode, spliced_tail in (
                        ("same", tail),
                        ("reverse", list(reversed(tail))),
                    ):
                        projection = [0] + head + [ALL_ONES] + spliced_tail
                        rows.append(
                            {
                                "selector_index": selector["selector_index"],
                                "base_direction": selector["base_direction"],
                                "orientation": orientation,
                                "rotation_index": rotation_index,
                                "split_index": split_index,
                                "head_length": len(head),
                                "tail_length": len(spliced_tail),
                                "tail_mode": tail_mode,
                                "projection": projection,
                                "step_word": cyclic_steps(projection),
                            }
                        )
    return rows


def folded_gray_selector_transport_packet() -> dict:
    bt274 = gray_projection_selector_phase_lock_packet()
    projection = bt274["bt176_even_projection"]
    target_step_word = cyclic_steps(projection)
    reflected_gray_period = target_step_word[:4]
    selected_cycle = bt274["selected_selector"]["moving_cycle"]
    selected_head = selected_cycle[: Q + 1]
    selected_tail = selected_cycle[Q + 1 :]
    folded_from_selector_7 = [0] + selected_head + [ALL_ONES] + list(reversed(selected_tail))

    splice_rows = cap_splice_rows()
    exact_step_matches = [row for row in splice_rows if row["step_word"] == target_step_word]
    exact_projection_matches = [row for row in splice_rows if row["projection"] == projection]
    forward_matches = [
        row
        for row in exact_step_matches
        if row["selector_index"] == 7
        and row["orientation"] == "atlas_forward"
        and row["rotation_index"] == 0
    ]
    inverse_matches = [
        row
        for row in exact_step_matches
        if row["selector_index"] == 6 and row["orientation"] == "atlas_reverse"
    ]

    cap_directions = {
        "real_cap_to_head": projection[0] ^ projection[1],
        "head_to_all_ones_cap": selected_head[-1] ^ ALL_ONES,
    }
    target_rows = [
        {
            "selector_index": row["selector_index"],
            "base_direction": row["base_direction"],
            "orientation": row["orientation"],
            "rotation_index": row["rotation_index"],
            "split_index": row["split_index"],
            "head_length": row["head_length"],
            "tail_length": row["tail_length"],
            "tail_mode": row["tail_mode"],
            "projection": row["projection"],
            "step_word": row["step_word"],
        }
        for row in exact_step_matches
    ]

    checks = {
        "bt176_projection_is_folded_selector_7": projection == folded_from_selector_7,
        "target_step_word_is_reflected_gray_period_squared": target_step_word
        == reflected_gray_period * LAMBDA
        == [3, 5, 3, 9, 3, 5, 3, 9],
        "target_steps_are_two_bit_internal_moves": all(
            hamming_weight(step) == 2 for step in target_step_word
        ),
        "selected_cycle_has_selector_word_repeated": cyclic_steps(selected_cycle)
        == [5, 3, 9, 5, 3, 9],
        "fold_split_is_q_plus_1_by_q_minus_1": len(selected_head) == Q + 1
        and len(selected_tail) == Q - 1,
        "both_caps_use_same_direction_3": cap_directions
        == {"real_cap_to_head": 3, "head_to_all_ones_cap": 3},
        "cap_splice_search_space_is_960": len(splice_rows) == 960,
        "exact_step_word_has_two_representations": len(exact_step_matches) == LAMBDA,
        "exact_projection_has_two_representations": len(exact_projection_matches) == LAMBDA,
        "two_representations_are_base_14_pair": sorted(
            (row["selector_index"], row["base_direction"]) for row in exact_step_matches
        )
        == [(6, 14), (7, 14)],
        "forward_representation_is_selector_7": len(forward_matches) == 1
        and forward_matches[0]["split_index"] == Q + 1
        and forward_matches[0]["tail_mode"] == "reverse",
        "inverse_representation_is_selector_6_reverse": len(inverse_matches) == 1
        and inverse_matches[0]["split_index"] == Q + 1
        and inverse_matches[0]["tail_mode"] == "reverse",
        "all_step_matches_equal_bt176_projection": all(
            row["projection"] == projection for row in exact_step_matches
        ),
    }

    return {
        "breakthrough": 275,
        "title": "Folded Gray selector transport",
        "bt176_even_projection": projection,
        "target_step_word": target_step_word,
        "reflected_gray_period": reflected_gray_period,
        "selected_selector_7_cycle": selected_cycle,
        "selected_cycle_step_word": cyclic_steps(selected_cycle),
        "folded_from_selector_7": folded_from_selector_7,
        "fold_split": {"head": Q + 1, "tail": Q - 1},
        "cap_directions": cap_directions,
        "cap_splice_search_space": len(splice_rows),
        "exact_step_match_count": len(exact_step_matches),
        "exact_projection_match_count": len(exact_projection_matches),
        "exact_step_matches": target_rows,
        "architectural_reading": (
            "BT274's selector choice is promoted to a full transport law. The "
            "BT176 even Gray projection is exactly selector 7's q!-cycle folded "
            "through the fixed caps 0 and 15 with a q+1 by q-1 split. The full "
            "reflected-Gray two-step word [3,5,3,9]^2 is recovered by exactly "
            "the base-14 inverse pair: selector 7 forward and selector 6 "
            "reversed. Thus the physical now-clock is a folded, orientation-"
            "resolved q!-cycle, not an arbitrary traversal of the octonion "
            "frame."
        ),
        "boundary": (
            "This theorem is internal to the F2^4/Gray/selector carrier. The "
            "next target is to identify which W(3,3) now-fan labels realize the "
            "two fixed caps and the q+1|q-1 fold."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = folded_gray_selector_transport_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 275: FOLDED GRAY SELECTOR TRANSPORT")
    print("=" * 78)
    print()
    print(f"BT176 projection      = {packet['bt176_even_projection']}")
    print(f"target step word      = {packet['target_step_word']}")
    print(f"selector 7 cycle      = {packet['selected_selector_7_cycle']}")
    print(f"exact step matches    = {packet['exact_step_match_count']}")
    print(f"verified              = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_275_folded_gray_selector_transport.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
