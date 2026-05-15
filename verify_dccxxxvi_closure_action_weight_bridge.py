#!/usr/bin/env python3
"""Part DCCXXXVI: closure-action / weight bridge.

Builds on DCCXXXV by turning the discrete proper-time interval into a path action.

For a monotone causal path
    T_a -> T_{a+1} -> ... -> T_b
with unit line elements ds = Delta_tau = 1 on each elementary step, define

    S(a,b) = sum_path ds = Delta_tau(a,b),
    W(a,b) = 2^{-S(a,b)} = C_a / C_b.

So the closure path action is exactly the logarithm-base-2 of the codec scale ratio,
and the corresponding path weight is exactly the inverse scale ratio.
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

from verify_dccxxxv_closure_interval_invariant_bridge import build_bridge as build_dccxxxv

OUT_PATH = ROOT / "data" / "dccxxxvi_closure_action_weight_bridge.json"
BASE_SCALE = 12


@dataclass(frozen=True)
class BridgeSummary:
    causal_class_count: int
    elementary_action: int
    maximal_action: int
    maximal_weight_numerator: int
    maximal_weight_denominator: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dccxxxv = build_dccxxxv()
    classes = dccxxxv["causal_classes"]
    taus = [c["proper_time"] for c in classes]
    scales = [c["representative_scale"] for c in classes]

    elementary_edges = [
        {
            "from": taus[i],
            "to": taus[i + 1],
            "ds": 1,
            "delta_tau": 1,
            "action": 1,
            "weight": {"numerator": 1, "denominator": 2},
        }
        for i in range(len(taus) - 1)
    ]

    path_table = []
    for i, tau_a in enumerate(taus):
        row = []
        for j, tau_b in enumerate(taus):
            if j < i:
                row.append({
                    "from": tau_a,
                    "to": tau_b,
                    "causal": False,
                    "action": None,
                    "weight": None,
                    "scale_ratio": None,
                })
            else:
                action = tau_b - tau_a
                ratio = scales[j] // scales[i]
                row.append({
                    "from": tau_a,
                    "to": tau_b,
                    "causal": True,
                    "action": action,
                    "weight": {"numerator": 1, "denominator": ratio},
                    "scale_ratio": ratio,
                })
        path_table.append(row)

    composition_witness = []
    for i in range(len(taus)):
        for j in range(i, len(taus)):
            for k in range(j, len(taus)):
                ratio_ij = scales[j] // scales[i]
                ratio_jk = scales[k] // scales[j]
                ratio_ik = scales[k] // scales[i]
                composition_witness.append({
                    "i": taus[i],
                    "j": taus[j],
                    "k": taus[k],
                    "action_ik": taus[k] - taus[i],
                    "action_ij_plus_jk": (taus[j] - taus[i]) + (taus[k] - taus[j]),
                    "ratio_ik": ratio_ik,
                    "ratio_ij_times_jk": ratio_ij * ratio_jk,
                })

    identities = {
        "elementary_steps_have_unit_action": all(edge["action"] == 1 and edge["ds"] == 1 for edge in elementary_edges),
        "path_action_equals_delta_tau": all(
            path_table[i][j]["action"] == (taus[j] - taus[i])
            for i in range(len(taus)) for j in range(i, len(taus))
        ),
        "path_action_equals_log2_scale_ratio": all(
            path_table[i][j]["scale_ratio"] == 2 ** path_table[i][j]["action"]
            for i in range(len(taus)) for j in range(i, len(taus))
        ),
        "path_weight_is_inverse_scale_ratio": all(
            path_table[i][j]["weight"]["denominator"] == path_table[i][j]["scale_ratio"]
            for i in range(len(taus)) for j in range(i, len(taus))
        ),
        "action_is_additive_under_composition": all(
            item["action_ik"] == item["action_ij_plus_jk"] for item in composition_witness
        ),
        "weight_is_multiplicative_under_composition": all(
            item["ratio_ik"] == item["ratio_ij_times_jk"] for item in composition_witness
        ),
        "maximal_path_has_action_five_and_weight_one_over_32": (
            path_table[0][-1]["action"] == 5 and path_table[0][-1]["weight"] == {"numerator": 1, "denominator": 32}
        ),
    }

    summary = BridgeSummary(
        causal_class_count=len(classes),
        elementary_action=1,
        maximal_action=path_table[0][-1]["action"],
        maximal_weight_numerator=path_table[0][-1]["weight"]["numerator"],
        maximal_weight_denominator=path_table[0][-1]["weight"]["denominator"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "action_definition": {
            "line_element": "ds = Delta_tau on elementary causal edges",
            "path_action": "S(a,b) = sum_path ds = Delta_tau(a,b)",
            "path_weight": "W(a,b) = 2^{-S(a,b)} = C_a / C_b",
            "base_scale": BASE_SCALE,
        },
        "elementary_edges": elementary_edges,
        "path_table": path_table,
        "composition_witness": composition_witness,
        "bridge_claim": {
            "exact_layer": (
                "The closure chain carries an exact discrete action S=Delta_tau whose path weight is the inverse codec scale ratio W=2^{-S}."
            ),
            "conditional_layer": (
                "Interpreting this weight as a full continuum path-integral amplitude requires an additional continuum measure and dynamical prescription."
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
