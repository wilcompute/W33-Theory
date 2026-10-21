#!/usr/bin/env python3
"""Five W33/RH followups: exact finite audits plus analytic falsifiers.

Run: OPENBLAS_NUM_THREADS=1 python analysis/w33_20261021_rh_five_followups.py
Produces JSON certificate + compressed complete 160x156 integer embedding.
Classical RH is not proved.
"""
from __future__ import annotations
import base64
import hashlib
import itertools
import json
import math
import sys
import zlib
from pathlib import Path
import mpmath as mp
import numpy as np

def norm(v):
    a=next(int(x) for x in v if x)
    return tuple(int(x*a)%3 for x in v)

def sym(x,y):
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def geometry():
    points=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(points)==40
    idx={p:i for i,p in enumerate(points)}
    lines=set()
    for i,j in itertools.combinations(range(40),2):
        if sym(points[i],points[j]):continue
        line=frozenset(idx[norm(tuple((a*x+b*y)%3 for x,y in zip(points[i],points[j])))]
                       for a,b in itertools.product(range(3),repeat=2) if a or b)
        assert len(line)==4
        lines.add(line)
    lines=sorted(lines,key=lambda s:tuple(sorted(s)))
    assert len(lines)==40
    A=np.zeros((40,40),dtype=np.int64)
    N=np.zeros((40,40),dtype=np.int64)
    edge_line={}
    for k,line in enumerate(lines):
        for i in line:N[i,k]=1
        for i,j in itertools.combinations(sorted(line),2):
            A[i,j]=A[j,i]=1
            edge_line[(i,j)]=k
    assert np.array_equal(N@N.T,A+4*np.eye(40,dtype=np.int64))
    assert np.array_equal(A@A,8*np.eye(40,dtype=np.int64)-2*A+
                          4*np.ones((40,40),dtype=np.int64))
    return points,lines,A,N,edge_line

def rank_mod_p_columns(M,p=101,return_solver=False):
    piv={}
    n=M.shape[1]
    for i in range(n):
        w=M[:,i].copy()%p
        c=np.zeros(n,dtype=np.int64);c[i]=1
        for k,(v,b) in piv.items():
            if w[k]:
                a=int(w[k]);w=(w-a*v)%p;c=(c-a*b)%p
        nz=np.flatnonzero(w)
        if not len(nz):continue
        k=int(nz[0]);q=pow(int(w[k]),-1,p)
        piv[k]=((w*q)%p,(c*q)%p)
    if not return_solver:return len(piv)
    def solve(v):
        w=np.array(v,dtype=np.int64)%p
        sol=np.zeros(n,dtype=np.int64)
        for k,(b,c) in piv.items():
            if w[k]:
                a=int(w[k]);w=(w-a*b)%p;sol=(sol+a*c)%p
        if np.any(w):raise ValueError("outside span")
        return sol
    return piv,solve

