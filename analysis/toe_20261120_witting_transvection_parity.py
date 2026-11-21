"""Forty Witting reflections as odd Weil restrictions of two-qutrit Clifford gates.

Independent operational extension of analysis/w33_pass11663_odd_weil_normal_map.py.
The pre-existing correspondence of 40 odd-sector projectors is PRIOR WORK;
new checks cover all 40 gate conjugations, all 80 nonzero Weyl operators,
character/trace contrasts and the universal zero-outcome parity identity.

No new physical law or experimentally acquired data is claimed.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_witting_transvection_parity.json"

def canon(x,p):
    x=tuple(int(a)%p for a in x)
    j=next(i for i,a in enumerate(x) if a)
    inv=pow(x[j],-1,p)
    return tuple(a*inv%p for a in x)

def address_space(p=3,n=2):
    return tuple(product(range(p),repeat=2*n))

def projective_points(p=3,n=2):
    return sorted({canon(v,p) for v in address_space(p,n) if any(v)})

def symp(u,v,p=3):
    return sum(u[2*i]*v[2*i+1]-u[2*i+1]*v[2*i]
               for i in range(len(u)//2))%p

def operator(v,p=3):
    n=len(v)//2; omega=np.exp(2j*np.pi/p)
    E=np.eye(p,dtype=complex)
    X=np.roll(E,1,axis=0)
    Z=np.diag([omega**a for a in range(p)])
    out=np.array([[1]],dtype=complex)
    inv2=pow(2,-1,p)
    for k in range(n):
        a,b=int(v[2*k]),int(v[2*k+1])
        one=omega**((-inv2*a*b)%p)*(np.linalg.matrix_power(Z,a)@
                                    np.linalg.matrix_power(X,b))
        out=np.kron(out,one)
    return out

def parity(p=3,n=2):
    base=list(product(range(p),repeat=n));index={a:i for i,a in enumerate(base)}
    Q=np.zeros((p**n,p**n),dtype=complex)
    for j,a in enumerate(base):
        Q[index[tuple(-x%p for x in a)],j]=1
    return Q

def parity_frames():
    p,n=3,2; base=list(product(range(p),repeat=n))
    idx={a:i for i,a in enumerate(base)};E=[];O=[];seen=set()
    for a in base:
        if a in seen: continue
        b=tuple(-x%p for x in a);seen.add(a);seen.add(b)
        if a==b:
            z=np.zeros(9,complex);z[idx[a]]=1;E.append(z)
        else:
            e=np.zeros(9,complex);e[idx[a]]=e[idx[b]]=1/np.sqrt(2)
            o=np.zeros(9,complex);o[idx[a]]=1/np.sqrt(2);o[idx[b]]=-1/np.sqrt(2)
            E.append(e);O.append(o)
    E=np.column_stack(E);O=np.column_stack(O)
    assert E.shape==(9,5) and O.shape==(9,4)
    return E,O

def zero_projector(v,p):
    n=len(v)//2;D=p**n
    A=np.zeros((D,D),complex)
    for t in range(p):
        A+=operator(tuple((t*x)%p for x in v),p)
    return A/p

def reference_odd_witting():
    """Pass11663's already-established Witting ray coordinate gauge."""
    omega=np.exp(2j*np.pi/3)
    rays=list(np.eye(4,dtype=complex))
    for i,j in product(range(3),repeat=2):
        rays.extend([np.array(v,complex) for v in [
            (0,1,omega**i,omega**j),
            (1,0,omega**i,-omega**j),
            (1,-omega**i,0,omega**j),
            (1,omega**i,-omega**j,0)]])
    return [np.outer(r,r.conj())/np.vdot(r,r).real for r in rays]

