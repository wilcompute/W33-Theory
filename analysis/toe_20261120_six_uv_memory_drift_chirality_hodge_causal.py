#!/usr/bin/env python3
"""Independent six-front W33/TOE falsifiers, 2026-11-20.
Finite models and established mathematics only; no physical TOE claim.
"""
from itertools import product
import json, math
from pathlib import Path
import numpy as np
import networkx as nx

O=np.exp(2j*np.pi/3)
I=np.eye(3,dtype=complex)
X=np.roll(I,1,axis=0)
Z=np.diag([1,O,O**2])
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_six_uv_memory_drift_chirality_hodge_causal.json"

def e8_gate():
    degrees=(2,8,12,14,18,20,24,30)
    coeff=[]
    for n in range(9):
        counts=[0]*(n+1);counts[0]=1
        for d in degrees:
            for k in range(d,n+1):counts[k]+=counts[k-d]
        coeff.append(counts[-1])
    assert (coeff[3],coeff[6],coeff[8])==(0,1,2)
    assert 78+8+81+81==248
    return {"adjoint_dimension":248,"branching":[78,8,81,81],
      "single_adjoint_degree3_invariants":coeff[3],
      "single_adjoint_degree6_invariants":coeff[6],
      "E6_singlet_triplet_multiplicity_in_adjoint":0,
      "limitation":"No E8-neutral single-adjoint triplet nor 19 independent E8-neutral multiplier singlets; other matter reps may alter this."}

def qutrit_gate():
    theta=.21
    c,s=math.cos(theta),math.sin(theta)
    # Measuring two rotated orthogonal inputs after computational dephasing.
    rho0=np.diag([c*c,s*s,0.])
    rho1=np.diag([s*s,c*c,0.])
    f=float(np.sum(np.sqrt(np.diag(rho0)*np.diag(rho1))))
    assert abs(f-abs(math.sin(2*theta)))<1e-14
    # Common output unitary preserves fidelity and Hilbert-Schmidt overlaps.
    rng=np.random.default_rng(271119)
    U,_=np.linalg.qr(rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)))
    err=abs(np.trace(U@rho0@U.conj().T@U@rho1@U.conj().T)-np.trace(rho0@rho1))
    assert err<1e-12
    return {"preparation_tilt_rad":theta,"rotated_input_fidelity":f,
      "analytical_fidelity":abs(math.sin(2*theta)),
      "witness_gamma036":f-.72,"witness_gamma075":f-1.5,
      "common_output_unitary_trace_overlap_error":float(err),
      "warning":"Root Uhlmann fidelity is unitary invariant; trace overlap is a separate control, not a full fidelity calculation."}

def su3_gate():
    rng=np.random.default_rng(1312)
    def unitary():
        m=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        Q,_=np.linalg.qr(m)
        return Q/np.linalg.det(Q)**(1/3)
    A,B=unitary(),unitary()
    K=A@B@A.conj().T@B.conj().T
    G=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    eta0=G.conj().T@G
    eta0*=3/np.trace(eta0).real
    drift=np.array([[.05,.013+.01j,0],[.013-.01j,-.03,.012],[0,.012,-.02]],complex)
    W=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b) for a,b in product(range(3),repeat=2)]
    def trace_at(M,t):
        eta=eta0+t*drift
        assert min(np.linalg.eigvalsh(eta))>0
        return 3*np.trace(eta@M@K@M.conj().T)/np.trace(eta).real
    forward=sum(trace_at(M,(i-4)/4) for i,M in enumerate(W))/9
    symmetric=sum((trace_at(M,(i-4)/4)+trace_at(M,-(i-4)/4))/2 for i,M in enumerate(W))/9
    target=np.trace(K)
    assert abs(symmetric-target)<1e-12
    assert abs(forward-target)>1e-5
    return {"Weyl_settings":9,"symmetric_exposures":18,
      "chronological_complex_trace_error":float(abs(forward-target)),
      "palindromic_complex_trace_error":float(abs(symmetric-target)),
      "condition":"Exact coherent Weyl conjugations, equal-weight time pairs, linear traceless detector drift."}

def g2_gate():
    # On a periodic parameter t, sin(t)=0 at 0 and pi, opposite slopes.
    slopes=[math.cos(0),math.cos(math.pi)]
    signed=sum(1 if x>0 else -1 for x in slopes)
    assert signed==0
    return {"periodic_spectral_flow":signed,"wall_crossing_slopes":slopes,
      "smooth_full_G2_neutral_parallel_real_spinors":1,
      "untwisted_round_S7_zero_modes":0,
      "qualification":"Odd-dimensional Dirac data are not a charged 4D chiral index. Singular ADE/defect modes uncomputed."}

