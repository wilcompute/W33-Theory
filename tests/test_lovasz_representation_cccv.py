"""PART CCCV – Tests for Lovász Orthonormal Labeling and Geometric Representation.

Covers 27 checks from the bridge plus extended property verification.
"""
import math
import sys
import pathlib
import pytest

EXPLORATION = pathlib.Path(__file__).resolve().parents[1] / "exploration"
sys.path.insert(0, str(EXPLORATION))

from PART_CCCV_LOVASZ_REPRESENTATION_BRIDGE import (
    # constants
    V, K, LAM, MU, EDGES, ALPHA, CLIQUE_NU, q,
    MULT_R, MULT_S, R_EIG, S_EIG, GUT_DIM, SU5_MATTER, GENERATIONS,
    # theta
    lovasz_theta,
    independence_number,
    theta_lower_bound_alpha,
    theta_upper_bound_chi,
    theta_equals_alpha,
    lovasz_theta_from_spectral,
    # orthonormal labeling
    orthonormal_labeling_dim_lower_bound,
    orthonormal_labeling_dim_exact,
    orthonormal_labeling_gram_matrix_eigenvalues,
    orthonormal_labeling_vectors_norm,
    orthonormal_labeling_inner_products_nonedges,
    orthonormal_labeling_uniqueness,
    orthonormal_labeling_automorphism_group,
    # complement
    complement_graph_lovasz_theta,
    complement_edges,
    complement_independence_number,
    shannon_capacity_inequality,
    # applications
    independence_number_via_lovasz,
    chromatic_number_via_theta,
    clique_cover_number,
    fractional_independence_number,
    fractional_chromatic_number,
    # geometric
    geometric_realization_unit_sphere,
    geometric_realization_polytope,
    # SM crosswalk & verification
    sm_crosswalk,
    verify_all,
    build_cccv_summary,
)


# ─────────────────────────────────────────────
# 1. W(3,3) constants
# ─────────────────────────────────────────────
class TestConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240

    def test_ALPHA(self):
        assert ALPHA == 10

    def test_CLIQUE_NU(self):
        assert CLIQUE_NU == 4

    def test_q(self):
        assert q == 3

    def test_eigenvalue_r(self):
        assert R_EIG == 2

    def test_eigenvalue_s(self):
        assert S_EIG == -4

    def test_gut_dim(self):
        assert GUT_DIM == 27

    def test_su5_matter(self):
        assert SU5_MATTER == 15

    def test_generations(self):
        assert GENERATIONS == 3


# ─────────────────────────────────────────────
# 2. Lovász theta function
# ─────────────────────────────────────────────
class TestLovaszTheta:
    def test_lovasz_theta_value(self):
        assert lovasz_theta() == 10

    def test_lovasz_theta_equals_alpha(self):
        assert lovasz_theta() == ALPHA

    def test_independence_number(self):
        assert independence_number() == 10

    def test_theta_lower_bound_alpha(self):
        assert theta_lower_bound_alpha() == 10

    def test_theta_upper_bound(self):
        assert theta_upper_bound_chi() == 10

    def test_theta_equals_alpha_true(self):
        assert theta_equals_alpha() is True

    def test_theta_from_spectral(self):
        assert lovasz_theta_from_spectral() == 10

    def test_theta_is_positive(self):
        assert lovasz_theta() > 0

    def test_theta_is_integer(self):
        assert isinstance(lovasz_theta(), int)

    def test_theta_divides_V(self):
        assert V % lovasz_theta() == 0

    def test_theta_lower_le_theta(self):
        assert theta_lower_bound_alpha() <= lovasz_theta()


# ─────────────────────────────────────────────
# 3. Orthonormal labeling dimension
# ─────────────────────────────────────────────
class TestOrthonormalLabeling:
    def test_dim_lower_bound(self):
        assert orthonormal_labeling_dim_lower_bound() == 3

    def test_dim_exact(self):
        assert orthonormal_labeling_dim_exact() == 3

    def test_dim_equals_q(self):
        assert orthonormal_labeling_dim_exact() == q

    def test_gram_matrix_rank_3(self):
        gram = orthonormal_labeling_gram_matrix_eigenvalues()
        assert gram["rank"] == 3

    def test_gram_matrix_has_V_eigenvalues(self):
        gram = orthonormal_labeling_gram_matrix_eigenvalues()
        assert gram["V"] == V

    def test_gram_matrix_eigenvalues_length(self):
        gram = orthonormal_labeling_gram_matrix_eigenvalues()
        assert len(gram["eigenvalues"]) == V

    def test_gram_matrix_rank_lt_V(self):
        gram = orthonormal_labeling_gram_matrix_eigenvalues()
        assert gram["rank"] < gram["V"]

    def test_unit_vector_norm(self):
        assert orthonormal_labeling_vectors_norm() == 1.0

    def test_nonedge_inner_product_negative(self):
        assert orthonormal_labeling_inner_products_nonedges() < 0

    def test_labeling_not_unique(self):
        assert orthonormal_labeling_uniqueness() is False

    def test_automorphism_group_size(self):
        assert orthonormal_labeling_automorphism_group() == 24

    def test_automorphism_group_equals_mult_r(self):
        assert orthonormal_labeling_automorphism_group() == MULT_R

    def test_dim_lower_le_exact(self):
        assert orthonormal_labeling_dim_lower_bound() <= orthonormal_labeling_dim_exact()


