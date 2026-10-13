"""TOE50 exact two-front independent replay, with previous physics regressions."""
from pathlib import Path
import subprocess,sys,json
import pytest
R=Path(__file__).resolve().parents[1]
@pytest.fixture(scope="module")
def certs():
 out={}
 for key,source,certificate in (
  ("spectral","w33_20261013_toe50_inverse_acoustic_spectral_trace.py","w33_20261013_toe50_inverse_acoustic_spectral_trace.json"),
  ("dual","w33_20261013_toe50_dual_cusp_spread_decoder.py","w33_20261013_toe50_dual_cusp_spread_decoder.json"),
 ):
  p=subprocess.run([sys.executable,str(R/"analysis"/source)],cwd=R,text=True,capture_output=True,timeout=150)
  assert p.returncode==0,(key,p.stdout[-1000:],p.stderr[-1600:])
  out[key]=json.loads((R/"data"/certificate).read_text())
 return out
def test_nonuniqueness_of_microgeometry_under_exact_leading_cone(certs):
 x=certs["spectral"]
 assert x["Jacobian_rank"]==6 and x["fixed_leading_G_level_set_dimension"]==154
 assert x["positive_weight_count"]==160
 assert abs(x["kernel_slope_dTdt"])>100
 a=x["positive_equal_G_samples"]
 assert len(a)==5
 assert all(r["min_weight"]>1/8 for r in a)
 assert all(r["acoustic_G_inf_err"]<1e-11 for r in a)
 assert a[0]["gapped_spectral_trace"]<a[-1]["gapped_spectral_trace"]
 assert x["tangent_norm_J"]<1e-10
def test_exact_dual_cusp_spread_integer_identity(certs):
 x=certs["dual"]
 assert x["counts"]=={"W33_lines":40,"W33_spreads":36,"lines_per_spread":10,"spreads_per_line":9}
 assert x["rank_of_combined_cusp_spread_measurement"]==40
 assert x["max_reconstruction_error"]<1e-11
 assert x["random_arbitrary_real_40_channel_reconstructions"]==50
 assert "orthogonal projectors" in x["positive_orthogonal_resolution"]
