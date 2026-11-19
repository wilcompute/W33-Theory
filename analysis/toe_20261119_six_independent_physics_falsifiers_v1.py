#!/usr/bin/env python3
"""Six independent TOE consistency gates. Exact finite models, not a TOE.
Run: python analysis/toe_20261119_six_independent_physics_falsifiers_v1.py
"""
import itertools, json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_six_independent_physics_falsifiers_v1.json"
sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1.,-1.]).astype(complex)
def dagger(x): return x.conj().T

def wilson_dirac(L,flux,m0=1.):
    """Wilson kernel on a periodic 2D torus with INTEGER magnetic flux."""
    N=L*L
    D=np.zeros((2*N,2*N),complex)
    site=lambda x,y: (x%L)*L+y%L
    for x in range(L):
        for y in range(L):
            i=site(x,y)
            D[2*i:2*i+2,2*i:2*i+2]+=(2-m0)*np.eye(2)
            for mu,(dx,dy,u) in enumerate([
              (1,0,np.exp(-2j*np.pi*flux*y/L**2)),
              (0,1,1. if y<L-1 else np.exp(2j*np.pi*flux*x/L))]):
                j=site(x+dx,y+dy)
                D[2*i:2*i+2,2*j:2*j+2]+=-.5*(np.eye(2)-[sx,sy][mu])*u
                D[2*j:2*j+2,2*i:2*i+2]+=-.5*(np.eye(2)+[sx,sy][mu])*np.conj(u)
    return D

def spinor_gate():
    data=[]
    for L in [4,6]:
        for flux in [-1,0,1]:
            D=wilson_dirac(L,flux)
            H=np.kron(np.eye(L*L),sz)@D
            err=np.linalg.norm(H-dagger(H))
            eig=np.linalg.eigvalsh(H)
            index=int(round(-np.sum(np.sign(eig))/2))
            assert err<1e-10 and index==-flux
            data.append({"L":L,"flux":flux,"overlap_index":index,
              "H_hermiticity_residual":float(err),
              "kernel_spectral_gap":float(np.min(abs(eig)))})
    return {"checks":len(data),"cases":data,
      "limitations":"Flux, 2D topology, gamma matrices and mass chosen externally; reflection positivity, 3+1 chirality and anomalies untested"}

def gravity_gate(n=5,m=1.3,alpha=.6):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    t=len(pairs); trace=[]; det=[]
    for mask in range(1<<t):
        A=np.zeros((n,n))
        for k,(i,j) in enumerate(pairs):
            if mask>>k&1:A[i,j]=1
        G=np.linalg.inv(m*np.eye(n)-alpha*A)
        trace.append(float(np.vdot(G,G).real))
        det.append(float(np.linalg.det(m*np.eye(n)-alpha*A)))
    strict=0
    for mask in range(1<<t):
        for k in range(t):
            if not mask>>k&1:
                assert trace[mask|(1<<k)]>trace[mask]+1e-10
                strict+=1
    assert max(det)-min(det)<1e-10
    # Entrywise nonnegative path count Neumann series proves global monotonicity.
    return {"event_count":n,"labeled_forward_graphs":1<<t,
      "single_edge_monotonicity_checks":strict,
      "determinant_spread":max(det)-min(det),
      "response_min":min(trace),"response_max":max(trace),
      "exact_claim":"For nonnegative edge weights, adding any forward edge strictly raises Tr(G dagger(G)); this biases positive action/weights toward dense DAGs",
      "limitations":"Labeled topological order fixed; graphs need not be transitively closed; this is not a continuum causal-set gravity measure"}

def su2(axis,theta):
    axis=np.asarray(axis,float)
    axis=axis/np.linalg.norm(axis)
    return expm(1j*theta*(axis[0]*sx+axis[1]*sy+axis[2]*sz))
def gauge_gate():
    rng=np.random.default_rng(20261119)
    maxerr=0.; records=[]
    for trial in range(48):
        edges=[su2(rng.normal(size=3),rng.uniform(-2,2)) for _ in range(4)]
        frames=[su2(rng.normal(size=3),rng.uniform(-2,2)) for _ in range(4)]
        W=edges[0]@edges[1]@dagger(edges[2])@dagger(edges[3])
        e=[edges[0],edges[1],dagger(edges[2]),dagger(edges[3])]
        et=[frames[j]@e[j]@dagger(frames[(j+1)%4]) for j in range(4)]
        Wt=et[0]@et[1]@et[2]@et[3]
        err=np.linalg.norm(Wt-frames[0]@W@dagger(frames[0]))
        maxerr=max(maxerr,float(err))
        assert err<1e-10
        if trial<2:records.append({"trace_W_real":float(np.trace(W).real),"frame_error":float(err)})
    return {"gauge_cases":48,"max_frame_error":maxerr,
      "sample_Wilson_traces":records,
      "limitations":"The link unitaries and causal paths are inputs, no Yang-Mills kinetic action derived"}

