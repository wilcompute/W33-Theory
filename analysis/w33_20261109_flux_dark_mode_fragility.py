#!/usr/bin/env python3
"""W33 incidence: exact flat U(1) gauge invariance versus physical cycle flux.

160 links, 80 vertices, 81 independent cycle holonomies. Pure vertex
gauge phases preserve rank 25 and 15+15 dark sectors. Independent link
flux generically destroys that rank deficiency. A single physical edge
phase raises rank exactly 1 => 28 instead of 30 chiral zero modes.
No claim of gravity, actual photonic experiment, or physical gauge law.
"""
import json,sys,math
from pathlib import Path
import numpy as np
import networkx as nx
from w33_20261109_point_line_30_zero_modes import action

def build():
    pts,lines,inc,_=action()
    B=np.zeros((40,40),float)
    edges=[]
    for i,li in enumerate(inc):
        for j in li:B[i,j]=1.;edges.append((i,j))
    G=nx.Graph()
    G.add_nodes_from(range(80))
    G.add_edges_from((i,40+j) for i,j in edges)
    assert nx.is_connected(G)
    assert G.number_of_nodes()==80 and G.number_of_edges()==160
    assert len(nx.cycle_basis(G))==81
    return B,edges,G

def fundamental_flows(G):
    tree=nx.bfs_tree(G,0).to_undirected()
    assert tree.number_of_edges()==79
    chords=sorted(set(tuple(sorted(x)) for x in G.edges())-
                  set(tuple(sorted(x)) for x in tree.edges()))
    assert len(chords)==81
    cycles=[]
    for a,b in chords:
        path=nx.shortest_path(tree,a,b)
        arcs=list(zip(path,path[1:]))+[(b,a)]
        signs=[]
        for x,y in arcs:
            p,l=(x,y-40) if x<40 else (y,x-40)
            signs.append((p,l,1 if x<40 else -1))
        cycles.append(signs)
    return tree,cycles

def holonomy(phi,cycles):
    arr=np.array([sum(sign*phi[p,j] for p,j,sign in arcs) for arcs in cycles])
    return (arr+np.pi)%(2*np.pi)-np.pi

def dim(T):
    s=np.linalg.svd(T,compute_uv=False)
    return int(sum(s>1e-9)),float(s[-1]),float(s[24]),float(s[25])
