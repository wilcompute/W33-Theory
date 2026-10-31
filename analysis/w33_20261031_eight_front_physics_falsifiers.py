#!/usr/bin/env python3
"""Eight W33 TOE frontiers: five specified followups + three physical falsifiers.

This is a finite computational workbench: no derived Standard Model, continuum gravity,
real-form selection, laboratory photonics, or intrinsic speed of light.
"""
from __future__ import annotations
import json, math, sys, itertools, argparse
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from symmetric_fast import fast_build
from analysis.w33_20261031_54d_beamsplitter_compiler import canonical, payload as opt_payload
from analysis.w33_20261031_plaquette_strict_duality_gap import geometry as w33_geometry
from analysis.w33_20261031_local_tick_mediator import energy_matrix

OUT=ROOT/"data/w33_20261031_eight_front_physics_falsifiers.json"

def graph9():
    p=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())
    points,lines=fast_build(9);chosen=p["results"][0]["chosen"]
    sub=[set(lines[j]) for j in chosen]
    g=nx.Graph();g.add_nodes_from(range(48))
    g.add_edges_from((i,j) for i in range(48) for j in range(i+1,48) if sub[i]&sub[j])
    colors=nx.bipartite.color(g)
    left=sorted(i for i in g if colors[i]==0)
    right=sorted(i for i in g if colors[i]==1)
    b=np.array([[int(g.has_edge(i,j)) for j in right] for i in left],int)
    assert b.shape==(24,24) and g.number_of_edges()==240
    return g,b

def torsion_and_gauge(g,b):
    d=smith_normal_form(Matrix(b.tolist()),domain=ZZ)
    diag=[abs(int(d[i,i])) for i in range(24)]
    assert diag==[1]*11+[5]*7+[0]*6
    graph_betti=g.number_of_edges()-g.number_of_nodes()+nx.number_connected_components(g)
    assert graph_betti==193
    return {"smith_diagonal":{"one":11,"five":7,"zero":6},
      "integral_cokernel_torsion_dimension_F5":7,"graph_H1_dimension_F5":graph_betti,
      "automatic_identification":False,
      "falsifier":"Demand an equivariant natural map from incidence-cokernel 5-torsion to graph cohomology, plus a gauge connection and a Hamiltonian. Neither 7 nor a Z5 phase is by itself a physical particle or gauge field.",
      "status":"EXACT_COMPARISON_NOT_EQUIVALENCE"}

def rot12(t):
    c,s=math.cos(t),math.sin(t)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]],float)

def rot23(t):
    c,s=math.cos(t),math.sin(t)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]],float)

def local_optical(t,p,ph2=math.pi,ph3=math.pi):
    v=rot23(p)@rot12(t)
    d=np.diag([1,np.exp(1j*ph2),np.exp(1j*ph3)])
    return v@d@v.T

def optical_fidelity():
    U0,_=canonical()
    t=math.atan2(math.sqrt(10),2);p=math.atan2(1,3)
    assert np.max(abs(U0-local_optical(t,p)))<1e-14
    schedule=opt_payload()
    rng=np.random.default_rng(31031)
    result={}
    for side in ("plus","minus"):
        entries=schedule[side]["schedule"]
        blocks=[];blocks_uniform=[]
        phase_spread=[]
        for rec in entries:
            j=rec["canonical_to_local_order"];sign=rec["canonical_sign_gauge"]
            S=np.zeros((3,3),float)
            for k,q in enumerate(j):S[q,k]=sign[k]
            actual=S@U0@S.T
            err=rng.normal(0,0.01,size=4)
            noisy=S@local_optical(t+err[0],p+err[1],
                                  math.pi+err[2],math.pi+err[3])@S.T
            blocks.append(np.trace(actual.conj().T@noisy))
            blocks_uniform.append(np.trace(actual.conj().T@(np.exp(0.035j)*actual)))
            phase_spread.append(float(np.max(abs(noisy.conj().T@noisy-np.eye(3)))))
        d=81
        tr=sum(blocks);tr_common=sum(blocks_uniform)
        favg=(abs(tr)**2+d)/(d*(d+1))
        f_common=(abs(tr_common)**2+d)/(d*(d+1))
        assert .99<favg<1 and abs(f_common-1)<1e-13
        eta=.995
        survival=eta**5
        result[side]={"blocks":27,"two_mode_angle_and_phase_noise_rms_radians":.01,
          "seed":31031,"unitary_average_gate_fidelity_ideal_vs_noisy":float(favg),
          "coherent_common_global_phase_fidelity":float(f_common),
          "max_unitarity_defect":max(phase_spread),
          "assumed_uniform_power_survival_per_five_stages_eta_0p995":survival,
          "noise_model":"Four independent normal perturbations per block; fixed ideal signed permutations. Equal scalar power attenuation eta per stage and mode, independent of phase noise."}
    return {"status":"PASS_IDEAL_SIMULATION_NOT_MEASURED_HARDWARE","orientations":result,
      "not_inferred":"No FT threshold, calibration from waveguide data, or actual physical loss/crosstalk statistics."}

