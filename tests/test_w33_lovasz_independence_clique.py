"""Tests for W(3,3) Lovász-extremal independence-clique duality (MCXLVIII)."""
from fractions import Fraction
from analysis.w33_lovasz_independence_clique import lovasz_independence_clique_packet


def _frac(entry):
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def test_lovasz_theta_G():
    p = lovasz_independence_clique_packet()
    theta_G = _frac(p["lovasz_theta"]["theta_G"])
    assert theta_G == Fraction(10, 1)


def test_lovasz_theta_Gbar():
    p = lovasz_independence_clique_packet()
    theta_Gbar = _frac(p["lovasz_theta"]["theta_Gbar"])
    assert theta_Gbar == Fraction(4, 1)


def test_lovasz_product_equals_v():
    p = lovasz_independence_clique_packet()
    assert p["lovasz_theta"]["product_equals_v"]
    product = _frac(p["lovasz_theta"]["product_theta_G_times_Gbar"])
    assert product == Fraction(40, 1)


def test_alpha_and_omega():
    p = lovasz_independence_clique_packet()
    ic = p["independence_clique"]
    assert ic["alpha"] == 10
    assert ic["omega"] == 4
    assert ic["alpha_times_omega"] == 40
    assert ic["perfect_partition"]


def test_alpha_formula():
    p = lovasz_independence_clique_packet()
    ic = p["independence_clique"]
    assert ic["alpha_formula_check"]
    assert _frac(ic["alpha_from_formula"]) == Fraction(10, 1)


def test_fractional_chromatic_equals_omega():
    p = lovasz_independence_clique_packet()
    fc = p["fractional_chromatic"]
    assert fc["chi_f_equals_omega"]
    assert _frac(fc["chi_f"]) == Fraction(4, 1)


def test_clique_power_law():
    p = lovasz_independence_clique_packet()
    cp = p["clique_power_law"]
    assert cp["verified"]
    assert cp["omega"] == 4
    assert cp["r"] == 2
    assert cp["power"] == 4


def test_physical_dimensions():
    p = lovasz_independence_clique_packet()
    pd = p["physical_dimensions"]
    assert pd["alpha_matches_superstring"]   # alpha = 10 = d_string
    assert pd["omega_matches_spacetime"]     # omega = 4 = d_SM
    assert pd["decomposition_verified"]      # 10 - 4 = 6 compact dims
    assert pd["compact_dims"] == 6


def test_doubly_extremal():
    p = lovasz_independence_clique_packet()
    de = p["doubly_extremal_certificate"]
    assert de["alpha_achieves_lovasz_bound"]
    assert de["omega_achieves_lovasz_bound"]
    assert de["both_bounds_tight"]


def test_vertex_partition():
    p = lovasz_independence_clique_packet()
    vp = p["vertex_partition"]
    assert vp["color_classes"] == 4
    assert vp["vertices_per_class"] == 10
    assert vp["total_vertices"] == 40