def qutrit_memory_gate():
    ghz=np.zeros(27,complex)
    for j in range(3):ghz[13*j]=1/np.sqrt(3)
    rho=np.outer(ghz,ghz.conj())
    klass=np.zeros((27,27),complex)
    for j in range(3):klass[13*j,13*j]=1/3
    def pair(r,drop):
        return np.trace(r.reshape((3,)*6),axis1=drop,axis2=drop+3).reshape(9,9)
    errs=[float(np.linalg.norm(pair(rho,k)-pair(klass,k))) for k in range(3)]
    X=np.zeros((3,3),complex)
    for j in range(3):X[(j+1)%3,j]=1
    XXX=np.kron(np.kron(X,X),X)
    coh=float(np.trace(XXX@rho).real)
    cl=float(np.trace(XXX@klass).real)
    assert max(errs)<1e-12 and abs(coh-1)<1e-12 and abs(cl)<1e-12
    return {"two_output_marginal_residuals":errs,"XXX_coherent":coh,
      "XXX_dephased":cl,
      "limitations":"Three-party GHZ coherence is not itself a causal process-tensor quantum-memory witness; arbitrary intermediate interventions not tested"}

def flavor_gate():
    mass=np.diag([1.,2.,4.]).astype(complex)
    a=np.array([1.,2j,3.],complex)
    b=np.array([2.,1+1j,-1j],complex)
    one=mass-np.outer(a,a.conj())/20
    two=one-np.outer(b,b.conj())/17
    cp=lambda H:float(np.imag(H[0,1]*H[1,2]*H[2,0]))
    assert abs(cp(one))<1e-12 and abs(cp(two))>1e-5
    # Distinct diagonal up masses make the cycle phase a CP-odd flavor
    # invariant; still not the physical Jarlskog normalized to SM masses.
    assert np.linalg.norm(one-dagger(one))<1e-12
    return {"one_heavy_mixing_row_CP_cycle":cp(one),
      "two_independent_heavy_rows_CP_cycle":cp(two),
      "limitations":"Heavy couplings arbitrary; no physical Yukawa or CKM fit; rank-one no-go previously identified in repo"}

def unitarity_gate():
    # Exact finite-dimensional Julia unitary dilation of a strict causal
    # contraction T. For forward-only triangular unitary on the SAME
    # Hilbert space, column orthogonality forces all non-diagonal entries zero.
    T=np.array([[0.,.35],[0.,0.]],complex)
    A=np.diag(np.sqrt(np.diag(np.eye(2)-T@dagger(T))))
    B=np.diag(np.sqrt(np.diag(np.eye(2)-dagger(T)@T)))
    U=np.block([[T,A],[B,-dagger(T)]])
    residual=float(np.linalg.norm(dagger(U)@U-np.eye(4)))
    assert residual<1e-12
    rng=np.random.default_rng(1119)
    controls=0
    for n in [2,3,5,8]:
        for _ in range(32):
            Q=np.eye(n,dtype=complex)+.02*np.triu(
                rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)),1)
            assert np.linalg.norm(dagger(Q)@Q-np.eye(n))>1e-9
            controls+=1
    return {"dilation_unitarity_error":residual,
      "nontrivial_triangular_unitary_rejections":controls,
      "theorem":"Finite triangular unitary matrix must be diagonal; nontrivial forward causal propagation as an operation needs layered time evolution, monitoring/postselection, or dilation",
      "limitations":"Dilation adds coherent ancilla and reverse amplitudes in larger Hilbert space; does not derive a unique microscopic dynamics"}

def run():
    results={
        "spinors":spinor_gate(),
        "gravity":gravity_gate(),
        "gauge":gauge_gate(),
        "temporal_qutrit":qutrit_memory_gate(),
        "matter_flavor":flavor_gate(),
        "unitary_causal_dilation":unitarity_gate(),
    }
    certificate={"research_date":"2026-11-19",
      "status":"SIX_FINITE_FALSIFICATION_TRACKS_PASSED_NOT_A_TOE",
      "novelty":"Mostly known theorems independently cross-tested; strongest synthesis is dense-DAG monotonicity plus triangular-unitary obstruction",
      "all_results":results,
      "source_comparison":["2026-11-19_causal_spectral_response_block_DAG_wilson.md","2026-11-19_TOE_five_keystone_falsifications_full_research.md"]}
    OUT.write_text(json.dumps(certificate,indent=2)+"\n",encoding="utf8")
    return certificate
if __name__=="__main__":
    c=run()
    print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk not in ("cases","sample_Wilson_traces")}) for k,v in c["all_results"].items()},indent=2))
    print("CERTIFICATE",OUT)
