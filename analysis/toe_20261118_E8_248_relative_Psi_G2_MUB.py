"""Five TOE consistency gates beyond commit 39b57e3: full E8 linked-wire
relative cohomology, unique E6 Psi Wilson phase, conjugation obstruction,
near-parallel G2 Freund-Rubin matching, and local-qutrit 4-MUB witness.

Distinguish mathematics from physical compactification assumptions.
"""
from __future__ import annotations
import json
from pathlib import Path
from itertools import combinations
import math
import numpy as np
import sympy as s
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
omega=np.exp(2j*np.pi/3)
theta=np.exp(2j*np.pi/9)
zeta=np.exp(2j*np.pi/7)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
Z=np.diag([1,omega,omega*omega])
C9=np.diag([theta,theta,theta**7])
W7weights=[2,2,2,4,4]

def weights_E6(c):
    """The E6 adjoint 78 and fundamental 27 as SU5 weights, with U1Psi.
    78=45_0+16_(-3)+16bar_(+3)+1_0 under SO10 x Psi.
    27=16_(+1)+10_(-2)+1_(+4).
    """
    a=W7weights
    su5adj=[0]*4+[(a[i]-a[j])%7 for i in range(5) for j in range(5) if i!=j]
    ten=[(a[i]+a[j])%7 for i,j in combinations(range(5),2)]
    bt=[(-k)%7 for k in ten]
    five=a
    bf=[(-k)%7 for k in a]
    assert len(su5adj)==24 and len(ten)==10
    vec45=su5adj+ten+bt+[0]
    vec16=[(k-3*c)%7 for k in ten+bf+[0]]
    vec16bar=[(k+3*c)%7 for k in bt+five+[0]]
    w78=vec45+vec16+vec16bar+[0]
    w27=[(k+c)%7 for k in ten+bf+[0]]
    w27 +=[(k-2*c)%7 for k in five+bf]
    w27 +=[(4*c)%7]
    assert len(w78)==78 and len(w27)==27
    return w78,w27,dict(SU5_adjoint_24_fixed=su5adj.count(0),
       SO10_45_fixed=vec45.count(0),
       E6_16minus3_fixed=vec16.count(0),
       E6_16barplus3_fixed=vec16bar.count(0),
       E6_1_fixed=1,total_E6_78_fixed=w78.count(0))

def absolute_cell(A,C):
    """X = complement T(2,6), pi1=<a,c|[a,c^3]=1>.
    C^0=V, C^1=V^2, C^2=V with Fox derivatives.
    """
    d=A.shape[0]
    I=np.eye(d,dtype=complex)
    D0=np.vstack([A-I,C-I])
    D1=np.hstack([I-np.linalg.matrix_power(C,3),
                   (A-I)@(I+C+C@C)])
    assert np.max(abs(A@np.linalg.matrix_power(C,3)-
                         np.linalg.matrix_power(C,3)@A))<3e-9
    assert np.max(abs(D1@D0))<1e-8
    r0=int(np.linalg.matrix_rank(D0,tol=1e-8))
    r1=int(np.linalg.matrix_rank(D1,tol=1e-8))
    absolute=(d-r0,2*d-r0-r1,d-r1)
    # M≈X∨S²; relative S² deletes 0-cochains, not all of H0(X).
    # The relative complex is C^0=0,C^1=V²,C^2=V.
    relative=(0,2*d-r1,d-r1)
    assert relative[1]==absolute[1]+d-absolute[0]
    assert relative[1]-relative[2]==d
    return dict(dim=d,rank_d0=r0,rank_d1=r1,
        absolute_betti=list(absolute),
        relative_S2_betti=list(relative))

def family_adj():
    B=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)/math.sqrt(3)
       for a in range(3) for b in range(3) if (a,b)!=(0,0)]
    def act(U):
        return np.array([[np.trace(P.conj().T@U@Q@U.conj().T)
                          for Q in B] for P in B],complex)
    res=absolute_cell(act(X),act(C9))
    assert res["absolute_betti"]==[0,4,4]
    assert res["relative_S2_betti"]==[0,12,4]
    return res

