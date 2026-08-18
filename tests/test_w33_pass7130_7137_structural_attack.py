import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS7130_7137_STRUCTURAL_ATTACK.json"
Q7 = ROOT / "data" / "PART_W33_Q7_PARTIAL_OVOID_33.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_pass7130_7137_certificate_frontier():
    d = load(CERT)
    assert d["status"] == "PASS"

    p = d["pass_7130_blocker_deficiency"]
    assert p["q9_model"] == {
        "outside_x": 769,
        "witness_y": 51,
        "binary_variables": 820,
        "outside_edge_constraints": 32310,
        "blocker_implications": 4590,
    }
    assert "unrestricted" in p["proved_radius"].lower()
    assert "no alpha=51 claim" in p["proved_radius"]

    s = d["pass_7131_stabilizer"]
    assert s["order"] == 2
    assert s["isomorphism"] == "C2"
    assert s["generator_square"] == "I"
    assert s["similitude_multiplier"] == 2
    assert s["inside_orbits"] == "1 + 25*2"
    assert s["unique_fixed_witness_point"] == 80
    assert s["semilinear_frame_match_counts"] == {
        "id_linear": 51,
        "id_frobenius": 6,
        "pi_linear": 51,
        "pi_frobenius": 6,
    }

    g = d["pass_7132_gram_compression"]
    assert g["verified_entries"] == 2601
    assert g["anchor_graph_indices"] == [22, 24, 78, 95]
    assert "198 GF(9) variables" in g["target_52_variable_reduction"]

    b = d["pass_7133_blocker_orbits"]
    assert b["inside_fingerprint_classes"] == 26
    assert b["outside_fingerprint_classes"] == 394
    assert b["outside_fingerprint_class_sizes"] == {"1": 19, "2": 375}
    assert b["fingerprints_equal_C2_orbits"] is True

    q7 = d["pass_7134_q7_control"]
    assert q7["stored_size"] == 33
    assert q7["zero_blockers"] == 0
    assert q7["one_blockers"] == 0
    assert q7["stabilizer_order"] == 2
    assert q7["inside_orbits"] == "1 + 16*2"

    f = d["pass_7135_frobenius_union"]
    assert f["intersection"] == 4
    assert f["cross_graph_sides"] == [47, 47]
    assert f["perfect_matching"] == 47
    assert f["alpha_of_union"] == 51

    c = d["pass_7136_quadratic_character"]
    assert c["q9"]["matrix_symmetry"] == "symmetric"
    assert c["q9"]["rank_over_Q"] == 51
    assert c["q7"]["matrix_symmetry"] == "skew-symmetric"
    assert c["q7"]["rank_over_Q"] == 32

    l = d["pass_7137_fixed_lines"]
    assert l["q9_fixed_projective_points"] == 20
    assert l["each_line_size"] == 10
    assert l["each_line_totally_isotropic"] is True
    assert l["swap_fixed_pair"] == [80, 40]
    assert 40 in l["eigenspace_lines"]["lambda_minus1"]
    assert 80 in l["eigenspace_lines"]["lambda_minus1"]


def test_q7_control_witness_is_frozen_and_scoped():
    d = load(Q7)
    assert d["q"] == 7
    assert d["size"] == 33
    assert len(d["points"]) == 33
    assert len(d["point_indices"]) == 33
    assert len(set(d["point_indices"])) == 33
    assert d["verified_pairwise_noncollinear"] is True
    assert d["zero_blockers"] == 0
    assert d["one_blockers"] == 0
    assert "proves only existence" in d["scope"]


def test_shared_manifest_reaches_the_new_insert():
    manifest = (ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex").read_text(encoding="utf-8")
    needle = r"\input{analysis/PASS7130_7137_structural_attack_insert}%"
    assert manifest.count(needle) == 1
