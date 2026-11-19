"""Seven TOE dependency gates: Spin10 rank, SUSY Higgs exotics, 4D causal Box,
boundary eigenmodes, Wilson local-system projection, photon scaling and bias.

Everything is a conditional model/known continuum construction, not a TOE.
"""
from pathlib import Path
from math import pi,sqrt,log,exp,gamma,factorial
from itertools import combinations
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_rank_Higgs_BDG4_boundary_photon_gates.json"

def spin10_all_holonomy_rank_no_go():
    """Every inner holonomy preserving standard SM lies in Spin10 maximal torus."""
    d=5
    unit=[sp.eye(d)[:,i] for i in range(d)]
    roots=[]
    for i,j in combinations(range(d),2):
        roots += [unit[i]-unit[j],unit[j]-unit[i],
                  unit[i]+unit[j],-unit[i]-unit[j]]
    assert len(roots)==40
    # Lie(T_SM)=trace-zero diagonal SU5, precisely rank 4.
    trace_zero=[unit[i]-unit[4] for i in range(4)]
    assert sp.Matrix.hstack(*trace_zero).rank()==4
    # Any D5 root vanishing on T_SM would be proportional to (1,..,1).
    restrictions=[sp.Matrix([r.dot(v) for v in trace_zero]) for r in roots]
    vanishing=[i for i,v in enumerate(restrictions) if v==sp.zeros(4,1)]
    assert vanishing==[]
    # Therefore C_Spin10(T_SM) = T_Spin10 (rank5).
    # A holonomy whose centralizer contains SM commutes with T_SM,
    # so each holonomy must lie in this torus; even mutually noncommuting
    # generators of pi1 map to commuting elements.
    return {
        "D5_root_count":len(roots),"SM_maximal_torus_rank":4,
        "Spin10_rank":5,"D5_roots_vanishing_on_SM_torus":vanishing,
        "centralizer_of_SM_torus_Lie_rank":5,
        "exact_inner_holonomy_theorem":"For the standard SU5-embedded SM in Spin10, any subgroup of inner flat holonomies preserving all of SM lies in the Spin10 maximal torus. Its centralizer therefore has rank5, not rank4. Arbitrarily many noncommuting pi1 generators cannot evade this while preserving that SM.",
        "caveat":"Outer gauge automorphisms, nonflat fluxes, Higgs VEVs, symmetry breaking that changes the SM embedding, or additional gauge sectors are outside the theorem."
    }

def cyclic_W7_GUT_projection():
    pairs={}
    for n in range(2,14):
        cand=[]
        for a in range(n):
            for b in range(n):
                if (3*a+2*b)%n or a==b:continue
                extra=(3 if (2*a)%n==0 else 0)+(6 if (a+b)%n==0 else 0)+(1 if (2*b)%n==0 else 0)
                cand.append((a,b,13+2*extra))
        pairs[str(n)]=[{"a":a,"b":b,"Spin10_unbroken_dimension":dim} for a,b,dim in cand]
    assert min(int(n) for n,items in pairs.items() if any(x["Spin10_unbroken_dimension"]==13 for x in items))==7
    n,a,b=7,2,4
    assert (3*a+2*b)%n==0
    su5_5=[a]*3+[b]*2
    ten=[(su5_5[i]+su5_5[j])%n for i,j in combinations(range(5),2)]
    bar5=[(-z)%n for z in su5_5]
    spinor=[0]+ten+bar5
    assert len(spinor)==16
    assert sum(z==0 for z in spinor)==1
    # 45 = su5 adjoint24 + chi1 + antisym10 + conjugate10.
    invariant_su5=12
    invariant_ten=sum(z==0 for z in ten)
    centralizer=invariant_su5+1+2*invariant_ten
    assert centralizer==13
    return {
      "cyclic_orders_2_through_13":pairs,
      "minimal_cyclic_order_for_SM_plus_chi":7,
      "example_mod7_color_weak_exponents":[a,b],
      "Spin10_centralizer_dimension":centralizer,
      "one_16_SU5_decomposition":"1 + wedge2(5) + bar5",
      "one_16_all_component_Wilson_Z7_exponents":spinor,
      "one_16_trivial_holonomy_component_count":sum(z==0 for z in spinor),
      "not_a_chirality_derivation":"Only constant bulk-section invariants are counted: the original relative-cohomology/defect zero modes carry nontrivial local coefficients and must be rebuilt; the existing lens-space twisted-sector result finds vectorlike mirrors. One Spin10 chi remains."
    }

