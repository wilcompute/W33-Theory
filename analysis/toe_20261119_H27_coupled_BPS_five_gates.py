"""H27 coupled BPS wall: constructive theorem and five independent physical gates.

Conditional canonical-global-SUSY 3-scalar Wess-Zumino toy, not an E8/G2
compactification. See accompanying report for the analytic trapping proof.
"""
import json
from math import sqrt, log, pi, ceil
from pathlib import Path
import itertools
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import solve_ivp, cumulative_trapezoid, trapezoid

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_deformed_H27_coupled_BPS_five_gates.json"
G=.25
R=(5/3)**(1/3)
PHI=(1+sqrt(5))/2

def W(v,g=G):
    S=sum(x**3 for x in v)
    return sum(x**3-x**6/2 for x in v)+g*np.prod(v)*(S-2)

def F(v,g=G):
    S=sum(x**3 for x in v)
    return np.array([3*x*x*(1-x**3)+g*np.prod([v[j] for j in range(3) if j!=i])*(S-2+3*x**3)
                     for i,x in enumerate(v)],float)

def H(v,g=G):
    S=sum(x**3 for x in v)
    out=np.diag([6*x-15*x**4 for x in v])
    for i,x in enumerate(v):
        rest=[v[k] for k in range(3) if k!=i]
        out[i,i]+=12*g*rest[0]*rest[1]*x*x
        for j in range(3):
            if i!=j:
                k=3-i-j
                out[i,j]=g*v[k]*(S-2+3*x**3+3*v[j]**3)
    return out

