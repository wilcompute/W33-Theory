"""TOE five-front stress tests: source Higgs rescue, Z7 Wilson incompatibility,
SUSY GUT threshold budget, BDG4 Poisson noise, photonic fault/resource scaling.
Finite conditional models, NOT a physical G2 compactification or a TOE.
"""
import json
from pathlib import Path
from math import pi,sqrt,log,comb
from itertools import combinations
import numpy as np
import sympy as s
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_uv_messenger_orbifold_causal_vacuum_followup import e8_renormalizable_messenger_completion
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261119_two_ten_Wilson_BDG_noise_photon_certificate.json"

def two_ten_Higgs():
    secs,_,_=sector_census();old=e8_renormalizable_messenger_completion()
    cs={x["label"]:np.array(x["SU4_charge"],int) for x in secs}
    Q=dict(zip(old["charged_field_order"],[np.array(x,int) for x in old["field_charges"]]))
    vevs=dict(zip(old["charged_field_order"],np.sqrt(old["singlet_squared_vevs"])))
    qh=cs["16_1"]
    ops=[("16H² 10_34","10_34",2,["B"]),
         ("bar16H² 10_34","10_34",-2,["C","D"]),
         ("16H² 10_24","10_24",2,["E","G1"]),
         ("bar16H² 10_24","10_24",-2,["A","D"])]
    for name,ten,sign,ins in ops:
        z=sign*qh+cs[ten]+sum((Q[x] for x in ins),np.zeros(3,int))
        assert np.array_equal(z,np.zeros(3,int)),(name,z)
    v=1.5;M=10.
    a=v*vevs["B"]/M;b=v*vevs["C"]*vevs["D"]/M**2
    c=v*vevs["E"]*vevs["G1"]/M**2;d=v*vevs["A"]*vevs["D"]/M**2
    mass=np.array([[0,a,c],[b,0,0],[d,0,0]],float)
    right=np.array([0,c,-a])/np.hypot(a,c)
    left=np.array([0,d,-b])/np.hypot(b,d)
    assert np.linalg.matrix_rank(mass)==2
    assert np.linalg.norm(mass@right)<1e-12 and np.linalg.norm(left@mass)<1e-12
    assert right[1]!=0 and left[1]!=0
    assert np.array_equal(cs["16_1"]+cs["16_2"]+cs["10_34"],np.zeros(3,int))
    # 19 singlets (rank16) + 16+bar16+driver+2 real tens (rank22).
    active=19+16+16+1+20
    hessian=old["full_superpotential_Hessian_rank"]+22
    gauge=3+21;physical=active-hessian-gauge
    assert (active,hessian,gauge,physical)==(72,38,24,10)
    return {"operators":[{"name":n,"singlets":f} for n,t,z,f in ops],
      "mass_row_order":["H16_bar5","10_34_bar5","10_24_bar5"],
      "mass_column_order":["bar16H_5","10_34_5","10_24_5"],
      "mass_matrix":mass.tolist(),"mass_rank":2,
      "light_5_components":right.tolist(),"light_bar5_components":left.tolist(),
      "projection_10_34_5_abs":float(abs(right[1])),
      "projection_10_34_bar5_abs":float(abs(left[1])),
      "active_chiral_components":active,"hessian_rank":hessian,
      "broken_complex_gauge_dimension":gauge,"physical_massless_chiral_components":physical,
      "massless_representation":"one complete SU5 5+bar5; colored triplets remain",
      "family_16_1_and_Higgs_16H_same_charges":True,
      "old_discrete_Z4R_gravitational_parity":int(old["five_R2_drivers_gravitational_Z4R_mod2_from_prior_minimal_spectrum"]),
      "new_two_R0_spinors_one_R2_driver_parity_shift":(-16-16+1)%2,
      "combined_discrete_Z4R_gravitational_parity_without_additional_inflow":(int(old["five_R2_drivers_gravitational_Z4R_mod2_from_prior_minimal_spectrum"])-16-16+1)%2,
      "gauge_allowed_unsuppressed_16_1_16_2_10_34":True,
      "limits":"Four operators gauge allowed but actual strict punctured S3 bulk cup vanishes. Missing mirror 16H and overlap coefficients, global anomaly inflow, SM doublet splitting, physical Higgs VEV and family mixing control."}

