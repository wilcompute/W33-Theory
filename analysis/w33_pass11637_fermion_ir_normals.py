"""Pass11637: full-normal fermion and IR replay of the supplied45/126 shell.
Prior11634 owns bosonic Frechet implementation. PriorOct1 full E6 determinant
is a different inventory and its T saddle is not inherited here. Not pole masses.
"""
from pathlib import Path
import json,sys,hashlib,argparse
import numpy as np
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as j
from numpy.polynomial.legendre import leggauss
from scipy.optimize import root as solve
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11625_11629_composites_joint_vacua as old
OUT=ROOT/'data/w33_pass11637_fermion_ir_normals.json'
def make_action(order=32,infrared=.1,yukawa=.03,families=3):
    V,T,D=old.scalar_data();V,T,D=map(j.asarray,[V,T,D]);I45=j.eye(45);I252=j.eye(252)
    def fields(q):return j.einsum('a,aij->ij',q[:45],V),j.einsum('a,aij->ij',q[45:],D)
    def quantities(q):
        A,S=fields(q);a=q[:45];ta=j.einsum('a,aij->ij',a,T)
        ns=j.vdot(S,S).real;X=S@S.conj().T;F=A@A@A+A;Z=ta@S+S@ta.T+3j*S
        return A,S,a,ta,ns,X,F,Z
    def tree(q):
        A,S,a,ta,ns,X,F,Z=quantities(q)
        return (j.dot(a,a)-3)**2+j.vdot(F,F).real/2+(ns-1)**2+ns*ns-j.trace(X@X).real+j.vdot(Z,Z).real
    def hs(q):
        A,S,a,ta,ns,X,F,Z=quantities(q)
        ha=8*j.outer(a,a)+4*(j.dot(a,a)-3)*I45
        df=V@A@A+A@V@A+A@A@V+V
        ha+=j.einsum('aij,bij->ab',df,df)
        va=V@A;av=A@V
        def row(i):
            d2=V[i]@va+V@va[i]+V[i]@av+V@av[i]+av[i]@V+av@V[i]
            return j.einsum('ij,bij->b',F,d2)
        ha+=jax.vmap(row)(j.arange(45))
        gs=2*j.einsum('bij,ij->b',D.conj(),S).real
        dx=D@S.conj().T+S@D.conj().transpose(0,2,1)
        hh=4*j.outer(gs,gs)+(4*ns-2)*I252
        hh-=2*j.einsum('aij,bji->ab',dx,dx,optimize=True).real
        hh-=4*j.einsum('aij,ik,bkj->ab',D.conj(),X,D,optimize=True).real
        ja=T@S+S@T.transpose(0,2,1);js=ta@D+D@ta.T+3j*D;J=j.concatenate([ja,js])
        H=j.zeros((297,297)).at[:45,:45].set(ha).at[45:,45:].set(hh)
        H+=2*j.einsum('aij,bij->ab',J.conj(),J,optimize=True).real
        cross=2*j.einsum('ij,abij->ab',Z.conj(),T[:,None]@D[None]+D[None]@T[:,None].transpose(0,1,3,2)).real
        return H.at[:45,45:].add(cross).at[45:,:45].add(cross.T)
    def hv(q):
        A,S,*_=quantities(q)
        ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1)
        return j.einsum('aij,bij->ab',ga,ga)/2+2*j.einsum('aij,bij->ab',gs.conj(),gs).real
    z,w=leggauss(order);x=j.asarray((infrared**2+.25)/2+(.25-infrared**2)*z/2)
    weight=j.asarray(w*(.25-infrared**2)/2)*x/(64*j.pi**2)
    def spectral_data(H):
        lam,Q=j.linalg.eigh((H+H.T)/2)
        first=j.sum(weight[None,:]/(x[None,:]+lam[:,None]),axis=1)
        return lam,Q,first
    @jax.custom_jvp
    def first_matrix(H):
        lam,Q,first=spectral_data(H)
        return (Q*first)@Q.T
    @first_matrix.defjvp
    def first_rule(primals,tangents):
        H,=primals;E,=tangents;lam,Q,first=spectral_data(H)
        den=x[None,:]+lam[:,None]
        loewner=-(weight[None,:]/den)@(1/den).T
        f=(Q*first)@Q.T
        return f,Q@(loewner*(Q.T@E@Q))@Q.T
    @jax.custom_jvp
    def trace_shell(H):
        lam=j.linalg.eigvalsh((H+H.T)/2)
        return j.sum(weight[None,:]*j.log1p(lam[:,None]/x[None,:]))
    @trace_shell.defjvp
    def trace_rule(primals,tangents):
        H,=primals;E,=tangents
        return trace_shell(H),j.sum(first_matrix(H)*E.T)
    def action(q):
        _,S=fields(q);mf=S.conj().T@S
        rf=j.concatenate([j.concatenate([mf.real,-mf.imag],axis=1),j.concatenate([mf.imag,mf.real],axis=1)],axis=0)
        # One Weyl fermion carries two spin degrees; realification doubles
        # each of the16 eigenvalues, so the coefficient is -families.
        return .001*tree(q)+trace_shell(.001*hs(q))+3*trace_shell(.001*hv(q))-families*trace_shell(yukawa**2*rf)
    return fields,tree,hs,hv,action,trace_shell,first_matrix

def background_map():
    V,T,D=old.scalar_data();cols=[]
    for p in np.eye(3):
        A,S=old.background(p);cols.append(np.r_[np.einsum('aij,ij->a',V,A)/2,2*np.einsum('aij,ij->a',D.conj(),S).real])
    return np.array(cols).T

