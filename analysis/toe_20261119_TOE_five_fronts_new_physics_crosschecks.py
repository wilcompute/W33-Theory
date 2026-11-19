"""Physics-first TOE five-front falsification/escape certificates, November 19 2026.

1. Compact relative triple cup on punctured T^3 vs S^3 no-go.
2. E8 balanced-source singlet positive-cone D-flat obstruction.
3. Charged-family Takagi hierarchy theorem for hollow symmetric Yukawas.
4. Full homogeneous Einstein-scalar constraint propagation vs deformed dynamics.
5. Event-ready memory witness versus unassisted quantum erasure capacity.
6. Two split SU5 multiplets as formal one-loop escape, GUT-scale/proton risk.

All claimed facts are scoped to explicit assumptions; no TOE or G2 vacuum.
"""
from __future__ import annotations
from itertools import combinations, product
from math import pi, sqrt, log, exp, ceil
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.stats import binom
from toe_20261119_balanced_source_E8_cup_gate import sector_census

ROOT = Path(__file__).resolve().parents[1]

def compact_topology_cup():
    # T^3 - open B^3. Compactly supported relative one-forms
    # alpha_i=dx_i-d(chi(r)*xi_i) equal 0 in collar of ball and dx_i outside.
    # Since the extended alpha_i are cohomologous to dx_i on T3, triple integral=1.
    r0,r1=.10,.20
    def chi_deriv(r):
        if r<=r0:return (1.,0.)
        if r>=r1:return (0.,0.)
        t=(r-r0)/(r1-r0)
        smooth=6*t**5-15*t**4+10*t**3
        deriv=(30*t**4-60*t**3+30*t**2)/(r1-r0)
        return 1-smooth,-deriv
    def triple_density(r):
        h,dh=chi_deriv(r)
        return (1-h)**3-(1-h)**2*r*dh
    annulus,err=quad(lambda r:4*pi*r*r*triple_density(r),r0,r1,
                     epsabs=1e-12,epsrel=1e-12,limit=300)
    # Outside support of chi, det(alpha)=1; inside r0 det=0.
    outer=1-4*pi*r1**3/3
    pairing=outer+annulus
    assert abs(pairing-1)<1e-12
    # exact relation d/dr [r^3(1-chi)^3]/3
    for r in np.linspace(r0+.005,r1-.005,11):
        h,dh=chi_deriv(r)
        lhs=r*r*triple_density(r)
        rhs=r*r*(1-h)**3-r**3*(1-h)**2*dh
        assert abs(lhs-rhs)<1e-13
    return {
      "source_base":"T3 minus open ball (one spherical source boundary)",
      "relative_H1_rank":3,
      "relative_classes":"alpha_i=dtheta_i-d(chi*xi_i), i=x,y,z",
      "vanish_near_boundary":True,"cup_product_integral":pairing,
      "relative_triple_cup_is_nonzero":True,
      "annulus_integral":annulus,"outer_integral":outer,
      "analytical_radial_identity":"r^2 det(alpha)= (1/3) d_r[r^3(1-chi)^3]",
      "S3_puncture_comparison":"S3 minus balls: H1 bulk zero and strict boundary collar relative H1 triple cup vanishes (parallel cb1a667). Punctured T3 has three bulk H1 classes and triple relative cup =1.",
      "limitation":"Nonzero bulk cohomology ALLOWS, but does not produce, E8 gauge-invariant physical Yukawa amplitudes; a T3 gauge 3-cycle generally carries additional adjoint H1 modes, and no G2 metric or sourced 7D geometry is constructed."
    }

