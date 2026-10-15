"""Native tritangent qubit/qutrit code regression."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261015_toe81_native_tritangent_css import certificate,rank_mod,gf2_rank

def test_finite_field_elimination():
    assert rank_mod([[1,0,1],[0,1,1],[1,1,2]],3)==2
    assert rank_mod([[1,0],[0,1]],3)==2
    assert rank_mod([[1,1],[2,2]],3)==1
    assert gf2_rank([0b011,0b101,0b110])==2

def test_native_tritangent_topology_and_binary_css():
    c=certificate()
    assert c["status"]=="PASS_TOE81_NATIVE_E6_TRITANGENT_CSS_HOMOLOGY"
    t=c["chain_complex"]
    assert (t["vertices"],t["edges"],t["triangles"])==(27,135,45)
    assert t["betti"]==[1,64,0]
    assert t["fundamental_group"]=="free group F_64"
    assert t["collapsed_graph_edges"]==90
    assert len(c["explicit_binary_logical_Z_generator_edge_indices"])==64
    b=c["binary_css"]
    assert b["logical_qubits"]==64
    assert (b["X_distance"],b["Z_distance"],b["minimum_distance"])==(2,4,2)
    assert b["number_of_weight2_X_logical_supports"]==135
    assert b["number_of_weight4_Z_logical_supports"]==1080
    assert len(c["explicit_binary_distance2_X_witness_edge_indices"])==2
    assert len(c["explicit_binary_distance4_Z_witness_edge_indices"])==4

def test_ternary_qutrit_and_holonomy_moduli():
    c=certificate()
    assert c["ternary_css"]=={
        "physical_edge_qutrits":135,"logical_qutrits":64,
        "X_distance":2,"Z_distance":4,
        "oriented_chain_identity_checked":True}
    assert c["free_holonomy_moduli"]["abelian_U1"]=="(U(1))^64"
    assert len(c["tritangent_vertex_triples"])==45
    assert len(c["edge_index_to_native_octagon_pair"])==135
