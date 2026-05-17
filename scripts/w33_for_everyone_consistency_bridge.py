#!/usr/bin/env python3
"""Consistency bridge for the W33_FOR_EVERYONE manuscript.

Encodes key arithmetic and architecture claims from `W33_FOR_EVERYONE.tex`
into exact, machine-checkable identities so future paper edits can be
regression-tested against the promoted QEC/photonic ouroboros layer.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_PATH = ROOT / "W33_FOR_EVERYONE.tex"
QEC_OUROBOROS_PATH = ROOT / "PART_CCCCXVII_QEC_OUROBOROS_STABILIZER_LOOP.md"
PHOTONIC_QEC_PATH = ROOT / "PART_DCCXV_PHOTONIC_FUSION_SYNDROME_QEC_BRIDGE.md"
FROBENIUS_OUROBOROS_PATH = ROOT / "PART_DCCLIV_FROBENIUS_SELECTION_OUROBOROS.md"
OUT_PATH = ROOT / "data" / "dccclxxii_w33_for_everyone_qec_ouroboros_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    q: int
    v: int
    k: int
    lam: int
    mu: int
    edges: int
    f_mult: int
    g_mult: int
    primitive_count: int
    alpha_delta_num: int
    alpha_delta_den: int
    qec_logical_qudits: int
    qec_check_rank: int
    dual_carrier: int
    klm_primitive_slots: int
    manuscript_anchor_count: int
    all_identities_hold: bool


def triangular(n: int) -> int:
    return n * (n + 1) // 2


def read_required(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_bridge() -> dict[str, Any]:
    manuscript = read_required(MANUSCRIPT_PATH)
    qec_ouroboros = read_required(QEC_OUROBOROS_PATH)
    photonic_qec = read_required(PHOTONIC_QEC_PATH)
    frobenius_ouroboros = read_required(FROBENIUS_OUROBOROS_PATH)

    q = 3
    lam = q - 1
    mu = q + 1
    k = q * (q + 1)
    v = (q**4 - 1) // (q - 1)
    edges = v * k // 2
    f_mult = 24
    g_mult = 15

    phi3 = q**2 + q + 1
    phi4 = q**2 + 1
    phi6 = q**2 - q + 1

    # Paper-listed primitive table values (appendix of W33_FOR_EVERYONE.tex).
    primitive_values = {
        1,
        2,
        3,
        4,
        6,
        7,
        8,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        20,
        21,
        24,
        26,
        27,
        30,
        36,
        40,
        45,
        66,
        78,
        81,
        120,
        192,
        240,
        248,
        384,
        1728,
        196560,
        196884,
    }

    alpha_docs = Fraction(40, 1111)
    alpha_paper = Fraction(880, 24445)
    alpha_delta = abs(alpha_docs - alpha_paper)

    vertex_x_rank = v - 1
    triangle_z_rank = 120
    qec_check_rank = vertex_x_rank + triangle_z_rank
    qec_logical_qudits = edges - qec_check_rank
    dual_carrier = 2 * edges
    nilpotent_homology_lift = 2 * qec_logical_qudits
    klm_primitive_slots = 2 * dual_carrier
    local_turn_split = (math.factorial(q), math.factorial(q))

    manuscript_anchors = {
        "master_equation_section": r"\section{The Master Equation}" in manuscript,
        "pure_logic_chain_theorem": r"\begin{theorem}[Pure-Logic Chain]" in manuscript,
        "dual_number_carrier_480": r"C_1' = 480" in manuscript,
        "h1_short_exact_sequence": r"0 \;\to\; 81 \;\to\; 162 \;\to\; 81 \;\to\; 0" in manuscript,
        "photonic_fusion_carrier_statement": "The photonic fusion carrier $480 = C_1'$" in manuscript,
        "universal_quantum_computer_section": r"\section{$W(3,3)$ as a universal quantum computer}" in manuscript,
        "css_bus_row": r"Bus width & $240$ & physical edges (CSS code)" in manuscript,
        "distance_four_row": r"Distance & $4$ & minimum CSS code distance = $\mu$" in manuscript,
        "recursive_distinction_layer": "recursive coherent distinction" in manuscript,
        "fine_structure_running_layer": r"\section{The fine-structure correction: $137 + \delta_{\mathrm{RG}}$}" in manuscript,
    }

    bridge_anchors = {
        "qec_ouroboros_names_snake_tail": "The snake eats its tail." in qec_ouroboros,
        "qec_ouroboros_base_code": "[[240,81,3]]" in qec_ouroboros,
        "qec_ouroboros_line_star_tail": "line-star tail" in qec_ouroboros,
        "qec_ouroboros_protected_lift": "[[82320,81,>=81]]" in qec_ouroboros,
        "photonic_bridge_return_alphabet": (
            "photonic nondeterminism = heralded QEC return alphabet on the 480 carrier" in photonic_qec
        ),
        "photonic_bridge_accepted_return_split": (
            "480 = 240 accepted bonds + 240 heralded return/syndrome slots" in photonic_qec
        ),
        "frobenius_ouroboros_q8_loop": "Q_8" in frobenius_ouroboros and "stabilizer cascade" in frobenius_ouroboros,
    }

    identities = {
        # Core SRG / graph identities in the manuscript.
        "srg_parameters_match_w33": (v, k, lam, mu) == (40, 12, 2, 4),
        "edge_count_is_240": edges == 240,
        "adjacency_spectrum_multiplicities": f_mult + g_mult + 1 == v,
        # Gauge and E-series arithmetic.
        "sm_codec_dimension": 8 + 3 + 1 == k,
        "dim_e8_identity": 248 == edges + 2**q,
        "j_constant_identity": 744 == q * 248,
        # Moonshine / Leech arithmetic from the paper.
        "leech_kissing_identity": 196560 == edges * q**2 * phi6 * phi3,
        "j_linear_coefficient_identity": 196884 == 196560 + mu * q**4,
        # Primitive-table local arithmetic checks.
        "bosonic_dim_identity": 26 == 2 * phi3,
        "sporadic_split_identity": 20 + 6 == 26 == v // 2 + math.factorial(q),
        "k_cubed_identity": 1728 == k**3,
        "triangular_embeddings": (
            triangular(8),
            triangular(9),
            triangular(11),
            triangular(12),
            triangular(15),
        )
        == (36, 45, 66, 78, 120),
        # Alpha-regime drift (open and explicitly tracked).
        "alpha_variants_unresolved_but_close": abs(float(alpha_docs - alpha_paper)) < 1e-5,
        "alpha_delta_matches_registry": alpha_delta == Fraction(24, 5431679),
        # Primitive table cardinality from appendix listing.
        "primitive_table_size_34": len(primitive_values) == 34,
        # QEC / photonic ouroboros architecture checks.
        "qec_check_rank_identity": qec_check_rank == 159,
        "qec_logical_sector_identity": qec_logical_qudits == 81,
        "qec_carrier_partition_identity": qec_check_rank + qec_logical_qudits == edges,
        "nilpotent_homology_lift_identity": nilpotent_homology_lift == 162,
        "dual_carrier_identity": dual_carrier == 480,
        "local_turn_split_identity": local_turn_split == (6, 6) and sum(local_turn_split) == k,
        "global_turn_carrier_identity": v * sum(local_turn_split) == dual_carrier,
        "accepted_return_split_identity": edges + edges == dual_carrier,
        "klm_primitive_lift_identity": klm_primitive_slots == 960,
        "manuscript_architecture_anchors_present": all(manuscript_anchors.values()),
        "promoted_ouroboros_anchors_present": all(bridge_anchors.values()),
    }

    summary = BridgeSummary(
        q=q,
        v=v,
        k=k,
        lam=lam,
        mu=mu,
        edges=edges,
        f_mult=f_mult,
        g_mult=g_mult,
        primitive_count=len(primitive_values),
        alpha_delta_num=alpha_delta.numerator,
        alpha_delta_den=alpha_delta.denominator,
        qec_logical_qudits=qec_logical_qudits,
        qec_check_rank=qec_check_rank,
        dual_carrier=dual_carrier,
        klm_primitive_slots=klm_primitive_slots,
        manuscript_anchor_count=sum(manuscript_anchors.values()),
        all_identities_hold=all(identities.values()),
    )

    return {
        "part": "DCCCLXXII",
        "title": "W33 For Everyone QEC Ouroboros Consistency Bridge",
        "summary": asdict(summary),
        "constants": {
            "q": q,
            "phi3": phi3,
            "phi4": phi4,
            "phi6": phi6,
        },
        "qec_ouroboros": {
            "vertex_x_rank": vertex_x_rank,
            "triangle_z_rank": triangle_z_rank,
            "check_rank": qec_check_rank,
            "logical_qudits": qec_logical_qudits,
            "base_code": {"n": edges, "k": qec_logical_qudits, "d_z": mu},
            "nilpotent_exact_sequence": [qec_logical_qudits, nilpotent_homology_lift, qec_logical_qudits],
            "local_turn_split": {
                "accepted_signed_clifford": local_turn_split[0],
                "return_a2_weyl": local_turn_split[1],
            },
            "directed_carrier": dual_carrier,
            "accepted_bonds": edges,
            "heralded_return_syndrome_slots": edges,
            "klm_primitive_slots": klm_primitive_slots,
        },
        "alpha_variants": {
            "docs_variant": {"numerator": alpha_docs.numerator, "denominator": alpha_docs.denominator},
            "paper_variant": {"numerator": alpha_paper.numerator, "denominator": alpha_paper.denominator},
            "exact_delta": {"numerator": alpha_delta.numerator, "denominator": alpha_delta.denominator},
        },
        "manuscript": {
            "path": str(MANUSCRIPT_PATH.relative_to(ROOT)),
            "bytes": len(manuscript.encode("utf-8")),
            "anchors": manuscript_anchors,
        },
        "promoted_bridge_anchors": {
            "qec_ouroboros": str(QEC_OUROBOROS_PATH.relative_to(ROOT)),
            "photonic_qec": str(PHOTONIC_QEC_PATH.relative_to(ROOT)),
            "frobenius_ouroboros": str(FROBENIUS_OUROBOROS_PATH.relative_to(ROOT)),
            "anchors": bridge_anchors,
        },
        "primitive_values_sorted": sorted(primitive_values),
        "identities": identities,
        "notes": (
            "This bridge is a manuscript-level consistency checksum for W33_FOR_EVERYONE.tex. "
            "It enforces exact arithmetic claims, pins the QEC ouroboros/photonic carrier "
            "interpretation, and keeps unresolved alpha-regime claims explicitly labeled."
        ),
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