def charged_family_texture():
    rng=np.random.default_rng(20261119)
    worst=0.
    for _ in range(6000):
        a,b,c=rng.normal(size=3)+1j*rng.normal(size=3)
        Y=np.array([[0,a,b],[a,0,c],[b,c,0]],dtype=complex)
        sv=np.linalg.svd(Y,compute_uv=False)
        violation=float(sv[0]-sv[1]-sv[2])
        worst=max(worst,violation)
        assert violation<2e-12
        assert sv[0] <= 2*sv[1]+2e-12
    # Approximate illustrative dimensionless hierarchy; not mass input.
    target=np.array([1.,.01,.00001])
    # If Y_phys=Y_hollow+Delta, Weyl gives
    # s1_phys-delta <= s1_h <= s2_h+s3_h <= s2_phys+s3_phys+2delta.
    lower=(target[0]-target[1]-target[2])/3
    assert lower>.3
    return {
      "E8_parallel_source_texture":"Y=[[0,a,b],[a,0,c],[b,c,0]] with complex a,b,c",
      "exact_takagi_inequality":"s1<=s2+s3, so s1/s2<=2 for s2>0",
      "proof":"Takagi Y=U diag(s1,s2,s3) U^T. Diagonal zeros imply s1 |U_i1|^2 <= sum_{j>1} s_j |U_ij|^2 by triangle inequality, for each row i. Sum over rows; column normalization gives s1<=s2+s3.",
      "random_complex_matrices_checked":6000,"max_numeric_inequality_violation":worst,
      "illustrative_normalized_target_singular_values":target.tolist(),
      "spectral_norm_minimum_nonhollow_correction":lower,
      "correction_proof":"If Y_phys=Y_hollow+Delta and delta=||Delta||_2, singular-value Lipschitz inequality yields s1_phys <= s2_phys+s3_phys+3delta.",
      "claim_limit":"Assumes single complex-symmetric hollow Yukawa, canonical kinetic metrics, and no Higgs-dependent vectorlike mixing. In a realistic model the masses must be compared at a common renormalization scale; this illustrative 1:0.01:0.00001 example is NOT used as measured input."
    }

def e8_singlet_cone():
    sectors,fields,census=sector_census()
    # SU4 weights q1+q2+q3+q4=0 in Z3^3.
    weights=[np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1]),
             np.array([-1,-1,-1])]
    h=np.array([3,1,-1])
    S=[a for a in sectors if a["label"].startswith("S_")]
    assert len(S)==6
    selected=[]
    for a in S:
        charge=np.array(a["SU4_charge"],dtype=int)
        height=int(h@charge)
        if a["b1"]: selected.extend([(a["label"],charge,height)]*a["b1"])
        if a["b2"]: selected.extend([(a["label"]+"_conj",-charge,-height)]*a["b2"])
    assert len(selected)==census["charged_singlet_fields"]==8
    # Two conjugate charged singlets survive: a naive positive-cone
    # obstruction is FALSE. Search exact gauge-neutral charge loops instead.
    charge_by_name={name:q for name,q,z in selected}
    assert "S_12_conj" in charge_by_name and "S_14_conj" in charge_by_name
    loop=("S_13","S_34","S_14_conj")
    loop_sum=sum((charge_by_name[k] for k in loop),np.zeros(3,dtype=int))
    assert np.array_equal(loop_sum,np.zeros(3,dtype=int))
    # Equal condensate magnitudes along this loop make all 3 U(1)
    # moment maps vanish. The S12/conjugate pair supplies another D-flat ray.
    D_vector=loop_sum+charge_by_name["S_12"]+charge_by_name["S_12_conj"]
    assert np.array_equal(D_vector,np.zeros(3,dtype=int))
    active_ten=[a for a in sectors if a["label"].startswith("10_") and a["b1"]>0]
    assert len(active_ten)==5
    diagonal_candidates={}
    for i in range(3):
        one=[]
        for t in active_ten:
            tcharge=np.array(t["SU4_charge"])
            for label,scharge,_ in selected:
                if np.array_equal(2*weights[i]+tcharge+scharge,np.zeros(3,dtype=int)):
                    one.append({"Higgs":t["label"],"spurion":label})
        diagonal_candidates[f"16_{i+1}^2"]=one
    assert all(diagonal_candidates[k] for k in ("16_1^2","16_2^2","16_3^2"))
    # The vectorlike S12 pair and chiral gauge-neutral triangle may condense
    # together with zero D_a for all Cartan generators (canonical metric).
    # Existence of a cubic singlet loop also produces F~S*S; a generic
    # nonzero W=kappa*S13*S34*S14_conj obstructs this particular F-flat ray.
    return {"charged_singlet_multiplets":len(selected),
            "singlet_charge_spectrum":[{"name":k,"charge":q.tolist(),"height":z}
                                       for k,q,z in selected],
            "charged_singlet_pairs":["S_12/S_12_conj","S_14/S_14_conj"],
            "Dflat_triangle_fields":list(loop),
            "Dflat_triangle_charge_sum":loop_sum.tolist(),
            "combined_Dflat_pair_and_triangle":D_vector.tolist(),
            "Dflat_nonzero_Spin10_singlet_condensate_exists_at_zero_FI":True,
            "one_singlet_spurion_diagonal_selection":diagonal_candidates,
            "all_three_diagonal_operators_formally_gauge_allowed":True,
            "Fflat_warning":"A nonzero cubic W=kappa*S13*S34*S14_conj has nonzero F-terms on the triangle ray if all three VEVs are nonzero. Kappa, other operators, and their actual relative-cup overlap are NOT determined here.",
            "physical_limit":"One-spurion gauge invariance and D-flatness are necessary but NOT sufficient to realize fermion masses: the strict bulk relative-cup on the punctured S3 remains zero, full F-flatness/source action, gauge anomalies and realistic unbroken SM are open. Imported chiral singlet spectrum is from cb1a667."
           }

