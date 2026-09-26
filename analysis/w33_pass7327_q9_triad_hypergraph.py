#!/usr/bin/env python3
"""Pass7327: intrinsic arithmetic and symmetry of the 103 special q=9 blocker triads."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from w33_pass7107_q9_target_52 import build
import w33_pass7130_7137_structural_attack as s

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7327_Q9_TRIAD_HYPERGRAPH.json'
S=s.S9

def gf2rank(A):
    piv={}
    for row in A:
        x=sum((int(v)&1)<<i for i,v in enumerate(row))
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    return len(piv)

def main():
    P,adj,B=build();Sset=set(S);special=[];counts=Counter()
    for a,b,c in itertools.combinations(range(51),3):
        z=len(adj[S[a]]&adj[S[b]]&adj[S[c]]);counts[z]+=1
        if z==10:special.append((a,b,c))
    assert counts==Counter({1:20722,10:103}) and len(special)==103
    H=np.zeros((103,51),dtype=np.int64);deg=Counter();pair=Counter()
    for r,e in enumerate(special):
        for x in e:H[r,x]=1;deg[x]+=1
        for p in itertools.combinations(e,2):pair[tuple(sorted(p))]+=1
    assert gf2rank(H)==51
    D=smith_normal_form(sp.Matrix(H),domain=sp.ZZ);diag=[abs(int(D[i,i])) for i in range(51)];snf=Counter(diag)
    # Colored incidence graph automorphisms.
    G=nx.Graph()
    for i in range(51):G.add_node(('p',i),kind='p',deg=int(deg[i]))
    for r,e in enumerate(special):
        G.add_node(('e',r),kind='e',deg=3)
        for i in e:G.add_edge(('p',i),('e',r))
    nm=nx.algorithms.isomorphism.categorical_node_match(['kind','deg'],[None,None])
    autos=list(nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=nm).isomorphisms_iter())
    pointperms={tuple(m[('p',i)][1] for i in range(51)) for m in autos};aut_order=len(pointperms)
    # Certified geometric involution A9 on the witness.
    pidx={p:i for i,p in enumerate(P)};pos={v:i for i,v in enumerate(S)}
    perm=[]
    for idx in S:
        y=s.norm9(tuple(s.matvec9(s.A9,P[idx])));j=pidx[y];assert j in Sset;perm.append(pos[j])
    perm=tuple(perm);assert tuple(range(51)) in pointperms and perm in pointperms
    # Weighted 2-section fingerprint.
    W=np.zeros((51,51),dtype=np.int64)
    for (i,j),m in pair.items():W[i,j]=W[j,i]=m
    eig=np.linalg.eigvalsh(W.astype(float));eh=Counter(round(float(x),8) for x in eig)
    out={'schema':'w33.pass7327.q9_triad_hypergraph.v1','status':'PASS','vertices':51,'hyperedges':103,'uniformity':3,
      'triad_center_distribution':{'1':20722,'10':103},'GF2_incidence_rank':51,
      'integer_SNF':{str(k):v for k,v in sorted(snf.items())},
      'vertex_degree_histogram':{str(k):v for k,v in sorted(Counter(deg.values()).items())},
      'pair_multiplicity_histogram':{str(k):v for k,v in sorted(Counter(pair.values()).items())},
      'incidence_hypergraph_automorphism_order':aut_order,'geometric_C2_involution_present':perm in pointperms,
      'point_automorphisms':[list(p) for p in sorted(pointperms)[:10]],
      'weighted_2section_spectrum_rounded':{str(k):v for k,v in sorted(eh.items())},
      'theorem':('The 103 ten-center triads have automorphism group exactly the same C2 as the q=9 witness stabilizer; the third blocker moment alone recovers the surviving witness symmetry.' if aut_order==2 else 'The 103-triad hypergraph has the displayed intrinsic automorphism group; it contains the certified geometric C2 and therefore supplies a strictly q=9-native symmetry reduction object.'),
      'solver_use':'Hypergraph automorphism orbits and full-rank incidence can be used as symmetry-breaking/cutting data in target-48 searches; they are not themselves an alpha=51 proof.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','aut':aut_order,'SNF':out['integer_SNF']}))
if __name__=='__main__':main()
