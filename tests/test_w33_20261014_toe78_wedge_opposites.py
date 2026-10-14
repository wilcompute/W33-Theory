"""TOE78 all-480 local Levi wedges, 27-cycle opposite-point bijection."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe78_wedge_opposites import certificate
def test_native_480_two_arcs_each_have_27_distinct_opposite_midpoint_octagons():
    c=certificate()
    assert c["status"]=="PASS_TOE78_ALL_W33_WEDGES_27_OPPOSITE_BIJECTION"
    assert c["incidence_two_arc_count"]==480
    assert c["two_arc_bipartition_classes"]=={"point":240,"line":240}
    assert c["every_wedge_octagons"]==27
    assert c["wedge_octagon_incidences"]==c["octagon_wedge_incidences"]==12960
    assert c["all_480_wedges_verified_distinct_midpoint_bijections"]
    assert len(c["chosen_theta_chord_opposite_map"]["native_shared_octagon_to_canonical_opposite_vertex"])==27