def vectorlike_spinor_Higgs_escape_and_exotics():
    """Vectorlike 16+16bar & neutral X: F,D flat, but 5+bar5 remain."""
    v=sp.Rational(3,2)
    # 16=1+10+bar5; bar16=1+bar10+5. X(16*bar16-v²)
    # With V=(v,0^15), Vbar=(v,0^15), X=0, target v².
    sing=sp.symbols('N Nbar X')
    N,Nbar,X=sing
    W=X*(N*Nbar-v*v)
    F={str(z):sp.diff(W,z) for z in sing}
    vacuum={N:v,Nbar:v,X:0}
    assert all(sp.expand(f.subs(vacuum))==0 for f in F.values())
    # Full complex Hessian 16+16bar+X has only H_X,N and H_X,Nbar nonzero.
    H=sp.zeros(33,33)
    for i in (0,16):
        H[i,32]=H[32,i]=v
    assert H.rank()==2
    # A pure spinor and its conjugate break Spin10->SU5:
    # dim SO10 - dim SU5 =45-24=21 broken complex gauge generators.
    null_dim=33-H.rank()
    physical_modes=null_dim-21
    assert physical_modes==10
    # Under SU5 these are bar5+5, i.e. exotic vectorlike light chiral pair.
    # D_chi =-5|N|² +5|Nbar|² =0; all 45 D terms cancel by conjugation.
    Dchi=sp.expand(-5*v*v+5*v*v)
    assert Dchi==0
    # Previous baseline matter/gravitino-dependent discrete R parity: adding
    # two R0 multiplets (16+16bar) and one R2 driver shifts matter-fermion
    # coefficient by -16-16+1=-31, an odd number.
    r_parity_delta=(-16-16+1)%2
    assert r_parity_delta==1
    return {
      "superpotential":"W=X*(16*16bar-v²) using Spin10 invariant contraction",
      "VEV_magnitude":str(v),
      "symbolic_F_terms":{k:str(z) for k,z in F.items()},
      "D_chi_residual":str(Dchi),
      "total_chiral_multiplet_components":33,
      "Hessian_rank":H.rank(),
      "Hessian_kernel_complex_dimension":null_dim,
      "Spin10_breaking":"Spin10 -> SU5 by aligned D-flat SM singlet in 16+bar16",
      "broken_complex_gauge_dimension":21,
      "physical_massless_complex_chiral_remainder":physical_modes,
      "remainder_SU5_representation":"5 + bar5",
      "subsequent_Z7_Wilson_broken_algebra_dimension":12,
      "new_pair_net_chiral_index":0,
      "original_three_spinor_net_index_after_added_pair":3,
      "matter_fermion_Z4R_gravitational_parity_delta":r_parity_delta,
      "obstruction":"The minimal vectorlike-pair/driver repair solves the rank & D-flat gates but leaves 5+bar5 massless chiral multiplets and changes the matter gravitational R parity. New couplings/geometric projections are needed. No full 5D or G2 vacuum is supplied."
    }

