#!/usr/bin/env python3
"""2026-11-19: five integrated TOE physics gates plus a global center bridge.

1. A bounded causal interval's order complex is a cone (no H1 holonomy).
2. SU2 gauge covariance and F² limit DO NOT uniquely specify lattice action.
3. The SAME retarded Green function has distinct positive KMS noise spectra.
4. Exact three-layer poset entropy competes with an ALREADY EXISTING 4D Regge action.
5. SM Z6 global quotient + anomaly equations leave an integer hypercharge lattice.
6. Pure adjoint gauge dynamics loses center information seen by chiral doublets.

All results are conditional checks with imposed structures, not a TOE or
a derived 4D Einstein, Born, or Standard Model dynamical completion.
"""
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.special import iv

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_five_full_physics_gates_global_obstructions.json"
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261105_regge_s4_nonlinear_hessian as regge

def gf2rank(A):
    b=np.asarray(A,dtype=np.uint8).copy()%2
    row=0
    for j in range(b.shape[1]):
        if row==len(b):break
        nz=np.flatnonzero(b[row:,j])
        if len(nz)==0:continue
        k=row+int(nz[0])
        b[[k,row]]=b[[row,k]]
        for i in range(len(b)):
            if i!=row and b[i,j]:b[i]^=b[row]
        row+=1
    return row

def order_complex(V,cover):
    """Order complex of transitive closure of finite acyclic Hasse edges."""
    V=tuple(V)
    n=len(V)
    idx={x:i for i,x in enumerate(V)}
    R=np.zeros((n,n),bool)
    for a,b in cover:R[idx[a],idx[b]]=True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i,j]=bool(R[i,j] or (R[i,k] and R[k,j]))
    assert not np.diag(R).any()
    c={}
    for k in range(1,n+1):
        seq=[]
        for sub in itertools.combinations(range(n),k):
            if all(R[i,j] for i,j in itertools.combinations(sub,2)):
                seq.append(sub)
        if seq:c[k-1]=seq
    ranks={}
    for k in range(1,max(c)+1):
        larger=c.get(k,[])
        smaller=c.get(k-1,[])
        small_index={s:i for i,s in enumerate(smaller)}
        boundary=np.zeros((len(smaller),len(larger)),np.uint8)
        for col,simp in enumerate(larger):
            for sub in itertools.combinations(simp,k):
                boundary[small_index[sub],col]=1
        ranks[k]=gf2rank(boundary)
    betti={k:len(simp)-ranks.get(k,0)-ranks.get(k+1,0)
           for k,simp in c.items()}
    assert all(x>=0 for x in betti.values())
    return {"vertices":n,"simplex_counts":{str(k):len(simp) for k,simp in c.items()},
            "boundary_ranks":{str(k):v for k,v in ranks.items()},
            "betti":{str(k):v for k,v in betti.items()},
            "H1_mod2":betti.get(1,0)}

def causal_spin_gate():
    # A four-vertex crown has an order-complex cycle K2,2.
    crown=[(0,2),(0,3),(1,2),(1,3)]
    open_=order_complex(range(4),crown)
    # Bounded interval has both a first and a last causal event.
    bounded=[(0,1),(0,2),(1,3),(1,4),(2,3),(2,4),(3,5),(4,5)]
    full=order_complex(range(6),bounded)
    # Even a single canonical least event cones the entire order complex.
    with_min=order_complex(range(5),[(0,1),(0,2),(1,3),(1,4),(2,3),(2,4)])
    assert open_["H1_mod2"]==1
    assert full["betti"].get("0")==1 and all(
        v==0 for k,v in full["betti"].items() if int(k)>0)
    assert with_min["H1_mod2"]==0
    assert full["simplex_counts"]["3"]==4
    return {"status":"PASS","unbounded_crown":open_,
      "bounded_causal_interval":full,"with_unique_initial_event":with_min,
      "exact_proof":"If a finite poset has a least element, every chain simplex is a face of a simplex containing it; its order complex is a cone and all reduced homology vanishes. A greatest element works equally.",
      "spin_implication":"The full bounded interval order complex cannot carry nontrivial H1 spin holonomies. Noncontractible spin topology requires another construction (spatial covers, complements or globally nontrivial posets).",
      "scope":"Mod-2 homology of a selected finite poset, NOT a Lorentzian spin bundle, induced physical spin structure or global topology no-go for every causal set."}

