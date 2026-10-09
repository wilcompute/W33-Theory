"""The proved smooth polynomial is an explicit new numerical input."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11758_smooth_snapshot_followthrough as M


def test_smooth_run_hashes_and_input_identity():
    p=json.loads(M.OUT.read_text())
    assert p['source_sha256']==hashlib.sha256(Path(M.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    for name,digest in p['inputs'].items():assert digest==hashlib.sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert p['polynomial']==str(M.polynomial()[1]) and p['snapshot_global_smoothness_certified']
    assert not p['physical_normalized_Yukawa_certified']


def test_new_sampling_and_input_context_restore():
    old=M.A.Q.reference_polynomial;old_terms=M.A.polynomial_terms()
    with M.actual_smooth_input():
        assert M.A.Q.reference_polynomial is M.polynomial
        assert M.A.polynomial_terms()!=old_terms
        d=M.A.sample_hypersurface(81758,12)
        assert len(d['z'])==24 and d['polynomial_residual']<1e-11
        assert np.max(abs(M.A.chart_polynomial(d['z'],d['bits'])))<1e-11
    assert M.A.Q.reference_polynomial is old and M.A.polynomial_terms()==old_terms


def test_smoothness_does_not_hide_numerical_sensitivity():
    p=json.loads(M.OUT.read_text());coarse,fine=p['runs']
    for run in p['runs']:
        v=run['metric']['validation']
        assert run['polynomial_residual']<1e-11 and v['min_sample_metric_eigenvalue']>0
        assert v['corrected_log_density_variance']<v['reference_log_density_variance']
        assert v['weighted_relative_MA_rms']>.1
        assert run['HYM']['validation']['beta_product_max']<1e-10
        assert max(run['HYM']['validation']['corrected_rms'])>.5
    ratio=fine['harmonic']['F_rescaling_invariant_geometry_proxy']/coarse['harmonic']['F_rescaling_invariant_geometry_proxy']
    assert abs(ratio-1)>.1 # independent control against a claimed converged mass
