"""Tests for Pillar 102: E₆ Architecture and Schläfli graph."""

import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT))
from THEORY_PART_CCII_E6_ARCHITECTURE import architecture_analysis


@pytest.fixture(scope="module")
def arch():
    try:
        return architecture_analysis()
    except FileNotFoundError as exc:
        pytest.skip(f"E6 architecture data unavailable: {exc}", allow_module_level=True)


class TestDegree:
    """A1: Every QID has exactly degree 10."""

    def test_uniform_degree_10(self, arch):
        assert arch["A1_uniform_degree_10"] is True

    def test_degree_set(self, arch):
        assert arch["A1_degree_set"] == [10]

    def test_27_vertices(self, arch):
        assert arch["A1_num_vertices"] == 27


class TestWeylIndex:
    """A2: |W(E₆)|/|N| = 270 = #transport edges."""

    def test_index_270(self, arch):
        assert arch["A2_WE6_over_N"] == 270

    def test_equals_edge_count(self, arch):
        assert arch["A2_equals_transport_edges"] is True

    def test_weyl_order(self, arch):
        assert arch["A2_WE6"] == 51840

    def test_n_order(self, arch):
        assert arch["A2_N_order"] == 192


class TestValence:
    """A3: Schläfli valence = |W(D₅)|/|N| = 10."""

    def test_wd5(self, arch):
        assert arch["A3_WD5"] == 1920

    def test_valence_10(self, arch):
        assert arch["A3_schlafli_valence"] == 10

    def test_valence_match(self, arch):
        assert arch["A3_valence_match"] is True


class TestTransitivity:
    """A4: N acts transitively on 27 QIDs."""

    def test_single_orbit(self, arch):
        assert arch["A4_transitive_on_27"] is True

    def test_orbit_sizes(self, arch):
        assert arch["A4_orbit_sizes"] == [27]


class TestTritangent:
    """A5: Three self-loop QIDs form a tritangent clique."""

    def test_three_self_loops(self, arch):
        assert arch["A5_num_self_loops"] == 3

    def test_self_loop_qids(self, arch):
        assert arch["A5_self_loop_qids"] == [13, 14, 26]

    def test_clique_complete(self, arch):
        assert arch["A5_clique_complete"] is True


class TestMultiplicity:
    """A6: Edge multiplicity structure sums to 270."""

    def test_total_270(self, arch):
        assert arch["A6_total_check"] == 270

    def test_multiplicity_categories(self, arch):
        md = arch["A6_multiplicity_distribution"]
        assert "2" in md and "4" in md and "6" in md


class TestBijections:
    """A7: Key bijection counts."""

    def test_192_flags(self, arch):
        assert arch["A7_flags"] == 192

    def test_270_edges(self, arch):
        assert arch["A7_edges"] == 270

    def test_27_qids(self, arch):
        assert arch["A7_qids"] == 27
