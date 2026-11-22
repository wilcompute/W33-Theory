"""Five experiment-led W33/Witting falsifiers (2026-11-22).

Motivations: experimental causal-switch tests, contextuality QRNG, loophole-free
ququart multioutcome Bell tests, Z2 gauge Aharonov-Bohm interference, photonic
Klein-bottle exceptional topology. The experiments do NOT demonstrate W33.
No physical experiment, security proof, spacetime or gauge dynamics is claimed.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
import toe_20261121_relational_reference_pareto as geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261122_experiment_driven_five_fronts.json"
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]
PRIVATE=[0,1,2,5,6,8,10,11,12,13,15,16,19,21,23,24,27,28,30,32,34,35,37,39]

EXPERIMENTS={
 "causal_switch":"https://doi.org/10.1126/sciadv.aee2912",
 "contextuality_QRNG":"https://doi.org/10.1103/62lv-gmsz",
 "binarization_loophole_ququart":"https://doi.org/10.1103/ydch-vgmy",
 "Z2_AB_gauge":"https://doi.org/10.1038/s41567-026-03400-6",
 "Klein_photonic_topology":"https://doi.org/10.1038/s41377-026-02516-x"
}

def witting():
    rays,H,A,P=geometry.geometry()
    assert rays.shape==(40,4) and H.shape==(45,40)
    assert set(H.sum(0))=={9} and set(H.sum(1))=={8}
    return rays,H,A,P

def ray_projectors(rays):
    Q=np.einsum("ai,aj->aij",rays,rays.conj())
    assert np.max(abs(Q.sum(0)-10*np.eye(4)))<1e-11
    return Q

def switch_front(rays):
    """State-mixed controlled order of Householder ray reflections."""
    Q=ray_projectors(rays);I=np.eye(4,dtype=complex)
    overlap=np.einsum("aij,bji->ab",Q,Q).real
    counts={"orthogonal":0,"nonorthogonal":0};residual=0.
    for a,b in itertools.combinations(range(40),2):
        r=float(overlap[a,b]);U=I-2*Q[a];V=I-2*Q[b]
        comm=V@U-U@V
        pm=float(np.vdot(comm,comm).real/16)  # rho=I4/4 and 50/50 order control
        residual=max(residual,abs(pm-2*r*(1-r)))
        if abs(r)<1e-11:
            counts["orthogonal"]+=1
            assert abs(pm)<1e-11
        else:
            counts["nonorthogonal"]+=1
            assert abs(r-1/3)<1e-11 and abs(pm-4/9)<1e-11
    assert counts=={"orthogonal":240,"nonorthogonal":540}
    assert residual<1e-11
    for v in (0,.2,.5,.8,1):
        pc=(1-v)/2
        pn=pc+v*4/9
        assert abs(pn-pc-v*4/9)<1e-12
    return {"status":"PASS","unordered_pairs":780,"ray_pair_counts":counts,
        "commuting_minus_probability":0.0,
        "noncommuting_minus_probability":4/9,
        "exact_mixed_target_formula":"pminus=2*r*(1-r), r=Tr(Pa Pb)",
        "max_analytic_residual":residual,
        "dephased_switch_visibility_formula":"pminus(v)=(1-v)/2+v*pminus(1)",
        "globally_conjugating_ray_vectors_cannot_change_two_reflection_result":True,
        "boundary":"A ququart switch-pair overlap witness, NOT a device-independent causal inequality or an oriented Bargmann-phase witness."}

def readout_matrix(sel):
    assert len(set(sel))==len(sel)==24
    C=np.zeros((25,40),dtype=int)
    C[np.arange(24),sel]=1
    C[-1,[i for i in range(40) if i not in sel]]=1
    assert np.all(C.sum(0)==1)
    return C

def entropy_front(H):
    """Raw/conditioned classical minentropy, not secure random bits."""
    conditional=H/8
    assert np.max(abs(conditional.sum(1)-1))<1e-11
    rows=[]
    for name,C in [("full40",np.eye(40)),("old25",readout_matrix(OLD)),
                   ("new25",readout_matrix(NEW)),("privacy25",readout_matrix(PRIVATE))]:
        p=conditional@C.T
        raw=-math.log2(float(p.mean(0).max()))
        known=-math.log2(float(np.mean(p.max(1))))
        rows.append({"detector":name,"number_outcomes":int(len(C)),
                     "raw_classical_Hmin_bits":raw,"given_chart_Hmin_bits":known})
    assert abs(rows[0]["raw_classical_Hmin_bits"]-math.log2(40))<1e-11
    assert abs(rows[0]["given_chart_Hmin_bits"]-3)<1e-11
    for r in rows[1:]:
        assert abs(r["raw_classical_Hmin_bits"]-math.log2(2.5))<1e-11
        assert abs(r["given_chart_Hmin_bits"]-math.log2(2.5))<1e-11
    return {"status":"PASS","detector_profiles":rows,
         "compression_exact_raw_Hmin_loss_bits":4.,
         "security_certified_quantum_min_entropy":False,
         "full_outcome_known_to_adversary_Hmin_bits":0.,
         "boundary":"Only observed classical distributions. No trusted contextuality test, no semi-device-independent security model or randomness certification; 2026 qutrit QRNG reported 0.077±0.002 certified bits under DIFFERENT assumptions."}

def MI(P):
    assert abs(P.sum()-1)<1e-10
    Q=np.outer(P.sum(1),P.sum(0))
    mask=P>1e-15
    return float(np.sum(P[mask]*np.log2(P[mask]/Q[mask])))

def bell_front(rays):
    """One true 40-outcome ququart POVM on each half of |Phi4>, not Bell violation."""
    Q=ray_projectors(rays)
    r=np.einsum("aij,bji->ab",Q,Q).real
    # E_i=Pi/10, F_j=conj(Pj)/10, and |Phi4> yields p_ij=Tr(PiPj)/400
    p=r/400
    assert np.max(abs(p.sum(0)-1/40))<1e-11
    ideal=MI(p)
    assert abs(ideal-(.2+.9*math.log2(4/3)))<1e-11
    vals=[]
    for name,C in [("full40",np.eye(40)),("old25",readout_matrix(OLD)),
                   ("new25",readout_matrix(NEW)),("privacy25",readout_matrix(PRIVATE))]:
        joint=C@p@C.T
        bits=MI(joint)
        assert bits<=ideal+1e-11
        vals.append({"detector":name,"joint_outcome_count":int(len(C)**2),
                     "classical_mutual_information_bits":bits,
                     "fraction_of_full_joint_information":bits/ideal})
    assert abs(vals[1]["classical_mutual_information_bits"]-.23449967635092483)<1e-11
    assert abs(vals[2]["classical_mutual_information_bits"]-.22342229274284534)<1e-11
    assert vals[1]["classical_mutual_information_bits"]>vals[2]["classical_mutual_information_bits"]
    return {"status":"PASS","joint_formula":"P(i,j)=Tr(Pi Pj)/400",
       "full_mutual_information_exact":".2+.9*log2(4/3)",
       "detectors":vals,
       "one_fixed_setting_is_locally_simulable":True,
       "explicit_single_setting_LHV":"shared variable (i,j) sampled with p(i,j), deterministic local outputs",
       "boundary":"These are multioutcome correlations, NOT Bell-inequality violation. At least two settings, specified Bell functional and device accounting needed."}

def W33():
    points=[]
    for lead in range(4):
        for tail in itertools.product(range(3),repeat=3-lead):
            points.append((0,)*lead+(1,)+tail)
    def sp(a,b):
        return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
    A=np.array([[int(i!=j and sp(u,v)==0)
               for j,v in enumerate(points)] for i,u in enumerate(points)])
    assert len(points)==40 and set(A.sum(0))=={12}
    assert np.max(abs(np.sort(np.linalg.eigvalsh(A))-
           np.sort(np.r_[[-4]*15,[2]*24,[12]])))<1e-10
    return A

def gauge_AB_front():
    """A gauge-invariant interferometer on one graph four-cycle."""
    A=W33()
    candidates=[]
    for u in range(40):
        for v in range(u+1,40):
            if not A[u,v]:
                neighbors=np.flatnonzero((A[u]>0)&(A[v]>0)).tolist()
                assert len(neighbors)==4
                candidates.append((u,v,neighbors))
    assert len(candidates)==540
    u,v,commons=candidates[0];a,b=commons[:2]
    arms=[[(u,a),(a,v)],[(u,b),(b,v)]]
    edges=[(i,j)for i in range(40)for j in range(i+1,40)if A[i,j]]
    link=lambda x,y:(min(x,y),max(x,y))
    base={edge:1 for edge in edges}
    def Wilson(weights):
        return math.prod(weights[link(*e)] for arm in arms for e in arm)
    negative=base.copy();negative[link(*arms[0][0])]=-1
    assert Wilson(base)==1 and Wilson(negative)==-1
    rng=np.random.default_rng(20261122)
    for trial in range(200):
        s=rng.choice([-1,1],size=40)
        for t in (base,negative):
            changed={(i,j):t[i,j]*int(s[i])*int(s[j])for i,j in edges}
            assert Wilson(changed)==Wilson(t)
    return {"status":"PASS","vertices":40,"edges":len(edges),
       "cycle_rank":len(edges)-40+1,
       "four_cycles_selected_from_nonadjacent_pair":540,
       "example_loop":[u,a,v,b,u],
       "two_arm_interference_probability":"Pplus=(1+Wilson)/2",
       "positive_flux_Pplus":(1+Wilson(base))/2,
       "negative_flux_Pplus":(1+Wilson(negative))/2,
       "local_gauge_transformation_checks":400,
       "boundary":"Externally specified STATIC Z2 links on W33 and abstract paths; not gauge-field dynamics, Gauss laws or an experimental Aharonov-Bohm signal."}

def grid(L,twisted):
    """Horizontal periodic, vertical seam reflected if twisted."""
    id=lambda x,y:(x%L)*L+(y%L)
    E=set()
    for x in range(L):
        for y in range(L):
            E.add(tuple(sorted((id(x,y),id(x+1,y)))))
            top=id(x,y+1) if y<L-1 else id(L-1-x if twisted else x,0)
            E.add(tuple(sorted((id(x,y),top))))
    assert len(E)==2*L*L
    A=np.zeros((L*L,L*L),dtype=np.int64)
    for a,b in E:A[a,b]=A[b,a]=1
    assert set(A.sum(1))=={4}
    return A,E

def cover(L):
    """Connected 2-sheet orientation cover of the twisted square lattice."""
    id=lambda sh,x,y:((sh*L+x)*L+y)
    E=set()
    for sh in range(2):
        for x in range(L):
            for y in range(L):
                E.add(tuple(sorted((id(sh,x,y),id(sh,(x+1)%L,y)))))
                top=id(sh,x,y+1)if y<L-1 else id(1-sh,L-1-x,0)
                E.add(tuple(sorted((id(sh,x,y),top))))
    n=2*L*L;A=np.zeros((n,n),dtype=np.int64)
    for a,b in E:A[a,b]=A[b,a]=1
    assert set(A.sum(0))=={4}
    deck=np.array([id(1-sh,x,y)for sh in range(2)
                   for x in range(L)for y in range(L)])
    assert np.array_equal(A,A[np.ix_(deck,deck)])
    proj={tuple(sorted((a%(L*L),b%(L*L))))for a,b in E}
    assert proj==grid(L,True)[1]
    reach={0};stack=[0]
    while stack:
        for v in np.flatnonzero(A[stack.pop()]):
            v=int(v)
            if v not in reach:reach.add(v);stack.append(v)
    assert len(reach)==n
    return n

def Klein_front():
    rows=[]
    for L in (6,8):
        T,_=grid(L,False);K,_=grid(L,True)
        et=np.linalg.eigvalsh(T.astype(float))
        ek=np.linalg.eigvalsh(K.astype(float))
        assert min(et)<-3.99999 and min(ek)>-4+1e-6
        length,count=None,None
        for n in (3,5,7,9,11):
            assert int(np.trace(np.linalg.matrix_power(T,n)))==0
            x=int(np.trace(np.linalg.matrix_power(K,n)))
            if x>0 and length is None:length,count=n,x
        assert length==L+1
        assert math.prod([1]*(L-1)+[-1,1])==-1
        rows.append({"L":L,"vertices":L*L,
           "Klein_orientation_cover_vertices":cover(L),
           "torus_min_eigenvalue":float(min(et)),
           "Klein_min_eigenvalue":float(min(ek)),
           "spectral_l2_difference":float(np.linalg.norm(np.sort(et)-np.sort(ek))),
           "first_odd_Klein_closed_walk_length":length,
           "first_odd_Klein_closed_walk_count":count,
           "Klein_vertical_orientation_holonomy":-1,
           "torus_orientation_holonomy":1})
    return {"status":"PASS","grid_comparisons":rows,
       "orientation_double_cover":"two 2-sheet square lattices joined across reflected seam; connected cover and deck involution verified",
       "boundary":"A specific HERMITIAN finite-grid control of orientability, not a replica of non-Hermitian exceptional points. Odd graph cycle behavior is discretization-dependent and not equivalent to nonorientability in general."}

def main():
    rays,H,A,P=witting()
    results={
      "date":"2026-11-22","status":"PASS",
      "literature":EXPERIMENTS,
      "front1_Witting_reflection_quantum_switch":switch_front(rays),
      "front2_classical_minentropy_and_security_boundary":entropy_front(H),
      "front3_true_multioutcome_ququart_correlations":bell_front(rays),
      "front4_W33_Z2_two_path_AB_interference":gauge_AB_front(),
      "front5_torus_Klein_nonorientable_control":Klein_front(),
      "scope":"Five finite-model mathematical tests motivated by external 2026 experiments. No real measurements, certification of nonlocality/contextuality, or fundamental TOE."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS five external-literature experimental falsifiers",OUT,flush=True)
    return results

if __name__=="__main__":main()