def local_clock():
    E=energy_matrix()
    assert E.shape==(120,120)
    x=math.exp(-.7)
    T=np.exp(-.7*E)
    ev=np.linalg.eigvalsh(T)
    target=np.sort(np.array([1+2*x**3+117*x*x]+
        [1+2*x**3-3*x*x]*39+[1-x**3]*80))
    assert np.max(abs(ev-target))<1e-10
    lam0=target[-1];lam1=target[-2]
    xi=1/math.log(lam0/lam1)
    # Label-swap maps entire 40 direction classes to each other, not only W33 automorphisms.
    directions=[tuple([a]+[int(j) for j in np.flatnonzero(E[a]==3)]) for a in range(0,120,3)]
    assert len(set(directions))==40 and all(len(set(z))==3 for z in directions)
    # Extract intrinsic label classes rather than trusting their indexing.
    classes=[];unused=set(range(120))
    while unused:
        a=min(unused);cls=tuple(sorted(np.flatnonzero(E[a]==3).tolist()+[a]))
        assert len(cls)==3;classes.append(cls);unused-=set(cls)
    swap=np.arange(120)
    for a,b in zip(classes[0],classes[1]):swap[a],swap[b]=swap[b],swap[a]
    assert np.array_equal(E,E[np.ix_(swap,swap)])
    return {"status":"EXACT_LOCAL_CHAIN_WITH_ACCIDENTAL_SYMMETRY",
      "temperature_betaJ":.7,"lambda_Perron":float(lam0),
      "lambda_subleading":float(lam1),"one_dimensional_correlation_length_sites":xi,
      "positive_temperature_unique_symmetric_transfer_state":True,
      "actual_projector_tick_interaction":"E(a,b)=3-Tr(Pi_a Pi_b) in {0,2,3}",
      "larger_than_W33_symmetry":"S3 wreath S40; arbitrary swaps of forty direction classes preserve E",
      "limitation":"No unique tick, geometry discrimination, intrinsic preferred real form, or physical time without extra microscopic terms."}

def chern(m,n=21,partner=False):
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1.,-1.]).astype(complex)
    vec=np.empty((n,n,2),complex)
    emin=1e9
    for a in range(n):
        for b in range(n):
            k=2*math.pi*np.array([a,b])/n
            if partner: k=(-k)%(2*math.pi)
            H=np.sin(k[0])*sx+np.sin(k[1])*sy+(m+np.cos(k[0])+np.cos(k[1]))*sz
            if partner:H=H.conj()
            eig,uv=np.linalg.eigh(H)
            emin=min(emin,float(eig[1]-eig[0]))
            vec[a,b]=uv[:,0]
    plaquettes=0.
    for a in range(n):
        for b in range(n):
            A=vec[a,b];B=vec[(a+1)%n,b];C=vec[(a+1)%n,(b+1)%n];D=vec[a,(b+1)%n]
            links=[np.vdot(A,B),np.vdot(B,C),np.vdot(D,C),np.vdot(A,D)]
            assert min(abs(z) for z in links)>1e-7
            plaquettes+=np.angle(links[0]*links[1]/(links[2]*links[3]))
    return int(round(plaquettes/(2*math.pi))),emin

