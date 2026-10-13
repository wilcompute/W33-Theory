"""TOE54 finite-lattice Lorentz obstruction and native Maxwell tests."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
@pytest.fixture(scope="module")
def cert():
 q=subprocess.run([sys.executable,str(R/"analysis/w33_20261013_toe54_lorentz_dispersion.py")],
  cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
 assert q.returncode==0,(q.stdout[-1000:],q.stderr[-1600:])
 return json.loads((R/"data/w33_20261013_toe54_finite_lorentz_dispersion.json").read_text())
def test_native_two_mode_acoustic_limit_but_finite_dispersion(cert):
 assert cert["status"]=="PASS_TOE54_FINITE_BLOCH_EXACT_GLOBAL_LORENTZ_OBSTRUCTION"
 assert cert["n_samples"]==24
 for row in cert["samples"]:
  assert row["max_P_gradient"]<1e-9
  assert row["third_gapped_omega_sq"]>80
  assert len(row["light_omega_sq"])==2
  assert all(x>0 for x in row["light_omega_sq"])
  assert abs(row["mean_light_phase_velocity_sq"]-2)<.01
def test_rational_isotropic_leading_cone_does_not_fix_quartic_terms(cert):
 d=cert["directional_finite_k_summary"]
 assert len(d)==6
 assert all(z["fractional_shift_r0p16_vs_2"]<-.001 for z in d.values())
 assert abs(d["axis_z"]["r0p02_to_r0p04_quartic_proxy_slope"]-
       d["diagonal_xyz"]["r0p02_to_r0p04_quartic_proxy_slope"])>.1
 assert all(z["relative_polarization_split_r0p16"]>1e-4 for z in d.values())
def test_exact_Fourier_periodicity_and_finite_operator_bound(cert):
 assert cert["rigorous_uniform_operator_norm_bound"]>1
 assert cert["max_three_axis_2pi_Bloch_periodicity_residual"]<1e-12
 assert "real-analytic det" in cert["strict_theorem"]
 assert "continuum limit" in cert["physics_boundary"]
def test_physical_units_not_inferred(cert):
 assert cert["squared_continuum_speed_target"]==2
 assert "No exact Lorentz invariance" in cert["physics_boundary"]
