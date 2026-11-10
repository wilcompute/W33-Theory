#!/usr/bin/env python3
"""Constructive W33 U(1) gauge fixing: 81 measurable chord Wilson syndromes.

Fundamental tree has 79 incidence edges and 81 independent chords.
Every arbitrary phase assignment on all 160 links decomposes into
79 vertex-gauge differences + 81 gauge-invariant chord residuals.
Exactly zero Wilson syndromes iff pure gauge (mod 2pi).
This is graph cohomology, not quantization of any physical photon phase.
"""
import json,math,sys
from pathlib import Path
import numpy as np
import networkx as nx
from w33_20261109_flux_dark_mode_fragility import build,fundamental_flows

def wrap(x):return (x+np.pi)%(2*np.pi)-np.pi

def decode(phi,G):
    tree=nx.bfs_tree(G,0).to_undirected()
    pot=np.full(80,np.nan)
    pot[0]=0.
    for parent,child in nx.bfs_edges(tree,0):
        point,line=(parent,child-40) if parent<40 else (child,parent-40)
        if parent<40:pot[child]=pot[parent]-phi[point,line]
        else:pot[child]=pot[parent]+phi[point,line]
    assert np.all(np.isfinite(pot))
    residual=wrap(phi-(pot[:40,None]-pot[None,40:]))
    for a,b in tree.edges():
        p,l=(a,b-40) if a<40 else (b,a-40)
        assert abs(residual[p,l])<1e-12
    return pot,residual,tree

def main(path=None):
    B,edges,G=build()
    tree,cycles=fundamental_flows(G)
    idx={edge:i for i,edge in enumerate(edges)}
    D=np.zeros((80,160),dtype=int)
    for j,(p,l) in enumerate(edges):
        D[p,j]=1;D[40+l,j]=-1
    C=np.zeros((81,160),dtype=int)
    chordpos=[]
    for row,arcs in enumerate(cycles):
        for p,l,sgn in arcs:C[row,idx[(p,l)]]=sgn
        e=next((p,l) for p,l,sgn in arcs if not tree.has_edge(p,40+l))
        chordpos.append(idx[e])
    assert len(set(chordpos))==81
    Q=C[:,chordpos]
    assert np.array_equal(abs(Q),np.eye(81,dtype=int))
    assert np.array_equal(C@D.T,np.zeros((81,80),dtype=int))
    assert np.linalg.matrix_rank(D)==79
    rng=np.random.default_rng(2026110969)
    alpha=rng.uniform(-3,3,40)
    beta=rng.uniform(-3,3,40)
    gauge=np.where(B>0,alpha[:,None]-beta[None,:],0)
    pot,delta,_=decode(gauge,G)
    assert max(abs(delta[B>0]))<1e-12
    phi=np.where(B>0,rng.uniform(-1,1,(40,40)),0)
    pot,r,_=decode(phi,G)
    active=np.array([r[p,l] for p,l in edges])
    assert abs(max(abs(active))-max(abs(active[chordpos])))<1e-12
    assert np.sum(abs(active)>1e-9)==81
    flux_syndrome=wrap(C@np.array([phi[p,l] for p,l in edges]))
    chord_res=np.array([r[edges[i][0],edges[i][1]] for i in chordpos])
    assert np.max(abs(wrap(flux_syndrome- np.diag(Q)*chord_res)))<1e-12
    assert np.max(abs(wrap((phi+gauge)[B>0]-phi[B>0]-gauge[B>0])))<1e-12
    _,shift,_=decode(np.where(B>0,phi+gauge,0),G)
    assert np.max(abs(wrap((shift-r)[B>0])))<1e-12
    # Rebuild full twisted incidence from decoded gauge+holonomy.
    P=np.diag(np.exp(1j*pot[:40]))
    L=np.diag(np.exp(-1j*pot[40:]))
    reconst=P@(B*np.exp(1j*r))@L
    original=B*np.exp(1j*phi)
    assert np.max(abs(reconst-original))<1e-12
    result={"status":"PASS_W33_81_INDEPENDENT_WILSON_SYNDROME_GAUGE_DECODER",
     "native_80_vertex_160_edge_incidence":{
        "vertices":80,"links":160,"spanning_tree_links":79,
        "off_tree_chords":81},
     "exact_81_by_81_chord_syndrome_submatrix":"signed diagonal with ±1 entries",
     "cycle_matrix_times_gradient_transpose_zero":True,
     "vertex_edge_boundary_rank":79,
     "cycle_rank":81,
     "pure_gauge_residual_max_abs_radians":float(max(abs(delta[B>0]))),
     "generic_flux_independent_nonzero_chords":int(sum(abs(active)>1e-9)),
     "canonical_reconstructed_twisted_incidence_max_error":float(np.max(abs(reconst-original))),
     "under_vertex_rephasing_canonical_chord_residual_max_error":float(np.max(abs(wrap((shift-r)[B>0])))),
     "interpretation":"Every 160-element U1 edge configuration on connected W33 Levi graph has 79 removable gauge degrees and 81 physically gauge-invariant chord fluxes. All 81 vanish iff phase assignment is vertex gauge (mod 2pi), which preserves W33 rank25/30 dark modes. A nonzero flux does not automatically lift all 30 but can do so; generic independent phases have full rank in the companion experiment.",
     "prior_art":"Graph cycle space/homology rank 81 and 1620 minimal W33 octagons already documented in repo. This executable constructive decoder is a native-geometry witness, not a novel continuum field theory.",
     "scope":"A purely finite U(1) tight-binding gauge model with exact phases. Real experiments must estimate Wilson loop phases with uncertainty and account for losses, nonuniform hopping, source preparation and detector imperfections. No physical gauge coupling constant, spacetime continuum or dynamical gauge equations derived."}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FLUX_SYNDROME",json.dumps({"tree":79,"chords":81,
     "reconstruction_error":result["canonical_reconstructed_twisted_incidence_max_error"],
     "gauge_error":result["under_vertex_rephasing_canonical_chord_residual_max_error"]}))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