def levi_intertwiner(points,lines,A,N):
    I=np.eye(80,dtype=np.int64);Z=np.zeros((40,40),dtype=np.int64)
    L=np.block([[Z,N],[N.T,Z]])
    L2=L@L
    assert not np.any(L2@(L2-6*I)@(L2-16*I))
    Q6=L2@(16*I-L2)
    Q0=(L2-6*I)@(L2-16*I)
    T=np.block([[L,-3*I],[I,np.zeros((80,80),dtype=np.int64)]])
    columns=[];chosen={4:[],2:[]}
    R=np.zeros((156,156),dtype=np.int64)
    for Q,d,constant,needed in ((Q6,4,-9,24),(Q0,2,-3,30)):
        for gen in range(160):
            v=np.zeros(160,dtype=np.int64)
            if gen<80:v[:80]=Q[:,gen]
            else:v[80:]=Q[:,gen-80]
            orbit=[]
            for k in range(d):
                orbit.append(v);v=T@v
            assert np.array_equal(v,constant*orbit[0])
            candidate=columns+orbit
            if rank_mod_p_columns(np.column_stack(candidate))!=len(candidate):continue
            off=len(columns)
            columns.extend(orbit);chosen[d].append(gen)
            for k in range(d):
                if k<d-1:R[off+k+1,off+k]=1
                else:R[off,off+k]=constant
            if len(chosen[d])==needed:break
        assert len(chosen[d])==needed
    C=np.column_stack(columns)
    assert C.shape==(160,156)
    assert np.array_equal(T@C,C@R)
    assert rank_mod_p_columns(C)==156
    w=points[0];idx={pt:k for k,pt in enumerate(points)}
    line_idx={line:j for j,line in enumerate(lines)}
    perm=[idx[norm(tuple((u+sym(pt,w)*v)%3 for u,v in zip(pt,w)))]
          for pt in points]
    perm_l=[line_idx[frozenset(perm[i] for i in line)] for line in lines]
    assert len(set(perm))==len(set(perm_l))==40
    G=np.zeros((80,80),dtype=np.int64)
    for i,j in enumerate(perm):G[j,i]=1
    for i,j in enumerate(perm_l):G[40+j,40+i]=1
    assert np.array_equal(G@L,L@G)
    GH=np.block([[G,np.zeros_like(G)],[np.zeros_like(G),G]])
    assert np.array_equal(GH@T,T@GH)
    piv,solver=rank_mod_p_columns(C,return_solver=True)
    D=np.column_stack([solver(GH@C[:,i]) for i in range(156)])
    assert not np.any((C@D-GH@C)%101)
    assert not np.any((D@R-R@D)%101)
    assert not np.any(D[:96,96:]) and not np.any(D[96:,:96])
    raw=C.astype("<i4").tobytes(order="C")
    digest=hashlib.sha256(raw).hexdigest()
    artifact={
        "dtype":"<i4","shape":[160,156],"compression":"zlib+base64",
        "data":base64.b64encode(zlib.compress(raw,level=9)).decode(),
        "sha256_raw":digest,
        "column_order":"24 quartic length-4 blocks then 30 quadratic length-2 blocks",
        "note":"Full 160x156 integer embedding. Select independent 156 rows for a square rational coordinate transform."
    }
    # Materialize an actual invertible 156x156 coordinate matrix, not just the embedding.
    selected=list(piv.keys())
    C_square=C[selected,:]
    assert C_square.shape==(156,156)
    assert rank_mod_p_columns(C_square)==156
    square_raw=C_square.astype("<i4").tobytes(order="C")
    square_sha=hashlib.sha256(square_raw).hexdigest()
    artifact.update({
        "coordinate_square_shape":[156,156],
        "coordinate_square_data":base64.b64encode(zlib.compress(square_raw,level=9)).decode(),
        "coordinate_square_sha256":square_sha
    })
    return ({
        "status":"PASS","dimension":156,"blocks_quartic":24,"blocks_quadratic":30,
        "integer_intertwining":True,"rank_mod101":156,
        "symplectic_transvection_commutes":True,
        "induced_action_commutes_mod101":True,"matrix_sha256":digest,
        "artifact_shape":[160,156],"selected_rows_mod101":selected,
        "square_coordinate_rank_mod101":156,"square_coordinate_sha256":square_sha,
        "generators_quartic":chosen[4],"generators_quadratic":chosen[2],
        "geometric_point_permutation":perm,"geometric_line_permutation":perm_l,
        "scope":"Abstract rational operator module; no canonical geometric/Galois-equivariant curve map"
    },artifact)

