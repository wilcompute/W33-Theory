"""TOE physics dependency audit: test what finding X genuinely unlocks.

Six executable gates:
1 E8 GS shifts live in Higgs charge lattice; index4 is Spin10 center.
2 Signed 3-layer causal expectation is finite BUT fails Box(s)=-8.
3 Localized Yukawa/M2-action hierarchy scales without claiming real geometry.
4 SU5 orbifold flavor parity cannot split triplet/octet counts without new term.
5 Single-photon mode Hilbert dimension and efficient passive simulation.
6 Explicit dependency DAG scores and minimum physical closure targets.
Not a completed TOE or a derived compactification.
"""
from pathlib import Path
from math import pi, sqrt, exp, log
from itertools import product
import json
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from scipy.integrate import quad
from toe_20261119_balanced_source_E8_cup_gate import sector_census
from toe_20261119_uv_messenger_orbifold_causal_vacuum_followup import e8_renormalizable_messenger_completion
from toe_20261119_two_GS_axions_causal_layer_and_Bell_gates import global_e8_anomaly_two_axions
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_TOE_dependency_first_gate_bridge.json"

def e8_GS_Higgs_center_bridge():
    sectors,fields,_=sector_census()
    model=e8_renormalizable_messenger_completion()
    Q=sp.Matrix(model["field_charges"])
    H=smith_normal_form(Q,domain=sp.ZZ)
    invariants=[abs(int(H[i,i])) for i in range(3)]
    assert invariants==[1,1,4]
    ax1=sp.Matrix([[2,1,1]])
    ax2=sp.Matrix([[0,1,-5]])
    s=Q.row(3)
    assert s==ax1
    assert -2*Q.row(0)+4*Q.row(2)-Q.row(3)==ax2
    K=Q.col_join(ax1).col_join(ax2)
    HK=smith_normal_form(K,domain=sp.ZZ)
    combined=[abs(int(HK[i,i])) for i in range(3)]
    assert combined==invariants
    # Q lies in index-4 lattice: q1+q2+q3 == 0 (mod4).
    assert all(sum(int(Q[i,j]) for j in range(3))%4==0 for i in range(Q.rows))
    assert (sum(ax1)%4)==0 and (sum(ax2)%4)==0
    center={}
    for representation in (16,10,1):
        qs=[list(map(int,q)) for dd,q,name in fields if dd==representation]
        residues=sorted(set(sum(q)%4 for q in qs))
        assert len(residues)==1
        center[str(representation)]={"sum_charge_mod4":residues[0],
                                    "Z4_phase_power_i":residues[0],
                                    "multiplet_count":len(qs)}
    assert center["16"]["sum_charge_mod4"]==1
    assert center["10"]["sum_charge_mod4"]==2
    assert center["1"]["sum_charge_mod4"]==0
    cubic=global_e8_anomaly_two_axions()
    assert cubic["two_axion_exact_factorization_residual"]=="0"
    return {
        "eight_Higgs_charge_matrix":model["field_charges"],
        "Higgs_Smith_invariants":invariants,
        "two_GS_shift_charge_vectors":[[2,1,1],[0,1,-5]],
        "GS_shift1_exact_Higgs_phase":"theta_D, D=S14 with q=(2,1,1)",
        "GS_shift2_exact_Higgs_phase":"-2 theta_A +4 theta_C -theta_D",
        "combined_Higgs_plus_GS_Smith_invariants":combined,
        "lattice_character_constraint":"q1+q2+q3 == 0 mod 4 for every Higgs and GS shift row",
        "representation_residues":center,
        "center_interpretation":"Generator exp(2pi i (q1+q2+q3)/4) acts as i on Spin10 16, -1 on 10, 1 on singlets. This is the standard Spin10 center action under the global (Spin10 x SU4)/Z4 identification, NOT automatically a new physical Z4 nor the protective Z4^R.",
        "mathematical_unlocked":"Two necessary GS shift vectors can be expressed as integral combinations of phases of existing nonzero singlet VEVs; no independent arbitrary charge sectors required at charge-lattice level.",
        "physical_remaining":"Effective anomalous Wess-Zumino couplings, axion kinetic/Stueckelberg terms, covariant quantization, global quotient, anomaly inflow, R symmetry and 11D geometric origin are not derived. Higgs phases alone never prove quantum anomaly cancellation."
    }

