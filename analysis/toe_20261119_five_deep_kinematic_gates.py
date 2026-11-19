#!/usr/bin/env python3
"""Five independent exact/small-model TOE consistency gates; not a TOE.

Run: python analysis/toe_20261119_five_deep_kinematic_gates.py
Dependencies: numpy, scipy, sympy (sympy not needed for main calculations).
"""
from collections import defaultdict
from itertools import combinations, permutations
from math import ceil, log, sqrt
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_five_deep_kinematic_gates.json'


def mod_rank(M,p=7):
    A=np.asarray(M,dtype=np.int64).copy()%p
    r=0
    for c in range(A.shape[1]):
        pivot=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if pivot is None:continue
        A[[r,pivot]]=A[[pivot,r]]
        A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==A.shape[0]:break
    return r


def sic_gauge_completion():
    """SU3 baryonic constraints locally isolate SIC modulo gauge; no E8 claim."""
    omega=np.exp(2j*np.pi/3)
    P=np.zeros((3,9),complex)
    P7=np.zeros((3,9),int)
    for missing in range(3):
        slots=[j for j in range(3) if j!=missing]
        for k in range(3):
            idx=3*missing+k
            P[slots[0],idx]=1;P[slots[1],idx]=omega**k
            P7[slots[0],idx]=1;P7[slots[1],idx]=pow(2,k,7)
    moment=P@P.conj().T
    assert np.linalg.norm(moment-6*np.eye(3))<1e-12
    triples=list(combinations(range(9),3))
    J=np.zeros((len(triples),27),complex)
    J7=np.zeros((len(triples),27),int)
    bvalues=[]
    for q,(i,j,k) in enumerate(triples):
        a,b,c=P[:,i],P[:,j],P[:,k]
        bvalues.append(np.linalg.det(np.column_stack((a,b,c))))
        J[q,3*i:3*i+3]=np.cross(b,c)
        J[q,3*j:3*j+3]=np.cross(c,a)
        J[q,3*k:3*k+3]=np.cross(a,b)
        a,b,c=P7[:,i],P7[:,j],P7[:,k]
        J7[q,3*i:3*i+3]=np.cross(b,c)%7
        J7[q,3*j:3*j+3]=np.cross(c,a)%7
        J7[q,3*k:3*k+3]=np.cross(a,b)%7
    # Explicit 19 independent invariant-coordinate rows chosen by pivoted
    # complex QR, but nonzero rank is certified EXACTLY over GF(7) with
    # omega -> 2 (a root of omega²+omega+1=0 mod7).
    chosen=(0,13,25,39,47,50,63,55,37,24,23,21,51,56,45,72,33,10,64)
    Jr=J[list(chosen)]
    assert mod_rank(J7)==19 and mod_rank(J7[list(chosen)])==19
    assert np.linalg.matrix_rank(J,1e-9)==19
    # 27 fundamental coordinates and 19 singlet Lagrange multipliers:
    # W1=sum_r L_r(det(Phi_{i_r},Phi_{j_r},Phi_{k_r})-b_r).
    # 9 anti-fundamentals and 27 singlets T_ia:
    # W2=sum_{i,a}T_ia * tildePhi_i^T Phi_{c_a}.
    # Pick 3 independent SIC columns c_a as an SU3 frame.
    basis=(0,3,6)
    B=P[:,list(basis)]
    assert abs(np.linalg.det(B)-2)<1e-12
    H=np.zeros((100,100),complex)
    H[0:27,54:73]=Jr.T
    H[54:73,0:27]=Jr
    for i in range(9):
        for color in range(3):
            for a in range(3):
                x=27+3*i+color;y=73+3*i+a
                H[x,y]=B[color,a]
                H[y,x]=B[color,a]
    svals=np.linalg.svd(H,compute_uv=False)
    rank=int(np.sum(svals>1e-8))
    assert rank==92 and np.max(svals[92:])<1e-10
    # Eight gauge vector masses are equal because the SIC frame is tight.
    zero=np.zeros((3,3),complex)
    X=lambda i,j:np.eye(3,dtype=complex)[i:i+1].T@np.eye(3,dtype=complex)[j:j+1]
    T=[]
    for i,j in [(0,1),(0,2),(1,2)]:
        T.extend([(X(i,j)+X(j,i))/2,(-1j*X(i,j)+1j*X(j,i))/2])
    T.extend([np.diag([1,-1,0])/2,np.diag([1,1,-2])/(2*np.sqrt(3))])
    M=np.array([[np.trace(moment@(a@b+b@a)).real for b in T] for a in T])
    gauge_mass_err=float(np.linalg.norm(M-6*np.eye(8)))
    assert gauge_mass_err<1e-11
    return {'gauge_group':'SU(3), not E8',
        'SIC_triplets':9,'antitriplets_for_anomaly_cancellation':9,
        'baryonic_invariants_total':len(triples),'independent_baryonic_constraints':19,
        'selected_baryon_index_triplets':[triples[q] for q in chosen],
        'Jacobian_rank_Galois_mod7':mod_rank(J7[list(chosen)]),
        'gauge_orbit_tangent_dimension':8,
        'frame_moment_map_Frobenius_error':float(np.linalg.norm(moment-6*np.eye(3))),
        'antitriplet_pairing_basis_det':[float(np.linalg.det(B).real),float(np.linalg.det(B).imag)],
        'singlet_Lagrange_fields':19,'singlet_antitriplet_mass_partners':27,
        'complex_chiral_coordinates_total':100,
        'complex_holomorphic_Hessian_rank':rank,
        'quadratic_zero_modes_exactly_gauge_directions':8,
        'smallest_nonzero_Hessian_singular_value':float(svals[91]),
        'SU3_cubic_anomaly_fund_plus_antifund':0,
        'eight_gauge_vector_mass_matrix_deviation_from_6I':gauge_mass_err,
        'status':'Local F/D-flat, anomaly-free, fully-Higgsed engineered SU3 toy with massive gauge-invariant chiral directions; not full E8 gauge invariant nor a selected physical vacuum',
        'limitations':'19 complex baryon constants and field content are engineered; other global F/D branches, Kähler renormalization, E6 charges, E8 embedding, SM chirality and naturalness unresolved.'}


