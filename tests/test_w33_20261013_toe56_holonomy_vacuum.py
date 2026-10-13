"""TOE56 extra: W33 Gaussian boson diamagnetic holonomy-vacuum no-go."""
from pathlib import Path
import json,sys,subprocess
import pytest
R=Path(__file__).resolve().parents[1]
@pytest.fixture(scope="module")
def result():
 p=subprocess.run([sys.executable,str(R/"analysis"/"w33_20261013_toe56_bosonic_holonomy_vacuum.py")],
   cwd=R,capture_output=True,text=True,timeout=120)
 assert p.returncode==0,(p.stdout[-500:],p.stderr[-1200:])
 return json.loads((R/"data"/"w33_20261013_toe56_holonomy_scalar_one_loop.json").read_text())
def test_native_W33_positive_bosonic_diamagnetic_bound(result):
 assert result["native_graph"]=={"vertices":80,"oriented_edges":160,"regular_degree":4,"harmonic_U1_flat_connections":3}
 assert result["convergence_ratio_upper_bound"]<1
 assert "EVERY compact link connection" in result["exact_global_theorem"]
 assert result["minimum_sampled_energy_difference"]>0
def test_numerical_CP_even_hessian_positive(result):
 assert len(result["sampled_holonomy_cases"])==32
 assert min(result["local_harmonic_Hessian_eigenvalues"])>0
 assert result["maximum_CP_reversal_deviation"]<1e-9
 assert result["gauge_transform_logdet_residual"]<1e-9
def test_exclusion_scope_is_only_Gaussian_bosonic_scalar(result):
 assert result["scalar_parameters"]["positive_mass_squared"]>0
 assert "NOT" in result["negative_conclusion"]
 assert "Does NOT exclude CP breaking" in result["negative_conclusion"]