def causal_wave_operator_failure():
    # Flat Minkowski (-,+,+,+): s=t^2-r^2, Box(s)=-2-6=-8.
    # The previous signed causal count has w=(1,-5,4), k=0..2.
    # Analytic interval-layer expectation at origin over future 0<t<1.
    kappa=pi/24
    def g(s):
        if s==0:return 1.
        if s>=1:return 0.
        z=sqrt(1-s)
        return z-s*log((1+z)/sqrt(s))
    def weight(z):return exp(-z)*(1-5*z+2*z*z)
    def signal(rho,monomial_power):
        f=lambda s:pi*rho*weight(rho*kappa*s*s)*g(s)*(s**monomial_power)
        return quad(f,0,1,epsabs=4e-10,epsrel=3e-10,limit=260)[0]
    rows=[]
    for rho in (40,160,640,2560,10240,40960,163840,1000000):
        const=signal(rho,0);interval=signal(rho,1)
        rows.append({"density":rho,"weighted_constant":const,
                     "weighted_s_t2_minus_r2":interval,
                     "putative_Box_s_value_after_only_subtracting_center_3f0":interval})
    assert abs(rows[-1]["weighted_constant"]-3)<.004
    assert abs(rows[-1]["weighted_s_t2_minus_r2"])<.105
    assert all(abs(rows[j+1]["weighted_s_t2_minus_r2"])<
               abs(rows[j]["weighted_s_t2_minus_r2"]) for j in range(2,len(rows)-1))
    # Leading O(rho^0) of weighted s moment cancels because sum w =0.
    # The remaining s*g(s) next term is O(log(rho)/sqrt(rho)).
    import sympy as sp
    weights=sp.Matrix([1,-5,4])
    assert sum(weights)==0
    m0=sp.Matrix([1,sp.Rational(1,2),sp.Rational(3,8)])
    assert m0.dot(weights)==0
    return {
      "region":"3+1 Minkowski future cone 0<t<1; finite Poisson sprinkling density rho",
      "probe_field":"s=t^2-x^2-y^2-z^2, f(origin)=0",
      "continuum_metric_signature":"(-,+,+,+)",
      "continuum_Box_on_probe":-8,
      "signed_layer_weights":[1,-5,4],
      "numerical":rows,
      "constant_limit":3,
      "s_probe_limit":0,
      "asymptotic_s_probe":"O(log(rho)/sqrt(rho)) ->0 from leading moment cancellation; zero-center term cannot rescue it.",
      "negative_result":"Finite signed count on f=constant DOES NOT yield a correctly normalized d'Alembertian. In the given unrescaled operator limit the nonharmonic s=t²-r² has limit0 while Box(s)=-8. Requires extra operator normalization, renormalization/mesoscale and more test fields.",
      "not_a_no_go":"One can rescale, change weights, add higher layers, or use the proven independent causal-set operators. This test only invalidates interpreting this particular finite signed expectation as an Einstein/Box derivation."
    }

