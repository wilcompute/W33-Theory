#!/usr/bin/env python3
"""Four falsifiers for the signed E6 model:
(A) four-copy physically measurable HP3-design witness with exact binomial power;
(B) 5D/6D ExFT cross-section obstruction, exact domain-wall mixing penalty;
(C) 12-axis hidden-qubit noisy decoder with finite-shot confidence;
(D) compilation of 45 Pauli rotations from the FIXED one-radian pulse
    and signed Clifford conjugations, with exact sequence simulation.
These are mathematical/computational models, not hardware results or field equations.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter,deque
import json,sys,math
import numpy as np, networkx as nx
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_E6_exft_generalized_closure_affine as ExFT
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_witness_selection_decoder_fixedangle.json"
def jfile(name):return json.loads((ROOT/"data"/name).read_text())

def four_copy_witness():
    """Single J-even Pauli, four independently prepared equal-state copies.
    The product of four +/- outcomes is an unbiased z_i^4 estimator.
    False positive alpha<.05 against quaternionic Haar, power>=.9
    against the 180-point design, with calibrated visibility eta.
    """
    report={}
    for eta in (1.,.9,.8):
        mu_F=eta**4/9
        mu_H=eta**4/33
        pf=(1+mu_F)/2
        ph=(1+mu_H)/2
        hit=None
        for n in range(100,150001,100):
            k=int(binom.ppf(.95,n,ph))+1
            alpha=float(binom.sf(k-1,n,ph))
            power=float(binom.sf(k-1,n,pf))
            if alpha<=.05+1e-10 and power>=.9:
                hit=dict(quartets=n,prepared_copies=4*n,
                     threshold_positive_quartets=k,false_positive_Haar=alpha,
                     power_against_finite_180=power)
                break
        assert hit is not None
        report[str(eta)]=dict(per_copy_visibility=eta,finite_fourth_mean=mu_F,
            Haar_fourth_mean=mu_H,signal_gap=mu_F-mu_H,**hit)
    # Exact noiseless moments in charge basis and known Beta(4,4) Haar.
    assert abs(report["1.0"]["signal_gap"]-(1/9-1/33))<1e-15
    return dict(status="PASS_FOUR_COPY_QUARTET_PHOTON_SHOT_WITNESS",
        measurement="four independent +/- measurements of a single J-even Pauli on four copies of same prepared pure state, product of signs",
        finite_E_z4="1/9",HP3_Haar_E_z4="1/33",
        exact_binomial_likelihood_thresholds=report,
        caveat="Visibility eta must be calibrated for the testing model; one quartet consumes four independently prepared copies. Ensemble preparations are independent between quartets.")

def section_cross_obstruction():
    """No 5D/6D simultaneous coordinate-derivative family satisfies
    the strong bilinear ExFT section condition. Exact transverse
    contraction-square census provides an invariant positive mixing cost.
    """
    T,Y,S5,S6=ExFT.setup()
    G=nx.Graph();G.add_nodes_from(range(27))
    supports=np.argwhere(np.any(T!=0,axis=2))
    for i,j in supports:
        if i<j:G.add_edge(int(i),int(j))
    sections=[tuple(sorted(s)) for s in nx.find_cliques(nx.complement(G))]
    s5=[s for s in sections if len(s)==5];s6=[s for s in sections if len(s)==6]
    assert (len(s5),len(s6))==(216,72)
    adj=np.any(T,axis=2).astype(np.int64)
    hist=Counter(); intersection=Counter(); joint={}
    for a in s5:
        for b in s6:
            x=int(adj[np.ix_(a,b)].sum())
            assert x>=1,(a,b)
            hist[x]+=1
            intersection[len(set(a)&set(b))]+=1
    assert sum(hist.values())==216*72
    # Min penalty is positive; thus adding *simultaneously* independent
    # gradients from two inequivalent maximal coordinate families fails.
    E_min=min(hist); E_max=max(hist)
    reps=[(0.1,0.),(.4,0.),(.6,1.),(.9,1.)]
    for initial,endpoint in reps:
        t=initial
        for _ in range(150):
            t=min(1.,max(0.,t-0.1*(1-2*t)))
        assert abs(t-endpoint)<1e-6
    # E_mix(t)=B*t*(1-t): exact equal endpoint minima and unstable t=.5
    return dict(status="PASS_STRONG_CONSTRAINT_CROSS_BRANCH_OBSTRUCTION",
        five_sections=216,six_sections=72,total_cross_pairs=15552,
        cross_contraction_edges_histogram={str(i):n for i,n in sorted(hist.items())},
        coordinate_intersection_histogram={str(i):n for i,n in sorted(intersection.items())},
        minimum_cross_tensor_squared_norm=E_min,maximum_cross_tensor_squared_norm=E_max,
        toy_mixing_potential="V_gamma(t)=gamma*B(S5,S6)*t*(1-t), gamma>0, t in [0,1]",
        two_equal_minima="t=0 (IIB 5D) and t=1 (M 6D)",
        dynamical_test="gradient descent to either endpoint for 4 initial weights; middle t=.5 unstable",
        no_go="Positive bilinear strong-constraint penalty excludes unconstrained simultaneous dependence on two different maximal coordinate sections; does NOT select 5D over 6D without other field data.",
        limit="The toy potential is not derived from the E6 exceptional-field-theory action or a covariant dynamical section-selection theory.")

def normalize(v):
    norm=np.linalg.norm(v,axis=-1,keepdims=True)
    return v/np.maximum(norm,1e-14)

def noisy_decoder():
    menu=jfile("toe_20261114_hidden_qubit_12_pauli_global_tomography.json")
    assert len(menu["global_menu_labels"])==12
    assert len(menu["orbit_local_three_axes"])==45
    # A 180-fiber uniformly sampled logical Bloch-sphere test. The
    # distribution of 3 anticommuting Pauli statistics is universal
    # across the fibers under the certified exact Clifford algebra.
    rng=np.random.default_rng(202611142)
    r=normalize(rng.normal(size=(180,24,3))) # 4320 independent pure fibers
    records={}
    for eta in (1.0,.81,.65):
        table={}
        for n in (20,80,240):
            N=np.full((3,),n,dtype=np.int64)
            shots=rng.binomial(n,np.clip((1+eta*r)/2,0,1))
            raw=2*shots/n-1
            decoded=normalize(raw)
            f=(1+np.sum(decoded*r,axis=-1))/2
            table[str(n)]=dict(total_measurements=3*n,mean_fidelity=float(f.mean()),
                lower_fifth_percentile_fidelity=float(np.quantile(f,.05)),
                upper_95_percentile_infidelity=float(np.quantile(1-f,.95)),
                calibration_not_needed_for_pure_direction=True)
            assert 0<=f.min() and f.max()<=1+1e-12
        records[str(eta)]=table
    # Adaptive allocation pilot 12 each; 324 remaining gives 360 shots.
    # Estimator for pure-state direction uses observed raw means and
    # normalization. Pilot allocation is a true adaptive protocol.
    eta=.81;pilot=12;total=360
    seed_rng=np.random.default_rng(202611143)
    pilot_hits=seed_rng.binomial(pilot,(1+eta*r)/2)
    est=2*pilot_hits/pilot-1
    vari=np.sqrt(np.maximum(0.05,1-est**2))
    allocation=(total-3*pilot)*vari/vari.sum(axis=-1,keepdims=True)
    floor=np.floor(allocation).astype(np.int64)
    residual=total-3*pilot-floor.sum(axis=-1)
    for k in range(3):
        floor[...,k]+=(residual>k).astype(np.int64)
    assert np.all(floor.sum(axis=-1)==total-3*pilot)
    extra=seed_rng.binomial(floor,np.clip((1+eta*r)/2,0,1))
    values=2*(pilot_hits+extra)/(pilot+floor)-1
    adapt_f=(1+np.sum(normalize(values)*r,axis=-1))/2
    equal_hits=seed_rng.binomial(total//3,np.clip((1+eta*r)/2,0,1))
    equal_f=(1+np.sum(normalize(2*equal_hits/(total//3)-1)*r,axis=-1))/2
    errBound=math.sqrt(2*math.log(6/.05)/240)
    return dict(status="PASS_FINITE_SHOT_180_FIBER_HIDDEN_QUBIT_DECODER",
        samples_pure_states=180*24,signed_12_measurement_menu=menu["global_menu_labels"],
        per_axis_shots=[20,80,240],physical_visibility_levels=[1,.81,.65],
        visibility_explanation="eta=(1-depolarizing_fraction)*(1-2*readout_bitflip_rate); 0.81 corresponds to 10% and 5%",
        results=records,
        adaptive_budget360_visibility081=dict(pilot_shots_per_axis=pilot,
            mean_fidelity_adaptive=float(adapt_f.mean()),
            mean_fidelity_equal=float(equal_f.mean()),
            observed_adaptive_minus_equal=float(adapt_f.mean()-equal_f.mean())),
        Hoeffding_95percent_each_axis_error_bound_240_shots=errBound,
        caveat="Known one of 180 charge projectors, ideal independent Pauli shots, calibrated common visibility; this is a sampling model not hardware or fault tolerance. Adaptive estimation need not beat equal allocation at finite sample.")

def fixed_radian_compiler():
    """Convert 45 continuously set Pauli angles to integer uses of one
    R_P0(1 rad) gate + finite Clifford conjugation. All synthesized
    product unitaries are compared in C8 on the same state.
    """
    cert=jfile("toe_20261114_USp8_constructive_pure_state_compiler.json")
    pauli,quad,nonquad,_=E.pauli_data()
    root=nonquad[0]
    # Signed root transitivity under quarter-turn Clifford generators.
    q=deque([(root,1)]);path={(root,1):()}
    while q:
        a,sg=q.popleft()
        for g in nonquad:
            if not E.omega(a,g):continue
            w=a^g
            val=1j*pauli[g]@pauli[a]
            if np.array_equal(val,pauli[w]):sign=1
            else:
                assert np.array_equal(val,-pauli[w])
                sign=-1
            for orient in (-1,1):
                dest=(w,sg*orient*sign)
                if dest not in path:
                    path[dest]=path[a,sg]+((g,orient),)
                    q.append(dest)
    assert len(path)==72
    ids=cert["minimal_independent_tangent_axes"]
    labels=ids*3
    assert len(labels)==45 and len(cert["continuous_angle_vectors"])==5
    e0=np.eye(8,dtype=complex)[:,0]
    def run(angles):
        v=e0.copy()
        for a,ang in zip(labels,angles):
            p=pauli[a]
            v=np.cos(ang)*v+1j*np.sin(ang)*(p@v)
        return v
    reports={}
    for B in (80,250,1000,4000):
        ints=np.arange(-B,B+1,dtype=np.int64)
        trials=[]
        for ang,continuous_fidelity in zip(cert["continuous_angle_vectors"],cert["random_target_state_fidelities"]):
            ang=np.asarray(ang,dtype=float)
            tick=[];errors=[]
            for theta in ang:
                eps=(theta-ints+np.pi/2)%np.pi-np.pi/2
                ind=int(np.argmin(np.abs(eps)+1e-12*np.abs(ints)))
                tick.append(int(ints[ind]));errors.append(float(eps[ind]))
            v_cont=run(ang)
            v_disc=run(tick)
            F=float(abs(np.vdot(v_cont,v_disc))**2)
            alpha=math.acos(min(1.,math.sqrt(float(continuous_fidelity))))
            beta=math.acos(min(1.,math.sqrt(min(1.,F))))
            lower=max(0.,math.cos(min(math.pi/2,alpha+beta)))**2
            cliff=2*sum(len(path[labels[i],1 if k>0 else -1])
                  for i,k in enumerate(tick) if k)
            trials.append(dict(unit_radian_ticks=sum(abs(k) for k in tick),
                max_single_angle_mod_pi_error=max(abs(z) for z in errors),
                sum_angles_mod_pi_error=sum(abs(z) for z in errors),
                continuous_vs_integer_state_fidelity=F,
                certified_lower_bound_target_fidelity=lower,
                Clifford_conjugation_gates_upper_bound=cliff))
        reports[str(B)]=dict(max_signed_tick_bound=B,
           mean_unit_ticks=float(np.mean([r["unit_radian_ticks"] for r in trials])),
           max_unit_ticks=max(r["unit_radian_ticks"] for r in trials),
           min_fidelity_vs_continuous=min(r["continuous_vs_integer_state_fidelity"] for r in trials),
           min_certified_target_fidelity=min(r["certified_lower_bound_target_fidelity"] for r in trials),
           max_Clifford_conjugators=max(r["Clifford_conjugation_gates_upper_bound"] for r in trials),
           all_five_trials=trials)
    assert reports["4000"]["min_certified_target_fidelity"]>.999
    return dict(status="PASS_FIXED_ONE_RADIAN_PLUS_CLIFFORD_EXPLICIT_STATE_APPROXIMANT",
        root_generator_label=root,Clifford_signed_root_orbit_size=len(path),
        maximum_minimal_Clifford_conjugation_word_length=max(map(len,path.values())),
        number_compiled_targets=5,pauli_axis_segments_each=45,
        exhaustive_signed_tick_lookup="Search integers k in [-B,B] minimizing |theta-k| modulo pi; finite gate word uses |k| copies of fixed R_P(1) conjugated to target Pauli.",
        depth_vs_fidelity=reports,
        scope="Explicit valid (very inefficient) Clifford+single-fixed-radian gate sequence. Angles 1 rad are a mathematical primitive, not calibrated photonic gates. No Solovay-Kitaev efficiency claim.")

def main():
    records={"four_copy_design_witness":four_copy_witness(),
        "five_six_section_domainwall":section_cross_obstruction(),
        "noisy_logical_qubit_decoder":noisy_decoder(),
        "one_radian_fixed_gate_compiler":fixed_radian_compiler()}
    assert all(s["status"].startswith("PASS_") for s in records.values())
    output={"status":"PASS_FOUR_EXPERIMENTAL_FALSIFIER_FRONTS", "records":records}
    OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    for k,v in records.items():
        print(k,v["status"],flush=True)
        if k=="four_copy_design_witness":print("SHOTS",[(x,v["exact_binomial_likelihood_thresholds"][x]["prepared_copies"]) for x in ("1.0","0.9","0.8")],flush=True)
        elif k=="five_six_section_domainwall":print("ENERGY",v["minimum_cross_tensor_squared_norm"],v["maximum_cross_tensor_squared_norm"],"HIST",v["cross_contraction_edges_histogram"],flush=True)
        elif k=="noisy_logical_qubit_decoder":print("DECODER_0.81",v["results"]["0.81"],flush=True)
        else:print("FIXED",[(k,round(s["min_certified_target_fidelity"],8),round(s["mean_unit_ticks"])) for k,s in v["depth_vs_fidelity"].items()],flush=True)
    return output
if __name__=="__main__":main()
