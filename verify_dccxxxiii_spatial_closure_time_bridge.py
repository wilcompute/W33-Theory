#!/usr/bin/env python3
"""Part DCCXXXIII: spatial-closure / time bridge.

This part makes the 3+1 reading executable:
- the three Clifford bivectors {B23, B31, B12} provide the spatial triad,
- the closure clock from DCCXXXI provides the fourth, scalar update channel,
- the codec-flow law from DCCXXXII shows that this fourth channel is exactly
  the logarithm base 2 of scale relative to the base codec 12.

So the emergent 3+1 split is not "four spatial axes"; it is
    3 spatial bivector channels + 1 closure-generated clock channel.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxx_clifford_even_quaternion_pauli_bridge import build_bridge as build_dccxxx
from verify_dccxxxi_loop_closure_clock_bridge import build_bridge as build_dccxxxi
from verify_dccxxxii_closure_clock_codec_flow_bridge import build_bridge as build_dccxxxii

OUT_PATH = ROOT / "data" / "dccxxxiii_spatial_closure_time_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    spatial_dimension: int
    time_dimension: int
    total_state_dimension: int
    base_codec_scale: int
    final_clock_value: int
    final_scale: int
    all_identities_hold: bool


def _log2_ratio(scale: int, base: int) -> int:
    ratio = scale // base
    if base <= 0 or scale <= 0 or scale % base != 0:
        raise ValueError("Scale must be a positive integer multiple of base")
    if ratio & (ratio - 1) != 0:
        raise ValueError("Scale/base must be a power of two")
    return int(math.log2(ratio))


def build_bridge() -> dict[str, Any]:
    dccxxx = build_dccxxx()
    dccxxxi = build_dccxxxi()
    dccxxxii = build_dccxxxii()

    basis = dccxxx["clifford_even_subalgebra"]["basis"]
    spatial_basis = [b for b in basis if b != "1"]
    events = dccxxxi["clock_model"]["events"]
    tau = dccxxxi["clock_model"]["tau"]
    base = dccxxxii["summary"]["base_codec_scale"]
    scales = dccxxxii["codec_flow"]["values"]

    logarithmic_time = [_log2_ratio(scale, base) for scale in scales]
    state_history = [
        {
            "step": idx + 1,
            "spatial_basis": spatial_basis,
            "closure_event": events[idx],
            "tau": tau[idx],
            "scale": scales[idx],
            "log2_scale_over_12": logarithmic_time[idx],
        }
        for idx in range(len(events))
    ]

    identities = {
        "three_spatial_bivectors_exist": spatial_basis == ["B23", "B31", "B12"],
        "identity_completes_fourth_clifford_even_basis_slot": basis == ["1", "B23", "B31", "B12"],
        "closure_clock_is_single_scalar_channel": all(isinstance(t, int) for t in tau),
        "three_plus_one_gives_four_total_channels": len(spatial_basis) + 1 == len(basis) == 4,
        "time_is_exact_logarithm_of_codec_scale": logarithmic_time == tau,
        "closure_event_zero_holds_time_event_one_advances_time": all(
            tau[i] - (tau[i - 1] if i else 0) == events[i] for i in range(len(events))
        ),
        "time_channel_is_not_an_extra_spatial_bivector": "1" not in spatial_basis and len(set(spatial_basis)) == 3,
        "final_scale_is_12_times_two_to_time": scales[-1] == base * (2 ** tau[-1]),
    }

    summary = BridgeSummary(
        spatial_dimension=len(spatial_basis),
        time_dimension=1,
        total_state_dimension=len(spatial_basis) + 1,
        base_codec_scale=base,
        final_clock_value=tau[-1],
        final_scale=scales[-1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "spatial_time_split": {
            "spatial_basis": spatial_basis,
            "time_channel": "tau = log2(C/12)",
            "state_dimension": [len(spatial_basis), 1],
            "interpretation": "3 Clifford bivector channels plus 1 closure-generated scalar clock channel.",
        },
        "state_history": state_history,
        "bridge_claim": {
            "exact_layer": (
                "The three bivectors B23, B31, B12 form the spatial triad, while the closure clock is exactly the base-2 logarithm of codec scale relative to 12."
            ),
            "conditional_layer": (
                "Reading this discrete scalar clock as macroscopic physical time still requires additional dynamical and continuum hypotheses."
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
