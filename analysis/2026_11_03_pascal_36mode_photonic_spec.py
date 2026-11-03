#!/usr/bin/env python3
"""36-site Pascal photonic benchmark with *same-sized degree-preserving*
rewired control, loss, detunings, reproducible output-count classification.
All parameters are illustrative hardware tolerances, not device data.
"""
from pathlib import Path
import json,runpy,numpy as np,networkx as nx
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
G=runpy.run_path(str(ROOT/"analysis"/"2026_11_03_pascal_resistance_flow.py"))["graph"]
OUT=ROOT/"data"/"2026_11_03_pascal_36mode_photonic_spec.json"
def distributions(M,root,t):
    n=len(M);state=np.eye(n,dtype=complex)[:,root]
    out=expm(-1j*M*t)@state
    p=np.abs(out)**2
    assert abs(p.sum()-1)<1e-10
    return p
def tv(p,q):return float(np.linalg.norm(p-q,ord=1)/2)
def run():
    pts,idx,L,_=G(2)
    n=len(pts);root=idx[(0,0)]
    assert n==36
    graph=nx.Graph()
    graph.add_nodes_from(range(n))
    for i,j in zip(*np.triu_indices(n,1)):
        if L[i,j]<0:graph.add_edge(i,j)
    assert nx.is_connected(graph)
    rg=graph.copy()
    nx.double_edge_swap(rg,nswap=100,max_tries=20000,seed=631)
    if not nx.is_connected(rg):
        # Reproducible connected null with same degrees.
        for seed in range(632,700):
            rg=graph.copy()
            nx.double_edge_swap(rg,nswap=100,max_tries=20000,seed=seed)
            if nx.is_connected(rg):break
    assert nx.is_connected(rg)
    assert sorted(dict(graph.degree()).values())==sorted(dict(rg.degree()).values())
    assert list(dict(graph.degree()).values())==list(dict(rg.degree()).values())
    H=L.toarray()
    Hr=nx.laplacian_matrix(rg,nodelist=list(range(n))).toarray().astype(float)
    rng=np.random.default_rng(20261103)
    t=4.
    p=distributions(H,root,t)
    q=distributions(Hr,root,t)
    same_N_tv=tv(p,q)
    assert same_N_tv>.1
    A=np.diag(np.diag(H))-H
    no_detuning=-A
    badp=distributions(no_detuning,root,t)
    onsite_error=tv(p,badp)
    # Identical exponential loss in every channel multiplies all counts,
    # so conditioned on detection, p is unchanged.
    loss_fraction=.35
    assert abs((p*(1-loss_fraction)/(p*(1-loss_fraction)).sum()-p).max())<1e-10
    perturb=[]
    for seed in range(12):
        random=np.random.default_rng(1313+seed)
        Hnoise=np.zeros((n,n))
        for i,j in graph.edges():
            w=1+random.uniform(-.05,.05)
            Hnoise[i,j]-=w;Hnoise[j,i]-=w
            Hnoise[i,i]+=w;Hnoise[j,j]+=w
        Hnoise+=np.diag(random.uniform(-.05,.05,size=n))
        pn=distributions(Hnoise,root,t)
        perturb.append(tv(p,pn))
    # Hypothesis test: data from Pascal p or same-N degree-preserving
    # rewired q; assign by higher multinomial log-likelihood.
    # Requires both calibrated probability models and known output labeling.
    eps=1e-12
    nshots=300
    trials=250
    detected=int(nshots*(1-loss_fraction))
    count_success={"pascal":0,"rewired":0}
    logweights=np.log(np.maximum(p,eps)/np.maximum(q,eps))
    for label,prob in (("pascal",p),("rewired",q)):
        for k in range(trials):
            counts=rng.multinomial(detected,prob)
            predicted="pascal" if float(counts@logweights)>0 else "rewired"
            count_success[label]+=int(predicted==label)
    ans={"status":"PASS_36_MODE_DEGREE_MATCHED_PHOTONIC_BENCHMARK",
      "vertices":n,"edges":int(graph.number_of_edges()),
      "root_index":root,"dimensionless_propagation_time":t,
      "same_size_and_same_degree_sequence_rewired_control_TV":same_N_tv,
      "without_required_degree_dependent_onsite_TV":onsite_error,
      "uniform_loss_fraction_illustrative":loss_fraction,
      "uniform_loss_normalized_distribution_exactly_unchanged":True,
      "edge_coupling_uncertainty_bound_illustrative":.05,
      "onsite_detuning_error_bound_illustrative_J":.05,
      "12_seed_distribution_TV_under_fabrication_uncertainty":perturb,
      "shot_protocol":{"injected_photons":nshots,"detected_photons_assumed":detected,
         "trials_per_hypothesis":trials,
         "correct_classifications_pascal":count_success["pascal"],
         "correct_classifications_rewired":count_success["rewired"],
         "method":"multinomial likelihood-ratio, calibrated ideal distributions, known fixed output-port identity; zero dark counts and no cross talk assumed"},
      "hardware_matrix":"Hii=J*weighted_degree_i+detuning_i, Hij=-J*coupling_ij on nearest-neighbor links; propagation along z implements exp(-i H z); J z is dimensionless.",
      "construction":"Degree-preserving 100-double-edge-swap connected null, same 36 vertices and 63 edges. This tests topology beyond size and local degree. Rewired graph need not be geometrically planar or feasible as identical single-layer waveguides.",
      "limitations":"No fabrication, optical loss/crosstalk calibration, fiber coupling length, real device resolution, dark counts or physical hardware. The rewired null may need crossings/multiplane routing; it is a mathematical control. Photon counts are synthetic and use chosen 35% uniform loss.",
      "replay_seed":20261103}
    OUT.write_text(json.dumps(ans,indent=2)+"\n")
    print("36MODE",{"topology_TV":round(same_N_tv,4),"no_onsite_TV":round(onsite_error,4),"shot_success":count_success,"max_disorder_TV":round(max(perturb),4)})
    return ans
if __name__=="__main__":run()
