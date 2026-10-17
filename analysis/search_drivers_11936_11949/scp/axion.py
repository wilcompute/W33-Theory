import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
def obs(tau,td,eu,ed,zd):
    Yu=P42.theta(np.array([[tau,eu],[eu,tau]])); Yd=P42.normalised(np.array([[tau,ed],[ed,td]]),(0,zd))
    Uu,su,_=np.linalg.svd(Yu); Ud,sd,_=np.linalg.svd(Yd); V=(Uu.conj().T@Ud)[::-1,::-1]
    J=np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0]))
    return su[1]/su[0], su[2]/su[1], sd[1]/sd[0], sd[2]/sd[1], abs(V[0,1]), abs(V[1,2]), abs(V[0,2]), J, np.angle(np.linalg.det(Yu)*np.linalg.det(Yd))
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c
    print(k,'base   ',np.round(obs(tau,td,eu,ed,zd),5))
    for which in ('u','d'):
        for ph in (0.3,1.0,2.0):
            e2=eu*np.exp(1j*ph) if which=='u' else eu; d2=ed*np.exp(1j*ph) if which=='d' else ed
            print(k,'arg eps_%s +%.1f'%(which,ph),np.round(obs(tau,td,e2,d2,zd),5))
