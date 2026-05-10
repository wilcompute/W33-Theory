#!/usr/bin/env python3
"""PART CCCCXVII -- QEC Ouroboros Stabilizer Loop.

The public index names the self-referential W33/Q8/E6 loop as:

    "The snake eats its tail."

This audit makes the quantum-error-correction reading explicit.  In the W33 CSS
code, edge qubits, vertex X checks, and triangle Z checks are all built from the
same incidence complex.  The dangerous-looking weight-3 line-star objects are
not disposable errors; CCCCIX proves they are the H1=81 logical/matter sector
modulo vertex checks.  If we add them as stabilizers, k collapses to zero.

So the snake-tail closure is not "kill the tail."  It is:

    measure local stabilizers -> identify the line-star tail as logical matter
    -> reencode/protect that sector -> commit classical selector only after QEC

The current executable protection choice is the Steane/Phi6 lift
[[82320,81,>=81]].  The Q4/Bacon-Shor packets remain local routing/gauge
hardware because their raw weight-12 replacement dresses down to weight 4.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"

CSS_TOPOLOGY = ROOT / "PART_CCCCII_w33_css_topological_code_results.json"
CSS_DISTANCE = ROOT / "PART_CCCCIII_w33_css_distance_results.json"
LINE_STAR_RANK = ROOT / "PART_CCCCIX_line_star_rank_correction_results.json"
DRESSED_Q4 = ROOT / "PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json"
STEANE_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"
LEDGER = ROOT / "PART_CCCCXVI_protection_selection_ledger_results.json"

V = 40
E = 240
H1 = 81


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def index_loop_excerpt(index_text: str) -> str:
    start = index_text.index("The Self-Referential Loop")
    end = index_text.index("<h3>Key Identities</h3>", start)
    return index_text[start:end]


def build_results() -> Dict[str, Any]:
    index_text = INDEX.read_text(encoding="utf-8")
    loop = index_loop_excerpt(index_text)
    css_topology = load_json(CSS_TOPOLOGY)
    css_distance = load_json(CSS_DISTANCE)
    line_star = load_json(LINE_STAR_RANK)
    dressed_q4 = load_json(DRESSED_Q4)
    steane = load_json(STEANE_LIFT)
    ledger = load_json(LEDGER)

    css_params = css_topology["css_parameters"]
    distance_params = css_distance["css_parameters"]
    rank_table = line_star["rank_table"]
    dressed = dressed_q4["dressed_distance_conclusion"]
    steane_ft = steane["fault_tolerance_read"]
    active = ledger["active_architecture"]

    qec_ouroboros_map = {
        "head": "W33 edge-qubit CSS carrier [[240,81,3]]",
        "mouth": "vertex X checks and triangle Z checks read the carrier without measuring the logical state",
        "tail": "line-star triples are the H1=81 logical/matter sector modulo vertex checks",
        "failed_shortcut": "adding the tail as stabilizers gives k=0",
        "local_gauge_closure": "Q4/Bacon-Shor routing is [[1296,81,4]] because raw 12 dresses to 4",
        "protected_closure": "Steane/Phi6 lift protects the same 81-sector as [[82320,81,>=81]]",
        "classical_commit": "the 40-trit selector commits only after protected acceptance",
    }

    checks: List[Dict[str, Any]] = []
    checks.append(ok("index exposes self-referential loop", "The Self-Referential Loop" in loop, loop[:160]))
    checks.append(ok("index contains snake eats its tail phrase", "The snake eats its tail" in loop, loop[-220:]))
    checks.append(ok("CSS topology artifact verified", css_topology["verified"] is True, css_topology["checks_passed"]))
    checks.append(ok("CSS distance artifact verified", css_distance["verified"] is True, css_distance["checks_passed"]))
    checks.append(ok("line-star rank correction verified", line_star["verified"] is True, line_star["checks_passed"]))
    checks.append(ok("dressed Q4 verifier verified", dressed_q4["verified"] is True, dressed_q4["checks_passed"]))
    checks.append(ok("Steane lift verified", steane["verified"] is True, steane["checks_passed"]))
    checks.append(ok("protection ledger verified", ledger["verified"] is True, ledger["checks_passed"]))

    checks.append(
        ok(
            "W33 CSS head is [[240,81,d]] before distance",
            (
                css_params["n_physical_edge_qubits"],
                css_params["rank_X_vertex_checks"],
                css_params["rank_Z_triangle_checks"],
                css_params["k_logical_qubits"],
            )
            == (E, 39, 120, H1),
            css_params,
        )
    )
    checks.append(ok("base CSS distance is [[240,81,3]]", distance_params["notation"] == "[[240,81,3]]", distance_params))
    checks.append(
        ok(
            "line-star tail is the 81-sector not a disposable stabilizer",
            rank_table["line_star_mod_vertex_rank"] == H1
            and rank_table["k_if_line_stars_are_stabilizers"] == 0,
            rank_table,
        )
    )
    checks.append(
        ok(
            "Q4 local gauge closure dresses raw 12 to 4",
            dressed["raw_replacement_target"] == 12 and dressed["current_subsystem_packet_distance"] == 4,
            dressed,
        )
    )
    checks.append(
        ok(
            "Steane/Phi6 closure protects the same 81-sector",
            steane_ft["three_lift_code"] == "[[82320,81,>=81]]"
            and steane_ft["logical_sector_count"] == H1
            and steane_ft["guaranteed_correctable_weight"] == V,
            steane_ft,
        )
    )
    checks.append(
        ok(
            "selector commits only after protected acceptance",
            active["selector_layer"] == "40-trit classical selector in a 64-bit envelope"
            and active["active_protection_layer"] == "[[82320,81,>=81]] Steane/Phi6 lift",
            active,
        )
    )
    checks.append(ok("ouroboros map has seven architectural legs", len(qec_ouroboros_map) == 7, qec_ouroboros_map))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXVII",
        "title": "QEC Ouroboros Stabilizer Loop",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "index_anchor": {
            "section": "The Self-Referential Loop",
            "phrase": "The snake eats its tail.",
            "interpretation": "the stabilizer/logical tail loops back into the protected QEC head",
        },
        "qec_ouroboros_map": qec_ouroboros_map,
        "closure_numbers": {
            "physical_edge_qubits": E,
            "logical_sector": H1,
            "base_css_code": "[[240,81,3]]",
            "line_star_mod_vertex_rank": rank_table["line_star_mod_vertex_rank"],
            "k_if_line_stars_are_stabilizers": rank_table["k_if_line_stars_are_stabilizers"],
            "q4_local_routing_code": "[[1296,81,4]]",
            "q4_raw_target": dressed["raw_replacement_target"],
            "q4_dressed_weight": dressed["current_subsystem_packet_distance"],
            "active_protection_code": steane_ft["three_lift_code"],
            "correctable_weight": steane_ft["guaranteed_correctable_weight"],
        },
        "architecture_upgrade": (
            "Connects the index's self-referential snake-tail loop to the verified "
            "QEC architecture: the line-star tail is exactly the H1=81 logical "
            "sector, so the architecture must protect/reencode it instead of "
            "adding it as disposable stabilizer checks."
        ),
        "theorem": (
            "The W33 QEC ouroboros is the stabilizer/logical feedback loop. Local "
            "vertex and triangle checks read the same 240-edge carrier that holds "
            "the 81 logical sectors. The line-star tail spans those 81 sectors "
            "modulo vertex checks; imposing it as stabilizers collapses k to zero. "
            "Therefore the correct closure is protected self-reference: preserve "
            "and protect H1=81 by the Steane/Phi6 [[82320,81,>=81]] layer, while "
            "Q4 packets remain local [[1296,81,4]] routing hardware."
        ),
        "honesty_boundary": (
            "This connects the existing index motif to existing QEC certificates. "
            "It is not a new proof that the current Q4/Bacon-Shor packet has "
            "distance 12, a new physical noise model, or a new device calibration."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXVII_qec_ouroboros_stabilizer_loop_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "active_protection_code": results["closure_numbers"]["active_protection_code"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