def main(path=None):
    B,edges,G=build()
    _,cycles=fundamental_flows(G)
    rng=np.random.default_rng(20261109)
    alpha=rng.uniform(-np.pi,np.pi,40)
    beta=rng.uniform(-np.pi,np.pi,40)
    pure=(alpha[:,None]-beta[None,:])*B
    Tpure=B*np.exp(1j*pure)
    rank0,_,_,_=dim(Tpure)
    assert rank0==25
    sv0=np.linalg.svd(B,compute_uv=False)
    svg=np.linalg.svd(Tpure,compute_uv=False)
    assert np.max(abs(sv0-svg))<1e-12
    assert max(abs(holonomy(pure,cycles)))<1e-12
    # Projected symmetry gauge is a genuine unitary equivalence, not an
    # independent link-phasing mechanism with arbitrary Wilson holonomies.
    P=(8*np.eye(40)-4*(B@B.T-4*np.eye(40))+np.ones((40,40)))/24
    D=np.diag(np.exp(1j*alpha))
    Pg=D@P@D.conj().T
    assert abs(np.trace(Pg)-15)<1e-12
    assert np.max(abs(Tpure.conj().T@Pg))<1e-12

    u,v=edges[0]
    theta=math.pi/5
    one=B.astype(complex)
    one[u,v]=np.exp(1j*theta)
    rank1,_,_,_=dim(one)
    assert rank1==26
    cycle_one=holonomy(np.zeros((40,40)),cycles) # zero-flux control
    assert np.max(abs(cycle_one))<1e-12
    singlephi=np.zeros((40,40));singlephi[u,v]=theta
    flux=holonomy(singlephi,cycles)
    assert sum(abs(flux)>1e-8)>=1
    # Gauge-equivalent changed flux preserves all 40 singular values.
    one_g=np.diag(np.exp(1j*alpha))@one@np.diag(np.exp(-1j*beta))
    assert np.max(abs(np.linalg.svd(one_g,compute_uv=False)-
                      np.linalg.svd(one,compute_uv=False)))<1e-12
    assert np.max(abs(holonomy(singlephi+pure,cycles)-flux))<1e-12

    match=nx.algorithms.bipartite.maximum_matching(G,top_nodes=range(40))
    selected=sorted((u,match[u]-40) for u in range(40))[:15]
    assert len(selected)==15 and len({a for a,b in selected})==15
    assert len({b for a,b in selected})==15
    kcontrols=[]
    for k in (0,1,2,3,5,8,10,12,15):
        K=B.astype(complex)
        for ix,(p,l) in enumerate(selected[:k]):
            K[p,l]=np.exp(1j*(.55+.007*ix))
        rk,mn,s24,s25=dim(K)
        assert rk<=25+k
        assert 80-2*rk>=max(0,30-2*k)
        kcontrols.append({"independently_detuned_edges":k,
                "matrix_rank":rk,"dark_zero_modes":80-2*rk,
                "rigorous_rank_upper_bound":min(40,25+k),
                "rigorous_zero_mode_lower_bound":max(0,30-2*k),
                "smallest_singular_value":mn})
    many=B*np.exp(1j*rng.uniform(-.9,.9,size=(40,40))*B)
    fullrank,minsv,_,_=dim(many)
    assert fullrank==40
    # Any putative "topologically protected" dark spectrum on this finite
    # bipartite graph must specify which flux or symmetry perturbations
    # are allowed: generic physically gauge-invariant loops lift all.
    # The native incidence graph girth is 8 (prior repo result).
    cycles_len=[]
    for a,b in G.edges():
        H=G.copy();H.remove_edge(a,b)
        cycles_len.append(nx.shortest_path_length(H,a,b)+1)
    assert min(cycles_len)==8
    result={"status":"PASS_W33_81_U1_FLUX_CYCLES_AND_RANK_FRAGILITY",
     "vertices":80,"edges":160,"connected_components":1,
     "cycle_space_dimension_E_minus_V_plus_1":81,
     "shortest_incidence_cycle_edges":min(cycles_len),
     "number_fundamental_Wilson_holonomies":len(cycles),
     "pure_gauge_spectrum_max_error":float(max(abs(sv0-svg))),
     "pure_gauge_max_cycle_flux_abs":float(max(abs(holonomy(pure,cycles)))),
     "pure_gauge_dark_mode_count":80-2*rank0,
     "one_detuned_incidence_edge":[u,v],
     "one_edge_phase":theta,
     "one_edge_rank":rank1,
     "one_edge_chiral_zero_modes":80-2*rank1,
     "single_edge_number_nonzero_independent_Wilson_holonomies":int(sum(abs(flux)>1e-8)),
     "single_edge_flux_gauge_invariance_max_error":float(np.max(abs(holonomy(singlephi+pure,cycles)-flux))),
     "independent_disjoint_edge_detuning_controls":kcontrols,
     "generic_nonzero_flux_rank":fullrank,
     "generic_nonzero_flux_smallest_singular_value":minsv,
     "gauge_covariant_dark_projector_error":float(max(abs(Tpure.conj().T@Pg).ravel())),
     "exact_mathematical_claim":"Any 80-node bipartite W33 incidence network has 81 independent U(1) cycle phases. Vertex rephasings preserve rank25 and 30 zero modes. Changing k individual incidence entries increases rank by at most k, leaving >=max(0,30-2k) zero modes. The single nontrivial incidence edge change always raises rank to26 because both endpoint standard basis vectors have nonzero projections onto the left/right 15D kernels. The generic all-link phase assignment is full rank40, so flat-band degeneracy is not protected under unrestricted physical flux.",
     "scope":"Finite chiral one-body tight-binding graph and U1 edge phase model only. Prior repo already established E−V+1=81 and 1620 minimal 8-cycles. This test adds transparent rank/flux comparison with explicit symmetry hypotheses; neither a continuum chiral index nor a physical photon/gravity derivation."}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("W33_FLUX",json.dumps({"flat":80-2*rank0,"single":80-2*rank1,
      "full_flux_rank":fullrank,"cycle_rank":81,
      "k": [(x["independently_detuned_edges"],x["dark_zero_modes"]) for x in kcontrols]}))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
