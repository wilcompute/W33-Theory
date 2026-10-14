"""TOE77 exact 216-stabilizer and possible Heisenberg H27 action."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_H27_shared_octagon_group import certificate
def test_actual_H27_classification_not_numerical_coincidence():
    c=certificate()
    assert c["status"]=="PASS_TOE77_NATIVE_27_OCTAGON_EXPLICIT_GROUP_STRUCTURE"
    assert c["pair_stabilizer_order_in_PGSp"]==216
    assert c["pair_orbit_size"]==240
    assert c["transitive_on_27_shared_octagons"]
    assert 216%c["induced_faithful_permutation_group_order"]==0
    assert sum(int(v) for v in c["group_order_histogram"].values())==c["induced_faithful_permutation_group_order"]
    if c["selected_Sylow27_is_extraspecial_Heisenberg_H27"]:
        assert c["selected_Sylow27_center_order"]==3
        assert c["selected_Sylow27_regular_on_27_octagons"]
        assert c["selected_Sylow27_element_order_histogram"]=={1:1,3:26}
