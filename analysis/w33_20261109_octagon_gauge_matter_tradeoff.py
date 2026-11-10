#!/usr/bin/env python3
"""Positive local W33 octagon Wilson action vs half-filled fermion free energy.

Existing TOE61 proves 3π dominance among EIGHT nonlocal deck sectors
for every beta>0. Here evaluate all 1620 shortest incidence cycles
at the 15-edge gapping masks and compare simple *local* gauge action
plus free fermions to flat and eight deck sector controls. No physical
coupling constant chosen or dynamic gauge action solved.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261109_minimal_15_flux_lift import find_support
from w33_20261010_toe38_local_maxwell_2complex import prep

def loops_length8(G):
    seen=set()
    for start in G.nodes():
        for b in G.neighbors(start):
            if b<=start:continue
            stack=[(b,[start,b],{start,b})]
            while stack:
                cur,path,visited=stack.pop()
                if len(path)==8:
                    if start in G[cur]:
                        seq=tuple(path)
                        rev=(start,)+tuple(reversed(path[1:]))
                        seen.add(min(seq,rev))
                    continue
                for v in G.neighbors(cur):
                    if v>start and v not in visited:
                        stack.append((v,path+[v],visited|{v}))
    return sorted(seen)

def edge_phase_count(cycles,selected):
    s={frozenset((a,b)) for a,b in selected}
    hist={i:0 for i in range(9)}
    for ring in cycles:
        k=sum(frozenset((a,b)) in s for a,b in zip(ring,ring[1:]+ring[:1]))
        hist[k]+=1
    return hist

def F(T,beta):
    sig=np.linalg.svd(T,compute_uv=False)
    v=beta*sig/2
    return float(-(2/beta)*sum(np.logaddexp(v,-v)))
def main(path=None):
    B,edges,G=build()
    rings=loops_length8(G)
    assert len(rings)==1620,(len(rings))
    old=json.loads((Path(__file__).resolve().parents[1]/"data/w33_20261109_minimal_15_flux_lift.json").read_text())
    opt=json.loads((Path(__file__).resolve().parents[1]/"data/w33_20261109_flux_mass_gap_design.json").read_text())
    masks={
      "flat":[],
      "minimal_original":[(x["point"],40+x["line"]) for x in old["constructed_phase_only_pi_flip_links"]],
      "minimal_gap_optimized":[(x["point"],40+x["line"]) for x in opt["best_15_edges"]]}
    phases={}
    spectrum={}
    for name,changes in masks.items():
        hist=edge_phase_count(rings,changes)
        odd=sum(v for k,v in hist.items() if k%2)
        T=B.astype(int)
        for p,l in changes:T[p,l-40]=-1
        sig=np.linalg.svd(T,compute_uv=False)
        phases[name]={"number_pi_modified_edges":len(changes),
           "octagons_odd_pi_flux":odd,
           "octagons_zero_pi_flux":1620-odd,
           "octagons_by_changed_edge_intersection_count":hist,
           "Wilson_action_per_unit_plaquette_coupling":2*odd,
           "hop_min_singular":float(sig[-1]),
           "hop_rank":int(sum(sig>1e-9))}
        spectrum[name]=T
    assert phases["flat"]["Wilson_action_per_unit_plaquette_coupling"]==0
    assert phases["minimal_original"]["octagons_odd_pi_flux"]>0

    ed,volts,_,_,_,picked,_=prep()
    from itertools import product
    deck=[]
    def builddeck(c):
        b=np.zeros((80,80),int)
        for (a,v),vol in zip(ed,volts):
            s=(-1)**int(np.asarray(c)@vol)
            b[a,v]=b[v,a]=s
        # nonzero ±1 edges and symmetric; its 80 eigenvalues ±sigma
        ee=np.linalg.eigvalsh(b)
        return ee
    # For each deck c, count shortest-cycle Wilson pi-frustrations using
    # the same independently embedded W33 graph edges.
    from collections import defaultdict
    import networkx as nx
    DG=nx.Graph()
    DG.add_nodes_from(range(80));DG.add_edges_from(map(tuple,ed))
    drings=loops_length8(DG)
    assert len(drings)==1620
    edgeindex={frozenset((a,b)):i for i,(a,b) in enumerate(ed)}
    for c in product((0,1),repeat=3):
        signs=np.array([int((np.asarray(c)@x)%2) for x in volts])
        odd=0
        for ring in drings:
            flux=sum(signs[edgeindex[frozenset((a,b))]] for a,b in zip(ring,ring[1:]+ring[:1]))
            odd+=flux%2
        eig=builddeck(c)
        deck.append({"character":list(c),
           "octagon_pi_odd_count":int(odd),
           "local_Wilson_action_per_unit_coupling":int(2*odd),
           "finite_half_filled_F_beta1":float(-np.logaddexp(eig/2,-eig/2).sum())})
    # For comparing sectors with different bipartite matrices,
    # F from the 40 positive singulars = -2/beta log(2 cosh..).
    betas=(.5,1.,4.)
    comparisons=[]
    for beta in betas:
        values={name:F(T,beta) for name,T in spectrum.items()}
        # For any proposed nontrivial π configuration x:
        # [F(x)+g² E_oct(x)] - [F(flat)+g²*0] = dF + g²*E.
        cases={}
        for k in ("minimal_original","minimal_gap_optimized"):
            delta=values[k]-values["flat"]
            action=phases[k]["Wilson_action_per_unit_plaquette_coupling"]
            cases[k]={"fermion_free_energy_minus_flat":delta,
              "positive_Wilson_gauge_penalty_per_unit":action,
              "critical_gauge_penalty_weight_to_tie_flat_if_fermion_favors_flux":float(-delta/action) if delta<0 else None}
        comparisons.append({"inverse_temperature":beta,"fermion_free_energies":values,
             "two_flux_cases_compared_to_flat":cases})
    # No fixed preferred gauge coupling g² from W33; even among corners,
    # other U1 phases can potentially lower total action further.
    out={"status":"PASS_W33_LOCAL_OCTAGON_WILSON_ENERGY_VS_15_EDGE_FERMIONIC_FLUX",
     "fundamental_octagon_count":len(rings),
     "existing_TOE61_prior_art":"TOE61 proved all-beta ordering among 8 special deck flux characters; this experiment does NOT claim novelty for octagon counts, three-pi sector, or free-fermion flux phases.",
     "fifteen_edge_cases":phases,
     "three_deck_Z2_corner_octagon_controls":deck,
     "finite_half_filled_free_fermion_vs_positive_local_Wilson_action":comparisons,
     "positive_local_octagon_gauge_energy":"S_mag/kappa=sum_{all1620 8-cycles} (1-cos Wilson_flux); with pi edges each frustrated cycle contributes2",
     "exact_flat_energy_consequence":"S_mag>=0 and pure gauge is a ground configuration for kappa>0; proving *uniqueness up to gauge* for all U1 phases additionally requires octagon cycle lattice to be saturated, not merely rank81 over R.",
     "scope":"This is finite static gauge plus integrated-out free zero-chemical-potential fermion toy thermodynamics on W33, not a solved dynamical gauge vacuum, real physical value of kappa, standard-model chirality, or spontaneous CP. Apparent flat-vs-flux crossing for selected sectors is NOT global minimization over all 81 continuous holonomies.",
     "numerical_controls":"Both 15-edge supports use exactly unit-magnitude ±1 incidences. All 1620 simple 8-cycles are enumerated independently; unmodified flat flux is zero. The three-deck corners use original TOE38 cochains rather than relabeling the selected 15-edge pattern."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("LOCAL_WILSON",json.dumps({"odd15_original":phases["minimal_original"]["octagons_odd_pi_flux"],
         "odd15_optimized":phases["minimal_gap_optimized"]["octagons_odd_pi_flux"],
         "threepi_odd":deck[-1]["octagon_pi_odd_count"],
         "beta1_free_deltas":comparisons[1]["two_flux_cases_compared_to_flat"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
