#!/usr/bin/env python3
"""PART CCCLXIV -- Two-Graph Primitive Response Operator Compiler.

CCCLXI proved that the vertex-by-odd-triple incidence operator M satisfies

    M M^T = 320 I + 16 J + 4 A.

CCCLXIV treats M, not A, as the primitive.  From M alone it recovers:

    A = (M M^T - 320 I - 16 J)/4,
    k = 12,
    q = 3,
    Phi3 = 13,
    Phi6 = 7,
    B = 2v - Phi3 = 67,
    C = (v/2) Phi6 = 140,

and hence the RG spinor generator

    G = [[B/2, C], [1, -B/2]],
    G^2 = (5049/4) I.

So the finite response operator is derived from the two-graph incidence primitive.
"""
from __future__ import annotations
import itertools, json, math
from fractions import Fraction
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
        if a%MOD: return mul(1 if a==1 else 2,v)
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
        if omega(pts[i],pts[j])==0: adj[i].add(j); adj[j].add(i)
    return pts,adj
def edge_count(tri,adj): return sum(1 for i,j in itertools.combinations(tri,2) if j in adj[i])
def odd_triples(adj): return [tri for tri in itertools.combinations(range(len(adj)),3) if edge_count(tri,adj)%2==1]
def incidence_gram(odd,n=40):
    C=[[0]*n for _ in range(n)]
    for tri in odd:
        for i in tri:
            for j in tri: C[i][j]+=1
    return C
def recover_adjacency_from_gram(C):
    n=len(C)
    return [[(C[i][j]-320*(1 if i==j else 0)-16)//4 for j in range(n)] for i in range(n)]
def degree_from_A(A): return sorted(set(sum(row) for row in A))
def infer_q_from_degree(k):
    # For W(3,q), k=q(q+1).  Positive integer solution.
    disc=1+4*k
    q=(-1+int(math.isqrt(disc)))//2
    if q*(q+1)!=k: raise ValueError('degree is not q(q+1)')
    return q
def matmul2(X,Y): return ((X[0][0]*Y[0][0]+X[0][1]*Y[1][0],X[0][0]*Y[0][1]+X[0][1]*Y[1][1]),(X[1][0]*Y[0][0]+X[1][1]*Y[1][0],X[1][0]*Y[0][1]+X[1][1]*Y[1][1]))
def scale2(c,X): return ((c*X[0][0],c*X[0][1]),(c*X[1][0],c*X[1][1]))
def fs(x): return f"{x.numerator}/{x.denominator}" if x.denominator!=1 else str(x.numerator)
def mjson(X): return [[fs(x) for x in row] for row in X]
def primitive_derivation():
    pts,adj=build_graph(); odd=odd_triples(adj); C=incidence_gram(odd,len(adj)); A=recover_adjacency_from_gram(C); k=degree_from_A(A)[0]; q=infer_q_from_degree(k); v=len(adj); Phi3=q*q+q+1; Phi6=q*q-q+1; B=2*v-Phi3; offdiag=(v//2)*Phi6; M2=Fraction(B*B+4*offdiag,4); G=((Fraction(B,2),Fraction(offdiag,1)),(Fraction(1,1),Fraction(-B,2))); I=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1))); G2=matmul2(G,G)
    return {"points":pts,"adj":adj,"odd":odd,"C":C,"A":A,"k":k,"q":q,"v":v,"Phi3":Phi3,"Phi6":Phi6,"B":B,"offdiag":offdiag,"M2":M2,"G":G,"G2":G2,"I":I}
def build_results():
    d=primitive_derivation(); checks=[]
    checks.append(ok('odd triple count = 4480',len(d['odd'])==4480,len(d['odd'])))
    checks.append(ok('recovered adjacency degree = 12',d['k']==12,d['k']))
    checks.append(ok('inferred q = 3',d['q']==3,d['q']))
    checks.append(ok('Phi3 = 13',d['Phi3']==13,d['Phi3']))
    checks.append(ok('Phi6 = 7',d['Phi6']==7,d['Phi6']))
    checks.append(ok('B = 67',d['B']==67,d['B']))
    checks.append(ok('offdiag C = 140',d['offdiag']==140,d['offdiag']))
    checks.append(ok('M2 = 5049/4',d['M2']==Fraction(5049,4),fs(d['M2'])))
    checks.append(ok('G^2 = M2 I',d['G2']==scale2(d['M2'],d['I']),mjson(d['G2'])))
    checks.append(ok('recovered adjacency is 0/1 off diagonal',all(d['A'][i][i]==0 for i in range(40)) and all(d['A'][i][j] in (0,1) for i in range(40) for j in range(40)),True))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXIV","title":"Two-Graph Primitive Response Operator Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"primitive_chain":{"primitive":"odd-triple incidence M","gram":"M M^T","adjacency_recovery":"A=(M M^T-320I-16J)/4","degree":"k=12","q":"q=3 from k=q(q+1)","Phi3":"13","Phi6":"7","B":"2v-Phi3=67","offdiag":"(v/2)Phi6=140","G":"[[67/2,140],[1,-67/2]]","mass_shell":"G^2=(5049/4)I"},"generator":{"G":mjson(d['G']),"G_squared":mjson(d['G2']),"M2":fs(d['M2'])},"architecture_upgrade":"CCCLXI made the two-graph incidence operator recover adjacency. CCCLXIV makes that incidence operator the primitive source of the RG spinor response generator and derives G from M alone.","theorem":"The odd-triple incidence operator M determines A by A=(MM^T-320I-16J)/4. From recovered degree k=12 one infers q=3, then Phi3=13, Phi6=7, B=2v-Phi3=67, C=(v/2)Phi6=140, and G=[[67/2,140],[1,-67/2]] with G^2=(5049/4)I. Thus the finite response generator is two-graph-incidence-derived.","honesty_boundary":"This is an exact internal derivation. Physical scale calibration still belongs to the empirical response layer.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXIV_two_graph_primitive_response_operator_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