def W7_characters():
    w=[2,2,2,4,4]
    table=[]
    for ch in range(7):
        a=[(x+ch)%7==0 for x in w];b=[(-x+ch)%7==0 for x in w]
        table.append({"character":ch,"five_color":sum(a[:3]),"five_weak":sum(a[3:]),
                      "barfive_color":sum(b[:3]),"barfive_weak":sum(b[3:])})
    assert (table[0]["five_weak"],table[0]["barfive_weak"])==(0,0)
    assert table[3]["five_weak"]==2 and sum(table[3][k] for k in ("five_color","barfive_color","barfive_weak"))==0
    assert table[4]["barfive_weak"]==2 and sum(table[4][k] for k in ("five_color","barfive_color","five_weak"))==0
    spinor=[0]+[(w[i]+w[j])%7 for i,j in combinations(range(5),2)]+[(-x)%7 for x in w]
    assert len(spinor)==16 and sum(z==0 for z in spinor)==1
    return {"order":7,"W_diagonal_exponents":w,"ten_vector_character_table":table,
      "untwisted_16_invariant_components":1,"trivial_character_10_has_no_weak_doublets":True,
      "characters_to_get_one_weak_five_and_bar_five":[3,4],
      "global_constant_zero_mode_clash":"If Spin10 singlet Higgs and B,C,D,E,G1,A spurion VEVs have trivial constant C7 character, each A²10 dressed mass term requires 10 character zero, while a surviving weak 5 needs character3 and weak bar5 needs character4. Thus cannot combine pre-Wilson 72-field mass matrix with a naive constant-flat-section Wilson projection.",
      "required_escape":"Real C7-supporting compact singular gauge locus, nonconstant defect/brane profiles or genuinely twisted local coefficients and exact chiral cohomology. Earlier L4 base does not support C7.",
      "limitation":"Flat constant global sections only; nontrivial localized modes and boundary defects could evade it."}

def interval_5D_Dirac_boundary_spectrum():
    """Solve a first-order Dirac interval spectral proxy, not a 5D Majorana GUT."""
    from math import atan,cos,sin
    samples=[]
    for mu in (0,0.01,1,10,100):
        roots=[atan(mu)+k*pi for k in range(3)]
        x=roots[0]
        # fL'= -m fR, fR'=m fL; fR(0)=0 and fR(L)=mu fL(L).
        assert abs(sin(x)-mu*cos(x))<1e-12
        samples.append({"brane_ratio_h":mu,"first_3_positive_masses_times_L":roots,
                        "first_mode_left_boundary_amplitude":1,
                        "first_mode_right_boundary_amplitude":0})
    assert samples[-1]["first_3_positive_masses_times_L"][0]>1.56
    return {"Dirac_first_order_equations":"fL'=-m fR, fR'=m fL on 0<y<L",
       "boundary_conditions":"fR(0)=0, fR(L)=h fL(L), real h",
       "mass_quantization":"m_n L=atan(h)+n*pi (n=0,1,...); h dimensionless",
       "test_cases":samples,
       "two_triplets_one_octet_toy_parameters":{"triplet_1_h":0,"triplet_2_h":0,
                                             "octet_1_h":0,"octet_2_h":100},
       "one_octet_lifted_near_half_KK_scale":True,
       "physical_warning":"A first-order two-profile Dirac boundary-value calculation only. It does NOT derive a supersymmetric 5D adjoint Majorana brane action, exact chirality, global gauge anomalies, KK threshold matching or proton decay; h=100 is inserted."}


def GUT_thresholds():
    dbl=s.Matrix([s.Rational(3,5),1,0]);trip=s.Matrix([s.Rational(2,5),0,1])
    assert dbl+trip==s.ones(3,1)
    L=log(2e16/1e3)/(2*pi)
    diff=[-float(dbl[i]-dbl[j])*L for i,j in ((0,1),(0,2),(1,2))]
    return {"extra_N1_doublet_chiral_pair_beta":[str(x) for x in dbl],
      "extra_N1_triplet_chiral_pair_beta":[str(x) for x in trip],
      "full_SUSY_5_plus_bar5_beta":[str(x) for x in dbl+trip],
      "illustrative_threshold_mass_doublet_triplet_GeV":[1000,2e16],
      "one_loop_delta_inverse_alpha_differences_12_13_23":diff,
      "limits":"Not a full 5D Dirac boundary eigenproblem, complete two-loop RGE, proton-lifetime prediction, or derivation of a physical Higgs. Do not double-count MSSM Higgs doublets."}

