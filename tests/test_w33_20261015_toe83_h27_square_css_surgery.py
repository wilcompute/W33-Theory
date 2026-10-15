"""TOE83 exact regression: H27-equivariant four-cycle CSS surgery."""
from functools import lru_cache
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261015_toe83_h27_square_css_surgery import certificate
from w33_20261015_toe82_native_H27_h1_character import certificate as previous

@lru_cache(maxsize=1)
def result():
    return certificate()

def test_native_toe82_source():
    old=previous()
    assert old["complex"]=={"vertices":27,"edges":135,"faces":45,
                            "boundary_ranks_F2":[26,45],"H1_dimension":64}
    assert old["H27_invariant_H1_dimension_characteristic_zero"]==0

def test_square_orbit_census():
    r=result()["orbit_metadata"]
    assert r["square_count"]==1080
    assert r["H27_orbit_sizes"]=={"27":40} or r["H27_orbit_sizes"]=={27:40}
    assert r["fewest_orbit_solution_count"]==468
    assert r["selected_orbits"]==[0,10]
    assert r["added_square_count"]==54
    assert r["rank_faces"]==83
    assert r["logical_qubits"]==26
    assert r["second_homology_dimension"]==16

def test_exact_binary_and_ternary_distances():
    r=result()
    assert r["binary"]["n"]==135
    assert r["binary"]["k"]==26
    assert (r["binary"]["X_distance"],r["binary"]["Z_distance"])==(6,4)
    assert r["ternary"]["k"]==26
    assert (r["ternary"]["X_distance"],r["ternary"]["Z_distance"])==(6,4)
    assert len(r["binary"]["X_weight6_witness"])==6
    assert len(r["ternary"]["Z_weight4_witness"])==4

def test_frozen_certificate_matches():
    p=ROOT/"data/w33_20261015_toe83_h27_square_css_surgery.json"
    frozen=json.loads(p.read_text(encoding="utf8"))
    r=result()
    assert frozen["binary"]==r["binary"]
    assert frozen["ternary"]==r["ternary"]
    assert frozen["orbit_metadata"]["selected_orbits"]==r["orbit_metadata"]["selected_orbits"]