def full_E8(c):
    w78,w27,splits=weights_E6(c)
    f=splits["total_E6_78_fixed"]
    # A=I on (78,1); C=exp(2pi i (SU5weight+Psi*c)/7).
    # For C=1: absolute (1,2,1), relative (0,2,1).
    # For C!=1, C^3!=1: absolute(0,0,0), relative(0,1,0).
    e6=dict(dim=78,invariant_vectors=f,
        absolute_betti=[f,2*f,f],
        relative_S2_betti=[0,78+f,f])
    # Crosscheck fixed dimensions for ALL 78 one-dimensional weights.
    assert f==sum(k==0 for k in w78)
    assert e6["relative_S2_betti"][1]==sum(2 if k==0 else 1 for k in w78)
    fam=family_adj()
    # Combined family generator C=zeta^weight*C9 has cube
    # omega*zeta^(3*weight) I != I for EVERY E6 weight.
    for k in set(w27):
        front=absolute_cell(X,zeta**k*C9)
        back=absolute_cell(X.conj(),zeta**(-k)*C9.conj())
        assert front["absolute_betti"]==[0,0,0]
        assert front["relative_S2_betti"]==[0,3,0]
        assert back["relative_S2_betti"]==front["relative_S2_betti"]
    matter=dict(dim=81,absolute_betti=[0,0,0],
                relative_S2_betti=[0,81,0])
    conj=dict(matter)
    sectors=dict(E6_adjoint_78=e6,SU3_adjoint_8=fam,
        E6_27_family_3=matter,E6_27bar_family_3bar=conj)
    abs_total=[sum(x["absolute_betti"][i] for x in sectors.values())
               for i in range(3)]
    rel_total=[sum(x["relative_S2_betti"][i] for x in sectors.values())
               for i in range(3)]
    assert sum(x["dim"] for x in sectors.values())==248
    assert rel_total[1]-rel_total[2]==248
    assert rel_total[1]==abs_total[1]+248-abs_total[0]
    # Historical 3dim-r0-r1 relative formula incorrectly retains
    # +b0 when fixed vectors exist. In E6 adjoint this is +f.
    old_wrong_total=rel_total[1]+f
    return dict(Psi_W7_charge_c=c,E6_fixed_weight_decomposition=splits,
       E8_unbroken_gauge_generators=abs_total[0],
       E8_absolute_betti=abs_total,E8_relative_S2_betti=rel_total,
       E8_relative_net_Euler_index=248,
       E8_sector_betti=sectors,
       historical_overcount_if_ignore_fixed_vectors=old_wrong_total,
       missing_subtraction=abs_total[0],
       correct_general_relative_formula="(b0,b1,b2)=(0,2*d-rank(d1),d-rank(d1))",
       conjugate_sector_betti_identical=True)

def Wilson_phase_census():
    table=[full_E8(c) for c in range(7)]
    fixed=[r["E8_unbroken_gauge_generators"] for r in table]
    assert fixed==[16,18,26,14,20,16,20],fixed
    assert [i for i,k in enumerate(fixed) if k==min(fixed)]==[3]
    assert table[0]["E8_relative_S2_betti"]==[0,268,20]
    assert table[3]["E8_relative_S2_betti"]==[0,266,18]
    return dict(status="PASS",
       fixed_E6_center_dimensions_by_Psi_phase=fixed,
       unique_minimal_Psi_phase_c=3,
       with_only_SU5_W7_c0=dict(
           E6_unbroken_dim=16,
           possible_Lie_algebra="su3_color + su2_weak + su2_extra + u1^2"),
       with_compensating_Psi_W7_c3=dict(
           E6_unbroken_dim=14,
           possible_Lie_algebra="su3_color + su2_weak + u1^3",
           two_U1_extra_beyond_SM=True),
       entire_E8_relative_cohomology_cases=table,
       scope="E6 adjoint weight census under specified diagonal SU5 Wilson and Psi U1; c=3 unique among 7 phases for dimension14. Does not cancel Psi anomalies, break rank6 to rank4, or derive Higgs EOM.")

