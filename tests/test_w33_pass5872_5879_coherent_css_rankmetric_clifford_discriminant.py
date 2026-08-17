from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5872_5879_COHERENT_CSS_RANKMETRIC_CLIFFORD_DISCRIMINANT.json"
PRODUCER = ROOT / "analysis" / "w33_pass5872_5879_coherent_css_rankmetric_clifford_discriminant.py"


def load():
    return json.loads(CERT.read_text())


def test_exact_producer_replays_frozen_certificate():
    expected = load()
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True, capture_output=True, text=True)
    assert load() == expected


def test_coherent_closure_and_wedderburn():
    d=load()["pass_5872_joint_coherent_closure"]
    assert d["refinement_counts"] == [5,15,15]
    assert d["orthogonal_group_order"] == 72
    assert d["wl_classes_equal_Oplus_orbitals"] is True
    assert d["center_dimension"] == 4
    assert d["complex_commutant_wedderburn"] == "M3(C) + M2(C) + C + C"


def test_css_no_go_and_radon_replacement_bridge():
    d=load()
    c=d["pass_5873_css_interface_nogo"]
    r=d["pass_5876_discriminant_radon_exact_sequence"]
    assert c["global_q5_footprint_check_code"] == [156,65,12]
    assert c["supported_embedding_into_check_code"] is False
    assert c["any_12_coordinate_shortening_dimension_upper_bound"] == 1
    assert r["kernel_equals_Reye_code_objectwise"] is True
    assert r["image_equals_line_Gram_radical"] is True
    assert r["quotient_is_det_Pauli_9plus6_objectwise"] is True


def test_allfield_rankmetric_graph_and_clifford_lift():
    d=load()
    g=d["pass_5874_allfield_unit_difference_graph"]
    assert g["examples"]["2"]["srg"] == [16,6,2,2]
    assert g["examples"]["3"]["srg"] == [81,48,27,30]
    assert g["examples"]["7"]["srg"] == [2401,2016,1687,1722]
    assert g["q2_order"] == 1152
    c=d["pass_5875_clifford_lift"]
    assert c["relative_group_order"] == 72
    assert c["Sp4_2_order"] == 720
    assert c["Clifford_preimage_projective_order"] == 1152


def test_three_outside_box_probes():
    d=load()
    f=d["pass_5877_oddq_determinant_character_fourier"]
    assert f["prime_exact_anchors"]["3"]["scalar"] == -9
    assert f["prime_exact_anchors"]["5"]["scalar"] == 25
    assert f["prime_exact_anchors"]["7"]["scalar"] == -49
    m=d["pass_5878_q3_max_clique_orbits"]
    assert m["maximum_clique_size"] == 9
    assert m["full_rank_isometry_group_orbits_on_9_cliques"] == [162,486]
    assert m["affine_span_dimensions_by_orbit"] == {"162":2,"486":4}
    r=d["pass_5879_reye_dual_min_shell_reconstruction"]
    assert r["Cdual"] == [12,8,3]
    assert r["dual_16_weight3_supports_equal_original_Reye_lines"] is True
    assert r["line_heavy_intersection_spectrum"] == {"0":48,"2":144}
