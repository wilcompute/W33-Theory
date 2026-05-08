"""Tests for PART CCCII: Node Centrality Measures in W(3,3)"""
import json
import pathlib
import pytest
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "exploration"))

from PART_CCCII_CENTRALITY_MEASURES_BRIDGE import (
    avg_distance_from_vertex, closeness_centrality, eigenvector_centrality_value,
    harmonic_centrality, harmonic_centrality_normalized, katz_centrality_value,
    pervasiveness_index, diameter_value, eccentricity_each_vertex,
    distance_distribution, degree_all_vertices, verify_all, build_cccii_summary,
    V, K, R_EIG,
)

class TestVerifyAll:
    def test_verify_all_passes_27(self):
        _, passed, total = verify_all()
        assert total == 27
        assert passed == 27

    def test_no_failing_checks(self):
        checks, passed, total = verify_all()
        failed = [name for name, ok in checks if not ok]
        assert failed == []

class TestBasicProperties:
    def test_all_vertices_regular(self):
        assert degree_all_vertices() == K

    def test_diameter_3(self):
        assert diameter_value() == 3

    def test_eccentricity_eq_diameter(self):
        assert eccentricity_each_vertex() == diameter_value()

class TestDistanceDistribution:
    def test_distance_distribution_sums_V(self):
        dist_dist = distance_distribution()
        total = sum(count for _, count in dist_dist)
        assert total == V

    def test_distance_1_has_K_vertices(self):
        assert distance_distribution()[1][1] == K

    def test_distance_2_has_24(self):
        assert distance_distribution()[2][1] == 24

    def test_distance_3_has_3(self):
        assert distance_distribution()[3][1] == 3

class TestCloseness:
    def test_avg_distance_approx_1_77(self):
        avg_d = float(avg_distance_from_vertex())
        assert 1.75 < avg_d < 1.80

    def test_avg_distance_69_over_39(self):
        avg_d = float(avg_distance_from_vertex())
        assert abs(avg_d - 69/39) < 0.0001

    def test_closeness_positive(self):
        assert closeness_centrality() > 0

class TestEigenvectorCentrality:
    def test_eigenvector_approx_0_316(self):
        ec = eigenvector_centrality_value()
        assert abs(ec - 0.316) < 0.01

    def test_eigenvector_approx_r_over_sqrt_V(self):
        import math
        ec = eigenvector_centrality_value()
        expected = R_EIG / math.sqrt(V)
        assert abs(ec - expected) < 0.0001

class TestHarmonicCentrality:
    def test_harmonic_eq_25(self):
        assert harmonic_centrality() == 25

    def test_harmonic_normalized_approx_0_641(self):
        hn = harmonic_centrality_normalized()
        assert abs(hn - 25/39) < 0.01

    def test_harmonic_positive(self):
        assert harmonic_centrality() > 0

class TestKatzCentrality:
    def test_katz_centrality_approx_5(self):
        kc = katz_centrality_value()
        assert abs(kc - 5.0) < 0.1

    def test_katz_positive(self):
        assert katz_centrality_value() > 0

class TestPervasiveness:
    def test_pervasiveness_between_0_1(self):
        p = pervasiveness_index()
        assert 0 < p < 1

    def test_pervasiveness_approx_0_59(self):
        p = pervasiveness_index()
        assert abs(p - 0.59) < 0.05

class TestBuildSummary:
    def test_build_cccii_summary_runs(self):
        s = build_cccii_summary()
        assert s is not None

    def test_summary_status_pass(self):
        s = build_cccii_summary()
        assert s["status"] == "PASS"

    def test_summary_part_label(self):
        s = build_cccii_summary()
        assert s["part"] == "CCCII"

    def test_summary_checks_27(self):
        s = build_cccii_summary()
        assert s["checks_pass"] == 27
        assert s["checks_total"] == 27

    def test_json_written(self):
        build_cccii_summary()
        out = (
            pathlib.Path(__file__).resolve().parents[1]
            / "PART_CCCII_CENTRALITY_MEASURES_results.json"
        )
        assert out.exists()

    def test_json_content_pass(self):
        build_cccii_summary()
        out = (
            pathlib.Path(__file__).resolve().parents[1]
            / "PART_CCCII_CENTRALITY_MEASURES_results.json"
        )
        with open(out) as fh:
            data = json.load(fh)
        assert data["status"] == "PASS"
        assert data["checks_pass"] == 27
