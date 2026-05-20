from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_zero_sheet_w33_interlacing_shadow.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_zero_sheet_w33_interlacing_shadow", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zero_sheet_is_induced_principal_subgraph_of_w33() -> None:
    module = load_module()
    payload = module.build_payload()

    assert payload["summary"]["all_identities_hold"] is True
    assert payload["summary"]["w33_vertices"] == 40
    assert payload["summary"]["w33_edges"] == 240
    assert payload["summary"]["zero_sheet_vertices"] == 8
    assert payload["identities"]["induced_copy_matches_zero_sheet_adjacency"] is True
    assert payload["zero_sheet"]["induced_w33_vertex_indices"] == [4, 0, 8, 21, 14, 22, 16, 1]


def test_zero_sheet_w33_edge_decomposition_is_exact() -> None:
    module = load_module()
    payload = module.build_payload()
    edge_decomposition = payload["edge_decomposition"]

    assert edge_decomposition["zero_internal_edges"] == 9
    assert edge_decomposition["cut_edges"] == 78
    assert edge_decomposition["complement_internal_edges"] == 153
    assert edge_decomposition["total"] == 240
    assert payload["identities"]["cut_edges_are_e6_dimension"] is True
    assert payload["identities"]["complement_internal_edges_are_q2_times_odd_instances"] is True
    assert payload["zero_sheet"]["external_degree_sequence"] == [9, 8, 10, 11, 10, 11, 10, 9]


def test_zero_sheet_w33_interlacing_certificate_uses_exact_cubic_signs() -> None:
    module = load_module()
    payload = module.build_payload()
    certificate = payload["interlacing_certificate"]

    assert certificate["full_w33_ordered_spectrum"] == "[12, 2^24, -4^15]"
    assert certificate["zero_sheet_squared_cubic"] == "f(y)=y^3-9y^2+17y-8"
    assert certificate["cubic_signs"] == {
        "f(0)": -8,
        "f(1)": 1,
        "f(2)": -2,
        "f(6)": -14,
        "f(7)": 13,
    }
    assert certificate["root_interval_certificate"]["squared_roots_lie_in"] == [
        [0, 1],
        [1, 2],
        [6, 7],
    ]
    assert payload["identities"]["cubic_roots_interlace_by_interval_certificate"] is True
