from __future__ import annotations

from analysis.w33_q4_tomotope_reye_double_cover import (
    q4_tomotope_reye_double_cover_packet,
)


PACKET = q4_tomotope_reye_double_cover_packet()


def test_mclxxxii_q4_source_incidence_graph() -> None:
    source = PACKET["q4_source"]

    assert source["face_nodes"] == 24
    assert source["edge_nodes"] == 32
    assert source["incidences"] == 96
    assert source["degree_profile"] == {3: 32, 4: 24}
    assert source["component_sizes"] == [56]


def test_mclxxxii_antipodal_quotient_has_reye_size_and_lift_multiplicity() -> None:
    quotient = PACKET["antipodal_quotient"]

    assert quotient["translation"] == (1, 1, 1, 1)
    assert quotient["face_orbits"] == 12
    assert quotient["edge_orbits"] == 16
    assert quotient["incidences"] == 48
    assert quotient["degree_profile"] == {3: 16, 4: 12}
    assert quotient["component_sizes"] == [28]
    assert quotient["incidence_lift_multiplicity_profile"] == {2: 48}
    assert quotient["isomorphic_to_reye"] is True


def test_mclxxxii_reye_model_is_12_4_16_3() -> None:
    reye = PACKET["reye_model"]

    assert reye["points"] == 12
    assert reye["lines"] == 16
    assert reye["incidences"] == 48
    assert reye["point_line_profile"] == "12_4, 16_3"
    assert reye["degree_profile"] == {3: 16, 4: 12}
    assert reye["component_sizes"] == [28]


def test_mclxxxii_tomotope_locks() -> None:
    lock = PACKET["tomotope_lock"]

    assert lock["vertices"] == 4
    assert lock["edges"] == 12
    assert lock["triangles"] == 16
    assert lock["cells"] == 8
    assert lock["edge_triangle_medial_incidences"] == 48
    assert lock["automorphism_group_order"] == 96
    assert lock["flags"] == 192
    assert lock["q4_to_medial_cover_degree"] == 2
    assert lock["q4_incidence_equals_automorphism_group_order"] is True
    assert lock["tomotope_flags_over_q4_incidence"] == 2


def test_mclxxxii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 20
    assert all(PACKET["checks"].values())
