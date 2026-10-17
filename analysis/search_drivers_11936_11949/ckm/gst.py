import numpy as np
from scipy.optimize import fsolve
N=np.arange(-40,41)
def th(a,z,Om): return np.sum(np.exp(1j*np.pi*(N+a)**2*Om+2j*np.pi*(N+a)*z))
def Yk(zeta,tau,k):
    g=np.exp(-1.5*np.pi*zeta.imag**2/tau.imag); Y=np.zeros((3,3),complex)
    for i in range(3):
        j=(k-i)%3; Y[i,j]=g*th(((i-j)%3)/3,3*zeta,6*tau)
    return Y
def svd_sorted(Y):
    U,s,Vh=np.linalg.svd(Y); return U,s
# down sector: fit (Im tau_d, nu_d) to m_s/m_b, m_d/m_s at M_Z
tgt=(np.log(0.055/2.89),np.log(2.9/55))
def eqs(p):
    tau=1j*p[0]; s=np.sort(np.linalg.svd(Yk(p[1]*tau,tau,0),compute_uv=False))[::-1]
    return [np.log(s[1]/s[0])-tgt[0],np.log(s[2]/s[1])-tgt[1]]
pd=fsolve(eqs,[2.6,0.12]); print('down fit Im tau, nu =',pd, eqs(pd))
taud=1j*pd[0]; zd=pd[1]*taud
# up sector localised (fit as before)
tgtu=(np.log(0.619/171.7),np.log(1.27/619))
def equ(p):
    tau=1j*p[0]; s=np.sort(np.linalg.svd(Yk(p[1]*tau,tau,0),compute_uv=False))[::-1]
    return [np.log(s[1]/s[0])-tgtu[0],np.log(s[2]/s[1])-tgtu[1]]
pu=fsolve(equ,[4.2,0.12]); tauu=1j*pu[0]; zu=pu[1]*tauu
Uu,su=svd_sorted(Yk(zu,tauu,0))
rng=np.random.default_rng(0)
rows=[]
for _ in range(400):
    e1=10**rng.uniform(-5,-1.5)*np.exp(2j*np.pi*rng.random()); e2=10**rng.uniform(-5,-1.5)*np.exp(2j*np.pi*rng.random())
    Yd=Yk(zd,taud,0)+e1*Yk(zd,taud,1)+e2*Yk(zd,taud,2)
    Ud,sd=svd_sorted(Yd)
    V=abs(Uu.conj().T@Ud)
    # identify V_us: element between up-quark (lightest up) and strange (2nd down) ... use mass ordering: columns sorted desc by svd
    Vus=V[2,1]; Vcb=V[1,0]; Vub=V[2,0]
    md_ms=sd[2]/sd[1]
    rows.append((abs(e1),abs(e2),Vus,np.sqrt(md_ms),Vcb,Vub, sd[1]/sd[0]))
rows=np.array(rows)
sel=rows[(rows[:,2]>0.1)&(rows[:,2]<0.4)]
print('cases with 0.1<Vus<0.4:',len(sel))
if len(sel): print('Vus / sqrt(md/ms): median %.3f  spread %.3f'%(np.median(sel[:,2]/sel[:,3]),np.std(sel[:,2]/sel[:,3])))
print('overall corr log Vus vs log sqrt(md/ms):',np.corrcoef(np.log(rows[:,2]+1e-12),np.log(rows[:,3]))[0,1])
for r in sel[:10]: print(np.round(r,4))