def coupled_BPS():
    a=np.array([0.,1.,1.]); b=R*np.ones(3)
    assert np.linalg.norm(F(a))<1e-14 and np.linalg.norm(F(b))<1e-13
    ea,U=eigh(H(a));eb=eigh(H(b))[0]
    assert ea[0]<0 and ea[1]<0 and ea[2]>0 and max(eb)<0
    assert np.allclose(eb,[-69*R/4,-69*R/4,-15*R/2],rtol=1e-12)
    # Exact analytical positive-invariant rectangle [0,r] x [1,r].
    # x'=3x²(1-x³)+g q²(4x³+2q³-2)
    # q'=3q²(1-q³)+g x q(x³+5q³-2)
    # Fx_q = 2g q(4x³+5q³-2)>0;
    # Fq_x = g q(4x³+5q³-2)>0.
    # d(Fq/q)/dq = 3-12q³+15g x q² < 3-7.5q³ <0
    # as 1<=q<=r<6/5, 0<=x<=r.
    # For 0<x<=1, Fx>0 throughout; for 1<x<r,
    # Fq(x,x)=Fx(x,x)=x²*(5/2-3x³/2)>0 and its unique
    # Fq=0 root q*(x)>x, so Fx(x,q*)>Fx(x,x)>0.
    # Thus only equilibria a and b on the closed rectangle.
    assert 1<R<1.2 and 15*G*1.2<9
    for x in np.linspace(0,R,41):
        for q in np.linspace(1,R,41):
            dFx_dq=2*G*q*(4*x**3+5*q**3-2)
            dFq_dx=G*q*(4*x**3+5*q**3-2)
            dFq_over_q_dq=3-12*q**3+15*G*x*q*q
            assert dFx_dq>0 and dFq_dx>0 and dFq_over_q_dq<0
    eps=1.e-4
    u=U[:,-1]
    if u[0]<0:u=-u
    assert u[0]>0 and u[1]>0 and u[2]>0
    initial=a+eps*u
    def ode(t,y):
        f=F(y[:3])
        return np.r_[f,2*(f@f)]
    sol=solve_ivp(ode,(0,88),np.r_[initial,0.],rtol=2e-11,
                  atol=1e-12,max_step=.08)
    assert sol.success and np.linalg.norm(sol.y[:3,-1]-b)<1e-10
    assert np.max(abs(sol.y[1]-sol.y[2]))<1e-12
    assert min(sol.y[0])>0 and max(sol.y[0])<=R+1e-12
    assert min(sol.y[1])>=1 and max(sol.y[1])<=R+1e-12
    delta=W(b)-W(a)
    assert abs(delta-13/12)<1e-12
    # Starting eps away from saddle excludes a positive tail of O(eps²).
    assert abs(sol.y[3,-1]-2*delta)<2e-8
    # dF/dz=H(v) F(v), hence F(v(z)) is a normalizable
    # zero mode of D=partial_z-H(v(z)); exact chain-rule identity.
    max_chain=0
    for k in np.linspace(0,len(sol.t)-1,50).astype(int):
        v=sol.y[:3,k]
        J=H(v);fv=F(v)
        dv=1e-5
        num=(F(v+dv*fv)-F(v-dv*fv))/(2*dv)
        max_chain=max(max_chain,float(np.linalg.norm(num-J@fv)))
    assert max_chain<1e-7
    return {"source":[0,1,1],"target":[float(R)]*3,
      "new_wall_proved_in_symmetric_y_equals_z_plane":True,
      "positive_invariant_rectangle":"0<=x<=r, 1<=q<=r, r^3=5/3",
      "unique_stationary_points_in_rectangle":2,
      "proof_ingredients":["inward flow on four faces","strict Fq/q decrease in q",
         "positive Fx on Fq nullcline for 0<x<r",
         "one unstable eigenvector entering rectangle",
         "W strictly increasing unless F=0; compact invariant region and only sink b"],
      "source_Hessian_eigenvalues":ea.tolist(),
      "target_Hessian_eigenvalues":eb.tolist(),
      "source_positive_Hessian_count":int(sum(ea>1e-10)),
      "target_positive_Hessian_count":int(sum(eb>1e-10)),
      "natural_Hessian_Dirac_Fredholm_index":int(sum(ea>1e-10)-sum(eb>1e-10)),
      "source_W":float(W(a)),"target_W":float(W(b)),
      "exact_delta_W":"13/12","exact_BPS_tension":"13/6",
      "numerical_energy_integral":float(sol.y[3,-1]),
      "ending_gradient_norm":float(np.linalg.norm(F(sol.y[:3,-1]))),
      "max_chain_rule_DF_minus_HF_error":max_chain,
      "starting_saddle_displacement":eps,
      "limitations":"Real 3-field global-SUSY gradient sector with canonical Kähler. Actual E8/SU3 gauge-invariant multifield UV, F/D flatness, gauge fields, chiral spectrum and anomaly inflow NOT constructed."},sol

def coupling_interval_theorem():
    # For 0<g<=3/8, r(g)^3=(3-2g)/(3-6g) increases in g
    # (derivative 12/(3-6g)^2 >0), hence g*r(g) <= (3/8)*3^(1/3)
    # < 3/5, certified by cubing: 81/512 < 27/125.
    # So d(Fq/q)/dq <= 3-(12-15gr)q^3 < 3-3q^3 <=0,
    # strictly at q>=1 because gr<3/5.
    assert 81*125<27*512
    gs=[.0625,.125,.25,.35,.375]
    rows=[]
    for g in gs:
        rg=((3-2*g)/(3-6*g))**(1/3)
        a=np.array([0.,1.,1.]);b=np.array([rg]*3)
        ea=np.linalg.eigvalsh(H(a,g));eb=np.linalg.eigvalsh(H(b,g))
        tens=(4*g*g+3)/(3*(1-2*g))
        assert g*rg<.6 and ea[0]<0<ea[-1] and max(eb)<0
        assert abs(2*(W(b,g)-W(a,g))-tens)<1e-12
        rows.append({"g":g,"r":rg,"g_times_r":g*rg,
           "exact_tension_formula_evaluated":tens,
           "source_Hessian_plus_count":int(sum(ea>0)),
           "target_Hessian_plus_count":int(sum(eb>0))})
    return {"proved_interval":"0<g<=3/8",
      "critical_endpoint_formula":"r(g)^3=(3-2g)/(3-6g)",
      "exact_BPS_tension_all_g":"(4g^2+3)/(3(1-2g))",
      "rigorous_uniform_monotonicity_bound":"g*r(g) <= (3/8)*cuberoot(3) < 3/5 on 0<g<=3/8; d(Fq/q)/dq <0",
      "certifying_integer_comparison":"81*125<27*512",
      "source_single_positive_and_target_no_positive_Hessian_modes_all_g":True,
      "sample_checks":rows,
      "physics_scope":"Global-SUSY real canonical scalar gradient theorem, not a gauge-invariant E8 compactification or a physical three-family BPS monopole."}