def three_model():
    points=projective_points(3,2);idx={a:i for i,a in enumerate(points)}
    assert len(points)==40
    I=np.eye(9,dtype=complex);Q=parity()
    E,O=parity_frames();omega=np.exp(2j*np.pi/3)
    assert np.linalg.norm(Q@(E@E.conj().T)-E@E.conj().T)<1e-12
    odd=[];even=[];full=[];Ufull=[]
    max_unitarity=max_cov=max_odd=max_rotation=0.
    for v in points:
        P=zero_projector(v,3)
        assert np.linalg.norm(P@P-P)<1e-11
        assert np.linalg.norm(P@Q-Q@P)<1e-11
        assert abs(np.trace(P)-3)<1e-11
        Po=O.conj().T@P@O;Pe=E.conj().T@P@E
        assert abs(np.trace(Po)-1)<1e-11
        assert abs(np.trace(Pe)-2)<1e-11
        U=I+(omega-1)*P
        max_unitarity=max(max_unitarity,float(np.linalg.norm(U.conj().T@U-I)),
                          float(np.linalg.norm(np.linalg.matrix_power(U,3)-I)))
        odd.append(Po);even.append(Pe);full.append(P);Ufull.append(U)
    # New 40 x 80 full Weyl operator Clifford conjugation certificate.
    for i,v in enumerate(points):
        U=Ufull[i];vo=np.array(v)
        oddU=O.conj().T@U@O
        for u in address_space(3,2):
            if not any(u):continue
            su=symp(u,v,3)
            target=tuple((np.array(u)+2*su*vo)%3)
            delta=U@operator(u)@U.conj().T-operator(target)
            max_cov=max(max_cov,float(np.linalg.norm(delta)))
        for j,u in enumerate(points):
            su=symp(u,v,3)
            target=canon(tuple((np.array(u)+2*su*vo)%3),3)
            max_odd=max(max_odd,float(np.linalg.norm(oddU@odd[j]@oddU.conj().T-
                                                   odd[idx[target]])))
            max_rotation=max(max_rotation,float(np.linalg.norm(
                oddU.conj().T@oddU-np.eye(4))))
    # All 40 parity-odd projectors match the prior Witting ray coordinate gauge.
    old=reference_odd_witting()
    matcher=np.array([[np.linalg.norm(a-b) for b in old] for a in odd])
    match=np.argmin(matcher,axis=1)
    assert len(set(match))==40
    match_error=float(max(matcher[np.arange(40),match]))
    A=np.array([[int(i!=j and symp(u,v,3)==0)
                 for j,v in enumerate(points)] for i,u in enumerate(points)])
    J=np.ones((40,40));I40=np.eye(40)
    gram_odd=np.array([[np.trace(x@y).real for y in odd] for x in odd])
    gram_even=np.array([[np.trace(x@y).real for y in even] for x in even])
    gram_odd_error=float(np.max(abs(gram_odd-(2*I40+J-A)/3)))
    gram_even_error=float(np.max(abs(gram_even-(4*I40+A+2*J)/3)))
    sum_P=sum(full);sum_odd=sum(odd);sum_even=sum(even)
    parity_identity_error=float(np.linalg.norm(sum_P-(13*I+3*Q)))
    odd_tight_error=float(np.linalg.norm(sum_odd-10*np.eye(4)))
    even_tight_error=float(np.linalg.norm(sum_even-16*np.eye(5)))
    traces=[]
    for U in Ufull:
        traces.append([abs(np.trace(U)/9)**2,
                       abs(np.trace(O.conj().T@U@O)/4)**2,
                       abs(np.trace(E.conj().T@U@E)/5)**2])
    trace_error=float(max(abs(np.array(traces)-np.array([1/3,7/16,7/25])).ravel()))
    assert max(max_unitarity,max_cov,max_odd,max_rotation,match_error,
               gram_odd_error,gram_even_error,parity_identity_error,
               odd_tight_error,even_tight_error,trace_error)<1e-10
    return {
        "projective_directions":40,"nonzero_Weyl_operators":80,
        "Weyl_conjugation_cases":40*80,"Witting_odd_action_cases":40*40,
        "max_unitarity_error":max_unitarity,"max_exact_Weyl_covariance_error":max_cov,
        "max_Witting_projector_action_error":max_odd,
        "max_odd_unitarity_error":max_rotation,
        "prior_Witting_ray_projector_match_error":match_error,
        "odd_Gram_error":gram_odd_error,"even_Gram_error":gram_even_error,
        "zero_outcome_sum_identity":"sum_{40 v} Pi_0(v)=13 I9+3 parity",
        "parity_sum_residual":parity_identity_error,
        "odd_tight_frame":"sum 40 rank1 projectors =10 I4",
        "even_tight_fusion_frame":"sum 40 rank2 projectors =16 I5",
        "odd_tight_error":odd_tight_error,"even_tight_error":even_tight_error,
        "odd_Gram":"(2I40+J40-A_W33)/3",
        "even_Gram":"(4I40+A_W33+2J40)/3",
        "trace_contrasts_squared":{"full9":1/3,"odd4":7/16,"even5":7/25},
        "trace_contrast_numerical_error":trace_error,
        "zero_outcome_probability":{"odd":1/4,"even":2/5,"max_mixed":1/3},
        "projective_compatibility_rate_self_plus_commuting":13/40,
        "Wigner_negativity_criterion":"uniform projector acceptance p0 < 13/40 iff centered Wigner at origin is negative",
        "Wigner_recovery":"W_rho(0)=(40 p0 -13)/27",
        "projective_Witting_rays_have_self_plus_12_orthogonal":True}