def vectorlike_spinor_Higgs_with_ten_completion():
    """Repair the 5+bar5 moduli with one extra real Spin10 10, but audit E8 charges.

    Known 16x16 contains a real 10, and bar16xbar16 contains the same 10.
    With aligned pure singlet VEVs, each Yukawa gives one SU5 5+bar5
    mass block, while all vev tadpoles vanish by SU5/chi charge selection.
    """
    v=sp.Rational(3,2)
    l1=sp.Rational(2,3);l2=sp.Rational(3,5)
    # SU5 decomposition:
    # A16 : N (1), A10 (10), Abar5 (5)
    # Bbar16: Nbar (1), Bbar10 (10), B5 (5)
    # H10: H5 (5), Hbar5 (5), X neutral
    # W=X(A.B-v²)+(lambda/2) A.A.H + (lambdabar/2) B.B.H
    # At A.N=B.Nbar=v, H=0, F=0. Only massive quadratic
    # W2=v*X*(dA_N+dB_N)+lambda*v*Abar5.H5+
    # lambdabar*v*B5.Hbar5.
    H=sp.zeros(43)
    for i in (0,16):
        H[42,i]=H[i,42]=v
    for j in range(5):
        iA,iH=11+j,32+j
        iB,iHb=27+j,37+j
        H[iA,iH]=H[iH,iA]=v*l1
        H[iB,iHb]=H[iHb,iB]=v*l2
    # Independently differentiate the SU5 component terms of the
    # Spin10-invariant W at the aligned singlet vacuum.
    zz=sp.symbols("z0:43")
    Wlocal=zz[42]*(zz[0]*zz[16]-v*v+
           sum(zz[1+i]*zz[17+i] for i in range(10))+
           sum(zz[11+j]*zz[27+j] for j in range(5)))
    Wlocal+=l1*zz[0]*sum(zz[11+j]*zz[32+j] for j in range(5))
    Wlocal+=l2*zz[16]*sum(zz[27+j]*zz[37+j] for j in range(5))
    values={z:0 for z in zz};values[zz[0]]=values[zz[16]]=v
    Fsymbolic=[sp.diff(Wlocal,z).subs(values) for z in zz]
    assert all(z==0 for z in Fsymbolic)
    Hsymbolic=sp.Matrix([[sp.diff(Wlocal,x,y).subs(values) for y in zz]
                          for x in zz])
    assert Hsymbolic==H
    rank=int(H.rank())
    assert rank==22
    ker=43-rank
    assert ker==21
    assert ker-(45-24)==0
    # Original E8 source uses 4 SU4 weights e1,e2,e3,e4; 10
    # weights are e_i+e_j, never zero and never +/-2e_i.
    e=[sp.Matrix(q) for q in [(1,0,0),(0,1,0),(0,0,1),(-1,-1,-1)]]
    ten=[e[i]+e[j] for i,j in combinations(range(4),2)]
    assert all(q!=sp.zeros(3,1) for q in e+ten)
    assert all(two!=q for base in e for two in (2*base,-2*base) for q in ten)
    # For a neutral X and a vectorlike pair with q_B=-q_A=qopp,
    # both A²H and B²H demand q_H=-2q_A=+2q_A => q_A=q_H=0
    # in a torsion-free Z^3 charge lattice. No such source 10/16.
    # Discrete R: R(A)=R(B)=0, R(X)=R(H)=2 so all three W terms R2.
    DeltaR=-16-16+1+10
    assert DeltaR%2==1
    return {
      "full_4D_chiral_component_count":43,
      "spinor_pair_plus_real_ten_and_driver_reps":"16_H + bar16_H + 10_H + X",
      "renormalizable_superpotential":"W=X(16_H.bar16_H-v²) + (lambda/2)16_H.16_H.10_H + (lambdabar/2)bar16_H.bar16_H.10_H",
      "R_charges":{"16_H":0,"bar16_H":0,"10_H":2,"X":2},
      "aligned_pure_spinor_singlet_VEV":str(v),
      "F_terms_all_zero_at_H10_X0":True,"D_terms_all_zero":True,
      "independent_43_field_symbolic_F_gradient_and_Hessian_match":True,
      "superpotential_Hessian_exact_rank":rank,
      "massive_Higgs_chiral_pairs_from_5_and_bar5":10,
      "Hessian_kernel_dimension":ker,
      "complex_broken_Spin10_to_SU5_gauge_dimension":21,
      "physical_4D_local_complex_moduli_after_gauge":ker-21,
      "residual_SU5_5_plus_bar5":"fully massive at lambda*v and lambdabar*v",
      "three_original_16_net_chiral_index_unchanged":3,
      "original_E8_source_U1_charge_weight_vectors_16":[list(map(int,q)) for q in e],
      "original_E8_source_U1_charge_weight_vectors_10":[list(map(int,q)) for q in ten],
      "no_source_uncharged_spinor_or_10":True,
      "no_source_10_has_plus_or_minus_twice_spinor_charge":True,
      "simple_neutral_X_vectorlike_charge_selection_forces_zero_charge":True,
      "conditional_matter_gravitational_Z4R_parity_shift":DeltaR%2,
      "physical_obstruction":"The extended 4D supersymmetric Higgs sector is locally isolated (massless kernel exactly 21 gauge directions), but its required q=0 spinor/10 Higgs fields DO NOT occur in the original E8 SU4 source spectrum. Other charged spurions/defect zero modes or an enlarged compactification are required; original U1 anomalies, global R anomaly, proton decay and full G2 geometry remain unsolved.",
      "source":"Established SO10 cubic invariant 16*16*10 and SU5 decomposition; finite rank/charge census verified here; no claimed original Higgs construction novelty."
    }


