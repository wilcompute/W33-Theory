"""New low-rank squeezed quantum Gaussian trial over each classical W33 star.
No lower bound or true vacuum eigenstate is inferred. Restricted to real
Gaussian covariances on W with two star-adapted eigen-directions.
"""
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import w33_pass11769_quantized_current_vacuum as H
def anchor(vertex,U,V):
    q=np.zeros(80,dtype=np.int64)
    if vertex<40:q[:40]=-1;q[vertex]=39
    else:q[40:]=1;q[vertex]=-39
    X=V@q+40
    active=np.flatnonzero(X)
    assert len(active)==4
    pn=-40*U[active].sum(axis=0)
    Y=U@pn+40*7680
    assert np.all(X*Y==0)
    # Centers in the mean-zero point/line 78-space W.
    q0=q/math.sqrt(20)
    p0=pn/(7680*math.sqrt(20))
    return q0,p0

def compact(U,V,vertex):
    q,p=anchor(vertex,U,V)
    e=q/np.linalg.norm(q)
    ortho=p-e*np.dot(e,p)
    assert np.linalg.norm(ortho)>1e-8
    f=ortho/np.linalg.norm(ortho)
    uu=U/40; vv=V/40; b=1/math.sqrt(20)
    A=(vv@q+b)**2; B=(uu@p+b)**2
    v0=np.einsum('ij,ij->i',vv,vv);u0=np.einsum('ij,ij->i',uu,uu)
    ve=(vv@e)**2;vf=(vv@f)**2
    ue=(uu@e)**2;uf=(uu@f)**2
    def energy(x):
        t0,t1,t2=np.exp(x)
        vq=(t0*v0+(t1-t0)*ve+(t2-t0)*vf)/2
        up=(u0/t0+(1/t1-1/t0)*ue+(1/t2-1/t0)*uf)/2
        return float(np.sum((A+vq)*(B+up)))
    starts=[[0,0,0],[1,1,1],[0,2,-2],[0,-2,2],[-1,2,2],[1,-1,2]]
    tries=[minimize(energy,np.array(x,dtype=float),method='BFGS',options={'gtol':1e-8,'maxiter':250}) for x in starts]
    best=min(tries,key=lambda x:x.fun)
    isotropic=minimize(lambda x:energy(np.array([x[0]]*3)),[0.],method='BFGS')
    return {"star":vertex,"minimum_low_rank_real_gaussian":float(best.fun),
            "covariance_eigenvalues":[float(t) for t in np.exp(best.x)],
            "gradient_inf":float(np.max(np.abs(best.jac))),"solver_success":bool(best.success),
            "isotropic_star_gaussian_optimum":float(isotropic.fun),
            "stationarity_not_global_proof":True}
def main():
    g=H.geometry()
    U=np.rint(40*g['u']).astype(np.int64);V=np.rint(40*g['v']).astype(np.int64)
    samples=[compact(U,V,i) for i in (0,1,39,40,41,79)]
    assert max(x['minimum_low_rank_real_gaussian'] for x in samples)-min(x['minimum_low_rank_real_gaussian'] for x in samples)<1e-5
    assert all(x['minimum_low_rank_real_gaussian']<x['isotropic_star_gaussian_optimum'] for x in samples)
    old=H.exact_trial()
    result=dict(status="PASS",sampled_stars=samples,total_stars=80,
        prior_centered_nonstar_complex_gaussian_energy=old['energy'],
        restricted_method="Schrodinger real Gaussian on 78-space, covariance with star-q and star-p 2-plane eigenvalues t1,t2 and t0 on 76D orthogonal complement; exact Wick expectation evaluated numerically and optimized with six seeds.",
        rigorous_variational_logic="Each explicitly stated positive covariance defines a normalized Schwartz-state upper bound for the spectral infimum, even when optimizer stationarity is not rigorously certified.",
        limitation="This restricted covariance family can fail to find true E0. Comparison with prior non-Gaussian Ritz trial is a variational bound only. No spontaneous vacuum selection, continuum EFT, or mass gap.")
    t=ROOT/'data/w33_20261009_round18_classical_star_squeezed_trial.json'
    t.write_text(json.dumps(result,indent=2)+'\n')
    print("STAR",[(z['star'],z['minimum_low_rank_real_gaussian'],z['isotropic_star_gaussian_optimum']) for z in samples],"OLD",old['energy'],flush=True)
if __name__=='__main__':main()
