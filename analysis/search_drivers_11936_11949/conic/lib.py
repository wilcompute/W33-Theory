import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, json, numpy as np
sys.path.insert(0, _ANA)
import w33_pass11890_11892_vacuum_phase_diagram as V, w33_pass11874_11878_siegel_fixed_points_cp_magic as S
from w33_pass11869_11873_siegel_level3_two_qutrits import theta_null_2
import w33_pass11926_g25_tangent_vacua as G26, w33_pass11923_stabiliser_higgs_lock as H23
def spectrum(u, ts, rng, guess=None):
    out = []
    for t in ts:
        c = np.r_[1, t*u]; c /= np.linalg.norm(c); Om, res, guess = V.invert(c, rng, guess); Om = S.siegel_reduce(Om)
        sv = np.linalg.svd(theta_null_2(Om, N=40).reshape(3, 3), compute_uv=False); out.append((t, res, sv[1]/sv[0], sv[2]/sv[0]))
    return np.array(out)