def chiral_topology():
    rows={}
    for m in (-3.,-1.,1.,3.):
        plus,gap=chern(m,21)
        minus,gap2=chern(m,21,True)
        assert plus==-minus and gap>0 and gap2>0
        assert (plus==0)==(abs(m)>2)
        rows[str(m)]={"chern":plus,"antiunitary_partner_chern":minus,
                       "sampled_min_band_gap":gap}
    for n in (11,17,25):
        a,g=chern(-1,n);b,h=chern(-1,n,True)
        assert a==-b and abs(a)==1
    return {"status":"PASS_TWO_BAND_TOPOLOGICAL_CONTROL",
      "bulk_hamiltonian":"sin kx sigma_x + sin ky sigma_y + (m+cos kx+cos ky) sigma_z",
      "conjugate_partner":"H_minus(k)=H_plus^*(-k); integer Chern changes sign",
      "phase_diagram":rows,"grids_checked":[11,17,21,25],
      "limitations":"This is the standard externally supplied QWZ 2D lattice model, not an intrinsic W33 Weyl/CP derivation or a Standard-Model anomaly."}

def wave_continuum():
    Q=np.array([[5,2.5,-3,0],[2.5,5,0,-3],[-3,0,6,-3],[0,-3,-3,6]],float)
    assert np.min(np.linalg.eigvalsh(Q))>0
    bound=4*float(np.abs(Q).sum())
    dt=1/math.sqrt(bound)
    max_lam=0.
    for phases in itertools.product(np.linspace(0,2*math.pi,8,endpoint=False),repeat=4):
        p=np.exp(1j*np.array(phases))-1
        lam=float(np.vdot(p,Q@p).real)
        max_lam=max(max_lam,lam)
        assert lam>=-1e-12 and dt*dt*lam<=4+1e-12
    m=np.array([1,2,1,0],float)
    ideal=float(m@Q@m)
    data=[]
    for n in (8,16,32,64):
        k=2*math.pi*m/n
        p=np.exp(1j*k)-1
        lam=float(np.vdot(p,Q@p).real)
        ratio=lam/(2*math.pi/n)**2
        assert lam>0
        omega=2*math.asin(dt*math.sqrt(lam)/2)/dt
        data.append({"N":n,"lambda":lam,"continuum_qform":ideal,
            "relative_error":abs(ratio-ideal)/ideal,"leapfrog_omega":omega})
    assert all(data[i]["relative_error"]>data[i+1]["relative_error"] for i in range(3))
    return {"status":"PASS_CONDITIONAL_LATTICE_WAVE_PROPAGATION",
      "native_metric_Q":Q.tolist(),"acoustic_gradient":"p_mu=e^(ik_mu)-1; lambda=p^* Q p",
      "analytic_stable_dt_upper_bound":2/math.sqrt(bound),
      "chosen_dt":dt,"sampled_max_lambda":max_lam,
      "one_tick_strict_coordinate_support":"couples offsets 0, ±e_mu, ±(e_mu-e_nu): L1 radius <=2 per tick",
      "refinement":data,"limitation":"Externally supplied time step and wave kinetic action. Discrete causality does not determine physical light speed, Lorentz invariance, or Einstein gravity."}

