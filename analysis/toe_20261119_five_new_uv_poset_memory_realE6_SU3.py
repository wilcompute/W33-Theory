#!/usr/bin/env python3
"""Five TOE falsification controls, Nov 19 2026.
Finite mathematics and toy quantum channels; no physical TOE.
Requires numpy and sympy. Run from any directory.
"""
import itertools,json
from pathlib import Path
from collections import defaultdict
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_five_new_uv_poset_memory_realE6_SU3.json"

def uv_gate():
    degrees=(2,8,12,14,18,20,24,30)
    h=[1]+[0]*12
    for d in degrees:
        for i in range(d,13): h[i]+=h[i-d]
    assert h[6]==1 and h[3]==0 and h[8]==2
    # For 9 qutrit SIC rays with weights w_i:
    # Tr(S²)-(Tr S)²/3 = [9*sum(w²)-(sum w)²]/12.
    # By Cauchy, this vanishes for nonzero w only if all 9 equal.
    om=np.exp(2j*np.pi/3)
    rays=[]
    for missing in range(3):
        active=[i for i in range(3) if i!=missing]
        for phase in range(3):
            v=np.zeros(3,complex);v[active]=[1,om**phase]
            rays.append(v/np.sqrt(2))
    projectors=[np.outer(v,v.conj()) for v in rays]
    assert np.linalg.norm(sum(projectors)-3*np.eye(3))<1e-12
    err=0.
    for mask in range(1,512):
        m=mask.bit_count()
        S=sum((projectors[j] for j in range(9) if mask>>j&1),np.zeros((3,3),complex))
        dev=float(np.linalg.norm(S-m*np.eye(3)/3)**2)
        expected=m*(9-m)/12
        err=max(err,abs(dev-expected))
        assert abs(dev-expected)<1e-12
        assert m==9 or dev>1e-10
    # The E6 symmetric cubic d_ABC times SU3 epsilon_ijk vanishes
    # for a single commuting (27,3) superfield by exchange antisymmetry.
    # A single SL3(C) triplet has no nonconstant polynomial invariants:
    # the group acts transitively on its nonzero vectors.
    return {"E8_single_adjoint_basic_degrees":degrees,
      "degree6_invariants_of_one_E8_adjoint":h[6],
      "degree6_basis":"(quadratic Casimir)^3",
      "one_SU3_triplet_nonconstant_holomorphic_invariants":0,
      "commuting_single_27x3_symmetric_E6_cubic_times_SU3_epsilon":0,
      "nonempty_SIC_subset_checks":511,"max_SIC_subset_identity_error":err,
      "positive_SIC_triplet_fields_needed_for_D_flatness":9,
      "restriction":"Only if all D-term contributors are positively weighted SU3 fundamentals on those SIC rays; additional fields, antitriplets and Higgsing can change conclusions."}

def poset_gate():
    n=5;edges=list(itertools.combinations(range(n),2))
    relations={}
    for mask in range(1<<len(edges)):
        A=np.zeros((n,n),bool)
        for e,(i,j) in enumerate(edges):A[i,j]=bool(mask>>e&1)
        for k in range(n):A|=A[:,k,None]&A[None,k,:]
        relations[A.tobytes()]=A.copy()
    assert len(relations)==357
    permutations=list(itertools.permutations(range(n)))
    def canonical(A):
        return min(A[np.ix_(p,p)].tobytes() for p in permutations)
    unlabeled={canonical(A):A for A in relations.values()}
    assert len(unlabeled)==63
    hist=defaultdict(list)
    for key,A in unlabeled.items():
        h=[0]*(n-1)
        for i,j in itertools.product(range(n),repeat=2):
            if A[i,j]:h[int(np.sum(A[i,:]&A[:,j]))]+=1
        hist[tuple(h)].append(key)
    assert len(hist)==28
    assert sum(len(v)>1 for v in hist.values())==18
    assert max(map(len,hist.values()))==7
    return {"directed_adjacencies":1024,"distinct_naturally_ordered_relations":357,
      "unlabeled_posets":63,"distinct_interval_histograms":28,
      "histograms_with_nonisomorphic_collisions":18,
      "maximum_nonisomorphic_posets_sharing_interval_histogram":7,
      "restriction":"A global layer-count action is not injective on finite causal orders; this does not prohibit dynamical causal set gravity."}

def e6_real_gate():
    t=s.symbols("t",real=True)
    q=8*t*t-2*t+1
    assert s.simplify(q-(8*(t-s.Rational(1,8))**2+s.Rational(7,8)))==0
    root=[s.Rational(1,8)-s.I*s.sqrt(7)/8,s.Rational(1,8)+s.I*s.sqrt(7)/8]
    assert all(s.simplify(q.subs(t,r))==0 for r in root)
    return {"critical_polynomial":"8*t^2-2*t+1",
      "minimum_over_real_t":"7/8","real_critical_points":0,
      "complex_critical_points":[str(r) for r in root],
      "source":"Grigorian arXiv:2611.21589",
      "restriction":"The algebraic E6 stabilizer is external prior art. No compact real gauge group, 7D chiral index or physical action derived."}