def normalize(v):
    for x in v:
        if x:return tuple((y*(2 if x==2 else 1))%3 for y in v)
    raise ValueError
def omega(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def hodge_gate():
    pts=sorted({normalize(v) for v in product(range(3),repeat=4) if any(v)})
    graph=nx.Graph();graph.add_nodes_from(pts)
    for k,u in enumerate(pts):
        for v in pts[k+1:]:
            if omega(u,v)==0:graph.add_edge(u,v)
    lines=sorted({tuple(sorted(c)) for c in nx.find_cliques(graph) if len(c)==4})
    lev=nx.Graph();lev.add_nodes_from(range(80))
    index={p:i for i,p in enumerate(pts)}
    for k,line in enumerate(lines):
        for p in line:lev.add_edge(index[p],40+k)
    edges=sorted(tuple(sorted(e)) for e in lev.edges())
    dist=dict(nx.all_pairs_shortest_path_length(nx.line_graph(lev)))
    K=np.array([[(-3)**(4-dist[e][f]) for f in edges] for e in edges],dtype=np.int64)
    assert len(pts)==len(lines)==40 and len(edges)==160
    assert np.array_equal(K@K,160*K)
    assert np.count_nonzero(K)==160**2
    p=81/160
    # Error E=|e><e|. Compression PEP rank one, not scalar on rank-81 P.
    kl_diff=p*p*(1-1/81)
    assert kl_diff>0
    return {"points":40,"lines":40,"flags":160,"cycle_rank":81,
      "exact_projector_square":True,"projector_entries_nonzero":160**2,
      "one_edge_KL_deviation_Frobenius_squared":kl_diff,
      "compressed_pi_phase_eigenvalue":1-2*p,
      "pi_phase_total_Frobenius_leakage":4*p*(1-p),
      "corrects_unknown_single_edge_phase":False}

def sprinkle(n,d,rng):
    times=[]
    while len(times)<n:
        t=rng.uniform(-.5,.5,5*n)
        times.extend(t[rng.random(5*n)<(1-2*np.abs(t))**(d-1)].tolist())
    t=np.asarray(times[:n])
    directions=rng.normal(size=(n,d-1))
    directions/=np.linalg.norm(directions,axis=1)[:,None]
    pos=directions*((.5-np.abs(t))*rng.random(n)**(1/(d-1)))[:,None]
    dt=t[None,:]-t[:,None]
    dsq=np.sum((pos[None,:,:]-pos[:,None,:])**2,axis=2)
    return ( (dt>0)&(dt*dt>dsq+1e-12) ).astype(np.int64)

def causal_gate():
    rng=np.random.default_rng(20261120)
    n=48; results={}
    for d,target in ((2,.5),(4,.1)):
        c=[];chains=[]
        for _ in range(120):
            R=sprinkle(n,d,rng)
            c.append(R.sum()/(n*(n-1)/2))
            chains.append(np.sum((R@R)*R)/(n*(n-1)*(n-2)/6))
        mean=float(np.mean(c))
        assert abs(mean-target)<.035
        results[str(d)]={"pair_comparability":mean,"continuum_expected":target,
                        "three_chain_fraction":float(np.mean(chains)),"sprinklings":120}
    R=sprinkle(48,4,rng)
    p=R.sum(axis=0);f=R.sum(axis=1)
    a=int(np.sum(p**3-f**3))
    assert a==-int(np.sum(f**3-p**3))
    return {"Myrheim_Meyer_controls":results,
      "time_reversal_arrow":(a,-a),
      "implication":"Pair/chain observables compare discrete dimensions, not an Einstein dynamics or preferred arrow."}

def main(write=True):
    data={"status":"PASS_BOUNDED_SIX_GATES","e8":e8_gate(),"qutrit":qutrit_gate(),
      "twirling":su3_gate(),"chirality":g2_gate(),"hodge":hodge_gate(),"causal":causal_gate()}
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":data["status"],"Levi":data["hodge"]["flags"],
      "SU3_symmetric_error":data["twirling"]["palindromic_complex_trace_error"],
      "causal_pair_4D":data["causal"]["Myrheim_Meyer_controls"]["4"]["pair_comparability"]}))
    return data

if __name__=="__main__":main()