def completed_weil_resolvent():
    mp.mp.dps=75
    sigma=[mp.mpf(v) for v in ("1.1","1.25","1.5","2","3","5")]
    def arch(s):
        return 1/s+1/(s-1)-mp.log(mp.pi)/2+mp.digamma(s/2)/2
    def prime(s):
        return -mp.diff(mp.zeta,s)/mp.zeta(s)
    def xi_log(s):
        return arch(s)-prime(s)
    K=mp.matrix([[(xi_log(a)+xi_log(b))/(a+b-1)
                  for b in sigma] for a in sigma])
    ev=mp.eigsy(K,eigvals_only=True)
    assert min(ev)>0
    roots=[mp.mpf(".5")+e*mp.mpf(".2")+f*mp.mpc(0,14)
           for e in (1,-1) for f in (1,-1)]
    Q=mp.matrix([[mp.re(sum(1/((a-r)*(b-(1-r))) for r in roots))
                  for b in sigma] for a in sigma])
    qe=mp.eigsy(Q,eigvals_only=True)
    assert qe[0]<0
    return {
        "status":"PASS","sigma":[str(s) for s in sigma],
        "smallest_completed_kernel_eigenvalue":mp.nstr(ev[0],28),
        "largest_completed_kernel_eigenvalue":mp.nstr(ev[len(ev)-1],24),
        "off_line_quartet_smallest_eigenvalue":mp.nstr(qe[0],23),
        "prime_term_first":mp.nstr(prime(sigma[0]),23),
        "gamma_endpoint_term_first":mp.nstr(arch(sigma[0]),23),
        "completed_xi_log_derivative_first":mp.nstr(xi_log(sigma[0]),23),
        "identity":"K_ij=[xi'/xi(si)+xi'/xi(sj)]/(si+sj-1), xi'/xi=A-(-zeta'/zeta)",
        "test_family":"Mellin transforms 1/(sigma-s), noncompact power functions, not all Weil tests",
        "scope":"Six-point numerical kernel and negative control only, not global Weil positivity"
    }

def formal_hecke(A):
    I=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
    P1=3*J;P24=80*I+20*A-8*J;P15=40*I-20*A+5*J
    assert np.array_equal(P1+P24+P15,120*I)
    for P in (P1,P24,P15):assert np.array_equal(P@P,120*P)
    for P,Q in ((P1,P24),(P1,P15),(P24,P15)):assert not np.any(P@Q)
    primes=[2,3,5,7,11,13]
    for p in primes:
        assert abs(2)<2*p**1.5 and abs(-4)<2*p**1.5
        Hp=(1+p**3)*P1+2*P24-4*P15
        assert np.array_equal(Hp@A,A@Hp)
        Hpp=Hp@Hp-120*120*p**3*I
        rhs=((1+p**3)**2-p**3)*P1@P1+(4-p**3)*P24@P24+(16-p**3)*P15@P15
        assert np.array_equal(Hpp,rhs)
    return {
        "status":"PASS","three_projector_ranks":[1,24,15],
        "toy_prime_eigenvalues":{"constant":"1+p^3","rank24":"2","rank15":"-4"},
        "tested_primes":primes,
        "all_nonconstant_toy_coefficients_within_weight4_Deligne_bound":True,
        "scope":"Formal commutative Hecke recurrence only; no modular eigenform, motive, all-prime continuation or RH"
    }

def apartments(A,N,edge_line):
    flags=list(zip(*np.nonzero(N)))
    eidx={(p,li):i for i,(p,li) in enumerate(flags)}
    assert len(eidx)==160
    result=set()
    for x,y in itertools.combinations(range(40),2):
        if A[x,y]:continue
        common=[z for z in range(40) if A[x,z] and A[y,z]]
        for a,b in itertools.combinations(common,2):
            path=(x,a,y,b)
            mask=0;lset=set()
            for u,v in zip(path,path[1:]+path[:1]):
                li=edge_line[tuple(sorted((u,v)))];lset.add(li)
                mask^=(1<<eidx[(u,li)])|(1<<eidx[(v,li)])
            assert len(lset)==4 and mask.bit_count()==8
            result.add(mask)
    assert len(result)==1620
    return sorted(result),flags

def pivots_GF2(masks):
    p={}
    for m in masks:
        x=m
        while x:
            i=x.bit_length()-1
            if i not in p:p[i]=x;break
            x^=p[i]
    return p

