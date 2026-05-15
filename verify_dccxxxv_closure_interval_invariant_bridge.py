#!/usr/bin/env python3
"""Part DCCXXXV: closure-interval invariant bridge.

Builds on DCCXXXIV by defining an exact interval invariant on the discrete proper-time
levels of the closure process.

For causal classes T_a <= T_b with proper times tau_a <= tau_b, define

    Delta_tau(a,b) = tau_b - tau_a,
    sigma(a,b) = Delta_tau(a,b)^2.

This is the discrete analogue of a proper-time interval on the closure chain:
- it vanishes on the diagonal,
- it is additive at the Delta_tau level along composable chains,
- it is read directly from codec-scale ratios via
      Delta_tau = log2(C_b / C_a),
      sigma = (log2(C_b / C_a))^2.
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

from verify_dccxxxiv_proper_time_causal_order_bridge import build_bridge as build_dccxxxiv

OUT_PATH = ROOT / "data" / "dccxxxv_closure_interval_invariant_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    causal_class_count: int
    maximal_interval: int
    maximal_interval_squared: int
    final_scale_ratio: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dccxxxiv = build_dccxxxiv()

    classes = dccxxxiv["causal_order"]["classes"]
    taus = [c["proper_time"] for c in classes]
    scales = [c["representative_scale"] for c in classes]

    interval_table = []
    for i, tau_a in enumerate(taus):
        row = []
        for j, tau_b in enumerate(taus):
            if j < i:
                row.append({
                    "from": taus[i],
                    "to": taus[j],
                    "causal": False,
                    "delta_tau": None,
                    "sigma": None,
                    "scale_ratio": None,
                })
            else:
                delta = tau_b - tau_a
                ratio = scales[j] // scales[i]
                row.append({
                    "from": tau_a,
                    "to": tau_b,
                    "causal": True,
                    "delta_tau": delta,
                    "sigma": delta * delta,
                    "scale_ratio": ratio,
                })
        interval_table.append(row)

    additive_witness = []
    for i in range(len(taus)):
        for j in range(i, len(taus)):
            for k in range(j, len(taus)):
                additive_witness.append({
                    "i": taus[i],
                    "j": taus[j],
                    "k": taus[k],
                    "delta_ik": taus[k] - taus[i],
                    "delta_ij_plus_jk": (taus[j] - taus[i]) + (taus[k] - taus[j]),
                })

    logarithmic_ratio_witness = [
        {
            "from": taus[i],
            "to": taus[j],
            "delta_tau": taus[j] - taus[i],
            "scale_ratio": scales[j] // scales[i],
        }
        for i in range(len(taus))
        for j in range(i, len(taus))
    ]

    identities = {
        "there_are_six_causal_classes": len(classes) == 6,
        "interval_vanishes_on_diagonal": all(interval_table[i][i]["sigma"] == 0 for i in range(len(taus))),
        "delta_tau_is_additive_along_causal_chains": all(
            item["delta_ik"] == item["delta_ij_plus_jk"] for item in additive_witness
        ),
        "scale_ratio_is_two_to_delta_tau": all(
            witness["scale_ratio"] == 2 ** witness["delta_tau"] for witness in logarithmic_ratio_witness
        ),
        "sigma_is_square_of_log_scale_ratio": all(
            interval_table[i][j]["sigma"] == (interval_table[i][j]["delta_tau"] ** 2)
            for i in range(len(taus))
            for j in range(i, len(taus))
        ),
        "causal_orientation_matches_tau_order": all(
            interval_table[i][j]["causal"] is True for i in range(len(taus)) for j in range(i, len(taus))
        ) and all(
            interval_table[i][j]["causal"] is False for i in range(len(taus)) for j in range(i)
        ),
        "maximal_interval_matches_0_to_5": interval_table[0][-1]["delta_tau"] == 5 and interval_table[0][-1]["sigma"] == 25,
    }

    summary = BridgeSummary(
        causal_class_count=len(classes),
        maximal_interval=interval_table[0][-1]["delta_tau"],
        maximal_interval_squared=interval_table[0][-1]["sigma"],
        final_scale_ratio=interval_table[0][-1]["scale_ratio"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "interval_definition": {
            "delta_tau": "tau_b - tau_a for T_a <= T_b",
            "sigma": "(tau_b - tau_a)^2",
            "scale_law": "delta_tau = log2(C_b / C_a)",
        },
        "causal_classes": classes,
        "interval_table": interval_table,
        "additivity_witness": additive_witness,
        "logarithmic_ratio_witness": logarithmic_ratio_witness,
        "bridge_claim": {
            "exact_layer": (
                "The closure process carries an exact discrete proper-time interval invariant sigma=(Delta_tau)^2, with Delta_tau read directly from codec-scale ratios."
            ),
            "conditional_layer": (
                "Promoting this discrete interval to a continuum Lorentzian interval requires a separate limiting or dynamical argument."
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
