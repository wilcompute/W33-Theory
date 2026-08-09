import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def test_borel_overgroup_interval_and_obstruction_axes():
    a = load("PART_W33_PASS4528_BOREL_OVERGROUP_SPLITTING.json")
    assert a["group_order"] == 25920
    assert [r["double_coset_size"] for r in a["H_double_cosets"]] == [162,486,486,1458,1458,4374,4374,13122]
    assert [r["generated_overgroup"] for r in a["H_double_cosets"] if r["split"]] == ["Borel_flag_162"]
    b = load("PART_W33_PASS4529_RANK2_BUILDING_OBSTRUCTION_COMPASS.json")
    assert b["class_coordinates"] == {"fixed_line":[1,0], "sum":[0,1], "second":[1,1]}
    assert b["restriction_kernels"]["incident_Borel_162"]["dimension"] == 2


def test_q5q_symbolic_and_compiler():
    q = load("PART_W33_PASS4530_Q5Q_SYMBOLIC_PROTECTED_LAW.json")
    assert q["q3_anchor"] == {"h":279,"rho":70,"radical":209,"protected":70}
    assert q["Q5q_theorem"]["protected_dimension"] == "rho(q)=rank_2(N^T N)"
    c = load("PART_W33_PASS4531_FLAG_GAUGE_COMPILER.json")
    assert c["primitive_operations"] == 42
    assert c["schedule_depth"] == c["depth_lower_bound"] == 9
    assert c["depth_optimal_in_model"] is True


def test_edge_locality_nine_layer_and_eight_state_spectrum():
    e = load("PART_W33_PASS4532_BOREL_EDGE_LOCAL_CELL_FUSION.json")
    assert [r["orbit_size"] for r in e["protected_edge_orbits"]] == [3,3,9,9,27,27,81,81]
    assert e["edge_location_totals"] == {"internal":24,"boundary":108,"exterior":108}
    s = load("PART_W33_PASS4533_BOREL_POWER_THREE_STAIRCASE.json")
    assert s["vertex_staircase"]["orbit_sizes"] == [1,3,9,27]
    assert s["stabilizer_staircase"] == [54,18,6,2]
    t = load("PART_W33_PASS4534_LOCAL_EDGE_TOMOGRAPHY_NINE_LAYER.json")
    assert t["protected_H10_dimension"] == 10
    assert t["edge_image_span_dimension"] == 9
    assert t["local_ranks"]["center_spokes_12"] == 9
    assert t["minimal_local_spoke_basis_size"] == 9
    x = load("PART_W33_PASS4535_BOREL_EDGE_TRANSFER_QUOTIENT.json")
    assert x["full_edge_graph"]["distinct_spectrum"] == [22,12,6,-2]
    assert x["quotient_eigenvalue_multiplicities"] == {"22":1,"12":2,"6":1,"-2":4}
    assert all(sum(row) == 22 for row in x["equitable_quotient_matrix"])


def test_manuscript_and_public_chains_are_live():
    p4519 = (ROOT / "analysis/PASS4519_flag_borel_sylow3_normalizer_insert.tex").read_text()
    assert r"\input{analysis/PASS4528_4535_borel_building_compiler_edge_insert}" in p4519
    insert = (ROOT / "analysis/PASS4528_4535_borel_building_compiler_edge_insert.tex").read_text()
    for p in range(4528,4536):
        assert f"Pass {p}" in insert or f"Pass~{p}" in insert
    page = (ROOT / "docs/apartment-obstruction-cohomology-gq.html").read_text()
    assert "Pass 4528" in page and "Bonkers #3" in page
    card = (ROOT / "analysis/PASS4528_4535_borel_building_compiler_edge_index_insert.html").read_text()
    assert 'id="pass4528-4535-borel-building-compiler-edge"' in card
