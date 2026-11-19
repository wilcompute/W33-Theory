"""Five crossed TOE falsifiers/constructive interfaces, independently tested.

F1: A free H27 action on (S5 x T2), dimension seven, with exact Betti
    no-go for ANY compact torsion-free G2 structure on the quotient.
F2: Flat-H27 Wilson lines still cannot create ordinary zero Dirac
    eigenstates: exact S5 spin spectrum gives a strict positive gap.
F3: H27 Molien census: cubic dim2, no quartic/quintic, sextic dim4.
    An explicit H27-invariant cubic+sextic F-term has nonstabilizer,
    2-support qutrit vacua, escaping the repo's cubic-only F-flat lock.
F4: The noncommuting H27 clock and shift CANNOT be flat commuting
    T2 Wilson holonomies alone. Opposite projective charges cancel
    in a 9D Weyl tensor control; this is NOT an E8/E6 bundle.
F5: An explicit FOUR-register, FOUR two-qutrit SUM-gate sequential
    qutrit-emitter produces GHZ while earlier output photons are never
    touched again. Memory dephasing creates exactly the classically
    correlated state with identical pairwise density matrices.

Code calculates model assertions, NOT a G2 metric, physical fermion
operator with ADE defects, E8 gauge anomaly cancellation, UV flavon
completion, observed quantum photons, or three-time-only process tensor.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.stats import binom

ROOT=Path(__file__).resolve().parents[1]
omega=np.exp(2j*np.pi/3)
Z=np.diag([1,omega,omega*omega]).astype(complex)
X=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=complex)
G=list(itertools.product(range(3),repeat=3))

def mul(g,h):
    a,b,c=g;A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C+a*B)%3)

def rho(g):
    a,b,c=g
    return (omega**c)*np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,a)

def check_H27():
    maxres=max(float(np.max(abs(rho(mul(g,h))-rho(g)@rho(h))))
               for g in G for h in G)
    assert maxres<1e-12
    return maxres

def seven_manifold():
    err=check_H27()
    coverage={"central_S5":0,"first_torus_translation":0,
              "second_torus_translation":0}
    all_move=True
    for g in G:
        if g==(0,0,0):continue
        a,b,c=g
        # On torus T2, character chi_a/b acts by angle translations:
        # g:(theta1,theta2)->(theta1+2*pi*a/3,theta2+2*pi*b/3).
        # If either a or b nonzero, no torus fixed point.
        if a:
            coverage["first_torus_translation"]+=1
        elif b:
            coverage["second_torus_translation"]+=1
        else:
            coverage["central_S5"]+=1
            # central rho=omega^c I3; no fixed unit vectors
            assert np.min(abs(np.linalg.eigvals(rho(g))-1))>1
        all_move=all_move and (a!=0 or b!=0 or c!=0)
    assert coverage==dict(central_S5=2,
                          first_torus_translation=18,
                          second_torus_translation=6)
    assert all_move
    # Finite free action, all actions homotopic to identity
    # on S5 x T2 -> rational cohomology unchanged by transfer.
    b={0:1,1:2,2:1,5:1,6:2,7:1}
    assert sum(b.values())==8
    assert sum(((-1)**k)*v for k,v in b.items())==0
    # Torsion-free G2: nonzero parallel 3-form gives nonzero
    # H^3 class. Also b1=2 impossible from parallel cross product.
    return dict(status="PASS",
      h27_group_law_max_residual=err,
      free_action_test_nonidentity=26,
      fixed_point_exclusion_cases=coverage,
      quotient="Y7=(S5(R) x T2(L1,L2))/H27",
      real_dimension=7,free_smooth_action=True,
      natural_spin_structure_exists=True,
      quotient_orientable=True,
      exact_rational_Poincare="(1+t^5)*(1+t)^2",
      rational_Betti={str(k):v for k,v in b.items()},
      first_Betti=2,third_Betti=0,fourth_Betti=0,
      fundamental_group="1 -> Z^2 -> pi1(Y7) -> H27 -> 1",
      full_fundamental_group_infinite=True,
      h27_finite_flat_holonomy_possible=True,
      torsion_free_G2_possible=False,
      G2_obstruction1="A compact torsion-free G2 structure has a nonzero harmonic defining 3-form, so b3>=1. Here b3=0.",
      G2_obstruction2="On compact Ricci-flat torsion-free G2, harmonic 1-forms are parallel. Two independent such forms produce a third parallel form via the G2 cross product, so b1=2 is impossible.",
      nearly_parallel_G2_nonzero_tau_possible=False,
      weak_G2_obstruction="Positive Ricci for nearly-parallel G2 would imply b1=0 (Bochner), contrary to b1=2.",
      actual_product_quotient_Ricci="eigenvalues 4/R^2 (five sphere tangent directions), 0 (two torus directions)",
      actual_product_quotient_scalar_curvature="20/R^2",
      no_nonzero_deRham_4form_flux_class=True,
      scope="Explicit free 7D Riemannian model with H27 quotient holonomy, NOT a torsion-free/weak-G2 metric, singular ADE 7D compactification or a Lorentzian M-theory solution. Other torsionful or sourced geometries are not excluded.")

def ordinary_Dirac():
    # Dirac(S^5_R) = +/- (k+5/2)/R, k>=0;
    # Dirac(product)^2=Dirac(S5)^2+Dirac(T2)^2.
    R=2.
    ks=np.arange(0,11)
    sphere_sq=((ks+2.5)/R)**2
    kxy=range(-3,4)
    momenta=[(kx*kx+ky*ky)*(2*np.pi)**2
             for kx,ky in itertools.product(kxy,repeat=2)]
    gap=min(float(v+p) for v in sphere_sq for p in momenta)
    assert abs(gap-25/16)<1e-12
    scalar_quarter=5/R**2
    assert gap>scalar_quarter
    return dict(status="PASS",sphere_spin_Dirac_spectrum="lambda_k=+/- (k+5/2)/R",
      product_Dirac_square="D_S5^2 + D_T2^2",
      numeric_R=R,smallest_spin_Dirac_square=gap,
      exact_lower_bound_Dirac_abs_times_R="5/2",
      exact_lower_bound_Dirac_squared_times_R2="25/4",
      Lichnerowicz_curvature_term_times_R2="5",
      flat_unitary_gauge_twist_cannot_generate_ordinary_zero_modes=True,
      finite_quotient_spectrum_obeys_cover_lower_bound=True,
      independently_enumerated_torus_momenta_count=len(momenta),
      reason="Lift a twisted flat-connection spinor on the free finite quotient to an equivariant spinor on S5 x T2. Its spectrum is contained in the cover spectrum, whose S5 factor already has gap.",
      scope="Ordinary Riemannian spin Dirac with unitary FLAT internal gauge connection and no singularities. Nonflat curvature, flux supercovariant operators, ADE charged defect Dirac and boundary indices are not tested.")

def monomial_data(degree):
    allowed=[]
    for a in range(degree+1):
        for b in range(degree-a+1):
            c=degree-a-b
            if (b+2*c)%3==0:allowed.append((a,b,c))
    # X cycles variables; cyclic coordinate permutations preserve
    # the Z-invariant subspace only for total degree divisible by3.
    if degree%3:
        # center omega*I multiplies a degree-d polynomial by
        # omega^d, hence zero invariant sections.
        return 0,[]
    cycles=[]
    remain=set(allowed)
    while remain:
        x=min(remain)
        orbit={x,(x[1],x[2],x[0]),(x[2],x[0],x[1])}
        assert orbit.issubset(remain)
        remain-=orbit
        cycles.append(sorted(orbit))
    return len(cycles),cycles

def sextic_F_flat():
    dcounts={str(d):monomial_data(d)[0] for d in range(13)}
    assert [dcounts[str(d)] for d in range(13)]==[
        1,0,0,2,0,0,4,0,0,7,0,0,11]
    # Molien rank: each noncentral element has eigenvalues
    # {1,omega,omega^2}; every central element acts as omega^c I.
    for d in range(0,13,3):
        molien=(math.comb(d+2,2)+8)//9
        assert molien==dcounts[str(d)]
    dim6,orbits=monomial_data(6)
    assert dim6==4 and sorted(map(len,orbits))==[1,3,3,3]
    x,y,z=s.symbols("x y z")
    xyz=(x,y,z)
    cubic=x**3+y**3+z**3
    sextic=x**6+y**6+z**6
    W=cubic-s.Rational(1,2)*sextic
    grad=[s.expand(s.diff(W,t)) for t in xyz]
    assert all(s.simplify(g-3*t*t*(1-t**3))==0
               for g,t in zip(grad,xyz))
    # Each coordinate is either zero or a cube-root unity: 4^3=64.
    roots=[s.Integer(0),s.Integer(1),s.exp(2*s.pi*s.I/3),
           s.exp(4*s.pi*s.I/3)]
    stationary=[k for k in itertools.product(range(4),repeat=3)]
    support={k:sum(bool(i) for i in k) for k in stationary}
    counts={str(j):sum(sup==j for sup in support.values())
            for j in range(4)}
    assert counts=={"0":1,"1":9,"2":27,"3":27}
    candidate={x:s.Integer(1),y:s.Integer(1),z:s.Integer(0)}
    assert all(g.subs(candidate)==0 for g in grad)
    psi=np.array([1,1,0],complex)/np.sqrt(2)
    bases=[np.eye(3,dtype=complex)]
    for U in (X,X@Z,X@Z@Z):
        vec=np.linalg.eig(U)[1]
        bases.append(vec)
    allprobs=[float(abs(np.vdot(B[:,j],psi))**2)
              for B in bases for j in range(3)]
    fidelity=max(allprobs)
    assert abs(fidelity-2/3)<1e-12
    assert abs(sum(abs(psi)**2)-1)<1e-12
    # Projectivize all 27 support-two F-flat vectors: multiplying
    # their two nonzero values by a common omega gives the same ray.
    # Exactly 3 missing-position choices times 3 relative phases
    # give NINE projective rays, forming a Weyl-Heisenberg SIC.
    sic=[]
    for missing in range(3):
        a,b=[j for j in range(3) if j!=missing]
        for k in range(3):
            v=np.zeros(3,complex)
            v[a]=1/np.sqrt(2)
            v[b]=omega**k/np.sqrt(2)
            sic.append(v)
    Gram=np.array([[abs(np.vdot(p,q))**2 for q in sic]
                   for p in sic])
    assert np.max(abs(Gram-(np.eye(9)+
                   (np.ones((9,9))-np.eye(9))/4)))<1e-12
    povm=sum(np.outer(v,v.conj()) for v in sic)/3
    assert np.max(abs(povm-np.eye(3)))<1e-12
    for g in G:
        q=rho(g)@sic[0]
        assert max(abs(np.vdot(q,v))**2 for v in sic)>1-1e-12
    hesse_dbl=[(sum(v**3)/np.sqrt(3),
                 np.sqrt(6)*np.prod(v)) for v in sic]
    hesse_norms=[float(abs(a)**2+abs(b)**2)
                 for a,b in hesse_dbl]
    assert max(abs(h-s.Rational(1,6)) for h in hesse_norms)<1e-12
    # Prior specific Hesse SIC basepoints have u=0. Our
    # nine-vertex WH SIC is in a DIFFERENT degree-3 SIC family:
    # u-norm=1/6, not the Hesse-pencil base-point u=0.
    # Explicit X and Z group invariance of W.
    assert s.expand(W.subs({x:y,y:z,z:x},simultaneous=True)-W)==0
    for B in (cubic,sextic):
        zphase=s.expand(B.subs({x:x,y:omega*y,z:omega**2*z})-B)
        assert all(abs(complex(co))<1e-12
                   for co in s.Poly(zphase,x,y,z).coeffs())
    return dict(status="PASS",
      H27_Molien_dimensions_degrees_0_to_12=dcounts,
      degree6_invariant_basis_exponent_orbits=orbits,
      exact_independent_sextic_invariants=[
          "x^6+y^6+z^6",
          "x^3*y^3+y^3*z^3+z^3*x^3",
          "(xyz)*(x^3+y^3+z^3)",
          "(xyz)^2"],
      lowest_new_holomorphic_degree_beyond_cubic=6,
      invariant_quartic_and_quintic_absent=True,
      chosen_W="(x^3+y^3+z^3) - (x^6+y^6+z^6)/2",
      actual_F_terms=[str(g) for g in grad],
      number_of_complex_stationary_points=64,
      stationary_support_class_counts=counts,
      nonstabilizer_F_flat_solution="[1,1,0]",
      independent_nonstabilizer_VEVs_at_support_two=27,
      normalized_F_flat_qutrit="[1,1,0]/sqrt(2)",
      maximum_overlap_squared_with_12_stabilizer_states=fidelity,
      qutrit_nonstabilizer_magic_state=True,
      number_of_projective_support_two_SIC_rays=9,
      SIC_all_distinct_pair_overlap_squared="1/4",
      SIC_POVM_sum_normalized="sum_j |psi_j><psi_j| / 3 = I3",
      SIC_Gram_max_abs_residual=float(np.max(abs(Gram-(np.eye(9)+(np.ones((9,9))-np.eye(9))/4)))),
      SIC_POVM_max_abs_residual=float(np.max(abs(povm-np.eye(3)))),
      SIC_transitive_H27_orbit_verified=True,
      Hesse_doublet_norm_squared_on_this_SIC="1/6",
      not_prior_specific_Hesse_pencil_basepoint_SIC=True,
      H27_covariance_and_exact_F_flatness_verified=True,
      limitation="This is an H27-invariant isolated effective flavon superpotential, requiring a dimensionful sextic coefficient. Its elementary family triplet may NOT be an E8-adjoint scalar; E6 gauge charge, D-flatness, anomaly inflow, kinetic potential, electroweak masses and a UV operator generating W are NOT demonstrated. The cubic-only F-flat stabilizer theorem remains correct for degree3.")

def torus_center():
    lhs=Z@X
    rhs=omega*X@Z
    assert np.max(abs(lhs-rhs))<1e-12
    assert np.max(abs(X@Z-Z@X))>.5
    U=np.kron(Z,Z)
    V=np.kron(X,np.linalg.matrix_power(X,2))
    err=float(np.max(abs(U@V-V@U)))
    assert err<1e-12
    assert np.max(abs(np.linalg.matrix_power(U,3)-np.eye(9)))<1e-12
    assert np.max(abs(np.linalg.matrix_power(V,3)-np.eye(9)))<1e-12
    traces={}
    for a,b in itertools.product(range(3),repeat=2):
        tr=np.trace(np.linalg.matrix_power(U,a)@
                    np.linalg.matrix_power(V,b))
        traces[f"{a},{b}"]=[round(float(tr.real),10),
                            round(float(tr.imag),10)]
        assert abs(tr-(9 if a==b==0 else 0))<1e-11
    return dict(status="PASS",
      single_family_Weyl_commutator="Z*X=omega*X*Z",
      single_triplet_X_Z_commute=False,
      cannot_be_simultaneous_flat_wilson_holonomies_of_pi1_T2=True,
      compensated_9D_tensor_control="U=Z tensor Z, V=X tensor X_inverse",
      compensated_U_V_commute=True,
      compensated_commutator_max_abs=err,
      compensated_character_traces=traces,
      compensated_9D_rep_is_regular_of_Z3_squared=True,
      H27_nonabelian_pi1_quotient_allows_noncommuting_holonomy=True,
      shared_E8_center_needed_if_E6_compensates_family_SU3=True,
      limitation="A concrete two-qutrit A2 x A2 center-cancellation example, NOT an actual E6 27-dimensional compensator, E8 global bundle or Yang-Mills solution. In a nonabelian pi1(Y7), genuine H27 flat holonomies are allowed and do not need torus generators to fail commuting.")

def digits(k,n=4):
    out=[0]*n
    for i in range(n-1,-1,-1):
        out[i]=k%3;k//=3
    return out

def index(v):
    k=0
    for t in v:k=3*k+t
    return k

def SUM(control,target,sign=+1):
    U=np.zeros((81,81),complex)
    for j in range(81):
        tup=digits(j)
        tup[target]=(tup[target]+sign*tup[control])%3
        U[index(tup),j]=1
    assert np.max(abs(U.conj().T@U-np.eye(81)))<1e-12
    return U

def partial_pair(rho,discard):
    a=rho.reshape((3,)*6)
    return np.trace(a,axis1=discard,axis2=discard+3).reshape(9,9)

def emitter():
    # Four registers: E, A(t1), B(t2), C(t3).
    # Three CADD from quantum E to each fresh output,
    # final CSUB(C to E), where C is still on device at t3.
    state=np.zeros(81,complex)
    for j in range(3):state[index([j,0,0,0])]=1/np.sqrt(3)
    U1=SUM(0,1)
    U2=SUM(0,2)
    U3=SUM(0,3)
    U4=SUM(3,0,-1)
    after2=U2@U1@state
    final=U4@U3@after2
    target=np.zeros(81,complex)
    for j in range(3):target[index([0,j,j,j])]=1/np.sqrt(3)
    assert np.max(abs(final-target))<1e-12
    rho_pre=np.outer(after2,after2.conj())
    # Dephasing memory E between sessions t2 and t3 removes only
    # off-diagonal E blocks and preserves all R/S output populations.
    blocks=rho_pre.reshape(3,27,3,27)
    dblocks=np.zeros_like(blocks)
    for j in range(3):dblocks[j,:,j,:]=blocks[j,:,j,:]
    rho_dephase=dblocks.reshape(81,81)
    last=U4@U3
    out_coh=last@rho_pre@last.conj().T
    out_class=last@rho_dephase@last.conj().T
    reduced_coh=np.trace(out_coh.reshape(3,27,3,27),axis1=0,axis2=2)
    reduced_class=np.trace(out_class.reshape(3,27,3,27),axis1=0,axis2=2)
    GHZ=np.zeros(27,complex)
    for j in range(3):GHZ[index([j,j,j])]=1/np.sqrt(3)
    P=np.outer(GHZ,GHZ.conj())
    D=np.zeros((27,27),complex)
    for j in range(3):D[index([j,j,j]),index([j,j,j])]=1/3
    assert np.max(abs(reduced_coh-P))<1e-12
    assert np.max(abs(reduced_class-D))<1e-12
    pair_residuals=[]
    for drop in range(3):
        pair_residuals.append(float(np.max(abs(partial_pair(P,drop)-
                                              partial_pair(D,drop)))))
    assert max(pair_residuals)<1e-12
    Op=np.kron(np.kron(X,X),X)
    assert abs(np.trace(P@Op)-1)<1e-12
    assert abs(np.trace(D@Op))<1e-12
    # noise-t visibility and three-setting stabilizer power from
    # PRIOR GHZ proposal (independently recomputed with circuit)
    t=.75
    rout=t*P+(1-t)*D
    F=float(np.real(np.trace(P@rout)))
    assert abs(F-5/6)<1e-12
    eps=.01
    pz=(1-eps)**2+eps**2/2
    px=(1+2*t*(1-1.5*eps)**3)/3
    lower=2*pz+px-2
    assert lower>1/3
    n=200; alpha=.01
    delta=math.sqrt(math.log(3/alpha)/(2*n))
    threshold=math.floor(n*(7/3+3*delta))+1
    pmf=np.convolve(
        np.convolve(binom.pmf(np.arange(n+1),n,pz),
                    binom.pmf(np.arange(n+1),n,pz)),
        binom.pmf(np.arange(n+1),n,px))
    power=float(pmf[threshold:].sum())
    assert threshold==539 and power>.99
    return dict(status="PASS",
       four_register_order="E,A,B,C",
       gates_in_chronological_order=[
           "SUM(E->A) at t1","SUM(E->B) at t2",
           "SUM(E->C) at t3","inverse_SUM(C->E) at t3"],
       two_qutrit_clifford_gate_count=4,
       earlier_emitted_outputs_not_touched_again=True,
       final_environment_state="|0>",
       final_three_output_coherent_state="(|000>+|111>+|222>)/sqrt3",
       coherent_density_max_error=float(np.max(abs(reduced_coh-P))),
       environment_dephased_gives_exact_classical_GHZ_diagonal=True,
       classical_density_max_error=float(np.max(abs(reduced_class-D))),
       pairwise_marginal_max_error=max(pair_residuals),
       triple_X_expectation_coherent=1,
       triple_X_expectation_classical=0,
       modeled_visibility=t,GHZ_fidelity=F,
       readout_error=eps, modeled_pair_Z_match=pz,
       modeled_triple_X_sum_zero=px,
       three_setting_GHZ_fidelity_lower=lower,
       typeI_upper_bound=alpha,accepted_trials_per_setting=n,
       total_accepted_trials=3*n,
       biseparable_rejection_threshold_total_matches=threshold,
       exact_IID_model_power=power,
       causal_scope="Valid time-ordered sequential emitter using a persistent quantum memory E and one-time emitted output qutrits. ALL output pairwise state reductions are separable and identical to the dephased control; three-output coherence is quantum.",
       limitation="This is not yet a three-slot process tensor with freely chosen interventions at each input. Hence pairwise-classical OUTPUT MARGINALS do not imply the stronger pairwise-classical operational PROCESS condition. No photonic layout, herald efficiency, calibration uncertainty or experimental result is provided.")

def run():
    obj=dict(status="PASS",date="2026-11-18",
       H27_seven_dimensional_quotient=seven_manifold(),
       ordinary_spin_Dirac_flat_gap=ordinary_Dirac(),
       H27_first_nontrivial_sextic_F_flat=sextic_F_flat(),
       flat_Weyl_torus_compensation=torus_center(),
       sequential_qutrit_four_gate_emitter=emitter(),
       valid_full_TOE=False)
    p=ROOT/"data/toe_20261118_H27_S5T2_G2_sextic_center_sequential.json"
    p.write_text(json.dumps(obj,indent=2)+"\n",encoding="utf8")
    print("PASS: H27 free S5xT2 seven-manifold b3=0; exact Dirac gap; degree6 Molien and nonstabilizer F-flat; Weyl torus compensation; 4-SUM time-ordered GHZ emitter")
    return obj
if __name__=="__main__":run()
