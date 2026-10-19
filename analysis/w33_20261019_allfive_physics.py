"""All-five continuation: microscopic no-go, thermal frontiers, exact echo,
and finite Clifford-module diagnostics. Distinguish exact identities from
restricted numerical optimization and conditional experimental protocols.
"""
from __future__ import annotations
import json, itertools, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
from w33_20261019_tick_operator_frame_majorization import points, symp, pauli, build_projectors
from w33_20261019_tick_commutator_extremum import maximal_cliques

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_allfive_physics.json"
P=build_projectors(points())
ps=points()
B=np.array([[int(i!=j and symp(a,b)!=0) for j,b in enumerate(ps)] for i,a in enumerate(ps)])
adj=np.ones((40,40),dtype=int)-np.eye(40,dtype=int)-B
K=(4/3)*np.kron(B,np.ones((3,3)))
I=np.eye(9)
pauli0=P[::3]
rng=np.random.default_rng(20261019)
CL=maximal_cliques([sum(int(B[i,j])<<j for j in range(40)) for i in range(40)])
seven=next(x for x in CL if len(x)==7)

def free_rates(w,T):
    vals=eigh(I-np.tensordot(w,P,axes=1),eigvals_only=True)
    return float(-T*np.log(np.exp(-vals/T).sum()))

def fgrad40(s,T,kappa):
    H=I-np.tensordot(s,pauli0,axes=1)
    eig,U=eigh(H)
    Gibbs=np.exp(-(eig-eig[0])/T)
    Gibbs/=Gibbs.sum()
    F=float(eig[0]-T*np.log(np.exp(-(eig-eig[0])/T).sum()))
    rho=(U*Gibbs)@U.conj().T
    dF=-np.einsum("ij,pji->p",rho,pauli0).real
    C=float((2/3)*s@B@s)
    dC=(4/3)*B@s
    return F+kappa*C,dF+kappa*dC

def track1():
    a=0
    comm=next(j for j in range(1,40) if adj[a,j])
    noncomm=next(j for j in range(1,40) if B[a,j])
    overlap=lambda j:float(np.trace(P[0]@P[3*j]).real)
    # High-T F=-T ln9+2/3-(Tr Q^2-1)/(18 T)+O(T^-2);
    # the pair coefficients are independent of W33 collinearity.
    ws=rng.dirichlet(np.ones(120),size=12)
    residual=[]
    for w in ws:
        Q=np.tensordot(w,P,axes=1)
        exact=float(np.trace(Q@Q).real)
        formula=float(1+3*np.dot(w,w)-sum(np.sum(w[3*p:3*p+3])**2 for p in range(40)))
        residual.append(abs(exact-formula))
    # Constructive conditional source: an engineered Wilson plaquette built
    # from projector-phase gates. U_ab=U_a U_b U_a^dag U_b^dag,
    # U_a=I+(exp(i theta)-1) P_a. The exact trace identity gives
    # S_W = gamma sum_{a<b} w_a w_b [1-Re Tr U_ab/9]
    # = gamma |exp(i theta)-1|^4 /18 * C(w), gamma>=0.
    # This is an explicit *additional* action, not derived from the
    # bare two-qutrit Gibbs partition function of Pass 12055.
    theta=np.pi/2
    wilson_kappa=abs(np.exp(1j*theta)-1)**4/18
    wilson_pair=(8/27)*0.25
    assert abs(wilson_pair-wilson_kappa*(1/3)) < 1e-12
    return {
      "result":"NO-GO for W33-incidence dependence in quadratic/high-temperature variance of fixed-rate Gibbs model",
      "overlap_collinear":overlap(comm),"overlap_noncollinear":overlap(noncomm),
      "exact_trQ2":"Tr Q^2 = 1 + 3 sum_a w_a^2 - sum_p (sum_k w_pk)^2",
      "high_T_expansion":"F_T = -T log 9 + 2/3 -(Tr Q^2-1)/(18T)+O(T^-2), sum w=1",
      "max_trace_residual":max(residual),
      "conditional_wilson_plaquette_action":"gamma sum_{a<b} w_a w_b [1-ReTr(Ua Ub Ua^dag Ub^dag)/9] = kappa C; Ua=exp(i theta Pa)",
      "derived_kappa":"gamma |exp(i theta)-1|^4 / 18 >= 0 for gamma>=0",
      "theta_pi_over_two_kappa_per_gamma":float(wilson_kappa),
      "negative_kappa_requires_nonstandard_sign_or_active_dynamics":True,
      "scope":"This does not exclude W33 at third+ order or a separately specified matter-induced effective action",
      "pass":abs(overlap(comm)-overlap(noncomm))<1e-12 and max(residual)<1e-10
    }

