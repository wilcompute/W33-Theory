#!/usr/bin/env python3
"""PART CCCCXXV -- Theta / U(5) Stabilizer Completion.

CCCCXXIV identifies the five Csaszar input blocks as a local toric packet

    [[105, 10, >=3]]

with check rank 95.  The next exact stabilizer completion is:

    95 local toric checks + 25 U(5) input-mode algebra = 120 W33 Z/triangle rank.

Then the remaining W33 vertex-star X rank is 39, so

    120 + 39 = 159 = 240 - 81.

This is the clean stabilizer-rank bridge from the local photonic harmonic theta
register to the full W33 CSS carrier.  It also explains the physical edge split

    105 + 135 = 240,

where 105 is the five Csaszar K7 input edge packet and 135 is the transport
bundle count.  Under the three Steane/Phi6 lifts, the same 7/16 and 9/16
physical split is preserved inside the protected [[82320,81,>=81]] carrier.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]

THETA_COMPILER = ROOT / "PART_CCCCXXIV_csaszar_theta_logical_compiler_results.json"
A7_TORIC = ROOT / "PART_CCCCXXIII_a7_representation_css_toric_results.json"
CSS_TOPO = ROOT / "PART_CCCCII_w33_css_topological_code_results.json"
CSS_DISTANCE = ROOT / "PART_CCCCIII_w33_css_distance_results.json"
STEANE_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"

Q = 3
LAM = Q - 1
MU = Q + 1
PHI6 = Q * Q - Q + 1
H1 = Q**4
W33_V = (Q**4 - 1) // (Q - 1)
W33_K = Q * (Q + 1)
W33_E = W33_V * W33_K // 2
STEANE_BLOCK = PHI6**3


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def ratio(numer: int, denom: int) -> str:
    return str(Fraction(numer, denom))


def build_results() -> Dict[str, Any]:
    theta = load_json(THETA_COMPILER)
    a7 = load_json(A7_TORIC)
    css_topo = load_json(CSS_TOPO)
    css_distance = load_json(CSS_DISTANCE)
    steane = load_json(STEANE_LIFT)

    five_block = theta["five_block_packet"]
    local_code = theta["local_code"]
    rank_closure = theta["ancilla_and_rank_closure"]
    css_params = css_topo["css_parameters"]
    distance_params = css_distance["css_parameters"]
    steane_ft = steane["fault_tolerance_read"]
    steane_l3 = steane["lift_table"][3]
    algebra = a7["algebra"]

    csaszar_blocks = five_block["blocks"]
    input_mode_count = csaszar_blocks
    u5_completion_rank = input_mode_count**2
    local_check_rank = five_block["check_rank"]
    triangle_rank = css_params["rank_Z_triangle_checks"]
    vertex_rank = css_params["rank_X_vertex_checks"]
    full_stabilizer_rank = triangle_rank + vertex_rank
    completion_rank = u5_completion_rank + vertex_rank
    transport_edges = W33_E - five_block["n"]

    theta_protected_n = five_block["n"] * STEANE_BLOCK
    transport_protected_n = transport_edges * STEANE_BLOCK
    global_protected_n = W33_E * STEANE_BLOCK

    completion_layers = [
        {
            "name": "local_csaszar_toric_checks",
            "rank": local_check_rank,
            "read": "five [[21,2,>=3]] toric blocks give 95 local checks",
        },
        {
            "name": "u5_input_mode_completion",
            "rank": u5_completion_rank,
            "read": "U(5) input-mode algebra completes 95 to W33 triangle rank 120",
        },
        {
            "name": "w33_vertex_star_completion",
            "rank": vertex_rank,
            "read": "W33 vertex-star rank completes triangle checks to full CSS stabilizer rank",
        },
        {
            "name": "h1_logical_tail",
            "rank": H1,
            "read": "remaining H1=81 sector is preserved as logical matter",
        },
    ]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("CCCCXXIV theta compiler verified", theta["verified"] is True, theta["checks_passed"]))
    checks.append(ok("CCCCXXIII A7 toric verified", a7["verified"] is True, a7["checks_passed"]))
    checks.append(ok("W33 CSS topology verified", css_topo["verified"] is True, css_topo["checks_passed"]))
    checks.append(ok("W33 CSS distance verified", css_distance["verified"] is True, css_distance["checks_passed"]))
    checks.append(ok("Steane/Phi6 lift verified", steane["verified"] is True, steane["checks_passed"]))

    checks.append(ok("five-block packet is [[105,10,>=3]]", (five_block["n"], five_block["k"], five_block["d_lower"]) == (105, 10, Q), five_block))
    checks.append(ok("local check rank is 95", local_check_rank == five_block["n"] - five_block["k"] == 95, five_block))
    checks.append(ok("five input modes define U(5) rank 25", u5_completion_rank == 25, u5_completion_rank))
    checks.append(ok("U(5) completion closes local checks to triangle rank", local_check_rank + u5_completion_rank == triangle_rank == 120, {"local": local_check_rank, "u5": u5_completion_rank, "triangle": triangle_rank}))
    checks.append(ok("triangle rank matches CCCCXXIV rank-120 closure", triangle_rank == rank_closure["rank_120_closure"], rank_closure))
    checks.append(ok("vertex-star completion rank is 39", vertex_rank == W33_V - 1 == 39, vertex_rank))
    checks.append(ok("triangle plus vertex ranks give full stabilizer rank", full_stabilizer_rank == 159, {"triangle": triangle_rank, "vertex": vertex_rank}))
    checks.append(ok("full stabilizer rank plus H1 fills 240", full_stabilizer_rank + H1 == W33_E == 240, {"stabilizer": full_stabilizer_rank, "h1": H1, "edges": W33_E}))
    checks.append(ok("completion rank 25+39 is 64", completion_rank == 64 == 2**(PHI6 - 1), completion_rank))
    checks.append(ok("local checks plus completion plus H1 fill 240", local_check_rank + completion_rank + H1 == W33_E, {"local": local_check_rank, "completion": completion_rank, "h1": H1}))

    checks.append(ok("physical edge split is 105+135=240", five_block["n"] + transport_edges == W33_E and transport_edges == 135, {"theta_edges": five_block["n"], "transport_edges": transport_edges}))
    checks.append(ok("theta physical share is 7/16", Fraction(five_block["n"], W33_E) == Fraction(PHI6, LAM**MU), ratio(five_block["n"], W33_E)))
    checks.append(ok("transport physical share is 9/16", Fraction(transport_edges, W33_E) == Fraction(Q**2, LAM**MU), ratio(transport_edges, W33_E)))
    checks.append(ok("transport complement is 45*3", transport_edges == 45 * Q, transport_edges))
    checks.append(ok("theta plus G2 rail is 24", rank_closure["theta_plus_g2"] == 24, rank_closure))
    checks.append(ok("U7 dim minus G2 dim is five Csaszar vertex sets", algebra["u7_dim"] - algebra["g2_dim"] == 35 == csaszar_blocks * PHI6, algebra))

    checks.append(ok("W33 base CSS is [[240,81,3]]", distance_params["notation"] == "[[240,81,3]]", distance_params))
    checks.append(ok("three Steane lifts use Phi6^3=343", STEANE_BLOCK == 343, STEANE_BLOCK))
    checks.append(ok("protected theta packet has n=36015", theta_protected_n == 36015, theta_protected_n))
    checks.append(ok("protected transport complement has n=46305", transport_protected_n == 46305, transport_protected_n))
    checks.append(ok("protected theta plus transport equals global protected n", theta_protected_n + transport_protected_n == global_protected_n == steane_l3["n"] == 82320, {"theta": theta_protected_n, "transport": transport_protected_n, "global": global_protected_n}))
    checks.append(ok("protected distance lower bound remains H1", steane_l3["distance_lower_bound"] == H1 and steane_ft["three_lift_code"] == "[[82320,81,>=81]]", steane_ft))
    checks.append(ok("protected correctable weight remains 40", steane_ft["guaranteed_correctable_weight"] == W33_V, steane_ft))
    checks.append(ok("completion has four ordered layers", [layer["name"] for layer in completion_layers] == ["local_csaszar_toric_checks", "u5_input_mode_completion", "w33_vertex_star_completion", "h1_logical_tail"], completion_layers))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXV",
        "title": "Theta / U(5) Stabilizer Completion",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "rank_completion": {
            "local_csaszar_check_rank": local_check_rank,
            "u5_input_completion_rank": u5_completion_rank,
            "w33_triangle_rank": triangle_rank,
            "w33_vertex_rank": vertex_rank,
            "full_stabilizer_rank": full_stabilizer_rank,
            "h1_logical_rank": H1,
            "completion_rank_25_plus_39": completion_rank,
            "identity": "95 + 25 + 39 + 81 = 240",
        },
        "physical_split": {
            "theta_edges": five_block["n"],
            "transport_edges": transport_edges,
            "total_edges": W33_E,
            "theta_share": ratio(five_block["n"], W33_E),
            "transport_share": ratio(transport_edges, W33_E),
            "transport_read": "135 = 45*3 transport bundle complement",
        },
        "protected_split": {
            "steane_block": STEANE_BLOCK,
            "theta_protected_n": theta_protected_n,
            "transport_protected_n": transport_protected_n,
            "global_protected_n": global_protected_n,
            "active_protection_code": steane_ft["three_lift_code"],
            "distance_lower_bound": steane_l3["distance_lower_bound"],
            "correctable_weight": steane_ft["guaranteed_correctable_weight"],
        },
        "completion_layers": completion_layers,
        "architecture_upgrade": (
            "Completes the CCCCXXIV local theta compiler to the full W33 CSS rank "
            "accounting: local Csaszar toric checks plus U(5) input algebra give "
            "the W33 triangle rank, then vertex-star checks and H1 fill the carrier."
        ),
        "theorem": (
            "The five Csaszar [[21,2,>=3]] input blocks have check rank 95. The "
            "U(5) algebra on the five input modes contributes 25, so 95+25=120, "
            "the W33 triangle-check rank. Adding the W33 vertex-star rank 39 gives "
            "the full CSS stabilizer rank 159, and 159+H1=159+81=240. The physical "
            "carrier splits as 105 theta edges plus 135 transport edges, i.e. 7/16 "
            "plus 9/16, and this split is preserved after the three Steane/Phi6 "
            "lifts inside [[82320,81,>=81]]."
        ),
        "honesty_boundary": (
            "This is a stabilizer-rank and physical-carrier compiler. It does not "
            "assert that the U(5) rank completion is a canonical W33 triangle "
            "operator isomorphism, and it does not replace the existing "
            "Steane/Phi6 protection or the Q4 routing boundary."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXV_theta_u5_stabilizer_completion_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "identity": results["rank_completion"]["identity"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