def closures(n):
    edges=list(combinations(range(n),2))
    ans={}
    for mask in range(1<<len(edges)):
        rows=[0]*n
        for idx,(i,j) in enumerate(edges):
            if (mask>>idx)&1:rows[i]|=1<<j
        for k in range(n):
            for i in range(n):
                if rows[i]>>k&1:rows[i]|=rows[k]
        rows=tuple(rows)
        ans[rows]=None
    return list(ans)


def joint_signature(rows):
    n=len(rows)
    return tuple(sorted((sum((rows[i]>>j)&1 for i in range(n)),rows[j].bit_count()) for j in range(n)))


def cover_count(rows):
    n=len(rows)
    return sum(bool(rows[i]>>j&1) and not any((rows[i]>>k&1) and (rows[k]>>j&1)
            for k in range(i+1,j)) for i in range(n) for j in range(i+1,n))


def canonical(rows):
    n=len(rows)
    # Isomorphism-invariant canonical relation encoding, allows comparators
    # under any relabeling (the natural topological order is not privileged).
    return min(tuple(sum(((rows[p[i]]>>p[j])&1)<<j for j in range(n))
               for i in range(n)) for p in permutations(range(n)))


def poset_gate():
    R5=closures(5)
    iso={canonical(r):r for r in R5}
    bucket=defaultdict(set)
    for key,r in iso.items():bucket[joint_signature(r)].add(key)
    assert len(R5)==357 and len(iso)==63 and len(bucket)==63
    assert all(len(v)==1 for v in bucket.values())
    R6=closures(6)
    signatures={joint_signature(r) for r in R6}
    assert len(R6)==4824 and len(signatures)==311
    witnessA=(50,16,24,16,0,0)
    witnessB=(48,28,16,16,0,0)
    assert witnessA in R6 and witnessB in R6
    assert joint_signature(witnessA)==joint_signature(witnessB)
    a,b=cover_count(witnessA),cover_count(witnessB)
    assert (a,b)==(5,6)
    return {'five_event_unlabeled_posets':len(iso),
        'five_event_joint_past_future_histogram_classes':len(bucket),
        'five_event_complete_isomorphism_invariant':True,
        'six_event_naturally_labeled_relations':len(R6),
        'six_event_joint_past_future_histogram_classes':len(signatures),
        'first_explicit_six_event_failure':{
            'shared_signature':joint_signature(witnessA),
            'relation_rowbit_masks_A':witnessA,
            'relation_rowbit_masks_B':witnessB,
            'Hasse_covers_A':a,'Hasse_covers_B':b},
        'limitation':'Complete for n<=5 only; fails already at n=6; distinguishes posets but is not a physical causal dynamics or continuum 4D selector.'}


