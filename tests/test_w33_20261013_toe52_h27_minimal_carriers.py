"""TOE52 H27 three-slice theorem and Bloch reciprocity regressions."""
from pathlib import Path
import subprocess,sys,json
import pytest
R=Path(__file__).resolve().parents[1]
@pytest.fixture(scope="module")
def frozen():
 for script in ("w33_20261013_toe52_h27_bridge.py","w33_20261013_toe52_bloch_reciprocity.py"):
  run=subprocess.run([sys.executable,str(R/"analysis"/script)],cwd=R,
      capture_output=True,text=True,timeout=100)
  assert run.returncode==0,(script,run.stdout[-800:],run.stderr[-1000:])
 return {k:json.loads((R/"data"/f"w33_20261013_toe52_{path}.json").read_text())
  for k,path in [("h27","h27_K81_minimal_slices"),("bloch","bloch_reciprocity")]}
def test_exact_heisenberg_nonabelian_group(frozen):
 p=frozen["h27"]
 assert p["H27_group_order"]==27
 assert p["center_order"]==3
 assert p["element_order_distribution"]=={"1":1,"3":26}
 assert p["W33_line_orbit_lengths"]==[1,1,1,1,9,9,9,9]
 assert p["H27_line_permutation_fixed_points_by_element"]=={"4":2,"7":24,"40":1}
def test_W33_line_spectral_invariant_multiplicities(frozen):
 p=frozen["h27"]["H27_invariant_subspace_dimensions"]
 assert p=={"all40":8,"constant1":1,"plus24":4,"minus15":3,"even25":5}
def test_integer_modular_rank_lower_bounds_and_minimal_slices(frozen):
 data=frozen["h27"]["tested_81D_slice_counts"]
 assert [data[str(k)]["full_integer_mod101_rank"] for k in (1,2,3)]==[35,38,40]
 assert [data[str(k)]["even25_integer_mod101_rank"] for k in (1,2,3)]==[23,25,25]
 assert [data[str(k)]["spread15_integer_mod101_rank"] for k in (1,2,3)]==[15,15,15]
def test_group_equivariant_polar_isometries(frozen):
 cases=frozen["h27"]["explicit_polar_isometries"]
 assert {k:z["carrier_slices"] for k,z in cases.items()}=={"spread15":1,"even25":2,"full40":3}
 assert all(z["max_orthonormality_residual"]<1e-11 for z in cases.values())
 assert all(z["max_covariance_27_group_elements"]<1e-11 for z in cases.values())
 assert all(z["min_singular_integer_Reynolds"]>.01 for z in cases.values())
def test_no_full_K81_equivariance_claim(frozen):
 p=frozen["h27"]
 assert "No full K81 or Sp4" in p["representation_theorem"]
 assert "NOT automatically" in p["scientific_limits"]
def test_opposite_bloch_momenta_cannot_add_spectral_rank(frozen):
 p=frozen["bloch"]
 assert p["status"]=="PASS"
 assert p["rank_3wavevectors_9moments"]==p["rank_with_three_opposite_wavevectors_18moments"]==9
 assert len(p["k_examples"])==3
 assert all(z["P_minus_vs_conjP_plus_error"]<1e-12 for z in p["k_examples"])
 assert all(z["max_weight_gradient_error"]<1e-8 for z in p["k_examples"])
