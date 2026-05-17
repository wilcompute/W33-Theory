#!/usr/bin/env python3
"""Part DCCLXXV: photonic retry / closure-kernel bridge.

DCCXV made p_fusion=1/2 a native heralded QEC return ledger. DCCLXXIV made
G=(1/2)S the closure-clock transfer kernel. This bridge identifies the shared
finite retry law:

    d consecutive heralded returns carry weight 2^{-d},
    d = 0..5 on the six-level closure clock.

The result is scheduler-level arithmetic only. It is not a detector-loss
threshold or optical hardware proof.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxv_photonic_fusion_syndrome_qec_bridge import (  # noqa: E402
    build_bridge as build_fusion,
)
from verify_dcclxxiv_closure_transfer_resolvent_equivalence_bridge import (  # noqa: E402
    build_bridge as build_closure_kernel,
)


OUT_PATH = ROOT / "data" / "dcclxxv_photonic_retry_closure_kernel_bridge.json"

Q = 3
V = (Q**4 - 1) // (Q - 1)


@dataclass(frozen=True)
class BridgeSummary:
    closure_depth_count: int
    fusion_denominator: int
    accepted_slots: int
    return_slots: int
    directed_attempt_slots: int
    klm_primitive_slots: int
    maximal_retry_denominator: int
    all_identities_hold: bool


def _frac(cell: dict[str, int]) -> Fraction:
    return Fraction(cell["numerator"], cell["denominator"])


def build_bridge() -> dict[str, Any]:
    fusion = build_fusion()
    closure = build_closure_kernel()

    closure_depths = int(closure["summary"]["causal_class_count"])
    generator_weight = Fraction(
        closure["summary"]["generator_weight_num"],
        closure["summary"]["generator_weight_den"],
    )

    local = fusion["local_to_global"]
    qec = fusion["qec_absorption"]

    retry_rows = []
    entry_rows = {
        (row["from"], row["to"]): row
        for row in closure["entry_rows"]
    }
    for miss_count in range(closure_depths):
        row = entry_rows[(0, miss_count)]
        transfer_weight = _frac(row["power_entry"])
        retry_rows.append(
            {
                "heralded_return_count": miss_count,
                "transfer_weight": {
                    "numerator": transfer_weight.numerator,
                    "denominator": transfer_weight.denominator,
                },
                "retry_read": f"2^-{miss_count}",
            }
        )

    directed_attempts = int(fusion["summary"]["fusion_attempts"])
    klm_primitives = int(fusion["summary"]["klm_primitives"])

    identities = {
        "fusion_summary_holds": bool(fusion["summary"]["all_identities_hold"]),
        "closure_kernel_summary_holds": bool(closure["summary"]["all_identities_hold"]),
        "fusion_denominator_matches_transfer_weight": generator_weight == Fraction(1, 2),
        "closure_depth_count_matches_success_slots": (
            closure_depths == int(local["local_signed_clifford_slots"])
        ),
        "closure_depth_count_matches_return_slots": (
            closure_depths == int(local["local_a2_weyl_return_slots"])
        ),
        "local_attempt_alphabet_is_two_closure_depths": (
            int(fusion["summary"]["local_attempt_alphabet"]) == 2 * closure_depths
        ),
        "accepted_and_return_rows_are_equal_depth_lifts": (
            int(fusion["summary"]["accepted_bond_slots"])
            == int(fusion["summary"]["heralded_syndrome_slots"])
            == V * closure_depths
        ),
        "directed_attempt_slots_are_vertex_lift_of_retry_alphabet": (
            directed_attempts == V * 2 * closure_depths == 480
        ),
        "klm_primitives_are_binary_rail_lift": klm_primitives == 2 * directed_attempts == 960,
        "retry_weights_are_transfer_powers": all(
            Fraction(row["transfer_weight"]["numerator"], row["transfer_weight"]["denominator"])
            == Fraction(1, 2**row["heralded_return_count"])
            for row in retry_rows
        ),
        "maximal_retry_tail_is_one_over_32": (
            retry_rows[-1]["transfer_weight"] == {"numerator": 1, "denominator": 32}
        ),
        "qec_absorption_preserves_h1": (
            int(qec["vertex_check_rank"])
            + int(qec["triangle_check_rank"])
            + int(qec["logical_h1"])
            == int(qec["edge_qubit_carrier"])
            == int(fusion["summary"]["accepted_bond_slots"])
        ),
    }

    summary = BridgeSummary(
        closure_depth_count=closure_depths,
        fusion_denominator=generator_weight.denominator,
        accepted_slots=int(fusion["summary"]["accepted_bond_slots"]),
        return_slots=int(fusion["summary"]["heralded_syndrome_slots"]),
        directed_attempt_slots=directed_attempts,
        klm_primitive_slots=klm_primitives,
        maximal_retry_denominator=retry_rows[-1]["transfer_weight"]["denominator"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "retry_kernel": {
            "law": "d heralded returns carry transfer weight 2^{-d}",
            "depth_rows": retry_rows,
            "finite_horizon": "d=0..5; the sixth transfer power vanishes by nilpotence",
        },
        "photonic_ledger": {
            "accepted_slots": fusion["summary"]["accepted_bond_slots"],
            "return_slots": fusion["summary"]["heralded_syndrome_slots"],
            "directed_attempt_slots": directed_attempts,
            "klm_primitive_slots": klm_primitives,
            "qec_identity": qec["css_identity"],
        },
        "identities": identities,
        "theorem": (
            "Photonic Retry Closure-Kernel Theorem. The p_fusion=1/2 heralded "
            "return ledger of DCCXV and the G=(1/2)S closure transfer kernel of "
            "DCCLXXIV carry the same finite retry law: d consecutive return "
            "updates have weight 2^{-d} for d=0..5. Across 40 vertices the "
            "six accepted depths plus six return depths give 480 directed "
            "attempt slots, and the KLM rail doubles this to 960 primitives "
            "while 39+120+81=240 preserves H1=81."
        ),
        "honesty_boundary": (
            "This is a finite scheduler/QEC retry-kernel theorem. It does not "
            "prove a physical fusion threshold, detector model, loss budget, "
            "biological origin claim, or continuum dynamics theorem."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")


if __name__ == "__main__":
    main()
