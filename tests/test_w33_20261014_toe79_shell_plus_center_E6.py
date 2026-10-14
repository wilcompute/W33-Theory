"""Canonical W33 shell degree 8, 9 H27 center fibers, GQ(2,4) cubic completion."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe79_shell_plus_center_E6 import certificate

def test_canonical_opposite_shell_plus_nine_centers_equals_E6_cubic_incidence():
    c=certificate()
    assert c["status"]=="PASS_TOE79_CANONICAL_W33_SHELL_PLUS_CENTER_E6_COMPLETION"
    assert c["W33_center_point"]==1
    assert len(c["W33_opposite_point_indices"])==27
    assert c["opposite_shell_induced_W33_collinearity_edges"]==108
    assert c["opposite_shell_degree"]==8
    assert c["opposite_shell_triangles"]==36
    assert c["Heisenberg_center_C3_fibers"]==9
    assert c["Heisenberg_center_added_edges"]==27
    assert c["completed_cubic_E6_27_line_edges"]==135
    assert c["completed_GQ24_degree"]==10
    assert c["completed_45_tritangent_triples"]==45
    assert c["point_stabilizer_preserves_completed_E6_graph"]
    assert c["point_stabilizer_preserves_nine_center_fibers"]
    assert len(c["native_shell_36_triangles"])==36
    assert len(c["native_center_9_tritangent_fibers"])==9
