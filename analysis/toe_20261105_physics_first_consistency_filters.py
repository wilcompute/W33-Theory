#!/usr/bin/env python3
"""TOE physical consistency filters: anomaly, causal dimension, Fock locality, speeds.

These are independent physics controls, NOT W33-derived, NOT a TOE solution.
Novelty is the explicit cross-domain rejection suite, not its component laws.
"""
from __future__ import annotations
import itertools,json,math
from functools import reduce
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln
from sympy import symbols, factor
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_physics_first_consistency_filters.json"

def anomalies():
    q,h,l=symbols("q h l")
    u,d,e,n=-q-h,-q+h,-l+h,-l-h
    su3=factor(2*q+u+d)
    su2=factor(3*q+l)
    grav=factor(6*q+3*u+3*d+2*l+e+n)
    cubic=factor(6*q**3+3*u**3+3*d**3+2*l**3+e**3+n**3)
    assert su3==0 and grav==0
    assert su2==3*q+l
    assert cubic==-6*h*h*(3*q+l)
    noNgrav=factor((grav-n).subs(l,-3*q))
    noNcubic=factor((cubic-n**3).subs(l,-3*q))
    assert factor(noNgrav-(h-3*q))==0 and factor(noNcubic-(h-3*q)**3)==0
    def charges(a,b):
        return (a,-a-b,-a+b,-3*a,3*a+b,3*a-b)
    def checker(c):
        Q,U,D,L,E,N=c
        return {
            "SU3_squared_U1":2*Q+U+D,
            "SU2_squared_U1":3*Q+L,
            "gravitational_U1":6*Q+3*U+3*D+2*L+E+N,
            "U1_cubed":6*Q**3+3*U**3+3*D**3+2*L**3+E**3+N**3}
    grid=[]
    for a,b in itertools.product(range(-3,4),repeat=2):
        c=charges(a,b)
        assert all(v==0 for v in checker(c).values())
        grid.append((a,b))
    from fractions import Fraction
    y=charges(Fraction(1,6),Fraction(1,2))
    bl=charges(Fraction(1,3),Fraction(0))
    assert y==(Fraction(1,6),Fraction(-2,3),Fraction(1,3),
               Fraction(-1,2),Fraction(1),Fraction(0))
    assert bl==(Fraction(1,3),Fraction(-1,3),Fraction(-1,3),
                Fraction(-1),Fraction(1),Fraction(1))
    # Witten SU2 global anomaly: 3 quark LH doublets + 1 lepton=4 even
    assert (3+1)%2==0
    return {"status":"PASS",
        "representation":"one generation all left-handed Weyl Q,u^c,d^c,L,e^c,N^c, one Higgs H",
        "Yukawa_charges":{"u":"-q-h","d":"-q+h","l":"-3q",
             "e":"3q+h","n":"3q-h"},
        "cubic_before_SU2_constraint":str(cubic),
        "SU3_and_mixed_gravity_cancel_before_SU2":True,
        "SU2_constraint":"l=-3q",
        "SU2_doublets":4,"Witten_anomaly_cancelled":True,
        "one_generation_anomaly_free_integer_grid_cases":len(grid),
        "anomaly_free_charge_basis":"X = alpha*Y_SM + beta*(B-L), alpha=2h, beta=3q-h",
        "SM_Y_basis":[str(x) for x in y],
        "BL_basis":[str(x) for x in bl],
        "without_N_gravity_anomaly":str(noNgrav),
        "without_N_cubic_anomaly":str(noNcubic),
        "with_N_Majorana_mass_requires":"n=3q-h=0 => h=3q",
        "no_unique_hypercharge_with_N_without_extra_input":True}

def minimal_chiral():
    # True chiral: no 0 charge and no +/- opposing pair, modulo global sign.
    solutions=[]
    qset=[x for x in range(-9,10) if x]
    for c in itertools.combinations_with_replacement(qset,5):
        if sum(c) or sum(x**3 for x in c):continue
        if any(-x in c for x in c):continue
        if reduce(math.gcd,(abs(x) for x in c))!=1:continue
        if tuple(c)>tuple(sorted(-x for x in c)):continue
        solutions.append(c)
    assert solutions==[(-9,-5,-1,7,8)],solutions
    # For 3 left-handed Weyl U1 charges, sum q=0 and sum q^3=3 q1 q2 q3.
    # For 4, if q4=-(q1+q2+q3), sum q^3 =
    # -3(q1+q2)(q1+q3)(q2+q3): an opposite pair is necessary.
    return {"status":"PASS","primitive_chiral_five_fermion_solutions_maxabs_le9":solutions,
     "no_primitive_chiral_five_charge_set_maxabs_le8":True,
     "no_n_le4_nonvectorlike_integer_anomaly_free_multiplet":"algebraic sum/cubic factorization",
     "physical_boundary":"4D local U1 anomaly cancellation is necessary, not a lattice measure, mass mechanism or global anomaly check."}

