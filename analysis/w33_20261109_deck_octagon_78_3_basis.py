#!/usr/bin/env python3
"""Unimodular 78+3 octagon splitting relative to TOE38's 3-deck lift.

Old TOE38 1382 0-deck-winding octagons have rank 78 over R and admit
3 missing harmonic deck holonomies. Ask whether an exact 78+3 selection
of *actual 8-cycles* gives a unit integer minor for the entire Z81
cycle lattice, proving no residual torsion when winding loops included.
"""
import json,sys,numpy as np,networkx as nx
from pathlib import Path
from sympy import Matrix
from w33_20261109_full_octagon_integer_gauge_basis import loops_length8,rankmod,pivot_mod2
from w33_20261010_toe38_local_maxwell_2complex import prep

def main(path=None):
    ed,volts,lookup,zero,comm,picked,fc=prep()
    E=[tuple(map(int,x)) for x in ed]
    DG=nx.Graph()
    DG.add_nodes_from(range(80));DG.add_edges_from(E)
    G=nx.bfs_tree(DG,0).to_undirected()
    chords=sorted({frozenset(e) for e in DG.edges()}-
                  {frozenset(e) for e in G.edges()},key=lambda x:sorted(x))
    assert len(chords)==81
    ci={z:i for i,z in enumerate(chords)}
    ei={frozenset(e):i for i,e in enumerate(E)}
    rings=loops_length8(DG)
    assert len(rings)==1620
    W=np.zeros((len(rings),81),dtype=int)
    wind=[]
    for k,ring in enumerate(rings):
        charge=np.zeros(3,int)
        for a,b in zip(ring,ring[1:]+ring[:1]):
            e=ei[frozenset((a,b))]
            sign=1 if a==E[e][0] else -1
            charge+=sign*volts[e]
            if frozenset((a,b)) in ci:
                W[k,ci[frozenset((a,b))]]+=sign
        wind.append(tuple(int(t) for t in charge))
    z=[k for k,x in enumerate(wind) if x==(0,0,0)]
    nz=[k for k,x in enumerate(wind) if x!=(0,0,0)]
    assert len(z)==1382 and len(nz)==238
    rank_zero={str(p):rankmod(W[z],p) for p in (2,3,5)}
    rank_all={str(p):rankmod(W,p) for p in (2,3,5)}
    assert all(r==78 for r in rank_zero.values()),rank_zero
    assert all(r==81 for r in rank_all.values()),rank_all
    ordering=z+nz
    selected_local_indices=pivot_mod2(W[ordering])
    chosen=[ordering[k] for k in selected_local_indices]
    chosen_zero=sum(k in set(z) for k in chosen)
    assert len(chosen)==81 and chosen_zero==78
    det=int(Matrix(W[chosen].tolist()).det(method="domain-ge"))
    assert abs(det)==1,det
    indep_wind=[wind[k] for k in chosen if k in set(nz)]
    assert len(indep_wind)==3
    out={"status":"PASS_W33_EXACT_UNIMODULAR_78_PLUS_3_OCTAGON_DECK_SPLIT",
      "old_TOE38_local_zero_winding_octagons":1382,
      "old_TOE38_nonzero_three_deck_winding_octagons":238,
      "all_length8_octagons":1620,
      "local_zero_deck_octagon_integer_chord_rank_mod_primes":rank_zero,
      "full_octagon_integer_chord_rank_mod_primes":rank_all,
      "explicit_integer_Z81_basis_from_exact_actual_octagons":{
          "zero_deck_octagons":78,
          "nonzero_deck_octagons":3,
          "determinant":str(det),
          "selected_indices_into_canonical_1620_octagon_list":chosen,
          "three_selected_deck_winding_vectors":indep_wind},
      "strong_consequence":"For an action on ALL 1620 shortest loops, 78 actual zero-deck-winding and 3 actual nonzero-deck-winding octagons have an integer 81x81 unimodular cycle matrix. Their vanishing U1 holonomies enforce pure gauge, with no residual discrete torsion; positive Wilson all-octagon ground up to gauge is flat. In the previous TOE38 skeleton, the 1382 local octagons alone have rank 78, so cannot constrain the three deck-harmonic directions. The two actions are physically distinct.",
      "scope":"This supplements existing TOE38 established 1382/238 split and 78 local rank. New feature is a 78+3 exact integral unimodular certificate selecting ONLY genuine shortest octagons. Adding winding cycles to the action can be physically nonlocal in a spatial three-deck embedding. A finite cycle rank and unique gauge orbit are not derivations of 3D space, quantum gravity, coupling constants or measured SM physics."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("DECK_UNIMODULAR",json.dumps({"ranklocal":rank_zero,"rankfull":rank_all,
          "counts":[chosen_zero,len(chosen)-chosen_zero],"det":str(det),
          "windings":indep_wind}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
