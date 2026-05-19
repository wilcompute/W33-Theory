from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_hamming_horizon_functor_search.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_hamming_horizon_functor_search", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hamming_horizon_functor_balances_72_coordinates_into_eight_sheets() -> None:
    module = load_module()
    payload = module.build_payload()

    assert payload["summary"]["coordinates"] == 72
    assert payload["summary"]["hamming_sheets"] == 8
    assert payload["summary"]["sheet_size"] == 9
    assert payload["summary"]["balanced_gauge_lifts_found"] == 24
    assert payload["summary"]["all_identities_hold"] is True
    assert payload["assignment_summary"]["label_counts"] == {
        "Z": 9,
        "D01": 9,
        "D10": 9,
        "D11": 9,
        "V00": 9,
        "V01": 9,
        "V10": 9,
        "V11": 9,
    }


def test_hamming_horizon_functor_has_clean_coordinate_type_split() -> None:
    module = load_module()
    payload = module.build_payload()
    by_label = payload["assignment_summary"]["type_by_label"]

    assert by_label["Z"] == {"mixed_edge": 9}
    for label in ("V00", "V01", "V10", "V11"):
        assert by_label[label] == {"column_edge": 3, "mixed_edge": 6}
    for label in ("D01", "D10", "D11"):
        assert by_label[label] == {
            "mixed_edge": 1,
            "parity_symbol": 2,
            "row_edge": 6,
        }


def test_hamming_horizon_functor_respects_fano_line_incidence() -> None:
    module = load_module()
    payload = module.build_payload()

    assert payload["identities"]["nonzero_labels_are_fano_incident"] is True
    assert payload["identities"]["zero_sheet_is_exactly_9_mixed_edges"] is True
    for coord in payload["coordinates"]:
        if coord["label"] == "Z":
            assert coord["kind"] == "mixed_edge"
        else:
            assert coord["incidence_ok"] is True


def test_hamming_horizon_functor_support_rows_keep_expected_weight() -> None:
    module = load_module()
    payload = module.build_payload()
    support_profile = payload["assignment_summary"]["support_profile"]

    assert set(support_profile) == {"P01", "P02", "P03", "P12", "P13", "P23"}
    for profile in support_profile.values():
        assert profile["active_coordinates"] == 16
        assert len(profile["fano_line"]) == 3


def test_hamming_horizon_zero_sheet_has_rank_two_triangle_free_graph() -> None:
    module = load_module()
    payload = module.build_payload()
    zero_graph = payload["zero_sheet_subgraph"]

    assert zero_graph["vertex_count"] == 8
    assert zero_graph["edge_count"] == 9
    assert zero_graph["component_sizes"] == [8]
    assert zero_graph["cycle_rank"] == 2
    assert zero_graph["triangle_free"] is True
    assert zero_graph["simple_cycle_lengths"] == [4, 4, 6]
    assert zero_graph["row_incidence"] == {0: 9, 1: 3, 2: 6}
    assert zero_graph["column_incidence"] == {0: 3, 1: 5, 2: 5, 3: 5}