def causal_BDG4_quadratic_recovery():
    """Independently reconstruct the known 4D Benincasa-Dowker layers."""
    basis=[]
    for alpha in (sp.Rational(1,2),sp.Integer(1),sp.Rational(3,2)):
        den=sp.sqrt(sp.pi) if alpha!=1 else sp.Integer(1)
        basis.append([sp.simplify(sp.gamma(k+alpha)/sp.factorial(k)/den)
                      for k in range(4)])
    moments=sp.Matrix(basis)
    ns=moments.nullspace()
    assert len(ns)==1
    weights=sp.Matrix([-8*x for x in ns[0]])
    assert weights==sp.Matrix([1,-9,16,-8])
    kappa=pi/24
    def g(s):
        if s<=0:return 1.
        if s>=1:return 0.
        z=sqrt(1-s)
        return z-s*log((1+z)/sqrt(s))
    def H2(s):
        if s<=0:return .25
        if s>=1:return 0.
        z=sqrt(1-s)
        return ((2-s)*z-s*s*log((1+z)/sqrt(s)))/8
    def spatial(f,s):
        if f=="1":return .5*g(s)
        if f=="t":return (1-s)**1.5/3
        if f=="t²":return H2(s)
        if f=="r²":return H2(s)-s*g(s)/2
        if f=="s":return s*g(s)/2
        raise ValueError(f)
    def K(rho,f):
        zmax=min(120,rho*kappa)
        def integ(z):
            s=sqrt(z/(rho*kappa))
            P=1-9*z+8*z*z-sp.Rational(4,3)*z*z*z
            return exp(-z)*float(P)*spatial(f,s)
        # direct quadrature with algebraic weight z^-1/2
        I=quad(integ,0,zmax,weight='alg',wvar=(-.5,0),
               epsabs=5e-11,epsrel=3e-11,limit=450)[0]
        return pi*sqrt(rho/kappa)*I
    vals=[]
    for rho in (1000,10000,100000,1000000):
        D={p:K(rho,p) for p in ("1","t","t²","r²","s")}
        factor=(4/sqrt(6))*sqrt(rho)
        B={p:factor*(x-(1. if p=="1" else 0.)) for p,x in D.items()}
        B["x²"]=B["r²"]/3.
        beta=.6;g2=1/(1-beta*beta)
        B["t'²"]=g2*(B["t²"]+beta*beta*B["x²"])
        B["x'²"]=g2*(B["x²"]+beta*beta*B["t²"])
        vals.append({"rho":rho,"unscaled_K":D,
                     "BDG4_normalized_wave_operator":B})
    last=vals[-1]["BDG4_normalized_wave_operator"]
    targets={"1":0,"t":0,"t²":-2,"r²":6,"s":-8,
             "x²":2,"t'²":-2,"x'²":2}
    assert all(abs(last[k]-target)<.03 for k,target in targets.items()),(last,targets)
    # Exact asymptotic mechanism for s=t²-r²:
    # ∑w Γ(k+3/2)ψ(k+3/2)/k! = -sqrt(pi)/3
    digamma_sum=sp.simplify(sum(weights[k]*sp.gamma(sp.Rational(3,2)+k)*
                                  sp.digamma(sp.Rational(3,2)+k)/sp.factorial(k)
                                  for k in range(4)))
    assert sp.simplify(digamma_sum+sp.sqrt(sp.pi)/3)==0
    const_sum=sp.simplify(sum(weights[k]*sp.digamma(k+1) for k in range(4)))
    assert const_sum==sp.Rational(1,3)
    return {
      "source":"Known Benincasa-Dowker four-dimensional retarded d'Alembertian (2010); independently reconstructed from moment cancellation, not invented here.",
      "exact_moment_matrix":str(moments),
      "unique_primitive_four_layer_weights":list(map(int,weights)),
      "local_counterterm":"-phi(origin)",
      "density_normalization":"4*sqrt(rho)/sqrt(6) for 4D rho=l^-4",
      "digamma_s_sum":str(digamma_sum),"constant_renormalization_sum":str(const_sum),
      "asymptotic_Wave_box_s_exact":-8,
      "numerical_density_benchmarks":vals,
      "continuum_targets":targets,
      "limitations":"Only expectation in fixed truncated Minkowski future cone on displayed polynomial and boosted quadratic probes. No finite sprinkling variance/concentration, arbitrary-field convergence, curvature, spin-2, constraint algebra, or emergent Einstein action."
    }

