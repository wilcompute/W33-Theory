#!/usr/bin/env python3
import itertools,json
from pathlib import Path
import numpy as np,networkx as nx
OUT=Path(__file__).resolve().parents[1]/'data/PART_W33_PASS4986_TWIN_DARK15_LEVI_OBSTRUCTION.json'
def canon(v):
    for x in v:
        if x%3:
            z=1 if x%3==1 else 2
            return tuple((z*y)%3 for y in v)
def sp(a,b): return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
def gf2rank(M):
    piv={}
    for row in M%2:
        x=sum(int(b)<<i for i,b in enumerate(row) if b)
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)
def main():
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    G=nx.Graph();G.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if sp(P[i],P[j])==0:G.add_edge(i,j)
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==4)
    Z=np.zeros((40,40),dtype=int)
    for j,L in enumerate(lines):
        for p in L:Z[p,j]=1
    A=nx.to_numpy_array(G,nodelist=range(40),dtype=int);Q=Z.T@Z-4*np.eye(40,dtype=int)
    Pp=A@A-14*A+24*np.eye(40,dtype=int);Pl=Q@Q-14*Q+24*np.eye(40,dtype=int)
    assert np.linalg.matrix_rank(Pp)==15 and np.linalg.matrix_rank(Pl)==15
    assert not np.any(Pp@Z) and not np.any(Z@Pl)
    Levi=np.block([[np.zeros((40,40),dtype=int),Z],[Z.T,np.zeros((40,40),dtype=int)]);nullity=80-np.linalg.matrix_rank(Levi)
    assert (np.linalg.matrix_rank(Z),nullity,gf2rank(A),gf2rank(Q))==(25,30,16,10)
    out={'pass':4986,'point_module':'1+24+15_p','line_module':'1+24+15_l','exact_zero_channels':['P15_point Z = 0','Z P15_line = 0'],'Levi':{'incidence_rank':25,'nullity':30,'nullspace':'15_p (+) 15_l'},'nonisomorphism_certificate':{'GF2_adjacency_rank_point':16,'GF2_adjacency_rank_line':10,'incidence_preserving_side_swap_exists':False},'theorem':'The point-side and line-side dark fifteens are inequivalent twins. Incidence kills both, and the Levi nullspace is their direct 30-dimensional sum. Different binary adjacency ranks rule out an incidence-preserving point-line side swap.','boundary':'Pass4977 already rules out the ordinary PGSp outer twist as a 15-to-15 bridge.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
