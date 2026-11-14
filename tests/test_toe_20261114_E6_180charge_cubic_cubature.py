"""Regression: exact signed E6 cubic reconstructed by 180 integral charges."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261114_E6_180charge_cubic_cubature as C

def test_full_cubic_cubature_and_fourth_incidence_moments():
    cert=C.main()
    assert cert["status"]=="PASS_EXACT_180CHARGE_SIGNED_E6_CUBIC_CUBATURE"
    assert cert["charges_positive_unit_cubic"]==180
    assert cert["tritangents"]==45
    assert cert["Schlaefli_two_section_edges"]==135
    assert cert["coordinate_degree"]==5
    assert cert["exact_random_integer_cubature_trials"]==40
    assert cert["spherical_design_strength"]==2
    assert not cert["is_spherical_3design"]

if __name__=="__main__":
    test_full_cubic_cubature_and_fourth_incidence_moments()
    print("PASS 1/1 (180 charges reconstruct all signed cubic and incidence moments)",flush=True)
