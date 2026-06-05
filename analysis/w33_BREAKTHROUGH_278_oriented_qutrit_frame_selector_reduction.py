"""W(3,3) BREAKTHROUGH 278: oriented qutrit frame selector reduction.

BT277 found the residual now-fixing Fano/octonion orientation gauge:

    48 = 6 q-axis orderings * 8 lifts per ordering.

The repo's C3/Fano orientation bridge says that once a qutrit triangle is
oriented, the orientation-preserving orders are the C3 cycles and the opposite
orders are dot/dual reversals.  BT278 applies that to the BT277 axis sequences.

The six axis sequences are the six permutations of the temporal axes, each
repeated twice:

    (a,b,c,a,b,c).

Choosing an oriented temporal qutrit frame means choosing one starting axis and
one C3 orientation, for example

    (0,1,2,0,1,2).

Exactly eight Fano/octonion lifts remain.  That eight equals the BT272
Mobius-Kantor selector count 2^q.  So the selector atlas is precisely the
residual lift set after the now cap, temporal axes, and oriented qutrit frame
are fixed.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


Q = 3
MU = 4
LAMBDA = 2
POSITIVE_AXIS_SEQUENCE = [0, 1, 2, 0, 1, 2]
NEGATIVE_AXIS_SEQUENCE = [0, 2, 1, 0, 2, 1]


def _artifact(name: str) -> dict:
    path = ROOT / "data" / name
    if not path.exists():
        raise RuntimeError(f"missing prerequisite artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _rotations(seq: list[int]) -> set[tuple[int, ...]]:
    return {tuple(seq[index:] + seq[:index]) for index in range(Q)}


def oriented_qutrit_frame_selector_reduction_packet() -> dict:
    bt272 = _artifact("w33_BREAKTHROUGH_272_mobius_kantor_selector_classification.json")
    bt277 = _artifact("w33_BREAKTHROUGH_277_fano_orientation_gauge_stabilizer.json")

    distribution = {
        tuple(row["axis_sequence"]): row["count"]
        for row in bt277["axis_sequence_distribution"]
    }
    positive_sequences = _rotations(POSITIVE_AXIS_SEQUENCE)
    negative_sequences = _rotations(NEGATIVE_AXIS_SEQUENCE)
    positive_count = sum(distribution[sequence] for sequence in positive_sequences)
    negative_count = sum(distribution[sequence] for sequence in negative_sequences)
    selected_positive_count = distribution[tuple(POSITIVE_AXIS_SEQUENCE)]
    selected_negative_count = distribution[tuple(NEGATIVE_AXIS_SEQUENCE)]
    selector_count = bt272["mobius_kantor_selector_count"]

    checks = {
        "bt277_orientation_gauge_is_48": bt277["orientation_gauge_size"] == 48,
        "axis_sequence_patterns_are_qfactorial": len(distribution) == 6,
        "each_axis_sequence_has_2_to_q_lifts": set(distribution.values()) == {2**Q},
        "positive_c3_orientations_are_three": len(positive_sequences) == Q,
        "negative_reversal_orientations_are_three": len(negative_sequences) == Q,
        "positive_and_negative_partition_six_sequences": positive_sequences.isdisjoint(negative_sequences)
        and positive_sequences | negative_sequences == set(distribution),
        "positive_orientation_total_is_24": positive_count == 24,
        "negative_orientation_total_is_24": negative_count == 24,
        "fixing_start_axis_and_positive_orientation_leaves_8": selected_positive_count == 2**Q,
        "fixing_start_axis_and_negative_orientation_leaves_8": selected_negative_count == 2**Q,
        "selected_oriented_frame_count_matches_bt272_selectors": selected_positive_count == selector_count,
        "bt272_selector_count_is_2_to_q": selector_count == 2**Q,
        "selector_stabilizer_factorization_is_qfactorial_times_selectors": bt272["selector_stabilizer_order"]
        == 6 * selector_count
        == bt277["orientation_gauge_size"],
    }

    return {
        "breakthrough": 278,
        "title": "Oriented qutrit frame selector reduction",
        "axis_sequence_distribution": [
            {"axis_sequence": list(sequence), "count": count}
            for sequence, count in sorted(distribution.items())
        ],
        "positive_c3_sequences": [list(sequence) for sequence in sorted(positive_sequences)],
        "negative_reversal_sequences": [list(sequence) for sequence in sorted(negative_sequences)],
        "positive_orientation_lift_count": positive_count,
        "negative_orientation_lift_count": negative_count,
        "selected_positive_axis_sequence": POSITIVE_AXIS_SEQUENCE,
        "selected_positive_lift_count": selected_positive_count,
        "selected_negative_axis_sequence": NEGATIVE_AXIS_SEQUENCE,
        "selected_negative_lift_count": selected_negative_count,
        "bt272_selector_count": selector_count,
        "factorization": "48 = q! * 2^q = 6 axis orderings * 8 selector lifts",
        "architectural_reading": (
            "BT277's residual 48-element Fano/octonion gauge factors as the six "
            "possible q-axis orderings times eight lifts per ordering. Choosing "
            "an oriented temporal qutrit frame, e.g. (0,1,2,0,1,2), leaves "
            "exactly 8 = 2^q lifts, matching the BT272 Mobius-Kantor selector "
            "atlas. The selector atlas is therefore the residual octonion lift "
            "set after now cap, axes, and qutrit orientation are fixed."
        ),
        "boundary": (
            "This reduces 48 to the eight selector lifts. It does not yet choose "
            "one selector from those eight; that remaining choice should be a "
            "sign, holonomy, or composition-factor condition."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = oriented_qutrit_frame_selector_reduction_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 278: ORIENTED QUTRIT FRAME SELECTOR REDUCTION")
    print("=" * 78)
    print()
    print(f"factorization       = {packet['factorization']}")
    print(f"positive lifts      = {packet['positive_orientation_lift_count']}")
    print(f"selected frame lifts= {packet['selected_positive_lift_count']}")
    print(f"BT272 selectors     = {packet['bt272_selector_count']}")
    print(f"verified            = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_278_oriented_qutrit_frame_selector_reduction.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
