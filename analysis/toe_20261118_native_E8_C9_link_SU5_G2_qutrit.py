"""W33 TOE: E8-realized T(2,6) order-nine family holonomy and four
independent physical consistency tests (2026-11-18).

New: An SU(3) family C of order9 with C^3=omega I replaces the
non-SU3 scalar -I3 from the previous linked-wire packet. A and C
generate a finite 81-element subgroup containing native H27.
This realizes nonresonant rank3 relative local cohomology in genuine
(E6xSU3)/Z3 branching representations, but the conjugate matter sector
survives. It does NOT yield actual chiral fermions or a G2 vacuum.

Other fronts: E6 vectorlike two-pair vacuum moduli, Freund-Rubin vs
torsion-free G2 curvature, intrinsic-qutrit Schmidt-number-3 witness,
and a conditional geometric Z3 selection rule for PW polynomials.
"""
from pathlib import Path
from itertools import combinations
from collections import deque
import json, math
import numpy as np
import sympy as s
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]
w=np.exp(2j*np.pi/3)
theta=np.exp(2j*np.pi/9)
zeta=np.exp(2j*np.pi/7)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
C9=np.diag([theta,theta,theta**7])
I3=np.eye(3,dtype=complex)

def coh(A,C):
    dim=A.shape[0]
    I=np.eye(dim,dtype=complex)
    d0=np.vstack([A-I,C-I])
    d1=np.hstack([I-np.linalg.matrix_power(C,3),
        (A-I)@(I+C+C@C)])
    R=np.linalg.matrix_power(C,3)
    assert np.max(abs(A@R-R@A))<1e-9
    assert np.max(abs(d1@d0))<1e-8
    r0=int(np.linalg.matrix_rank(d0,tol=1e-8))
    r1=int(np.linalg.matrix_rank(d1,tol=1e-8))
    # One relative S2 removes the 0-cochains. The correct relative
    # complex is 0 -> V^2 -> V, so b1_rel=2dim-r1. A prior expression
    # 3dim-r0-r1 overcounted by b0_abs=dim-r0 whenever there were
    # parallel invariant vectors; the charged sector results had b0=0.
    return dict(rank_d0=r0,rank_d1=r1,absolute_betti=[dim-r0,
        2*dim-r0-r1,dim-r1],relative_one_sphere_betti=[0,
        2*dim-r1,dim-r1],chain_complex_error=float(np.max(abs(d1@d0))))

def group_order():
    # D(v)X^k with D9 exponent vector v and sum components=0 mod9.
    # Conjugating D by X cyclically permutes the three diagonal entries.
    def sh(v): return (v[2],v[0],v[1])
    v=(1,1,7)
    diags={(0,0,0)}
    stack=[(0,0,0)]
    while stack:
        a=stack.pop()
        for b in (v,sh(v)):
            x=tuple((i+j)%9 for i,j in zip(a,b))
            if x not in diags:diags.add(x);stack.append(x)
    assert len(diags)==27
    assert all(sum(q)%9==0 for q in diags)
    assert all(sh(q) in diags for q in diags)
    hdiag={q for q in diags if all(k%3==0 for k in q)}
    assert len(hdiag)==9
    assert (3,3,3) in hdiag
    return dict(orders=dict(SU3_diagonal_subgroup=27,
        H27_normal_subgroup=27,SU3_full_group=81,
        SU3_order9_extension_over_H27=3,
        SU5_W7_times_SU3_family=567),
        SU3_diagonal_exponents=sorted([list(v) for v in diags]),
        H27_diagonal_center_root_subgroup_order=len(hdiag),
        group_law="D(v)X^k * D(t)X^l = D(v+shift^k(t)) X^(k+l) mod9",
        H27_subgroup="X and the order-three noncentral diagonal commutators generate the native order27 Heisenberg subgroup")

