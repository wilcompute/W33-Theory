#!/usr/bin/env python3
"""Part DCCXXXII: closure-clock / codec-flow bridge.

Extends DCCXXXI by coupling the discrete closure clock tau_n to the Pauli/Klitzing
codec ladder from DCCXXIX.

Rule:
- each closure event (e_n = 1) triggers one doubling step,
- non-closure events hold scale fixed.

With base codec scale 12, the flow is
    C_n = 12 * 2^{tau_n}
for tau_n from DCCXXXI.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxix_pauli_klitzing_codec_ladder_bridge import build_bridge as build_dccxxix
from verify_dccxxxi_loop_closure_clock_bridge import build_bridge as build_dccxxxi

OUT_PATH = ROOT / "data" / "dccxxxii_closure_clock_codec_flow_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    base_codec_scale: int
    steps: int
    final_tau: int
    final_scale: int
    reached_96: bool
    reached_192: bool
    all_identities_hold: bool


def codec_flow_from_clock(base: int, tau: list[int]) -> list[int]:
    return [base * (2**t) for t in tau]


def build_bridge() -> dict[str, Any]:
    dccxxix = build_dccxxix()
    dccxxxi = build_dccxxxi()

    base = dccxxix["summary"]["pauli_valency_12"]
    b_ladder = dccxxix["ladders"]["mod_b_direct"]  # [12,24,48,96]
    a_ladder = dccxxix["ladders"]["mod_a_sheet_lift"]  # [24,48,96,192]

    events = dccxxxi["clock_model"]["events"]
    tau = dccxxxi["clock_model"]["tau"]
    flow = codec_flow_from_clock(base, tau)
    flow_with_base = [base] + flow

    unique_flow = sorted(set(flow_with_base))

    identities = {
        "base_scale_matches_pauli_valency_and_codec": (
            base == 12 and dccxxix["summary"]["klitzing_rectified_12"] == 12
        ),
        "clock_events_are_binary": all(e in (0, 1) for e in events),
        "tau_is_monotone": all(tau[i] <= tau[i + 1] for i in range(len(tau) - 1)),
        "scale_definition_is_12_times_two_to_tau": all(
            flow[i] == base * (2 ** tau[i]) for i in range(len(tau))
        ),
        "event_zero_holds_scale_event_one_doubles": all(
            (
                (events[i] == 0 and flow[i] == (flow[i - 1] if i else flow[i]))
                or (events[i] == 1 and flow[i] == (2 * flow[i - 1] if i else flow[i]))
            )
            for i in range(len(events))
        ),
        "flow_unique_levels_embed_b_ladder": all(x in unique_flow for x in b_ladder),
        "flow_reaches_a_omnitruncated_192": (a_ladder[-1] in flow),
        "final_scale_matches_final_tau": flow[-1] == base * (2 ** tau[-1]),
    }

    summary = BridgeSummary(
        base_codec_scale=base,
        steps=len(events),
        final_tau=tau[-1],
        final_scale=flow[-1],
        reached_96=(96 in flow),
        reached_192=(192 in flow),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "clock": {
            "events": events,
            "tau": tau,
            "tau0": 0,
        },
        "codec_flow": {
            "definition": "C_n = 12 * 2^{tau_n}",
            "values": flow,
            "values_with_base": flow_with_base,
            "unique_levels": unique_flow,
        },
        "reference_ladders": {
            "mod_b_direct": b_ladder,
            "mod_a_sheet_lift": a_ladder,
        },
        "bridge_claim": {
            "exact_layer": (
                "Closure-clock increments generate a deterministic doubling flow that embeds the Klitzing codec ladder levels."
            ),
            "conditional_layer": (
                "Interpreting the flow index as physical RG time requires additional dynamical assumptions beyond the discrete closure theorem."
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
