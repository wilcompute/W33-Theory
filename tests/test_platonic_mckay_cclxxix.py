"""
Tests for Part CCLXXIX: Platonic Solids, McKay Correspondence, and the W(3,3) ADE Atlas
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exploration.PART_CCLXXIX_PLATONIC_MCKAY_BRIDGE import (
    verify_tetrahedron_w33,
    verify_cube_octahedron_w33,
    verify_icosahedron_w33,
    verify_dodecahedron_w33,
    verify_platonic_euler_characteristic,
    verify_rotation_group_orders,
    verify_binary_tetrahedral_mckay,
    verify_binary_octahedral_mckay,
    verify_binary_icosahedral_mckay,
    verify_e6_tilde_kac_labels,
    verify_e7_tilde_kac_labels,
    verify_e8_tilde_kac_labels,
    verify_coxeter_numbers_e_series,
    verify_coxeter_numbers_small_rank,
    verify_platonic_duality,
    verify_mckay_e_series_chain,
    verify_transport_icosahedron_link,
    verify_polyhedral_product_identities,
    verify_kac_label_max_values,
    verify_icosa_as_binary_icosahedral_quotient,
    verify_coxeter_label_ade_completeness,
    verify_solid_angle_identity,
    verify_vertex_counts_w33,
    verify_edge_counts_w33,
    verify_binary_group_kac_sq_tower,
    verify_mckay_aut_order_connections,
    verify_icosa_dodeca_subgraph_params,
    build_cclxxix_bridge_summary,
)


def test_verify_tetrahedron_w33():
    ok, data = verify_tetrahedron_w33()
    assert ok, f"tetrahedron_w33 failed: {data}"


def test_verify_cube_octahedron_w33():
    ok, data = verify_cube_octahedron_w33()
    assert ok, f"cube_octahedron_w33 failed: {data}"


def test_verify_icosahedron_w33():
    ok, data = verify_icosahedron_w33()
    assert ok, f"icosahedron_w33 failed: {data}"


def test_verify_dodecahedron_w33():
    ok, data = verify_dodecahedron_w33()
    assert ok, f"dodecahedron_w33 failed: {data}"


def test_verify_platonic_euler_characteristic():
    ok, data = verify_platonic_euler_characteristic()
    assert ok, f"platonic_euler_characteristic failed: {data}"


def test_verify_rotation_group_orders():
    ok, data = verify_rotation_group_orders()
    assert ok, f"rotation_group_orders failed: {data}"


def test_verify_binary_tetrahedral_mckay():
    ok, data = verify_binary_tetrahedral_mckay()
    assert ok, f"binary_tetrahedral_mckay failed: {data}"


def test_verify_binary_octahedral_mckay():
    ok, data = verify_binary_octahedral_mckay()
    assert ok, f"binary_octahedral_mckay failed: {data}"


def test_verify_binary_icosahedral_mckay():
    ok, data = verify_binary_icosahedral_mckay()
    assert ok, f"binary_icosahedral_mckay failed: {data}"


def test_verify_e6_tilde_kac_labels():
    ok, data = verify_e6_tilde_kac_labels()
    assert ok, f"e6_tilde_kac_labels failed: {data}"


def test_verify_e7_tilde_kac_labels():
    ok, data = verify_e7_tilde_kac_labels()
    assert ok, f"e7_tilde_kac_labels failed: {data}"


def test_verify_e8_tilde_kac_labels():
    ok, data = verify_e8_tilde_kac_labels()
    assert ok, f"e8_tilde_kac_labels failed: {data}"


def test_verify_coxeter_numbers_e_series():
    ok, data = verify_coxeter_numbers_e_series()
    assert ok, f"coxeter_numbers_e_series failed: {data}"


def test_verify_coxeter_numbers_small_rank():
    ok, data = verify_coxeter_numbers_small_rank()
    assert ok, f"coxeter_numbers_small_rank failed: {data}"


def test_verify_platonic_duality():
    ok, data = verify_platonic_duality()
    assert ok, f"platonic_duality failed: {data}"


def test_verify_mckay_e_series_chain():
    ok, data = verify_mckay_e_series_chain()
    assert ok, f"mckay_e_series_chain failed: {data}"


def test_verify_transport_icosahedron_link():
    ok, data = verify_transport_icosahedron_link()
    assert ok, f"transport_icosahedron_link failed: {data}"


def test_verify_polyhedral_product_identities():
    ok, data = verify_polyhedral_product_identities()
    assert ok, f"polyhedral_product_identities failed: {data}"


def test_verify_kac_label_max_values():
    ok, data = verify_kac_label_max_values()
    assert ok, f"kac_label_max_values failed: {data}"


def test_verify_icosa_as_binary_icosahedral_quotient():
    ok, data = verify_icosa_as_binary_icosahedral_quotient()
    assert ok, f"icosa_as_binary_icosahedral_quotient failed: {data}"


def test_verify_coxeter_label_ade_completeness():
    ok, data = verify_coxeter_label_ade_completeness()
    assert ok, f"coxeter_label_ade_completeness failed: {data}"


def test_verify_solid_angle_identity():
    ok, data = verify_solid_angle_identity()
    assert ok, f"solid_angle_identity failed: {data}"


def test_verify_vertex_counts_w33():
    ok, data = verify_vertex_counts_w33()
    assert ok, f"vertex_counts_w33 failed: {data}"


def test_verify_edge_counts_w33():
    ok, data = verify_edge_counts_w33()
    assert ok, f"edge_counts_w33 failed: {data}"


def test_verify_binary_group_kac_sq_tower():
    ok, data = verify_binary_group_kac_sq_tower()
    assert ok, f"binary_group_kac_sq_tower failed: {data}"


def test_verify_mckay_aut_order_connections():
    ok, data = verify_mckay_aut_order_connections()
    assert ok, f"mckay_aut_order_connections failed: {data}"


def test_verify_icosa_dodeca_subgraph_params():
    ok, data = verify_icosa_dodeca_subgraph_params()
    assert ok, f"icosa_dodeca_subgraph_params failed: {data}"


def test_build_cclxxix_bridge_summary():
    summary = build_cclxxix_bridge_summary()
    assert summary["all_checks_pass"] is True
    assert summary["total_checks"] == 237
    assert summary["part"] == "CCLXXIX"
