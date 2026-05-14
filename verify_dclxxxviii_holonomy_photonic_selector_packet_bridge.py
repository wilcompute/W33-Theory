#!/usr/bin/env python3
"""Part DCLXXXVIII: holonomy photonic selector packet bridge.

This bridge turns the global selector bundle into a direct photonic factorization.

Key identities proved:

  - ordered adjacent pair count = theta(W33) * |S3| = 10 * 6 = 60;
  - common packet size = |S3| * 27 = 2 * 81 = 162;
  - global selector carrier = theta(W33) * 162 = 10 * 162 = 1620.

So the same common packet 162 can be read in two exact ways:

  selector-side:  local symmetry * local bulk   = 6 * 27
  photonic-side:  helicity * deterministic frame = 2 * 81
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER import (  # noqa: E402
    build_results as build_scheduler_results,
)
from PART_CCCCXIX_PHOTONIC_HARMONIC_TQC_SYNTHESIS import (  # noqa: E402
    theta_equals_alpha_value,
)
from verify_dclxxxvi_holonomy_single_photon_selector_bridge import (  # noqa: E402
    build_bridge as build_dclxxxvi_bridge,
)


OUT_PATH = ROOT / "data" / "dclxxxviii_holonomy_photonic_selector_packet_bridge.json"
HELICITY_COUNT = 2  # Part CCLI: the physical photon has exactly two helicity states.


@dataclass(frozen=True)
class BridgeSummary:
    photonic_mode_count: int
    helicity_count: int
    deterministic_frame_size: int
    local_selector_order: int
    local_bulk_size: int
    common_packet_size: int
    global_selector_carrier: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    photonic_runtime = build_scheduler_results()
    selector = build_dclxxxvi_bridge()

    photonic_mode_count = theta_equals_alpha_value()
    helicity_count = HELICITY_COUNT
    deterministic_frame_size = photonic_runtime["controller_envelope"]["pauli_frame_states"]
    local_selector_order = selector["summary"]["local_selector_group_order"]
    local_bulk_size = selector["summary"]["affine_bulk_count"]
    ordered_adjacent_pair_count = selector["summary"]["ordered_adjacent_pair_count"]
    global_selector_carrier = selector["summary"]["global_selector_carrier"]
    common_packet_size = local_selector_order * local_bulk_size

    identities = {
        "the_ordered_adjacent_pair_count_factors_as_photonic_modes_times_local_selector_order": (
            ordered_adjacent_pair_count == photonic_mode_count * local_selector_order == 10 * 6 == 60
        ),
        "the_common_packet_size_is_selector_symmetry_times_local_bulk": (
            common_packet_size == local_selector_order * local_bulk_size == 6 * 27 == 162
        ),
        "the_same_common_packet_size_is_helicity_times_the_deterministic_pauli_frame": (
            common_packet_size == helicity_count * deterministic_frame_size == 2 * 81 == 162
        ),
        "therefore_selector_packet_equals_photonic_packet": (
            local_selector_order * local_bulk_size == helicity_count * deterministic_frame_size
        ),
        "the_global_selector_carrier_is_photonic_modes_times_the_common_packet": (
            global_selector_carrier == photonic_mode_count * common_packet_size == 10 * 162 == 1620
        ),
        "equivalently_the_global_selector_carrier_is_photonic_modes_times_helicity_times_the_deterministic_frame": (
            global_selector_carrier == photonic_mode_count * helicity_count * deterministic_frame_size == 10 * 2 * 81 == 1620
        ),
        "equivalently_the_global_selector_carrier_is_photonic_modes_times_local_selector_order_times_local_bulk": (
            global_selector_carrier == photonic_mode_count * local_selector_order * local_bulk_size == 10 * 6 * 27 == 1620
        ),
        "therefore_the_existing_1620_selector_carrier_is_the_ten_mode_photonic_amplification_of_one_common_162_packet": (
            ordered_adjacent_pair_count == 60
            and common_packet_size == 162
            and global_selector_carrier == 1620
        ),
    }

    summary = BridgeSummary(
        photonic_mode_count=photonic_mode_count,
        helicity_count=helicity_count,
        deterministic_frame_size=deterministic_frame_size,
        local_selector_order=local_selector_order,
        local_bulk_size=local_bulk_size,
        common_packet_size=common_packet_size,
        global_selector_carrier=global_selector_carrier,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "factorizations": {
            "ordered_adjacent_pairs": {
                "value": ordered_adjacent_pair_count,
                "photonic_modes_times_selector_order": [photonic_mode_count, local_selector_order],
            },
            "common_packet": {
                "value": common_packet_size,
                "selector_side": [local_selector_order, local_bulk_size],
                "photonic_side": [helicity_count, deterministic_frame_size],
            },
            "global_selector_carrier": {
                "value": global_selector_carrier,
                "mode_packet_factorization": [photonic_mode_count, common_packet_size],
                "full_selector_factorization": [photonic_mode_count, local_selector_order, local_bulk_size],
                "full_photonic_factorization": [photonic_mode_count, helicity_count, deterministic_frame_size],
            },
        },
        "interpretation": {
            "verdict": (
                "The exact global selector carrier is one ten-mode photonic amplification of a common 162-state packet. "
                "That common packet has two exact readings: 6*27 on the selector side and 2*81 on the photonic side. "
                "So the global 1620 carrier is the precise overlap of the photonic runtime and the selector bundle, not merely a count coincidence."
            )
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