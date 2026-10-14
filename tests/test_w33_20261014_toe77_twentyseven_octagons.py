"""Full PGSp stabilizer audit of 27 common theta-chord W33 octagons."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_twentyseven_octagons import certificate
def test_two_chord_27_incidence_does_not_fake_H27_equivariance():
    c=certificate()
    assert c["status"]=="PASS_TOE77_TWO_CHORD_27_OCTAGON_STABILIZER_AUDIT"
    assert c["octagons_per_native_flag_edge"]==[81,81]
    assert c["octagons_containing_both_edges"]==27
    assert c["octagons_containing_at_least_one"]==135
    assert c["PGSp_group_order"]%c["unordered_two_flag_pair_orbit_size"]==0
    assert c["PGSp_group_order"]//c["unordered_two_flag_pair_orbit_size"]==c["unordered_pair_stabilizer_order"]
    assert sum(c["stabilizer_orbit_sizes_on_27_common_octagons"])==27