# ─────────────────────────────────────────────
# 4. Complement graph
# ─────────────────────────────────────────────
class TestComplementGraph:
    def test_complement_theta(self):
        assert complement_graph_lovasz_theta() == 4

    def test_complement_theta_equals_mu(self):
        assert complement_graph_lovasz_theta() == MU

    def test_complement_edges(self):
        assert complement_edges() == 540

    def test_complement_edges_formula(self):
        expected = V * (V - 1) // 2 - EDGES
        assert complement_edges() == expected

    def test_complement_independence_number(self):
        assert complement_independence_number() == 4

    def test_complement_independence_equals_clique_nu(self):
        assert complement_independence_number() == CLIQUE_NU

    def test_shannon_capacity_equality(self):
        assert shannon_capacity_inequality() == V

    def test_shannon_capacity_exact_40(self):
        assert shannon_capacity_inequality() == 40

    def test_shannon_product_theta_times_complement(self):
        product = lovasz_theta() * complement_graph_lovasz_theta()
        assert product == V

    def test_total_edges_plus_complement(self):
        assert EDGES + complement_edges() == V * (V - 1) // 2


# ─────────────────────────────────────────────
# 5. Independence and chromatic bounds
# ─────────────────────────────────────────────
class TestBounds:
    def test_independence_via_lovasz(self):
        assert independence_number_via_lovasz() == 10

    def test_chromatic_times_alpha_equals_V(self):
        assert chromatic_number_via_theta() is True

    def test_clique_cover_number(self):
        assert clique_cover_number() == 4

    def test_clique_cover_equals_complement_theta(self):
        assert clique_cover_number() == complement_graph_lovasz_theta()

    def test_fractional_independence_le_theta(self):
        assert fractional_independence_number() <= lovasz_theta()

    def test_fractional_independence_value(self):
        assert fractional_independence_number() == 10

    def test_fractional_chromatic_exact(self):
        assert fractional_chromatic_number() == 4.0

    def test_fractional_chromatic_formula(self):
        assert abs(fractional_chromatic_number() - V / lovasz_theta()) < 1e-9

    def test_fractional_chromatic_ge_chi(self):
        # χ_f ≤ χ for vertex-transitive graphs; χ_f = V/θ = 4 = χ here
        assert fractional_chromatic_number() <= 4 + 1e-9


# ─────────────────────────────────────────────
# 6. Geometric realization
# ─────────────────────────────────────────────
class TestGeometric:
    def test_unit_sphere_realization(self):
        assert geometric_realization_unit_sphere() is True

    def test_polytope_dimension(self):
        poly = geometric_realization_polytope()
        assert poly["dimension"] == 3

    def test_polytope_vertices(self):
        poly = geometric_realization_polytope()
        assert poly["vertices"] == V

    def test_polytope_is_dict(self):
        assert isinstance(geometric_realization_polytope(), dict)

    def test_polytope_dimension_equals_q(self):
        poly = geometric_realization_polytope()
        assert poly["dimension"] == q


# ─────────────────────────────────────────────
# 7. SM Crosswalk
# ─────────────────────────────────────────────
class TestSMCrosswalk:
    def test_crosswalk_has_7_entries(self):
        assert len(sm_crosswalk()) == 7

    def test_crosswalk_has_theta_key(self):
        keys = sm_crosswalk().keys()
        assert any("lovasz" in k for k in keys)

    def test_crosswalk_has_dimension_key(self):
        keys = sm_crosswalk().keys()
        assert any("dim" in k or "labeling" in k for k in keys)

    def test_crosswalk_has_shannon_key(self):
        keys = sm_crosswalk().keys()
        assert any("shannon" in k or "capacity" in k for k in keys)

    def test_crosswalk_all_strings(self):
        for v in sm_crosswalk().values():
            assert isinstance(v, str)

    def test_crosswalk_has_automorphism_key(self):
        keys = sm_crosswalk().keys()
        assert any("aut" in k for k in keys)


# ─────────────────────────────────────────────
# 8. Verification and summary
# ─────────────────────────────────────────────
class TestVerifyAll:
    def test_verify_all_27_checks(self):
        checks, passed, total = verify_all()
        assert total == 27

    def test_verify_all_pass_count(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert len(result) == 3

    def test_verify_all_list_of_tuples(self):
        checks, passed, total = verify_all()
        for name, ok in checks:
            assert isinstance(name, str)
            assert isinstance(ok, bool)

    def test_verify_all_no_failures(self):
        checks, passed, total = verify_all()
        failed = [name for name, ok in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"


class TestBuildSummary:
    def test_build_summary_returns_dict(self):
        summary = build_cccv_summary()
        assert isinstance(summary, dict)

    def test_build_summary_part(self):
        summary = build_cccv_summary()
        assert summary["part"] == "CCCV"

    def test_build_summary_status_pass(self):
        summary = build_cccv_summary()
        assert summary["status"] == "PASS"

    def test_build_summary_checks_pass(self):
        summary = build_cccv_summary()
        assert summary["checks_pass"] == summary["checks_total"]

    def test_build_summary_has_discoveries(self):
        summary = build_cccv_summary()
        assert len(summary["discoveries"]) >= 8

    def test_build_summary_has_fields(self):
        summary = build_cccv_summary()
        assert "lovasz_theta" in summary["fields"]

    def test_build_summary_lovasz_theta_10(self):
        summary = build_cccv_summary()
        assert summary["fields"]["lovasz_theta"] == 10

    def test_build_summary_shannon_capacity_40(self):
        summary = build_cccv_summary()
        assert summary["fields"]["shannon_capacity_product"] == 40

    def test_build_summary_orthonormal_dim_3(self):
        summary = build_cccv_summary()
        assert summary["fields"]["orthonormal_labeling_dimension"] == 3

    def test_build_summary_json_file_written(self):
        summary = build_cccv_summary()
        out = pathlib.Path(__file__).resolve().parents[1] / "PART_CCCV_LOVASZ_REPRESENTATION_results.json"
        assert out.exists()
