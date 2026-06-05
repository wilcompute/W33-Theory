"""W(3,3) BREAKTHROUGH 285: e-cube pivot selector lift.

BT278 reduced the residual now-fixing Fano/octonion gauge to the eight
Mobius-Kantor selector lifts.  BT285 uses the new BT282/283 hypercube routing
interpretation to reduce those eight lifts to one.

The BT176 binary-reflected Q4 Gray clock has single-bit e-cube step word

    1,2,1,4,1,2,1,8, ...

so every two-hop even-octonion move uses the LSB pivot bit 1 plus one
non-pivot bit:

    3,5,3,9,3,5,3,9.

The path from scalar cap 0 to now cap 15 is

    0 -> 3 -> 6 -> 5 -> 12 -> 15

with two cap edges both equal 3.  Deleting those two cap edges leaves the
internal q-word

    [5,3,9].

That is exactly BT274's selector-prefix word.  In the BT273 selector atlas,
this word first forces the base direction to be

    15 xor pivot = 14,

and then selects the forward orientation, selector 7.  Therefore the e-cube
pivot routing convention is the missing lift condition:

    48 --oriented qutrit frame--> 8 --e-cube pivot--> 1.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_273_selector_phase_clock_atlas import (  # noqa: E402
    ALL_ONES,
    Q,
    selector_phase_clock_atlas_packet,
)
from analysis.w33_BREAKTHROUGH_274_gray_projection_selector_phase_lock import (  # noqa: E402
    gray_projection_selector_phase_lock_packet,
)
from analysis.w33_BREAKTHROUGH_278_oriented_qutrit_frame_selector_reduction import (  # noqa: E402
    oriented_qutrit_frame_selector_reduction_packet,
)


PIVOT_BIT = 1
FIRST_NONPIVOT_BIT = 2
ECUBE_DIMENSION_ORDER = [1, 2, 4, 8]


def _bt176_packet() -> dict:
    path = ROOT / "data" / "w33_BREAKTHROUGH_176_gray_octonion_now_fan_6way.json"
    if not path.exists():
        raise RuntimeError("BT176 JSON artifact missing; run BT176 first")
    return json.loads(path.read_text(encoding="utf-8"))


def _directions(path: list[int]) -> list[int]:
    return [path[index] ^ path[index + 1] for index in range(len(path) - 1)]


def _cyclic_directions(cycle: list[int]) -> list[int]:
    return [cycle[index] ^ cycle[(index + 1) % len(cycle)] for index in range(len(cycle))]


def ecube_pivot_selector_lift_packet() -> dict:
    bt176 = _bt176_packet()
    bt273 = selector_phase_clock_atlas_packet()
    bt274 = gray_projection_selector_phase_lock_packet()
    bt278 = oriented_qutrit_frame_selector_reduction_packet()

    gray_clock = bt176["gray4_clock"]
    gray_steps = _cyclic_directions(gray_clock)
    two_hop_pairs = [
        [gray_steps[index], gray_steps[index + 1]]
        for index in range(0, len(gray_steps), 2)
    ]
    even_projection = bt176["even_projection"]
    even_step_word = _cyclic_directions(even_projection)
    now_index = even_projection.index(ALL_ONES)
    scalar_to_now_path = even_projection[: now_index + 1]
    scalar_to_now_word = _directions(scalar_to_now_path)
    cap_direction = PIVOT_BIT ^ FIRST_NONPIVOT_BIT
    internal_q_word = scalar_to_now_word[1:-1]
    pivot_base_direction = ALL_ONES ^ PIVOT_BIT

    selector_rows = []
    prefix_matches = []
    for row in bt273["selector_rows"]:
        direction_word = _cyclic_directions(row["moving_cycle"])
        selector_row = {
            "selector_index": row["selector_index"],
            "base_direction": row["base_direction"],
            "omitted_coordinate_axis": row["omitted_coordinate_axis"],
            "moving_cycle": row["moving_cycle"],
            "direction_word": direction_word,
            "contains_pivot_alphabet": sorted(set(direction_word)) == sorted(
                PIVOT_BIT ^ bit for bit in ECUBE_DIMENSION_ORDER if bit != PIVOT_BIT
            ),
            "prefix_matches_internal_q_word": direction_word[:Q] == internal_q_word,
        }
        selector_rows.append(selector_row)
        if selector_row["prefix_matches_internal_q_word"]:
            prefix_matches.append(selector_row)

    selected = prefix_matches[0] if len(prefix_matches) == 1 else None
    base14_rows = [row for row in selector_rows if row["base_direction"] == pivot_base_direction]
    base14_orientations = [
        {
            "selector_index": row["selector_index"],
            "direction_word": row["direction_word"],
            "prefix_matches": row["prefix_matches_internal_q_word"],
        }
        for row in base14_rows
    ]

    checks = {
        "bt278_leaves_eight_selector_lifts": bt278["selected_positive_lift_count"] == 8
        and bt278["bt272_selector_count"] == 8,
        "gray_clock_uses_ecube_dimension_order": sorted(set(gray_steps)) == ECUBE_DIMENSION_ORDER,
        "gray_steps_are_reflected_pivot_schedule": gray_steps
        == [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4, 1, 2, 1, 8],
        "two_hop_pairs_all_start_with_pivot": all(pair[0] == PIVOT_BIT for pair in two_hop_pairs),
        "even_step_word_is_pivot_plus_nonpivot_schedule": even_step_word
        == [3, 5, 3, 9, 3, 5, 3, 9],
        "scalar_to_now_path_is_bt176_first_half": scalar_to_now_path == [0, 3, 6, 5, 12, 15],
        "scalar_to_now_word_has_cap_edges_3": scalar_to_now_word == [3, 5, 3, 9, 3]
        and scalar_to_now_word[0] == scalar_to_now_word[-1] == cap_direction,
        "internal_q_word_is_bt274_prefix": internal_q_word == bt274["initial_direction_word"] == [5, 3, 9],
        "pivot_base_direction_is_14": pivot_base_direction == 14,
        "base14_is_omitted_pivot_axis": all(
            row["omitted_coordinate_axis"] == PIVOT_BIT for row in base14_rows
        )
        and len(base14_rows) == 2,
        "internal_q_word_selects_unique_selector": len(prefix_matches) == 1,
        "selected_selector_is_7": selected is not None and selected["selector_index"] == 7,
        "selected_selector_matches_bt274": selected is not None
        and selected["selector_index"] == bt274["selected_selector"]["selector_index"],
        "inverse_orientation_is_selector_6_not_prefix": sorted(
            row["selector_index"] for row in base14_rows
        )
        == [6, 7]
        and any(row["selector_index"] == 6 and not row["prefix_matches_internal_q_word"] for row in base14_rows),
        "selector_reduction_is_48_to_8_to_1": bt278["selected_positive_lift_count"] == 8
        and len(prefix_matches) == 1,
    }

    return {
        "breakthrough": 285,
        "title": "E-cube pivot selector lift",
        "ecube_dimension_order": ECUBE_DIMENSION_ORDER,
        "pivot_bit": PIVOT_BIT,
        "gray4_clock": gray_clock,
        "gray_step_word": gray_steps,
        "two_hop_pairs": two_hop_pairs,
        "even_projection": even_projection,
        "even_step_word": even_step_word,
        "scalar_to_now_path": scalar_to_now_path,
        "scalar_to_now_word": scalar_to_now_word,
        "cap_direction": cap_direction,
        "internal_q_word": internal_q_word,
        "pivot_base_direction": pivot_base_direction,
        "base14_orientations": base14_orientations,
        "selected_selector": selected,
        "selector_rows": selector_rows,
        "reduction": "48 --oriented qutrit frame--> 8 --e-cube pivot--> selector 7",
        "architectural_reading": (
            "BT282/283 explain why BT274's selector prefix is not an arbitrary "
            "Gray-code accident. The binary-reflected e-cube route uses bit 1 "
            "as a pivot in every two-hop even move. The scalar-to-now segment "
            "has cap edges 3 at both ends; deleting those caps leaves [5,3,9], "
            "which forces base 14 = 15 xor pivot and uniquely selects selector "
            "7 from the eight oriented selector lifts. Thus the hypercube "
            "routing convention closes the 48 -> 8 -> 1 lift chain."
        ),
        "boundary": (
            "This proves the selector choice from the standard LSB-first "
            "binary-reflected e-cube convention. It does not yet classify all "
            "coordinate-conjugate e-cube conventions; those should give the "
            "other base directions in the BT273 atlas."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = ecube_pivot_selector_lift_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 285: E-CUBE PIVOT SELECTOR LIFT")
    print("=" * 78)
    print()
    print(f"scalar-to-now word = {packet['scalar_to_now_word']}")
    print(f"internal q-word    = {packet['internal_q_word']}")
    print(f"pivot base         = {packet['pivot_base_direction']}")
    print(f"selected selector  = {packet['selected_selector']['selector_index']}")
    print(f"verified           = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_285_ecube_pivot_selector_lift.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