def einstein_scalar_constraint():
    # Flat 3+1 FRW with homogeneous canonical scalar (M_pl=1).
    # Hdot=-pi^2/2, phi_dot=pi, pi_dot=-3H*pi-m^2 phi
    # C=3H^2 -pi^2/2 -m^2phi^2/2; Cdot=0 on exact equations.
    m=.2
    phi0=4.;v0=-.15
    H0=sqrt((v0*v0+m*m*phi0*phi0)/6)
    initial=[phi0,v0,H0]
    def rhs(t,y,gamma=1.):
        phi,v,H=y
        return [v,-3*H*v-m*m*phi,-gamma*v*v/2]
    tgrid=np.linspace(0,25,501)
    good=solve_ivp(rhs,(0,25),initial,args=(1.,),t_eval=tgrid,rtol=1e-11,atol=1e-13)
    bad=solve_ivp(rhs,(0,25),initial,args=(1.05,),t_eval=tgrid,rtol=1e-11,atol=1e-13)
    assert good.success and bad.success
    C=lambda a:3*a[2]**2-(a[1]**2+m*m*a[0]**2)/2
    g=C(good.y);b=C(bad.y)
    assert max(abs(g))<2e-9
    assert max(abs(b))>1e-4
    # Analytic Cdot=3H(1-gamma)*v^2 (straight substitution).
    mid=bad.y[:,250]
    analytic=3*mid[2]*(1-1.05)*mid[1]**2
    numeric=(b[251]-b[249])/(tgrid[251]-tgrid[249])
    assert abs(analytic-numeric)<1e-6
    return {"model":"3+1 Einstein gravity with spatially flat FRW ansatz and homogeneous canonical scalar",
            "V_phi":"m^2 phi^2 /2", "m_in_reduced_planck_units":m,
            "Hamiltonian_constraint":"C=3Mpl^2 H^2-pi^2/2-V=0",
            "constraint_preserving_equations":"Hdot=-pi^2/(2Mpl^2), phidot=pi, pidot=-3Hpi-Vprime",
            "symbolic_identity":"Cdot=0; with Hdot=-gamma pi^2/(2Mpl^2), Cdot=3H(1-gamma) pi^2",
            "initial_data":[phi0,v0,H0],
            "max_constraint_drift_consistent":float(max(abs(g))),
            "max_constraint_drift_gamma_1p05":float(max(abs(b))),
            "gamma":1.05,"midpoint_Cdot_prediction":float(analytic),
            "midpoint_Cdot_finite_difference":float(numeric),
            "limitation":"Fully consistent reduced homogeneous Einstein-scalar equations, not a derivation of 3+1 local Dirac constraint brackets, graviton spectrum, quantum dynamics, or Einstein equations from a new microscopic substrate."}