def Yukawa_geometry_action_target():
    model=e8_renormalizable_messenger_completion()
    spur=np.array(model["formal_rank3_diagonal_dimensionless_masses_with_lambda_equals_one"])
    sr=float(max(spur)/min(spur))
    target=1e5
    R=target/sr
    DeltaS=log(R)
    separation=sqrt(3*DeltaS)
    # Gaussian triple-overlap of profiles centered at (0,0,d):
    # integral exp(-sum_j |x-xj|²/2sig²) / coincident integral
    # =exp(-d²/(3sig²)).
    assert abs(exp(-separation**2/3)-1/R)<1e-12
    # Could instead obtain the same suppression from M2 instanton actions
    # with equal unknown prefactors: exp(-Delta Vol/l11³).
    # No volume/sigma is derived by the 4D EFT.
    return {
        "source_spurion_factors":spur.tolist(),
        "spurion_max_min_ratio":sr,
        "illustrative_family_hierarchy_target":target,
        "minimum_unknown_overlap_times_Higgs_projection_ratio":R,
        "dimensionless_Euclidean_M2_action_difference_if_equal_prefactors":DeltaS,
        "Gaussian_triple_overlap_required_displacement_in_widths":separation,
        "Gaussian_exact_ratio":"exp(-d^2/(3 sigma^2)) for three equal-width nonnormalized profiles at x1=x2=0,x3=d",
        "minimal_geometric_task":"Derive distinct instanton actions or localized Dirac-mode overlap integrals in the REAL compact singular G2 geometry; identify the two Spin10 10_H light-doublet projections.",
        "critical_caveat":"This is an inverse engineering target. Neither Gaussian positions/widths nor M2 volumes, prefactors, Kähler metrics or SM masses follow from E8 source data. Original ordinary S3 bulk cup=0."
    }

def orbifold_reps_and_boundary_mass():
    # SM-preserving boundary involution on SU5 gauge part:
    # P=diag(+,+,+,-,-), acts + on BOTH su3 and su2 adjoints.
    # Any extra flavor parities F0,Fpi shared by the adjoint components
    # therefore leave identical plus-plus flavor subspaces.
    F0=np.diag([1,1,-1])
    Fpi=np.diag([1,-1,1])
    common=int(np.linalg.matrix_rank(np.column_stack([
       np.eye(3)[:,j] for j in range(3) if
       np.all(F0@np.eye(3)[:,j]==np.eye(3)[:,j]) and
       np.all(Fpi@np.eye(3)[:,j]==np.eye(3)[:,j])
    ])))
    assert common==1
    # Two simple identical zero-mode adjoints -> two triplets,two octets.
    # After SU5 broken on a boundary, an SM-invariant Majorana octet
    # boundary mass is allowed, while a triplet mass can be separately
    # selected. This is only a low-energy EFT algebraic model.
    MKK=1e13
    octet=np.diag([1e5,MKK])
    trip=np.diag([1e7,1e7])
    assert sum(np.diag(octet)<1e6)==1
    assert sum(np.diag(trip)<1e8)==2
    return {
      "inner_SU5_boundary_involution":[1,1,1,-1,-1],
      "shared_flavor_parity_example":{"F0":F0.diagonal().tolist(),"Fpi":Fpi.diagonal().tolist(),"common_plusplus_dim":common},
      "exact_same_count_theorem":"For any common flavor involutions F0,Fpi, both su3 and su2 adjoint components of SU5 have gauge parity + at both boundaries, so their zero-mode flavor spaces are identical. Parities alone cannot produce 2 triplets and 1 octet.",
      "low_energy_octet_boundary_mass_example_GeV":np.diag(octet).tolist(),
      "low_energy_triplet_mass_example_GeV":np.diag(trip).tolist(),
      "one_octet_two_triplets_example":True,
      "needed_new_physics":"An SU5-breaking brane-localized color-octet Majorana mass operator or representation-specific boundary dynamics (not mere shared flavor parities). Its coefficient and full KK eigenvalue problem are still inputs.",
      "important_limit":"Boundary operator is gauge invariant under SM on an SU5-broken boundary, but no 5D Dirac boundary-value problem, proton rate, 5D anomaly or two-loop full spectrum is solved."
    }