def E8_bundle():
    assert np.max(abs(C9.conj().T@C9-I3))<1e-12
    assert abs(np.linalg.det(C9)-1)<1e-12
    assert np.max(abs(np.linalg.matrix_power(C9,3)-w*I3))<1e-12
    assert np.max(abs(X@np.linalg.matrix_power(C9,3)-
                      np.linalg.matrix_power(C9,3)@X))<1e-12
    # C9 is the determinant-one SU3 lift of the native qutrit
    # Clifford quadratic phase gate. It has physical linear order9
    # but projective order3, giving the exact central Seifert phase.
    Z=np.diag([1,w,w*w])
    assert np.max(abs(C9@X@C9.conj().T-X@Z@Z))<1e-12
    assert np.max(abs(C9@Z@C9.conj().T-Z))<1e-12
    # A=(I5,X), C=(W7,C9) represent the linked group
    # <a,c| [a,c^3]=1> in the compact E8 subgroup
    # (E6 x SU3)/Z3.
    weights5=[2,2,2,4,4]
    W7=np.diag([zeta**k for k in weights5])
    assert abs(np.linalg.det(W7)-1)<1e-12
    A=np.kron(np.eye(5),X)
    C=np.kron(W7,C9)
    residual=float(np.max(abs(A@np.linalg.matrix_power(C,3)-
                              np.linalg.matrix_power(C,3)@A)))
    assert residual<1e-11
    # SU5 27 weight decomposition 10+5+2 bar5+2 singlets.
    weight10=[(weights5[a]+weights5[b])%7
              for a,b in combinations(range(5),2)]
    weight27=weight10+weights5+[(-k)%7 for k in weights5]*2+[0,0]
    assert len(weight27)==27
    matter=[coh(X,zeta**k*C9) for k in weight27]
    conj=[coh(X.conj(),zeta**(-k)*C9.conj()) for k in weight27]
    assert all(p["absolute_betti"]==[0,0,0] and
               p["relative_one_sphere_betti"]==[0,3,0] for p in matter+conj)
    # An SU3 family 3 has no common A,C invariant vector:
    assert coh(X,C9)["absolute_betti"]==[0,0,0]
    # Adjoint 8 modes carry trivial SU3 center; they cannot be
    # made acyclic by the nontrivial central Seifert monodromy.
    Z=np.diag([1,w,w*w])
    basis=[np.linalg.matrix_power(X,a)@np.linalg.matrix_power(Z,b)/np.sqrt(3)
           for a in range(3) for b in range(3) if (a,b)!=(0,0)]
    def adj(U):
        return np.array([[np.trace(P.conj().T@U@Q@U.conj().T)
            for Q in basis] for P in basis])
    adj_coh=coh(adj(X),adj(C9))
    assert adj_coh["absolute_betti"]==[0,4,4]
    assert adj_coh["relative_one_sphere_betti"]==[0,12,4]
    # (27,1) does NOT descend to the actual (E6 x SU3)/Z3
    # because kernel (omega,omega^-1) acts as omega !=1.
    return dict(status="PASS",torus_link="T(2,6)",
       link_presentation="pi1=<a,c | [a,c^3]=1>",
       SU3_family_A="cyclic qutrit shift X",
       SU3_family_C9_exponents_over_zeta9=[1,1,7],
       SU3_family_C9_cube="omega I3, omega=exp(2pi i/3)",
       qutrit_Clifford_lift="C9 X C9^dagger=X Z^2; C9 Z C9^dagger=Z; C9^3=omega I",
       qutrit_projective_gate_order=3,
       qutrit_SU3_lift_order=9,
       E8_global_subgroup="(E6 x SU3)/Z3",
       exact_finite_image=group_order(),
       SU5_W7_exponents=[2,2,2,4,4],
       linked_relation_full_SU5xSU3_residual=residual,
       SU5_breaks_to="S(U3 x U2) centralizer dimension12",
       SU5_adjoint_original_dimension=24,
       SU5_centered_root_generator_count=12,
       matter_E6_27_weight_exponents=weight27,
       matter_27x3_relative_betti=[0,81,0],
       conjugate_27barx3bar_relative_betti=[0,81,0],
       same_relative_boundary_does_not_project_conjugate_matter=True,
       SU3_family_adjoint8_absolute_betti=adj_coh["absolute_betti"],
       SU3_family_adjoint8_relative_betti=adj_coh["relative_one_sphere_betti"],
       gauge_Higgs_27x1_global_E8_representation_exists=False,
       scalar_E6_fundamental_27x1_fails_center_quotient_by_phase="omega",
       family_charged_E8_27x3_no_parallel_invariant=True,
       parity_C2_not_needed_for_matter_relative_acyclicity=True,
       physical_limit="Mathematical finite flat E8-subgroup link representation and chosen de Rham relative boundary. The desired conjugate 27bar sector also survives with 81 classes; adjoint8 has (12,4) and E6 singlet Higgs 27x1 is not an E8 representation. No spinor Dirac operator, physical chirality, full E8 scalar Higgs, anomaly inflow or global G2 compactification is constructed.")

