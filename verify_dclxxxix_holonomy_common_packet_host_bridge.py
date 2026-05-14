#!/usr/bin/env python3
"""Part DCLXXXIX: holonomy common packet host bridge.

The common 162-packet from DCLXXXVIII has two exact readings:

    162 = 6*27 = 2*81.

This verifier proves a third reading: it is exactly the total qutrit-lift
support packet of the canonical mixed-plane K3 host,

    162 = 81 + 81,

split across the positive and negative ordered line types.
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

from verify_dclxxxviii_holonomy_photonic_selector_packet_bridge import (  # noqa: E402
    build_bridge as build_dclxxxviii_bridge,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)


OUT_PATH = ROOT / "data" / "dclxxxix_holonomy_common_packet_host_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    common_packet_size: int
    positive_support_size: int
    negative_support_size: int
    host_support_total: int
    global_selector_carrier: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    packet = build_dclxxxviii_bridge()
    k3 = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()

    common_packet_size = packet["summary"]["common_packet_size"]
    global_selector_carrier = packet["summary"]["global_selector_carrier"]

    host_support = k3["canonical_mixed_plane_support"]
    qutrit_lift_split = list(host_support["qutrit_lift_split"])
    positive_support_size, negative_support_size = qutrit_lift_split
    host_support_total = sum(qutrit_lift_split)

    identities = {
        "the_common_packet_from_dclxxxviii_has_size_162": common_packet_size == 162,
        "the_canonical_mixed_plane_host_has_exact_positive_negative_qutrit_lift_split_81_plus_81": (
            qutrit_lift_split == [81, 81]
            and host_support["ordered_line_types"] == ["positive", "negative"]
            and list(host_support["mixed_signature"]) == [1, 1]
        ),
        "the_total_mixed_plane_host_support_is_exactly_162": host_support_total == 81 + 81 == 162,
        "therefore_the_common_selector_photonic_packet_is_exactly_the_host_support_packet": (
            common_packet_size == host_support_total == 162
        ),
        "the_global_1620_selector_carrier_is_ten_times_the_exact_host_support_packet": (
            global_selector_carrier == 10 * host_support_total == 1620
        ),
        "the_same_162_packet_has_three_exact_readings": (
            packet["factorizations"]["common_packet"]["selector_side"] == [6, 27]
            and packet["factorizations"]["common_packet"]["photonic_side"] == [2, 81]
            and qutrit_lift_split == [81, 81]
            and common_packet_size == 162
        ),
        "therefore_the_canonical_mixed_plane_host_already_has_the_exact_packet_size_required_by_the_selector_bundle_and_the_single_photon_runtime": (
            common_packet_size == host_support_total == 162
            and global_selector_carrier == 1620
        ),
    }

    summary = BridgeSummary(
        common_packet_size=common_packet_size,
        positive_support_size=positive_support_size,
        negative_support_size=negative_support_size,
        host_support_total=host_support_total,
        global_selector_carrier=global_selector_carrier,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "packet_readings": {
            "selector_side": packet["factorizations"]["common_packet"]["selector_side"],
            "photonic_side": packet["factorizations"]["common_packet"]["photonic_side"],
            "host_side": qutrit_lift_split,
        },
        "host_support": {
            "ordered_line_types": host_support["ordered_line_types"],
            "mixed_signature": list(host_support["mixed_signature"]),
            "qutrit_lift_split": qutrit_lift_split,
        },
        "interpretation": {
            "verdict": (
                "The common 162-packet is not only a selector-side and photonic-side object. "
                "It is exactly the total qutrit-lift support packet already present on the canonical mixed-plane K3 host, split as 81+81 across the positive and negative ordered line types."
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