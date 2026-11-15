"""Pass 12676: W(E6) stabiliser of the F_8 configuration, branching controls, tritangent orbits, face size."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))
C8 = 2.4985086466880784


def test_W_E6_stabiliser_and_controls():
    d = load("w33_f8_E6_configuration_group.json")
    assert d["W_E6_order"] == 51840 and d["config_stabiliser_order"] == 18
    assert d["config_stabiliser_element_orders"] == {"1": 1, "2": 9, "3": 2, "9": 6}
    assert d["config_stabiliser_line_orbits"] == [9, 9, 9]
    assert d["stab_line_1_10_16"] == 1920 and d["n_steiner_trihedral_pairs"] == 120 and d["stab_trinification_triple"] == 1296
    assert d["stab_F8_line_partition"] == 54 and not d["F8_partition_is_trinification"]


def test_tritangent_orbits():
    d = load("w33_f8_E6_configuration_group.json")["other_orbits"]
    f8 = [r for r in d if r["size"] == 9 and abs(r["min_c"] - C8) < 1e-6]
    assert len(f8) == 3 and sum(r["ours"] for r in f8) == 1
    mub = [r for r in d if r["weights"] == [[1, 63]]]
    assert len(mub) == 3 and all(abs(r["min_c"] - 7) < 1e-6 for r in mub)


def test_face_size():
    d = load("w33_f8_codespace_deg8_certificate_1249254323_500000000.json")
    assert d["certified"] and d["face_total"] == 766
