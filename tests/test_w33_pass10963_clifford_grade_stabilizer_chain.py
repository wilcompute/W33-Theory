import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10963_clifford_grade_stabilizer_chain.py"
CERT = ROOT / "data/w33_pass10963_clifford_grade_stabilizer_chain.json"
EXACT = ROOT / "data/w33_pass10963_exact_stabilizer_generators.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert load()["status"] == (
        "PASS_CLIFFORD_GRADE_STABILIZER_TETRAHEDRAL_CHAIN"
    )
def test_exact_stabilizer_chain():
    s = load()["packet_stabilizers"]
    assert s["V10"]["group"] == "D8"
    assert s["V10"]["order"] == 8
    assert s["V10"]["exact"] is True
    assert s["P19"]["group"] == "QD16 = SD16"
    assert s["P19"]["order"] == 16
    assert s["P19"]["clock_normalizer"] is True
    assert s["P19"]["sylow_2_subgroup"] is True
    assert s["chain"] == "C8 < QD16; D8 < QD16 < GL(2,3)"


def test_cores_and_quotients():
    q = load()["cores_and_quotients"]
    assert q["core_V10_stabilizer_order"] == 2
    assert q["core_V10_stabilizer"] == "central C2"
    assert q["V10_packet_action_image"] == "S4"
    assert q["V10_packet_orbit_size"] == 6
    assert q["core_P19_stabilizer_order"] == 8
    assert q["core_P19_stabilizer"] == "Q8"
    assert q["P19_packet_action_image"] == "S3"
    assert q["P19_packet_orbit_size"] == 3
def test_tetrahedral_packet_dictionary():
    t = load()["tetrahedral_dictionary"]
    assert len(t["four_vertices"]) == 4
    assert t["equivariant"] is True
    assert len(t["coset_edge_labels"]) == 6
    assert len(t["coset_matching_labels"]) == 3
    assert sorted(len(x) for x in t["coset_pairs"]) == [2, 2, 2]
    assert "six edges" in t["six_V10_packets"]
    assert "perfect matchings" in t["three_P19_packets"]


def test_packet_overlap_census_and_common_hull():
    p = load()["packet_intersections"]
    assert p["V10_pair_intersection_histogram"] == {"0": 12, "1": 3}
    assert p["V10_cross_gram_rank_histogram"] == {"1": 3, "9": 12}
    assert p["P19_pair_intersection_histogram"] == {"8": 3}
    assert p["P19_cross_gram_rank_histogram"] == {"9": 3}
    assert p["common_orbit_hull_dimension"] == 33
    assert p["V10_orbit_hull_equals_P19_orbit_hull"] is True
    assert p["each_P19_contains_exactly_two_V10_packets"] is True
def test_exact_generator_certificate():
    x = json.loads(EXACT.read_text(encoding="utf-8"))
    assert x["field"] == "Q(i,sqrt(2))"
    assert x["b_preserves_all_10_vectors"] is True
    assert x["b_preserves_all_19_packet_generators"] is True
    assert x["outsider_preserves_vector_generators"] == 0
    assert x["outsider_preserves_packet_generators"] == 0
    assert x["exact_zero_tests"] is True


def test_gap_crosscheck_is_frozen():
    text = (ROOT / "analysis/w33_pass10963_group_structure.g").read_text(
        encoding="utf-8"
    )
    assert "Normalizer(G,C8)" in text
    assert "Core(G,H19)" in text
    assert "Core(G,H10)" in text
    assert "IntermediateSubgroups(G,H10)" in text
def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(
        encoding="utf-8"
    )
    assert docs.count('id="pass10963-clifford-grade-tetrahedron"') == 1
    assert tail.count(
        "PASS10963_CLIFFORD_GRADE_STABILIZER_CHAIN_INSERT}%"
    ) == 1
