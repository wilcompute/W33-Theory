"""Part CCCCXXXIX -- E8 edge/root dictionary boundary witness."""

from __future__ import annotations

import json
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

mod = importlib.import_module("PART_CCCCXXXIX_E8_EDGE_ROOT_DICTIONARY_BOUNDARY")


def _load_results() -> dict:
    out = ROOT / "PART_CCCCXXXIX_e8_edge_root_dictionary_boundary_results.json"
    if not out.exists():
        mod.main()
    return json.loads(out.read_text(encoding="utf-8"))


def test_main_runs_and_writes_json() -> None:
    rc = mod.main()
    assert rc == 0
    out = ROOT / "PART_CCCCXXXIX_e8_edge_root_dictionary_boundary_results.json"
    assert out.exists()


def test_verified_and_check_count() -> None:
    data = _load_results()
    assert data["Verified"] is True
    assert data["checks_total"] == 15
    assert data["checks_passed"] == 15


def test_w33_line_graph_degree() -> None:
    data = _load_results()
    assert data["w33"]["edges"] == 240
    assert data["w33"]["line_graph_vertices"] == 240
    assert data["w33"]["line_graph_degree_set"] == [22]


def test_e8_counts_and_packets() -> None:
    data = _load_results()
    assert data["e8"]["roots"] == 240
    assert data["e8"]["doubled_norms"] == [8]

    packet = data["e8"]["sample_dot_packet"]
    assert packet["8"] == 1
    assert packet["-8"] == 1
    assert packet["4"] == 56
    assert packet["-4"] == 56
    assert packet["0"] == 126


def test_no_naive_threshold_match() -> None:
    data = _load_results()
    degrees = data["e8"]["naive_threshold_degree_sets"]
    assert degrees["dot_plus_one"] == [56]
    assert degrees["dot_zero"] == [126]
    assert degrees["dot_minus_one"] == [56]
    assert 22 not in (degrees["dot_plus_one"] + degrees["dot_zero"] + degrees["dot_minus_one"])
