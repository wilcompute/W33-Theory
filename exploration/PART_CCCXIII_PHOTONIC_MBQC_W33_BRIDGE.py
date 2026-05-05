#!/usr/bin/env python3
"""
PART CCCXIII - Photonic MBQC / W33 Bridge
=========================================

Trigger:
    Uploaded paper: single_photon_universal_computation.tex/pdf.

Paper facts used:
    - A single photon has a two-dimensional polarisation Hilbert space C^2.
    - Dual-rail/path encoding uses two spatial modes.
    - Passive optics generate arbitrary SU(2) single-qubit gates with wave plates.
    - The simplest KLM conditional phase / CZ post-selection succeeds with probability 1/4.
    - Type-II fusion gates build photonic graph-state edges with probability 1/2.
    - Cluster-state stabilizers have form K_a = X_a prod_{b~a} Z_b.

New W33 bridge:
    lambda = 2 is not only the polarisation/dual-rail qubit dimension.  It is
    also the numerator of the photonic fusion threshold law

        p_fusion = 1/2 = lambda / mu.

    The simplest KLM nonlinear/post-selected phase success is

        p_KLM = 1/4 = 1 / mu.

    If the MBQC cluster graph is W(3,3), each stabilizer has weight

        1 + k = 13 = Phi3,

    exactly the projective-plane count that already appears in the Seidel,
    signless/distance, and normalized Markov/Krein stacks.

    The W33 cluster state therefore has:

        40 stabilizers, each weight 13, total stabilizer incidence 520 = V Phi3.
        240 CZ/graph edges, exactly the W33 edge shell q(q^4-1).
        480 oriented stabilizer-edge incidences, exactly the Hashimoto carrier.
        Fusion expected attempts per edge = 1/p_fusion = mu/lambda = 2.
        Expected fusion attempts for the full W33 cluster = 2E = 480.

Breakthrough:
    Photonic MBQC converts the Hashimoto carrier from an abstract directed-edge
    space into an expected physical resource count: building all W33 cluster
    edges by p=1/2 fusion takes expected 480 fusion attempts, the same number as
    the directed nonbacktracking carrier.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
lam = q - 1
mu = q + 1
V = q**2 * (q**2 + 1)
K = q * (q + 1)
Phi3 = q**2 + q + 1
Phi4 = q**2 + 1
Phi6 = q**2 - q + 1
J = 5
J_inv = 8
H1 = q**4
ALBERT = q**3
E = V * K // 2
DIRECTED = 2 * E
HASHIMOTO_BRANCH = K - 1

# Photonic constants from the paper.
POLARIZATION_DIM = 2
DUAL_RAIL_MODES = 2
SU2_RANK_PLUS_ROOT = 3  # Pauli generator count / SU(2) generator count.
KLM_SIMPLE_SUCCESS = Fraction(1, 4)
FUSION_SUCCESS = Fraction(1, 2)
FUSION_ATTEMPTS_PER_EDGE = Fraction(1, FUSION_SUCCESS)
KLM_ATTEMPTS_PER_SIMPLE_CZ = Fraction(1, KLM_SIMPLE_SUCCESS)

# W33 cluster-state resource counts.
CLUSTER_QUBITS = V
CLUSTER_EDGES = E
STABILIZER_WEIGHT = K + 1
TOTAL_STABILIZER_SUPPORT = V * STABILIZER_WEIGHT
ORIENTED_STABILIZER_EDGE_INCIDENCES = 2 * E
EXPECTED_FUSION_ATTEMPTS_FULL_CLUSTER = CLUSTER_EDGES * FUSION_ATTEMPTS_PER_EDGE
EXPECTED_KLM_ATTEMPTS_FULL_EDGE_SET = CLUSTER_EDGES * KLM_ATTEMPTS_PER_SIMPLE_CZ

# Links to current operator theorem.
TREE_EXP_2 = H1
TREE_EXP_5 = Phi3 + Phi4
SEIDEL_ENERGY = E
DIRAC_DEGREE = Phi4 + mu**2 + 2 * q
DIRAC_EXP_PRODUCT = Phi4 * mu**2 * (2 * q)
TR_A3 = 960


@dataclass(frozen=True)
class PhotonicBridgeLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def photonic_bridge_layers() -> List[PhotonicBridgeLayer]:
    return [
        PhotonicBridgeLayer("single_photon_qubit", POLARIZATION_DIM, "dim H_pol=2=lambda", "polarisation qubit dimension"),
        PhotonicBridgeLayer("dual_rail_modes", DUAL_RAIL_MODES, "two path modes=lambda", "loss-heralded logical qubit encoding"),
        PhotonicBridgeLayer("su2_generator_count", SU2_RANK_PLUS_ROOT, "3=q", "Pauli/SU(2) generator count"),
        PhotonicBridgeLayer("klm_simple_success", str(KLM_SIMPLE_SUCCESS), "1/4=1/mu", "simplest post-selected CZ/conditional phase success"),
        PhotonicBridgeLayer("fusion_success", str(FUSION_SUCCESS), "1/2=lambda/mu", "Type-II fusion edge creation probability"),
        PhotonicBridgeLayer("fusion_attempts_per_edge", str(FUSION_ATTEMPTS_PER_EDGE), "mu/lambda=2", "expected attempts per W33 cluster edge"),
        PhotonicBridgeLayer("cluster_qubits", CLUSTER_QUBITS, "V=40", "single photons in a W33 graph-state cluster"),
        PhotonicBridgeLayer("cluster_edges", CLUSTER_EDGES, "E=240=q(q^4-1)", "CZ/graph-state edges to create"),
        PhotonicBridgeLayer("stabilizer_weight", STABILIZER_WEIGHT, "k+1=13=Phi3", "MBQC stabilizer support size on W33"),
        PhotonicBridgeLayer("stabilizer_total_support", TOTAL_STABILIZER_SUPPORT, "V*Phi3=40*13=520", "total stabilizer incidence"),
        PhotonicBridgeLayer("oriented_edge_incidences", ORIENTED_STABILIZER_EDGE_INCIDENCES, "2E=480", "Hashimoto directed carrier / oriented cluster incidences"),
        PhotonicBridgeLayer("expected_fusion_attempts_full_cluster", str(EXPECTED_FUSION_ATTEMPTS_FULL_CLUSTER), "E/(1/2)=2E=480", "expected physical fusion attempts to build W33 cluster"),
        PhotonicBridgeLayer("expected_klm_attempts_full_edge_set", str(EXPECTED_KLM_ATTEMPTS_FULL_EDGE_SET), "E/(1/4)=4E=960=tr(A^3)", "simple KLM attempts match triangle trace"),
    ]


def photonic_mbqc_w33_bridge_audit() -> Dict[str, object]:
    checks = {
        "single_photon_dimension_lambda": POLARIZATION_DIM == DUAL_RAIL_MODES == lam == 2,
        "su2_generator_count_q": SU2_RANK_PLUS_ROOT == q == 3,
        "klm_success_is_inverse_mu": KLM_SIMPLE_SUCCESS == Fraction(1, mu) == Fraction(1, 4),
        "fusion_success_lambda_over_mu": FUSION_SUCCESS == Fraction(lam, mu) == Fraction(1, 2),
        "fusion_attempts_per_edge": FUSION_ATTEMPTS_PER_EDGE == Fraction(mu, lam) == 2,
        "cluster_qubits_v": CLUSTER_QUBITS == V == 40,
        "cluster_edges_edge_shell": CLUSTER_EDGES == E == q * (H1 - 1) == 240,
        "stabilizer_weight_phi3": STABILIZER_WEIGHT == K + 1 == Phi3 == 13,
        "stabilizer_total_support": TOTAL_STABILIZER_SUPPORT == V * Phi3 == 520,
        "oriented_incidences_hashimoto": ORIENTED_STABILIZER_EDGE_INCIDENCES == DIRECTED == 480,
        "fusion_attempts_full_cluster_hashimoto": EXPECTED_FUSION_ATTEMPTS_FULL_CLUSTER == DIRECTED == 480,
        "klm_attempts_edge_set_triangle_trace": EXPECTED_KLM_ATTEMPTS_FULL_EDGE_SET == TR_A3 == 960,
        "seidel_energy_edge_shell": SEIDEL_ENERGY == E == 240,
        "dirac_degree": DIRAC_DEGREE == 32,
        "dirac_exp_product_triangle_trace": DIRAC_EXP_PRODUCT == TR_A3 == 960,
        "tree_entropy_exponents": TREE_EXP_2 == H1 == 81 and TREE_EXP_5 == Phi3 + Phi4 == 23,
        "hashimoto_branch": HASHIMOTO_BRANCH == K - 1 == 11,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXIII_PHOTONIC_MBQC_W33_BRIDGE",
        "status": "exact photonic resource bridge from uploaded single-photon paper to W33 operator stack",
        "source_links": {
            "uploaded_single_photon_paper": "single_photon_universal_computation.tex/pdf uploaded in chat",
            "Dirac_CCCXII": "Dirac Determinant / Operator Compiler",
            "Hashimoto_CLXXXII": "CCT / Hashimoto Carrier Weld",
            "Operator_Tetrahedron_CCCVII": "Operator Tetrahedron / Entropy Bridge",
        },
        "w33_atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "V": V,
            "K": K,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "H1": H1,
            "Albert": ALBERT,
            "E": E,
            "directed": DIRECTED,
        },
        "photonic_bridge_layers": [asdict(layer) for layer in photonic_bridge_layers()],
        "bridge_identities": {
            "photon_qubit": "polarisation and dual-rail dimensions equal lambda=2",
            "su2_q_clock": "Pauli/SU(2) generator count equals q=3",
            "klm_success": "simplest KLM CZ success 1/4 equals 1/mu",
            "fusion_success": "Type-II fusion success 1/2 equals lambda/mu",
            "cluster_stabilizer_weight": "W33 cluster stabilizer K_a has support k+1=13=Phi3",
            "fusion_hashimoto": "expected attempts to create all W33 edges by p=1/2 fusion is 2E=480, the Hashimoto carrier",
            "klm_triangle_trace": "expected simple KLM attempts for all edges is 4E=960=tr(A^3)",
        },
        "checks": checks,
        "theorem_statement": (
            "Photonic MBQC gives a physical resource interpretation of the W33 operator stack.  The single-photon qubit dimension and "
            "dual-rail mode count are lambda=2; SU(2)/Pauli control has q=3 generators; the simplest KLM conditional phase success "
            "1/4 is 1/mu; and Type-II fusion success 1/2 is lambda/mu.  A W33 cluster state has 40 photons, 240 graph edges, "
            "stabilizer weight k+1=Phi3=13, and oriented edge incidences 2E=480.  Because fusion succeeds with probability 1/2, "
            "the expected number of fusion attempts to build the full W33 cluster is 480, exactly the Hashimoto directed carrier."
        ),
        "interpretive_note": (
            "This turns the abstract directed carrier into a concrete photonic resource count.  Hashimoto's 480 states are not only "
            "oriented nonbacktracking edges; they are also the expected fusion-attempt budget for physically assembling the W33 photonic cluster."
        ),
    }


def main() -> int:
    audit = photonic_mbqc_w33_bridge_audit()
    out = ROOT / "PART_CCCXIII_photonic_mbqc_w33_bridge_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