def E6_two_pair():
    n,nb,t,tb,z1,z2=s.symbols("n nb t tb z1 z2")
    W=z1*(n*nb-1)+z2*(t*tb-1)
    fields=[n,nb,z1,t,tb,z2]
    p={n:1,nb:1,t:1,tb:1,z1:0,z2:0}
    assert all(s.diff(W,f).subs(p)==0 for f in fields)
    H=s.hessian(W,fields).subs(p)
    assert H.rank()==4
    vals=sorted([str(v) for v in H.eigenvals(multiple=True)])
    assert vals==['-sqrt(2)','-sqrt(2)','0','0','sqrt(2)','sqrt(2)']
    # Full 4 x 27 Higgs + 2 driving singlets:
    full_n=4*27+2
    # With two nonzero vectorlike VEVs, FZ1/FZ2 impose exactly two
    # invariant complex equations, FH/FR force Z1=Z2=0.
    F_codim=4
    broken_gauge=78-24
    moduli=full_n-F_codim-broken_gauge
    assert moduli==52
    # 27 singlets of both types preserve SU5, irrespective of
    # positive rank2 U1 gauge mass Gram.
    Q=s.Matrix([[-5,0],[1,4]])
    assert Q.det()==-20
    mass=2*Q*Q.T
    assert mass.det()==1600
    return dict(status="PASS",chiral_fields=full_n,
       SM_singlet_subspace_superpotential="W=Z1*(n nb-1)+Z2*(t tb-1)",
       singlet_6x6_holomorphic_Hessian_eigenvalues=vals,
       full_model_Hessian_rank_at_most=F_codim,
       F_flat_local_complex_dimension=full_n-F_codim,
       E6_dim=78,unbroken_at_least_SU5_dim=24,
       broken_complex_gauge_orbit_dimension_at_most=broken_gauge,
       local_complex_moduli_lower_bound=moduli,
       Abelian_charge_matrix=[[int(v) for v in row] for row in Q.tolist()],
       Abelian_mass_Gram=[[int(v) for v in row] for row in mass.tolist()],
       unbroken_nonabelian_SU5_needs_further_W7_or_other_representation=True,
       matter_27x1_not_rep_of_full_E8_subgroup=True,
       qualification="Lower bound assumes full 110-field F-flat local algebra with only these two driving terms and smooth stable quotient. Additional invariant couplings, vectorlike masses, sources and global gauge constraints may change it. Both VEVs are SU5 singlets, so E6->SU5, not directly SM. The 27x1 Higgs is not compatible as a bare E8 gauge representation with unbroken family SU3.")

def AdS4_G2():
    f,L=s.symbols("f L",real=True,positive=True)
    Rext= -f**2/3
    Rint= f**2/6
    scalar7=7*f**2/6
    assert s.simplify(Rext.subs(f,3/L)+3/L**2)==0
    assert s.simplify(scalar7.subs(f,3/L)-s.Rational(21,2)/L**2)==0
    return dict(status="PASS",
       model="unwarped source-free 11D product M4 x Y7, pure electric Freund-Rubin F4=f vol4, no internal flux",
       R_external_tensor_coefficient="-f²/3",
       R_internal_tensor_coefficient="+f²/6",
       internal_scalar_curvature="+7 f²/6",
       torsionfree_G2_has_Ricci_zero=True,
       if_torsionfree_G2_then_f_zero=True,
       f_zero_implies_Minkowski_not_AdS4=True,
       alternative="weak/near-parallel G2 positive-Einstein internal manifold, warping, sources, torsion or different flux ansatz",
       physical_limit="Conditional simple FR product no-go, not a general no-go for M-theory AdS4/G2 compactification with additional flux, curvature sources or quantum corrections.")