def replay(infrared,yukawa,order=32):
    fields,tree,hs,hv,f,_,_=make_action(order,infrared,yukawa)
    M=background_map();sm=j.asarray(M);vf=jax.jit(jax.value_and_grad(lambda x:f(sm@x)))
    start=np.array(old.quantum_vacuum()['stationary_SM_slice'])
    fun=lambda x:np.array(vf(j.asarray(x))[1])
    sol=solve(fun,start,tol=1e-10);p=sol.x;q=M@p
    assert np.linalg.norm(fun(p))<1e-9
    jf=jax.jit(f);value=float(jf(q));grad=jax.jit(jax.grad(f));g,lin=jax.linearize(grad,j.asarray(q));g=np.array(g)
    batch=jax.jit(jax.vmap(lin));rows=[];eye=np.eye(297)
    for start in range(0,297,8):
        dirs=np.zeros((8,297));n=min(8,297-start);dirs[:n]=eye[start:start+n]
        rows.extend(np.array(batch(j.asarray(dirs)))[:n])
    H=np.array(rows);assert np.max(abs(H-H.T))<1e-9;H=(H+H.T)/2
    A,S=map(np.array,fields(q));V,T,D=old.scalar_data();ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1)
    G=np.vstack([np.einsum('aij,bij->ab',V,ga)/2,2*np.einsum('aij,bij->ab',D.conj(),gs).real])
    U,sig,_=np.linalg.svd(G,full_matrices=True);rank=int(sum(sig>1e-9));N=U[:,rank:];ev=np.linalg.eigvalsh(N.T@H@N)
    assert rank==33 and np.linalg.norm(g)<1e-8 and np.linalg.norm(H@G)<1e-8
    scalar_min=float(np.linalg.eigvalsh(.001*np.array(hs(q))).min());assert infrared**2+scalar_min>0
    assert min(np.linalg.eigvalsh(S.conj().T@S))>-1e-12
    rng=np.random.default_rng(11637);v=N@rng.normal(size=264);v/=np.linalg.norm(v);step=2e-4
    fd=(float(jf(q+step*v))+float(jf(q-step*v))-2*value)/step**2;exact=float(v@H@v);assert abs(fd-exact)<2e-7
    return dict(infrared=infrared,yukawa=yukawa,order=order,SM_slice=p.tolist(),value=value,
      full_gradient_norm=float(np.linalg.norm(g)),gauge_rank=rank,Ward_HG_norm=float(np.linalg.norm(H@G)),
      normal_eigenvalues=ev.tolist(),minimum_normal_curvature=float(ev[0]),all_normal_positive=bool(ev[0]>0),
      scalar_minimum_mass_squared=scalar_min,minimum_scalar_denominator=infrared**2+scalar_min,
      naive_lower_cutoff_boundary=float(np.sqrt(max(0.,-scalar_min))),directional_AD=exact,directional_FD=fd),dict(H=H,G=G,N=N,q=q,v=v)

def produce(order=64,compare_order=None):
    cases=[];arrays={}
    for index,(k,y) in enumerate([(.1,.03),(.06,.03),(.03,.03),(.1,.3)]):
        print('fermion full297 case',index,k,y,flush=True)
        d,a=replay(k,y,order);cases.append(d);arrays.update({f'{name}_{index}':val for name,val in a.items()});print(d['minimum_normal_curvature'],d['minimum_scalar_denominator'],flush=True)
    if compare_order is not None:
        for index in [0,2]:
            d,a=replay(cases[index]['infrared'],cases[index]['yukawa'],compare_order)
            error=float(np.linalg.norm(a['H']-arrays[f'H_{index}'],2))
            print('quadrature fullH control',index,order,compare_order,error,flush=True)
            assert error<1e-8
            cases[index]['quadrature_control']=dict(reference_order=compare_order,H_operator_error=error,reference_normal_gap=d['minimum_normal_curvature'])
    archive=ROOT/'data/w33_pass11637_fermion_ir_normals.npz';np.savez_compressed(archive,**arrays)
    out=dict(status='PASS',passes=[11637],cases=cases,families=3,
      declared_action='V=.001 Vtree + shell(.001 Hs)+3 shell(.001 Hv)-2*3 shell(y² Sdag S); shell integral x log(1+m²/x)/(64pi²), x from k² to .25. Canonical297 scalar coordinates. Three Weyl16 with supplied same Yukawa y to symmetric126 S.',
      operator='L_Y=-y/2 sum_family psi.T epsilon_spin Sdag psi+h.c.; S transforms U S U.T, so mass=y Sdag and massdag mass=y² S Sdag has same singular spectrum as Sdag S. Spinor indices are contracted with antisymmetric Lorentz epsilon. Representation/conjugation chosen to match prior126 carrier.',
      boundary='Full numerical normal Hessians in a supplied finite Landau-shell EFT. Fixed tree curvature becomes negative below the stored naive cutoff boundary; no continuation through the logarithm or uncomputed Goldstone resummation, interval/pole mass, observed parameter fit, all-loop or UV claim.',
      archive=str(archive.relative_to(ROOT)),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
      prior_owners=['analysis/w33_pass11634_full_quantum_normals.py','analysis/w33_pass11625_11629_composites_joint_vacua.py','analysis/w33_20261001_complete_gauge_scalar_fermion_loop.py'],
      primary_sources=['https://arxiv.org/abs/1712.08068'],producer_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest())
    OUT.write_text(json.dumps(out,indent=2)+'\n');print('fermion IR PASS',flush=True)
if __name__=='__main__':produce(int(sys.argv[1]) if len(sys.argv)>1 else 64,int(sys.argv[2]) if len(sys.argv)>2 else None)