def memory_gate():
    # R(reference)-S(system)-E(memory); each qutrit.
    d=3;psi=np.zeros((3,3,3),complex)
    for i in range(3):psi[i,i,0]=1/np.sqrt(3)
    psi=psi.transpose(0,2,1) # SWAP S,E stores input in E
    rho=np.outer(psi.ravel(),psi.ravel().conj()).reshape((3,)*6)
    phi=np.zeros(9,complex)
    for i in range(3):phi[4*i]=1/np.sqrt(3)
    ideal=np.outer(phi,phi.conj())
    resets=[np.diag([1.,0,0]),np.eye(3)/3,np.array([[.5,.5,0],[.5,.5,0],[0,0,0]],complex)]
    def retrieve(environment,sigma):
        # Causal-break replacement of S, then second S/E swap.
        RE=np.trace(environment,axis1=1,axis2=4)
        after=np.einsum("aebf,st->asebtf",RE,sigma)
        after=after.transpose(0,2,1,3,5,4)
        return np.trace(after,axis1=2,axis2=5).reshape(9,9)
    err=max(np.linalg.norm(retrieve(rho,sg)-ideal) for sg in resets)
    assert err<1e-12
    def negativity(Q):
        PT=Q.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
        return float(-sum(x for x in np.linalg.eigvalsh(PT) if x<0))
    RS=np.trace(rho,axis1=2,axis2=5)
    replace=np.einsum("asbt,ef->asebtf",RS,np.eye(3)/3)
    rows=[]
    for p in (0,.1,.24,.25,.3,.5,1):
        y=retrieve(p*rho+(1-p)*replace,resets[0])
        assert np.linalg.norm(y-(p*ideal+(1-p)*np.eye(9)/9))<1e-12
        N=negativity(y)
        assert abs(N-max(0,(4*p-1)/3))<1e-12
        rows.append({"p":p,"negativity":N})
    dephased=rho.copy()
    for e in range(3):
        for f in range(3):
            if e!=f:dephased[:,:,e,:,:,f]=0
    classical=negativity(retrieve(dephased,resets[0]))
    assert classical<1e-12
    return {"causal_break_reset_count":len(resets),
      "max_ideal_entanglement_recovery_error":float(err),
      "memory_depolarizing_scan":rows,
      "analytical_negativity":"max(0,(4p-1)/3)",
      "classical_dephased_memory_negativity":classical,
      "quantum_memory_sufficient_visibility":"p>1/4",
      "restriction":"Intervention-aware SWAP toy certifies quantum memory, not genuinely-three-time-only memory or photonic implementation."}

def su3_gate():
    a=np.exp(1j*np.array([.37,1.1,-1.47]))
    b=np.exp(1j*np.array([.41,.91,-1.32]))
    A=np.diag(a);B0=np.diag(b)
    k=np.arange(3)
    F=np.exp(2j*np.pi*np.outer(k,k)/3)/np.sqrt(3)
    B=F@B0@F.conj().T
    C=lambda X,Y:X@Y@X.conj().T@Y.conj().T
    w=np.trace(C(A,B))
    norm=float(np.linalg.norm(A@B-B@A)**2)
    assert abs(np.trace(C(A,B0))-3)<1e-12
    assert abs(norm-(6-2*w.real))<1e-12 and norm>4
    rng=np.random.default_rng(271119);frame=0.
    for _ in range(24):
        M=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        V,_=np.linalg.qr(M);V/=np.linalg.det(V)**(1/3)
        frame=max(frame,float(abs(np.trace(C(V@A@V.conj().T,V@B@V.conj().T))-w)))
    I=lambda theta:6+2*np.real(np.exp(-1j*theta)*w)
    reconstructed=(I(0)-6)/2+1j*(I(np.pi/2)-6)/2
    assert frame<1e-12 and abs(reconstructed-w)<1e-12
    return {"commutator_trace":[float(w.real),float(w.imag)],
      "Frobenius_commutator_norm_squared":norm,
      "exact_identity":"||AB-BA||_F^2=6-2 Re Tr(ABA†B†)",
      "gauge_frame_checks":24,"maximum_frame_error":frame,
      "two_reference_phase_trace_reconstruction_error":float(abs(reconstructed-w)),
      "restriction":"Group-theoretic two-loop control, not an implemented optical interferometer or dynamically sourced gauge field."}

def run():
    result={"status":"FIVE_PROVEN_FINITE_GATES_NOT_A_TOE",
      "date":"2026-11-19","tracks":{"uv":uv_gate(),"causal":poset_gate(),
      "g2_e6":e6_real_gate(),"temporal_memory":memory_gate(),"two_loop_SU3":su3_gate()}}
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
    print("CERTIFICATE",OUT)