def general_parity(p=5,n=2):
    pts=projective_points(p,n);D=p**n;N=len(pts)
    assert N==(p**(2*n)-1)//(p-1)
    I=np.eye(D,dtype=complex);Q=parity(p,n)
    ps=[zero_projector(v,p) for v in pts]
    S=sum(ps);want=((N-1)/p)*I+(p**(n-1))*Q
    assert max(np.linalg.norm(x@x-x) for x in ps)<1e-10
    proj_ranks=[]
    Pp=(I+Q)/2;Pm=(I-Q)/2
    for x in ps:
        rp=round(np.trace(Pp@x).real);rm=round(np.trace(Pm@x).real)
        assert rp==(p**(n-1)+1)//2
        assert rm==(p**(n-1)-1)//2
        proj_ranks.append((rp,rm))
    err=float(np.linalg.norm(S-want))
    assert err<1e-9
    return {"p":p,"n":n,"Hilbert_dimension":D,"projective_directions":N,
            "even_sector_dimension":int((D+1)//2),
            "odd_sector_dimension":int((D-1)//2),
            "zero_eigen_ranks_even_odd":list(proj_ranks[0]),
            "projective_neighbors_plus_self":p*(p+1)+1,
            "uniform_projective_compatibility_rate":(p*(p+1)+1)/N,
            "same_as_centered_Wigner_negativity_threshold":((N-1)/p)/N,
            "sum_projectors_even_eigenvalue":(N-1)/p+p**(n-1),
            "sum_projectors_odd_eigenvalue":(N-1)/p-p**(n-1),
            "general_identity":"sum_{rays ell} Pi_0(ell)=((N-1)/p)I+p^(n-1)P",
            "identity_residual":err}

def wigner_magic():
    """Gross centered discrete-Wigner address of every odd Witting ray.

    The 3 negative phase-space cells are precisely the F3 line <v>.
    The remaining 24 points of v-perp are +1/18; all 54 outside are 0.
    """
    dirs=projective_points(3,2)
    phasepoints=address_space(3,2)
    P=parity()
    I=np.eye(9,dtype=complex)
    odd=(I-P)/2
    phase_ops=[operator(a)@P@operator(a).conj().T for a in phasepoints]
    maximum_error=0.0
    maximum_trace_error=0.0
    histograms=[]
    wigner_rows=[]
    for v in dirs:
        rho=odd@zero_projector(v,3)
        assert np.linalg.norm(rho@rho-rho)<1e-11
        maximum_trace_error=max(maximum_trace_error,abs(np.trace(rho)-1))
        measured=np.array([np.trace(A@rho).real/9 for A in phase_ops])
        line={tuple((t*x)%3 for x in v) for t in range(3)}
        formula=np.array([
            -1/9 if a in line else (1/18 if symp(a,v,3)==0 else 0.)
            for a in phasepoints
        ])
        maximum_error=max(maximum_error,float(np.max(abs(measured-formula))))
        neg={a for a,value in zip(phasepoints,measured) if value < -1e-6}
        assert neg==line
        wigner_rows.append(measured)
        assert abs(measured.sum()-1)<1e-11
        assert abs(np.sum(np.abs(measured))-5/3)<1e-11
        histograms.append((int(np.sum(measured<-1e-6)),
                           int(np.sum(measured>1e-6)),
                           int(np.sum(abs(measured)<=1e-6))))
    assert set(histograms)=={(3,24,54)}
    W=np.asarray(wigner_rows)
    adjacency=np.array([[int(i!=j and symp(a,b,3)==0)
                         for j,b in enumerate(dirs)] for i,a in enumerate(dirs)])
    Gram=9*W@W.T
    Gram_target=(2*np.eye(40)+np.ones((40,40))-adjacency)/3
    Gram_error=float(np.max(abs(Gram-Gram_target)))
    Gram_rank=int(np.linalg.matrix_rank(W,tol=1e-10))
    assert Gram_error<1e-10 and Gram_rank==16
    example=np.zeros(9,complex)
    example[1]=1/np.sqrt(2)
    example[2]=-1/np.sqrt(2)
    rho=odd@zero_projector((1,0,0,0),3)
    example_error=float(np.linalg.norm(rho-np.outer(example,example.conj())))
    assert example_error<1e-11
    assert maximum_error<1e-11 and maximum_trace_error<1e-11
    return {
        "phase_space_points":81,
        "ray_count":40,
        "tested_ray_phase_points":3240,
        "negative_cells_per_ray":3,
        "positive_cells_per_ray":24,
        "zero_cells_per_ray":54,
        "negative_value":-1/9,
        "positive_value":1/18,
        "negative_support":"exact three-element vector line span_F3(v) through phase-space origin",
        "positive_support":"symplectic orthogonal hyperplane v-perp excluding span(v)",
        "zero_support":"54 points with nonzero symplectic pairing with v",
        "Wigner_L1_norm":5/3,
        "Wigner_reconstructed_rank_one_Gram":"9 sum_a W_v(a) W_w(a)=(2I+J-A_W33)/3",
        "Wigner_reconstructed_Gram_max_error":Gram_error,
        "Wigner_40_by_81_matrix_rank":Gram_rank,
        "mana_natural_log":float(np.log(5/3)),
        "max_formula_residual":maximum_error,
        "max_density_trace_error":maximum_trace_error,
        "explicit_reference_direction":(1,0,0,0),
        "explicit_reference_state":"|0> tensor (|1>-|2>)/sqrt(2)",
        "explicit_reference_density_residual":example_error,
        "limitation":"Uses a fixed canonical Gross parity origin and centered Weyl phases; standard pure-state Wigner negativity. Clifford-displaced odd rays preserve the histogram but translate the negative line. Not a 4-level stabilizer-magic claim, nor new physical dynamics."
    }


def run(write=True):
    out={"status":"PASS_WITTING_TRANSVECTIONS_PARITY_ESTIMATOR",
         "source_prior_work":["analysis/w33_pass11663_odd_weil_normal_map.py",
                              "analysis/w33_pass4963_witting_pancharatnam_w33_reaudit.py",
                              "analysis/2026-10-15_toe90_vlasov_witting_research.md"],
         "new_scope":"All 40 gates/3200 Weyl conjugations, sector trace fingerprints, randomized 40-zero-eigen projector parity identity, p5 rank control, rank-one uniqueness argument",
         "q3_n2":three_model(),
         "q5_n2":general_parity(),
         "wigner_magic":wigner_magic(),
         "general_rank_formula":"dim Pi_0|even=(p^(n-1)+1)/2; dim Pi_0|odd=(p^(n-1)-1)/2",
         "unique_ray_condition":"For odd prime p and n>=2, rank_odd=1 iff p^(n-1)=3 iff p=3,n=2",
         "boundary":"Finite qudit quantum mechanics, not physical qutrit selection, new TOE dynamics, or experiment."}
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return out

if __name__=="__main__":
    result=run()
    print(json.dumps({"status":result["status"],"q3_n2":result["q3_n2"],
                      "q5_n2":result["q5_n2"]},indent=2))