def memory_capacity_gate():
    d=3;depol=.20;F=1-8*depol/9
    eta=.45
    q=eta*F
    qcap=max(0,2*eta-1)*log(d,2)
    assert q>1/3 and qcap==0
    # Memory+erasure channel has zero unassisted capacity if bare erasure
    # channel of efficiency <=1/2 has zero Q, by concatenation/data processing.
    # We use robust exact binomial power (true q, null p0=1/3).
    def binom_threshold(n,alpha=.001):
        # k smallest integer such that P_{p0}(X>=k) <=alpha.
        lo,hi=0,n+1
        while lo<hi:
            k=(lo+hi)//2
            if binom.sf(k-1,n,1/3)<=alpha:hi=k
            else:lo=k+1
        return lo
    def power_at(n,q):
        k=binom_threshold(n)
        return float(binom.sf(k-1,n,q)),k
    power_rows=[]
    for efficiency in (.45,.5,.6):
        qq=efficiency*F
        lo,hi=1,100
        while power_at(hi,qq)[0]<.90:
            hi*=2
            assert hi<200000
        while lo<hi:
            mid=(lo+hi)//2
            if power_at(mid,qq)[0]>=.90:hi=mid
            else:lo=mid+1
        observed_power,k=power_at(hi,qq)
        # threshold discreteness can make local nonmonotonicities; nearby n
        # search checks first <= n, rather than assert monotonically.
        for n in range(max(1,hi-64),hi):
            if power_at(n,qq)[0]>=.9:
                hi=n;observed_power,k=power_at(n,qq)
                break
        power_rows.append({"eta":efficiency,"true_all_trial_success":qq,
                           "n_approx_90pct_power_at_0p1pct_typeI":hi,
                           "critical_Bell_success_count":k,
                           "exact_binomial_power_at_n":observed_power,
                           "unassisted_erasure_capacity_qubits_per_use":max(0,2*efficiency-1)*log(d,2)})
    assert power_rows[0]["unassisted_erasure_capacity_qubits_per_use"]==0
    return {"memory_dimension":d,"depolarization_p":depol,
            "conditional_Bell_fraction":F,"detection_eta":eta,
            "unconditional_Bell_witness_probability":q,
            "entanglement_breaking_Bell_fidelity_bound":1/3,
            "erasure_p":1-eta,"unassisted_Q_of_pure_qutrit_erasure":qcap,
            "unassisted_Q_of_erasures_plus_depolarization":"zero for eta <=1/2 by data processing",
            "key_distinction":"An event-ready entanglement-fidelity witness may reject entanglement-breaking behavior even when the unassisted asymptotic quantum capacity is provably zero.",
            "sample_size_power_rows":power_rows,
            "sample_size_assumptions":"Independent all-trial Bernoulli Bell success with known calibrated null bound 1/3, alpha=.001, power>=.90, true success eta*F. No experiments performed.",
            "limits":"Heralded two-way-assisted transmission is different; hidden coherent bypass and untrusted references invalidate the witness premise."}

