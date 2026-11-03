"""Regression checks for six independently executable five-front TOE packets.

Run on the authorized local checkout; no external network or API required.
"""
from __future__ import annotations
import json
import math
import subprocess
import sys
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 "2026_11_03_pascal_w33_s3_holonomy.py",
 "2026_11_03_pascal_w33_triangle_wilson.py",
 "2026_11_03_pascal_e8_a2_root_boundary.py",
 "2026_11_03_pascal_two_scalar_resolvent_rg.py",
 "2026_11_03_pascal_scale_identifiability.py",
 "2026_11_03_pascal_photonic_falsifier.py",
]
DATA={
 "holonomy":"2026_11_03_pascal_w33_s3_holonomy.json",
 "wilson":"2026_11_03_pascal_w33_triangle_wilson.json",
 "e8":"2026_11_03_pascal_e8_a2_root_boundary.json",
 "resolvent":"2026_11_03_pascal_two_scalar_resolvent_rg.json",
 "scale":"2026_11_03_pascal_scale_identifiability.json",
 "photonic":"2026_11_03_pascal_photonic_falsifier.json",
}

@pytest.fixture(scope="module")
def certificates():
    for name in SCRIPTS:
        result=subprocess.run([sys.executable,str(ROOT/"analysis"/name)],
               capture_output=True,text=True,cwd=str(ROOT),timeout=90)
        assert result.returncode==0,(name,result.stdout[-2000:],result.stderr[-2000:])
        assert "PASS" in result.stdout,(name,result.stdout)
    return {key:json.loads((ROOT/"data"/path).read_text(encoding="utf-8"))
            for key,path in DATA.items()}

def test_all_six_replay(certificates):
    assert len(certificates)==6
    assert all(a["status"].startswith("PASS_") for a in certificates.values())

def test_w33_faithful_s3_holonomy(certificates):
    rows=certificates["holonomy"]["cases"]
    assert [r["holonomy_subgroup_order"] for r in rows]==[6,6,6]
    assert [r["predicted_exact_covariantly_constant_dimensions"] for r in rows]==[12]*3
    assert rows[0]["verified_zero_modes"]==12
    assert rows[0]["twisted_graph_laplacian_dimension"]==240
    assert rows[0]["all_eigenvalues_nonnegative"]
    assert rows[0]["smallest_positive_eigenvalue"]>.6
    assert rows[0]["w33_point_orbit_size_census"]=={"1":2,"2":1,"3":6,"6":3}

def test_cycle_census_matches_euler(certificates):
    for r in certificates["holonomy"]["cases"]:
        v=6**r["level"]
        e=9*(v-1)//5
        assert r["nodes"]==v
        assert r["edges"]==e
        assert r["cycle_rank"]==e-v+1

def test_wilson_flux_and_triangle_recursion(certificates):
    rows=certificates["wilson"]["checks"]
    assert [r["triangles"] for r in rows]==[4,25,151,907]
    assert all(r["w33_wilson_trace_each_plaquette"]==8 for r in rows)
    for r in rows:
        assert abs(r["normalized_wilson_action_sum"]-r["triangles"]*.8)<1e-10

def test_all_e8_fibers_are_actual_a2_roots(certificates):
    d=certificates["e8"]
    assert d["fibers"]==40
    assert d["all_fibers_A2_root_subsystems"]
    assert d["W_A2"]==6
    assert d["Aut_root_A2_extended"]==12
    assert d["Pascal_coordinate_S3_fiber_subgroup"]==6
    assert all(x["weyl_a2_is_transitive"] for x in d["fiber_checks"])
    assert all(x["equivariant_boundary_isomorphism_count"]==12 for x in d["fiber_checks"])

def test_boundary_resolvent_nonzero_frequency(certificates):
    d=certificates["resolvent"]
    assert len(d["tests"])==5
    assert all(len(row["levels"])==4 for row in d["tests"])
    err=max(abs(q["max_abs_error"]) for row in d["tests"] for q in row["levels"] if "max_abs_error" in q)
    assert err<1e-7,err
    assert d["closure_dimension"]==2

def test_scale_firewall_and_no_4d_product(certificates):
    d=certificates["scale"]
    assert d["exact_mass_time_ratio"]=="90/7"
    ratio=90/7
    for m in range(1,7):
        ds=2*m*math.log(6)/math.log(ratio)
        assert abs(ds-4)>1e-3
    assert "only c=0" in d["exact_conductance_fixed_point"]

def test_photon_probabilities_and_triangle_control(certificates):
    d=certificates["photonic"]
    assert d["quantum_unitarity_and_classical_mass_test"]
    assert len(d["simulation"])==6
    assert len(d["full_lattice_negative_controls"])==8
    controls={(r["level"],r["dimensionless_time"]):r for r in d["full_lattice_negative_controls"]}
    assert .56<controls[(2,4.)]["total_variation_quantum_vs_undeleted_triangle"]<.59
    assert .77<controls[(3,4.)]["total_variation_quantum_vs_undeleted_triangle"]<.79
    assert all(0<=r["total_variation_quantum_vs_undeleted_triangle"]<=1 for r in controls.values())

def test_symmetric_disorder_controls(certificates):
    rows=certificates["photonic"]["symmetric_disorder_5pct_tests"]
    assert len(rows)==12
    assert all(0<=r["distribution_total_variation"]<=1 for r in rows)
    assert all(r["relative_coupling_disorder_max"]==.05 for r in rows)
    assert set(r["level"] for r in rows)=={2,3}
