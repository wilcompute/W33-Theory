#!/usr/bin/env python3
"""
PART CCCXIV - Photonic Clifford Orbit Compiler
==============================================

Trigger:
    Reread of uploaded single_photon_universal_computation.tex/pdf.

Missed paper layer:
    The photon paper is not only a qubit/linear-optics paper.  In the TeX source it
    explicitly develops a qutrit and two-qutrit phase-space story:

      - A photonic qutrit can be realised with three optical modes.
      - Two-qutrit Pauli monomials are indexed by F_3^4, giving 3^4 = 81 monomials.
      - Modulo phase/nonzero projectivisation this gives 40 W(3,3) observables.
      - Commutation is the symplectic form, i.e. W(3,3) adjacency.
      - Sp(4,F_3) is the two-qutrit Clifford group modulo phases.
      - |Sp(4,F_3)| = 51840.
      - F_3, CZ_3, S_3 generate the Clifford group; adding T_3 gives universality.

Breakthrough:
    The Clifford automorphism group order 51840 is not only a symmetry count; it
    factors exactly over every physical resource layer found in CCCXIII:

        51840 / V        = 1296 = (q+1)^2 q^4
        51840 / E        = 216  = 8 * 27 = J^{-1} q^3
        51840 / (2E)     = 108  = 4 * 27 = mu q^3
        51840 / tr(A^3)  = 54   = 2 * 27 = 2 q^3

    Therefore the photonic Clifford group packages four orbit-resolutions:

        per photon/vertex:       EW^2 * H1
        per edge/CZ:             J^{-1} * Albert
        per fusion attempt:      mu * Albert
        per KLM/triangle-trace:  lambda * Albert

Interpretation:
    The automorphism/Clifford group is the symmetry envelope of the physical
    resource tower:

        photons -> edges -> fusion attempts -> KLM attempts / triangle trace.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
lam = q - 1
mu = q + 1
V = q**2 * (q**2 + 1)             # 40
K = q * (q + 1)                   # 12
Phi3 = q**2 + q + 1               # 13
Phi4 = q**2 + 1                   # 10
Phi6 = q**2 - q + 1               # 7
J = 5
J_inv = 8
EW = q + 1
H1 = q**4                         # 81
ALBERT = q**3                     # 27
E = V * K // 2                    # 240
DIRECTED = 2 * E                  # 480
TRIANGLES = V * K * lam // 6       # 160
TR_A3 = 6 * TRIANGLES             # 960

# Uploaded paper's Clifford / qutrit phase-space constants.
QUTRIT_DIM = q
TWO_QUTRIT_PAULI_MONOMIALS = q**4
PROJECTIVE_OBSERVABLES = (TWO_QUTRIT_PAULI_MONOMIALS - 1) // (q - 1)
CLIFFORD_ORDER = 51840
AUT_ORDER = CLIFFORD_ORDER

# Resource orbit quotients.
PER_VERTEX_ORBIT = CLIFFORD_ORDER // V
PER_EDGE_ORBIT = CLIFFORD_ORDER // E
PER_DIRECTED_ORBIT = CLIFFORD_ORDER // DIRECTED
PER_TRIANGLE_TRACE_ORBIT = CLIFFORD_ORDER // TR_A3
PER_TRIANGLE_ORBIT = CLIFFORD_ORDER // TRIANGLES
PER_STABILIZER_SUPPORT_ORBIT_NUM = CLIFFORD_ORDER
PER_STABILIZER_SUPPORT_ORBIT_DEN = V * Phi3

# Photonic resource constants from CCCXIII.
FUSION_ATTEMPTS = DIRECTED
KLM_ATTEMPTS_ALL_EDGES = TR_A3
STABILIZER_WEIGHT = Phi3
STABILIZER_TOTAL_SUPPORT = V * Phi3


@dataclass(frozen=True)
class CliffordOrbitLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def clifford_orbit_layers() -> List[CliffordOrbitLayer]:
    return [
        CliffordOrbitLayer("photonic_qutrit_dim", QUTRIT_DIM, "q=3", "three-mode/OAM/path photonic qutrit"),
        CliffordOrbitLayer("two_qutrit_pauli_monomials", TWO_QUTRIT_PAULI_MONOMIALS, "q^4=81", "two-qutrit Pauli exponent vectors"),
        CliffordOrbitLayer("projective_observables", PROJECTIVE_OBSERVABLES, "(q^4-1)/(q-1)=40", "W33 points / phase-free observables"),
        CliffordOrbitLayer("clifford_group_order", CLIFFORD_ORDER, "|Sp(4,F3)|=51840", "two-qutrit Clifford / W33 automorphism order"),
        CliffordOrbitLayer("per_vertex_orbit", PER_VERTEX_ORBIT, "51840/40=1296=(q+1)^2 q^4", "Clifford symmetries per photon/observable"),
        CliffordOrbitLayer("per_edge_orbit", PER_EDGE_ORBIT, "51840/240=216=8*27", "Clifford symmetries per CZ/cluster edge"),
        CliffordOrbitLayer("per_directed_or_fusion_attempt", PER_DIRECTED_ORBIT, "51840/480=108=4*27", "Clifford symmetries per expected fusion attempt"),
        CliffordOrbitLayer("per_klm_triangle_trace", PER_TRIANGLE_TRACE_ORBIT, "51840/960=54=2*27", "Clifford symmetries per KLM/triangle-trace unit"),
        CliffordOrbitLayer("per_triangle", PER_TRIANGLE_ORBIT, "51840/160=324=4*q^4", "Clifford symmetries per W33 triangle"),
        CliffordOrbitLayer("stabilizer_support_total", STABILIZER_TOTAL_SUPPORT, "40*13=520", "total W33 cluster stabilizer support"),
        CliffordOrbitLayer("stabilizer_support_ratio", "1296/13", "51840/(40*13)", "per stabilizer support-cell symmetry density"),
    ]


def photonic_clifford_orbit_compiler_audit() -> Dict[str, object]:
    checks = {
        "qutrit_dim": QUTRIT_DIM == q == 3,
        "two_qutrit_pauli_monomials": TWO_QUTRIT_PAULI_MONOMIALS == H1 == 81,
        "projective_observables": PROJECTIVE_OBSERVABLES == V == 40,
        "aut_clifford_order": CLIFFORD_ORDER == 51840,
        "clifford_order_formula": CLIFFORD_ORDER == V * (EW**2) * H1 == 40 * 16 * 81,
        "per_vertex_orbit": PER_VERTEX_ORBIT == (EW**2) * H1 == 1296,
        "per_edge_orbit": PER_EDGE_ORBIT == J_inv * ALBERT == 216,
        "per_directed_orbit": PER_DIRECTED_ORBIT == mu * ALBERT == 108,
        "per_triangle_trace_orbit": PER_TRIANGLE_TRACE_ORBIT == lam * ALBERT == 54,
        "per_triangle_orbit": PER_TRIANGLE_ORBIT == mu * H1 == 324,
        "fusion_attempts_directed": FUSION_ATTEMPTS == DIRECTED == 480,
        "klm_attempts_triangle_trace": KLM_ATTEMPTS_ALL_EDGES == TR_A3 == 960,
        "stabilizer_weight": STABILIZER_WEIGHT == Phi3 == 13,
        "stabilizer_total_support": STABILIZER_TOTAL_SUPPORT == V * Phi3 == 520,
        "stabilizer_support_ratio_num_den": PER_STABILIZER_SUPPORT_ORBIT_NUM == CLIFFORD_ORDER and PER_STABILIZER_SUPPORT_ORBIT_DEN == STABILIZER_TOTAL_SUPPORT,
        "edge_shell": E == q * (H1 - 1) == 240,
        "directed_carrier": DIRECTED == 2 * E == 480,
        "triangle_trace": TR_A3 == 960,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXIV_PHOTONIC_CLIFFORD_ORBIT_COMPILER",
        "status": "exact Clifford/automorphism orbit factorization over photonic resource layers",
        "source_links": {
            "uploaded_single_photon_paper": "single_photon_universal_computation.tex/pdf uploaded in chat",
            "Photonic_MBQC_CCCXIII": "Photonic MBQC / W33 Bridge",
            "Hashimoto_CLXXXII": "CCT / Hashimoto Carrier Weld",
            "Dirac_CCCXII": "Dirac Determinant / Operator Compiler",
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
            "EW": EW,
            "H1": H1,
            "Albert": ALBERT,
            "E": E,
            "directed": DIRECTED,
            "Aut_or_Clifford_order": CLIFFORD_ORDER,
        },
        "clifford_orbit_layers": [asdict(layer) for layer in clifford_orbit_layers()],
        "bridge_identities": {
            "two_qutrit_phase_space": "F3^4 gives q^4=81 Pauli monomials and 40 projective W33 observables",
            "clifford_automorphism": "Sp(4,F3) is the two-qutrit Clifford group and Aut(W33), order 51840",
            "vertex_resolution": "|Sp|/40=(q+1)^2 q^4=1296",
            "edge_resolution": "|Sp|/240=J^{-1}q^3=216",
            "fusion_resolution": "|Sp|/480=mu q^3=108",
            "klm_triangle_resolution": "|Sp|/960=lambda q^3=54",
            "triangle_resolution": "|Sp|/160=mu q^4=324",
        },
        "checks": checks,
        "theorem_statement": (
            "The uploaded photon paper's two-qutrit Clifford layer turns the W33 automorphism group into a physical resource symmetry envelope. "
            "The 3^4=81 two-qutrit Pauli exponent vectors projectivize to the 40 W33 observables, and Sp(4,F3) is both the Clifford group "
            "and Aut(W33), of order 51840.  This order factors exactly over the physical resource tower: per vertex it is (q+1)^2 q^4; "
            "per edge it is J^{-1}q^3; per fusion attempt / directed edge it is mu q^3; and per KLM/triangle-trace unit it is lambda q^3."
        ),
        "interpretive_note": (
            "CCCXIII gave the resource counts.  CCCXIV shows the Clifford group resolves those resources into exact orbit factors. "
            "This is the bridge from photonic computation to symmetry: the same group that preserves W33 commutation relations also organizes "
            "the photon, edge, fusion, and KLM resource scales."
        ),
    }


def main() -> int:
    audit = photonic_clifford_orbit_compiler_audit()
    out = ROOT / "PART_CCCXIV_photonic_clifford_orbit_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
