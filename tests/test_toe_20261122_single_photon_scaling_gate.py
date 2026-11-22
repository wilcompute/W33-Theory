"""Regression for the sixth independent single-photon scaling firewall."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261122_single_photon_scaling_gate as scaling

def test_generic_one_photon_10_qubit_mesh_resource_census():
    result=scaling.verify()
    a=result["census"]
    assert a[1]["required_orthogonal_modes"]==4
    assert a[-1]["required_orthogonal_modes"]==1024
    assert a[-1]["generic_SU_d_real_parameters"]==1048575
    assert a[-1]["standard_Clements_two_mode_cells"]==523776
