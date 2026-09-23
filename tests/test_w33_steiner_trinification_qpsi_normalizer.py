from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_steiner_trinification_qpsi_normalizer.py"
DATA = ROOT / "data/w33_steiner_trinification_qpsi_normalizer.json"


def load_script():
    spec = importlib.util.spec_from_file_location(
        "steiner_trinification_qpsi_normalizer_test", SCRIPT
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_certificate_is_exact_recomputation():
    recomputed = load_script().main(write=False)
    assert recomputed == json.loads(DATA.read_text())


def test_kernel_atlas_normalizer_and_repair_are_frozen():
    out = json.loads(DATA.read_text())
    assert out["status"] == (
        "PASS_ALL_WE6_TRINIFICATION_CHARTS_EXCLUDE_NONFI_QPSI_NORMALIZERS"
    )

    kernel = out["ternary_kernel"]
    assert kernel["incidence_matrix_shape"] == [45, 27]
    assert kernel["rank_F3"] == 21
    assert kernel["nullity_F3"] == 6
    assert kernel["code_parameters"] == "[27,6,12]_3"
    assert kernel["kernel_word_count"] == 729
    assert kernel["weight_enumerator"] == {
        "0": 1,
        "12": 72,
        "18": 510,
        "21": 144,
        "27": 2,
    }
    assert kernel["balanced_9_9_9_words"] == 510
    assert kernel["special_labelled_words"] == 240
    assert kernel["ordinary_labelled_words"] == 270
    assert kernel["unlabelled_partitions"] == 40
    assert kernel["other_unlabelled_partitions"] == 45
    assert kernel["line_side_kernel_dimension_F3"] == 24
    assert out["steiner_prior_crosscheck"][
        "kernel_partitions_equal_prior_40_triads"
    ] is True

    dictionary = out["projective_121_dictionary"]
    assert dictionary["construction"] == "P(ker_F3(C) / <all-ones>) = PG(4,3)"
    assert dictionary["projective_ray_count"] == 121
    assert dictionary["codeword_lifts_per_ray"] == 6
    assert dictionary["W_E6_projective_action_order"] == 51840
    assert dictionary["W_E6_projective_orbit_sizes"] == [36, 40, 45]
    assert dictionary["norm_class_dictionary"] == {
        "norm_0": "40 Steiner triads",
        "norm_1": "45 tritangents",
        "norm_2": "36 double-sixes",
    }
    assert all(dictionary["objectwise_checks"].values())

    atlas = out["trinification_atlas"]
    assert atlas["charts_per_partition"] == 1296
    assert atlas["total_labelled_charts"] == 51840
    assert atlas["W_E6_order"] == 51840
    assert atlas["partition_stabilizer_order"] == 1296
    assert atlas["W_E6_action_on_labelled_atlas"] == "regular"

    normalizer = out["normalizer_closure"]
    assert normalizer["normalizing_powers_mod12"] == [0, 4, 8]
    assert normalizer["normalizing_chart_counts_by_D12_power"] == {
        str(power): 51840 if power in (0, 4, 8) else 0 for power in range(12)
    }
    assert normalizer["matter_parity_D12_power6_normalizes_in_any_chart"] is False

    repair = out["minimal_interface_repair"]
    assert repair["hamming_distance_to_separable_table_census"] == {
        "1": 5760,
        "5": 34560,
        "6": 11520,
    }
    assert repair["relative_anchor_distance_census_in_one_chart"] == {
        "1": 3,
        "5": 18,
        "6": 6,
    }
    assert repair["minimum_phase_cells"] == 1
    assert repair["best_chart_count"] == 5760
    assert len(repair["best_witness"]["matter81_defect_support"]) == 3

    obstruction = out["equivariant_compiler_obstruction"]
    assert obstruction["H27_maximum_rank"] == 9
    assert obstruction["H27_target_dimension"] == 27
    assert obstruction["K81_maximum_rank"] == 27
    assert obstruction["K81_target_dimension"] == 81
    assert obstruction["invertible_H27_equivariant_intertwiner_exists"] is False
    assert obstruction["invertible_K81_equivariant_compiler_exists"] is False
    assert "symmetry-changing" in obstruction["surviving_frontier"]
    assert all(out["checks"].values())