def ordering_theory(d):
    return float(math.exp(gammaln(d+1)+gammaln(d/2)-gammaln(1.5*d)-math.log(2)))

def sprinkle_interval(d,n,rng):
    # Uniform volume on the diamond between (0,0) and (1,0) of R^{1,d-1}.
    # Rejection on t with radial slice weight min(t,1-t)^(d-1).
    nd=d-1
    t=np.empty(n);x=np.empty((n,nd))
    done=0
    while done<n:
        m=4*(n-done)+32
        ti=rng.random(m)
        r=np.minimum(ti,1-ti)
        accept=rng.random(m)<(2*r)**nd
        pick=ti[accept][:n-done]
        k=len(pick)
        if not k:continue
        v=rng.normal(size=(k,nd))
        v/=np.linalg.norm(v,axis=1,keepdims=True)
        radii=np.minimum(pick,1-pick)*rng.random(k)**(1/nd)
        t[done:done+k]=pick
        x[done:done+k]=v*radii[:,None]
        done+=k
    return t,x

def causal_dimension():
    rows=[]
    for d in (2,3,4):
        rng=np.random.default_rng(20261105+23*d)
        empirical=[]
        for _ in range(16):
            t,x=sprinkle_interval(d,360,rng)
            dt=t[:,None]-t[None,:]
            dr2=np.sum((x[:,None,:]-x[None,:,:])**2,axis=2)
            related=(dt*dt>=dr2)&(dt!=0)
            R=int(np.triu(related,1).sum())
            empirical.append(2*R/(360*359))
        mean=float(np.mean(empirical))
        se=float(np.std(empirical,ddof=1)/math.sqrt(len(empirical)))
        estimate=float(brentq(lambda dd: ordering_theory(dd)-mean,1,7))
        assert abs(mean-ordering_theory(d))<max(.008,4*se)
        assert abs(estimate-d)<.16,(d,estimate)
        rows.append({"dimension_input":d,
          "sampled_interval_size_per_replicate":360,"replicates":16,
          "predicted_order_fraction":ordering_theory(d),
          "empirical_mean_order_fraction":mean,"replicate_standard_error":se,
          "reconstructed_dimension_from_mean":estimate})
    assert abs(ordering_theory(4)-.1)<1e-14
    return {"status":"PASS","data":rows,
      "assumption":"Minkowski Lorentzian causal cones imported to generate points; does NOT derive causal order or dimension from microscopic dynamics.",
      "theory":"Myrheim-Meyer dimension estimator in a flat Alexandrov interval."}

def one_photon_locality():
    # Bosonic 6 spatial modes, exactly one quantum: |j> = a_j^dagger|vac>.
    rng=np.random.default_rng(20261105)
    psi=rng.normal(size=6)+1j*rng.normal(size=6)
    psi/=np.linalg.norm(psi)
    nA=np.diag([1,1,1,0,0,0])
    nB=np.diag([0,0,0,1,1,1])
    assert np.linalg.norm(nA@nB)==0
    a=float(np.real(np.vdot(psi,nA@psi)))
    b=float(np.real(np.vdot(psi,nB@psi)))
    both=float(np.real(np.vdot(psi,nA@nB@psi)))
    assert abs(a+b-1)<1e-14 and both==0
    # A real two-excitation Fock state |1_A1,1_B4> has nA*nB=1.
    return {"status":"PASS","number_conserved_one_excitation":1,
       "spatial_modes":6,"A_occupancy":a,"B_occupancy":b,
       "A_and_B_coincidence":both,
       "two_excitation_A_and_B_coincidence":1,
       "no_go":"Passive one-excitation unitary evolution cannot generate joint local number-resolving detections in disjoint A and B.",
       "escape_routes":"Additional excitations, matter/environment ancilla, nonlinear particle conversion, or a mathematical encoding not interpreting logical counts as direct local photon clicks.",
       "boundary":"Does not exclude abstract time-bin high-dimensional qubit encodings; does exclude interpreting them as independent localized multiparticle Fock excitations under these assumptions."}