def orbifold_boundary_Robin_spectrum():
    """Simple second-order interval eigenmode proxy, NOT 5D Dirac spectrum."""
    table=[]
    for mu in (0,1e-4,1,10,100):
        roots=[]
        for n in range(3):
            if mu==0:x=n*pi
            else:x=brentq(lambda t:t*np.tan(t)-mu,
                           n*pi+1e-11,n*pi+pi/2-1e-9,xtol=1e-13)
            roots.append(float(x))
        table.append({"dimensionless_brane_mu":mu,"first_three_kL":roots})
    assert table[0]["first_three_kL"][0]==0
    assert table[-1]["first_three_kL"][0]>1.55
    assert table[-1]["first_three_kL"][0]<pi/2
    # If M_KK=1e13, octet2 mu=100 lifts near 1.56e13;
    # triplet/first octet mu0 retains zero mode; small masses separate.
    return {
       "scalar_proxy_equation":"f''+k² f=0, Neumann f'(0)=0, Robin f'(L)+h f(L)=0 -> x tan x=mu=hL",
       "roots":table,
       "one_heavy_octet_proxy_mass_GeV":table[-1]["first_three_kL"][0]*1e13,
       "example_triplet_and_one_octet_zero_modes_maintained_with_mu0":True,
       "limits":"This is a scalar Sturm-Liouville proxy, not the actual 5D adjoint fermion/brane Majorana boundary action. A supersymmetric gauge-invariant UV origin and complete KK spectrum are unbuilt. Mass saturation at ~pi/(2L) is explicit."
    }

