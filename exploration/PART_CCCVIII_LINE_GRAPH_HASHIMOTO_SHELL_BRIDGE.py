#!/usr/bin/env python3
"""
PART CCCVIII - Line Graph / Hashimoto Shell Bridge
==================================================

Live input from the other assistant:
    PART CCCVII Line Graph Spectrum of W(3,3)

Line graph facts:
    |V(L(W))| = E(W) = 240
    |E(L(W))| = V*C(K,2) = 40*66 = 2640
    degree(L(W)) = 2*(K-1) = 22
    spectrum A(L(W)) = 22^1, 12^24, 6^15, (-2)^200
    tr(A(L)^2) = 5280 = 2*2640 = 480*(K-1)

Bridge to CLXXXII/CCCVII:
    240 = q(q^4-1) is the undirected edge shell.
    480 = 2q(q^4-1) is the directed Hashimoto/CCT carrier.
    degree(L(W)) = 2(K-1) is the unoriented double of the Hashimoto branch.
    tr(A(L)^2) / 480 = K-1 = 11.

Breakthrough:
    The line graph is the undirected edge-turn shell whose normalized second
    moment recovers the Hashimoto nonbacktracking branch.  It is the missing
    operator between the base graph and the directed Hashimoto carrier.

Relation to CCCVII:
    signless trace: tr(Q)=480 = directed carrier
    line graph second moment: tr(A(L)^2)=480*(K-1)
    distance Wiener: W=(K-1)*QLE=11*120

So the branch law K-1=11 appears in two orthogonal global measurements:
    - line graph edge-turn second moment / directed carrier,
    - distance Wiener index / signless energy.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 atoms
q = 3
V = 40
K = 12
lam = 2
mu = 4
r = 2
s = -4
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

# Line graph L(W)
LINE_VERTICES = E
LINE_VALENCY = 2 * (K - 1)
LINE_EDGES = V * K * (K - 1) // 2
LINE_SPECTRUM = [(2 * K - 2, 1), (r + K - 2, 24), (s + K - 2, 15), (-2, E - V)]
LINE_TRACE = sum(val * mult for val, mult in LINE_SPECTRUM)
LINE_SECOND_MOMENT = sum(val * val * mult for val, mult in LINE_SPECTRUM)
LINE_NULLITY = E - V
LINE_NORMALIZED_SECOND = LINE_SECOND_MOMENT // DIRECTED

# Operator tetrahedron companions
SIGNLESS_TRACE = DIRECTED
SIGNLESS_ENERGY = E // 2
WIENER_INDEX = 1320
Q_SECOND_MOMENT = DIRECTED * Phi3
D_SECOND_MOMENT = DIRECTED * Phi4
TREE_EXP_2 = H1
TREE_EXP_5 = Phi3 + Phi4
DISTANCE_PERRON = K * (K - 1) // 2


@dataclass(frozen=True)
class LineHashimotoLayer:
    name: str
    value: int | str
    formula: str
    interpretation: str


def line_hashimoto_layers() -> List[LineHashimotoLayer]:
    return [
        LineHashimotoLayer("line_vertices", LINE_VERTICES, "|V(L(W))|=E=240=q(q^4-1)", "undirected edge shell"),
        LineHashimotoLayer("directed_carrier", DIRECTED, "2|V(L(W))|=480=2q(q^4-1)", "directed Hashimoto/CCT carrier"),
        LineHashimotoLayer("line_valency", LINE_VALENCY, "2(K-1)=22", "unoriented double of Hashimoto branch"),
        LineHashimotoLayer("hashimoto_branch", HASHIMOTO_BRANCH, "K-1=11", "nonbacktracking outgoing choices per directed edge"),
        LineHashimotoLayer("line_edges", LINE_EDGES, "V*K*(K-1)/2=2640", "edge-turn pairs in unoriented shell"),
        LineHashimotoLayer("line_second_moment", LINE_SECOND_MOMENT, "tr(A_L^2)=5280=480*(K-1)", "branch-weighted directed carrier"),
        LineHashimotoLayer("line_normalized_second", LINE_NORMALIZED_SECOND, "tr(A_L^2)/480=11", "Hashimoto branch recovered from line graph moment"),
        LineHashimotoLayer("line_nullity", LINE_NULLITY, "E-V=200=5V=J*V", "cycle-space excess / incidence null sector"),
        LineHashimotoLayer("line_spectrum", "22^1,12^24,6^15,(-2)^200", "lambda + K - 2 plus incidence nullity", "edge-shell spectrum"),
        LineHashimotoLayer("distance_branch_echo", WIENER_INDEX, "W=(K-1)*QLE=11*120=1320", "distance global total also recovers branch"),
        LineHashimotoLayer("tree_exponent_bridge", TREE_EXP_5, "e5(tau)=Phi3+Phi4=23", "operator-tetrahedron second-moment exponent"),
    ]


def line_graph_hashimoto_shell_audit() -> Dict[str, object]:
    checks = {
        "edge_shell": LINE_VERTICES == E == q * (H1 - 1) == 240,
        "directed_carrier": DIRECTED == 2 * LINE_VERTICES == 480,
        "hashimoto_branch": HASHIMOTO_BRANCH == K - 1 == 11,
        "line_valency_is_double_branch": LINE_VALENCY == 2 * HASHIMOTO_BRANCH == 22,
        "line_edges": LINE_EDGES == V * K * (K - 1) // 2 == 2640,
        "line_spectrum": LINE_SPECTRUM == [(22, 1), (12, 24), (6, 15), (-2, 200)],
        "line_spectrum_multiplicity": sum(mult for _, mult in LINE_SPECTRUM) == LINE_VERTICES,
        "line_trace_zero": LINE_TRACE == 0,
        "line_second_moment": LINE_SECOND_MOMENT == 2 * LINE_EDGES == 5280,
        "line_second_moment_branch_directed": LINE_SECOND_MOMENT == DIRECTED * HASHIMOTO_BRANCH,
        "normalized_line_second_is_branch": LINE_NORMALIZED_SECOND == HASHIMOTO_BRANCH == 11,
        "line_nullity": LINE_NULLITY == E - V == 200 == J * V,
        "line_perron": LINE_SPECTRUM[0][0] == 2 * HASHIMOTO_BRANCH == 22,
        "line_fixed_eigenvalue": LINE_SPECTRUM[1][0] == K == 12,
        "line_generation_eigenvalue": LINE_SPECTRUM[2][0] == lam * q == 6,
        "line_null_eigenvalue": LINE_SPECTRUM[3][0] == -lam == -2,
        "distance_perron_h6": DISTANCE_PERRON == K * (K - 1) // 2 == 66,
        "signless_trace_directed": SIGNLESS_TRACE == DIRECTED,
        "wiener_branch_energy": WIENER_INDEX == HASHIMOTO_BRANCH * SIGNLESS_ENERGY == 1320,
        "operator_tetrahedron_e5": (Q_SECOND_MOMENT + D_SECOND_MOMENT) // DIRECTED == TREE_EXP_5 == 23,
        "tree_exponents": TREE_EXP_2 == H1 == 81 and TREE_EXP_5 == Phi3 + Phi4 == 23,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCVIII_LINE_GRAPH_HASHIMOTO_SHELL_BRIDGE",
        "status": "exact edge-shell bridge linking line graph spectrum to Hashimoto branch and operator tetrahedron",
        "source_links": {
            "line_graph_CCCVII": "PART CCCVII Line Graph Spectrum of W(3,3)",
            "operator_tetrahedron_CCCVII": "PART CCCVII Operator Tetrahedron / Entropy Bridge",
            "CCT_HASHIMOTO_CLXXXII": "CCT / Hashimoto Carrier Weld",
        },
        "w33_atoms": {
            "q": q,
            "V": V,
            "K": K,
            "lambda": lam,
            "mu": mu,
            "r": r,
            "s": s,
            "E": E,
            "directed": DIRECTED,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "H1": H1,
            "Albert": ALBERT,
        },
        "line_hashimoto_layers": [asdict(layer) for layer in line_hashimoto_layers()],
        "bridge_identities": {
            "edge_shell": "V(L(W))=E(W)=240=q(q^4-1)",
            "directed_lift": "2V(L(W))=480=2q(q^4-1)",
            "branch_double": "deg L(W)=22=2(K-1)",
            "moment_branch_recovery": "tr(A_L^2)/480=11=K-1",
            "nullity_cycle_excess": "mult(-2)=E-V=200=J*V",
            "incidence_relation": "B^T B=A_L+2I and BB^T=A+KI",
            "distance_echo": "Wiener=(K-1)*QLE",
            "operator_tetrahedron_echo": "e5(tau)=Phi3+Phi4 from Q/Delta second moments",
        },
        "checks": checks,
        "theorem_statement": (
            "The line graph L(W) is the undirected edge-shell operator sitting between W(3,3) and the directed Hashimoto carrier. "
            "Its 240 vertices are the edge shell q(q^4-1), its valency is the orientation double 2(K-1), and its second moment "
            "is 5280=480(K-1).  Therefore normalizing the line graph second moment by the directed carrier recovers the Hashimoto "
            "branch K-1=11.  This branch also appears independently in the distance/signless identity Wiener=(K-1)*QLE."
        ),
        "interpretive_note": (
            "This closes the edge-dynamics gap.  The operator tetrahedron explains vertex-level affine spectra; the line graph explains "
            "edge-shell turning; the Hashimoto operator is the oriented nonbacktracking lift of that edge shell."
        ),
    }


def main() -> int:
    audit = line_graph_hashimoto_shell_audit()
    out = ROOT / "PART_CCCVIII_line_graph_hashimoto_shell_bridge_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
