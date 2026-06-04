"""W(3,3) BREAKTHROUGH 274: Gray projection selector phase lock.

BT176 repaired the Gray-octonion clock: the 16-tick Q4 Gray clock alternates
parity, and the even octonion frame is the every-other-tick projection

    [0, 3, 6, 5, 12, 15, 10, 9].

BT273 classified the 8 Mobius-Kantor selectors as

    8 = mu * lambda = 4 base directions * 2 orientations.

BT274 connects them.  The corrected BT176 even projection supplies the first
q = 3 internal direction word before the all-ones fixed point:

    [3, 6, 5, 12] has XOR directions [5, 3, 9].

Among the 8 BT273 selector q!-cycles:

    exactly 2 have direction alphabet {3,5,9}, and both have base 14;
    exactly 1 has the forward prefix [5,3,9].

That unique selector is BT273 selector 7.  Therefore the corrected Gray
projection clock selects one phase from the 8-selector atlas: base direction
14 and forward q!-orientation.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_273_selector_phase_clock_atlas import (  # noqa: E402
    Q,
    QFACT,
    selector_phase_clock_atlas_packet,
)


ALL_ONES = 15


def _bt176_packet() -> dict:
    path = ROOT / "data" / "w33_BREAKTHROUGH_176_gray_octonion_now_fan_6way.json"
    if not path.exists():
        raise RuntimeError("BT176 JSON artifact missing; run BT176 repair verifier first")
    return json.loads(path.read_text(encoding="utf-8"))


def _cyclic_directions(cycle: list[int]) -> list[int]:
    return [cycle[index] ^ cycle[(index + 1) % len(cycle)] for index in range(len(cycle))]


def gray_projection_selector_phase_lock_packet() -> dict:
    bt176 = _bt176_packet()
    bt273 = selector_phase_clock_atlas_packet()

    even_projection = bt176["even_projection"]
    all_ones_index = even_projection.index(ALL_ONES)
    initial_segment = [vertex for vertex in even_projection[:all_ones_index] if vertex != 0]
    initial_direction_word = [
        initial_segment[index] ^ initial_segment[index + 1]
        for index in range(len(initial_segment) - 1)
    ]
    direction_alphabet = sorted(set(initial_direction_word))

    selector_rows = []
    alphabet_matches = []
    prefix_matches = []
    for row in bt273["selector_rows"]:
        directions = _cyclic_directions(row["moving_cycle"])
        selector_row = {
            "selector_index": row["selector_index"],
            "base_direction": row["base_direction"],
            "moving_cycle": row["moving_cycle"],
            "direction_word": directions,
            "direction_alphabet": sorted(set(directions)),
            "alphabet_matches_bt176": sorted(set(directions)) == direction_alphabet,
            "prefix_matches_bt176": directions[:Q] == initial_direction_word,
        }
        selector_rows.append(selector_row)
        if selector_row["alphabet_matches_bt176"]:
            alphabet_matches.append(selector_row)
        if selector_row["prefix_matches_bt176"]:
            prefix_matches.append(selector_row)

    selected = prefix_matches[0] if len(prefix_matches) == 1 else None
    alphabet_base_distribution = Counter(row["base_direction"] for row in alphabet_matches)

    checks = {
        "bt176_projection_has_8_ticks": len(even_projection) == 8,
        "bt176_projection_starts_at_real_unit": even_projection[0] == 0,
        "bt176_projection_contains_all_ones": ALL_ONES in even_projection,
        "initial_segment_has_q_plus_1_vertices": len(initial_segment) == Q + 1,
        "initial_direction_word_has_q_entries": len(initial_direction_word) == Q,
        "initial_direction_alphabet_has_q_entries": len(direction_alphabet) == Q,
        "selector_atlas_has_8_rows": len(selector_rows) == 8,
        "alphabet_rule_selects_lambda_orientations": len(alphabet_matches) == 2,
        "alphabet_rule_selects_base_14": alphabet_base_distribution == {14: 2},
        "prefix_rule_selects_unique_orientation": len(prefix_matches) == 1,
        "selected_selector_is_7": selected is not None and selected["selector_index"] == 7,
        "selected_cycle_has_qfactorial_length": selected is not None
        and len(selected["moving_cycle"]) == QFACT,
    }

    return {
        "breakthrough": 274,
        "title": "Gray projection selector phase lock",
        "bt176_even_projection": even_projection,
        "initial_segment_before_all_ones": initial_segment,
        "initial_direction_word": initial_direction_word,
        "initial_direction_alphabet": direction_alphabet,
        "alphabet_match_count": len(alphabet_matches),
        "alphabet_match_selectors": [
            {
                "selector_index": row["selector_index"],
                "base_direction": row["base_direction"],
                "direction_word": row["direction_word"],
            }
            for row in alphabet_matches
        ],
        "selected_selector": selected,
        "selector_rows": selector_rows,
        "architectural_reading": (
            "The corrected BT176 Gray projection now chooses a BT273 selector "
            "phase. Its first q=3 internal direction word [5,3,9] first narrows "
            "the 8-selector atlas to the two orientations at base direction 14, "
            "then selects the forward orientation, selector 7. Thus the physical "
            "clock phase is not arbitrary inside the F2^4 carrier: the Gray "
            "projection chooses base 14 and one q!-cycle orientation."
        ),
        "boundary": (
            "This locks the selector phase inside the F2^4/Q4 model. The next "
            "target is to pull the selected base-14 phase back to W(3,3)'s "
            "now-fan and center-quad labels."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = gray_projection_selector_phase_lock_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 274: GRAY PROJECTION SELECTOR PHASE LOCK")
    print("=" * 78)
    print()
    print(f"BT176 initial directions = {packet['initial_direction_word']}")
    print(f"alphabet matches         = {packet['alphabet_match_selectors']}")
    print(f"selected selector        = {packet['selected_selector']['selector_index']}")
    print(f"selected base            = {packet['selected_selector']['base_direction']}")
    print(f"verified                 = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_274_gray_projection_selector_phase_lock.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
