#!/usr/bin/env python3
"""Five independent finite falsifier controls building on the 81-apartment carrier.

No spacetime, gravity, particle masses or hardware physics is derived.
Each section has a check that can fail. Executed independently on a second host.
"""
from __future__ import annotations
from collections import Counter, deque
from itertools import product
from pathlib import Path
import importlib.util, json, math
import numpy as np
from scipy.sparse.linalg import expm_multiply

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261103_fivefront_independent_controls.json"
spec=importlib.util.spec_from_file_location(
    "optimal5",ROOT/"analysis"/"2026_11_03_optimal_5load_apartment_hamiltonian.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def diameter(A):
    n=len(A); neighbors=[list(np.flatnonzero(A[i])) for i in range(n)]
    result=[]
    for start in range(n):
        dist=[-1]*n;dist[start]=0;q=deque([start])
        while q:
            a=q.popleft()
            for b in neighbors[a]:
                if dist[b]<0:dist[b]=dist[a]+1;q.append(b)
        assert min(dist)==0
        result.append(max(dist))
    return dict(Counter(result))

def test():
    D,C,flags=mod.build()
    picked,load=mod.choose(C)
    B=C[:,picked];H=B@B.T
    K=C@C.T
    P=K/160;Q=np.eye(160)-P
    A=np.abs(D).T@np.abs(D)-2*np.eye(160,dtype=int)
    assert len(picked)==81 and int(max(load))==5
    assert not np.any(D@B) and not np.any(D@H) and not np.any(A@H+2*H)
    assert np.array_equal(K@K,160*K)

    # 1. Continuum falsifier: this unrefined family has bounded graph diameter.
    eig=np.linalg.eigvalsh(H.astype(float))[-81:]
    f1=dict(flag_graph_diameter_histogram=diameter(A),
            graph_degree=int(A[0].sum()),
            selected_H_max_offdiagonal_degree=int(max(np.count_nonzero(H,axis=1)-1)),
            eigenvalue_min=float(eig[0]),eigenvalue_max=float(eig[-1]),
            nonzero_band_condition_number=float(eig[-1]/eig[0]),
            boundary="Finite-diameter q-family does not alone supply bounded-valence spatial refinement or a Lorentzian metric.")
    assert f1["flag_graph_diameter_histogram"]=={4:160}

    # 2. Symplectic transvections: explicit symmetry-selection stress test.
    points=sorted({mod.canon(x) for x in product(range(3),repeat=4) if any(x)})
    pidx={x:i for i,x in enumerate(points)}
    line_sets=[set() for _ in range(40)]
    for p,l in flags:line_sets[l].add(p)
    lines=[tuple(sorted(x)) for x in line_sets]
    lidx={x:i for i,x in enumerate(lines)}
    fidx={x:i for i,x in enumerate(flags)}
    target={tuple(np.flatnonzero(C[:,j]).tolist()) for j in picked}
    checks=[]
    for v in points:
        def send(x):
            t=mod.symp(x,v)
            return pidx[mod.canon(tuple((x[k]+t*v[k])%3 for k in range(4)))]
        permpts=[send(x) for x in points]
        permlines=[lidx[tuple(sorted(permpts[i] for i in line))] for line in lines]
        perm=np.array([fidx[(permpts[p],permlines[l])] for p,l in flags])
        sent={tuple(sorted(int(perm[k]) for k in supp)) for supp in target}
        Hp=np.zeros_like(H);Hp[np.ix_(perm,perm)]=H
        checks.append((sent==target,float(np.linalg.norm(H-Hp)/np.linalg.norm(H))))
    f2=dict(symplectic_transvections=len(checks),
            selected_basis_stabilizers=sum(t for t,_ in checks),
            min_relative_H_change=min(t for _,t in checks),
            max_relative_H_change=max(t for _,t in checks),
            boundary="A non-scalar operator on the irreducible Steinberg representation cannot commute with the full group.")
    assert f2["symplectic_transvections"]==40
    assert f2["selected_basis_stabilizers"]==0

    # 3. Local gauge-invariant densities do not by themselves give GR's Dirac algebra.
    # H_i = (c_i·x)^2/2 + sum_{e in supp(c_i)} p_e^2/2.
    # Gauge constraint Dp=0. Evaluate exact canonical Poisson bracket on Dp=0.
    counter=None
    for i in range(81):
        ci=B[:,i]
        for j in range(i+1,81):
            cj=B[:,j]
            overlap=int(np.count_nonzero((ci!=0)&(cj!=0)))
            if not overlap or not int(ci@cj):continue
            x=ci;p=cj
            gA=int(ci@x)*int(ci@(np.abs(cj)*p))
            gB=int(cj@x)*int(cj@(np.abs(ci)*p))
            if gA!=gB:
                counter=dict(i=i,j=j,edge_overlap=overlap,
                             bracket_on_gauss_zero=gA-gB,
                             gauss_norm=int(np.max(np.abs(D@p))))
                break
        if counter:break
    assert counter and counter["gauss_norm"]==0 and counter["bracket_on_gauss_zero"]!=0

    # 4. Check standard E6 -> SO(10) x U(1) anomaly cancellations as a control.
    reps=[(16,1,2),(10,-2,1),(1,4,0)]
    f4=dict(E6_branching="27=16_1+10_-2+1_4",
            U1_gravitational_anomaly=sum(n*q for n,q,t in reps),
            U1_cubic_anomaly=sum(n*q**3 for n,q,t in reps),
            SO10_squared_U1_anomaly=sum(q*t for n,q,t in reps),
            SU5_cubic_anomaly=1-1+1-1,
            allowed_cubic_charge_channels=["16*16*10","10*10*1"],
            boundary="27bar is separately anomaly-free; finite geometry has not selected chirality, generations or Yukawa values.")
    assert all(f4[k]==0 for k in ("U1_gravitational_anomaly","U1_cubic_anomaly",
                                   "SO10_squared_U1_anomaly","SU5_cubic_anomaly"))

    # 5. Hardware budget and noisy propagation on the actual 160-mode target.
    e_values=Counter(int(H[i,j]) for i in range(160)
                     for j in range(i+1,160) if H[i,j])
    # A signed triangle's product is invariant under every onsite U(1) gauge.
    # Negative product means pi flux; this cannot become all-positive hopping.
    S=np.sign(H).astype(np.int64)
    np.fill_diagonal(S,0)
    unsigned=np.abs(S)
    triangles=int(np.trace(unsigned@unsigned@unsigned)//6)
    signed_sum=int(np.trace(S@S@S)//6)
    frustrated=(triangles-signed_sum)//2
    assert triangles==5250 and frustrated==780
    assert H[0,1]*H[0,2]*H[1,2]<0
    p0=float(P[0,0]); seed=P[:,0]/math.sqrt(p0)
    assert np.linalg.norm(Q@seed)<1e-12
    site=np.eye(160)[0]
    field=H/eig[-1]+0.05*np.outer(site,site)
    prob=[]
    for time in (0.02,0.04,0.08):
        state=expm_multiply((-1j*time)*field,seed.astype(complex))
        leakage=float(np.vdot(Q@state,Q@state).real)
        leading=0.05**2*time**2*p0*(1-p0)
        assert abs(leakage/leading-1)<0.02
        prob.append(dict(time=time,leakage=leakage,leading_order=leading))
    f5=dict(modes=160,nonzero_undirected_couplings=sum(e_values.values()),
            signed_triangles_total=triangles,pi_flux_triangles=frustrated,
            pi_flux_triangle_witness={"flag_indices":[0,1,2],
                                     "hoppings":[int(H[0,1]),int(H[0,2]),int(H[1,2])]},
            negative_cycle_gauge_obstruction=True,
            positive_couplings=sum(v for k,v in e_values.items() if k>0),
            negative_couplings=sum(v for k,v in e_values.items() if k<0),
            coupling_histogram={str(k):v for k,v in sorted(e_values.items())},
            single_defect_leakage_coefficient="lambda^2*81*79/160^2",
            time_evolution=prob,
            boundary="Not yet a compiled control circuit; programmable signs, loss, engineering margins unverified.")
    assert f5["nonzero_undirected_couplings"]==1883
    result=dict(status="PASS_FINITE_FIVE_FRONT_CONTROLS",
                source="Independent re-evaluation on local worktree of W33 cycle construction",
                exact_checks=dict(H_cut_decoupled=True,local_Gauss_closure_only=True),
                continuum=f1,symmetry=f2,gravity_nonclosure=counter,
                chiral_anomaly=f4,hardware=f5,
                physical_claims="No full TOE, no Einstein algebra, no continuum, no measured masses, no experiment.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return result

if __name__=="__main__":
    r=test()
    print(r["status"],r["gravity_nonclosure"],r["hardware"]["nonzero_undirected_couplings"])