def fundamental(theta):
    return float(1-np.cos(theta/2))

def adjoint_rescaled(theta):
    # Fundamental SU2 character 2 cos(theta/2); adjoint trace=1+2 cos(theta).
    # Normalize adjoint action by (3/8) to match fundamental theta²/8.
    return float((1-np.cos(theta))/4)

def gauge_action_uniqueness_gate():
    records=[]
    for theta in [1e-3,.05,.25,.7,1.4,math.pi,2*math.pi]:
        sf=fundamental(theta);sa=adjoint_rescaled(theta)
        assert abs(sa-(sf-.5*sf**2))<1e-13
        records.append({"theta":theta,"fundamental_S":sf,
          "adjoint_rescaled_S":sa,"S_adjoint_minus_S_f":sa-sf,
          "exact_quartic_identity_residual":sa-sf+.5*sf**2})
    eps=.001
    assert abs(fundamental(eps)/(eps*eps)-1/8)<1e-8
    assert abs(adjoint_rescaled(eps)/(eps*eps)-1/8)<5e-8
    assert abs(adjoint_rescaled(.7)-fundamental(.7))>.0003
    # At center -I2, adjoint character unchanged while fundamental detects sign.
    center_fund=fundamental(2*math.pi)
    center_adj=adjoint_rescaled(2*math.pi)
    assert abs(center_fund-2)<1e-13 and abs(center_adj)<1e-13
    # Different Euler-Lagrange forces away from the common weak-field limit.
    theta=.7;h=1e-6
    df=(fundamental(theta+h)-fundamental(theta-h))/(2*h)
    da=(adjoint_rescaled(theta+h)-adjoint_rescaled(theta-h))/(2*h)
    assert abs(df-da)>.005
    return {"status":"PASS","one_plaquette_SU2_angle_checks":records,
      "exact_identity":"S_adj_rescaled = S_fund - 1/2 (S_fund)^2",
      "weak_field_common_quadratic":"theta^2/8",
      "finite_theta_07_force_fund":df,"finite_theta_07_force_adj":da,
      "center_minus_identity_fundamental_action":center_fund,
      "center_minus_identity_adjoint_action":center_adj,
      "lesson":"Gauge invariance, smooth-field locality and the same F² term do not uniquely determine a finite lattice action. Center-blind adjoint-only dynamics differs globally from center-sensitive fundamental matter.",
      "scope":"Exact single SU2 plaquette algebra and weak-field expansion; not a fundamental derivation of Yang-Mills couplings or quantum continuum."}

def n_thermal(beta,w):
    return 1/math.expm1(beta*w)

def wightman_greater(z,beta,w):
    n=n_thermal(beta,w)
    return ((n+1)*np.exp(-1j*w*z)+n*np.exp(1j*w*z))/(2*w)

def quantum_state_gate():
    w=1.7;t=.41
    ret=np.sin(w*t)/w
    rows=[]
    for beta in [.4,2.,10.]:
        n=n_thermal(beta,w)
        cov=(n+.5)*np.cos(w*t)/w
        # KMS: W_>(t-i beta)=W_<(t) on the exact free oscillator.
        wless=((n)*np.exp(-1j*w*t)+(n+1)*np.exp(1j*w*t))/(2*w)
        kms=abs(wightman_greater(t-1j*beta,beta,w)-wless)
        times=np.linspace(0,2.2,6)
        G=np.array([[wightman_greater(x-y,beta,w) for y in times] for x in times])
        herm=np.linalg.norm(G-G.conj().T)
        eigmin=float(np.min(np.linalg.eigvalsh(G)))
        assert kms<1e-11 and eigmin>-1e-11 and herm<1e-12
        comm=wightman_greater(t,beta,w)-wightman_greater(-t,beta,w)
        assert abs(comm+1j*ret)<1e-12
        rows.append({"inverse_temperature_beta":beta,"occupancy_n":n,
          "retarded_response_same_for_all_beta":ret,
          "symmetric_noise_covariance_at_t":cov,
          "mean_energy":w*(n+.5),
          "KMS_identity_error":float(kms),
          "positive_Wightman_kernel_min_eigenvalue":eigmin,
          "commutator_state_independent_error":float(abs(comm+1j*ret))})
    assert rows[0]["symmetric_noise_covariance_at_t"]>rows[-1]["symmetric_noise_covariance_at_t"]*2
    assert rows[0]["mean_energy"]>rows[-1]["mean_energy"]
    return {"status":"PASS","harmonic_frequency_w":w,"comparison_time_t":t,
      "thermal_states":rows,
      "G_ret_definition":"i theta(t)<[q(t),q(0)]>=theta(t) sin(wt)/w",
      "noise_definition":"(1/2)<{q(t),q(0)}>=(n_beta+1/2) cos(wt)/w",
      "KMS_definition":"Wgreater(t-i beta)=Wless(t) in this convention",
      "conclusion":"The SAME causal/retarded propagator is compatible with distinct positive, stationary quantum states; even imposing KMS leaves beta to be selected by physics. Dynamical fluctuation information is missing from response alone.",
      "scope":"Known canonical harmonic-oscillator KMS/FDT; does not derive the Born rule or a unique interacting relativistic Hadamard state."}