def one_photon_information_capacity():
    modes=[40,240,1024,4096,65536]
    rows=[]
    for d in modes:
        k=d.bit_length()-1
        assert 2**k<=d<2**(k+1)
        rows.append({"orthogonal_one_photon_modes":d,"dimension":d,
                     "qubits_max_by_subspace_dimension":k,
                     "complex_amplitude_storage":d,
                     "dense_gate_classical_complex_multiply_bound":d*d})
    # Apply 600 deterministic passive 2-mode Givens beam splitters
    # to a single-photon 240-mode amplitude vector and retain norm exactly.
    d=240
    rng=np.random.default_rng(20261119)
    psi=np.zeros(d,complex);psi[0]=1.
    for step in range(600):
        a,b=rng.choice(d,size=2,replace=False)
        theta=float(rng.uniform(-pi,pi));phi=float(rng.uniform(-pi,pi))
        ca=np.cos(theta);sa=np.sin(theta);phase=np.exp(1j*phi)
        va,vb=psi[a],psi[b]
        psi[a]=ca*va+phase*sa*vb
        psi[b]=-phase.conjugate()*sa*va+ca*vb
    norm=float(np.vdot(psi,psi).real)
    assert abs(norm-1)<1e-12
    return {
      "mode_table":rows,
      "40_mode_qubit_upper_bound":5,
      "240_mode_qubit_upper_bound":7,
      "n_logical_qubits_require_at_least_2_power_n_modes":"exact Hilbert dimension bound for one photon in d orthogonal modes",
      "240_mode_600_passive_gate_simulator_final_norm":norm,
      "classical_simulation":"One complex amplitude per optical mode; passive beam splitters and phase shifters update a length-d vector in O(d) or O(d²) for a dense interferometer. Polynomial in d, not guaranteed polynomial in encoded n.",
      "limits":"Temporal/OAM/polarization modes ALL count if orthogonal; adaptive multi-photon resources, nonlinear media, squeezed states, postselection, active feedforward and exotic Hilbert structures require separate accounting. Known multi-rail no-scaling limitation, not an impossibility theorem for ALL photonic QC."
    }

def photon_falsifier_resource_budget():
    # Predeclared hypothetical DIFFERENCE, NOT a prediction of any TOE.
    # One fixed setting with Bernoulli null p0=.50 and alternative p1=.51;
    # two-sided familywise alpha=0.001 (upper-tail threshold alpha/2).
    # We report the upward alternative's exact binomial power.
    from scipy.stats import binom
    n=55000;p0=.5;p1=.51;alpha=.001
    k=int(binom.isf(alpha/2,n,p0))
    false_pos_upper=float(binom.sf(k,n,p0))
    power=float(binom.sf(k,n,p1))
    false_pos_both=2*false_pos_upper
    herald=.5*(.8**2)*(.7**2)
    emissions=n/herald
    assert false_pos_both<alpha
    assert power>.90
    assert abs(herald-.1568)<1e-12
    return {
      "null_event_probability_assumed":p0,
      "hypothetical_nonstandard_probability_assumed_NOT_DERIVED":p1,
      "detected_event_probability_difference":p1-p0,
      "detected_successful_events_in_preregistered_fixed_setting":n,
      "two_sided_typeI_budget":alpha,
      "upper_binomial_rejection_condition":"count > "+str(k),
      "exact_upper_null_tail":false_pos_upper,
      "upper_alternative_power":power,
      "two_sided_null_tail_for_symmetric_p0":false_pos_both,
      "ideal_event_ready_heralded_acceptance_with_two_photons":herald,
      "expected_emitted_photon_pairs_at_assumed_acceptance":emissions,
      "important":"This is a power/resource budget for a posited p=.51, NOT a prediction of a TOE. If the physical model predicts ordinary QM p=.50, this experiment cannot distinguish it at any sample size. No independent full detection closure, source drift, calibration or multiple-setting correction is included."
    }


