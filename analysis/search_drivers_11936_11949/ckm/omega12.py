import numpy as np
r=np.arange(-14,15); n1,n2=[x.ravel() for x in np.meshgrid(r,r,indexing='ij')]
def Th2(a1,a2,Om):
    x1,x2=n1+a1,n2+a2
    return np.sum(np.exp(1j*np.pi*(Om[0,0]*x1*x1+2*Om[0,1]*x1*x2+Om[1,1]*x2*x2)))
N=np.arange(-40,41)
def th(a,z,Om): return np.sum(np.exp(1j*np.pi*(N+a)**2*Om+2j*np.pi*(N+a)*z))
# exact identity check
rng=np.random.default_rng(2)
for _ in range(3):
    A=rng.normal(size=(2,2)); Om=(A+A.T)/4+1j*(np.array([[2.0,0.4],[0.4,1.5]])+0.2*np.eye(2))
    a1,a2=1/3,1/3
    lhs=Th2(a1,a2,Om)
    rhs=sum(np.exp(1j*np.pi*(m+a2)**2*Om[1,1])*th(a1,(m+a2)*Om[0,1],Om[0,0]) for m in range(-14,15))
    print('identity rel err',abs(lhs-rhs)/abs(lhs))
# Gaussian regime: family masses at class a vs one-qutrit with z_eff=(a/3)Om12
def fam_masses_2(a,Om): return np.array([abs(Th2(c/3,a/3,Om)) for c in range(3)])
def fam_masses_1(a,Om): return np.array([abs(th(c/3,(a/3)*Om[0,1],Om[0,0])) for c in range(3)])
for O22 in (4.0,8.0,16.0):
    Om=np.array([[25.25j,4.57j],[4.57j,O22*1j]])
    for a in (0,1):
        m2=fam_masses_2(a,Om); m1=fam_masses_1(a,Om)
        r2=np.sort(m2)/np.sort(m2)[-1]; r1=np.sort(m1)/np.sort(m1)[-1]
        print(f'ImO22={O22} a={a}: two-qutrit ratios {np.round(r2,8)} one-qutrit(z_eff) {np.round(r1,8)} maxrel {np.max(abs(r2-r1)/np.maximum(r1,1e-30)):.2e}')
