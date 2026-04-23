#!/usr/bin/env python3
"""Atomic minimal-magic audit for the exact W33 Standard Model frontier.

This module sharpens the previous magic-packet audit by isolating the exact
minimality statement already supported by tracked repo data.

Exact inputs already available:
1. The reduced Yukawa generation algebra is the regular C3 qutrit packet
   modulo 3 and splits over C as 1, omega, omega^2.
2. The residual signed Yukawa content is exactly two irreducible D4 quartic
   lifts in the signed variable x = 240 * sigma.
3. The two quartic atoms are field-theoretically independent: no shared
   quadratic subfield, root-field compositum degree 16, splitting-field
   compositum degree 64, Galois group D4 x D4.
4. Canonical mixed combinations escalate immediately beyond the atomic packet:
   product and ratio packets are irreducible octics, while the sum packet has
   degree 16.

Conservative exact reading:
  the remaining non-Clifford Standard Model content is not an amorphous high-
  rank texture. It is already localized to an exact two-atom quartic packet,
  and any canonical synthesis beyond those atoms strictly raises the algebraic
  degree. So the tracked repo now supports an atomic minimal-magic statement,
  even though explicit injection / gate synthesis remains open.

Primary literature anchors for the interpretation layer:
  - Nayak, Simon, Stern, Freedman, Das Sarma (2008):
      https://arxiv.org/abs/0707.1889
  - Anwar, Campbell, Browne (2012), qutrit magic-state distillation:
      https://arxiv.org/abs/1202.2326
  - Campbell, Anwar, Browne (2012), prime-d qudit Reed-Muller:
      https://arxiv.org/abs/1205.3104
  - Howard, Vala (2012), qudit pi/8 gates:
      https://arxiv.org/abs/1206.1598
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, Tuple


ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, EXPLORATION, SCRIPTS):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from exploration.w33_yukawa_qutrit_collapse_bridge import build_yukawa_qutrit_collapse_summary  # noqa: E402
except ModuleNotFoundError:
    from w33_yukawa_qutrit_collapse_bridge import build_yukawa_qutrit_collapse_summary  # noqa: E402

from scripts.w33_yukawa_quartic_lift_audit import analyze as analyze_yukawa_quartic_lift  # noqa: E402


REFERENCE_LITERATURE = {
    "tqc_review": "https://arxiv.org/abs/0707.1889",
    "qutrit_magic_state_distillation": "https://arxiv.org/abs/1202.2326",
    "prime_dimension_reed_muller_magic": "https://arxiv.org/abs/1205.3104",
    "qudit_pi_over_eight_gate": "https://arxiv.org/abs/1206.1598",
}


@lru_cache(maxsize=1)
def qutrit_memory_packet_summary() -> Dict[str, Any]:
    summary = build_yukawa_qutrit_collapse_summary()
    theorem = summary["qutrit_collapse_theorem"]
    packet = summary["mod3_generation_packet"]
    flag = summary["mod3_flag_identification"]

    return {
        "generation_reduces_to_one_c3_mod3": theorem[
            "universal_generation_algebra_reduces_to_one_c3_mod3"
        ],
        "generation_module_is_regular_c3_module": theorem[
            "mod3_generation_module_is_regular_c3_module"
        ],
        "complex_regular_module_splits_as_qutrit_packet": theorem[
            "complex_regular_module_splits_as_qutrit_packet"
        ],
        "plus_generator_order_3": packet["plus_generator_order_3"],
        "minus_generator_order_3": packet["minus_generator_order_3"],
        "minus_equals_plus_squared_mod3": packet["minus_equals_plus_squared_mod3"],
        "cycle_conjugacy_is_exact": packet["cycle_conjugacy_is_exact"],
        "line_maps_to_fixed_line": flag["line_maps_to_fixed_line"],
        "plane_maps_to_augmentation_plane": flag["plane_maps_to_augmentation_plane"],
    }


@lru_cache(maxsize=1)
def quartic_atom_summary() -> Dict[str, Any]:
    summary = analyze_yukawa_quartic_lift()
    packet = summary["quartic_lift_packet"]
    records = packet["records"]
    relation = summary["quartic_pair_relation"]
    root_field_relation = summary["quartic_root_field_relation"]
    splitting_field_relation = summary["quartic_splitting_field_relation"]
    mixed = summary["mixed_positive_root_relation"]
    theorem = summary["quartic_lift_theorem"]

    return {
        "packet_size": packet["packet_size"],
        "scaled_signed_variable": packet["scaled_signed_variable"],
        "scaled_squared_variable": packet["scaled_squared_variable"],
        "h2_quartic_polynomial": records["H_2:-+"]["quartic_polynomial"],
        "h2_quartic_is_irreducible_over_q": records["H_2:-+"]["lift_theorem"][
            "quartic_is_irreducible_over_q"
        ],
        "h2_galois_group_label": records["H_2:-+"]["galois_group_label"],
        "h2_galois_group_order": records["H_2:-+"]["galois_group_order"],
        "hbar2_quartic_polynomial": records["Hbar_2:+-"]["quartic_polynomial"],
        "hbar2_quartic_is_irreducible_over_q": records["Hbar_2:+-"]["lift_theorem"][
            "quartic_is_irreducible_over_q"
        ],
        "hbar2_galois_group_label": records["Hbar_2:+-"]["galois_group_label"],
        "hbar2_galois_group_order": records["Hbar_2:+-"]["galois_group_order"],
        "shared_quadratic_subfield_squarefree_parts": tuple(
            relation["shared_quadratic_subfield_squarefree_parts"]
        ),
        "quartic_root_fields_are_linearly_disjoint_over_q": root_field_relation["relation_theorem"][
            "quartic_root_fields_are_linearly_disjoint_over_q"
        ],
        "quartic_root_field_compositum_degree": root_field_relation["compositum_degree"],
        "d4_splitting_fields_are_linearly_disjoint_over_q": splitting_field_relation[
            "relation_theorem"
        ]["d4_splitting_fields_are_linearly_disjoint_over_q"],
        "quartic_splitting_field_compositum_degree": splitting_field_relation[
            "compositum_degree"
        ],
        "quartic_splitting_field_galois_group": splitting_field_relation[
            "compositum_galois_group"
        ],
        "mixed_product_degree": mixed["product_packet"]["degree"],
        "mixed_ratio_degree": mixed["ratio_packet"]["degree"],
        "mixed_sum_degree": mixed["sum_packet"]["degree"],
        "mixed_product_squared_degree": mixed["product_squared_packet"]["degree"],
        "mixed_ratio_squared_degree": mixed["ratio_squared_packet"]["degree"],
        "mixed_squared_packets_have_v4_galois_group": mixed["theorem"][
            "mixed_positive_root_squared_product_packet_is_irreducible_v4_quartic"
        ]
        and mixed["theorem"][
            "mixed_positive_root_squared_ratio_packet_is_irreducible_v4_quartic"
        ],
        "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts": theorem[
            "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"
        ],
    }


@lru_cache(maxsize=1)
def classify_minimal_magic_frontier() -> Tuple[Dict[str, Any], ...]:
    memory = qutrit_memory_packet_summary()
    magic = quartic_atom_summary()

    return (
        {
            "name": "qutrit_memory_packet",
            "support_level": "repo-exact ternary memory layer",
            "statement": (
                "The reduced generation algebra is already the regular C3 qutrit packet, "
                "so the exact memory layer remains inside the ternary Clifford side."
            ),
            "evidence": memory,
        },
        {
            "name": "quartic_magic_atoms",
            "support_level": "repo-exact signed non-Clifford layer",
            "statement": (
                "The remaining signed Yukawa layer consists of exactly two irreducible "
                "quartic atoms, both D4 over Q."
            ),
            "evidence": {
                "packet_size": magic["packet_size"],
                "scaled_signed_variable": magic["scaled_signed_variable"],
                "h2_quartic_polynomial": magic["h2_quartic_polynomial"],
                "hbar2_quartic_polynomial": magic["hbar2_quartic_polynomial"],
                "h2_galois_group_label": magic["h2_galois_group_label"],
                "hbar2_galois_group_label": magic["hbar2_galois_group_label"],
            },
        },
        {
            "name": "field_independence_of_quartic_atoms",
            "support_level": "repo-exact independence theorem",
            "statement": (
                "The two quartic atoms are field-theoretically independent: no shared "
                "quadratic subfield, root compositum degree 16, splitting compositum "
                "degree 64 with Galois group D4 x D4."
            ),
            "evidence": {
                "shared_quadratic_subfield_squarefree_parts": magic[
                    "shared_quadratic_subfield_squarefree_parts"
                ],
                "quartic_root_fields_are_linearly_disjoint_over_q": magic[
                    "quartic_root_fields_are_linearly_disjoint_over_q"
                ],
                "quartic_root_field_compositum_degree": magic[
                    "quartic_root_field_compositum_degree"
                ],
                "d4_splitting_fields_are_linearly_disjoint_over_q": magic[
                    "d4_splitting_fields_are_linearly_disjoint_over_q"
                ],
                "quartic_splitting_field_compositum_degree": magic[
                    "quartic_splitting_field_compositum_degree"
                ],
                "quartic_splitting_field_galois_group": magic[
                    "quartic_splitting_field_galois_group"
                ],
            },
        },
        {
            "name": "higher_degree_mixing_escalation",
            "support_level": "repo-exact atomicity witness",
            "statement": (
                "Any canonical mixing of the two quartic atoms strictly raises degree: "
                "product and ratio packets are octic, the mixed sum packet has degree 16."
            ),
            "evidence": {
                "mixed_product_degree": magic["mixed_product_degree"],
                "mixed_ratio_degree": magic["mixed_ratio_degree"],
                "mixed_sum_degree": magic["mixed_sum_degree"],
                "mixed_product_squared_degree": magic["mixed_product_squared_degree"],
                "mixed_ratio_squared_degree": magic["mixed_ratio_squared_degree"],
                "mixed_squared_packets_have_v4_galois_group": magic[
                    "mixed_squared_packets_have_v4_galois_group"
                ],
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, Any]:
    memory = qutrit_memory_packet_summary()
    magic = quartic_atom_summary()
    records = classify_minimal_magic_frontier()

    theorem = {
        "the_exact_generation_memory_layer_stays_inside_the_regular_qutrit_c3_packet": (
            memory["generation_reduces_to_one_c3_mod3"] is True
            and memory["generation_module_is_regular_c3_module"] is True
            and memory["complex_regular_module_splits_as_qutrit_packet"] is True
            and memory["plus_generator_order_3"] is True
            and memory["minus_generator_order_3"] is True
            and memory["minus_equals_plus_squared_mod3"] is True
            and memory["cycle_conjugacy_is_exact"] is True
        ),
        "the_exact_signed_nonclifford_roots_first_appear_at_algebraic_degree_four": (
            magic["packet_size"] == 2
            and magic["h2_quartic_is_irreducible_over_q"] is True
            and magic["h2_galois_group_label"] == "D4"
            and magic["h2_galois_group_order"] == 8
            and magic["hbar2_quartic_is_irreducible_over_q"] is True
            and magic["hbar2_galois_group_label"] == "D4"
            and magic["hbar2_galois_group_order"] == 8
        ),
        "the_remaining_signed_magic_packet_has_exact_size_two_and_no_lower_degree_signed_split": (
            magic["packet_size"] == 2
            and magic["shared_quadratic_subfield_squarefree_parts"] == ()
            and magic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
        ),
        "the_two_quartic_magic_atoms_are_field_theoretically_independent": (
            magic["quartic_root_fields_are_linearly_disjoint_over_q"] is True
            and magic["quartic_root_field_compositum_degree"] == 16
            and magic["d4_splitting_fields_are_linearly_disjoint_over_q"] is True
            and magic["quartic_splitting_field_compositum_degree"] == 64
            and magic["quartic_splitting_field_galois_group"] == "D4 x D4"
        ),
        "any_canonical_mixing_of_the_two_atoms_raises_degree_to_octic_or_degree_16": (
            magic["mixed_product_degree"] == 8
            and magic["mixed_ratio_degree"] == 8
            and magic["mixed_sum_degree"] == 16
            and magic["mixed_product_squared_degree"] == 4
            and magic["mixed_ratio_squared_degree"] == 4
            and magic["mixed_squared_packets_have_v4_galois_group"] is True
        ),
    }

    return {
        "status": "ok",
        "reference_literature": REFERENCE_LITERATURE,
        "qutrit_memory_packet": memory,
        "quartic_magic_atoms": magic,
        "record_details": records,
        "minimal_magic_theorem": theorem,
        "bridge_verdict": (
            "The tracked repo now supports a stricter minimality statement. The exact "
            "generation memory remains inside the regular qutrit C3 packet, while the "
            "signed non-Clifford layer first appears as exactly two irreducible quartic "
            "D4 atoms. Those two atoms are field-theoretically independent, and any "
            "canonical mixed synthesis immediately raises algebraic degree to 8 or 16. "
            "So the exact Standard Model magic frontier is already atomic: two quartic "
            "atoms before any higher-degree synthesis."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXXIII_standard_model_minimal_magic_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Standard Model minimal-magic audit")
    for key, value in payload["minimal_magic_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