def z5_flux(g):
    assert nx.is_connected(g)
    tree=nx.minimum_spanning_tree(g)
    chords=sorted(set(tuple(sorted(e)) for e in g.edges())-
                  set(tuple(sorted(e)) for e in tree.edges()))
    assert len(chords)==193
    edge=chords[0]
    z=np.exp(2j*math.pi/5)
    rng=np.random.default_rng(20261031)
    gauge={u:z**int(t) for u,t in zip(g.nodes(),rng.integers(0,5,len(g)))}
    amp={(min(u,v),max(u,v)):1.+0j for u,v in g.edges()}
    amp[edge]=z
    def directed(u,v,values):
        key=(min(u,v),max(u,v))
        return values[key] if u<v else values[key].conjugate()
    transformed={(u,v):gauge[u]*w*gauge[v].conjugate() for (u,v),w in amp.items()}
    path=nx.shortest_path(tree,*edge)
    cycle=path+[path[0]]
    def hol(values):
        prod=1+0j
        for u,v in zip(cycle,cycle[1:]):prod*=directed(u,v,values)
        return prod
    before=hol(amp);after=hol(transformed)
    assert abs(before-after)<1e-13 and abs(abs(before)-1)<1e-13
    assert min(abs(before-z),abs(before-z.conjugate()))<1e-13
    return {"status":"PASS_Z5_FLUX_GAUGE_COVARIANCE_ON_DECLARED_GRAPH",
      "cycle_rank":193,"incidence_cokernel_torsion_rank":7,
      "one_chord_with_z5_flux":list(edge),"cycle_length":len(cycle)-1,
      "wilson_loop_complex":[float(before.real),float(before.imag)],
      "gauge_invariance_error":float(abs(before-after)),
      "interpretation":"One *chosen* graph Z5 edge connection produces a gauge invariant Wilson loop; graph cohomology offers 193 independent cycle directions, NOT a canonical seven-flux selection. No dynamic gauge action."}

def orientation_readout():
    F=np.array([[0,1,-3],[-1,0,2],[3,-2,0]],float)
    I=np.eye(3)
    Uplus=I+F@F/14+F/math.sqrt(14)
    Uminus=I+F@F/14-F/math.sqrt(14)
    neutral=I+F@F/7
    assert np.max(abs(Uplus@Uplus.T-I))<1e-14
    assert np.max(abs(Uminus@Uminus.T-I))<1e-14
    plus=abs(Uplus[:,0])**2;minus=abs(Uminus[:,0])**2
    TV=float(sum(abs(plus-minus))/2)
    assert abs(TV-12/(7*math.sqrt(14)))<1e-13
    assert np.linalg.norm(Uplus-Uminus)>0 and np.array_equal(neutral,neutral)
    def bayes_error(n):
        # Equal priors and independent ideal photons: optimal multinomial test.
        result=0.
        for i in range(n+1):
            for j in range(n-i+1):
                k=n-i-j
                logmult=math.lgamma(n+1)-math.lgamma(i+1)-math.lgamma(j+1)-math.lgamma(k+1)
                probp=math.exp(logmult+i*math.log(plus[0])+j*math.log(plus[1])+k*math.log(plus[2]))
                probm=math.exp(logmult+i*math.log(minus[0])+j*math.log(minus[1])+k*math.log(minus[2]))
                result+=min(probp,probm)/2
        return result
    errors=[0.5]+[bayes_error(n) for n in range(1,61)]
    thresholds={}
    eta=.995**5
    loss_errors=[sum(math.comb(n,k)*eta**k*(1-eta)**(n-k)*errors[k]
                     for k in range(n+1)) for n in range(len(errors))]
    for tolerance in (.001,.000001):
        key=str(tolerance)
        ideal=next(n for n in range(1,len(errors)) if errors[n]<tolerance)
        detected=next(n for n in range(1,len(errors)) if loss_errors[n]<tolerance)
        assert errors[ideal-1]>=tolerance and loss_errors[detected-1]>=tolerance
        thresholds[key]={"required_detected_photons":ideal,
                         "required_injected_photons_with_loss_eta0p995_per_stage":detected,
                         "ideal_error_at_threshold":errors[ideal],
                         "loss_model_error_at_threshold":loss_errors[detected]}
    assert thresholds["0.001"]["required_detected_photons"]==23
    assert thresholds["1e-06"]["required_detected_photons"]==54
    assert thresholds["0.001"]["required_injected_photons_with_loss_eta0p995_per_stage"]==24
    assert thresholds["1e-06"]["required_injected_photons_with_loss_eta0p995_per_stage"]==56
    return {"status":"PASS_IDEAL_SINGLE_PHOTON_DIRECTION_READOUT",
       "optimal_equal_prior_bayes_test":{"one_photon_error":errors[1],
           "photons_to_error_thresholds":thresholds,
           "assumption":"IID injected input photons, fixed calibrated U+ or U-, ideal number-resolving port measurements; loss independent, heralded no-click outcome; no dark counts, drifts, crosstalk."},
       "canonical_signed_F":F.astype(int).tolist(),
       "plus_port_probabilities":plus.tolist(),"minus_port_probabilities":minus.tolist(),
       "total_variation_distance_one_shot":TV,
       "exact_distance":"12/(7 sqrt(14))",
       "orientation_blind_reciprocal_pulse":"U0=I+F^2/7 remains identical under F -> -F",
       "scope":"A conditional source-and-detector basis can discriminate ± direction in one ideal lossless canonical 3-mode block; no spontaneous CP orientation or time arrow is produced."}

