import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys, numpy as np
sys.path.insert(0, _os.path.join(_DRV, 'conic')); import lib
rng=np.random.default_rng(9)
for k in range(5):
    v=rng.normal(size=2)+1j*rng.normal(size=2); u=np.r_[0,v]/np.linalg.norm(v)
    for t in (0.01,0.5):
        sp=lib.spectrum(u,[t],rng)[0]
        print('M2 %.4f t %g res %.0e s2 %.1e s3 %.1e' % (lib.H23.magic(u),t,sp[1],sp[2],sp[3]), flush=True)