def speed_nonuniversality():
    # Local unitary/stable scalar finite difference with distinct spatial stiffnesses.
    spacing=1/40;dt=spacing/2
    kin=2*math.pi/19
    values=[]
    for species,v in (("A",1.0),("B",1.2)):
        def omega(k):
            return (2/dt)*math.asin((dt*v/spacing)*math.sin(k*spacing/2))
        ph=omega(kin)/kin
        group=(omega(kin+1e-4)-omega(kin-1e-4))/(2e-4)
        assert abs(group-v)<4e-5
        values.append({"species":species,"microscopic_local_speed_coefficient":v,
            "phase_speed_at_k_2pi_over19":ph,"group_speed_at_k_2pi_over19":group})
    assert abs(values[1]["group_speed_at_k_2pi_over19"]-
               values[0]["group_speed_at_k_2pi_over19"])>.199
    return {"status":"PASS","model":"two independent stable local scalar lattice Hamiltonians with different spatial stiffness",
        "species":values,
        "obstruction":"Locality, stable propagation and translation invariance by themselves do not require a shared limiting speed.",
        "required_additional_input":"Emergent Lorentz invariance/renormalization-group mechanism or exact unifying symmetry enforcing equal light cones.",
        "boundary":"A counterexample to an inference, not a demonstration that the real universe violates Lorentz symmetry."}

def gauge_running():
    # Illustrative PDG-era MSbar inputs at Z pole, three SM generations,
    # one Higgs doublet, no new thresholds, SU5 alpha1 normalization.
    mz=91.1876
    alpha_em_inv=127.955
    sin2=.23122
    alpha_s=.1180
    initial=[.6*(1-sin2)*alpha_em_inv,sin2*alpha_em_inv,1/alpha_s]
    betas=[41/10,-19/6,-7]
    pairs=[]
    for i,j in itertools.combinations(range(3),2):
        t=2*math.pi*(initial[i]-initial[j])/(betas[i]-betas[j])
        mu=mz*math.exp(t)
        vals=[initial[k]-betas[k]*t/(2*math.pi) for k in range(3)]
        assert abs(vals[i]-vals[j])<1e-12
        pairs.append({"groups":[i+1,j+1],"log_mu_over_MZ":t,
             "crossing_GeV":mu,"inverse_couplings_at_crossing":vals,
             "remaining_inverse_coupling_mismatch":max(vals)-min(vals)})
    assert pairs[0]["crossing_GeV"]<1.1e13
    assert pairs[1]["crossing_GeV"]>2e14
    assert pairs[2]["crossing_GeV"]>9e16
    assert len({round(x["log_mu_over_MZ"],2) for x in pairs})==3
    return {"status":"PASS",
      "model":"SU(3)xSU(2)xU(1) one-loop RG with minimal 3-generation 1-Higgs Standard Model field content",
      "inputs_at_MZ":{"MZ_GeV":mz,"alpha_EM_inverse_approx":alpha_em_inv,
           "sin_squared_thetaW_MSbar":sin2,"alpha_strong":alpha_s},
      "SU5_normalized_beta_coefficients":betas,
      "SU5_normalized_inverse_couplings_at_MZ":initial,
      "pairwise_crossings":pairs,"no_one_loop_triple_unification":True,
      "necessary_next_physics":"Nonminimal spectrum/thresholds and two-loop RG must be specified, with proton decay and neutrino constraints checked.",
      "boundary":"One-loop extrapolation only; no derived unification group, extra states, thresholds or direct new-particle prediction."}

def main():
    results={"schema":"toe.physics_first.consistency_filters.20261105",
      "status":"PASS_FIVE_INDEPENDENT_TOE_CONSISTENCY_FRONTS",
      "anomaly_and_hypercharge":anomalies(),
      "minimal_chiral_u1":minimal_chiral(),
      "causal_set_dimension":causal_dimension(),
      "one_photon_locality":one_photon_locality(),
      "universal_speed_guard":speed_nonuniversality(),
      "gauge_running_nonunification":gauge_running(),
      "epistemic_boundary":"Established physics constraints and reproducible finite benchmarks; none derives TOE, observed values of constants, E8 gauge dynamics or the Standard Model spectrum."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PHYSICS_CONTROLS_PASS",
       "anomaly_grid",results["anomaly_and_hypercharge"]["one_generation_anomaly_free_integer_grid_cases"],
       "causal_dimensions",[(x["dimension_input"],round(x["reconstructed_dimension_from_mean"],4))
                           for x in results["causal_set_dimension"]["data"]],
       "one_photon_joint",results["one_photon_locality"]["A_and_B_coincidence"],
       "charge5",results["minimal_chiral_u1"]["primitive_chiral_five_fermion_solutions_maxabs_le9"],
       flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return results
if __name__=="__main__":main()