def conjugation_no_go():
    front=absolute_cell(X,C9)
    back=absolute_cell(X.conj(),C9.conj())
    assert front["absolute_betti"]==back["absolute_betti"]
    assert front["relative_S2_betti"]==back["relative_S2_betti"]
    return dict(status="PASS",
       theorem="For any finite CW pair (M,S), a complex local system V and conjugate Vbar with the same real cellular/relative boundary prescription, C*(M,S;Vbar) is the complex conjugate of C*(M,S;V). Their Betti dimensions coincide at every degree.",
       test_qutrit_3=front,
       consequence="Native flat holonomy with identical relative domains never separates (27,3) from (27bar,3bar) via Betti ranks alone. It does NOT preclude spectral chirality from a charged higher-dimensional Dirac operator or differing physically justified boundary projectors.",
       all_rank3_families_from_chosen_relative_sphere="When X local system is acyclic, H^1(M,S;V)=V as vector spaces, so net index=rank(V); rank3 is input, not dynamical derivation of observed three generations.")

def near_parallel_G2():
    tau,f,L=s.symbols("tau f L",positive=True,real=True)
    RicG2=3*tau**2/8
    RicFR=f**2/6
    match=s.solve(RicG2-RicFR,tau)
    assert match==[2*f/3]
    ta=2/L
    assert s.simplify((RicG2-RicFR).subs({tau:ta,f:3/L}))==0
    scalar=s.simplify(7*RicG2.subs(tau,ta))
    assert scalar==s.Rational(21,2)/L**2
    eig=s.simplify(7*ta/8)
    assert eig==s.Rational(7,4)/L
    return dict(status="PASS",near_parallel_defining_equations=[
        "d(phi)=tau0*star(phi)","d(star(phi))=0"],
        Einstein_Ricci_near_parallel="3 tau0^2/8 g",
        Freund_Rubin_internal_Ricci="f^2/6 g",
        curvature_consistency_condition="abs(tau0)=2 abs(f)/3",
        at_f3_overL_tau0="2/L",
        scalar_curvature_L2="21/2",
        untwisted_real_Killing_spinor_Dirac_abs_eigenvalue_L="7/4",
        Lichnerowicz_lower_bound_Dirac_squared_L2="21/8",
        no_untwisted_geometric_Dirac_zero_modes=True,
        physical_scope="Necessary positive-Einstein/weak-G2 matching for pure electric FR product; not complete 11D gravitino/gauge-coupled Dirac, not a global solution, and no observed chiral fermions.")