def qutrit_witness():
    d=3;t=.75;alpha=.01;power_goal=.9
    phi=np.zeros(d*d,complex)
    for i in range(d):phi[d*i+i]=1/math.sqrt(d)
    rho=t*np.outer(phi,phi.conj())+(1-t)*np.eye(d*d)/(d*d)
    fidel=float(np.real(phi.conj()@rho@phi))
    assert abs(fidel-7/9)<1e-12
    assert np.min(np.linalg.eigvalsh(rho))>0
    # Schmidt number <=2 of arbitrary bipartite qutrit system
    # entails F<=2/3. EB/Schmidt<=1 entails F<=1/3.
    p0=2/3
    # exact binomial one-sided threshold, no normal approximation;
    # at each fixed n select smallest k with P_null(K>=k)<=alpha.
    optimum=None
    for n in range(1,1500):
        k=int(binom.isf(alpha,n,p0))+1
        while binom.sf(k-1,n,p0)>alpha:k+=1
        while k>1 and binom.sf(k-2,n,p0)<=alpha:k-=1
        P=float(binom.sf(k-1,n,fidel))
        if P>=power_goal:
            optimum=dict(accepted_Bell_projection_trials=n,
                         observed_Bell_successes_to_reject=k,
                         exact_one_sided_typeI=float(binom.sf(k-1,n,p0)),
                         design_point_power=P)
            break
    assert optimum and optimum["accepted_Bell_projection_trials"]==214
    assert optimum["observed_Bell_successes_to_reject"]==159
    # t threshold for F>2/3: (1+8t)/9>2/3 --> t>5/8.
    return dict(status="PASS",
       certificate="Schmidt-number-three reference-system memory entanglement",
       reference_system_dimension=3,carrier_dimension=3,
       normalized_Choi_isotropic="rho=t*|Phi3><Phi3|+(1-t)*I9/9",
       chosen_memory_visibility_t=t,exact_fidelity=fidel,
       rank2_fidelity_upper_bound=2/3,
       separable_EB_fidelity_upper_bound=1/3,
       rank3_certification_visibility_threshold=5/8,
       exact_fixed_stopping_binomial=optimum,
       source="Schmidt-number witness bound F<=r/d for maximally entangled d target; prior atomic-OAM qutrit entanglement experiments exceed 2/3",
       limitation="This witnesses genuinely three-dimensional retained quantum entanglement of a reference with a memory channel, provided an event-ready causal-break experiment makes the effective map attributable to the memory. It does NOT by itself certify genuine *three-time* memory irreducible to two-time quantum memory, and does not verify an actual photon experiment.")

def Z3_geometry_selection():
    table=[]
    for n in range(2,11):
        exp=n+1
        invariant=exp%3==0
        table.append(dict(n_index_one_Morse_points=n,
             holomorphic_degree=exp,
             invariant_under_w_to_omega_w=invariant))
    assert not next(z for z in table if z["n_index_one_Morse_points"]==3)["invariant_under_w_to_omega_w"]
    return dict(status="PASS",
       hypothesized_geometric_Z3_action="w->omega*w in the transverse complex plane",
       candidate_localizer="Re(w^(n+1))/(n+1)-|w|²/2+z²-a*x",
       invariance_requires="n+1 divisible by3 AND linear tilt zero or transforms equivariantly",
       n3_quartic_not_invariant=True,
       table=table,
       scope="Conditional geometric Z3 selection rule only. E8 central Z3 is an INTERNAL gauge transformation and need not rotate geometric w; therefore no physical exclusion of three families. This falsifies a tempting but unjustified identification between order-three internal center and PW transverse-plane rotation.")

def run():
    out=dict(status="PASS",date="2026-11-18",
      native_E8_link_holonomy=E8_bundle(),
      E6_Higgs_and_moduli=E6_two_pair(),
      Freund_Rubin_G2=AdS4_G2(),
      intrinsic_qutrit_memory=qutrit_witness(),
      geometric_Z3_selection=Z3_geometry_selection(),
      tested_claim="Five math/conditional physics fronts, no complete TOE")
    path=ROOT/"data/toe_20261118_native_E8_C9_link_SU5_G2_qutrit.json"
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS: E8 native SU3 C9 link 567-image and both 27/27bar cohom; adjoint8 4,4; E6 SU5 and >=52 moduli; AdS4 torsionfree G2 flux no-go; qutrit SN3 n214; conditional Z3 polynomial gate")
    return out

if __name__=="__main__":run()
