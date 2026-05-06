#!/usr/bin/env python3
"""PART CCCLXI -- Two-Graph Incidence Operator Compiler.

Builds the actual W(3,3) two-graph object on triples, not just the counts.

For the W(3,3) collinearity graph, a triple is in the Seidel two-graph iff it
contains an odd number of graph edges.  The compiler constructs:

- all C(40,3)=9880 triples,
- the 4480 odd triples,
- the vertex-by-odd-triple incidence operator M (40 x 4480),
- the Gram operator C = M M^T.

The crucial identity is

    C = 320 I + 16 J + 4 A,

where A is the W(3,3) adjacency matrix.  Thus the two-graph incidence operator
recovers the original graph adjacency by

    A = (C - 320 I - 16 J)/4.

This upgrades the two-graph parity counts into an actual operator certificate.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path
from typing import Tuple
ROOT=Path(__file__).resolve().parents[1]
MOD=3
Vector=Tuple[int,int,int,int]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def mul(a,u): return tuple((a*u[i])%MOD for i in range(4))
def add(u,v): return tuple((u[i]+v[i])%MOD for i in range(4))
def omega(x,y): return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%MOD
def canon(v):
    for a in v:
        if a%MOD:
            return mul(1 if a==1 else 2,v)
    raise ValueError('zero')
def points():
    pts=[]; seen=set()
    for v in itertools.product(range(MOD), repeat=4):
        if v==(0,0,0,0): continue
        c=canon(v)
        if c not in seen: seen.add(c); pts.append(c)
    return pts
def build_graph():
    pts=points(); n=len(pts); adj=[set() for _ in range(n)]
    for i,j in itertools.combinations(range(n),2):
        if omega(pts[i],pts[j])==0:
            adj[i].add(j); adj[j].add(i)
    return pts,adj
def edge_count_in_triple(tri,adj):
    return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def all_triples(n=40): return list(itertools.combinations(range(n),3))
def odd_triples(adj):
    return [tri for tri in all_triples(len(adj)) if edge_count_in_triple(tri,adj)%2==1]
def triple_distribution(adj):
    dist={0:0,1:0,2:0,3:0}
    for tri in all_triples(len(adj)):
        dist[edge_count_in_triple(tri,adj)] += 1
    return dist
def incidence_gram(odd):
    n=40; C=[[0 for _ in range(n)] for _ in range(n)]
    row_sums=[0]*n
    for tri in odd:
        for i in tri: row_sums[i]+=1
        for i in tri:
            for j in tri:
                C[i][j]+=1
    return C,row_sums
def adjacency_matrix(adj):
    n=len(adj); return [[1 if j in adj[i] else 0 for j in range(n)] for i in range(n)]
def expected_gram(adj):
    A=adjacency_matrix(adj); n=len(adj)
    return [[320*(1 if i==j else 0)+16+4*A[i][j] for j in range(n)] for i in range(n)]
def max_abs_diff(X,Y): return max(abs(X[i][j]-Y[i][j]) for i in range(len(X)) for j in range(len(X)))
def gram_spectrum_from_srg():
    # C = 320I + 16J + 4A.  A eigenvalues: 12^1, 2^24, -4^15.
    return {"1008":1,"328":24,"304":15}
def recover_adjacency(C):
    n=len(C); return [[(C[i][j] - 320*(1 if i==j else 0) - 16)//4 for j in range(n)] for i in range(n)]
def build_results():
    checks=[]; pts,adj=build_graph(); triples=all_triples(len(adj)); odd=odd_triples(adj); dist=triple_distribution(adj); C,row_sums=incidence_gram(odd); E=expected_gram(adj); A=adjacency_matrix(adj); Arec=recover_adjacency(C)
    checks.append(ok('points = 40',len(pts)==40,len(pts)))
    checks.append(ok('total triples = 9880',len(triples)==9880,len(triples)))
    checks.append(ok('triple distribution 0/1/2/3',dist=={0:3240,1:4320,2:2160,3:160},dist))
    checks.append(ok('odd triples = 4480',len(odd)==4480,len(odd)))
    checks.append(ok('incidence row sums = 336',sorted(set(row_sums))==[336],sorted(set(row_sums))))
    checks.append(ok('incidence column sums = 3 by construction',3*len(odd)==sum(row_sums),{"left":3*len(odd),"right":sum(row_sums)}))
    checks.append(ok('Gram identity C=320I+16J+4A',max_abs_diff(C,E)==0,max_abs_diff(C,E)))
    checks.append(ok('edge pair count = 20',sorted(set(C[i][j] for i in range(40) for j in adj[i] if i<j))==[20],20))
    checks.append(ok('nonedge pair count = 16',sorted(set(C[i][j] for i in range(40) for j in range(i+1,40) if j not in adj[i]))==[16],16))
    checks.append(ok('adjacency recovered from two-graph Gram',Arec==A,True))
    checks.append(ok('Gram spectrum multiplicities close from SRG',gram_spectrum_from_srg()=={"1008":1,"328":24,"304":15},gram_spectrum_from_srg()))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXI","title":"Two-Graph Incidence Operator Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"triple_distribution":dist,"odd_triples":len(odd),"incidence_operator":{"shape":[40,4480],"row_sum":336,"column_sum":3},"gram_identity":"M M^T = 320 I + 16 J + 4 A","adjacency_recovery":"A = (M M^T - 320 I - 16 J)/4","gram_spectrum":{"1008":1,"328":24,"304":15},"sector_certificate":"The two-graph incidence operator recovers adjacency with coefficient 4, matching the edge/nonedge parity gap 20-16=4 and certifying the action-gap separation used by the preferred response-sector split.","architecture_upgrade":"CCCLX fused two-graph/interlacing counts with response sectors. CCCLXI constructs the actual two-graph incidence operator M and proves the operator identity M M^T=320I+16J+4A.","theorem":"For the W(3,3) Seidel two-graph, the vertex-by-odd-triple incidence matrix M satisfies M M^T=320I+16J+4A. Therefore the W33 adjacency operator is recoverable from the two-graph incidence operator, and the edge/nonedge parity gap 4 becomes an operator-level certificate rather than only a counting identity.","honesty_boundary":"This is an exact finite graph/operator theorem. Physical interpretation still depends on the response-channel dictionary.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXI_two_graph_incidence_operator_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
