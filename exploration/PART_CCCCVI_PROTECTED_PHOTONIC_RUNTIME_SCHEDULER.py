#!/usr/bin/env python3
"""PART CCCCVI -- Protected Photonic Runtime Scheduler.

CCCXCVI separated the photonic TOE runtime into probabilistic, deterministic,
quantum, and classical layers.  CCCCIV/CCCCV protected the finite kernel.  This
part closes the compiler gap between those statements: it gives an executable
stage contract for how a photonic event becomes a protected logical operation and
then a classical selector record.

The scheduler is deliberately finite.  It proves a handoff architecture, not a
device threshold or a biological-origin theorem.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]

Q = 3
LAM = Q - 1
MU = Q + 1
K = Q * (Q + 1)
V = (Q**4 - 1) // (Q - 1)
E = V * K // 2
DIRECTED = 2 * E
TRIANGLE_TRACE = 4 * E
H1 = Q**4
PHI6 = Q * Q - Q + 1
PROJECTIVE_FRAMES = (H1 - 1) // (Q - 1)
CARTAN_RANK = 2**Q

PHOTONIC = ROOT / "PART_CCCXCVI_photonic_life_runtime_architecture_results.json"
CSS_TOPO = ROOT / "PART_CCCCII_w33_css_topological_code_results.json"
CSS_DISTANCE = ROOT / "PART_CCCCIII_w33_css_distance_results.json"
DISTANCE_AMP = ROOT / "PART_CCCCIV_w33_distance_amplification_results.json"
CSS_LIFT = ROOT / "PART_CCCCIV_w33_css_steane_lift_results.json"
KERNEL = ROOT / "PART_CCCCV_protected_toe_kernel_results.json"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def ceil_log2_int(value: int) -> int:
    if value <= 0:
        raise ValueError("ceil_log2_int expects a positive integer")
    return (value - 1).bit_length()


def steane_level(candidates: Dict[str, Any], level: int) -> Dict[str, Any]:
    tower = candidates.get("steane_css_tower")
    if isinstance(tower, dict):
        return tower[str(level)]
    return candidates[f"steane_css_level_{level}"]


@dataclass(frozen=True)
class SchedulerStage:
    tick: int
    name: str
    regime: str
    input_contract: str
    output_contract: str
    exact_invariant: str
    failure_mode: str


def scheduler_stages() -> List[SchedulerStage]:
    return [
        SchedulerStage(
            0,
            "projective_carrier",
            "quantum",
            "single-photon qutrit modes",
            "40 W33 projective Pauli sites",
            "3^4=81 nonzero Pauli states project to 40 sites",
            "loss/decoherence before graph assembly",
        ),
        SchedulerStage(
            1,
            "heralded_fusion_assembly",
            "probabilistic",
            "240 target graph edges",
            "240 accepted entangling bonds",
            "p_fusion=1/2 gives 480 expected fusion attempts",
            "failed fusions are heralded and retried before logical measurement",
        ),
        SchedulerStage(
            2,
            "klm_primitive_budget",
            "probabilistic",
            "linear-optical CZ primitives",
            "primitive budget for the same 240 bonds",
            "p_KLM=1/4 gives 960 primitive attempts",
            "non-heralded primitive drift is outside this finite scheduler",
        ),
        SchedulerStage(
            3,
            "css_resource_validation",
            "quantum_error_correction",
            "W33 edge-qubit resource",
            "valid [[240,81,3]] CSS core",
            "39 X-rank + 120 Z-rank + 81 logical = 240",
            "bare distance remains only 3 until the protection lift is applied",
        ),
        SchedulerStage(
            4,
            "mbqc_feedforward",
            "deterministic",
            "40 trit detector outcomes",
            "81-state Pauli-frame update",
            "4 frame trits give 3^4=81 deterministic correction states",
            "invalid measurement bases break universality rather than randomness",
        ),
        SchedulerStage(
            5,
            "steane_phi6_protection",
            "quantum_error_correction",
            "[[240,81,3]] CSS core",
            "[[82320,81,>=81]] protected code",
            "three Phi6=7 lifts give distance lower bound 81",
            "more than 40 arbitrary faults exceed the proved correction budget",
        ),
        SchedulerStage(
            6,
            "classical_selector_commit",
            "classical",
            "40 trit measurement word",
            "one 64-bit-class selector record",
            "2^63 < 3^40 < 2^64",
            "classical memory corruption is not modeled as quantum noise",
        ),
        SchedulerStage(
            7,
            "e8_z3_operation_gate",
            "operation",
            "protected H1=81 matter sector",
            "verified E8 Z3 bracket operation",
            "8347 bracket terms checked with zero grade violations",
            "empirical Standard Model/gravity fitting remains outside this gate",
        ),
    ]


def build_results() -> Dict[str, Any]:
    photonic = load_json(PHOTONIC)
    css_topo = load_json(CSS_TOPO)
    css_distance = load_json(CSS_DISTANCE)
    distance_amp = load_json(DISTANCE_AMP)
    css_lift = load_json(CSS_LIFT)
    kernel = load_json(KERNEL)

    topo_params = css_topo["css_parameters"]
    distance_params = css_distance["css_parameters"]
    amp_candidates = distance_amp["exact_amplification_candidates"]
    amp_level_1 = steane_level(amp_candidates, 1)
    amp_level_3 = steane_level(amp_candidates, 3)
    lift_ft = css_lift["fault_tolerance_read"]
    lift_l3 = css_lift["lift_table"][3]
    constants = photonic["constants"]
    e8_audit = photonic["e8_operation_audit"]
    classical = photonic["classical_layer"]
    deterministic = photonic["deterministic_layer"]
    probabilistic = photonic["probabilistic_layer"]
    stages = scheduler_stages()

    measurement_states = Q**V
    controller_bits = ceil_log2_int(measurement_states)
    frame_bits = ceil_log2_int(H1)
    projective_frame_bits = ceil_log2_int(PROJECTIVE_FRAMES)

    checks: List[Dict[str, Any]] = []

    checks.append(ok("photonic runtime artifact verified", photonic["verified"] is True, photonic["checks_passed"]))
    checks.append(ok("protected kernel artifact verified", kernel["verified"] is True, kernel["checks_passed"]))
    checks.append(ok("CSS topology artifact verified", css_topo["verified"] is True, css_topo["checks_passed"]))
    checks.append(ok("CSS distance artifact verified", css_distance["verified"] is True, css_distance["checks_passed"]))
    checks.append(ok("upstream distance amplification artifact verified", distance_amp["verified"] is True, distance_amp["checks_passed"]))
    checks.append(ok("CSS Steane-lift artifact verified", css_lift["verified"] is True, css_lift["checks_passed"]))

    checks.append(ok("scheduler has eight Cartan-rank ticks", len(stages) == CARTAN_RANK == 8, len(stages)))
    checks.append(ok("scheduler ticks are contiguous", [stage.tick for stage in stages] == list(range(CARTAN_RANK)), [stage.tick for stage in stages]))
    checks.append(ok("scheduler includes quantum, probabilistic, deterministic, qec, classical, operation regimes", {"quantum", "probabilistic", "deterministic", "quantum_error_correction", "classical", "operation"} <= {stage.regime for stage in stages}, sorted({stage.regime for stage in stages})))

    checks.append(ok("W33 constants still 40/12/240", (constants["v"], constants["k"], constants["edges"]) == (V, K, E), constants))
    checks.append(ok("projective carrier has 40 sites", PROJECTIVE_FRAMES == V, PROJECTIVE_FRAMES))
    checks.append(ok("two-qutrit Pauli frame has 81 states", deterministic["pauli_frame_states"] == H1, deterministic))
    checks.append(ok("frame bit envelope is 7 bits", frame_bits == PHI6, frame_bits))
    checks.append(ok("projective frame bit envelope is 6 bits", projective_frame_bits == K // LAM, projective_frame_bits))

    checks.append(ok("fusion probability is 1/2", probabilistic["p_fusion"] == "1/2", probabilistic))
    checks.append(ok("KLM primitive probability is 1/4", probabilistic["p_klm"] == "1/4", probabilistic))
    checks.append(ok("fusion attempts equal directed W33 edges", probabilistic["expected_fusion_attempts"] == DIRECTED, probabilistic))
    checks.append(ok("KLM attempts equal triangle trace", probabilistic["expected_klm_attempts"] == TRIANGLE_TRACE, probabilistic))
    checks.append(ok("accepted fusion bonds equal CSS physical edge qubits", E == topo_params["n_physical_edge_qubits"] == distance_params["n"], {"edges": E, "css_n": distance_params["n"]}))

    checks.append(ok("CSS ranks close n = rankX + rankZ + k", topo_params["rank_X_vertex_checks"] + topo_params["rank_Z_triangle_checks"] + topo_params["k_logical_qubits"] == E, topo_params))
    checks.append(ok("CSS core distance is exact low-distance boundary d=3", distance_params["d"] == Q, distance_params))
    checks.append(ok("upstream first Steane amplification is [[1680,81,9]]", amp_level_1["n"] == 1680 and amp_level_1["d"] == 9, amp_level_1))
    checks.append(ok("Steane/Phi6 lift produces protected code", lift_ft["three_lift_code"] == "[[82320,81,>=81]]", lift_ft))
    checks.append(ok("local three-lift protection matches upstream tower level 3", amp_level_3["n"] == lift_l3["n"] and amp_level_3["d"] == lift_l3["distance_lower_bound"], {"upstream_level_3": amp_level_3, "local_lift": lift_l3}))
    checks.append(ok("protected physical qubits = 240*7^3", lift_l3["n"] == E * PHI6**3 == 82320, lift_l3))
    checks.append(ok("protected distance lower bound equals H1", lift_l3["distance_lower_bound"] == H1, lift_l3))
    checks.append(ok("protected correctable weight equals measurement trits", lift_ft["guaranteed_correctable_weight"] == classical["measurement_word_trits"] == V, {"correctable": lift_ft["guaranteed_correctable_weight"], "trits": classical["measurement_word_trits"]}))

    checks.append(ok("classical measurement word needs exactly 64 bits", controller_bits == 64 and 2**63 < measurement_states < 2**64, {"bits": controller_bits, "bound": "2^63 < 3^40 < 2^64"}))
    checks.append(ok("classical record states exceed signed 64-bit positive range", measurement_states > 2**63, measurement_states.bit_length()))
    checks.append(ok("classical record states fit unsigned 64-bit range", measurement_states < 2**64, measurement_states.bit_length()))

    checks.append(ok("H1 logical sector equals protected distance and E8 matter grade", kernel["closure_equalities"]["logical_sector"] == lift_l3["distance_lower_bound"] == e8_audit["h1_free_rank"] == H1, kernel["closure_equalities"]))
    checks.append(ok("E8 Z3 operation gate checked 8347 terms", e8_audit["z3_terms_checked"] == 8347, e8_audit))
    checks.append(ok("E8 Z3 operation gate has zero grade violations", e8_audit["z3_grade_violations"] == 0, e8_audit))
    checks.append(ok("g1 and g2 are both H1-sized matter grades", e8_audit["e8_dims"] == {"g0": 86, "g1": H1, "g2": H1, "total": 248}, e8_audit["e8_dims"]))

    verified = all(check["passed"] for check in checks)

    return {
        "part": "CCCCVI",
        "title": "Protected Photonic Runtime Scheduler",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "scheduler_stages": [asdict(stage) for stage in stages],
        "controller_envelope": {
            "measurement_trits": V,
            "measurement_states": str(measurement_states),
            "controller_bits": controller_bits,
            "pauli_frame_states": H1,
            "pauli_frame_bits": frame_bits,
            "projective_frame_states": PROJECTIVE_FRAMES,
            "projective_frame_bits": projective_frame_bits,
        },
        "handoff_contract": {
            "probabilistic_to_quantum": "retry heralded fusion/KLM primitives until the 240 W33 bonds are accepted",
            "quantum_to_deterministic": "MBQC measurements update the 81-state Pauli frame instead of randomizing the logical operation",
            "deterministic_to_protected": "the upstream first Steane amplification [[1680,81,9]] continues to the local level-3 protected code [[82320,81,>=81]], correcting 40 faults",
            "protected_to_classical": "the full W33 measurement record is a single 64-bit-class classical selector word",
            "protected_to_operation": "the protected H1=81 logical sector feeds the verified E8 Z3 operation gate",
        },
        "external_sources": {
            "klm_linear_optics": "https://www.nature.com/articles/35051009",
            "one_way_mbqc": "https://arxiv.org/abs/quant-ph/0108067",
            "fusion_linear_optics": "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.95.010501",
            "fault_tolerant_cluster": "https://arxiv.org/abs/quant-ph/0510135",
            "steane_qec": "https://arxiv.org/abs/quant-ph/9601029",
            "css_codes": "https://arxiv.org/abs/quant-ph/9512032",
        },
        "architecture_upgrade": (
            "Turns the protected finite kernel into an executable runtime schedule: "
            "heralded probabilistic assembly, CSS validation, deterministic MBQC "
            "feed-forward, Steane/Phi6 protection, classical selector commit, and "
            "E8 Z3 operation gate."
        ),
        "theorem": (
            "The protected W33 photonic runtime admits an eight-tick scheduler. "
            "The probabilistic layer retries p_fusion=1/2 and p_KLM=1/4 primitives "
            "until 240 W33 bonds are accepted, with expected attempt counts 480 and "
            "960. The deterministic layer maps 40 trit outcomes into an 81-state "
            "Pauli frame. The protected layer lifts [[240,81,3]] to "
            "[[82320,81,>=81]], making the distance lower bound 81 and the "
            "correctable weight 40. The classical layer commits the 40-trit record "
            "inside a 64-bit envelope, and the operation layer feeds the H1=81 "
            "sector into the verified E8 Z3 gate."
        ),
        "honesty_boundary": (
            "This scheduler proves the finite handoff contract between runtime "
            "layers. It does not simulate optical loss thresholds, detector dark "
            "counts, adaptive latency, or empirical Standard Model/gravity fits."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCVI_protected_photonic_runtime_scheduler_results.json"
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
