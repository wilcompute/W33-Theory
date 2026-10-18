import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import numpy as np
from scipy.optimize import least_squares
from downS import dres, UPS, up
rng=np.random.default_rng(7)
for s in '+-':
    Ou=up(*UPS[s]); b=1e9
    for _ in range(40):
        p0=np.array([*(rng.normal(size=2)*10**rng.uniform(-3,-.5)),rng.uniform(-1,1),10**rng.uniform(-2,.7),rng.uniform(-.5,.5),rng.normal(0,.3)])
        r=least_squares(lambda p:dres(p,Ou),p0); c=np.sum(r.fun**2); b=min(b,c)
    print('complex-down control, up',s,'best chi2 %.2e'%b)
