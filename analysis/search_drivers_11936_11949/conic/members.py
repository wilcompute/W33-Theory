import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, json, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
sys.path.insert(0, _ANA)
from w33_pass11869_11873_siegel_level3_two_qutrits import j_of_tau
import w33_pass11937_boundary_elliptic_points as B
fz = json.load(open(_os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11926_orbit_reps_frozen.json')))
G = lib.G26.clifford(); rng = np.random.default_rng(2)
for rec in fz['orbits']:
    u0, st = lib.G26.polish(np.array(rec['re'])+1j*np.array(rec['im']), G)
    m2 = lib.H23.magic(u0)
    if abs(m2 - np.log(8/5)) > 1e-6: continue
    reps = []
    for g in G:
        v = g @ u0; v /= np.linalg.norm(v)
        if not any(abs(abs(np.vdot(v, w)) - 1) < 1e-9 for w in reps): reps.append(v)
    print('members', len(reps), flush=True)
    for k, v in enumerate(reps):
        c = np.r_[1, 0.005*v]; c /= np.linalg.norm(c); Om, res, _ = lib.V.invert(c, rng); Om = lib.S.siegel_reduce(Om)
        d = np.diag(Om); tau = B.reduce_tau(d[int(np.argmin(d.imag))])
        sv = np.linalg.svd(lib.theta_null_2(Om, N=40).reshape(3, 3), compute_uv=False)
        print(k, 'res %.0e tau %s j %s b/a %.4f s2/t %.4f' % (res, np.round(tau, 5), np.round(complex(j_of_tau(tau)), 1), sv[2]/sv[1], sv[1]/sv[0]/0.005), flush=True)
