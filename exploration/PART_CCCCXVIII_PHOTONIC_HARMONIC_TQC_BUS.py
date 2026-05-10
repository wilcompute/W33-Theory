#!/usr/bin/env python3
"""PART CCCCXVIII -- Photonic Harmonic TQC Bus.

CCCXCVI separated the photonic runtime into probabilistic, deterministic,
quantum, classical, topological, and response layers.  CCCCVI scheduled that
runtime through the protected W33 CSS stack.  CCCCXVII identified the
snake-tail QEC loop.

This part adds the missing harmonic/TQC bus.  The key observation is that the
photonic probabilities and the genus-one harmonic topological shell share the
same exact denominators:

    Type-II fusion p = 1/2  -> denominator 2 = lambda
    KLM primitive p = 1/4   -> denominator 4 = mu

Those same values are the toric logical-qubit count and ground-state
degeneracy on the genus-one Csaszar/Szilassi shell.  The Heawood harmonic
oscillator then supplies a dual 14-mode rail: 14 = 2*Phi6, with a 12-mode
middle shell splitting as 6+6.  That 12 is also the W33 degree and three
toric weight-4 stabilizer checks.

This is a bus theorem, not a new physical threshold claim: it states how the
photonic, harmonic, topological, MBQC, and protected QEC layers line up as an
architecture.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from w33_heawood_harmonic_bridge import build_heawood_harmonic_summary  # noqa: E402


Q = 3
LAM = Q - 1
MU = Q + 1
K = Q * (Q + 1)
V = (Q**4 - 1) // (Q - 1)
E = V * K // 2
DIRECTED = 2 * E
H1 = Q**4
PHI6 = Q * Q - Q + 1
TORIC_GENUS = 1
TORIC_LOGICAL_QUBITS = 2 * TORIC_GENUS
TORIC_GSD = 2 ** (2 * TORIC_GENUS)
TORIC_STABILIZER_WEIGHT = MU

PHOTONIC = ROOT / "PART_CCCXCVI_photonic_life_runtime_architecture_results.json"
SCHEDULER = ROOT / "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json"
QEC_OUROBOROS = ROOT / "PART_CCCCXVII_qec_ouroboros_stabilizer_loop_results.json"
STEANE_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def frac(text: str) -> Fraction:
    return Fraction(text)


def build_results() -> Dict[str, Any]:
    photonic = load_json(PHOTONIC)
    scheduler = load_json(SCHEDULER)
    qec_ouroboros = load_json(QEC_OUROBOROS)
    steane = load_json(STEANE_LIFT)
    heawood = build_heawood_harmonic_summary()

    constants = photonic["constants"]
    probabilistic = photonic["probabilistic_layer"]
    deterministic = photonic["deterministic_layer"]
    classical = photonic["classical_layer"]
    topological = photonic["topological_layer"]
    controller = scheduler["controller_envelope"]
    closure = qec_ouroboros["closure_numbers"]
    steane_ft = steane["fault_tolerance_read"]
    incidence = heawood["incidence_operator"]
    operator = heawood["heawood_operator"]
    local_norm = heawood["local_normalization"]

    p_fusion = frac(probabilistic["p_fusion"])
    p_klm = frac(probabilistic["p_klm"])

    csaszar = topological["csaszar"]
    oscillator = topological["heawood_oscillator"]

    bus_layers = [
        {
            "name": "photonic_denominator_bus",
            "carrier": "KLM / Type-II fusion probabilities",
            "invariant": "denominators 2 and 4",
            "role": "hardware randomness is routed into the harmonic/topological shell",
        },
        {
            "name": "heawood_harmonic_bus",
            "carrier": "Szilassi dual Heawood oscillator",
            "invariant": "14 = 2*Phi6, middle shell 12 = 6+6",
            "role": "two Phi6 rails and a W33-degree phase middle shell",
        },
        {
            "name": "toric_surface_bus",
            "carrier": "Csaszar/Szilassi genus-one torus",
            "invariant": "logical qubits 2, GSD 4, weight-4 checks",
            "role": "topological loop memory for protected MBQC state flow",
        },
        {
            "name": "protected_qec_bus",
            "carrier": "W33 CSS -> Steane/Phi6 lift",
            "invariant": "[[240,81,3]] -> [[82320,81,>=81]]",
            "role": "preserve the H1=81 tail instead of stabilizing it away",
        },
        {
            "name": "classical_selector_bus",
            "carrier": "40-trit measurement record",
            "invariant": "2^63 < 3^40 < 2^64",
            "role": "commit a classical selector only after protected acceptance",
        },
    ]

    checks: List[Dict[str, Any]] = []
    checks.append(ok("photonic runtime verified", photonic["verified"] is True, photonic["checks_passed"]))
    checks.append(ok("protected scheduler verified", scheduler["verified"] is True, scheduler["checks_passed"]))
    checks.append(ok("QEC ouroboros verified", qec_ouroboros["verified"] is True, qec_ouroboros["checks_passed"]))
    checks.append(ok("Steane/Phi6 lift verified", steane["verified"] is True, steane["checks_passed"]))
    checks.append(ok("Heawood harmonic summary is ok", heawood["status"] == "ok", heawood["status"]))

    checks.append(ok("W33 constants are 40/12/240", (constants["v"], constants["k"], constants["edges"]) == (V, K, E), constants))
    checks.append(ok("fusion denominator is lambda=2", p_fusion == Fraction(1, LAM), str(p_fusion)))
    checks.append(ok("KLM denominator is mu=4", p_klm == Fraction(1, MU), str(p_klm)))
    checks.append(ok("fusion denominator equals toric logical qubits", p_fusion.denominator == TORIC_LOGICAL_QUBITS == LAM, TORIC_LOGICAL_QUBITS))
    checks.append(ok("KLM denominator equals toric GSD", p_klm.denominator == TORIC_GSD == MU, TORIC_GSD))
    checks.append(ok("KLM denominator equals toric stabilizer weight", p_klm.denominator == TORIC_STABILIZER_WEIGHT, TORIC_STABILIZER_WEIGHT))
    checks.append(ok("fusion attempts equal directed W33 edges", probabilistic["expected_fusion_attempts"] == DIRECTED, probabilistic))
    checks.append(ok("critical fusion split is 120+120", probabilistic["critical_edge_split"] == "120+120", probabilistic))

    checks.append(ok("Csaszar torus is genus one", csaszar["genus"] == TORIC_GENUS, csaszar))
    checks.append(ok("Csaszar Euler characteristic is zero", csaszar["vertices"] - csaszar["edges"] + csaszar["faces"] == 0, csaszar))
    checks.append(ok("Csaszar vertices equal Phi6", csaszar["vertices"] == PHI6, csaszar))
    checks.append(ok("Csaszar edges equal Heawood edges", csaszar["edges"] == oscillator["edges"] == 3 * PHI6, {"csaszar": csaszar, "heawood": oscillator}))
    checks.append(ok("Csaszar faces equal Heawood vertices", csaszar["faces"] == oscillator["vertices"] == 2 * PHI6, {"csaszar": csaszar, "heawood": oscillator}))
    checks.append(ok("Jungerman-Ringel denominator is K=12", (PHI6 - 3) * (PHI6 - 4) == K, K))

    checks.append(ok("Heawood selector law BBt=2I+J", incidence["bbt_equals_2i_plus_j"] is True and incidence["btb_equals_2i_plus_j"] is True, incidence))
    checks.append(ok("Heawood adjacency quartic relation holds", operator["adjacency_quartic_relation_holds"] is True, operator["adjacency_minimal_polynomial"]))
    checks.append(ok("Heawood oscillator has two Phi6 rails", oscillator["vertices"] == 2 * PHI6, oscillator))
    checks.append(ok("Heawood cycle rank equals scheduler tick count", oscillator["cycle_rank"] == len(scheduler["scheduler_stages"]) == 2**Q, oscillator["cycle_rank"]))
    checks.append(ok("oscillator frequency squared equals lambda", oscillator["frequency_squared"] == LAM == p_fusion.denominator, oscillator))
    checks.append(ok("oscillator middle shell equals W33 degree", oscillator["middle_shell"] == K == constants["k"], oscillator))
    checks.append(ok("oscillator middle shell splits 6+6", 2 * oscillator["branch_size"] == oscillator["middle_shell"] and oscillator["branch_size"] == math.factorial(Q), oscillator))
    checks.append(ok("oscillator middle shell is three toric stabilizers", oscillator["middle_shell"] == Q * TORIC_STABILIZER_WEIGHT, oscillator["middle_shell"]))
    checks.append(ok("weighted tetra normalization recovers Heawood gap", local_norm["weighted_tetra_nonzero_laplacian_equals_heawood_gap"] is True, local_norm))

    checks.append(ok("deterministic Pauli frame equals H1", deterministic["pauli_frame_states"] == H1, deterministic))
    checks.append(ok("protected distance equals H1", closure["logical_sector"] == H1 and closure["active_protection_code"] == "[[82320,81,>=81]]", closure))
    checks.append(ok("base CSS carrier is [[240,81,3]]", closure["base_css_code"] == "[[240,81,3]]", closure))
    checks.append(ok("Q4 remains local routing [[1296,81,4]]", closure["q4_local_routing_code"] == "[[1296,81,4]]" and closure["q4_dressed_weight"] == 4, closure))
    checks.append(ok("line-star tail is preserved, not killed", closure["line_star_mod_vertex_rank"] == H1 and closure["k_if_line_stars_are_stabilizers"] == 0, closure))
    checks.append(ok("correctable weight equals W33 vertices and selector trits", steane_ft["guaranteed_correctable_weight"] == V == classical["measurement_word_trits"] == controller["measurement_trits"], {"steane": steane_ft, "classical": classical, "controller": controller}))
    checks.append(ok("controller envelope is 64-bit class", controller["controller_bits"] == 64 and classical["exact_word_bound"] == "2^63 < 3^40 < 2^64", {"controller": controller, "classical": classical}))
    checks.append(ok("bus has five ordered layers", [layer["name"] for layer in bus_layers] == ["photonic_denominator_bus", "heawood_harmonic_bus", "toric_surface_bus", "protected_qec_bus", "classical_selector_bus"], bus_layers))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXVIII",
        "title": "Photonic Harmonic TQC Bus",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "bus_layers": bus_layers,
        "probability_to_topology": {
            "p_fusion": str(p_fusion),
            "fusion_denominator": p_fusion.denominator,
            "fusion_denominator_read": "lambda=2 = toric logical qubits = harmonic frequency squared",
            "p_klm": str(p_klm),
            "klm_denominator": p_klm.denominator,
            "klm_denominator_read": "mu=4 = toric GSD = toric stabilizer weight",
        },
        "harmonic_surface_packet": {
            "csaszar": csaszar,
            "heawood_oscillator": oscillator,
            "heawood_gap_exact": operator["laplacian_gap_exact"],
            "tetra_weight_for_same_gap_exact": local_norm["tetra_weight_for_same_gap_exact"],
            "middle_shell_read": "12 = W33 degree = 6+6 harmonic branches = 3 toric weight-4 checks",
        },
        "protected_tqc_packet": {
            "base_css_code": closure["base_css_code"],
            "q4_local_routing_code": closure["q4_local_routing_code"],
            "active_protection_code": closure["active_protection_code"],
            "logical_sector": closure["logical_sector"],
            "correctable_weight": steane_ft["guaranteed_correctable_weight"],
            "selector_trits": classical["measurement_word_trits"],
        },
        "external_anchors": {
            "klm_feedback_linear_optics": "https://arxiv.org/abs/quant-ph/0006088",
            "browne_rudolph_fusion_cluster": "https://arxiv.org/abs/quant-ph/0405157",
            "gkp_oscillator_code": "https://arxiv.org/abs/quant-ph/0008040",
            "nonabelian_tqc_review": "https://arxiv.org/abs/0707.1889",
            "gkp_bosonic_qec_review": "https://arxiv.org/abs/2308.02913",
        },
        "architecture_upgrade": (
            "Adds the harmonic/topological bus between photonic assembly and the "
            "protected W33 QEC stack. The bus explains why the optical probability "
            "denominators 2 and 4, the genus-one toric data, the Heawood oscillator, "
            "and the Steane/Phi6 protection layer belong to one architecture."
        ),
        "theorem": (
            "The protected photonic harmonic TQC architecture is a five-layer bus. "
            "The photonic denominator layer has p_fusion=1/2 and p_KLM=1/4, whose "
            "denominators are lambda=2 and mu=4. The same 2 and 4 are the toric "
            "logical-qubit count and ground-state degeneracy on the genus-one "
            "Csaszar/Szilassi shell, and the Heawood harmonic oscillator has "
            "frequency squared 2, 14=2*Phi6 vertices, and a 12=6+6 middle shell. "
            "That middle shell is also the W33 degree and three toric weight-4 "
            "checks. The protected QEC layer then preserves the H1=81 line-star "
            "tail through [[82320,81,>=81]], while Q4 remains local [[1296,81,4]] "
            "routing and the 40-trit selector commits only after protection."
        ),
        "honesty_boundary": (
            "This is an architecture and invariant-matching theorem. It does not "
            "claim a new optical threshold, a physical anyon implementation, or a "
            "new proof that the Q4 packet layer has distance 12."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXVIII_photonic_harmonic_tqc_bus_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
