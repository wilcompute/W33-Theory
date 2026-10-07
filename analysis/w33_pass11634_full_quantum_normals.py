"""Full297-coordinate finite-shell Hessian, not pole masses or a UV theory.

Reuse11625's declared scalar/vector inventory and cutoff scheme. The spectral
Frechet rule uses exact divided differences under the finite integral, avoiding
eigenvector derivatives at the many degenerate masses. Numerical certificate.
"""
from pathlib import Path
import json,sys,hashlib
import numpy as np
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as j
from numpy.polynomial.legendre import leggauss
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11625_11629_composites_joint_vacua as old
OUT=ROOT/'data/w33_pass11634_full_quantum_normals.json'

def make_action(order=32):
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
    z,w=leggauss(order);x=j.asarray((.01+.25)/2+(.25-.01)*z/2)
    weight=j.asarray(w*(.25-.01)/2)*x/(64*j.pi**2)
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
    def action(q):return .001*tree(q)+trace_shell(.001*hs(q))+3*trace_shell(.001*hv(q))
    return fields,tree,hs,hv,action,trace_shell,first_matrix

def payload(order=32):
    fields,tree,hs,hv,f,trace_shell,first_matrix=make_action(order)
    V,T,D=old.scalar_data();q3=np.array(old.quantum_vacuum()['stationary_SM_slice'])
    A,S=old.background(q3);q=np.r_[np.einsum('aij,ij->a',V,A)/2,2*np.einsum('aij,ij->a',D.conj(),S).real]
    assert np.max(abs(np.array(fields(j.asarray(q))[1])-S))<1e-13
    hsf=jax.jit(hs);h=np.array(hsf(j.asarray(q)))
    assert np.max(abs(h-old.scalar_hessian(A,S)))<1e-10
    jf=jax.jit(f);value=float(jf(j.asarray(q)))
    expected=old.shell_potential(q3,order=order)
    assert abs(value-expected)<1e-11
    print('full action matches prior shell',value,flush=True)
    grad=jax.jit(jax.grad(f));g,lin=jax.linearize(grad,j.asarray(q));g=np.array(g)
    # Capture the primal spectral eigenspaces once; no finite-difference Hessian.
    batch=jax.jit(jax.vmap(lin));rows=[];eye=np.eye(297)
    for start in range(0,297,8):
        dirs=np.zeros((8,297));n=min(8,297-start);dirs[:n]=eye[start:start+n]
        rows.extend(np.array(batch(j.asarray(dirs)))[:n])
        if start%64==0:print('full Hessian rows',min(start+8,297),flush=True)
    H=np.array(rows);symmetry=float(np.max(abs(H-H.T)));assert symmetry<1e-10;H=(H+H.T)/2
    ga=V@A-A@V;gs=T@S+S@T.transpose(0,2,1)
    gauge=np.vstack([np.einsum('aij,bij->ab',V,ga)/2,2*np.einsum('aij,bij->ab',D.conj(),gs).real])
    assert np.linalg.norm(H@gauge)<1e-8
    U,sig,_=np.linalg.svd(gauge,full_matrices=True);rank=int(sum(sig>1e-9));assert rank==33
    N=U[:,rank:];normal=N.T@H@N;eigs=np.linalg.eigvalsh(normal);assert eigs[0]>0
    rng=np.random.default_rng(11634);controls=[]
    for _ in range(4):
        v=rng.normal(size=297);v/=np.linalg.norm(v);deltas=[]
        exact=float(v@H@v)
        for step in [1e-3,5e-4,2.5e-4]:
            fd=(float(jf(q+step*v))+float(jf(q-step*v))-2*value)/step**2
            deltas.append(fd)
        assert abs(deltas[-1]-exact)<3e-7
        controls.append(dict(direction=v.tolist(),AD_curvature=exact,finite_difference_curvatures=deltas))
    minmass=float(np.linalg.eigvalsh(.001*h).min());assert minmass>-.01
    return dict(status='PASS',passes=[11634],quadrature_order=order,SM_slice=q3.tolist(),canonical_background=q.tolist(),
        value=value,full_gradient_norm=float(np.linalg.norm(g)),full_Hessian=H.tolist(),Hessian_symmetry_error=symmetry,
        gauge_rank=rank,gauge_Ward_HG_norm=float(np.linalg.norm(H@gauge)),gauge_frame=gauge.tolist(),normal_frame=N.tolist(),
        normal_dimension=264,normal_eigenvalues=eigs.tolist(),minimum_normal_curvature=float(eigs[0]),all_normal_positive=bool(eigs[0]>0),
        minimum_scalar_denominator=.01+minmass,directional_controls=controls,
        derivative_rule='For F(H)=integral wx log(1+H/x), DF=Tr[f1(H)dH]; Df1=Q[L o(QT dH Q)]QT with Lij=-sum wx/((x+lami)(x+lamj)). Exact divided-difference identity, including equal eigenvalues; evaluated in float64.',
        scheme='Exactly the supplied11625 finite Landau-background shell:297scalars,45vectors with factor3; c=g^2=.001, k=.1,UV=.5, no fermions. Full canonical Hessian at the prior3-real stationary point, projected orthogonally to its33gauge tangents.',
        boundary='A numerical full-normal certificate in one declared one-loop finite-cutoff scheme; no interval bound, k->0 limit, MS pole spectrum, fermion contribution, gauge-independent global effective action, observed masses or derived coefficients. Prior tree positivity is exact and separately owned.' )

def produce(order=64,compare_order=None):
    reference=payload(compare_order) if compare_order is not None else None
    d=payload(order)
    if reference is not None:
        error=float(np.linalg.norm(np.array(d['full_Hessian'])-np.array(reference['full_Hessian']),2))
        assert error<1e-9
        d['quadrature_control']={'reference_order':compare_order,'Hessian_operator_norm_difference':error,'reference_normal_gap':reference['minimum_normal_curvature'],'reference_gradient_norm':reference['full_gradient_norm']}
    d['producer_sha256']=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    OUT.write_text(json.dumps(d,indent=2)+'\n');print('all264normal result',d['all_normal_positive'],d['minimum_normal_curvature'],flush=True)
    return d
if __name__=='__main__':produce(int(sys.argv[1]) if len(sys.argv)>1 else 64,int(sys.argv[2]) if len(sys.argv)>2 else None)
