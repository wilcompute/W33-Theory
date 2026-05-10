#!/usr/bin/env python3
"""PART CCCCXVI -- Protection / Selection Ledger.

The current architecture has several valid components with different roles:

  - heralded photonic fusion/KLM attempts are retried;
  - triangle-flat cyclic covers are valid but do not raise distance;
  - line-star triples are the 81-dimensional matter sector, not disposable checks;
  - Q4/Bacon-Shor packets give local subsystem routing with dressed distance 4;
  - Steane/Phi6 concatenation gives the committed distance-81 protection layer;
  - only after protection does the 40-trit word become a classical selector.

This ledger prevents category mistakes.  In particular, it prevents the raw
Q4 packet replacement weight 12 from being used as a dressed-distance claim, and
it keeps the Steane/Phi6 lift as the active fault-tolerance layer.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]

Q = 3
V = 40
H1 = Q**4

SCHEDULER = ROOT / "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json"
CYCLIC_LOW_WEIGHT = ROOT / "PART_CCCCVII_cyclic_cover_low_weight_logicals_results.json"
LINE_STAR_RANK = ROOT / "PART_CCCCIX_line_star_rank_correction_results.json"
Q4_PACKET = ROOT / "PART_CCCCXIV_integrated_q4_packet_subsystem_matrix_results.json"
DRESSED_Q4 = ROOT / "PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json"
STEANE_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"
KERNEL = ROOT / "PART_CCCCV_protected_toe_kernel_results.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def build_results() -> Dict[str, Any]:
    scheduler = load_json(SCHEDULER)
    cyclic = load_json(CYCLIC_LOW_WEIGHT)
    line_star = load_json(LINE_STAR_RANK)
    q4 = load_json(Q4_PACKET)
    dressed = load_json(DRESSED_Q4)
    steane = load_json(STEANE_LIFT)
    kernel = load_json(KERNEL)

    cyclic_audits = cyclic["cover_audits"]
    line_rank = line_star["rank_table"]
    q4_packet = q4["global_packet_subsystem"]
    dressed_conclusion = dressed["dressed_distance_conclusion"]
    steane_ft = steane["fault_tolerance_read"]
    scheduler_contract = scheduler["handoff_contract"]

    ledger = [
        {
            "mechanism": "heralded_photonic_assembly",
            "source": "CCCCVI",
            "status": "retry_before_logic",
            "decision": "fusion/KLM failures are hardware retries, not committed logical faults",
            "scale": {"fusion_attempts": 480, "klm_attempts": 960},
        },
        {
            "mechanism": "triangle_flat_cyclic_covers",
            "source": "CCCCVII",
            "status": "valid_but_rejected_as_distance_upgrade",
            "decision": "L=2 and L=3 covers commute but retain d=3 via inherited line-star X logicals",
            "scale": {"L2_distance": 3, "L3_distance": 3},
        },
        {
            "mechanism": "line_star_matter_sector",
            "source": "CCCCIX",
            "status": "preserve_and_reencode",
            "decision": "line-stars span the 81-dimensional matter sector modulo vertex checks; killing them collapses k to zero",
            "scale": {"matter_rank": H1, "k_if_stabilized": 0},
        },
        {
            "mechanism": "q4_bacon_shor_packet",
            "source": "CCCCXIV/CCCCXV",
            "status": "local_routing_not_final_distance_layer",
            "decision": "the Q4 packet layer is [[1296,81,4]]; raw weight 12 dresses to weight 4 in the current center",
            "scale": {"packet_distance": 4, "raw_target": 12},
        },
        {
            "mechanism": "steane_phi6_lift",
            "source": "CCCCIV/CCCCVI",
            "status": "committed_quantum_protection",
            "decision": "the active protection layer is [[82320,81,>=81]], correcting 40 faults",
            "scale": {"distance_lower_bound": H1, "correctable_weight": V},
        },
        {
            "mechanism": "classical_selector_commit",
            "source": "CCCCVI",
            "status": "commit_after_protection",
            "decision": "the 40-trit selector is exposed only after protected logical acceptance",
            "scale": {"measurement_trits": V, "controller_bits": 64},
        },
        {
            "mechanism": "e8_z3_operation_gate",
            "source": "CCCCV/CCCCVI",
            "status": "bounded_operation_gate",
            "decision": "the protected H1=81 sector feeds the verified E8 Z3 operation gate",
            "scale": {"h1": H1, "z3_terms_checked": 8347},
        },
    ]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("scheduler verified", scheduler["verified"] is True, scheduler["checks_passed"]))
    checks.append(ok("cyclic low-weight audit verified", cyclic["verified"] is True, cyclic["checks_passed"]))
    checks.append(ok("line-star rank correction verified", line_star["verified"] is True, line_star["checks_passed"]))
    checks.append(ok("Q4 packet matrix verified", q4["verified"] is True, q4["checks_passed"]))
    checks.append(ok("dressed Q4 verifier verified", dressed["verified"] is True, dressed["checks_passed"]))
    checks.append(ok("Steane lift verified", steane["verified"] is True, steane["checks_passed"]))
    checks.append(ok("protected kernel verified", kernel["verified"] is True, kernel["checks_passed"]))

    checks.append(ok("cyclic covers preserve d=3", cyclic_audits["L2"]["distance_conclusion"] == "d=3 because d_X=3" and cyclic_audits["L3"]["distance_conclusion"] == "d=3 because d_X=3", cyclic_audits))
    checks.append(ok("line-stars are full 81 matter sector", line_rank["line_star_mod_vertex_rank"] == H1 and line_rank["k_if_line_stars_are_stabilizers"] == 0, line_rank))
    checks.append(ok("Q4 packet layer is [[1296,81,4]]", (q4_packet["n"], q4_packet["k"], q4_packet["d_packet_layer"]) == (1296, 81, 4), q4_packet))
    checks.append(ok("Q4 raw 12 target dresses to 4", dressed_conclusion["raw_replacement_target"] == 12 and dressed_conclusion["current_subsystem_packet_distance"] == 4, dressed_conclusion))
    checks.append(ok("Steane layer remains active distance-81 protection", steane_ft["three_lift_code"] == "[[82320,81,>=81]]" and steane_ft["guaranteed_correctable_weight"] == V, steane_ft))
    checks.append(ok("classical selector stays after protection", "64-bit-class" in scheduler_contract["protected_to_classical"] and scheduler["controller_envelope"]["measurement_trits"] == V, scheduler["controller_envelope"]))
    checks.append(ok("E8 operation gate stays bounded", kernel["closure_equalities"]["e8_z3_terms_checked"] == 8347 and kernel["closure_equalities"]["logical_sector"] == H1, kernel["closure_equalities"]))
    checks.append(ok("ledger has seven distinct decisions", len(ledger) == 7 and len({entry["mechanism"] for entry in ledger}) == 7, ledger))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXVI",
        "title": "Protection / Selection Ledger",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "ledger": ledger,
        "active_architecture": {
            "retry_layer": "heralded photonic assembly",
            "rejected_distance_upgrade": "triangle-flat cyclic covers L=2,3 remain d=3",
            "local_routing_layer": "[[1296,81,4]] Q4/Bacon-Shor subsystem packets",
            "active_protection_layer": "[[82320,81,>=81]] Steane/Phi6 lift",
            "selector_layer": "40-trit classical selector in a 64-bit envelope",
            "operation_layer": "H1=81 -> E8 Z3 gate with 8347 checked bracket terms",
        },
        "architecture_upgrade": (
            "Converts the recent cover, line-star, Q4 packet, dressed-distance, "
            "Steane, scheduler, and E8 artifacts into a protection/selection ledger "
            "that assigns each mechanism its correct architectural role."
        ),
        "theorem": (
            "In the current architecture, triangle-flat cyclic covers are valid but "
            "do not raise distance; line-star triples are the H1=81 matter sector; "
            "Q4/Bacon-Shor packets provide local [[1296,81,4]] subsystem routing but "
            "not a dressed [[1296,81,>=12]] proof; therefore the active quantum "
            "protection layer remains the Steane/Phi6 [[82320,81,>=81]] lift. The "
            "40-trit selector is committed only after that protection layer accepts, "
            "then the H1=81 sector feeds the bounded E8 Z3 gate."
        ),
        "honesty_boundary": (
            "This ledger solves role assignment, not device calibration. It does not "
            "simulate optical loss, detector dark counts, decoding latency, or a "
            "future column-locked Q4 distance repair."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXVI_protection_selection_ledger_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "active_protection_layer": results["active_architecture"]["active_protection_layer"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