def internal_topology(chiral):
    pts,lines=w33_geometry()
    W=nx.Graph();W.add_nodes_from(range(40))
    for line in lines:W.add_edges_from(itertools.combinations(line,2))
    A=nx.to_numpy_array(W,dtype=float)
    ev=np.linalg.eigvalsh(A)
    assert np.max(abs(ev))<=12+1e-10 and len(ev)==40
    chir=chiral["phase_diagram"]["-1.0"]["chern"]
    assert abs(chir)==1
    eps=.01
    assert 2*eps*np.max(abs(ev))<1. # External topological gap remains
    return {"status":"PASS_SPECTATOR_INTERNAL_TENSOR_FALSIFIER",
       "Hamiltonian":"H_QWZ(k) tensor I40 + epsilon I2 tensor A_W33",
       "spectator_modes":40,"internal_adjacency_spectrum":{"12":1,"2":24,"-4":15},
       "epsilon":eps,
       "positive_gap_lower_bound":"gap_QWZ - 16 epsilon (max-min adjacency =16)",
       "occupied_bundle_chern":40*chir,
       "partner_bundle_chern":-40*chir,
       "topological_charge_from_W33_alone":False,
       "interpretation":"An external 2D Chern band is replicated 40 times by an internal W33 spectator; it does not bootstrap Chern chirality from internal geometry or choose the sign."}

def build():
    graph,b=graph9()
    tors=torsion_and_gauge(graph,b)
    optics=optical_fidelity()
    clock=local_clock()
    ch=chiral_topology()
    wave=wave_continuum()
    three={"z5_synthetic_flux":z5_flux(graph),
           "directional_photon_readout":orientation_readout(),
           "external_chern_w33_spectator":internal_topology(ch)}
    return {"schema":"w33.20261031.eight_front_physics_falsifiers.v1",
      "status":"PASS_EIGHT_FINITE_TESTBED_FRONTS",
      "original_five":{"q9_A5_torsion":tors,"real_optical_noise":optics,
                       "local_clock_symmetry_audit":clock,
                       "chiral_index_control":ch,
                       "finite_speed_periodic_continuum":wave},
      "additional_three":three,
      "falsification_scope":"Models, numerical controls, exact algebra. All physics input structures are declared; no TOE proof, physical E8 real form, quantum gravity, or measured photonic chip.",
      "source_head":"2669069be2ddcee262b2a72569f01b2796177451"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=OUT)
    args=parser.parse_args()
    p=build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(p,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"status":p["status"],"original":len(p["original_five"]),
       "additional":len(p["additional_three"]),
       "orientation_TV":p["additional_three"]["directional_photon_readout"]["total_variation_distance_one_shot"],
       "chern":p["original_five"]["chiral_index_control"]["phase_diagram"]["-1.0"]["chern"],
       "output":str(args.output)},sort_keys=True))
if __name__=="__main__":main()
