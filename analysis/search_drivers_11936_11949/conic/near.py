import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng = np.random.default_rng(1)
for phi in [np.pi, 0.0, 2.0, np.angle((-0.0557+0.7042j)/(0.5836+0.4004j))]:
    s = np.array([0, 1, np.exp(1j*phi)])/np.sqrt(2)
    print('phi %.4f M2 %.6f' % (phi, lib.H23.magic(s)))
# seed-6 family: s = (0,1,e^{i phi6})/sqrt2 ; perturb towards e1 and towards (0,1,-e^{i phi})
phi6 = np.angle((-0.0557+0.7042j)/(0.5836+0.4004j))
s = np.array([0, 1, np.exp(1j*phi6)])/np.sqrt(2)
for name, w in [('e1', np.array([1,0,0],complex)), ('anti', np.array([0,1,-np.exp(1j*phi6)])/np.sqrt(2)), ('e1i', np.array([1j,0,0]))]:
    for th in [0.3, 0.1, 0.03, 0.01]:
        u = np.cos(th)*s + np.sin(th)*w
        sp = lib.spectrum(u, [0.01, 0.005, 0.0025], rng)
        print(name, 'th', th, ' '.join('t=%g res=%.0e s2=%.3e s3=%.3e' % tuple(r) for r in sp), flush=True)
