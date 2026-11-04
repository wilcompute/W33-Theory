"""Independent five-front falsifier regression. Finite mathematical claims only."""
from pathlib import Path
import importlib.util
import math
import pytest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis"/"toe_20261103_fivefront_independent_controls.py"
spec=importlib.util.spec_from_file_location("fivefront",SOURCE)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

@pytest.fixture(scope="module")
def r():
    return mod.test()

def test_continuum(r):
    assert r["continuum"]["flag_graph_diameter_histogram"]=={4:160}
    assert r["continuum"]["graph_degree"]==6
    assert r["continuum"]["nonzero_band_condition_number"]>100000

def test_symmetry(r):
    s=r["symmetry"]
    assert s["symplectic_transvections"]==40
    assert s["selected_basis_stabilizers"]==0
    assert s["min_relative_H_change"]>0.5

def test_gravity_boundary(r):
    g=r["gravity_nonclosure"]
    assert g["gauss_norm"]==0
    assert g["bracket_on_gauss_zero"]==-7

def test_e6_anomaly_control(r):
    a=r["chiral_anomaly"]
    assert all(a[k]==0 for k in ("U1_gravitational_anomaly","U1_cubic_anomaly",
        "SO10_squared_U1_anomaly","SU5_cubic_anomaly"))
    assert "27bar" in a["boundary"]

def test_hardware_and_flux(r):
    h=r["hardware"]
    assert h["nonzero_undirected_couplings"]==1883
    assert h["positive_couplings"]==871
    assert h["negative_couplings"]==1012
    assert h["signed_triangles_total"]==5250
    assert h["pi_flux_triangles"]==780
    assert h["pi_flux_triangle_witness"]["hoppings"]==[-1,-2,-1]
    assert all(math.isclose(x["leakage"],x["leading_order"],rel_tol=.02)
               for x in h["time_evolution"])
