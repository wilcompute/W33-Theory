"""Focused regression for the GAP-owned Pass 1147 certificate."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "analysis" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.g"
)
CERTIFICATE = (
    ROOT / "data" / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
)


def _assert_exact_certificate(payload: dict[str, object]) -> None:
    assert payload["status"] == "PASS"
    assert payload["directed_schlaefli"] == {
        "object": (
            "three colored copies of the directed-edge carrier of "
            "SRG(27,16,10,8)"
        ),
        "shell_patterns": [
            [-4, 0, 4],
            [-4, 4, 0],
            [0, -4, 4],
            [0, 4, -4],
            [4, -4, 0],
            [4, 0, -4],
        ],
        "shell_sizes": [27] * 6,
        "color_fiber_sizes": [432, 432, 432],
        "a2_orbit_sizes": [
            1,
            27,
            27,
            27,
            270,
            432,
            27,
            27,
            270,
            27,
            1,
            432,
            432,
            240,
        ],
        "srg_parameters": [27, 16, 10, 8],
        "directed_edge_count": 432,
        "directed_edge_stabilizer": {"order": 120, "structure": "S5"},
        "objectwise_bijection_verified": True,
    }

    transform = payload["steinberg_transform"]
    assert transform["matrix_shape"] == [325, 432]
    assert transform["rank"] == 81
    assert transform["rank_mod_1000003"] == 81
    assert transform["reversal_odd"] is True
    assert transform["vector_norm_squared"] == 600
    assert transform["gram_identity"] == "G^2=3200G"
    assert transform["projective_lines"] == 216
    assert transform["projective_dimension"] == 81
    assert transform["projective_valencies"] == [120, 60, 35]
    assert transform["absolute_angle_relations_form_association_scheme"] is False

    torsor = payload["a2_color_torsor"]
    assert torsor["combined_matrix_shape"] == [975, 1296]
    assert torsor["combined_rank"] == 243
    assert torsor["rational_sector_ranks"] == [81, 162]
    assert torsor["complex_sector_ranks"] == [81, 81, 81]

    enhanced = payload["enhanced_map"]
    assert enhanced["matrix_shape"] == [1020, 2240]
    assert enhanced["rank"] == 288
    assert enhanced["kernel_dimension"] == 1952
    assert enhanced["active_source_profile"] == {
        "cubic": 240,
        "schlaefli": 1296,
        "silent": 704,
    }
    assert enhanced["supports_disjoint"] is True

    residual = payload["residual_representation"]
    assert residual["dimension"] == 1952
    assert residual["degree_multiplicities"] == [
        [1, 13],
        [6, 16],
        [15, 5],
        [15, 4],
        [20, 21],
        [24, 2],
        [30, 9],
        [60, 4],
        [64, 10],
        [90, 1],
    ]

    integral = payload["integral_edge_lattice"]
    assert integral["matrix_shape"] == [432, 325]
    assert integral["rational_rank"] == 81
    assert integral["smith_diagonal_profile"] == {
        "1": 15,
        "2": 6,
        "4": 8,
        "8": 29,
        "40": 23,
    }
    assert integral["saturation_index_factorization"] == {"2": 178, "5": 23}
    assert integral["rank_mod_prime"] == {
        "2": 15,
        "3": 81,
        "5": 58,
        "7": 81,
        "11": 81,
    }
    assert integral["bad_primes"] == [2, 5]
    assert integral["structural_normalization"] == {
        "natural_Q_edge_content": 280,
        "projector_scale": 11200,
        "primitive_projector_multiplier": 40,
        "identity": "T=Q/280=40*P_4",
        "all_smith_invariants_divide_40": True,
        "prime7_cancellation": (
            "7 divides both Q's eigenvalue scale 11200 and every "
            "Schlaefli-edge Q-image content 280; it is absent from the "
            "primitive multiplier 40, the Smith product, and the rank drop"
        ),
    }
    assert integral["modular_image_composition"] == {
        "2": {
            "rank": 15,
            "irreducible_factor_dimensions": [1, 14],
            "ambient_81_Brauer_profile": {
                "1": 1,
                "6": 3,
                "8": 1,
                "14": 1,
                "40": 1,
            },
        },
        "5": {
            "rank": 58,
            "irreducible_factor_dimensions": [58],
            "ambient_81_Brauer_profile": {"23": 1, "58": 1},
        },
    }
    assert integral["integral_color_fourier_split"] == {
        "basis_matrix": [[1, 1, 0], [1, -1, 1], [1, 0, -1]],
        "smith_diagonal": [1, 1, 3],
        "one_color_index": 3,
        "rank81_index_factorization": {"3": 81},
        "rank81_index_decimal": "443426488243037769948249630619149892803",
    }
    bridge = integral["five_primary_critical_group_bridge"]
    assert bridge["W33_reduced_laplacian_smith_profile"] == {
        "1": 16,
        "10": 8,
        "40": 1,
        "160": 14,
    }
    assert bridge["literal_action"] == {
        "group": "W(E6)=PGSp(4,3)",
        "order": 51840,
        "derived_group": "PSp(4,3)",
        "derived_order": 25920,
        "generator_orders": [6, 6],
        "outer_sign_values": [-1, -1],
    }
    assert bridge["frame_saturation_quotient"] == {
        "prime": 5,
        "dimension": 23,
        "module": "irreducible 23-dimensional F5 W(E6)-module",
    }
    assert bridge["W33_sandpile_primary"] == {
        "prime": 5,
        "group": "(Z/5)^23",
        "dimension": 23,
        "module": "irreducible 23-dimensional F5 W(E6)-module",
    }
    assert bridge["Hom_dimensions"] == {
        "untwisted_W(E6)": 0,
        "outer_sign_twisted_W(E6)": 1,
        "restricted_PSp(4,3)": 1,
    }
    assert bridge["nonzero_scalar_intertwiners"] == {
        "untwisted": 0,
        "outer_sign_twisted": 4,
        "restricted_PSp(4,3)": 4,
    }
    assert bridge["all_nonzero_scalar_intertwiners_invertible"] is True
    assert bridge["module_isomorphism"] == (
        "(saturation quotient at 5) tensor outer_sign ~= K(W33)_5"
    )
    assert bridge["uniqueness"] == (
        "unique up to F5^x; exactly four nonzero scalar isomorphisms"
    )
    assert "no canonical integral lift" in bridge["scope"]
    assert bridge["saturated_frame_exact_sequence"] == {
        "sequence": (
            "0 -> irreducible_58 -> saturated_frame_mod5_81 -> "
            "K(W33)_5 tensor outer_sign -> 0"
        ),
        "splits_over_W(E6)": False,
        "splits_over_PSp(4,3)": False,
        "Hom_quotient_to_saturation": {
            "W(E6)": 0,
            "PSp(4,3)": 0,
        },
        "submodule_dimension_profiles": {
            "W(E6)": {"0": 1, "58": 1, "81": 1},
            "PSp(4,3)": {"0": 1, "58": 1, "81": 1},
        },
        "structure": (
            "the image 58 is the unique proper nonzero submodule; "
            "the saturated reduction is a nonsplit length-two module"
        ),
        "extension_scope": (
            "this certifies that the displayed extension class is nonzero; "
            "it does not compute the dimension of the full Ext^1 space"
        ),
    }


def test_checked_in_certificate_has_exact_pass1147_invariants() -> None:
    _assert_exact_certificate(json.loads(CERTIFICATE.read_text(encoding="utf-8")))


@pytest.mark.skipif(shutil.which("gap") is None, reason="GAP is required")
def test_gap_rebuild_is_deterministic(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    completed = subprocess.run(
        ["gap", "-q", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    rebuilt = (
        tmp_path
        / "data"
        / "w33_pass1147_schlaefli_steinberg_fourier_bridge.json"
    )
    assert rebuilt.read_bytes() == CERTIFICATE.read_bytes()
    _assert_exact_certificate(json.loads(rebuilt.read_text(encoding="utf-8")))