def track2():
    one=np.eye(40)[0]
    nonedge=next(j for j in range(1,40) if B[0,j])
    pair=np.zeros(40);pair[[0,nonedge]]=1/2
    line=next((tuple([i,j]+[q for q in range(40) if q!=i and q!=j and adj[i,q] and adj[j,q]][:2])
               for i in range(40) for j in range(i+1,40) if adj[i,j]),None)
    line=np.array(line,dtype=int)
    linew=np.zeros(40);linew[line]=1/4
    hept=np.zeros(40);hept[list(seven)]=1/7
    allw=np.ones(40)/40
    patterns={"singleton":one,"noncommuting_pair":pair,"commuting_line":linew,
              "heptad_7":hept,"uniform_40":allw}
    def getC(s):return float((2/3)*s@B@s)
    family=[]
    for T in (.2,.5,1.):
        f0=free_rates(np.kron(one,np.array([1,0,0])),T)
        fh=free_rates(np.kron(hept,np.array([1,0,0])),T)
        crossing=(f0-fh)/getC(hept)
        e=np.exp(-1/T)
        local_threshold=-1.5*(1-e)/(3+6*e)
        family.append({
          "temperature":T,"single_heptad_equal_energy_kappa":crossing,
          "single_vertex_local_instability_kappa":local_threshold,
          "pattern_F_and_C":{name:{"F":free_rates(np.kron(s,[1,0,0]),T),"C":getC(s)}
                            for name,s in patterns.items()}
        })
    # Restricted controlled ansatz: one outcome k=0 per Pauli direction.
    # No guarantee of global minimum over all 120 tick coordinates.
    numerical=[]
    for T in (.2,.5,1.):
        for kap in (-1.0,-.5,-.25,0.25):
            starts=[one,hept,allw,rng.dirichlet(np.ones(40))]
            sols=[]
            for guess in starts:
                res=minimize(fgrad40,guess,args=(T,kap),jac=True,method="SLSQP",
                    bounds=[(0,1)]*40,
                    constraints=[{"type":"eq","fun":lambda s:np.sum(s)-1,
                                  "jac":lambda s:np.ones_like(s)}],
                    options={"maxiter":100,"ftol":1e-9})
                sols.append((float(res.fun),res.x,bool(res.success)))
            best=min(sols,key=lambda t:t[0])
            numerical.append({"T":T,"kappa":kap,"best_energy":best[0],
              "support_over_1e-3":int(sum(best[1]>1e-3)),
              "best_C":getC(best[1]),"all_optimizers_reported_success":all(x[2] for x in sols),
              "scope":"heuristic restricted k=0-only 40-variable SLSQP, 4 starts"})
    return {
       "rigorous":"For kappa>=0, one tick globally minimizes F+kappa C (C>=0). For kappa<0, an upper test envelope from singleton and heptad; no global finite-kappa phase boundary established.",
       "finite_size_firewall":"Analytic Gibbs free energy of 9-dimensional fixed Hamiltonian; optimized order parameter can switch but not thermodynamic-limit criticality",
       "heptad_indices":list(seven),
       "family_scans":family,"restricted_SLSQP":numerical,
       "pass":abs(getC(hept)-4/7)<1e-11 and all(x["C"]>=-1e-12 for f in family for x in f["pattern_F_and_C"].values())
    }

def trace_echo(p,q,theta):
    z=np.exp(1j*theta)
    A=I+(z-1)*P[3*p]; D=I+(z-1)*P[3*q]
    U=A@D@A.conj().T@D.conj().T
    return float(1-np.trace(U).real/9)

