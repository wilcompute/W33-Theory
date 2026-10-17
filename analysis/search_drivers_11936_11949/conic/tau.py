import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, json, numpy as np, mpmath as mp
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
from w33_pass11869_11873_siegel_level3_two_qutrits import j_of_tau
fz = json.load(open(_os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11926_orbit_reps_frozen.json')))
G = lib.G26.clifford(); rng = np.random.default_rng(5)
dirs = {}
for rec in fz['orbits']:
    t0 = np.array(rec['re'])+1j*np.array(rec['im']); u, st = lib.G26.polish(t0, G); dirs['M2=%.4f' % lib.H23.magic(u)] = u
g = rng.normal(size=3)+1j*rng.normal(size=3); dirs['random'] = g/np.linalg.norm(g)
for name, u in dirs.items():
    guess = None
    for t in (0.01, 0.005):
        c = np.r_[1, t*u]; c /= np.linalg.norm(c); Om, res, guess = lib.V.invert(c, rng, guess); Om = lib.S.siegel_reduce(Om)
        d = np.diag(Om); k = int(np.argmin(d.imag)); tau = d[k]
        # reduce tau to the fundamental domain of SL2(Z)
        for _ in range(50):
            tau = tau - round(tau.real)
            if abs(tau) < 1: tau = -1/tau
            else: break
        print('%-12s t=%.3f res %.0e  Om diag Im %s  boundary tau=%s  j=%s' % (name, t, res, np.round(d.imag, 3), np.round(tau, 5), np.round(complex(j_of_tau(tau)), 2)), flush=True)
