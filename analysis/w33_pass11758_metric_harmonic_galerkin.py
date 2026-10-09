"""Finite-basis CY/HYM/harmonic experiment, not a certified physical vacuum.

11742 owns K and its holomorphic cup;11750 owns the named polynomial and
closed type2 input. Global smoothness of this snapshot is still unproved.
Galerkin minimization is classical; no priority claim for the method.
"""
from __future__ import annotations
from functools import lru_cache
import itertools as it
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11750_11757_integral_geometry_and_flux_dynamics as Q
N=Q.N


@lru_cache(None)
def polynomial_terms():
    z,F,_,_=Q.reference_polynomial()
    return tuple((tuple(a),float(c)) for a,c in s.Poly(F,*z).terms())


def chart_polynomial(z,bits,derivative=None):
    """Homogeneous polynomial evaluated in any of the16 product charts."""
    z=np.asarray(z);out=np.zeros(z.shape[:-1],complex)
    for a,c in polynomial_terms():
        e=np.where(bits,2-np.array(a),a).copy()
        if derivative is not None:
            c*=e[...,derivative];e[...,derivative]-=1
        out+=c*np.prod(z**np.maximum(e,0),axis=-1)
    return out


def sample_hypersurface(seed=11758,nbase=512):
    """Product-FS base sampling; both roots and explicit residue weights.

    The affine root parameterization has branch points of measure zero.
    Effective sample size and block uncertainty diagnose its large weights.
    """
    rng=np.random.default_rng(seed)
    homogeneous=rng.normal(size=(nbase,3,2))+1j*rng.normal(size=(nbase,3,2))
    bits=abs(homogeneous[:,:,1])>abs(homogeneous[:,:,0])
    u=np.where(bits,homogeneous[:,:,1],homogeneous[:,:,0])
    v=np.where(bits,homogeneous[:,:,0],homogeneous[:,:,1]);base=v/u
    points=[];charts=[]
    for z0,b0 in zip(base,bits):
        coeff=np.zeros(3,complex)
        for a,c in polynomial_terms():
            e=np.where(b0,2-np.array(a[:3]),a[:3])
            coeff[a[3]]+=c*np.prod(z0**e)
        for root in np.roots(coeff[::-1]):
            flip=abs(root)>1
            points.append([*z0,1/root if flip else root]);charts.append([*b0,flip])
    z=np.array(points);bits=np.array(charts)
    grad=np.stack([chart_polynomial(z,bits,i) for i in range(4)],axis=-1)
    A=np.zeros((len(z),4,3),complex);A[:,:3]=np.eye(3);A[:,3]=-grad[:,:3]/grad[:,3,None]
    weight=np.prod((1+abs(z[:,:3])**2)**2,axis=1)/abs(grad[:,3])**2
    return dict(z=z,bits=bits,grad=grad,A=A,weight=weight,
                polynomial_residual=float(np.max(abs(chart_polynomial(z,bits)))))


@lru_cache(None)
def bloch_jets():
    z,b=s.symbols('z b');k=1+z*b
    ns=((z+b)/k,(z-b)/(s.I*k),(1-z*b)/k)
    return s.lambdify((z,b),[[f,s.diff(f,z),s.diff(f,b),s.diff(f,z,b)] for f in ns],'numpy')


def potential_basis(z,bits,max_support=2):
    """26 or71 globally smooth invariant scalars and ambient Hessians.

    n_ia*n_ja (18) and n_ia²-n_iz² (8). Their ddbar corrections preserve
    the Kahler class; sampled positivity is not a global positivity proof.
    """
    count=len(z);jets=np.empty((count,4,3,4),complex)
    for i in range(4):
        arr=np.array(bloch_jets()(z[:,i],z[:,i].conj()))
        jets[:,i]=arr.transpose(2,0,1)
        # Under a chart inversion the global Bloch y,z reverse sign.
        sign=np.where(bits[:,i],-1,1)
        jets[:,i,1:]*=sign[:,None,None]
    vals=[];hs=[]
    for i in range(4):
        for a in (0,1):
            n,dz,db,h=jets[:,i,a].T
            nz,dzz,dbz,hz=jets[:,i,2].T
            H=np.zeros((count,4,4),complex)
            H[:,i,i]=2*(dz*db+n*h-dzz*dbz-nz*hz)
            vals.append(n*n-nz*nz);hs.append(H)
    chars=((-1,1),(-1,-1),(1,-1))
    for support_size in range(2,max_support+1):
        for support in it.combinations(range(4),support_size):
            for axes in it.product(range(3),repeat=support_size):
                if any(np.prod([chars[a][q] for a in axes])!=1 for q in range(2)):continue
                factors=[jets[:,i,a].T for i,a in zip(support,axes)]
                H=np.zeros((count,4,4),complex)
                for r,i in enumerate(support):
                    H[:,i,i]=factors[r][3]*np.prod([f[0] for j,f in enumerate(factors) if j!=r],axis=0)
                    for t,j in enumerate(support):
                        if r==t:continue
                        others=[f[0] for k,f in enumerate(factors) if k not in (r,t)]
                        H[:,i,j]=factors[r][2]*factors[t][1]*(np.prod(others,axis=0) if others else 1)
                vals.append(np.prod([f[0] for f in factors],axis=0));hs.append(H)
    return np.stack(vals,axis=1).real,np.stack(hs,axis=1)