def track3():
    zero=next(j for j in range(1,40) if adj[0,j])
    signal=next(j for j in range(1,40) if B[0,j])
    cases=[]
    err=0
    for theta in (.15,.5,1.,math.pi/2,math.pi):
        observed=trace_echo(0,signal,theta)
        predicted=float((32/27)*math.sin(theta/2)**4)
        null=trace_echo(0,zero,theta)
        err=max(err,abs(observed-predicted),abs(null))
        cases.append({"theta":theta,"noncommuting_deficit":observed,
                      "exact_prediction":predicted,"commuting_null_deficit":null})
    delta=8/27 # theta = pi/2
    alpha=.05
    shots=math.ceil(32*math.log(4/alpha)/(delta**2))
    return {
      "exact_identity":"1-Re Tr(Ucomm)/9 = |exp(i theta)-1|^4 ||[P,Q]||_F^2/18",
      "noncommuting_exact":"(32/27) sin(theta/2)^4",
      "commuting_exact":"zero for all theta",
      "cases":cases,"worst_numeric_residual":err,
      "interferometric_protocol":"Prepare maximally mixed 9-level target or maximally entangled Choi state; ancilla Hadamard-test real trace of Ucomm, with four controlled projector-phase gates; compare commuting control; phase randomization, detector/electronics sham.",
      "theta_pi_over_two_signal":delta,
      "total_shots_two_configs_95_percent_conservative":2*shots,
      "shots_per_config":shots,
      "shot_formula":"N >= 32 log(4/alpha) / delta^2 per condition for P(error of either mean by >= delta/4)<=alpha (Hoeffding)",
      "visibility_caution":"If ancilla fringe visibility v<1, replace delta by v*delta; require independent calibration and common-mode controls",
      "scope":"Exact unitary circuit prediction, not experimentally implemented or a demonstration of a literal past-future photon",
      "pass":err<1e-12
    }

def track4():
    # Conjugation by Pauli translations on the 80-dimensional traceless
    # two-qutrit Hermitian operators: nonidentity projective Pauli t acts
    # with trace |Tr D_t|^2-1=-1 on traceless 80-space.
    axes=[tuple(v) for v in itertools.product(range(3),repeat=4)]
    census=[]
    for t in axes:
        if not any(t):continue
        orbit=[symp(t,p) for p in ps]
        counts={str(k):orbit.count(k) for k in range(3)}
        # each p contributes 2 if fixed, -1 if shifted
        char=sum(2 if q==0 else -1 for q in orbit)
        census.append((char,counts))
    vals=set(x[0] for x in census)
    count_set=set(tuple(x[1][str(j)] for j in range(3)) for x in census)
    # 120 outcomes form a permutation action; 39-dimensional identity
    # relation kernel is pointwise fixed under Pauli translations.
    # character on 120 =39; subtract kernel 39 gives 0 on full M_9,
    # subtract scalar 1 gives -1 on traceless sector.
    return {
      "representation":"80-dimensional real traceless Hermitian qutrit-operator module, 40 orthogonal real 2-planes (Pauli directions)",
      "complexification":"80 one-dimensional nontrivial F3^4 characters, indexed by 80 nonzero displacement vectors",
      "Pauli_translation_nontrivial_character":-1,
      "Pauli_translation_80_actions_checked":len(census),
      "orthogonal_projective_points_to_nonzero_translation_counts":[13,27],
      "outcome_fixed_point_trace_120":39,
      "underlying_adjoint_trace81":0,
      "irreducibility":"As representation of affine symplectic/Clifford semidirect product F3^4 : Sp(4,3), the 80 complex nontrivial Pauli characters are permuted transitively, so the 80-dimensional complex representation is irreducible.",
      "E8_intertwiner_status":"OPEN: an 80-dimensional count or E8=80+56+56+56 is insufficient for equivariance; compare explicit generating matrices / characters before asserting module isomorphism",
      "scope":"Exact finite operator representation, not a physical E8 gauge identification",
      "pass":vals=={-1} and all(x[0]==13 and x[1]+x[2]==27 for x in count_set) and len(census)==80
    }

def main():
    parts={"microscopic":track1(),"phase":track2(),"echo":track3(),"representation":track4()}
    checks={k:bool(v["pass"]) for k,v in parts.items()}
    result={"schema":"w33.toe.tick_allfive.physics.v1","source_date":"2026-10-19",
            "status":"MATH_VERIFIED_PHYSICAL_DERIVATION_OPEN",
            "tracks":parts,"checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"checks":checks,"max_echo_residual":parts["echo"]["worst_numeric_residual"],
        "meas_shots":parts["echo"]["shots_per_config"],
        "crossover":parts["phase"]["family_scans"],"phase_optima":parts["phase"]["restricted_SLSQP"]},
        indent=2))
    assert result["all_checks_pass"]
    return result

if __name__=="__main__":
    main()
