import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
def ckm(Yu,Yd):
    Uu,_,_=np.linalg.svd(Yu); Ud,_,_=np.linalg.svd(Yd); V=(Uu.conj().T@Ud)[::-1,::-1]
    return np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0])), abs(V[0,1])
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c
    Omu=np.array([[tau,eu],[eu,tau]]); Omd=np.array([[tau,ed],[ed,td]])
    Yu=P42.theta(Omu); Yd=P42.normalised(Omd,(0,zd))
    J,vus=ckm(Yu,Yd); Jc,_=ckm(Yu.conj(),Yd.conj())
    # mirror Omega -> -conj Omega, z -> -conj z
    Yu_m=P42.theta(-Omu.conj()); Yd_m=P42.normalised(-Omd.conj(),(0,-np.conj(zd)))
    Jm,vm=ckm(Yu_m.conj(),Yd_m.conj())
    print(k,'J holomorphic %.3e | J with Y* (Weyl) %.3e | mirror+Y* %.3e  Vus %.5f/%.5f  mirror==conj? %.1e'%(J,Jc,Jm,vus,vm,np.abs(Yu_m-Yu.conj()).max()))
    # det Yd winding around eps_d=0
    for r in (0.02,0.005):
        ph=np.linspace(0,2*np.pi,241); a=[np.angle(np.linalg.det(P42.normalised(np.array([[tau,r*np.exp(1j*p)],[r*np.exp(1j*p),td]]),(0,zd)))) for p in ph]
        w=np.sum(np.angle(np.exp(1j*np.diff(a))))/(2*np.pi)
        print('   det Yd winding radius',r,':',round(w,3))
