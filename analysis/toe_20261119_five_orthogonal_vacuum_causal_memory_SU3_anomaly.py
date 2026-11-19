#!/usr/bin/env python3
"""TOE five independent gates after the 2026-11-19 parallel review.

All results are mathematical / small-model controls, NOT a derived 4D TOE.
Run from repository root or any working directory:
  python analysis/toe_20261119_five_orthogonal_vacuum_causal_memory_SU3_anomaly.py
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_five_orthogonal_causal_H27_qutrit_SU3_anomaly.json"
omega=np.exp(2j*np.pi/3)

def tri_response(A,m=1.3,alpha=.6):
    n=len(A)
    G=np.linalg.inv(m*np.eye(n)-alpha*A)
    return float(np.real(np.vdot(G,G)))

def order_closure(A):
    B=A.astype(bool).copy()
    n=len(A)
    for k in range(n):
        B |= (B[:,k,None]&B[None,k,:])
    return B

def covers(C):
    n=len(C);H=np.zeros((n,n),dtype=float)
    for i,j in combinations(range(n),2):
        if C[i,j] and not any(C[i,k] and C[k,j] for k in range(i+1,j)):
            H[i,j]=1
    return H

def causal_order_presentation():
    results=[]
    for n in (4,5):
        edges=list(combinations(range(n),2))
        groups=defaultdict(list)
        for mask in range(1<<len(edges)):
            A=np.zeros((n,n),float)
            for k,(i,j) in enumerate(edges):
                A[i,j]=(mask>>k)&1
            C=order_closure(A)
            sig=tuple(int(C[i,j]) for i,j in edges)
            groups[sig].append((mask,tri_response(A),C))
        ambiguous=sum(len(v)>1 for v in groups.values())
        gaps=[max(v[1] for v in cells)-min(v[1] for v in cells)
              for cells in groups.values()]
        max_canonical_spread=0.
        for cells in groups.values():
            r=[tri_response(covers(entry[2])) for entry in cells]
            max_canonical_spread=max(max_canonical_spread,max(r)-min(r))
        assert max_canonical_spread<1e-12
        results.append({"events":n,"graph_presentations":1<<len(edges),
          "distinct_causal_orders_with_fixed_label_order":len(groups),
          "orders_with_multiple_edge_presentations":ambiguous,
          "maximum_response_spread_within_one_order":max(gaps),
          "Hasse_canonical_response_spread_within_one_order":max_canonical_spread})
    assert results[0]["distinct_causal_orders_with_fixed_label_order"]==40
    assert results[1]["distinct_causal_orders_with_fixed_label_order"]==357
    assert results[1]["orders_with_multiple_edge_presentations"]==199
    n=5
    chain=np.zeros((n,n))
    for i in range(n-1):chain[i,i+1]=1
    full=np.triu(np.ones((n,n)),1)
    assert np.all(order_closure(chain)==order_closure(full))
    assert np.array_equal(covers(order_closure(full)),chain)
    return {"censuses":results,
      "same_total_order":{"Hasse_links":int(np.sum(chain)),
          "all_causal_relations":int(np.sum(full)),
          "Hasse_response":tri_response(chain),
          "closure_response":tri_response(full)},
      "physical_gate":"A propagator assigned to arbitrary edges is NOT an invariant of the causal order; choosing the canonical cover adjacency removes this presentation ambiguity but supplies an extra microscopic rule, not 4D continuum dynamics."}

def h27_f_flat_mass_lift():
    x,y,z,l=sp.symbols("x y z l")
    X=(x,y,z)
    S=sum(t**3 for t in X)
    W=sum(t**3-sp.Rational(1,2)*t**6 for t in X)+l*x*y*z*(S-2)
    F=[sp.diff(W,v) for v in X]
    H=sp.hessian(W,X)
    root={x:1,y:1,z:0}
    H110=H.subs(root)
    determinant=sp.factor(H110.det())
    assert determinant==162*l*l
    assert all(sp.simplify(f.subs(root))==0 for f in F)
    # Heisenberg generators: cyclic permutation, diagonal clock.
    assert sp.expand(W-W.xreplace({x:y,y:z,z:x}))==0
    assert sp.simplify(sp.expand(W-W.xreplace({x:x,y:sp.Symbol('w')*y,z:sp.Symbol('w')**2*z})))!=0  # symbolic w needs w^3=1
    # Explicit exact cyclotomic reduction for diagonal clock.
    w=sp.symbols("w")
    clock=sp.expand(W-W.xreplace({x:x,y:w*y,z:w**2*z}))
    clock=sp.Poly(clock,w)
    rem=sp.rem(clock,sp.Poly(w*w+w+1,w))
    assert sp.expand(rem.as_expr())==0
    fv=sp.lambdify((x,y,z,l),F,modules="numpy")
    hv=sp.lambdify((x,y,z,l),H,modules="numpy")
    lam=.25
    sic=[]
    maxF=0.;minS=1e9
    for missing in range(3):
        occupied=[j for j in range(3) if j!=missing]
        for a,b in product(range(3),repeat=2):
            v=np.zeros(3,dtype=complex)
            v[occupied]=[omega**a,omega**b]
            maxF=max(maxF,float(np.max(np.abs(fv(*v,lam)))))
            minS=min(minS,float(np.min(np.linalg.svd(hv(*v,lam),compute_uv=False))))
        for b in range(3):
            v=np.zeros(3,dtype=complex)
            v[occupied]=[1,omega**b]
            sic.append(v/np.linalg.norm(v))
    sic=np.array(sic)
    sicerr=float(np.max(np.abs(np.abs(sic.conj()@sic.T)**2-
                 (np.eye(9)+.25*(np.ones((9,9))-np.eye(9))))))
    assert maxF<1e-12 and minS>1e-4 and sicerr<1e-12
    mub=[]
    extF=0.;fullmin=1e9
    bins={0:[],1:[],2:[]}
    for a,b in product(range(3),repeat=2):
        xi=omega**(a+b)
        cuber=(3-2*lam*xi)/(3-6*lam*xi)
        r=cuber**(1/3)
        v=r*np.array([1,omega**a,omega**b],complex)
        extF=max(extF,float(np.max(np.abs(fv(*v,lam)))))
        fullmin=min(fullmin,float(np.min(np.linalg.svd(hv(*v,lam),compute_uv=False))))
        u=v/np.linalg.norm(v)
        mub.append(u);bins[(a+b)%3].append(u)
    orth=max(float(np.linalg.norm(np.array(B).conj()@np.array(B).T-np.eye(3))) for B in bins.values())
    cross=max(float(np.max(np.abs(np.abs(np.array(bins[i]).conj()@
                         np.array(bins[j]).T)**2-1/3)))
              for i,j in combinations(range(3),2))
    assert extF<1e-11 and fullmin>1 and orth<1e-12 and cross<1e-12
    # Weighted MUB bases remain tight frames even when the three orbit
    # amplitudes differ: nine separately assigned triplets have sum vv†~I.
    frames=[]
    for xi_cls in range(3):
        group=[]
        for a,b in product(range(3),repeat=2):
            if (a+b)%3!=xi_cls:continue
            xi=omega**(a+b)
            r=((3-2*lam*xi)/(3-6*lam*xi))**(1/3)
            group.append(r*np.array([1,omega**a,omega**b],complex))
        frames+=group
    moment=sum(np.outer(v,v.conj()) for v in frames)
    moment_err=float(np.linalg.norm(moment-np.trace(moment)/3*np.eye(3)))
    assert moment_err<1e-12
    assert sp.simplify(W.subs(root)-1)==0
    # Derivative with respect to lambda at original MUB point nonzero.
    original_MUB_gradient=sp.simplify(F[0].subs({x:1,y:1,z:1}))
    assert original_MUB_gradient==4*l
    return {"new_H27_superpotential":str(W),
      "H27_generator_invariance":"exact polynomial checks cyclic shift and diagonal phase mod (w²+w+1)",
      "SIC_Hessian_at_(1,1,0)":str(H110),
      "SIC_Hessian_determinant":str(determinant),
      "tested_lambda":lam,"exact_SIC_F_residual":maxF,
      "all_27_SIC_stationary_vectors_min_singular_Hessian":minS,
      "SIC_projective_Gram_residual":sicerr,
      "support3_preserving_amplitude_formula":"r^3=(3-2*lambda*xi)/(3-6*lambda*xi), xi=omega^(a+b)",
      "support3_F_residual":extF,"support3_min_singular_Hessian":fullmin,
      "support3_MUB_within_basis_residual":orth,
      "support3_MUB_between_basis_residual":cross,
      "nine_triplet_frame_moment_map_traceless_residual":moment_err,
      "previous_MUB_point_requires_rescaling":"F_x(1,1,1)=4*lambda",
      "limitations":"Single-triplet W is invariant under finite H27, not full continuous SU3 gauge; the moment map uses nine independent proposed triplets, NOT an SU3 gauge-invariant superpotential; no E8 UV completion, Kähler dynamics, radiative lifting or vacuum selection."}

def anomaly_gate():
    # Every field is left-handed Weyl, includes conjugates of right-handed SM states.
    fields=[("Q",3,2,Q(1,6),1),("u^c",3,1,Q(-2,3),-1),
      ("d^c",3,1,Q(1,3),-1),("L",1,2,Q(-1,2),0),
      ("e^c",1,1,Q(1),0),("nu^c",1,1,Q(0),0)]
    def totals(xs):
        U1grav=sum(n3*n2*q for _,n3,n2,q,_ in xs)
        U1cube=sum(n3*n2*q**3 for _,n3,n2,q,_ in xs)
        SU3SU3U1=sum(n2*Q(1,2)*q for _,n3,n2,q,_ in xs if n3==3)
        SU2SU2U1=sum(n3*Q(1,2)*q for _,n3,n2,q,_ in xs if n2==2)
        SU3cube=sum(n2*sgn for _,n3,n2,q,sgn in xs if n3==3)
        Witten=sum(n3 for _,n3,n2,q,_ in xs if n2==2)%2
        return [str(U1grav),str(U1cube),str(SU3SU3U1),str(SU2SU2U1),str(SU3cube),Witten]
    a=totals(fields);b=totals(fields[:-1])
    assert a==b==["0","0","0","0","0",0]
    # Removing charged Weyl field breaks at least one local anomaly.
    no_e=totals([f for f in fields if f[0]!="e^c"])
    assert no_e!=a
    return {"anomaly_channels":["grav² U1","U1³","SU3² U1","SU2² U1","SU3³","Witten SU2 parity"],
      "one_16_with_nuR":a,"one_15_without_nuR":b,
      "without_charged_eR":no_e,
      "theorem":"One Standard Model generation already cancels anomalies, with or without sterile nu_R; anomaly cancellation alone fixes neither 3 families nor the extra nu_R of an SO10 16.",
      "limitations":"This is a familiar Standard Model anomaly census; no derived physical chiral index, 4D fermion dynamics, GUT threshold, E8 spectrum or UV proof."}

def su3_phase_gate():
    theta=[.6,1.5,-2.1]
    W=np.diag(np.exp(1j*np.array(theta)))
    U=W
    t=np.trace(W)
    def intensity(phase):
        B=U+np.exp(1j*phase)*np.eye(3)
        return float(np.trace(B@B.conj().T).real)
    i0=intensity(0)
    i90=intensity(np.pi/2)
    reconstructed=(i0-6)/2+1j*(i90-6)/2
    assert abs(reconstructed-t)<2e-15
    eig0=np.linalg.eigvalsh((U+np.eye(3))@(U+np.eye(3)).conj().T)
    Udag=U.conj().T
    eigdag=np.linalg.eigvalsh((Udag+np.eye(3))@(Udag+np.eye(3)).conj().T)
    assert max(abs(eig0-eigdag))<1e-12
    # SU(3) characteristic polynomial: p(z)=z^3-t*z^2+conj(t)*z-1.
    eig=np.linalg.eigvals(U)
    poly=max(abs(e**3-t*e**2+np.conj(t)*e-1) for e in eig)
    chi6=t*t-np.conj(t)
    direct6=sum(e**2 for e in eig)+sum(eig[i]*eig[j] for i,j in combinations(range(3),2))
    assert abs(chi6-direct6)<1e-12 and poly<1e-12
    rng=np.random.default_rng(261119);frame_error=0.
    for _ in range(24):
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        Qm,Rm=np.linalg.qr(Z)
        Qm=Qm/np.linalg.det(Qm)**(1/3)
        Wf=Qm@U@Qm.conj().T
        frame_error=max(frame_error,float(abs(np.trace(Wf)-t)))
    assert frame_error<1e-12
    return {"SU3_fundamental_trace":[float(t.real),float(t.imag)],
        "intensity_phase0":i0,"intensity_phase_pi_over2":i90,
        "reconstructed_trace_error":float(abs(reconstructed-t)),
        "W_vs_Wdag_zero_phase_spectrum_error":float(max(abs(eig0-eigdag))),
        "W_vs_Wdag_pi_over2_intensity_difference":float(4*t.imag),
        "SU3_characteristic_polynomial_residual":float(poly),
        "chi_6_symmetric_rep_trace":[float(chi6.real),float(chi6.imag)],
        "chi_8_adjoint_rep_trace":float(abs(t)**2-1),
        "24_random_frame_max_trace_error":frame_error,
        "theorem":"Two coherent phase settings reconstruct the complex fundamental trace of a fixed classical SU3 holonomy, which determines its conjugacy class. Unshifted singular-value spectra cannot distinguish W from W†.",
        "limitations":"Known Wilson/interferometry group-theory prior art; phase calibration, source/measurement hardware, backreaction, fluctuating gauge fields and matter representations not derived."}

def temporal_memory_gate():
    ghz=np.zeros((27,),complex)
    for j in range(3):ghz[13*j]=1/np.sqrt(3)
    pure=np.outer(ghz,ghz.conj())
    classical=np.zeros((27,27),complex)
    for j in range(3):classical[13*j,13*j]=1/3
    plus=np.ones(3,dtype=complex)/np.sqrt(3)
    def heralded(rho):
        blocks=rho.reshape(3,9,3,9)
        out=np.einsum("a,abcd,c->bd",plus.conj(),blocks,plus)
        prob=float(np.trace(out).real)
        assert abs(prob-1/3)<1e-12
        return out/prob
    def negativity(M):
        PT=M.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
        ev=np.linalg.eigvalsh(PT)
        return float(-sum(e for e in ev if e<0))
    qutrit_coherence=[]
    for v in [0.,.1,.5,1.]:
        rho=v*pure+(1-v)*classical
        B=heralded(rho)
        neg=negativity(B)
        assert abs(neg-v)<1e-12
        qutrit_coherence.append({"GHZ_coherence":v,"conditional_BC_negativity":neg})
    # Noise mixture with maximally mixed three-qutrit state
    white=[]
    for v in [0.,.2,.25,.3,.5,1.]:
        rho=v*pure+(1-v)*np.eye(27)/27
        neg=negativity(heralded(rho))
        target=max(0.,(4*v-1)/3)
        assert abs(neg-target)<1e-12
        white.append({"GHZ_visibility":v,"conditional_negativity":neg})
    assert negativity(heralded(classical))<1e-12
    return {"dephasing_scan":qutrit_coherence,
       "white_noise_scan":white,
       "heralded_BC_entanglement_visibility_threshold":"v>1/4",
       "theorem":"Fourier-basis measurement of emitted GHZ qutrit A heralds entangled BC. Pairwise unconditioned marginals do not reveal the coherence, but conditional negativity=v for GHZ/dephased mixture.",
       "limitations":"This is LOCALIZABLE ENTANGLEMENT, not the stronger genuine-three-time quantum memory process-tensor witness. All input slots and arbitrary instruments are absent."}

def run():
    out={"date":"2026-11-19","repo_base":"c98ed7e233cac609cd2e99ed0860e633e5a8ae02",
      "scientific_status":"FIVE_SMALL_MODEL_GATES_PASSED_NOT_A_THEORY_OF_EVERYTHING",
      "tracks":{"causal_order":causal_order_presentation(),
        "H27_SIC_MUB_mass_repair":h27_f_flat_mass_lift(),
        "SM_SO10_anomalies":anomaly_gate(),
        "SU3_phased_Wilson":su3_phase_gate(),
        "temporal_qutrit_heralding":temporal_memory_gate()}}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:{q:v for q,v in value.items() if q in
       ["censuses","same_total_order","SIC_Hessian_determinant","all_27_SIC_stationary_vectors_min_singular_Hessian",
       "support3_F_residual","support3_MUB_between_basis_residual","one_16_with_nuR",
       "SU3_fundamental_trace","reconstructed_trace_error","heralded_BC_entanglement_visibility_threshold"]}
       for k,value in out["tracks"].items()},indent=2))
    print("PASS FIVE GATES",OUT)
    return out

if __name__=="__main__":run()