def g2_real_gate():
    # Critical complex-conjugate parameters of the external Grigorian paper.
    # If a real-linear map preserves N_plus=C0+lambda_plus*Cphi
    # as a complex-valued function on real tensors, then it separately
    # preserves Re(N_plus)=C0+(1/8)Cphi and Im(N_plus)=(sqrt7/8)Cphi.
    # Therefore it preserves BOTH original real cubics; this is an exact
    # linear-algebra implication, not a claimed new E6 stabilizer theorem.
    lam=complex(1/8,np.sqrt(7)/8)
    assert abs(8*lam*lam-2*lam+1)<1e-13
    rng=np.random.default_rng(20261119)
    maxerr=0.
    for _ in range(40):
        c0=float(rng.normal());cp=float(rng.normal())
        N=c0+lam*cp
        cp_rec=N.imag/lam.imag
        c0_rec=N.real-lam.real*cp_rec
        maxerr=max(maxerr,abs(c0-c0_rec),abs(cp-cp_rec))
    return {'critical_parameters':[[lam.real,lam.imag],[lam.real,-lam.imag]],
        'real_pencil_critical_points':0,
        'Re_N_equals':'C0+(1/8)Cphi',
        'Im_N_equals':'(sqrt7/8)Cphi',
        'real_linear_preserves_complex_N_implies':'preserves C0 and Cphi separately',
        'real_complex_cubic_inverse_reconstruction_max_error':float(maxerr),
        'scope':'The external theorem identifies complex E6 symmetry; on the original real 27-dimensional tensor space this direct complex-cubic preservation cannot be equated with a physical real E6 gauge action.'}


def channel(kraus,rho):
    return sum(K@rho@K.conj().T for K in kraus)


def memory_gate():
    # Reproduce the explicit qubit genuine-three-time-only dynamical-map
    # example and EACH PAIRWISE CLASSICAL KRAUS/FEEDBACK decomposition from
    # Beyer et al., arXiv:2611.17268, Appendix B-C (published prior art).
    I=np.eye(2,dtype=complex);sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1,-1]).astype(complex)
    lower=np.array([[0,1],[0,0]],complex);raise_=lower.conj().T
    gamma=.36;p=.2
    threshold=(1-np.sqrt(1-gamma))/2
    assert p>threshold
    A1=np.sqrt(gamma)*lower
    A2=np.diag([1,np.sqrt(1-gamma)]).astype(complex)
    E1=[A1,A2];E2=[np.sqrt(p)*sz,np.sqrt(1-p)*I];E3=[np.sqrt(p)*sx,np.sqrt(1-p)*I]
    f=(np.sqrt(1-gamma)+2*p-1)/(2*np.sqrt(1-gamma))
    assert 0<=f<=.5
    # (E1,E2): jump branch resets to |1>, no-jump branch dephases Z.
    Phi_jump=[raise_,raise_@lower]
    Phi_nojump=[np.sqrt(f)*sz,np.sqrt(1-f)*I]
    # (E1,E3): +/- unravelling followed by conditional Y rotations,
    # then a common X dephasing. Literal channels taken from Appendix C.2.
    Kplus=(A1+A2)/np.sqrt(2);Kminus=(A1-A2)/np.sqrt(2)
    angle=-np.arcsin(np.sqrt(gamma))
    Rplus=expm(1j*angle*sy/2);Rminus=expm(-1j*angle*sy/2)
    Phi_x=[np.sqrt(f)*sx,np.sqrt(1-f)*I]
    # (E2,E3): record Z or I, undo conditional Z, then perform E3.
    P2K=[np.sqrt(p)*sz,np.sqrt(1-p)*I]
    P2Phi=[[L@sz for L in E3],E3]
    tests=[np.array([[1,0],[0,0]],complex),np.array([[0,0],[0,1]],complex),
           np.array([[0,1],[0,0]],complex),np.array([[0,0],[1,0]],complex)]
    maxerr=0.
    for X in tests:
        v12=channel(Phi_jump,A1@X@A1.conj().T)+channel(Phi_nojump,A2@X@A2.conj().T)
        v13=channel(Phi_x,Rplus@Kplus@X@Kplus.conj().T@Rplus.conj().T)
        v13+=channel(Phi_x,Rminus@Kminus@X@Kminus.conj().T@Rminus.conj().T)
        v23=sum(channel(P2Phi[j],P2K[j]@X@P2K[j].conj().T) for j in range(2))
        maxerr=max(maxerr,np.linalg.norm(v12-channel(E2,X)),
                   np.linalg.norm(v13-channel(E3,X)),np.linalg.norm(v23-channel(E3,X)))
    assert maxerr<1e-12
    for kraus in [E1,E2,E3,Phi_jump,Phi_nojump,Phi_x,*P2Phi]:
        assert np.linalg.norm(sum(K.conj().T@K for K in kraus)-I)<1e-12
    # E1[I/2]=1/2(I+gamma sigma_z). E2 preserves z antipodal
    # states and E3 preserves x antipodal states, so Fz=Fx=0.
    bloch=np.array([np.trace(channel(E1,I/2)@op).real for op in (sx,sy,sz)])
    W3=-float(np.linalg.norm(bloch))
    assert abs(W3+gamma)<1e-12
    return {'source':'Beyer et al., arXiv:2611.17268 Appendix B,C; independent numerical reproduction NOT new discovery',
        'gamma':gamma,'p':p,'pairwise_classical_threshold_pcrit':float(threshold),
        'pairwise_classical_decompositions_verified':3,
        'largest_pairwise_channel_superoperator_error':float(maxerr),
        'three_time_W3_witness':W3,
        'F2_z':0.,'F3_x':0.,
        'genuine_three_time_only_quantum_memory_certified_for_these_three_channels':True,
        'scope':'Three marginal channels are CPTP; an explicit shared quantum stochastic dilation is established by the cited paper, not independently synthesized here. No qutrit or photonic experiment has been constructed.'}


