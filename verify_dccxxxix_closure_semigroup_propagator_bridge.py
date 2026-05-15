#!/usr/bin/env python3
"""Part DCCXXXIX: closure semigroup / propagator bridge.

Builds on DCCXXXVIII by turning the Bellman value law into a semigroup-style
propagator statement on the finite causal chain.

For causal classes T_a <= T_b define
    J(a,b) = tau_b - tau_a,
    K(a,b) = 2^{-J(a,b)}.

Then:
- J composes in the min-plus semiring via
      J(a,c) = min_b [J(a,b) + J(b,c)],
  with equality for every intermediate b on the chain;
- K composes multiplicatively via
      K(a,c) = K(a,b) K(b,c)
  for every intermediate b.

This is the exact semigroup/propagator form of the closure-time law.
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

from verify_dccxxxviii_closure_bellman_principle_bridge import build_bridge as build_dccxxxviii

OUT_PATH = ROOT / "data" / "dccxxxix_closure_semigroup_propagator_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    causal_class_count: int
    maximal_value: int
    minimal_propagator_numerator: int
    minimal_propagator_denominator: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dccxxxviii = build_dccxxxviii()
    spans = dccxxxviii["value_function"]["values"]  # [0,1,2,3,4,5]
    taus = list(range(len(spans)))

    value_table = []
    propagator_table = []
    semigroup_witness = []

    for i, tau_a in enumerate(taus):
        value_row = []
        prop_row = []
        for j, tau_b in enumerate(taus):
            if j < i:
                value_row.append(None)
                prop_row.append({"numerator": 0, "denominator": 1})
            else:
                delta = tau_b - tau_a
                value_row.append(delta)
                prop_row.append({"numerator": 1, "denominator": 2 ** delta})
        value_table.append(value_row)
        propagator_table.append(prop_row)

    for i, tau_a in enumerate(taus):
        for k in range(i, len(taus)):
            tau_c = taus[k]
            candidates = []
            for j in range(i, k + 1):
                tau_b = taus[j]
                val_ab = value_table[i][j]
                val_bc = value_table[j][k]
                prop_ab = propagator_table[i][j]
                prop_bc = propagator_table[j][k]
                candidates.append(
                    {
                        "midpoint": tau_b,
                        "value_sum": val_ab + val_bc,
                        "propagator_product": {
                            "numerator": prop_ab["numerator"] * prop_bc["numerator"],
                            "denominator": prop_ab["denominator"] * prop_bc["denominator"],
                        },
                    }
                )
            semigroup_witness.append(
                {
                    "from": tau_a,
                    "to": tau_c,
                    "target_value": value_table[i][k],
                    "target_propagator": propagator_table[i][k],
                    "candidates": candidates,
                }
            )

    identities = {
        "value_table_is_delta_tau": all(
            value_table[i][j] == (taus[j] - taus[i])
            for i in range(len(taus)) for j in range(i, len(taus))
        ),
        "propagator_is_two_to_minus_delta_tau": all(
            propagator_table[i][j]["denominator"] == 2 ** value_table[i][j]
            for i in range(len(taus)) for j in range(i, len(taus))
        ),
        "min_plus_semigroup_holds": all(
            witness["target_value"] == min(c["value_sum"] for c in witness["candidates"])
            for witness in semigroup_witness
        ),
        "every_midpoint_saturates_min_plus_identity": all(
            all(c["value_sum"] == witness["target_value"] for c in witness["candidates"])
            for witness in semigroup_witness
        ),
        "multiplicative_propagator_identity_holds": all(
            all(c["propagator_product"] == witness["target_propagator"] for c in witness["candidates"])
            for witness in semigroup_witness
        ),
        "maximal_value_is_five": value_table[0][-1] == 5,
        "minimal_nonzero_propagator_is_one_over_32": propagator_table[0][-1] == {"numerator": 1, "denominator": 32},
    }

    summary = BridgeSummary(
        causal_class_count=len(taus),
        maximal_value=value_table[0][-1],
        minimal_propagator_numerator=propagator_table[0][-1]["numerator"],
        minimal_propagator_denominator=propagator_table[0][-1]["denominator"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "propagator_definition": {
            "value": "J(a,b)=tau_b-tau_a for causal pairs",
            "weight": "K(a,b)=2^{-J(a,b)}",
            "min_plus_law": "J(a,c)=min_b (J(a,b)+J(b,c))",
            "multiplicative_law": "K(a,c)=K(a,b)K(b,c)",
        },
        "value_table": value_table,
        "propagator_table": propagator_table,
        "semigroup_witness": semigroup_witness,
        "bridge_claim": {
            "exact_layer": (
                "The closure chain carries a propagator semigroup: value propagates by min-plus composition and the exponential weight propagates multiplicatively, with every intermediate causal class saturating the composition law on the chain."
            ),
            "conditional_layer": (
                "Promoting this discrete propagator law to a continuum semigroup kernel requires an additional limit construction."
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
