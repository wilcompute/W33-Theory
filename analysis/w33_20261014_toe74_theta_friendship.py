"""TOE74: exact theta(4,4,4) Z2 corner degeneracy and three-triangle
quantum-cover compression.

Corrects the earlier TOE73 claim of interaction-induced switching among
three purportedly different Z2 corners: those sectors are isospectral by
the native S3 arm-permutation symmetry. Extends the compressed star
K1,6 to a friendship graph of three triangles using directly enumerated
seed-to-seed two-vertex transitions. Does NOT claim all orbit transitions.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_two_octagon_covariance import patch
from w33_20261014_toe74_quantum_neighbors import certificate as cover_cert

def theta_symmetry():
    p=patch()
    adj=[[] for _ in p["nodes"]]
    for edge,(a,b) in enumerate(p["p_ed"]):
        adj[a].append((b,edge));adj[b].append((a,edge))
    hubs=[i for i,a in enumerate(adj) if len(a)==3]
    assert len(hubs)==2 and all(len(a) in (2,3) for a in adj)
    assert sum(len(a)==2 for a in adj)==9
    h0,h1=sorted(hubs)
    routes=[]
    for neighbor,_ in adj[h0]:
        row=[h0,neighbor]
        prior,now=h0,neighbor
        while now!=h1:
            candidates=[b for b,e in adj[now] if b!=prior]
            assert len(candidates)==1
            nxt=candidates[0]
            row.append(nxt);prior,now=now,nxt
        assert len(row)==5
        routes.append(row)
    routes.sort(key=lambda path:path[1])
    assert len(routes)==3
    assert len({v for row in routes for v in row[1:-1]})==9
    assert {v for row in routes for v in row}==set(range(11))
    assert all([p["background"][v] for v in row]==
               [p["background"][v] for v in routes[0]] for row in routes)
    edge_set={frozenset((a,b)) for a,b in p["p_ed"]}
    automorphisms=[]
    for perm in itertools.permutations(range(3)):
        trans={h0:h0,h1:h1}
        for i,route in enumerate(routes):
            for t in (1,2,3):trans[route[t]]=routes[perm[i]][t]
        assert len(trans)==11
        assert {frozenset((trans[a],trans[b])) for a,b in p["p_ed"]}==edge_set
        assert all(p["background"][trans[i]]==p["background"][i] for i in range(11))
        automorphisms.append([int(trans[i]) for i in range(11)])
    # Fundamental winding vectors for all THREE simple octagons:
    # each is made of two distinct length-four routes. For nontrivial
    # Z2 holonomy, precisely two of these three cycle phases are pi.
    shifts=[tuple(int(x) for x in row) for row in p["P"][:,p["chords"]]]
    sectors={}
    for t in itertools.product((0,1),repeat=2):
        cycle_pi=tuple((a*t[0]+b*t[1])%2 for a,b in shifts)
        sectors["".join(map(str,t))]=list(cycle_pi)
    assert sectors["00"]==[0,0,0]
    nontriv=[tuple(sectors[t]) for t in ("01","10","11")]
    assert len(set(nontriv))==3
    assert all(sum(row)==2 for row in nontriv)
    return {
     "status":"PASS_TOE74_THETA_TRIPLE_Z2_ISOSPECTRALITY",
     "native_graph_sites_edges":[11,12],
     "degree_three_hubs":hubs,
     "native_three_equal_four_edge_routes":routes,
     "independent_cycle_rank":2,
     "three_octagon_windings_in_chords":shifts,
     "S3_arm_permutation_automorphisms":automorphisms,
     "four_Z2_cycle_parities":sectors,
     "all_three_nontrivial_Z2_corners_unitarily_equivalent":True,
     "theorem":"Three length-4 internally disjoint paths form Theta(4,4,4). S3 freely permutes its arms, preserving all nearest-neighbor density interactions and the bipartition. The three nonzero Z2 flux classes have cycle-parity multisets (pi,pi,0), hence S3 permutes them. Their full canonical finite-N Hamiltonians, spectra and Helmholtz free energies are unitarily equivalent for every V and beta.",
     "correction":"TOE73's changes in the nominal best corner among (pi,0),(0,pi),(pi,pi) reflect numerical tie-breaking, NOT a physical or mathematical flux switching transition.",
     "scope":"Exact for the specified 11-site static-Z2 theta-graph Hamiltonian, not the full 80-site W33 theorem or dynamical 4D gauge theory."}

def friendship_compression():
    c=cover_cert()
    rows=c["neighborhood_summary"]
    assert len(rows)==7
    A=np.zeros((7,7),dtype=np.int64)
    for i,row in enumerate(rows):
        for j in range(7):
            if i==j:continue
            A[i,j]=int(row["links_to_other_six_given_representatives"][str(j)])
    assert np.array_equal(A,A.T)
    assert np.sum(A[0])==6
    expected_extra={(1,2),(3,4),(5,6)}
    assert {tuple((i,j)) for i in range(1,7) for j in range(i+1,7)
            if A[i,j]}==expected_extra
    assert int(A.sum())//2==9
    tri=sum(int(A[i,j]*A[i,k]*A[j,k]) for i in range(7)
            for j in range(i+1,7) for k in range(j+1,7))
    assert tri==3
    eig=np.linalg.eigvalsh(A)
    target=np.sort(np.array([-2]+[-1]*3+[1]*2+[3],dtype=float))
    assert max(abs(eig-target))<1e-12
    # All 7 full group orbits are regular PGSp sets, with trivial
    # stabilizers, so each of the 9 seed edges transports uniquely
    # across the group to a perfect matching of size |PGSp|=51840.
    group=51840
    return {
     "status":"PASS_TOE74_NINE_MATCHING_FRIENDSHIP_GRAPH",
     "seed_seven_by_seven_adjacency":A.tolist(),
     "seed_graph_vertices":7,"seed_graph_edges":9,"seed_graph_triangles":3,
     "seed_graph_is_friendship_F3":True,
     "full_group_regular_orbit_size":group,
     "nine_full_group_equivariant_matchings":9,
     "exact_edges_in_deliberately_compressed_graph":9*group,
     "disconnected_friendship_components_in_deliberately_compressed_graph":group,
     "adjacency_eigenvalue_multiplicities":{"3":group,"-2":group,
         "1":2*group,"-1":3*group},
     "proof":"Six center-leaf moves and three independently found leaf-leaf moves (1,2), (3,4), (5,6) are exact 2-vertex changes preserving twenty loops. Free transitive PGSp action transports each to a perfect matching between two different 51840-cover orbits. Retaining ONLY these nine transported edge classes yields 51840 disjoint copies of friendship graph F3, with exact spectrum (3,-2,1^2,(-1)^3).",
     "scope":"The nine-matching compressed model is NOT the full induced seven-orbit graph; other within- and outside-orbit transitions were not classified. It is not emergent spacetime or physical gravity."}

def certificate():
    return {"status":"PASS_TOE74_THETA_AND_QUANTUM_TRIANGLE_CORRECTION",
            "theta":theta_symmetry(),"quantum":friendship_compression()}
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe74_theta_and_friendship.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],c["quantum"]["exact_edges_in_deliberately_compressed_graph"])