def fermion_gates(sol,wall):
    # Inserting H_W as the fermion mass gives index one, with the
    # translational zero mode psi(z)=F(v(z)). This is NOT 3 families.
    assert wall["natural_Hessian_Dirac_Fredholm_index"]==1
    O=np.exp(2j*pi/3)
    X=np.roll(np.eye(3),1,axis=1)
    Z=np.diag([1.,O,O**2])
    U=np.eye(4,dtype=complex);V=U.copy()
    U[1:,1:]=X;V[1:,1:]=Z
    # H27 equivariant singlet + triplet can select exactly 3,
    # at the expense of an exact triplet degeneracy.
    K=np.diag([PHI**-4,1.,1.,1.])
    assert np.linalg.norm(K@U-U@K)<1e-14
    assert np.linalg.norm(K@V-V@K)<1e-14
    portal=sol.y[0]*sol.y[1]*sol.y[2]/R**3
    assert abs(portal[0])<1e-4 and abs(portal[-1]-1)<1e-10
    # portal xyz is H27 clock-and-shift invariant (det U3=1).
    ends=[(2,2-9*l) for l in np.diag(K)]
    assert sum(lo>0 and hi<0 for lo,hi in ends)==3
    # Explicit no-automatic-three-index on circle:
    # interval chiral BC can select 3 left 0 modes but are INPUT.
    # For left mode f'=m f and right g'=-m g, a 1st-order
    # solution has one integration constant. For triplets, impose
    # right Dirichlet at both ends, left unrestricted => 3 left;
    # singlet mixed left/right Dirichlet at opposite ends => none.
    # On periodic S1 adjoint index always zero.
    return {"natural_mass_choice_M_Hessian_of_W_has_index":1,
      "natural_mass_translational_zero_mode":"psi(z)=F(v(z)), Dpsi=(partial_z-H(v))psi=0",
      "H27_irrep_choice":"one singlet plus one irreducible qutrit (1+3)",
      "H27_invariant_alternative_4ch_mass_operator":
        "M(z)=2 I -9 xyz/r^3 diag(phi^-4,1,1,1)",
      "H27_covariant_exact_commutators":True,
      "H27_invariant_portal":"xyz transforms with determinant1 under shift and clock",
      "alternative_noncompact_chiral_count":3,
      "alternative_singlet_mass_ends":ends[0],
      "alternative_triplet_mass_ends":ends[1],
      "alternative_triplet_profiles_identical":True,
      "orbifold_or_interval_with_imposed_boundary_parities_can_have_three_left_zero_modes":True,
      "smooth_circle_index":0,
      "serious_caution":"Three on an interval are set by boundary/domain parity and/or specified H27 triplet, not derived from Pascal K2; a constant bulk Dirac mass may violate an orbifold reflection parity unless its odd profile and action are constructed. H27 triplet degeneracy gives no observed flavor hierarchy. No complete inflow."}