def three_layer_entropy_gate():
    # Simple KR-like STRATIFIED LABELED family: bottom n/4, middle n/2,
    # top n/4; independent adjacent layer arrows, transitive closure.
    # This is a combinatorial SUBFAMILY, not literally every KR poset.
    rows=[]
    for N in (8,16,32,64):
        assert N%4==0
        A,B,C=N//4,N//2,N//4
        M=A*B+B*C
        beta=2.
        p=1/(1+math.exp(beta))
        rows.append({"N":N,"layer_sizes":[A,B,C],"independent_cover_bits":M,
          "log10_number_of_labeled_layered_posets":M*math.log10(2),
          "mean_links_beta_zero":M/2,
          "per_vertex_mean_cover_degree_beta_zero":M/N,
          "mean_links_beta_2":M*p,
          "per_vertex_mean_cover_degree_beta_2":2*M*p/N,
          "beta_needed_for_one_expected_link_per_event":math.log(M/N-1) if M>N else None})
    # Exact partition function: Z_N(beta)= (1+e^{-beta})^M.
    # To have E[#links]/N=c at large N, beta=ln(M/(cN)-1).
    assert all(rows[i+1]["per_vertex_mean_cover_degree_beta_zero"]>
               rows[i]["per_vertex_mean_cover_degree_beta_zero"] for i in range(len(rows)-1))
    hist=Counter(k.bit_count() for k in range(1<<16))
    assert len(hist)==17 and sum(hist.values())==65536
    assert all(hist[k]==math.comb(16,k) for k in range(17))
    # Reuse and verify the EXISTING full curved 4D Regge program, not a
    # duplicate announcement of its previously derived Hessian.
    S,V,areas,deficits=regge.evaluate(np.ones(15))
    expect=20*math.sqrt(3)/4*(2*math.pi-3*math.acos(.25))
    assert abs(S-expect)<1e-10
    h=1e-5;x=np.ones(15);x[0]+=h
    sp,_,_,_=regge.evaluate(x)
    x[0]=1-h
    sm,_,_,_=regge.evaluate(x)
    numerical=(sp-sm)/(2*h)
    expected=2*(2*math.pi-3*math.acos(.25))/math.sqrt(3)
    assert abs(numerical-expected)<1e-6
    return {"status":"PASS","three_layer_labeled_entropy":rows,
      "exact_enumeration_N8_link_count_histogram":{str(k):hist[k] for k in range(17)},
      "positive_weight_partition_function":"Z_N(beta)=[1+exp(-beta)]^{N^2/4} for independent adjacent layer links",
      "edge_probability":"p=1/(1+exp(beta)) and E[cover links]=N²p/4",
      "finite_weight_conclusion":"A finite N-independent positive Boltzmann edge penalty leaves O(N²) cover links and O(N) per-event mean incidence in this family. To hold mean edge count O(N), one must tune beta approximately log N; this is not an intrinsic 4D selector.",
      "existing_4D_Regge_S4_action":S,
      "existing_4D_Regge_S4_volume":V,
      "existing_4D_Regge_one_edge_gradient_numeric":numerical,
      "existing_4D_Regge_one_edge_gradient_Schlaefli":expected,
      "prior_repo_script":"analysis/toe_20261105_regge_s4_nonlinear_hessian.py",
      "critical_separation":"The 4D Regge action requires an inserted manifold/metric simplex complex. A sum over unrestricted causal posets must additionally defeat nonmanifoldlike history entropy. The toy positive weight does NOT exhaust oscillatory quantum BDG actions; known research can suppress KR orders.",
      "scope":"Exact count of a fixed-layer labeled family and rechecked 4D Euclidean Regge control; not general causal-set path-integral dynamics, Lorentzian Einstein constraints or 4D emergence."}

