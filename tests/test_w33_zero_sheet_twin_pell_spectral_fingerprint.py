from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_zero_sheet_twin_pell_spectral_fingerprint.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_zero_sheet_twin_pell_spectral_fingerprint", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zero_sheet_adjacency_charpoly_is_twin_pell_fingerprint() -> None:
    module = load_module()
    payload = module.build_payload()

    assert payload["summary"]["all_identities_hold"] is True
    assert payload["adjacency_characteristic_coefficients"] == [1, 0, -9, 0, 17, 0, -8, 0, 0]
    assert payload["summary"]["adjacency_characteristic_polynomial"] == "x^8 - 9x^6 + 17x^4 - 8x^2"
    assert payload["twin_pell_dictionary"]["squared_spectral_cubic_coefficients"] == [1, -9, 17, -8]
    assert payload["twin_pell_dictionary"]["q^2"] == 9
    assert payload["twin_pell_dictionary"]["2^q"] == 8
    assert payload["twin_pell_dictionary"]["q^2+2^q"] == 17


def test_zero_sheet_laplacian_tree_count_is_w33_g_multiplicity() -> None:
    module = load_module()
    payload = module.build_payload()

    assert payload["laplacian_characteristic_coefficients"] == [
        1,
        -18,
        129,
        -474,
        956,
        -1048,
        573,
        -120,
        0,
    ]
    assert payload["matrix_tree"]["spanning_tree_count"] == 15
    assert payload["matrix_tree"]["w33_g_multiplicity"] == 15
    assert payload["identities"]["matrix_tree_count_is_g_multiplicity"] is True


def test_zero_sheet_spectral_nullity_matches_cycle_rank() -> None:
    module = load_module()
    payload = module.build_payload()
    graph = payload["zero_sheet_subgraph"]

    assert graph["vertex_count"] == 8
    assert graph["edge_count"] == 9
    assert graph["cycle_rank"] == 2
    assert payload["adjacency_characteristic_coefficients"][-2:] == [0, 0]
    assert payload["identities"]["adjacency_nullity_equals_cycle_rank"] is True
    assert payload["identities"]["zero_sheet_is_8_vertices_9_edges_rank2"] is True
