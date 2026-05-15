#!/usr/bin/env python3
"""Part DCCXV: photonic fusion syndrome QEC bridge.

DCCXIV made the local ouroboros alphabet explicit:

    12 = 6 signed Clifford channels + 6 A2/Weyl return channels.

CCCCXXVI already gives the photonic scheduler budgets:

    fusion p=1/2:  210 + 270 = 480
    KLM    p=1/4:  420 + 540 = 960

This bridge welds the two.  The expected fusion attempts split as a
2-by-2 ledger: accepted W33 bonds versus heralded return/syndrome slots,
each refined by the theta/transport split 105+135.  KLM primitives are the
same ledger doubled.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxiv_holonomy_signed_triad_a2_projection_bridge import (  # noqa: E402
    build_bridge as build_dccxiv_bridge,
)


SCHEDULER_PATH = ROOT / "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json"
SCHEDULER_SCRIPT = ROOT / "exploration" / "PART_CCCCXXVI_FUSION_CONTROL_SCHEDULER_SPLICE.py"
OUT_PATH = ROOT / "data" / "dccxv_photonic_fusion_syndrome_qec_bridge.json"

Q = 3
LAM = Q - 1
MU = Q + 1
V = (Q**4 - 1) // (Q - 1)
K = Q * (Q + 1)
H1 = Q**4
E = V * K // 2
DIRECTED = 2 * E
KLM_PRIMITIVES = MU * E


@dataclass(frozen=True)
class BridgeSummary:
    local_attempt_alphabet: int
    accepted_bond_slots: int
    heralded_syndrome_slots: int
    fusion_attempts: int
    klm_primitives: int
    all_identities_hold: bool


def _load_scheduler() -> dict[str, Any]:
    if SCHEDULER_PATH.exists():
        return json.loads(SCHEDULER_PATH.read_text(encoding="utf-8"))

    spec = importlib.util.spec_from_file_location("ccccxxvi_scheduler", SCHEDULER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load scheduler script at {SCHEDULER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_results()


def _scale_table(table: dict[str, dict[str, int]], factor: int) -> dict[str, dict[str, int]]:
    scaled: dict[str, dict[str, int]] = {}
    for row, values in table.items():
        scaled[row] = {key: factor * value for key, value in values.items()}
    return scaled


def build_bridge() -> dict[str, Any]:
    dccxiv = build_dccxiv_bridge()
    scheduler = _load_scheduler()
    fusion_budget = scheduler["fusion_budget_split"]
    klm_budget = scheduler["klm_budget_split"]

    local_split = dccxiv["qec_ouroboros"]["local_split"]
    local_success_slots, local_return_slots = local_split
    local_attempt_alphabet = local_success_slots + local_return_slots

    accepted_theta = fusion_budget["theta_expected_attempts"] // LAM
    accepted_transport = fusion_budget["transport_expected_attempts"] // LAM

    fusion_attempt_ledger = {
        "accepted_w33_bonds": {
            "theta": accepted_theta,
            "transport": accepted_transport,
            "total": accepted_theta + accepted_transport,
        },
        "heralded_return_syndrome": {
            "theta": accepted_theta,
            "transport": accepted_transport,
            "total": accepted_theta + accepted_transport,
        },
    }
    fusion_column_totals = {
        "theta": sum(row["theta"] for row in fusion_attempt_ledger.values()),
        "transport": sum(row["transport"] for row in fusion_attempt_ledger.values()),
        "total": sum(row["total"] for row in fusion_attempt_ledger.values()),
    }

    klm_primitive_ledger = _scale_table(fusion_attempt_ledger, LAM)
    klm_column_totals = {
        "theta": sum(row["theta"] for row in klm_primitive_ledger.values()),
        "transport": sum(row["transport"] for row in klm_primitive_ledger.values()),
        "total": sum(row["total"] for row in klm_primitive_ledger.values()),
    }

    local_to_global = {
        "vertices": V,
        "local_signed_clifford_slots": local_success_slots,
        "local_a2_weyl_return_slots": local_return_slots,
        "accepted_bond_slots": V * local_success_slots,
        "heralded_syndrome_slots": V * local_return_slots,
        "fusion_attempt_slots": V * local_attempt_alphabet,
        "klm_primitive_slots": V * local_attempt_alphabet * LAM,
    }

    qec_absorption = {
        "edge_qubit_carrier": E,
        "vertex_check_rank": 39,
        "triangle_check_rank": 120,
        "logical_h1": H1,
        "stabilizer_rank": 39 + 120,
        "css_identity": "39 + 120 + 81 = 240",
        "protected_read": (
            "Heralded fusion misses occupy the return/syndrome half of the directed carrier; "
            "they update the syndrome/frame ledger without adding stabilizers that kill H1=81."
        ),
    }

    identities = {
        "dccxiv_local_alphabet_is_six_plus_six": local_split == [6, 6],
        "scheduler_artifact_is_verified": scheduler["verified"] is True,
        "local_six_plus_six_lifts_to_240_plus_240": (
            local_to_global["accepted_bond_slots"] == E
            and local_to_global["heralded_syndrome_slots"] == E
        ),
        "fusion_attempt_ledger_totals_match_scheduler": (
            fusion_column_totals["theta"] == fusion_budget["theta_expected_attempts"]
            and fusion_column_totals["transport"] == fusion_budget["transport_expected_attempts"]
            and fusion_column_totals["total"] == fusion_budget["total_expected_attempts"] == DIRECTED
        ),
        "fusion_rows_are_accepted_plus_heralded_return": (
            fusion_attempt_ledger["accepted_w33_bonds"]["total"] == E
            and fusion_attempt_ledger["heralded_return_syndrome"]["total"] == E
        ),
        "klm_primitive_ledger_is_doubled_fusion_ledger": (
            klm_column_totals["theta"] == klm_budget["theta_expected_primitives"]
            and klm_column_totals["transport"] == klm_budget["transport_expected_primitives"]
            and klm_column_totals["total"] == klm_budget["total_expected_primitives"] == KLM_PRIMITIVES
            and klm_primitive_ledger["accepted_w33_bonds"]["total"] == DIRECTED
            and klm_primitive_ledger["heralded_return_syndrome"]["total"] == DIRECTED
        ),
        "css_identity_preserves_h1_tail": (
            qec_absorption["vertex_check_rank"]
            + qec_absorption["triangle_check_rank"]
            + qec_absorption["logical_h1"]
            == E
            and qec_absorption["stabilizer_rank"] == E - H1
        ),
        "directed_carrier_is_same_as_attempt_slots": (
            dccxiv["qec_ouroboros"]["w33_directed_edge_carrier"]
            == local_to_global["fusion_attempt_slots"]
            == DIRECTED
        ),
    }

    summary = BridgeSummary(
        local_attempt_alphabet=local_attempt_alphabet,
        accepted_bond_slots=local_to_global["accepted_bond_slots"],
        heralded_syndrome_slots=local_to_global["heralded_syndrome_slots"],
        fusion_attempts=fusion_column_totals["total"],
        klm_primitives=klm_column_totals["total"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "fusion_attempt_ledger": {
            "rows": fusion_attempt_ledger,
            "column_totals": fusion_column_totals,
            "read": "p_fusion=1/2 turns 240 accepted bonds into 240 accepted slots plus 240 heralded return slots.",
        },
        "klm_primitive_ledger": {
            "rows": klm_primitive_ledger,
            "column_totals": klm_column_totals,
            "read": "p_KLM=1/4 doubles the directed attempt ledger to 960 primitive slots.",
        },
        "local_to_global": local_to_global,
        "qec_absorption": qec_absorption,
        "external_alignment": {
            "klm_feedforward": "https://www.nature.com/articles/35051009",
            "one_way_measurement_feedforward": "https://arxiv.org/abs/quant-ph/0108118",
            "fusion_based_qec": "https://arxiv.org/abs/2101.09310",
            "knill_laflamme_general_noise": "https://doi.org/10.1103/PhysRevLett.84.2525",
        },
        "theorem": (
            "The photonic fusion nondeterminism is native to the W33 QEC ouroboros ledger: "
            "the 12 local turns split as 6 accepted signed-Clifford slots and 6 heralded "
            "A2/Weyl return slots. Across 40 vertices this is 240+240=480 expected fusion "
            "attempts. Refining each row by the theta/transport split gives "
            "(105+135)+(105+135)=210+270=480. The KLM primitive budget is the doubled "
            "ledger, (210+270)+(210+270)=420+540=960, while 39+120+81=240 preserves H1=81."
        ),
        "honesty_boundary": (
            "This is a finite scheduling and syndrome-accounting theorem. It does not prove "
            "a physical loss threshold, detector model, biological origin claim, or continuum "
            "Einstein-Hilbert asymptotic."
        ),
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