def sm_anomalies(charges):
    a,u,d,l,e,n=charges
    return {"SU3_squared_U1":2*a+u+d,
            "SU2_squared_U1":3*a+l,
            "gravity_squared_U1":6*a+3*u+3*d+2*l+e+n,
            "U1_cubed":6*a**3+3*u**3+3*d**3+2*l**3+e**3+n**3,
            "SU3_cubed":sp.Integer(2-1-1),
            "SU2_Witten_left_doublets":4}

def sm_quotient_check(charges,higgs):
    # generator exp(2pi i/3) in color, -1 in weak, exp(i pi/3)
    # in y=6Y integral hypercharge. 2t+3s+y divisible by 6.
    trials=[1,-1,-1,0,0,0];weak=[1,0,0,1,0,0]
    return [int((2*t+3*s+int(y))%6) for t,s,y in zip(trials,weak,charges)]+[int((3+int(higgs))%6)]

def hypercharge_gate():
    a,x=sp.symbols("a x",integer=True)
    names=["Q_L","u_c","d_c","L_L","e_c","nu_c"]
    q=[a,-a-x,-a+x,-3*a,3*a+x,3*a-x]
    sm=sm_anomalies(q)
    assert all(sp.simplify(v)==0 for k,v in sm.items() if k!="SU2_Witten_left_doublets")
    # Direct symbolic factorization of anomaly equations before imposing Yukawas:
    b,e=sp.symbols("b e",integer=True)
    generic=[a,b,-2*a-b,-3*a,e,6*a-e]
    cubic_generic=sp.factor(sm_anomalies(generic)["U1_cubed"])
    assert sp.expand(cubic_generic-18*a*(2*a-b-e)*(4*a+b-e))==0
    examples=[]
    for A,X in [(1,3),(1,9),(7,3),(-5,-3),(13,15)]:
        vals=[int(z.subs({a:A,x:X})) for z in q]
        anomalies=sm_anomalies(vals)
        assert all(int(v)==0 for k,v in anomalies.items() if k!="SU2_Witten_left_doublets")
        quotient=sm_quotient_check(vals,X)
        assert quotient==[0]*7
        # Given a Higgs doublet with charge yH=X, all four Yukawas are invariant.
        yukawas=[vals[0]+vals[1]+X,
                 vals[0]+vals[2]-X,
                 vals[3]+vals[4]-X,
                 vals[3]+vals[5]+X]
        assert yukawas==[0,0,0,0]
        # U(1)_em=T3+y/(2y_H) for Higgs neutral lower component.
        neutrino_charge=(X-3*A)/(2*X)
        examples.append({"a_Q_integer_y":A,"x_Higgs_integer_y":X,
             "charges_by_field":dict(zip(names,vals)),"anomaly_sums":{k:int(v) for k,v in anomalies.items()},
             "Z6_center_residues":quotient,"all_renormalizable_Yukawa_charge_sums":yukawas,
             "left_neutrino_em_charge_given_Higgs":neutrino_charge,
             "nu_c_hypercharge":vals[5]})
    assert examples[0]["charges_by_field"]==dict(zip(names,[1,-4,2,-3,6,0]))
    assert examples[1]["left_neutrino_em_charge_given_Higgs"]!=0
    assert examples[0]["left_neutrino_em_charge_given_Higgs"]==0
    # If no nu_c, gravitational U1 anomaly is +(-nu_c); exact cancellation
    # forces nu_c=0, i.e. x=3a (for this branch and rep content).
    no_nu_grav=sp.simplify(sm["gravity_squared_U1"]-q[-1])
    assert sp.expand(no_nu_grav-(x-3*a))==0
    return {"status":"PASS","normalization":"y=6Y integral; SU3 triality t=±1, SU2 center parity s=0,1",
      "global_Z6_quotient_congruence":"2*t+3*s+y == 0 (mod 6)",
      "input_nonabelian_representations":"Q=(3,2); u_c=(bar3,1); d_c=(bar3,1); L=(1,2); e_c=(1,1); nu_c=(1,1)",
      "two_parameter_anomaly_free_Yukawa_family":dict(zip(names,[str(z) for z in q])),
      "Higgs_y_charge":"x", "integer_global_quotient_lattice":"a=1+6m and x=3+6n for integers m,n",
      "symbolic_anomalies":{k:str(v) for k,v in sm.items()},
      "generic_cubic_anomaly_factor_with_linear_conditions":str(cubic_generic),
      "sample_charge_families":examples,
      "no_nu_c_remaining_grav_anomaly":str(no_nu_grav),
      "extra_condition_for_neutral_nu_or_gauge_neutral_nu_c":"x=3a, reducing to the SM relative charges in the chosen field representation branch",
      "main_result":"Anomaly freedom + SM Z6 quotient + conventional rep content + one Higgs Yukawa structure still leaves infinitely many integer charge assignments IF nu_c exists. Observed neutrino neutrality or removing nu_c closes the remaining charge ratio freedom (up to common normalization).",
      "scope":"Established global SM quotient/anomaly logic, explicitly solved in one fixed generation branch. It does not derive the representations, 3 generations, gauge group, Higgs or neutrino neutrality from the causal substrate."}