def geometry(data,max_support=2):
    z,A=data['z'],data['A'];t=np.array([float(s.N(v)) for v in N.flavor_certificate()['positive_Kahler_point']])
    h=t/(1+abs(z)**2)**2
    g=np.einsum('nki,nk,nkj->nij',A.conj(),h,A)
    vals,H=potential_basis(z,data['bits'],max_support)
    hb=np.einsum('nki,nbkl,nlj->nbij',A.conj(),H,A)
    return g,vals,hb


def metric_loss(c,g,hb,grad3,w):
    gg=g+np.einsum('b,nbij->nij',c,hb)
    eig=np.linalg.eigvalsh(gg)
    if eig.min()<=0:return 1e6+1e6*float((np.minimum(eig,0)**2).sum()),np.zeros_like(c)
    inv=np.linalg.inv(gg);logeta=np.log(np.linalg.det(gg).real*abs(grad3)**2)
    w=w/w.sum();res=logeta-w@logeta
    deriv=np.einsum('nij,nbji->nb',inv,hb).real
    ridge=1e-6
    return float(w@(res*res)+ridge*c@c),2*np.einsum('n,nb->b',w*res,deriv)+2*ridge*c


def fit_metric(train,validation,max_support=2):
    g,v,hb=geometry(train,max_support);gv,vv,hv=geometry(validation,max_support)
    fun=lambda c:metric_loss(c,g,hb,train['grad'][:,3],train['weight'])
    result=minimize(fun,np.zeros(hb.shape[1]),jac=True,method='BFGS',options={'maxiter':180,'gtol':1e-7})
    # A finite training set can miss loss of positivity. Dampen against an
    # independent validation set, recording the accepted scale explicitly.
    scale=1.
    while np.linalg.eigvalsh(gv+np.einsum('b,nbij->nij',result.x*scale,hv)).min()<=0:
        scale*=.5
    c=result.x*scale
    def diagnostics(d,g,hb):
        gg=g+np.einsum('b,nbij->nij',c,hb);w=d['weight'];w=w/w.sum()
        eta=np.linalg.det(gg).real*abs(d['grad'][:,3])**2
        log=np.log(eta);base=np.log(np.linalg.det(g).real*abs(d['grad'][:,3])**2)
        return dict(reference_log_density_variance=float(w@((base-w@base)**2)),
                    corrected_log_density_variance=float(w@((log-w@log)**2)),
                    min_sample_metric_eigenvalue=float(np.linalg.eigvalsh(gg).min()),
                    weighted_relative_MA_rms=float(np.sqrt(w@((eta/(w@eta)-1)**2))),
                    effective_residue_samples=float(1/(w@w)),polynomial_residual=d['polynomial_residual'])
    return c,dict(basis_dimension=len(c),maximum_factor_support=max_support,optimizer_success=bool(result.success),iterations=int(result.nit),
                  validation_damping=scale,coefficients=c.tolist(),train=diagnostics(train,g,hb),
                  validation=diagnostics(validation,gv,hv))