def holonomy(A,N,edge_line):
    cycles,flags=apartments(A,N,edge_line)
    piv=pivots_GF2(cycles)
    assert len(piv)==81==160-80+1
    cols=[0]*160
    for k,m in enumerate(cycles):
        for j in range(160):
            if m>>j&1:cols[j]|=1<<k
    assert {x.bit_count() for x in cols}=={81}
    from collections import Counter
    distances=Counter((cols[i]^cols[j]).bit_count()
                      for i in range(160) for j in range(i+1,160))
    assert dict(distances)=={108:480,144:1440,156:4320,160:6480}
    rng=np.random.default_rng(20261021)
    Z=np.zeros((40,40),dtype=np.float64);radii=[]
    for _ in range(32):
        signs=rng.choice([-1.,1.],size=160)
        signed=np.zeros((40,40),dtype=np.float64)
        for (p,li),s in zip(flags,signs):signed[p,li]=s
        L=np.block([[Z,signed],[signed.T,Z]])
        radii.append(float(np.max(abs(np.linalg.eigvalsh(L)))))
    return {
        "status":"PASS","apartment_count":1620,"incidence_edges":160,
        "cycle_rank":81,"GF2_apartment_span_rank":len(piv),
        "number_of_gauge_classes":"2^81","one_edge_syndrome_weight":81,
        "two_edge_syndrome_distance_census":dict(sorted(distances.items())),
        "random_signing_trials":len(radii),
        "random_tempered_count":sum(r<=2*math.sqrt(3)+1e-9 for r in radii),
        "sample_radius_min":min(radii),"sample_radius_max":max(radii),
        "scope":"Apartment holonomies separate gauge classes; tempered signing classification remains open"
    }

def spectral_benchmark():
    mp.mp.dps=60
    k=1200
    def ladder(n):
        x=mp.mpf(n)-mp.mpf(7)/8
        return float(2*mp.pi*x/mp.lambertw(x/mp.e))
    t0=np.array([ladder(n) for n in range(1,k+1)])
    th1=math.acos(1/math.sqrt(11));th2=math.acos(-2/math.sqrt(11))
    t1=t0+np.array([.05*(24*math.cos(n*th1)+15*math.cos(n*th2))/39
                     for n in range(1,k+1)])
    assert min(t1)>0 and np.max(abs(t1-t0))<=0.05000000001
    zeros=np.array([float(mp.im(mp.zetazero(n))) for n in range(1,21)])
    errors={}
    for name,t in (("baseline",t0),("W33_scalar",t1)):
        errors[name]={
            "mean_first20_relative_error":float(np.mean(abs(t[:20]-zeros)/zeros)),
            "inverse_spectral_moments":{str(2*j):float(np.sum(t**(-2*j)))
                                        for j in (1,2,3)},
            "finite_det_values":{str(s):float(np.prod(1-(s/t)**2))
                                  for s in (2,4,6)}
        }
    def xi(t):
        s=mp.mpf(".5")+1j*t
        return mp.mpf(".5")*s*(s-1)*mp.power(mp.pi,-s/2)*mp.gamma(s/2)*mp.zeta(s)
    classical={str(t):float(mp.re(xi(t)/xi(0))) for t in (2,4,6)}
    errs={name:{s:abs(row["finite_det_values"][s]/val-1)
                for s,val in classical.items()} for name,row in errors.items()}
    return {
        "status":"PASS","n_levels":k,"zero_count_uninflated":True,
        "max_W33_modulation":.05,"finite_model_data":errors,
        "Xi_ratio_at_test_points":classical,"finite_det_relative_errors":errs,
        "bounded_scalar_perturbation_compact_resolvent":True,
        "scope":"Finite diagnostic products, not an exact Xi determinant or arithmetic triple"
    }

def run(out=None):
    points,lines,A,N,edge_line=geometry()
    levi,embedding=levi_intertwiner(points,lines,A,N)
    fronts={
        "rational_levi_intertwiner":levi,
        "completed_weil_resolvent":completed_weil_resolvent(),
        "formal_hecke_obstruction":formal_hecke(A),
        "Levi_apartment_gauge":holonomy(A,N,edge_line),
        "infinite_spectral_benchmark":spectral_benchmark(),
    }
    assert all(v["status"]=="PASS" for v in fronts.values())
    report={"status":"PASS_SCOPED","date":"2026-10-21",
            "classical_RH_proved":False,"frontiers":fronts}
    if out is not None:
        out=Path(out);out.mkdir(parents=True,exist_ok=True)
        (out/"w33_20261021_rh_five_followups.json").write_text(
            json.dumps(report,indent=2,sort_keys=True)+"\n")
        (out/"w33_20261021_rational_levi_160x156.json").write_text(
            json.dumps(embedding,sort_keys=True)+"\n")
    return report

if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    target=Path(sys.argv[1]) if len(sys.argv)>1 else root/"data"
    payload=run(target)
    for k,v in payload["frontiers"].items():print(k,v["status"])
    print("Classical RH proved:",payload["classical_RH_proved"])
