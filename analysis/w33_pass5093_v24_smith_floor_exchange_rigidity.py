#!/usr/bin/env python3
"""Pass5093: one-row exchange rigidity at the raw V24 Smith floor D=780."""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
import networkx as nx
from sympy import Matrix, ilcm
from analysis.w33_pass4992_4999_common import build_base
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS5093_V24_SMITH_FLOOR_EXCHANGE_RIGIDITY.json'

def transport():
    b=build_base();T=b['tritangents'];M=b['M'].astype(int);W=b['W'];L=b['L'];H36=b['H36'];DS=b['DS'];spreads=b['spreads'];iso=b['iso_ds_sp']
    AT=nx.Graph();AT.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if len(set(T[i])&set(T[j]))==1:AT.add_edge(i,j)
    indep=[frozenset(s) for s in itertools.combinations(range(45),3) if all(not AT.has_edge(*e) for e in itertools.combinations(s,2))]
    circuits={}
    for A in indep:
        common=set(range(45))
        for a in A:common&=set(AT.neighbors(a))
        for z in itertools.combinations(sorted(common-A),3):
            B=frozenset(z)
            if all(not AT.has_edge(*e) for e in itertools.combinations(B,2)):
                circuits[tuple(sorted((tuple(sorted(A)),tuple(sorted(B))))]=(A,B)
    steiner={tuple(sorted(s)):s for s in b['steiner']};line_to_circuits=defaultdict(list)
    for _,(A,B) in circuits.items():
        six=sorted(A|B);missed=tuple(sorted(d for d in range(36) if all(M[t,d]==0 for t in six)));assert missed in steiner
        common=set(range(40))
        for d in missed:common&=set(spreads[iso[d]])
        assert len(common)==1;line_to_circuits[next(iter(common))].append((A,B))
    cover_lines=defaultdict(set);opposite={}
    for l in range(40):
        cs=line_to_circuits[l];bybits={}
        for bits in itertools.product((0,1),repeat=3):
            S=frozenset().union(*(cs[i][bits[i]] for i in range(3)));bybits[bits]=tuple(sorted(S));cover_lines[tuple(sorted(S))].add(l)
        for bits,C in bybits.items():opposite[(l,C)]=bybits[tuple(1-x for x in bits)]
    special={}
    for C,ls in cover_lines.items():
        if len(ls)==4:
            pts=set(range(40))
            for l in ls:pts&=set(L[l])
            special[C]=next(iter(pts))
    point_cover={p:C for C,p in special.items()};flag_cover={}
    for C,ls in cover_lines.items():
        if len(ls)==1:
            l=next(iter(ls));op=opposite[(l,C)];p=special[op];flag_cover[(p,l)]=C
    flags=[(p,l) for l,Q in enumerate(L) for p in Q];fi={f:i for i,f in enumerate(flags)}
    ordered=[point_cover[p] for p in range(40)]+[flag_cover[f] for f in flags]
    U=np.zeros((200,45),dtype=np.int64)
    for i,C in enumerate(ordered):U[i,list(C)]=1
    pair_line={}
    for l,Q in enumerate(L):
        for p,q in itertools.combinations(Q,2):pair_line[tuple(sorted((p,q)))]=l
    aps=[c for c in itertools.combinations(range(40),4) if W.subgraph(c).number_of_edges()==4 and set(dict(W.subgraph(c).degree()).values())=={2}];assert len(aps)==1620
    Y=np.zeros((1620,200),dtype=np.int64)
    for k,S in enumerate(aps):
        for p in S:Y[k,p]=1
        for p,q in W.subgraph(S).edges():
            l=pair_line[tuple(sorted((p,q)))];Y[k,40+fi[(p,l)]]=1;Y[k,40+fi[(q,l)]]=1
    Z=Y@U;return aps,5*Z-12*np.ones_like(Z)

def inv_den_and_height(A):
    X=Matrix(A.tolist()).inv();d=1
    for z in X:d=ilcm(d,int(z.q))
    return int(d),max(abs(int(z*d)) for z in X),X

def main():
    aps,Z24=transport();assert sum(0 in a for a in aps)==162
    cols=[0,1,2,3,5,6,7,8,10,11,12,13,15,16,17,18,22,23,25,26,27,30,31,35]
    R=Z24[:162][:,cols].astype(np.int64)
    original=[0,1,2,3,6,7,8,9,12,13,14,15,18,19,20,21,22,23,27,28,36,39,42,63]
    balanced=[0,1,2,3,6,7,8,9,12,13,14,15,157,19,20,21,22,23,53,28,36,94,42,63]
    floor=[118,5,122,37,6,76,129,61,44,26,89,45,87,126,78,124,22,111,15,38,58,96,64,160]
    d0,h0,_=inv_den_and_height(R[original]);db,hb,_=inv_den_and_height(R[balanced]);D,H,Ai=inv_den_and_height(R[floor])
    assert (d0,db,D)==(9360,3120,780)
    cond0=float(np.linalg.cond(R[original].astype(float),2));condb=float(np.linalg.cond(R[balanced].astype(float),2));condF=float(np.linalg.cond(R[floor].astype(float),2))
    N=np.array([[int(Ai[i,j]*D) for j in range(24)] for i in range(24)],dtype=object);S=set(floor)
    def swap_den(pos,inn):
        v=(R[inn]-R[floor[pos]]).astype(object);col=N[:,pos]
        w=np.array([sum(v[k]*N[k,j] for k in range(24)) for j in range(24)],dtype=object)
        t=sum(v[k]*col[k] for k in range(24));s=D+t
        if s==0:return 0
        Num=N*s-np.outer(col,w);Den=D*s;g=abs(int(Den))
        for z in Num.flat:g=math.gcd(g,abs(int(z)))
        return abs(int(Den))//g
    floor_neighbors=[];full_rank=0
    for pos in range(24):
        for inn in range(162):
            if inn in S:continue
            d=swap_den(pos,inn)
            if d==0:continue
            full_rank+=1
            if d==780:
                B=floor.copy();B[pos]=inn
                floor_neighbors.append({'position':pos,'incoming_row':inn,'condition_2':float(np.linalg.cond(R[B].astype(float),2))})
    floor_neighbors.sort(key=lambda x:x['condition_2'])
    assert full_rank==3289 and len(floor_neighbors)==8 and floor_neighbors[0]['condition_2']>condF
    result={'pass':5093,'status':'PASS','point_star_rows':162,'core_columns':cols,'original':{'D':d0,'condition_2':cond0,'cleared_inverse_height':h0},'balanced':{'D':db,'condition_2':condb,'cleared_inverse_height':hb},'smith_floor':{'D':D,'condition_2':condF,'cleared_inverse_height':H,'basis':floor},'one_row_exchange':{'full_rank_candidates':full_rank,'D780_neighbors':len(floor_neighbors),'best_D780_neighbor':floor_neighbors[0],'all_D780_neighbors':floor_neighbors},'theorem':'The raw D=780 Smith-floor basis is a strict local minimum of numerical condition number among all D=780 bases reachable by one row exchange. Exactly eight one-row exchanges preserve D=780, and all worsen kappa_2.','boundary':'This is one-exchange local optimality, not a global conditioning optimum over all D=780 raw bases.'}
    OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
