"""Focused native-GAP regression for Passes 4324--4327."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4324_4327_chamber_hecke_hashimoto.g"
FROZEN = (
    ROOT
    / "data"
    / "PART_W33_PASS4324_4327_CHAMBER_HECKE_HASHIMOTO.json"
)
PASS_LINE = (
    "Passes 4324--4327 chamber Hecke/Hashimoto: "
    "31/31 checks; status=PASS"
)

EXPECTED_CHECKS = {
    "c2_braid_length_4",
    "chambers_160",
    "chiral_polynomial",
    "chiral_rank_48",
    "chiral_square_flag_polynomial",
    "conjugate_packet_is_24_copies_of_dim2",
    "conjugate_projector_exact",
    "conjugate_swap_law",
    "coxeter_minimal_polynomial",
    "coxeter_spectrum_multiplicities",
    "critical_clock_fourth_power_81",
    "critical_clock_rank_78",
    "distance_two_split",
    "folded_cubic_coefficients",
    "folded_cubic_complex_structure_689",
    "folded_cubic_exact_normal_form",
    "folded_cubic_minimal_polynomial",
    "four_one_dimensional_multiplicities",
    "hashimoto_block_factorization",
    "hashimoto_square_panel_orders",
    "hecke_image_dimension_8",
    "lines_40",
    "old_6455_explained",
    "oriented_halves_are_binary_degree_9",
    "oriented_halves_disjoint",
    "packet_basis_dimension_4",
    "packet_clifford_relations",
    "panel_quadratics",
    "panel_row_sums_3",
    "points_40",
    "time_reversal_transposes_hashimoto",
}


def _assert_strongest_exact_fields(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4324_4327.chamber_hecke_hashimoto.v1"
    assert payload["status"] == "PASS"
    assert payload["objects"] == {
        "points": 40,
        "lines": 40,
        "chambers": 160,
        "directed_chambers": 320,
        "point_graph_arcs": 480,
    }

    assert payload["pass_4324_hecke_machine"] == {
        "panel_relations": "P^2=2P+3I, L^2=2L+3I, PLPL=LPLP",
        "generated_algebra_dimension": 8,
        "chamber_module": (
            "1*chi_(3,3) + 15*chi_(3,-1) + 15*chi_(-1,3) + "
            "81*chi_(-1,-1) + 24*V_2"
        ),
        "hashimoto_factorization": (
            "B_Levi=[[0,L],[P,0]], B_Levi^2=diag(LP,PL)"
        ),
    }
    assert payload["pass_4325_oriented_distance_two"] == {
        "forward": "K=LP is a binary 9-out regular oriented distance-two half",
        "reverse": "K^T=PL is the disjoint reverse half",
        "symmetric_sum": "K+K^T=C^2-2C-6I",
        "K_characteristic_polynomial": (
            "(x-9)(x-1)^81(x+3)^30(x^2+9)^24"
        ),
        "critical_subspace_dimension_per_orientation": 78,
        "critical_clock": (
            "K^4=81I on ker((K+3I)(K^2+9I)); equivalently (K/3)^4=I"
        ),
    }

    conjugate = payload["pass_4326_conjugate_channel"]
    assert conjugate == {
        "chirality": "Omega=LP-PL",
        "characteristic_polynomial": "x^112(x^2+60)^24",
        "projector": "Pi_48=-Omega^2/60",
        "rank": 48,
        "complex_structure": "(Omega/sqrt(60))^2=-I on im(Pi_48)",
        "conjugate_swap": (
            "Omega(C-2I)=-(C-2I)Omega; C eigenvalues 2+sqrt(6) and "
            "2-sqrt(6) are exchanged"
        ),
        "exact_scope": (
            "This constructs the conjugate 24+24 channel; it does not "
            "construct a W(G2) action."
        ),
    }
    assert "does not construct a W(G2) action" in conjugate["exact_scope"]

    folded = payload["pass_4327_folded_cubic_normal_form"]
    assert folded == {
        "operator": "F=Pi_48 (T B_W33^3 T^T) Pi_48",
        "basis": "{Pi_48, X=(C-2I)Pi_48, Omega, X Omega}",
        "normal_form": "F=-68Pi_48-31X-(21/2)Omega+(2/3)XOmega",
        "off_diagonal_square": (
            "(-(21/2)Omega+(2/3)XOmega)^2=-6455Pi_48"
        ),
        "full_packet_polynomial": "F^2+136F+5313Pi_48=0",
        "packet_complex_structure": (
            "(F+68Pi_48)^2=-689Pi_48, with 689=13*53"
        ),
        "boundary": (
            "Exact finite operator identity. No continuum, particle, mass, "
            "or coupling identification is asserted."
        ),
    }
    assert folded["boundary"].startswith("Exact finite operator identity.")
    assert "No continuum, particle, mass, or coupling identification" in folded[
        "boundary"
    ]

    assert payload["prior_art_bridge"] == [
        "BT557 flag action",
        "BT617 folded cubic sector action",
        "BT622 conjugate root channel boundary",
        "BT744 Tits building dictionary",
        "Pass 4322 directed flags are the Levi Hashimoto carrier",
    ]
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Passes 4324--4327"

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
        / "PART_W33_PASS4324_4327_CHAMBER_HECKE_HASHIMOTO.json"
    )
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_strongest_exact_fields(json.loads(rebuilt_bytes))