def cross_sector_center_gate():
    # Gauge action, global topology and charged representations are tied:
    # SU2 center -1 vanishes in adjoint but not in fundamental doublets.
    S_f_minus=fundamental(2*math.pi)
    S_adj_minus=adjoint_rescaled(2*math.pi)
    assert abs(S_f_minus-2)<1e-13 and abs(S_adj_minus)<1e-13
    signs=[]
    for r in range(2):
        for t in (0,1):
            phase=(-1)**(r*t)
            signs.append({"number_of_fundamental_SU2_doublet_factors":r,
                         "center_element_minus_1_present":bool(t),
                         "matter_center_phase":phase})
    # The SM Z6 quotient cancels the simultaneous nontrivial color,
    # weak and U1 central phases on all allowed fields.
    charges=[1,-4,2,-3,6,0]
    residues=sm_quotient_check(charges,3)
    assert residues==[0]*7
    return {"status":"PASS","SU2_center_flux_adjoint_cost":S_adj_minus,
      "SU2_center_flux_fundamental_cost":S_f_minus,
      "center_action_on_fundamental_doublet":-1,
      "center_action_on_adjoint":+1,
      "fundamental_rep_phase_checks":signs,
      "SM_Z6_combined_center_residues":residues,
      "bridge":"A center-blind pure-adjoint action may share the same weak-field F² term, but SU2 doublet matter and global quotients distinguish its center sectors. A causal TOE must determine its global gauge form AND allowed matter representations jointly; local curvature algebra alone cannot.",
      "scope":"Known SU2/SO3 global-form and center representation effects. No empirical new physics or derived SM model."}