def yukawa_gut_gate(sol):
    x,y,z=sol.y[:3]
    portal=x*y*z/R**3
    t=sol.t
    # The symmetric threefold multiplet's normalized zero modes are identical
    # with an H27 scalar portal and H27-invariant K; only non-universal
    # source/defect flavor tensors produce different masses.
    m=2-9*portal
    phase=cumulative_trapezoid(m,t,initial=0)
    wave=np.exp(np.clip(phase-phase.max(),-700,0))
    wave/=sqrt(trapezoid(wave*wave,t))
    Hfl=np.eye(3)*trapezoid(wave*wave*portal,t)
    assert np.linalg.matrix_rank(Hfl)==3
    assert np.max(abs(np.linalg.svd(Hfl,compute_uv=False)-np.diag(Hfl)))<1e-11
    # SU3 gauge invariant epsilon_{ijk} Q_i U_j h_k for DISTINCT
    # commuting triplet fields => antisymmetric mass matrix, rank2.
    h=np.array([1.,2.,3.])
    A=np.array([[0,h[2],-h[1]],[-h[2],0,h[0]],[h[1],-h[0],0.]])
    singular=np.linalg.svd(A,compute_uv=False)
    assert np.linalg.matrix_rank(A)==2
    assert abs(np.linalg.det(A))<1e-12
    assert np.allclose(singular,[np.linalg.norm(h),np.linalg.norm(h),0])
    # Symmetric 6bar Higgs tensor can instead yield generic full rank.
    S=np.diag([1.,2.,3.])
    assert np.linalg.matrix_rank(S)==3
    return {"H27_unbroken_singlet_Higgs_Yukawa":
      "Y=c I3; rank3 but all three physical mass singular values equal",
      "H27_scalar_portal_overlap_factor":float(Hfl[0,0]),
      "three_identical_chiral_wavefunctions":True,
      "SU3_three_distinct_triplets_epsilon_Yukawa":"Y_ij=epsilon_ijk h_k",
      "gauged_SU3_family_cubic_anomaly_for_one_Spin10_16_triplet":16,
      "gauged_SU3_family_cubic_anomaly_for_one_E6_27_triplet":27,
      "complete_E8_E6xSU3_pair_anomaly":27-27,
      "gauged_family_anomaly_caution":"With SU3 family gauged, a single chiral (16,3) contributes +16 units of SU3_f^3 anomaly, while (27,3) contributes +27. The conjugate (27bar,3bar) cancels but would add unwanted opposite chirality unless projected/lifted consistently. For an un-gauged discrete H27 the continuous SU3_f^3 obstruction does not directly apply; discrete anomalies must be checked separately.",
      "epsilon_Yukawa_singular_values":singular.tolist(),
      "epsilon_Yukawa_rank":2,
      "symmetric_anti_sextet_Higgs_example_Yukawa_rank":3,
      "E8_UV_warning":"Single H27-invariant sextic of one SU3 triplet is not SU3 invariant; single E8 adjoint degree6 invariant space generated by quadratic Casimir cubed (parallel commit 6093b466). Distinct species and gauge-legal messenger operators required.",
      "scope":"Trivial H27 singlet Higgs gives degenerate mass3; epsilon triplet Higgs gives rank2. An independent 6bar Higgs or dynamically broken-H27 full-rank tensor is required for realistic masses, not derived from E8."}

