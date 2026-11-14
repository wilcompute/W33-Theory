"""Regression of all 180 minimal-charge twistor fibers and 2-designs."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_stabilizer_twistor_2design as T

def test_all_stabilizer_fibers_and_twistor_moments():
    result=T.main()
    assert result["status"]=="PASS_EXACT_STABILIZER_TWISTOR_CP7_TO_HP3_2DESIGN"
    assert result["lagrangian_three_qubit_stabilizer_bases"]==135
    assert result["complex_projective_stabilizer_states"]==1080
    assert result["quaternionic_projective_integral_BPS_charge_points"]==180
    assert result["fiber_cardinality"]==6
    assert result["each_fiber_exact_projective_2design"]
    assert result["packet_clifford_orbit_sizes_on_180_charges"]==[180]
    assert result["exact_discrete_overlap_census"]=={"0.0":540,"0.5":2160}

if __name__=="__main__":
    test_all_stabilizer_fibers_and_twistor_moments()
    print("PASS 1/1 (135 lagrangians, 1080 states, 180 exact twistor 2-designs)",flush=True)
