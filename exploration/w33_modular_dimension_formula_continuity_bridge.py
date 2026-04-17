"""Continuity bridge from the modular dimension formula to the live W33 chain.

The modular-dimension formula is classical, but in this repo it is useful only
when it closes onto the existing exact bridges.  This bridge records the three
live welds:

1. Weight 4 is one-dimensional, so every weight-4 modular form is a scalar
   multiple of E_4.  Since theta_{E8} is a weight-4 modular form with leading
   coefficient 1, this forces theta_{E8} = E_4.

2. Weight 12 has dim M_12 = 2 and dim S_12 = 1, so Delta is the unique cusp
   direction.  That is exactly why the two Rankin-Cohen bracket constructions
   land on scalar multiples of Delta.

3. Weight 12 is the first weight where dim M_k exceeds 1, so the holomorphic
   Eisenstein ring first fails to close integrally there; this is the exact
   location of the 691 anomaly.

So the dimension formula is not a detached textbook note.  It is the exact
dimension-theoretic source of the recent E8 theta, Delta, and 691 bridges.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_modular_dimension_formula_continuity_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_eisenstein_closure import (
    eisenstein_ring_closure_ladder,
    verify_691_E12_equals_441_E4cubed_plus_250_E6sq,
    verify_ramanujan_691_congruence,
)
from w33_modular_dimension_formula import dim_M, dim_S, derive_all
from w33_rankin_cohen_tower import verify_rc_E4_E4_2, verify_rc_E4_E6_1
from w33_theta_e8_lattice import verify_theta_E8_equals_E4_predicted


def build_summary() -> dict[str, Any]:
    dims = derive_all()
    theta_e8 = verify_theta_E8_equals_E4_predicted(n_max=4)
    rc22 = verify_rc_E4_E4_2(n_max=20)
    rc11 = verify_rc_E4_E6_1(n_max=20)
    e12 = verify_691_E12_equals_441_E4cubed_plus_250_E6sq(n_max=20)
    congr = verify_ramanujan_691_congruence(n_max=20)
    ladder = eisenstein_ring_closure_ladder()

    return {
        "modular_dimension_continuity_dictionary": {
            "dim_M_4": dim_M(4),
            "dim_M_8": dim_M(8),
            "dim_M_12": dim_M(12),
            "dim_S_12": dim_S(12),
            "first_weight_with_dim_M_ge_2": 12,
            "Delta_weight": 12,
            "W33_valency": 12,
        },
        "upstream_checks": {
            "dimension_formula": dims["summary_chain"],
            "theta_E8_equals_E4": theta_e8["all_match"],
            "rankin_cohen_E4_E4_2": rc22["all_match"],
            "rankin_cohen_E4_E6_1": rc11["all_match"],
            "E12_691_identity": e12["all_match"],
            "ramanujan_691_congruence": congr["all_match"],
            "closure_ladder": ladder,
        },
        "modular_dimension_continuity_theorem": {
            "dim_M4_equals_1_so_theta_E8_equals_E4_is_forced_by_uniqueness_of_weight_4_forms": bool(
                dim_M(4) == 1 and theta_e8["all_match"]
            ),
            "dim_S12_equals_1_so_both_rankin_cohen_weight_12_cusp_brackets_must_be_scalar_multiples_of_Delta": bool(
                dim_S(12) == 1 and rc22["all_match"] and rc11["all_match"]
            ),
            "dim_M12_equals_2_and_is_the_first_nontrivial_weight_where_the_holomorphic_Eisenstein_ring_fails_to_close_integrally": bool(
                dim_M(12) == 2
                and ladder["first_failure_at"] == 12
                and e12["all_match"]
                and congr["all_match"]
            ),
            "the_classical_12_periodic_dimension_formula_closes_exactly_onto_the_repo_E8_Delta_691_chain": bool(
                dims["summary_chain"]["dim_M_closed_form_matches_tabulated"]
                and dims["summary_chain"]["dim_M_is_12_periodic_with_offset_1"]
                and dim_M(4) == 1
                and theta_e8["all_match"]
                and dim_S(12) == 1
                and rc22["all_match"]
                and rc11["all_match"]
                and dim_M(12) == 2
                and e12["all_match"]
                and congr["all_match"]
            ),
        },
        "interpretation": (
            "The modular dimension formula now sits on the live repo chain. "
            "Weight-4 uniqueness forces theta_E8 = E4; weight-12 cusp uniqueness "
            "forces the Rankin-Cohen Delta constructions; and the first jump "
            "dim M_12 = 2 is exactly where the 691 anomaly enters."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MODULAR DIMENSION FORMULA CONTINUITY BRIDGE")
    print("=" * 72)
    for key, value in summary["modular_dimension_continuity_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
