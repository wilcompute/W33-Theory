"""Cross-check exact 27 shared-octagon cubic-surface incidence against independent E6 carrier."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe78_octagon_cubic_surface import certificate,independent_cubic_geometry

def test_27_native_octagons_unique_216_invariant_cubic_surface_E6_graph():
    c=certificate()
    assert c["status"]=="PASS_TOE78_NATIVE_OCTAGON_H27_D8_CUBIC_SURFACE_GRAPH"
    assert c["unique_216_invariant_SRG_27_10_1_5"]
    assert c["native_SRG_edges"]==135
    assert c["native_cubic_tritangents"]==45
    assert c["native_cubic_double_sixes"]==36
    assert c["native_cubic_graph_adjacency_spectrum"]=={"10":1,"1":20,"-5":6}
    assert len(c["native_to_independent_E6_cubic_line_index_isomorphism"])==27
    assert len(set(c["native_to_independent_E6_cubic_line_index_isomorphism"]))==27
    assert c["antiunitary_group_boundary"]["D8_elements_inverting_H27_center"]==4
    assert c["antiunitary_group_boundary"]["D8_elements_preserving_H27_center"]==4

def test_independent_quadratic_F2_6_graph_and_tritangents():
    G,T,D=independent_cubic_geometry()
    assert G.number_of_nodes()==27
    assert G.number_of_edges()==135
    assert len(T)==45 and len(D)==36
