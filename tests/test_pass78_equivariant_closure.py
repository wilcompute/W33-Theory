"""Pass 78 tests for the equivariant zeta / Terwilliger / code-boundary map."""

from __future__ import annotations

import json
import os
import sys
from contextlib import redirect_stdout
from functools import lru_cache
from io import StringIO
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


@lru_cache(maxsize=1)
def _data() -> dict:
    import w33_pass78_equivariant_closure as mod

    with redirect_stdout(StringIO()):
        mod.main()
    return json.loads(Path("w33_pass78_equivariant_closure.json").read_text(encoding="utf-8"))


def test_pass78_status() -> None:
    assert _data()["status"] == "PASS"


def test_vertex_artin_ihara_map() -> None:
    t1 = _data()["track1_vertex_artin_ihara"]
    assert t1["active_constituent_degrees"] == {"1": 1, "15": 1, "24": 1}
    assert t1["active_dimension_sum"] == 40
    assert t1["bass_denominator_degree"] == 480
    assert t1["inactive_irreducible_count_on_point_module"] == 31


def test_terwilliger_fingerprint() -> None:
    t2 = _data()["track2_terwilliger_fingerprint"]
    assert t2["bose_mesner_dimension"] == 3
    assert t2["terwilliger_dimension"] == 16
    assert t2["distance_fibre_sizes"] == [1, 12, 27]
    assert t2["local_graph_spectrum"] == {"-1": 8, "2": 4}


def test_ovoid_spread_duality() -> None:
    t3 = _data()["track3_ovoid_spread_duality"]
    assert t3["alpha_W33"] == 7
    assert t3["alpha_Q43"] == 10
    assert t3["spread_count"] == 36
    assert t3["line_participation_profile"] == {"9": 40}
    assert t3["spread_overlap_profile"] == {"1": 360, "4": 270}


def test_code_boundary_is_not_overpromoted() -> None:
    t4 = _data()["track4_66_code_boundary"]
    assert t4["explicit_generator_promoted_by_this_pass"] is False
    assert "generator" in t4["next_verification_target"].lower()


def test_weil_and_spence_boundaries() -> None:
    data = _data()
    t5 = data["track5_weil_clifford_carrier"]
    t6 = data["track6_spence_hearing_boundary"]
    assert t5["split_check"] is True
    assert t5["weil_split"] == [5, 4]
    assert t6["cospectral"] is True
    assert t6["locally_identical"] is True
    assert t6["non_isomorphic"] is True
    assert t6["full_28_adjacency_data_available_in_repo"] is False


def test_algebra_ladder() -> None:
    t7 = _data()["track7_algebra_ladder"]
    assert all(t7["checks"].values())
    dimensions = [row["dimension"] for row in t7["ladder"]]
    assert dimensions == [3, 9, 16, 40, 36, 480, 51840]