def BDG4_noise():
    rng=np.random.default_rng(20261119);out=[]
    for rho,trials in [(20,350),(50,300),(100,200)]:
        ks=[];nn=[]
        for _ in range(trials):
            n=int(rng.poisson(rho*pi/3));nn.append(n)
            t=rng.random(n)**.25;r=t*rng.random(n)**(1/3)
            z=2*rng.random(n)-1;phi=2*pi*rng.random(n)
            sphi=np.sqrt(1-z*z)
            xyz=np.column_stack((r*sphi*np.cos(phi),r*sphi*np.sin(phi),r*z))
            dt=t[:,None]-t[None,:]
            dx=np.sum((xyz[:,None,:]-xyz[None,:,:])**2,axis=2)
            cnt=np.sum((dt>0)&(dt*dt>dx),axis=1)
            weights=[1,-9,16,-8]
            ks.append(sum(weights[int(k)] for k in cnt if k<4))
        K=np.array(ks,float);B=(4*sqrt(rho)/sqrt(6))*(K-1)
        out.append({"rho":rho,"trials":trials,"mean_events":float(np.mean(nn)),
                    "expected_events":rho*pi/3,"mean_BDG4_constant":float(B.mean()),
                    "sd_BDG4_constant":float(B.std(ddof=1)),
                    "five_to_95_percent":np.percentile(B,[5,95]).tolist(),
                    "std_error_of_mean":float(B.std(ddof=1)/sqrt(trials))})
    assert all(x["sd_BDG4_constant"]>100 for x in out)
    return {"method":"Independent full 4D Minkowski future-cone Poisson sprinkling per trial. Count all causal interior events for each origin-to-event interval, then apply exactly 1,-9,16,-8 and B=4sqrt(rho)/sqrt6*(K-1).",
       "data":out,"warning":"The correct BDG4 continuum expectation need not imply small shot-to-shot fluctuations. The trial mean has substantial standard error; no quantum graviton or selected physical state is derived."}

def photonic_resources():
    tab=[]
    for n in (4,8,20,50):
        D=comb(3*n-1,n);code=2**n
        assert D>=code
        tab.append({"logical_qubits":n,"photons":n,"modes":2*n,
                    "dual_rail_code_dimension":code,"full_fixed_photon_Fock_dimension":D,
                    "all_survive_eta_0p9":.9**n,
                    "n_heralded_0p75_gates_all_succeed":.75**n,
                    "combined_naive_success":(.9*.75)**n})
    k=51/49;assert abs(k/(1+k)-.51)<1e-12
    return {"dual_rail_n_photon_vs_single_photon_mode_tradeoff":tab,
       "relative_success_acceptance_odds_bias_to_fake_p0p5_as_p0p51":k,
       "known_2026_nonGaussian_resource":"Heralded four-dimensional OAM photon-photon controlled-phase gate, Nature Photonics (2026), https://www.nature.com/articles/s41566-026-01846-x",
       "scope":"Mode economy requires n photons and active entangling resources; naive loss and gate postselection remain exponentially bad. No new quantum-vs-classical probability prediction; 4.08% relative acceptance bias mimics 1% absolute signal."}

def run():
    result={"two_ten_light_Higgs":two_ten_Higgs(),"Z7_Wilson_zero_mode_test":W7_characters(),
      "GUT_threshold_budget":GUT_thresholds(),"GUT_5D_Dirac_interval_toy":interval_5D_Dirac_boundary_spectrum(),"causal_BDG4_Poisson_variance":BDG4_noise(),
      "photon_modes_heralding":photonic_resources()}
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    for k in result:print("PASS",k)
    print("LIGHT_Higgs_X34",result["two_ten_light_Higgs"]["projection_10_34_5_abs"],result["two_ten_light_Higgs"]["projection_10_34_bar5_abs"])
    print("BDG_STD",[(x["rho"],x["sd_BDG4_constant"]) for x in result["causal_BDG4_Poisson_variance"]["data"]])
    print(OUT)
    return result
if __name__=="__main__":run()