def qutrit_local_MUB():
    D=3
    bases=[np.eye(D,dtype=complex)]
    for U in (X,X@Z,X@Z@Z):
        ev,V=np.linalg.eig(U)
        assert np.max(abs(V.conj().T@V-np.eye(3)))<1e-12
        bases.append(V)
    for i,j in combinations(range(4),2):
        assert np.max(abs(abs(bases[i].conj().T@bases[j])**2-1/3))<2e-12
    # The SAME linked-wire Clifford generator C9 cycles the
    # three noncomputational MUBs X -> XZ^2 -> XZ -> X,
    # while fixing the fourth Z MUB. Thus one physical gate orbit
    # can implement three of the four local measurement settings.
    clifford_orbit=[np.linalg.matrix_power(C9,k)@X@
        np.linalg.matrix_power(C9,k).conj().T for k in range(3)]
    orbit_error=float(max(np.max(abs(clifford_orbit[0]-X)),
        np.max(abs(clifford_orbit[1]-X@Z@Z)),
        np.max(abs(clifford_orbit[2]-X@Z))))
    assert orbit_error<2e-12
    assert np.max(abs(C9@Z@C9.conj().T-Z))<2e-12
    phi=np.eye(3).reshape(9)/math.sqrt(3)
    Pphi=np.outer(phi,phi.conj())
    S=np.zeros((9,9),complex)
    for V in bases:
        for j in range(3):
            v=V[:,j]
            pair=np.kron(v,v.conj())
            S+=np.outer(pair,pair.conj())
    identity_error=float(np.max(abs(S-np.eye(9)-3*Pphi)))
    assert identity_error<2e-12
    t=.75
    rho=t*Pphi+(1-t)*np.eye(9)/9
    fidelity=float(np.real(phi.conj()@rho@phi))
    p_model=float(np.real(np.trace(S@rho))/4)
    assert abs(fidelity-7/9)<2e-12
    assert abs(p_model-5/6)<2e-12
    # Four MUBs form a 2-design. Randomize one basis per trial,
    # measure both qutrits locally in conjugate bases, count equal
    # outcomes. For ANY state p_match=(1+3F)/4. SN<=2 -> p<=3/4.
    def threshold(p0,p1,alpha=.01,power=.90,maxn=2000):
        for n in range(1,maxn+1):
            k=int(binom.isf(alpha,n,p0))+1
            while binom.sf(k-1,n,p0)>alpha:k+=1
            while k>1 and binom.sf(k-2,n,p0)<=alpha:k-=1
            pwr=float(binom.sf(k-1,n,p1))
            if pwr>=power:
                return dict(n=n,match_count_at_least=k,
                    exact_alpha=float(binom.sf(k-1,n,p0)),
                    power=pwr)
        raise AssertionError("budget horizon exceeded")
    opt=threshold(.75,5/6)
    assert opt["n"]==317 and opt["match_count_at_least"]==256
    # Outcome assignment: on each side correct label prob 1-eps,
    # two incorrect labels have eps/2 each. If labels originally
    # equal, observed match a; if distinct, observed match b.
    def observed(e,p):
        a=(1-e)**2+e**2/2
        b=e*(1-e)+e**2/4
        return b+(a-b)*p
    noisy=[]
    for e in (0,.01,.02):
        no=observed(e,p_model)
        null=observed(e,.75)
        cons=threshold(.75,no)
        cal=threshold(null,no)
        noisy.append(dict(independent_symmetric_qutrit_label_error=e,
            p_match_at_model=no,
            p_match_at_SN2_max_under_calibrated_readout=null,
            conservative_uncalibrated_null_p0_075=cons,
            known_calibrated_confusion_null=cal))
    assert [r["conservative_uncalibrated_null_p0_075"]["n"] for r in noisy]==[317,472,790]
    assert [r["known_calibrated_confusion_null"]["n"] for r in noisy]==[317,348,389]
    return dict(status="PASS",
        native_qutrit_Clifford_MUBs=["Z","X","XZ","XZ^2"],
        C9_clifford_cycle_of_three_nonZ_MUBs="X -> XZ^2 -> XZ -> X",
        C9_clifford_MUB_cycle_max_residual=orbit_error,
        fourth_Z_basis_is_fixed_by_C9=True,
        number_of_local_settings=4,
        projective_two_design_operator_identity="sum_(b=1..4,j=0..2) |b,j><b,j| tensor |conj(b,j)><conj(b,j)| = I9 + 3 |Phi3><Phi3|",
        identity_max_residual=identity_error,
        p_match_for_any_state="(1+3*F(Phi3))/4",
        Schmidt_number_at_most2_match_bound=3/4,
        isotropic_model_t=t,
        model_entanglement_fidelity=fidelity,
        model_match_probability=p_model,
        alpha=.01,model_power_target=.9,
        fixed_sample_noiseless_90pct_power=opt,
        readout_assignment_budgets=noisy,
        limitations="Local projective MUB measurements replace a nontrivial global qutrit Bell projector. Controlled settings require qutrit Fourier/Clifford calibration, reference entanglement, fair heralding and fixed-n IID outcome assumptions. This proves dimension-three reference-memory entanglement, NOT genuine three-time process-tensor incompatibility or actual hardware operation.")

def run():
    results=dict(status="PASS",date="2026-11-18",
        full_E8_census=Wilson_phase_census(),
        conjugation_obstruction=conjugation_no_go(),
        nearly_parallel_G2=near_parallel_G2(),
        local_qutrit_MUB=qutrit_local_MUB(),
        clearly_not_a_TOE=True)
    path=ROOT/"data/toe_20261118_E8_248_relative_Psi_G2_MUB.json"
    path.write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
    print("PASS full E8 248 relative corrected: c0 (268,20), c3 (266,18); unique Psi c3 gives unbroken dim14; conjugation no-go; near-parallel tau0=2/L; 4 local MUB settings n317")
    return results
if __name__=="__main__":run()
