"""TOE65 front5: true native EDGE-product adversarial flux robustness.

238 explicit length-eight cycles -> 238x160 actual edge-incidence matrix.
Optimize the smallest exact weighted holonomy Hessian eigenvalue over all
160 independent positive edge amplitudes. This is exploratory, NOT global
certification or optimal threshold.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ED,V,*_=prep();ED=np.asarray(ED,int);V=np.asarray(V,int)
assert ED.shape==(160,2) and V.shape==(160,3)

def enumerate_winding_cycles():
    adj=[[] for _ in range(80)]
    for e,(a,b) in enumerate(ED):
        adj[a].append((b,e,1));adj[b].append((a,e,-1))
    cx=[];wx=[];allcounts=0
    for root in range(80):
        def walk(path,eids,w):
            nonlocal allcounts
            u=path[-1]
            if len(path)==8:
                for b,e,s in adj[u]:
                    if b!=root or path[1]>=u:continue
                    allcounts+=1
                    wt=tuple(map(int,w+s*V[e]))
                    if wt!=(0,0,0):
                        assert len(eids)==7
                        cx.append(eids+[e]);wx.append(wt)
                return
            for nxt,e,s in adj[u]:
                if nxt<=root or nxt in path:continue
                walk(path+[nxt],eids+[e],w+s*V[e])
        for b,e,s in adj[root]:
            if b>root:walk([root,b],[e],s*V[e])
    assert allcounts==1620 and len(cx)==238
    C=np.zeros((238,160),dtype=np.float64)
    for i,row in enumerate(cx):
        assert len(set(row))==8
        C[i,row]=1.
    w=np.asarray(wx,int)
    sign=np.where(w.sum(axis=1)%2,1.,-1.)
    assert int(sum(sign==1))==233 and int(sum(sign==-1))==5
    return C,w,sign

C,W,SGN=enumerate_winding_cycles()

def hessian(log_weights):
    coeff=SGN*np.exp(C@log_weights)
    return np.einsum("i,ij,ik->jk",coeff,W,W)

def objective(x):
    coeff=SGN*np.exp(C@x)
    H=np.einsum("i,ij,ik->jk",coeff,W,W)
    ev,q=np.linalg.eigh(H)
    vec=q[:,0]
    grads=C.T@(coeff*(W@vec)**2)
    return float(ev[0]),grads

def phase_gap(log_weights,theta):
    coeff=SGN*np.exp(C@log_weights)
    return float(np.dot(coeff,1-np.cos(W@theta)))

def certificate():
    rng=np.random.default_rng(651064)
    H0=hessian(np.zeros(160))
    assert np.allclose(H0,[[77,-1,-1],[-1,73,3],[-1,3,73]])
    sweeps=[]
    for eps in (.148,.20,.30,.45,.60):
        bounds=[(np.log(1-eps),np.log(1+eps))]*160
        trials=[]
        for trial in range(5):
            x=(np.zeros(160) if trial==0 else rng.uniform(bounds[0][0],bounds[0][1],160))
            ans=minimize(objective,x,jac=True,bounds=bounds,method="L-BFGS-B",
                         options={"maxiter":110,"ftol":1e-10,"gtol":1e-7})
            lam=float(ans.fun)
            eigvec=np.linalg.eigh(hessian(ans.x))[1][:,0]
            # Finite phase displacement in the least-stable direction.
            phase=float(phase_gap(ans.x,0.04*eigvec))
            # The minimum of the smallest eigenvalue over each ONE edge
            # magnitude (all others fixed) occurs at one endpoint, since
            # H is affine in that edge and lambda_min is concave.
            # Round the numerical optimizer to a rational cube vertex.
            pattern=(ans.x>(bounds[0][0]+bounds[0][1])/2).astype(int)
            endpoints=np.where(pattern,1+eps,1-eps)
            Hvertex=hessian(np.log(endpoints))
            vertex_eig,vertex_vec=np.linalg.eigh(Hvertex)
            trials.append({"min_hessian_eigenvalue":lam,
                           "small_displacement_leading_gap":phase,
                           "iterations":int(ans.nit),
                           "edge_corner_pattern":pattern.tolist(),
                           "vertex_rounded_min_eigenvalue":float(vertex_eig[0]),
                           "vertex_direction":vertex_vec[:,0].tolist(),
                           "grad_inf":float(max(abs(objective(ans.x)[1]))),
                           "optimizer_success":bool(ans.success)})
        best=min(trials,key=lambda z:z["min_hessian_eigenvalue"])
        sweeps.append({"epsilon":eps,"number_starts":len(trials),
                       "trial_eigenvalues":[x["min_hessian_eigenvalue"] for x in trials],
                       "best":best})
        print("TOE65 EDGEPRODUCT eps",eps,"minEig",best["min_hessian_eigenvalue"],"phasegap",best["small_displacement_leading_gap"],flush=True)
    # independently check the signed W matrix follows expected Fourier census.
    from collections import Counter
    freq=Counter(tuple(sorted([tuple(t),tuple(-t)])[0]) for t in W)
    assert sum(freq.values())==238 and sorted(freq.values())==[1,1,3,77,77,79]
    # At e=3/10 all edge magnitudes are exact rationals: 7/10 or 13/10.
    # Integer numerator H_int=10^8*H(pi), verified without floating
    # eigensolvers. A negative integer Rayleigh quotient is an exact
    # counterexample to universal local stability at 30% disorder.
    best30=next(z["best"] for z in sweeps if z["epsilon"]==0.30)
    pattern=np.asarray(best30["edge_corner_pattern"],dtype=int)
    highs=(C@pattern).astype(int)
    multipliers=np.asarray([13**int(k)*7**(8-int(k)) for k in highs],dtype=np.int64)
    H_integer=np.einsum("i,ij,ik->jk",(SGN.astype(np.int64)*multipliers),W,W)
    q=np.rint(1000*np.asarray(best30["vertex_direction"])).astype(np.int64)
    assert np.any(q!=0)
    integer_rayleigh=int(q@H_integer@q)
    assert integer_rayleigh<0,(integer_rayleigh,best30["vertex_rounded_min_eigenvalue"])
    exact_edge_weights=np.where(pattern,1.3,.7)
    delta=.01*q/np.linalg.norm(q)
    realized_gap=phase_gap(np.log(exact_edge_weights),delta)
    assert realized_gap<0
    rational_witness={"epsilon_rational":"3/10","low_weight_rational":"7/10",
                      "high_weight_rational":"13/10",
                      "high_edge_bits":pattern.tolist(),
                      "integer_test_direction":q.tolist(),
                      "integer_hessian_10pow8":H_integer.tolist(),
                      "exact_integer_rayleigh_numerator":integer_rayleigh,
                      "small_displacement_delta":delta.tolist(),
                      "negative_leading_term_gap":realized_gap,
                      "native_edges":160}
    return {"status":"PASS_TOE65_EXPLICIT_EDGE_PRODUCT_HESSIAN_SEARCH",
            "rational_30_percent_counterexample":rational_witness,
            "native_edges":160,"native_winding_cycles":238,
            "eight_edge_memberships_per_cycle":8,
            "unweighted_flux_hessian":H0.astype(int).tolist(),
            "adversarial_bounded_link_sweeps":sweeps,
            "scope":"Derivative-checked numerical local minimization in 160 edge weights at five epsilon values, not proof of optimal W33 disorder threshold, no certified global search, all-temperature result or physical device tolerance. Failure to find negative eigenvalue is NOT evidence of universal positivity."}
if __name__=="__main__":
    q=certificate()
    (ROOT/"data/w33_20261013_toe65_edge_product_adversary.json").write_text(json.dumps(q,indent=2)+"\n")
