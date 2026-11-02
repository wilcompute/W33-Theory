#!/usr/bin/env python3
"""2026-11-02: execute five independent W33 frontiers with explicit falsifiers.

Computes a 216-mode adjacent-Givens Naimark isometry compiler, the 15D
operator-kernel projector, a canonical cubic-adjoint counterexample, a
prime-seven positive-eigenspace witness, and normalized-Laplacian limits.
Physical device/cubic Jordan claims are explicitly NOT inferred.
"""
from __future__ import annotations
import sys, math, json, gzip, random
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
import w33_20261102_route_216_cubic_tomography as old
from even_line_sets_gf import build

def route_frame():
    pts,lines,N,ix,norm,omega=old.geometry()
    lid={frozenset(L):j for j,L in enumerate(lines)}
    seed=frozenset(old.SEED);seen={seed};front=[seed];gen=[]
    for a in pts:
        gp=[ix[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts]
        gen.append(tuple(lid[frozenset(gp[j] for j in L)] for L in lines))
    while front:
        nxt=[]
        for S in front:
            for perm in gen:
                T=frozenset(perm[j] for j in S)
                if T not in seen:seen.add(T);nxt.append(T)
        front=nxt
    assert len(seen)==216
    B=np.zeros((216,40),dtype=np.int64)
    for i,S in enumerate(sorted(seen,key=lambda S:tuple(sorted(S)))):B[i,list(S)]=1
    cov=B@N.T
    assert np.all((cov==0)|(cov==2))
    return cov-1,N

def compile_mesh(Z):
    W=(Z.T@Z).astype(float)
    e,vec=np.linalg.eigh(W)
    assert np.max(abs(e[:16]))<1e-8 and np.max(abs(e[16:]-360))<1e-8
    V=Z@vec[:,16:]/math.sqrt(360)
    for k in range(24):
        j=np.argmax(abs(V[:,k]))
        if V[j,k]<0:V[:,k]*=-1
    assert np.max(abs(V.T@V-np.eye(24)))<5e-12
    R=V.copy()
    mesh=[]
    for j in range(24):
        for i in range(215,j,-1):
            a,b=float(R[i-1,j]),float(R[i,j])
            t=math.hypot(a,b)
            c,s=(1.,0.) if t<1e-15 else (a/t,b/t)
            ra=R[i-1,:].copy();rb=R[i,:].copy()
            R[i-1,:]=c*ra+s*rb
            R[i,:]=-s*ra+c*rb
            mesh.append([i-1,c,s])
    ideal=np.zeros_like(R);ideal[:24,:]=np.eye(24)
    residual=float(np.max(abs(R-ideal)))
    assert len(mesh)==4884 and residual<1e-10
    Q=ideal.copy()
    for a,c,s in reversed(mesh):
        ra=Q[a].copy();rb=Q[a+1].copy()
        Q[a]=c*ra-s*rb
        Q[a+1]=s*ra+c*rb
    err=float(np.max(abs(Q-V)))
    assert err<1e-10 and np.max(abs(Q.T@Q-np.eye(24)))<1e-10
    p=ROOT/"data/w33_20261102_adjacent_givens_mesh.json.gz"
    with gzip.open(p,"wt",encoding="utf-8",compresslevel=9) as f:
        json.dump({"schema":"w33.20261102.naimark_givens_mesh.v1",
          "input_modes":24,"output_modes":216,
          "order":"apply in reverse listing to rectangular mode injection",
          "rotations":[[int(a),float(c),float(s)] for a,c,s in mesh]},f)
    # Whole-frame POVM fidelity under bounded fixed-angle perturbation
    rng=np.random.default_rng(20261102)
    calibrated={}
    for sd in (0.,0.0001,0.001):
        X=ideal.copy()
        for a,c,s in reversed(mesh):
            theta=math.atan2(s,c)+rng.normal(0,sd)
            c1,s1=math.cos(theta),math.sin(theta)
            ra=X[a].copy();rb=X[a+1].copy()
            X[a]=c1*ra-s1*rb
            X[a+1]=s1*ra+c1*rb
        assert np.max(abs(X.T@X-np.eye(24)))<1e-10
        calibrated[str(sd)]={"max_isometry_element_error":float(np.max(abs(X-V))),
           "frobenius_isometry_error":float(np.linalg.norm(X-V)),
           "completeness_error":float(np.max(abs(X.T@X-np.eye(24))))}
    return {"input_dimension":24,"output_modes":216,"adjacent_rotations":len(mesh),
        "max_reconstruction_error":err,"max_qr_residual":residual,
        "angle_error_rms_trials_radians":calibrated,
        "mesh_file":str(p.relative_to(ROOT)),
        "scope":"216-mode real orthogonal interferometer compiler, not a 24-mode-only detector or a validated hardware layout."}

def blind_space(Z):
    K=(Z@Z.T)**2
    vals,vec=np.linalg.eigh(K.astype(float))
    assert np.max(abs(vals[:15]))<1e-7
    expected={0:15,576:15,768:81,2304:80,3168:24,14400:1}
    measured={k:int(np.sum(np.abs(vals-k)<1e-5)) for k in expected}
    assert measured==expected
    P=vec[:,:15]@vec[:,:15].T
    diag=np.diag(P);val=15/216
    assert np.max(abs(diag-val))<1e-10
    assert np.linalg.norm(P@P-P)<1e-10
    assert np.linalg.norm(K@P)<1e-5
    return {"exact_null_rank_from_CRT":15,"blind_leverage_each_outcome":"5/72",
        "max_numerical_blind_leverage_deviation":float(np.max(abs(diag-val))),
        "null_projector_idempotence_residual":float(np.linalg.norm(P@P-P)),
        "operator_span_dim":201,"real_symmetric_operator_dim":300,"complex_hermitian_operator_dim":576,
        "scope":"15-dimensional kernel on measurement outcomes; not a proof of irreducible group-module type."}

def cubic_counterexample(Z):
    x=(Z.T@Z)[:,0]//12+(Z.T@Z)[:,1]//12
    assert np.array_equal((Z.T@Z)@x,360*x)
    def adj(w):return Z.T@((Z@w)**2)
    q=adj(x)
    qq=adj(q)
    norm=int(np.sum((Z@x)**3))
    assert norm==0 and np.any(qq)
    # For a cubic Jordan norm with the Euclidean metric inducing this sharp
    # map, sharp(sharp(x))=N(x)x; fails already at N(x)=0.
    return {"test_vector_indexed":"(ZtZ[:,0]+ZtZ[:,1])/12",
       "cubic_value":norm,"adjoint_nonzero":bool(np.any(q)),
       "adjoint_of_adjoint_nonzero":bool(np.any(qq)),
       "adjoint_twice_max_abs":int(np.max(abs(qq))),
       "canonical_euclidean_sharp_identity_holds":False,
       "scope":"Only the canonical frame-metric quadratic gradient; general trace form / 27D embedding NOT excluded."}

def q7_probe():
    pts,lines,N=build(7)
    assert N.shape==(400,400)
    src=json.loads((ROOT/"analysis/search_drivers_12466/even_line_sets_gf_q7_sym2.json").read_text())
    pid={p:i for i,p in enumerate(pts)}
    lid={frozenset(L):i for i,L in enumerate(lines)}
    S=frozenset(lid[frozenset(pid[tuple(v)] for v in L)] for L in src["chosen_lines"])
    assert len(S)==40
    counts=N[:,list(S)].sum(1)
    assert np.count_nonzero(counts==2)==160 and np.count_nonzero(counts==0)==240
    A=(N@N.T).astype(np.int64)-8*np.eye(400,dtype=np.int64)
    h=counts//2;x=5*h-2
    assert np.array_equal(A@x,6*x)
    assert int(x@x)==2400
    def omega(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%7
    def norm(v):
        f=next(z for z in v if z)
        return tuple(t*pow(f,-1,7)%7 for t in v)
    rng=random.Random(20261102)
    gens=[]
    for a in [pts[j] for j in (0,1,2,3,5,7,11,13,17,19,23,29,31,37,41,43)]:
        gp=[pid[norm(tuple((u[k]+omega(u,a)*a[k])%7 for k in range(4)))] for u in pts]
        gens.append(tuple(lid[frozenset(gp[i] for i in L)] for L in lines))
    seen={S};current=S
    for trial in range(5000):
        g=gens[rng.randrange(len(gens))]
        current=frozenset(g[i] for i in current)
        if trial%2==0:seen.add(current)
    assert len(seen)>100
    # Subset observations are nonuniform: do NOT call them the full orbit.
    for S in seen:
        t=N[:,list(S)].sum(1)
        assert np.count_nonzero(t==2)==160 and np.count_nonzero(t==0)==240
        y=5*(t//2)-2
        assert np.array_equal(A@y,6*y)
    return {"q":7,"points":400,"lines":400,"weight":40,
        "seed_even_coverage":True,"fixed_point_eigenvalue":6,
        "centered_integer_sign":"5 H - 2","squared_norm":2400,
        "distinct_random_walk_supports_verified":len(seen),
        "full_symplectic_orbit_size_from_parallel_certificate":720300,
        "conditional_full_orbit_covariance_coefficient":308700,
        "positive_eigenspace_dim":224,
        "scope":"One seed + nonuniform random walk; NOT exhaustive enumeration or proof of 720300 orbit."}

def continuum():
    values=[]
    for q in (3,5,7,9,11,101):
        k=q*(q+1)
        p=1-(q-1)/k
        m=1+1/q
        values.append({"q":q,"v":(q+1)*(q*q+1),"adjacency_eigenvalues":[k,q-1,-(q+1)],
           "normalised_laplacian_nonzero_eigenvalues":[p,m],
           "normalised_spectral_gap":p})
    assert all(v["normalised_spectral_gap"]>0.8 for v in values)
    return {"status":"NO_GAPLESS_LIMIT_FOR_BARE_W3Q_NORMALISED_LAPLACIAN",
        "diameter_for_all_q_at_least_2":2,
        "gap_limit_as_q_to_infinity":1,
        "tables":values,
        "scope":"Only bare point-graph normalized Laplacian; weighted covers/towers/other operators not ruled out."}

def main():
    Z,N=route_frame()
    assert Z.shape==(216,40)
    data={"status":"PASS_FIVE_DEEPER_FRONTS_AND_GAPS",
       "optical_compiler":compile_mesh(Z),"effect_blind_sector":blind_space(Z),
       "albert_cubic_euclidean_adjoint":cubic_counterexample(Z),
       "q7":q7_probe(),"continuum":continuum()}
    p=ROOT/"data/w33_20261102_five_deeper_fronts.json"
    p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    for key in list(data)[1:]:print(key,json.dumps(data[key])[:1000],flush=True)
    print(data["status"],flush=True)
    return data
if __name__=="__main__":main()
