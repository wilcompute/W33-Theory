import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import numpy as np, sys
from scipy.optimize import least_squares
sys.argv=['x']
from sfit import fixres, unpack, G
rng=np.random.default_rng(1)
th=0.73624*np.pi
for gd in G:
  for k in (0,1,2):
    best=9
    for _ in range(20):
        tau=np.exp(1j*th); eu=1j*0.0035*tau
        td=rng.uniform(-1,1)+1j*10**rng.uniform(-2,0.5); ed=(rng.normal()+1j*rng.normal())*0.05
        zd=rng.uniform(-.5,.5)+1j*rng.normal(0,.1)
        p0=np.array([tau.real,tau.imag,eu.real,eu.imag,ed.real,ed.imag,td.real,td.imag,zd.real,zd.imag])
        r=least_squares(lambda p: fixres(p,gd,k),p0,xtol=1e-15,ftol=1e-15,gtol=1e-15)
        fr=np.abs(fixres(r.x,gd,k)).max()
        if fr<best: best,bx=fr,r.x
    print(gd,k,'min fixres %.2e'%best, np.round(bx,4))