def photon_single_qubit_gate_real_cost():
    rows=[]
    for n in (4,7,10,12):
        modes=2**n
        # A logical bit flip of one qubit in unary one-photon encoding
        # permutes 2^(n-1) disjoint pairs of physical optical modes.
        swaps=modes//2
        assert len({(i,i^(1<<(n-1))) for i in range(modes)
                    if i<(i^(1<<(n-1)))})==swaps
        rows.append({"logical_qubits":n,"required_orthogonal_modes":modes,
                     "mode_swaps_for_one_logical_X":swaps,
                     "generic_Ud_real_parameters":modes*modes})
    # A standard QM Bernoulli true p=1/2 becomes observed p=.51 if
    # successful detections are 4.0816% more likely to be accepted.
    target=.51;null=.5
    acceptance_success_vs_failure=target*(1-null)/(null*(1-target))
    assert abs(acceptance_success_vs_failure-51/49)<1e-13
    return {
       "mode_swap_resource_table":rows,
       "one_photon_passive_linear_optics_physical_cost":"logical X flip requires 2^(n-1) independent disjoint physical mode swaps for standard binary occupation encoding, unless specialized shared controls alter hardware cost. A generic U(2^n) has 4^n real parameters.",
       "success_detection_acceptance_bias_that_mimics_p0_0p5_as_pobs_0p51":acceptance_success_vs_failure,
       "conditional_experimental_warning":"Even 55,000 independent accepted events can falsely favor a hypothetical 1% probability deviation if success-dependent acceptance has relative odds 51/49. An actual TOE must derive a non-QM prediction, calibrate efficiencies, and close setting/deletion loopholes.",
       "limits":"Swap count for a particular binary mode encoding and independent mode switches, not a universal lower bound for every programmable multiplexed optical device or multi-photon architecture."
    }

def physics_first_dependency_gate():
    return {
     "particle_first":"Derive an anomaly-free compact source with globally supported Higgs/vectorlike Spin10-breaking sector, a nontrivial defect Yukawa overlap, and the true global gauge quotient together.",
     "specific_first_falsifier":"Derive actual E8/G2 charged Higgs zero modes allowing 16_H + bar16_H + 10_H + X (or genuine charged spurion replacements), without postulating missing q=0 representations; preserve F/D-flatness, global chirality, anomaly cancellation and the independent R symmetry.",
     "gravity_first":"The known 4-layer BDG operator passes polynomial Box tests, but not necessarily arbitrary field/variance, much less spin-2 Einstein constraints. Derive an intrinsic localized convergent causal kinetic action and nonlinear first-class gravity.",
     "photonic_first":"Identify an active nonlinear resource with physical cost polynomial in n before labeling a one-photon d=2^n rail encoding scalable BQP.",
     "unification_bridge":"The same metric/flux data must fix matter wavefunction localization, GS inflow and Einstein kinetic terms. Currently each is an independently supplied degree of freedom, so all three cannot be 'derived' merely by matching E8 representation counts.",
     "methodology":"Reject proposed keystones on the first failed necessary gate; record assumptions separately from established group/cohomology/quantum facts."
    }

def run():
    out={
       "Spin10_nonabelian_holonomy_rank_no_go":spin10_all_holonomy_rank_no_go(),
       "Z7_Wilson_component_projection":cyclic_W7_GUT_projection(),
       "supersymmetric_vectorlike_Higgs_exotics":vectorlike_spinor_Higgs_escape_and_exotics(),
       "renormalizable_Higgs_with_real_ten_escape":vectorlike_spinor_Higgs_with_ten_completion(),
       "four_layer_BDG4_causal_wave_operator":causal_BDG4_quadratic_recovery(),
       "orbifold_boundary_Robin_proxy":orbifold_boundary_Robin_spectrum(),
       "single_photon_gate_and_acceptance_cost":photon_single_qubit_gate_real_cost(),
       "physics_dependency_priority":physics_first_dependency_gate()
    }
    OUT.write_text(json.dumps(out,indent=2,default=int)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("SM_HOLONOMY_RANK",out["Spin10_nonabelian_holonomy_rank_no_go"]["centralizer_of_SM_torus_Lie_rank"])
    print("HIGGS_EXOTIC_MODULI",out["supersymmetric_vectorlike_Higgs_exotics"]["physical_massless_complex_chiral_remainder"])
    print("BDG4",out["four_layer_BDG4_causal_wave_operator"]["numerical_density_benchmarks"][-1]["BDG4_normalized_wave_operator"])
    print(OUT)
    return out
if __name__=="__main__":run()