def fit_hym(data,metric_coeff,validation):
    def objects(d):
        g,v,h=geometry(d,4 if len(metric_coeff)>26 else 2);gg=g+np.einsum('b,nbij->nij',metric_coeff,h);gi=np.linalg.inv(gg)
        lap=np.einsum('nij,nbji->nb',gi,h).real
        A=d['A'];curv=np.array(N.K)[:,None,:]/(1+abs(d['z'])[None,:,:]**2)**2
        f=np.einsum('nki,lnk,nkj->lnij',A.conj(),curv,A)
        source=np.einsum('nij,lnji->nl',gi,f).real
        weight=d['weight']*np.linalg.det(gg).real*abs(d['grad'][:,3])**2
        return v,lap,source,weight/weight.sum(),gg
    v,L,src,w,_=objects(data)
    coeff=np.linalg.lstsq(L*np.sqrt(w[:,None]),src*np.sqrt(w[:,None]),rcond=1e-10)[0]
    coeff[:,2]=-coeff[:,0]-coeff[:,1]
    def diag(d):
        v,L,src,w,g=objects(d);res=src-L@coeff
        return dict(reference_rms=np.sqrt(w@(src*src)).tolist(),corrected_rms=np.sqrt(w@(res*res)).tolist(),
                    mean_reference_source=(w@src).tolist(),beta_product_max=float(abs((v@coeff).sum(axis=1)).max()))
    return coeff,dict(metric='H_i=prod kappa_j^(-K_ij) exp(beta_i); F_i=-ddbar log H_i',
                      coefficients=coeff.tolist(),train=diag(data),validation=diag(validation),
                      scope='Finite least-squares HYM correction on the approximate metric; nonzero validation residuals are retained.')


@lru_cache(None)
def reference_form_functions():
    z,F,_,_=Q.reference_polynomial();b=s.symbols('b:4');k=[1+x*y for x,y in zip(z,b)]
    vectors=[N.character_vector(a,(1,1)) for a in N.cohomology_actions()]
    f1=sum(vectors[0][2*i+j]*z[1]**i*z[2]**j for i,j in it.product(range(2),repeat=2))/k[0]**2
    f2=sum(vectors[1][2*i+j]*b[1]**i*z[3]**j for i,j in it.product(range(2),repeat=2))/k[1]**3
    _,_,forms=Q.type2_forms();f3=4*(forms[0,0]+forms[1,1])
    return [s.lambdify((*z,*b),f,'numpy') for f in (f1,f2,f3)]


def reference_forms(d):
    z,bits,A=d['z'],d['bits'],d['A'];north=np.where(bits,1/z,z)
    out=[]
    for k,component,f in zip(N.K,(0,1,3),reference_form_functions()):
        fiber=np.prod(np.where(bits,z**np.array(k),1),axis=1)
        formchart=np.where(bits[:,component],-1/z[:,component].conj()**2,1)
        value=f(*north.T,*north.conj().T)*fiber*formchart
        out.append(value[:,None]*A[:,component,:].conj())
    return out


def exact_form_basis(k,z,bits,A):
    """dbar of global invariant smooth line sections, minimal tensor basis."""
    inds=list(it.product(*[range(abs(a)+1) for a in k]));used=set();rows=[]
    for a in inds:
        if a in used or sum(a)%2:continue
        partner=tuple(abs(ki)-ai for ki,ai in zip(k,a));used|={a,partner}
        total=np.zeros((len(z),4),complex)
        for aa in set((a,partner)):
            v=[];db=[]
            for i,ki in enumerate(k):
                e=np.where(bits[:,i],abs(ki)-aa[i],aa[i]);zi=z[:,i];bar=zi.conj();kap=1+abs(zi)**2
                if ki>=0:
                    v.append(zi**e);db.append(np.zeros(len(z),complex))
                else:
                    m=-ki;v.append(bar**e/kap**m)
                    db.append(np.where(e>0,e*bar**np.maximum(e-1,0)/kap**m,0)-m*zi*bar**e/kap**(m+1))
            for j in range(4):
                total[:,j]+=db[j]*np.prod([v[i] for i in range(4) if i!=j],axis=0)
        rows.append(np.einsum('nk,nkj->nj',total,A.conj()))
    return np.stack(rows,axis=1)