def center_partition_nonperturbative_gate():
    """Actual SU2 single-plaquette Haar integral, not just action comparison.

    U=cos(phi) I+i sin(phi) n.sigma; normalized Haar radial measure
    (2/pi)sin(phi)^2 d phi, phi in [0,pi]. Wfund=(Tr U)/2=cos phi.
    """
    def measure(phi):return 2/math.pi*math.sin(phi)**2
    records=[]
    for beta in (0.,1.,2.,4.):
        def action_f(phi):return 1-math.cos(phi)
        def action_a(phi):return (1-math.cos(2*phi))/4
        sample={}
        for tag,act in (("fundamental",action_f),("adjoint",action_a)):
            Z=quad(lambda p:measure(p)*math.exp(-beta*act(p)),0,math.pi,epsabs=2e-13)[0]
            W=quad(lambda p:measure(p)*math.exp(-beta*act(p))*math.cos(p),
                   0,math.pi,epsabs=2e-13)[0]/Z
            sample[tag]={"Z":Z,"fundamental_Wilson_trace_normalized_mean":W}
        if beta>0:
            known=(iv(1,beta)-iv(3,beta))/(2*(iv(0,beta)-iv(2,beta)))
            assert abs(sample["fundamental"]["fundamental_Wilson_trace_normalized_mean"]-known)<1e-12
        assert abs(sample["adjoint"]["fundamental_Wilson_trace_normalized_mean"])<1e-12
        records.append({"beta":beta,**sample})
    assert records[2]["fundamental"]["fundamental_Wilson_trace_normalized_mean"]>.4
    return {"status":"PASS","single_plaquette_SU2_Haar_radial_measure":"(2/pi)sin(phi)^2 d phi",
      "fundamental_Wilson_loop_observable":"W=Tr(U)/2=cos(phi)",
      "Haar_partition_records":records,
      "exact_fundamental_mean":"[I1(beta)-I3(beta)]/[2(I0(beta)-I2(beta))]",
      "exact_adjoint_mean":0,
      "beta2_unequal_Wilson_mean":[records[2][x]["fundamental_Wilson_trace_normalized_mean"] for x in ("fundamental","adjoint")],
      "interpretation":"Even one-plaquette quantum/Haar averages distinguish center-sensitive and center-blind actions with identical weak-field quadratic terms. Adj action is invariant under U->-U and yields zero fundamental Wilson expectation.",
      "scope":"0D single SU2 plaquette class-function integral, NOT a four-dimensional continuum lattice gauge theory or a confinement theorem."}


def produce():
    gates={
      "I_bounded_poset_contractible_spin_holonomy_obstruction":causal_spin_gate(),
      "II_gauge_invariance_action_nonuniqueness_and_center":gauge_action_uniqueness_gate(),
      "III_response_noise_KMS_vacuum_ambiguity":quantum_state_gate(),
      "IV_exact_poset_entropy_and_existing_4D_Regge_control":three_layer_entropy_gate(),
      "V_SM_global_Z6_anomaly_Yukawa_charge_lattice":hypercharge_gate(),
      "VI_center_sensitive_matter_global_transport_bridge":cross_sector_center_gate(),
      "VII_nonperturbative_center_sensitive_Haar_observable":center_partition_nonperturbative_gate()
    }
    assert len(gates)==7 and all(x["status"]=="PASS" for x in gates.values())
    return {"status":"PASS: seven integrated conditional scientific gates, NOT A TOE",
      "date":"2026-11-19","TOE_solved":False,
      "4D_Einstein_Lorentzian_dynamics_derived":False,
      "Born_rule_or_unique_vacuum_derived":False,
      "SM_spectrum_or_couplings_derived":False,
      "sources":[
        "https://doi.org/10.1016/j.topol.2016.12.001",
        "https://www.scholarpedia.org/article/Lattice_gauge_theories",
        "https://cds.cern.ch/record/1497911/files/Lattice%202012_252.pdf",
        "https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.6.023113",
        "https://doi.org/10.1007/s10714-024-03281-1",
        "https://arxiv.org/abs/2209.00327",
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC5253799/",
        "https://doi.org/10.1103/PhysRevD.83.015009",
        "https://scoap3-prod-backend.s3.cern.ch/media/files/87510/10.1007/JHEP08%282024%29004_a.pdf"
      ],"gates":gates}
def main():
    result=produce()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2),encoding="utf8")
    g=result["gates"]
    print(json.dumps({"status":"PASS","gate_count":len(g),
      "causal_H1_unbounded_vs_bounded":[g["I_bounded_poset_contractible_spin_holonomy_obstruction"][s]["H1_mod2"] for s in ("unbounded_crown","bounded_causal_interval")],
      "SU2_center_action":[g["II_gauge_invariance_action_nonuniqueness_and_center"][s] for s in ("center_minus_identity_fundamental_action","center_minus_identity_adjoint_action")],
      "thermal_noise":[x["symmetric_noise_covariance_at_t"] for x in g["III_response_noise_KMS_vacuum_ambiguity"]["thermal_states"]],
      "4D_Regge_S":g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]["existing_4D_Regge_S4_action"],
      "hypercharge_samples":[(r["a_Q_integer_y"],r["x_Higgs_integer_y"],r["left_neutrino_em_charge_given_Higgs"]) for r in g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]["sample_charge_families"]],
      "output":str(OUT)}))
if __name__=="__main__":main()
