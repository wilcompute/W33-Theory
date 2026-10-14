"""All 6,480 canonical decorated native W33 octagons and opposite-point torsors."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe79_canonical_antipode_octagon import certificate
def test_all_40_points_six_flag_pairs_27_opposite_points_and_full_symplectic_orbit():
    c=certificate()
    assert c["status"]=="PASS_TOE79_CANONICAL_27_OPPOSITE_POINT_OCTAGON_GQ_MAP"
    assert c["pair_octagon_keys"]==240
    assert c["each_incident_flag_pair_octagons"]==27
    assert c["rooted_point_octagon_pair_antipode_states"]==6480
    assert c["complete_native_PGSp_orbit_size"]==6480
    assert c["stabilizer_order_chain"]=={
        "PGSp":51840,"point":1296,
        "point_plus_incident_line_pair":216,
        "point_plus_incident_line_pair_plus_noncollinear_point":8}
    assert c["theta_native_point"]==1 and c["theta_native_chords"]==[5,6]
    assert len(c["theta_opposite_point_to_octagon_bijection"])==27
    assert len({r["opposite_W33_point"] for r in c["theta_opposite_point_to_octagon_bijection"]})==27
