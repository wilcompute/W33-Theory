#!/usr/bin/env python3
"""Pass7489: resolve the 'third 1440' as marked sixer triples, not a 1440-order stabilizer.

The cubic-surface line configuration has 72 sixers, paired into 36 double-sixes.  The
Brosowsky-style 20x72 count is therefore the set of pairs (sixer, 3-subset of its six
lines).  This script reconstructs the 72/36 objects from the existing finite model and
verifies the 1440=72*C(6,3)=36*40 bundle exactly.  Group-theoretic orders are then read
through the already-certified W(E6) action: sixer stabilizer S6 (720), marked triple
stabilizer S3xS3 (36), double-six stabilizer 1440.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import networkx as nx
import bt1796_double_six_quotient_gauge as q
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7489_THIRD1440_MARKED_SIXER_BUNDLE.json'

def main():
    lines=q.support();G=nx.Graph();G.add_nodes_from({p for L in lines for p in L})
    for L in lines:
        for a,b in itertools.combinations(L,2):G.add_edge(a,b)
    S=nx.complement(G)
    sixers=sorted({tuple(sorted(c)) for c in nx.find_cliques(S) if len(c)==6})
    assert len(sixers)==72
    sid={s:i for i,s in enumerate(sixers)}
    double=[];partner={}
    for i,j in itertools.combinations(range(72),2):
        A=set(sixers[i]);B=set(sixers[j])
        if A&B:continue
        cross=[(a,b) for a in A for b in B if S.has_edge(a,b)]
        if len(cross)==6 and len({a for a,b in cross})==6 and len({b for a,b in cross})==6:
            double.append((i,j));partner[i]=j;partner[j]=i
    assert len(double)==36 and len(partner)==72 and all(partner[partner[i]]==i for i in range(72))
    marked=[]
    for i,s in enumerate(sixers):
        for T in itertools.combinations(s,3):marked.append((i,tuple(T)))
    assert len(marked)==1440 and len(set(marked))==1440
    fibers={tuple(sorted((i,j))):[] for i,j in double}
    for i,T in marked:fibers[tuple(sorted((i,partner[i])))].append((i,T))
    assert set(map(len,fibers.values()))=={40}
    # Complementing a marked triple inside its sixer is a fixed-point-free involution.
    comp={}
    for i,T in marked:
        U=tuple(sorted(set(sixers[i])-set(T)));comp[(i,T)]=(i,U)
    assert all(comp[comp[x]]==x and comp[x]!=x for x in comp)
    complement_pairs=len(comp)//2;assert complement_pairs==720
    # In each double-six fibre there are two 20-element sixer halves and 20 complement pairs per half.
    fibre_half_profiles=[]
    for D,F in fibers.items():
        h={i:sum(1 for j,T in F if j==i) for i in D};assert sorted(h.values())==[20,20]
        fibre_half_profiles.append(tuple(sorted(h.values())))
    W=51840
    assert W//72==720 and W//1440==36 and W//36==1440
    out={
      'schema':'w33.pass7489.third1440_marked_sixer_bundle.v1','status':'PASS',
      'cubic_surface_counts':{'sixers':72,'double_sixes':36,'marked_triples_per_sixer':20,'marked_sixer_triples':1440},
      'bundle':'1440 = 72*20 = 36*40; each double-six fibre consists of the 20 marked triples on each of its two sixers',
      'triple_complement_involution':{'fixed_point_free':True,'pairs':720},
      'W_E6_order':W,
      'orbit_stabilizer':{
        'sixer_orbit':{'size':72,'stabilizer_order':720,'stabilizer_structure':'S6'},
        'marked_sixer_triple_orbit':{'size':1440,'stabilizer_order':36,'stabilizer_structure':'S3 x S3'},
        'double_six_orbit':{'size':36,'stabilizer_order':1440},
        'double_six_stabilizer_on_its_marked_fibre':{'fibre_size':40,'point_stabilizer_order':36}
      },
      'resolution':'The previous two 1440s are stabilizer ORDERS of spread/double-six vertices. The Brosowsky 20x72 quantity is instead an ORBIT SIZE. They are not three instances of the same type of invariant.',
      'stronger_bridge':'The numerical collision is explained by a homogeneous bundle: W(E6)/36 -> W(E6)/1440 has fibre size 40, i.e. marked sixer triples project to double-sixes.',
      'boundary':'Finite cubic-surface/W(E6) combinatorics only; no physical identification is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','sixers':72,'double_sixes':36,'marked':1440,'fibre':40}))
if __name__=='__main__':main()