def fit_harmonic(train,validation,metric_coeff,beta_coeff):
    def objects(d):
        g,v,h=geometry(d,4 if len(metric_coeff)>26 else 2);g=g+np.einsum('b,nbij->nij',metric_coeff,h);gi=np.linalg.inv(g)
        w=d['weight']*np.linalg.det(g).real*abs(d['grad'][:,3])**2;w/=w.sum()
        H=np.prod((1+abs(d['z'])**2)[:,None,:]**(-np.array(N.K)[None,:,:]),axis=2)*np.exp(v@beta_coeff)
        return gi,w,H,reference_forms(d)
    gi,w,H,refs=objects(train);giv,wv,Hv,refv=objects(validation);cert=[]
    for family,k in enumerate(N.K):
        D=exact_form_basis(k,train['z'],train['bits'],train['A'])
        Dv=exact_form_basis(k,validation['z'],validation['bits'],validation['A'])
        # (0,1)-covectors pair with the inverse metric in conjugate order.
        gram=np.einsum('n,nbj,njk,nck->bc',w*H[:,family],D.conj(),gi.conj(),D)
        rhs=np.einsum('n,nbj,njk,nk->b',w*H[:,family],D.conj(),gi.conj(),refs[family])
        c=-np.linalg.pinv(gram,rcond=1e-10)@rhs
        def diag(nu,D,gi,w,H):
            corrected=nu+np.einsum('b,nbj->nj',c,D)
            raw=np.einsum('nj,njk,nk->n',nu.conj(),gi.conj(),nu).real*H
            norm=np.einsum('nj,njk,nk->n',corrected.conj(),gi.conj(),corrected).real*H
            return dict(reference_norm=float(w@raw),corrected_norm=float(w@norm))
        cert.append(dict(family=family+1,exact_form_trial_dimension=len(c),gram_rank=int(np.linalg.matrix_rank(gram)),
                         coefficients=[[float(x.real),float(x.imag)] for x in c],
                         galerkin_stationarity=float(np.linalg.norm(gram@c+rhs)),
                         train=diag(refs[family],D,gi,w,H[:,family]),
                         validation=diag(refv[family],Dv,giv,wv,Hv[:,family])))
    norms=[a['validation']['corrected_norm'] for a in cert]
    residue_norm=float(2*np.mean(validation['weight']))
    raw_proxy=float(.5/np.sqrt(np.prod(norms)))
    return dict(families=cert,geometry_only_coupling_proxy=float(.5/np.sqrt(np.prod(norms))),
                residue_norm_without_universal_measure_constant=residue_norm,
                F_rescaling_invariant_geometry_proxy=raw_proxy/np.sqrt(residue_norm),
                convention='Residue/Serre holomorphic cup=1/2; kinetic norms are CY-volume averages. The4D supergravity factor is not supplied.',
                scope='Finite trial-space weak harmonic minimization, not a global harmonicity certificate or predicted mass.')


@lru_cache(None)
def numerical_certificate():
    train=sample_hypersurface(11758,512);validation=sample_hypersurface(21758,512)
    c,metric=fit_metric(train,validation);beta,hym=fit_hym(train,c,validation)
    harmonic=fit_harmonic(train,validation,c,beta)
    fine=sample_hypersurface(31758,2048);test=sample_hypersurface(41758,2048)
    cf,mf=fit_metric(fine,test);bf,hf=fit_hym(fine,cf,test);ff=fit_harmonic(fine,test,cf,bf)
    convergence=dict(seeds=[31758,41758],base_samples_each=2048,root_samples_each=4096,
        metric=mf,HYM=hf,harmonic=ff,
        relative_normalization_proxy_change=float(ff['F_rescaling_invariant_geometry_proxy']/harmonic['F_rescaling_invariant_geometry_proxy']-1))
    ce,me=fit_metric(fine,test,4);be,he=fit_hym(fine,ce,test);fe=fit_harmonic(fine,test,ce,be)
    return dict(status='PASS',seeds=[11758,21758],base_samples_each=512,root_samples_each=1024,
        metric=metric,HYM=hym,harmonic=harmonic,
        independent_larger_run=convergence,
        enriched_basis_run=dict(metric=me,HYM=he,harmonic=fe,
            relative_normalization_proxy_change=float(fe['F_rescaling_invariant_geometry_proxy']/ff['F_rescaling_invariant_geometry_proxy']-1)),
        training_executed=True,certified_Ricci_flat_HYM_harmonic_solution=False,
        physical_normalized_Yukawa_certified=False,snapshot_global_smoothness_certified=False,
        scope='An executed reproducible approximation with validation residuals. No small residual, global positivity, smoothness, quadrature convergence, physical coupling or vacuum selection is assumed.')


if __name__=='__main__':
    value=numerical_certificate()
    value['source_sha256']=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    value['prior_source_sha256']={str(Path(mod.__file__).relative_to(ROOT)):hashlib.sha256(Path(mod.__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for mod in (Q,N)}
    out=ROOT/'data/w33_pass11758_metric_harmonic_galerkin.json';out.write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(value,indent=2));print(out)
