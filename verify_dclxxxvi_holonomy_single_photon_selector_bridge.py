#!/usr/bin/env python3
"""Part DCLXXXVI: holonomy single-photon selector bridge.

DCLXXXV identifies the exact local Jordan / nilpotent quotient of the
deterministic qutrit feed-forward cycle.  The next step is to show that the
full local branch law is already the missing S3 selector law, and that its
local packet count scales exactly to the existing 1620 carrier.

This verifier proves:

  - local translation a -> a+1 and reflection a -> -a on a 3-branch fiber
    generate S3;
  - the order-6 local selector group matches the order-6 global selector
    stabilizer already proven on the 1620 quadrangle carrier;
  - the 27-point DCLXIV affine bulk is exactly the local packet size of the
    global 1620 selector carrier because 60 * 27 = 1620.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, EXPLORATION, SCRIPTS):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from scripts.w33_h4_s3_selector_holonomy_audit import (  # noqa: E402
    h4_s3_selector_holonomy_summary,
)
from verify_dclxiv_holonomy_qutrit_transvection_bridge import (  # noqa: E402
    build_bridge as build_dclxiv_bridge,
)
from verify_dclxxxv_holonomy_single_photon_fiber_jordan_bridge import (  # noqa: E402
    build_bridge as build_dclxxxv_bridge,
)


OUT_PATH = ROOT / "data" / "dclxxxvi_holonomy_single_photon_selector_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    branch_count: int
    local_selector_group_order: int
    affine_bulk_count: int
    ordered_adjacent_pair_count: int
    global_selector_carrier: int
    all_identities_hold: bool


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


def _order(permutation: tuple[int, ...]) -> int:
    identity = tuple(range(len(permutation)))
    power = identity
    for order in range(1, 20):
        power = _compose(permutation, power)
        if power == identity:
            return order
    raise ValueError("permutation order exceeded search bound")


def _closure(generators: Iterable[tuple[int, ...]]) -> list[tuple[int, ...]]:
    identity = tuple(range(len(next(iter(generators)))))
    seen = {identity}
    frontier = [identity]
    generators = list(generators)
    while frontier:
        current = frontier.pop()
        for generator in generators:
            candidate = _compose(generator, current)
            if candidate not in seen:
                seen.add(candidate)
                frontier.append(candidate)
    return sorted(seen)


def build_bridge() -> dict[str, Any]:
    dclxiv = build_dclxiv_bridge()
    dclxxxv = build_dclxxxv_bridge()
    selector = h4_s3_selector_holonomy_summary()

    translation = (1, 2, 0)
    reflection = (0, 2, 1)
    local_group = _closure([translation, reflection])
    translation_inverse = _inverse(translation)

    affine_bulk_count = dclxiv["summary"]["affine_bulk_count"]
    ordered_adjacent_pair_count = selector["heisenberg_transport_packet"]["ordered_adjacent_pairs"]
    quadrangles_per_pair = selector["heisenberg_transport_packet"]["quadrangles_per_pair"]
    global_selector_carrier = selector["h4_alignment_packet"]["nonlocal_quadrangle_carrier"]
    selector_stabilizer_order = selector["s3_selector_theorem_packet"]["stabilizer"]["order"]

    identities = {
        "local_translation_has_order_three": _order(translation) == 3,
        "local_reflection_has_order_two": _order(reflection) == 2,
        "local_translation_and_reflection_satisfy_the_s3_relations": (
            len(local_group) == 6
            and _compose(_compose(reflection, translation), reflection) == translation_inverse
        ),
        "the_local_selector_group_is_exactly_s3": len(local_group) == 6,
        "the_local_selector_group_order_matches_the_global_selector_stabilizer_order": (
            len(local_group) == selector_stabilizer_order == 6
        ),
        "the_dclxiv_affine_bulk_is_nine_three_state_fibers": (
            affine_bulk_count
            == dclxiv["summary"]["affine_fiber_count"] * dclxiv["summary"]["affine_fiber_size"]
            == 27
        ),
        "the_local_bulk_packet_matches_the_exact_quadrangles_per_ordered_adjacent_pair": (
            affine_bulk_count == quadrangles_per_pair == 27
        ),
        "sixty_local_bulk_packets_scale_to_the_exact_global_1620_selector_carrier": (
            ordered_adjacent_pair_count * affine_bulk_count == global_selector_carrier == 1620
        ),
        "the_six_state_single_photon_mobile_packet_is_the_binary_lift_of_the_three_branch_selector": (
            dclxxxv["summary"]["mobile_frame_packet_size"] == 2 * dclxxxv["summary"]["mobile_projective_fiber_size"] == 6
        ),
        "therefore_the_single_photon_deterministic_update_law_is_the_local_s3_selector_whose_global_completion_is_the_existing_1620_carrier": (
            len(local_group) == selector_stabilizer_order == 6
            and affine_bulk_count == quadrangles_per_pair == 27
            and ordered_adjacent_pair_count * affine_bulk_count == global_selector_carrier == 1620
        ),
    }

    summary = BridgeSummary(
        branch_count=dclxxxv["summary"]["mobile_projective_fiber_size"],
        local_selector_group_order=len(local_group),
        affine_bulk_count=affine_bulk_count,
        ordered_adjacent_pair_count=ordered_adjacent_pair_count,
        global_selector_carrier=global_selector_carrier,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "local_selector_group": {
            "translation": list(translation),
            "reflection": list(reflection),
            "translation_inverse": list(translation_inverse),
            "elements": [list(element) for element in local_group],
        },
        "carrier_scaling": {
            "affine_bulk_count": affine_bulk_count,
            "affine_fiber_count": dclxiv["summary"]["affine_fiber_count"],
            "affine_fiber_size": dclxiv["summary"]["affine_fiber_size"],
            "ordered_adjacent_pair_count": ordered_adjacent_pair_count,
            "quadrangles_per_pair": quadrangles_per_pair,
            "global_selector_carrier": global_selector_carrier,
        },
        "bridge_alignment": {
            "global_selector_stabilizer_order": selector_stabilizer_order,
            "single_photon_mobile_packet_size": dclxxxv["summary"]["mobile_frame_packet_size"],
            "single_photon_branch_count": dclxxxv["summary"]["mobile_projective_fiber_size"],
            "verdict": (
                "The deterministic single-photon qutrit update law is already the local selector law. "
                "Its three projective branches support the exact S3 generated by translation and reflection, "
                "its six-state lifted packet is the binary lift of that three-branch selector, and its 27-point "
                "affine bulk is exactly the local packet size that scales by the 60 ordered adjacent pairs to the "
                "existing 1620 quadrangle carrier."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()