def dependency_DAG():
    # Auditable non-unique prioritization graph: edges prereq -> deliverable.
    # Node statuses describe current evidence, not subjective truth.
    stages={
       "compact_G2_geometry":"unbuilt",
       "source_chiral_index":"conditional_verified",
       "axion_inflow":"unbuilt",
       "full_anomaly_freedom":"unbuilt",
       "defect_Yukawa_integrals":"unbuilt",
       "charged_SM_masses":"unbuilt",
       "GUT_boundary_action":"toy_parity_only",
       "GUT_full_spectrum":"unbuilt",
       "UV_causal_action":"unbuilt",
       "metric_and_dimensional_limit":"unbuilt",
       "Einstein_constraints":"unbuilt",
       "quantum_time_generator":"unbuilt",
       "selected_quantum_state":"unbuilt",
       "process_tensor_prediction":"unbuilt",
       "falsifiable_test":"unbuilt",
       "physical_TOE_completion":"unbuilt"}
    edges=[
      ("compact_G2_geometry","source_chiral_index"),
      ("compact_G2_geometry","axion_inflow"),
      ("compact_G2_geometry","defect_Yukawa_integrals"),
      ("source_chiral_index","full_anomaly_freedom"),
      ("axion_inflow","full_anomaly_freedom"),
      ("defect_Yukawa_integrals","charged_SM_masses"),
      ("full_anomaly_freedom","charged_SM_masses"),
      ("GUT_boundary_action","GUT_full_spectrum"),
      ("charged_SM_masses","physical_TOE_completion"),
      ("GUT_full_spectrum","physical_TOE_completion"),
      ("UV_causal_action","metric_and_dimensional_limit"),
      ("metric_and_dimensional_limit","Einstein_constraints"),
      ("Einstein_constraints","physical_TOE_completion"),
      ("UV_causal_action","quantum_time_generator"),
      ("quantum_time_generator","selected_quantum_state"),
      ("selected_quantum_state","process_tensor_prediction"),
      ("process_tensor_prediction","falsifiable_test"),
      ("falsifiable_test","physical_TOE_completion")]
    adj={k:[] for k in stages}
    for a,b in edges:adj[a].append(b)
    def descendants(v,stack=()):
        assert v not in stack,"dependency cycle"
        ans=set()
        for w in adj[v]:
            ans.add(w);ans.update(descendants(w,stack+(v,)))
        return ans
    influence={k:len(descendants(k)) for k in stages}
    # Top score is geometry, causal microdynamics; do not make the entire
    # project hostage to ONE branch. Two independent experimentally testable
    # research trunks should progress in parallel.
    assert influence["compact_G2_geometry"]>=5
    assert influence["UV_causal_action"]>=5
    return {"nodes":stages,"edges":[list(x) for x in edges],
            "descendant_counts":influence,
            "first_particle_gate":"Construct exact compact source/defect geometry WITH two quantized GS axionic couplings and nonzero physical Yukawa integrals. Reject model before a mass fit if the global gauge/anomaly structure fails.",
            "first_gravity_gate":"Specify microscopic exchange action AND its continuum time/metric generator, then test the wave operator on constant, linear and quadratic fields. Reject candidate before claiming Einstein equations if Box(s) fails.",
            "computing_gate":"Account for exponential single-photon mode growth before claiming scalable BQP at polynomial hardware resources.",
            "logical_qualification":"A project-planning DAG with explicit assumptions and no unique objectively derived ranking. Several branches are independent, so pursuing one gate does not automatically derive every other part of the TOE."}

def main():
    out={
      "E8_GS_Higgs_center_lattice":e8_GS_Higgs_center_bridge(),
      "causal_signed_wave_operator_falsifier":causal_wave_operator_failure(),
      "localized_M2_Yukawa_target":Yukawa_geometry_action_target(),
      "orbifold_boundary_flavor_no_go_and_escape":orbifold_reps_and_boundary_mass(),
      "single_photon_mode_capacity":one_photon_information_capacity(),
      "photonic_experimental_resource_budget":photon_falsifier_resource_budget(),
      "physics_dependency_DAG":dependency_DAG()
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("CENTER",out["E8_GS_Higgs_center_lattice"]["Higgs_Smith_invariants"])
    print("CAUSAL",out["causal_signed_wave_operator_falsifier"]["numerical"][-1])
    print("HIERARCHY_M2_DELTA",out["localized_M2_Yukawa_target"]["dimensionless_Euclidean_M2_action_difference_if_equal_prefactors"])
    print("DAG_FIRST",sorted(out["physics_dependency_DAG"]["descendant_counts"].items(),key=lambda kv:-kv[1])[:4])
    print(OUT)
    return out
if __name__=="__main__":main()
