#!/usr/bin/env python3
"""Part DCIX: directional split bridge for oriented toroidal transport.

On the 7-mode cycle, oriented transports split canonically into:

  - forward steps d in {1,2,3}
  - backward steps d in {4,5,6}

Each step class has 7 transports, so:

  forward = 3*7 = 21,
  backward = 3*7 = 21,
  total oriented = 42.

This part certifies that directional split (21+21) is numerically aligned with
the dual-family edge split (Csaszar 21 + Szilassi 21), and closes via stabilizer:

  42 * 4 = 168.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STEP_PATH = ROOT / "data" / "tomotope_toroidal_step_transport_bridge.json"
EDGE_PAIR_PATH = ROOT / "data" / "tomotope_toroidal_edge_pair_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_directional_split_bridge.json"


@dataclass(frozen=True)
class DirectionalSummary:
    forward_oriented_count: int
    backward_oriented_count: int
    total_oriented_count: int
    csaszar_edges: int
    szilassi_edges: int
    slot_stabilizer_size: int
    weighted_directional_total: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    step = json.loads(STEP_PATH.read_text(encoding="utf-8"))
    edge_pair = json.loads(EDGE_PAIR_PATH.read_text(encoding="utf-8"))

    step_to_slot = step["step_to_slot"]
    slot_transport_counts = step["slot_transport_counts"]

    # step_to_slot keys are expected to be 1..6 (ints serialized as JSON object keys -> strings).
    def count_for_steps(step_labels: list[int]) -> int:
        total = 0
        for d in step_labels:
            slot = step_to_slot[str(d)] if str(d) in step_to_slot else step_to_slot[d]
            total += int(slot_transport_counts[slot])
        return total

    forward = count_for_steps([1, 2, 3])
    backward = count_for_steps([4, 5, 6])
    total_oriented = int(step["summary"]["oriented_transport_count"])

    cs_edges = int(edge_pair["summary"]["csaszar_edges"])
    sz_edges = int(edge_pair["summary"]["szilassi_edges"])
    stabilizer = int(edge_pair["summary"]["slot_stabilizer_size"])

    weighted = (forward + backward) * stabilizer

    identities = {
        "upstream_step_identities_hold": bool(step["summary"]["all_identities_hold"]),
        "upstream_edge_pair_identities_hold": bool(edge_pair["summary"]["all_identities_hold"]),
        "forward_count_is_21": forward == 21,
        "backward_count_is_21": backward == 21,
        "directional_counts_equal": forward == backward,
        "directional_sum_is_42": forward + backward == 42,
        "directional_sum_matches_oriented_total": forward + backward == total_oriented,
        "directional_split_matches_dual_family_split": (forward, backward) == (cs_edges, sz_edges),
        "weighted_total_is_168": weighted == 168,
        "weighted_total_matches_active_packet": (
            weighted == int(edge_pair["summary"]["active_packet_weight"])
        ),
    }

    summary = DirectionalSummary(
        forward_oriented_count=forward,
        backward_oriented_count=backward,
        total_oriented_count=total_oriented,
        csaszar_edges=cs_edges,
        szilassi_edges=sz_edges,
        slot_stabilizer_size=stabilizer,
        weighted_directional_total=weighted,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCIX directional certificate: oriented transports split as 21 forward + "
            "21 backward, mirroring the dual-family 21+21 shell and closing to 168 "
            "under stabilizer weight 4."
        ),
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
