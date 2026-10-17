import os as _os
_DRV = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))  # search_drivers_11936_11949
_ANA = _os.path.dirname(_DRV)  # analysis/
_DATA = _os.path.join(_os.path.dirname(_ANA), 'data', 'w33_pass11942_mcmc_chains')
import sys,numpy as np
sys.path.insert(0,_ANA); import w33_pass11942_hypercharge_wilson_leptons as P42
for k,x in P42.FITS.items():
    x=np.array(x); c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,zd=c
    Yd=P42.normalised(np.array([[tau,ed],[ed,td]]),(0,zd)); dd=np.linalg.det(Yd)
    ph=np.linspace(0,2*np.pi,2001)[:-1]; st=[]; tb=[]; tbu=[]
    for p in ph:
        Yu=P42.theta(np.array([[tau,eu*np.exp(1j*p)],[eu*np.exp(1j*p),tau]])); st.append(np.linalg.svd(Yu,compute_uv=False)[0]); du=np.linalg.det(Yu); tb.append(np.angle(du*dd)); tbu.append(np.angle(du))
    st=np.array(st); tb=np.array(tb); tbu=np.array(tbu)
    for lab,idx in (('min m_t',np.r_[np.argmin(st[:1000]),1000+np.argmin(st[1000:])]),('max m_t',np.r_[np.argmax(st[:1000]),1000+np.argmax(st[1000:])])):
        print(k,lab,[('phi %.3f'%ph[i],'thetabar %.3f'%tb[i],'arg det Yu %.3f'%tbu[i]) for i in idx])