def two_split_gut_gate():
    # Same one-loop inputs, SU(5) GUT hypercharge normalization.
    ae=127.930;sw=.23122;as3=.1180;MZ=91.1876
    inv=np.array([(3/5)*(1-sw)*ae,sw*ae,1/as3])
    bSM=np.array([41/10,-19/6,-7.])
    D=np.array([4/15,0.,2/3]);Lq=np.array([2/5,2/3,0.])
    assert np.allclose(D+Lq,[2/3]*3)
    # Universality: two identical split Dirac fiveplets contribute
    # the aggregate r=sum ln(mL_i/mD_i).
    diffs=np.array([[1,-1,0],[1,0,-1]])
    mat=np.column_stack([diffs@bSM,diffs@D])/(2*pi)
    logMU,rho=np.linalg.solve(mat,diffs@inv)
    MU=MZ*exp(logMU)
    assert logMU>20 and rho<-40 and MU>1e13
    # Single split impossible because |rho|>logMU.
    assert abs(rho)>logMU and abs(rho)<2*logMU
    # Two identical copies with light doublets at 1 TeV.
    mL=1000.
    mD=mL*exp(-rho/2)
    assert MZ<mL<mD<MU
    def run_at_mu():
        full=inv-bSM*logMU/(2*pi)
        for _ in range(2):
            full-=D*np.log(MU/mD)/(2*pi)
            full-=Lq*np.log(MU/mL)/(2*pi)
        return full
    inverse=run_at_mu()
    assert max(inverse)-min(inverse)<1e-11
    # Generic dimension-six proton-decay scaling if MX=MU; no full matrix
    # elements, threshold, alpha or flavor model is supplied.
    relative=(MU/1e16)**4
    assert relative<1e-8
    return {"SM_one_loop_inputs":{"alphaEM_inverse":ae,"sin2thetaW":sw,"alphaS":as3,"MZ_GeV":MZ},
            "SU5_vectorlike_D_beta":D.tolist(),"SU5_vectorlike_L_beta":Lq.tolist(),
            "formal_unification_MU_GeV":MU,
            "aggregate_split_log_mL_over_mD":rho,
            "single_pair_no_go":abs(rho)>logMU,
            "two_pairs_satisfy_mass_ordering_with_example":True,
            "two_pairs_mL_GeV":mL,"two_pairs_mD_GeV":mD,
            "two_pair_unified_inverse_alpha":inverse.tolist(),
            "one_loop_unification_spread":float(max(inverse)-min(inverse)),
            "relative_dimension_six_proton_lifetime_to_MX_1e16_same_couplings":relative,
            "proton_bound_reference":"Super-K 2020 p->e+ pi0 90% CL tau/B>2.4e34yr; reference only, not fitted proton lifetime",
            "takeaway":"A second split Dirac 5+5bar repairs the ONE-PAIR threshold ordering obstruction at one loop, but does not increase MU. A generic SU5 broken-gauge-boson mass MX~MU would face severe proton-decay tension, without an actual proton lifetime calculation.",
            "limits":"No two-loop thresholds, Yukawa, proton matrix elements, scalar sector, exact SU5 breaking model, or demonstration of experimental acceptability."}

def main():
    results={
       "compact_relative_cup":compact_topology_cup(),
       "hollow_Yukawa_hierarchy":charged_family_texture(),
       "E8_singlet_D_cone":e8_singlet_cone(),
       "homogeneous_Einstein_constraint":einstein_scalar_constraint(),
       "photon_memory_capacity":memory_capacity_gate(),
       "two_split_SU5_threshold":two_split_gut_gate()
    }
    output=ROOT/"data"/"toe_20261119_TOE_five_fronts_new_physics_crosschecks.json"
    output.write_text(json.dumps(results,indent=2,default=lambda o: o.item() if isinstance(o,np.generic) else str(o))+"\n",encoding="utf8")
    for k in results:print("PASS",k)
    print("Yukawa spectral lower:",results["hollow_Yukawa_hierarchy"]["spectral_norm_minimum_nonhollow_correction"])
    print("singlet D-flat charge cycle:",results["E8_singlet_D_cone"]["Dflat_triangle_charge_sum"])
    print("relative cup:",results["compact_relative_cup"]["cup_product_integral"])
    print("unification scale:",results["two_split_SU5_threshold"]["formal_unification_MU_GeV"])
    print("Q at eta.45:",results["photon_memory_capacity"]["unassisted_Q_of_pure_qutrit_erasure"])
    print(output)
    return results

if __name__=="__main__": main()
