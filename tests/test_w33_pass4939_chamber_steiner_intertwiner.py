"""Focused native-GAP regression for the Pass-4939 exact intertwiner."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4939_chamber_steiner_intertwiner.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4939_CHAMBER_STEINER_INTERTWINER.json"
PASS_LINE = "Pass 4939 chamber-Steiner intertwiner: 24/24 checks; status=PASS"

EXPECTED_CHECKS = {
    "all_psp_and_outer_pgsp_equivariance",
    "common_24d_commutant_dimension_1",
    "intertwiner_ranks_24",
    "intertwiners_supported_on_projectors",
    "intrinsic_cover_40_times_3",
    "lift_gram_factors_3_and_4",
    "line_point_carriers_distinguished_in_characteristic_three",
    "no_transverse_component_in_intertwiner",
    "nonzero_maps_not_dimension_numerology",
    "partial_inverse_on_chamber_lane",
    "partial_inverse_on_steiner_lane",
    "point_pencils_40_chambers_160",
    "point_pencils_reconstruct_w33_point_graph",
    "psp_and_full_orders_on_27",
    "qminus_counts_27_36",
    "quotient_group_orders_25920_51840",
    "quotient_is_srg_40_12_2_4",
    "quotient_projectors_exact",
    "quotient_psp_rank_3_subdegrees_1_12_27",
    "quotient_spectral_split_1_24_15",
    "sixers_72_double_sixes_36_steiner_120",
    "steiner_and_chamber_projectors_rank_24",
    "steiner_group_orders_25920_51840",
    "steiner_pair_orbits_exact",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4939.chamber_steiner_intertwiner.v2"
    assert payload["status"] == "PASS"
    assert payload["objects"] == {
        "steiner_triangles": 120,
        "steiner_fibers": 40,
        "fiber_size": 3,
        "quotient_lines": 40,
        "reconstructed_point_pencils": 40,
        "chambers": 160,
        "common_rank": 24,
    }
    assert payload["groups"] == {
        "PSp4_3_order": 25920,
        "PGSp4_3_order": 51840,
        "PSp_subdegrees": [1, 12, 27],
    }
    assert payload["quotient"] == {
        "graph": "Q(4,3) line-intersection graph SRG(40,12,2,4)",
        "Steiner_cover": "120=40x3",
        "spectral_split": [1, 24, 15],
        "dual_orientation": (
            "quotient vertices are W33 lines; maximal K4 pencils are W33 points"
        ),
        "line_F3_filtration": [14, 11, 14],
        "point_F3_filtration": [10, 19, 10],
        "identification": (
            "the Pass4870 W33 line-side quotient identification; "
            "unique only up to PGSp"
        ),
    }
    assert payload["maps"] == {
        "P24": "-(A-12I)(A+4I)/60",
        "target_lane": "Pass4936 chamber line lane Q_L",
        "F_S_from_L": "(1/4)L_S P24_line L_L^T : Q^160 -> Q^120",
        "F_L_from_S": "(1/3)L_L P24_line L_S^T : Q^120 -> Q^160",
        "ranks": [24, 24],
        "partial_inverses": [
            "F_L_from_S F_S_from_L=Q_L",
            "F_S_from_L F_L_from_S=Q_S",
        ],
        "equivariance": "all native PSp generators and one outer PGSp generator",
    }
    assert payload["literal_rational_centralizer_solve"] == {
        "carrier": "image(P24_line)",
        "dimension": 24,
        "endomorphism_unknowns": 576,
        "generator_count": 3,
        "scalar_equations": 1728,
        "rank_certificate_prime": 101,
        "constraint_rank_mod_prime": 575,
        "rational_centralizer_dimension": 1,
        "basis": "scalar identity line",
        "common_Hom_dimension_via_partial_inverse": 1,
    }
    module = payload["module_theorem"]
    assert module["commutant_dimension_on_common_24D_sector"] == 1
    assert "Pass4936 chamber line lane" in module["consequence"]
    assert "second isomorphic packet copy" in module["consequence"]
    assert "literal 576-variable rational centralizer solve" in module["reason"]
    assert "rank 575" in module["reason"]
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}
    assert any("Pass4949 owns" in item for item in payload["prior_art"])
    boundary = payload["boundary"]
    assert "chamber line lane" in boundary
    assert "line and point carriers are not identified" in boundary
    assert "14|11|14 and 10|19|10" in boundary
    assert "transverse 20+60 sector" in boundary
    assert "individual chart-dependent HP/HL selectors" in boundary


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4939"

    completed = subprocess.run(
        [gap, "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = (
        tmp_path
        / "data"
        / "PART_W33_PASS4939_CHAMBER_STEINER_INTERTWINER.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
