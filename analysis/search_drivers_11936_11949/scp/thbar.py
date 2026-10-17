import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c
    Yu=P42.theta(np.array([[tau,eu],[eu,tau]])); Yd=P42.normalised(np.array([[tau,ed],[ed,td]]),(0,zd))
    du,dd=np.linalg.det(Yu),np.linalg.det(Yd)
    print(k,'arg det Yu %.4f  arg det Yd %.4f  thetabar %.4f rad'%(np.angle(du),np.angle(dd),np.angle(du*dd)))
    # dependence on eps phases: rotate eps_u phase
    for ph in (0,0.5,1.0):
        e=abs(eu)*np.exp(1j*(np.angle(eu)+ph)); Yu2=P42.theta(np.array([[tau,e],[e,tau]]))
        print('   eps_u phase shift',ph,' arg det Yu %.4f'%np.angle(np.linalg.det(Yu2)))
