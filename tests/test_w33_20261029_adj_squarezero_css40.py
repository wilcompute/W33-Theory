"""W33 binary adjacency CSS geometry: six independent executable assertions."""
import pytest
from analysis.w33_20261029_adj_squarezero_css40 import verify,adjacency,lines,rank

@pytest.fixture(scope="module")
def c():return verify()

def test_srg_square_zero(c):
    assert c["parameters"]=={"v":40,"degree":12,"lambda":2,"mu":4,"edges":240,"lines":40}
    assert c["A_squared_mod2_is_zero"] and c["binary_adjacency_rank"]==16

def test_css_parameters_and_distance(c):
    assert c["CSS"]=={"n":40,"k":8,"d":6,"X_checks":16,"Z_checks":16,
                       "X_distance":6,"Z_distance":6}
    assert c["kernel_low_weight_counts"]=={"1":0,"2":0,"3":0,"4":0,"5":0,"6":240}

def test_full_stabilizer_space_enumerator(c):
    assert c["rowspace_weight_enumerator"]=={
       "0":1,"8":45,"12":1120,"16":15570,"20":32064,
       "24":15570,"28":1120,"32":45,"40":1}

def test_minimal_logicals_are_intersecting_line_hexads(c):
    assert c["minimum_logical_hexads"]==240
    assert c["hexads_per_vertex"]==36

def test_old_incidence_versus_new_point_adjacency(c):
    assert c["point_line_incidence_rank"]==25
    assert c["B_BT_mod2_equals_A"]

def test_graph_state_cut_entropy(c):
    assert c["graph_state_entanglement"]=={
        "line_cut_ebits":4,"hexad_cut_ebits":5,"global_binary_adjacency_rank_ceiling":16}
