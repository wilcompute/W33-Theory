import sys,json,numpy as np
sys.path.insert(0,'.'); from th40 import theta
DATA=dict(mc_mt=(0.620/168.26,.05), mu_mc=(1.23e-3/0.620,.20), ms_mb=(0.053/2.86,.08), md_ms=(2.67e-3/0.053,.10), Vus=(0.2250,.003), Vcb=(0.0411,.025), Vub=(0.00382,.05), J=(3.08e-5,.05))
def nsv(Om,z):
    Y=theta(Om,z); z=np.asarray(z); return Y*np.exp(-3*np.pi*z.imag@np.linalg.inv(Om.imag)@z.imag)
def ev(x):
    c=x[0::2]+1j*x[1::2]; tau,td,eu,ed,z2=c; Om=np.array([[tau,ed],[ed,td]])
    if tau.imag<0.03 or td.imag<0.004 or np.linalg.eigvalsh(Om.imag).min()<0.002: return None
    Yu=theta(np.array([[tau,eu],[eu,tau]])); Yd=nsv(Om,(0,z2)); Ye=nsv(Om,(0,6*z2)).T
    if not (np.isfinite(Yu).all() and np.isfinite(Yd).all() and np.isfinite(Ye).all()): return None
    try:
        Uu,su,_=np.linalg.svd(Yu); Ud,sd,_=np.linalg.svd(Yd); se=np.linalg.svd(Ye,compute_uv=False)
    except np.linalg.LinAlgError: return None
    V=(Uu.conj().T@Ud)[::-1,::-1]; J=abs(np.imag(V[0,0]*V[1,1]*np.conj(V[0,1])*np.conj(V[1,0])))
    o=dict(mc_mt=su[1]/su[0],mu_mc=su[2]/su[1],ms_mb=sd[1]/sd[0],md_ms=sd[2]/sd[1],Vus=abs(V[0,1]),Vcb=abs(V[1,2]),Vub=abs(V[0,2]),J=J)
    chi=sum((np.log(o[k]/v)/e)**2 for k,(v,e) in DATA.items())
    return chi, (se[1]/se[0], se[2]/se[1], sd[0]/se[0], abs(eu), abs(ed))
x=np.array(json.load(open('hy2_polished.json'))[int(sys.argv[1])]); rng=np.random.default_rng(int(sys.argv[2]))
cur=ev(x); chi=cur[0]; step=np.abs(x)*0.003+1e-5; acc=0; samples=[]
for it in range(int(sys.argv[3])):
    y=x+step*rng.normal(size=x.size); r=ev(y)
    if r is not None and np.log(rng.uniform())< -(r[0]-chi)/2:
        x,chi,cur=y,r[0],r; acc+=1
    if it%10==0: samples.append([chi,*cur[1]])
    if it==500: step*= (acc/500/0.25+0.1)
S=np.array(samples[len(samples)//4:])
print('chain',sys.argv[1:],'acc %.2f'%(acc/int(sys.argv[3])),'chi2 med %.2f'%np.median(S[:,0]),
      'mmu/mtau q05/50/95',np.round(np.quantile(S[:,1],[.05,.5,.95]),4),'me/mmu',np.round(np.quantile(S[:,2],[.05,.5,.95]),5),'yb/ytau',np.round(np.quantile(S[:,3],[.05,.5,.95]),3),'|ed|',np.round(np.quantile(S[:,5],[.05,.95]),4),flush=True)
np.save(f'chain_{sys.argv[1]}_{sys.argv[2]}.npy',S)