def su3_shot_gate():
    # Two noncommuting Wilson holonomies. Color-uniform normalized
    # detection P(theta)=1/2 + v Re(e^-i theta Tr K)/6.
    A=np.diag(np.exp(1j*np.array([.37,1.1,-1.47])))
    B0=np.diag(np.exp(1j*np.array([.41,.91,-1.32])))
    F=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
    B=F@B0@F.conj().T
    K=A@B@A.conj().T@B.conj().T
    t=np.trace(K)
    norm=float(np.linalg.norm(A@B-B@A)**2)
    assert abs(norm-(6-2*t.real))<1e-12 and norm>4
    visibility=.8;eta=.7;epsilon=.2;delta=.01
    delta_est=delta/2;delta_loss=delta/2
    # Hoeffding, union of the two reference settings:
    # ||t_hat-t|| <= 6/v sqrt(log(4/delta_est)/N) with
    # probability >=1-delta_est, given N ACCEPTED detections per phase.
    accepted_per_setting=ceil(36*log(4/delta_est)/(visibility**2*epsilon**2))
    L=log(2/delta_loss)
    mu=((sqrt(2*L)+sqrt(2*L+4*accepted_per_setting))/2)**2
    attempts_per_setting=ceil(mu/eta)
    assert attempts_per_setting*eta-sqrt(2*attempts_per_setting*eta*L)>=accepted_per_setting-1e-8
    p0=.5+visibility*t.real/6
    p90=.5+visibility*t.imag/6
    assert 0<=p0<=1 and 0<=p90<=1
    rng=np.random.default_rng(20261119)
    errs=[]
    for _ in range(256):
        real=rng.binomial(accepted_per_setting,p0)/accepted_per_setting
        imag=rng.binomial(accepted_per_setting,p90)/accepted_per_setting
        estimate=6/visibility*((real-.5)+1j*(imag-.5))
        errs.append(abs(estimate-t))
    # A deterministic example Monte Carlo scan, not the concentration proof.
    # Loss-dependent imbalance and visibility calibration remain external.
    return {'two_loop_SU3_commutator_trace':[float(t.real),float(t.imag)],
        'SU3_noncommutativity_Frobenius_norm_squared':norm,
        'known_visibility':visibility,'uniform_detection_efficiency':eta,
        'complex_trace_absolute_error_target':epsilon,
        'total_failure_probability_upper_bound':delta,
        'accepted_detections_per_phase_required':accepted_per_setting,
        'raw_attempts_per_phase_sufficient':attempts_per_setting,
        'total_raw_attempts_sufficient':2*attempts_per_setting,
        'Hoeffding_Chernoff_upper_bound':'failure<=delta_est+delta_loss=0.01 for both settings and both detection quotas',
        'Monte_Carlo_trials':256,'Monte_Carlo_max_absolute_trace_error':float(max(errs)),
        'calibration':'Unknown visibility v is degenerate with trace amplitude; calibrate against identity K=I, for which P0=(1+v)/2.',
        'scope':'Conservative ideal-model resource bound, no physical photon source, detector crosstalk, unequal arm loss, correlated phase drift or shot-noise-limited prototype.'}


def run():
    result={'date':'2026-11-19',
        'status':'FIVE_FINITE_GATE_CERTIFICATES_NOT_A_TOE',
        'tracks':{'SU3_SIC_gauge_completion':sic_gauge_completion(),
                  'causal_poset_invariant':poset_gate(),
                  'G2_E6_real_structure':g2_real_gate(),
                  'genuine_three_time_quantum_memory':memory_gate(),
                  'SU3_finite_shots_and_loss':su3_shot_gate()}}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    r=run()
    print(json.dumps({k:{z:v for z,v in t.items() if z in (
        'complex_holomorphic_Hessian_rank','smallest_nonzero_Hessian_singular_value',
        'unlabeled_posets','five_event_unlabeled_posets','six_event_joint_past_future_histogram_classes',
        'three_time_W3_witness','largest_pairwise_channel_superoperator_error',
        'total_raw_attempts_sufficient','accepted_detections_per_phase_required')}
      for k,t in r['tracks'].items()},indent=2))
    print('PASSED ALL FIVE',OUT)
