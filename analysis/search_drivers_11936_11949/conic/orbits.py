import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, json, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
fz = json.load(open(_os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11926_orbit_reps_frozen.json')))
G = lib.G26.clifford(); rng = np.random.default_rng(0)
for rec in fz['orbits']:
    t0 = np.array(rec['re'])+1j*np.array(rec['im']); u, st = lib.G26.polish(t0, G)
    o = lib.spectrum(u, [0.01, 0.005], rng)
    a, b = o[-1, 2]/0.005, o[-1, 3]/0.005; s3 = np.log(o[0, 3]/o[1, 3])/np.log(2)
    print('M2 %.4f stab %d : a=%.4f b=%.4f b/a=%.4f slope_light=%.2f resid %.0e' % (lib.H23.magic(u), st, a, b, b/a, s3, o[:, 1].max()), flush=True)