def causal_gate():
    # Two nonisomorphic 5-posets sharing ALL global interval layer counts.
    # Hasse undirected graph 2-edge star vs two disconnected edges.
    E1=[(0,1),(0,2)]
    E2=[(0,1),(2,3)]
    def sig(edges):
        A=np.zeros((5,5),dtype=int)
        for i,j in edges:A[i,j]=1
        H=A+A.T
        L=np.diag(H.sum(0))-H
        hist=[]
        for k in range(4):
            hist.append(sum(A[i,j] and sum(A[i,p] and A[p,j] for p in range(5))==k for i in range(5) for j in range(5)))
        return hist,np.linalg.eigvalsh(L),int(np.trace(L@L))
    h1,e1,t1=sig(E1);h2,e2,t2=sig(E2)
    assert h1==h2==[2,0,0,0]
    assert t1==10 and t2==8
    assert not np.allclose(e1,e2)
    return {"n":5,"same_global_causal_interval_histogram":[2,0,0,0],
      "poset_A_cover_edges":E1,"poset_B_cover_edges":E2,
      "Hasse_graph_laplacian_spectrum_A":e1.tolist(),
      "Hasse_graph_laplacian_spectrum_B":e2.tolist(),
      "Laplacian_trace_square_A":t1,"Laplacian_trace_square_B":t2,
      "lesson":"An interval-count-only action cannot distinguish these nonisomorphic posets; a Hasse spectral statistic can, but no physical Lorentzian gravitational action or continuum first-class Einstein constraints follows."}

def photon_gate():
    arr=[]
    for x,eta in [(0,.9),(.5,.9),(1.,.9),(2.,.9),(1.,.99)]:
        S=1+sqrt(1+np.exp(-2*x*x))
        gap=eta*eta*(S-2)
        # Under IID bounded CHSH score Z in [-4,4],
        # Hoeffding simultaneous type-I alpha and type-II beta:
        # N>=32*(sqrt(log(1/alpha))+sqrt(log(1/beta)))^2/gap^2.
        alpha=.001;beta=.1
        N=ceil(32*(sqrt(log(1/alpha))+sqrt(log(1/beta)))**2/gap**2)
        arr.append({"x":x,"eta":eta,"ideal_CHSH":S,
          "optimistic_loss_CHSH_upper":2+gap,"upper_violation_gap":gap,
          "iid_trials_for_alpha_0p001_power_90pct_IF_upper_bound_attained":N})
    assert arr[3]["iid_trials_for_alpha_0p001_power_90pct_IF_upper_bound_attained"]>10**9
    return {"cases":arr,
      "concentration":"Hoeffding for independent uniformly assigned CHSH scores Z in [-4,4], with alpha=.001 and beta=.1; assumes true mean reaches the optimistic loss upper bound.",
      "scope":"Strict local number SSR and iid differential phase noise; no certified optical collective gate/measurement, detector loophole closure, or beyond-QM signal. Eberhard efficiency 2/3 applies to a different optimized Bell protocol and cannot simply be transplanted."}

def run():
    wall,sol=coupled_BPS()
    out={"source_parallel":"37ba627b H27 mass lift; 184cd0b0 Pascal channel; 3700bb0f compactness/H27 coupling no-go",
      "coupled_BPS":wall,"coupling_interval_theorem":coupling_interval_theorem(),
      "chirality_and_compact":fermion_gates(sol,wall),
      "flavor_and_GUT":yukawa_gut_gate(sol),
      "causal_action_discriminator":causal_gate(),
      "photonic_power":photon_gate(),
      "status":"A real coupled BPS gradient wall EXISTS in the canonical 3-field H27 toy; the naturally induced Hessian fermion index is ONE, not three. No gauge-invariant E8 UV completion or compact anomaly-free three-family 4D TOE."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("BPS WALL: exact delta W=13/12 T=13/6, numeric T=",wall["numerical_energy_integral"])
    print("NATURAL HESSIAN FERMION INDEX:",wall["natural_Hessian_Dirac_Fredholm_index"])
    print("H27-SYMMETRIC ALTERNATIVE INDEX:",out["chirality_and_compact"]["alternative_noncompact_chiral_count"])
    print("SU3 EPSILON HIGGS RANK:",out["flavor_and_GUT"]["epsilon_Yukawa_rank"])
    print("CAUSAL COLLISION TR(L²)=",out["causal_action_discriminator"]["Laplacian_trace_square_A"],out["causal_action_discriminator"]["Laplacian_trace_square_B"])
    print("JSON",OUT)
    return out

if __name__=="__main__":run()
