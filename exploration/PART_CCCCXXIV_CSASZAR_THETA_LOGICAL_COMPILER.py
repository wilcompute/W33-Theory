#!/usr/bin/env python3
"""PART CCCCXXIV -- Csaszar Theta Logical Compiler.

CCCCXXIII proves that each Csaszar K7 torus carries a local CSS toric code

    [[21, 2, >=3]]

and CCCCXXII identifies five Csaszar modes as the input register inside the
seven-mode photonic harmonic algebra A(7).

This compiler proves the next exact alignment:

    five Csaszar inputs * two toric logical qubits = 10 = theta(W33).

So the Lovasz-theta value in CCCCXIX is not only an abstract graph invariant. It
is also the logical size of the five local Csaszar toric input blocks. The local
ground-state degeneracy 4 is theta(complement), and

    10 * 4 = 40 = Shannon capacity / W33 vertex count.

The two Szilassi ancilla modes contribute 2*Phi6 = 14 = dim(G2).  Together with
one scalar/control line, the rank bookkeeping also closes as

    105 local edge qubits + 14 G2 ancilla modes + 1 scalar = 120,

matching the W33 triangle-check rank.  This last equality is only a rank
handoff, not a claimed canonical isomorphism.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]

SYNTHESIS = ROOT / "PART_CCCCXIX_photonic_harmonic_tqc_synthesis_results.json"
TOROIDAL_ALGEBRA = ROOT / "PART_CCCCXXII_toroidal_photonic_algebra_results.json"
A7_TORIC = ROOT / "PART_CCCCXXIII_a7_representation_css_toric_results.json"
CSS_TOPO = ROOT / "PART_CCCCII_w33_css_topological_code_results.json"
CSS_DISTANCE = ROOT / "PART_CCCCIII_w33_css_distance_results.json"

Q = 3
LAM = Q - 1
MU = Q + 1
PHI6 = Q * Q - Q + 1
G2_DIM = 2 * PHI6


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def build_results() -> Dict[str, Any]:
    synthesis = load_json(SYNTHESIS)
    toroidal = load_json(TOROIDAL_ALGEBRA)
    a7 = load_json(A7_TORIC)
    css_topo = load_json(CSS_TOPO)
    css_distance = load_json(CSS_DISTANCE)

    arch = synthesis["architecture"]
    toroidal_alg = toroidal["algebra"]
    local_css = a7["css_code"]
    algebra = a7["algebra"]
    betti = a7["betti"]
    topo_params = css_topo["css_parameters"]
    distance_params = css_distance["css_parameters"]

    csaszar_blocks = toroidal_alg["input_modes_csaszar"]
    szilassi_ancilla = toroidal_alg["ancilla_modes_szilassi"]
    local_n = local_css["n"]
    local_k = local_css["k"]
    local_gsd = local_css["gsd"]
    local_d_lower = local_css["d_lower"]
    global_n = csaszar_blocks * local_n
    global_k = csaszar_blocks * local_k
    global_check_rank = csaszar_blocks * (local_css["rank_hz"] + local_css["rank_hx"])
    global_gsd = local_gsd**csaszar_blocks
    ancilla_g2_modes = szilassi_ancilla * PHI6
    scalar_control_line = 1
    rank_120_closure = global_n + ancilla_g2_modes + scalar_control_line

    compiler_layers = [
        {
            "name": "five_csaszar_input_blocks",
            "invariant": "5 local K7 toric blocks",
            "output": "[[105,10,>=3]] direct-product lower-bound packet",
        },
        {
            "name": "lovasz_theta_logical_register",
            "invariant": "5*2 = 10 = theta(W33)",
            "output": "ten local toric logical qubits",
        },
        {
            "name": "szilassi_g2_ancilla_rail",
            "invariant": "2*Phi6 = 14 = dim(G2)",
            "output": "ancilla symmetry rail for A(7)",
        },
        {
            "name": "rank_120_bookkeeping_closure",
            "invariant": "105 + 14 + 1 = 120",
            "output": "matches W33 triangle-check rank as a handoff count",
        },
    ]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("CCCCXIX synthesis verified", synthesis["verified"] is True, synthesis["checks_passed"]))
    checks.append(ok("CCCCXXII toroidal algebra verified", toroidal["verified"] is True, toroidal["checks_passed"]))
    checks.append(ok("CCCCXXIII A7 toric verified", a7["verified"] is True, a7["checks_passed"]))
    checks.append(ok("W33 CSS topology verified", css_topo["verified"] is True, css_topo["checks_passed"]))
    checks.append(ok("W33 CSS distance verified", css_distance["verified"] is True, css_distance["checks_passed"]))

    checks.append(ok("A(7) has seven modes", toroidal_alg["modes"] == PHI6 == algebra["modes"], {"toroidal": toroidal_alg, "a7": algebra}))
    checks.append(ok("five Csaszar input blocks", csaszar_blocks == PHI6 - LAM == 5, csaszar_blocks))
    checks.append(ok("two Szilassi ancilla modes", szilassi_ancilla == LAM == 2, szilassi_ancilla))
    checks.append(ok("local Csaszar CSS code is [[21,2,>=3]]", (local_n, local_k, local_d_lower) == (21, LAM, Q), local_css))
    checks.append(ok("local toric GSD is mu", local_gsd == MU == arch["complement_theta"], {"local_gsd": local_gsd, "complement_theta": arch["complement_theta"]}))
    checks.append(ok("local k equals torus beta1", local_k == betti["beta_1"] == LAM, betti))

    checks.append(ok("five local blocks have n=105", global_n == 105, global_n))
    checks.append(ok("five local blocks have k=10", global_k == 10, global_k))
    checks.append(ok("five-block logical size equals Lovasz theta", global_k == arch["lovasz_theta"], arch))
    checks.append(ok("theta times local GSD equals Shannon capacity", global_k * local_gsd == arch["shannon_capacity"] == 40, {"global_k": global_k, "local_gsd": local_gsd, "capacity": arch["shannon_capacity"]}))
    checks.append(ok("global GSD is 4^5 = 2^10", global_gsd == 4**5 == 2**global_k, global_gsd))
    checks.append(ok("direct product check rank closes n-k", global_check_rank == global_n - global_k == 95, {"rank": global_check_rank, "n": global_n, "k": global_k}))

    checks.append(ok("five Csaszar vertex sets total 35 = U7-G2", csaszar_blocks * PHI6 == algebra["u7_dim"] - algebra["g2_dim"] == 35, algebra))
    checks.append(ok("Szilassi ancilla rail is G2", ancilla_g2_modes == G2_DIM == algebra["g2_dim"], {"ancilla": ancilla_g2_modes, "g2": algebra["g2_dim"]}))
    checks.append(ok("theta logicals plus G2 rail gives 24", global_k + ancilla_g2_modes == 24, {"theta": global_k, "g2": ancilla_g2_modes}))
    checks.append(ok("rank-120 bookkeeping closure matches W33 triangle rank", rank_120_closure == topo_params["rank_Z_triangle_checks"] == 120, {"local_n": global_n, "g2": ancilla_g2_modes, "scalar": scalar_control_line, "rank": topo_params["rank_Z_triangle_checks"]}))

    checks.append(ok("W33 base CSS is [[240,81,3]]", distance_params["notation"] == "[[240,81,3]]", distance_params))
    checks.append(ok("local distance lower bound equals W33 base distance", local_d_lower == distance_params["d"] == Q, {"local": local_d_lower, "w33": distance_params["d"]}))
    checks.append(ok("W33 logical sector remains H1=81", topo_params["k_logical_qubits"] == Q**4 == 81, topo_params))
    checks.append(ok("compiler has four ordered layers", [layer["name"] for layer in compiler_layers] == ["five_csaszar_input_blocks", "lovasz_theta_logical_register", "szilassi_g2_ancilla_rail", "rank_120_bookkeeping_closure"], compiler_layers))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXIV",
        "title": "Csaszar Theta Logical Compiler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "local_code": {
            "notation": "[[21,2,>=3]]",
            "n": local_n,
            "k": local_k,
            "d_lower": local_d_lower,
            "gsd": local_gsd,
            "rank_hz": local_css["rank_hz"],
            "rank_hx": local_css["rank_hx"],
        },
        "five_block_packet": {
            "blocks": csaszar_blocks,
            "notation": "[[105,10,>=3]]",
            "n": global_n,
            "k": global_k,
            "d_lower": local_d_lower,
            "check_rank": global_check_rank,
            "gsd": global_gsd,
            "logical_equals_lovasz_theta": global_k == arch["lovasz_theta"],
            "theta_times_local_gsd": global_k * local_gsd,
        },
        "ancilla_and_rank_closure": {
            "szilassi_ancilla_modes": szilassi_ancilla,
            "ancilla_g2_modes": ancilla_g2_modes,
            "theta_plus_g2": global_k + ancilla_g2_modes,
            "rank_120_closure": rank_120_closure,
            "rank_120_read": "105 local Csaszar edge qubits + 14 G2 ancilla modes + 1 scalar/control line = W33 triangle-check rank 120",
        },
        "compiler_layers": compiler_layers,
        "architecture_upgrade": (
            "Identifies the Lovasz theta=10 register as the ten toric logical qubits "
            "carried by the five Csaszar K7 input blocks, and separates the two "
            "Szilassi modes as a G2=14 ancilla rail."
        ),
        "theorem": (
            "The five Csaszar input modes of A(7) compile to a direct-product local "
            "toric packet [[105,10,>=3]]. Its ten logical qubits equal Lovasz "
            "theta(W33)=10, while the local ground-state degeneracy equals "
            "theta(complement)=4 and 10*4=40 equals the W33 Shannon-capacity/vertex "
            "count. The two Szilassi ancilla modes supply 14=dim(G2), and the rank "
            "bookkeeping closes as 105+14+1=120, matching the W33 triangle-check "
            "rank without claiming a canonical isomorphism."
        ),
        "honesty_boundary": (
            "This is a local-to-global logical compiler and rank handoff. It does "
            "not prove a physical threshold, does not replace the Steane/Phi6 "
            "[[82320,81,>=81]] protection layer, and does not make the rank-120 "
            "bookkeeping equality into a canonical operator isomorphism."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXIV_csaszar_theta_logical_compiler_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "five_block_code": results["five_block_packet"]["notation"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
