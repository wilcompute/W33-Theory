import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np, itertools
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
def red_im(t):  # move to Im >= 0.35 region within same Gamma(3) class? just use as is
    return t
def R(t1,t2,eps=1e-4):
    Om = np.array([[t1, eps], [eps, t2]], complex)
    sv = np.linalg.svd(lib.theta_null_2(Om, N=80).reshape(3,3), compute_uv=False); sv = sv/sv[0]
    return sv[2]/sv[1]**2
S = lambda t: -1/t; T = lambda t: t+1; Ti = lambda t: t-1
pts = {}
for base, name in [(1j,'i'), (np.exp(2j*np.pi/3),'w')]:
    seen = []
    for word in itertools.product('STU', repeat=5):
        t = base
        for c in word: t = {'S':S,'T':T,'U':Ti}[c](t)
        if t.imag < 0.12: continue
        g = R(t,t)
        if not any(abs(g-x)<1e-6*max(1,x) for x,_ in seen): seen.append((g,t))
    pts[name] = seen
    print(name, [(round(2*g,6), complex(np.round(t,4))) for g,t in sorted(seen, key=lambda z: z[0].real)])
