#!/usr/bin/env python3
"""Pass7182: D4(E8) census, selected-90 lattice glue, ten-D4 spreads and spread code."""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7182_D4_GLUE_SPREAD_CODE.json'

def gf2basis(rows):
    B={}
    for x in rows:
        y=int(x)
        while y:
            k=y.bit_length()-1
            if k in B:y^=B[k]
            else:B[k]=y;break
    return [B[k] for k in sorted(B,reverse=True)]
def enum(B):
    C=Counter({0:1});x=0
    for n in range(1,1<<len(B)):
        g=n^(n>>1);h=(n-1)^((n-1)>>1);d=g^h;i=(d&-d).bit_length()-1;x^=B[i];C[x.bit_count()]+=1
    return dict(sorted(C.items()))
def cqs(adj):
    Q=set()
    for a,c,d in itertools.combinations(range(40),3):
        if c in adj[a] or d in adj[a] or d in adj[c]:continue
        x=frozenset(adj[a]&adj[c]&adj[d])
        if len(x)==4:Q.add(x)
    Q=sorted(Q,key=lambda x:tuple(sorted(x)));qi={q:i for i,q in enumerate(Q)};p={}
    for i,q in enumerate(Q):p[i]=qi[frozenset(set.intersection(*(adj[x] for x in q)))]
    assert len(Q)==90 and all(p[p[i]]==i and p[i]!=i for i in range(90));return Q,p
def pairs(p):
    S=set()
    for i,j in p.items():S.add(tuple(sorted((i,j))))
    return sorted(S)
def relation(Q,adj,i,j):
    A,B=Q[i],Q[j];return len(A&B),sum(1 for a in A for c in B if c in adj[a])
def simple(Q,R,fib):
    roots=sorted({v for f in Q for v in fib[f]})
    for c in roots:
        N=[v for v in roots if b.dot(R[c],R[v])==-4]
        for L in itertools.combinations(N,3):
            if all(b.dot(R[x],R[y])==0 for x,y in itertools.combinations(L,2)):
                X=(c,)+L
                if sp.Matrix([R[v] for v in X]).rank()==4:return X
    raise AssertionError
def frac(x):x=sp.Rational(x);return x-sp.floor(x)

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,partner=cqs(adj);P=pairs(partner);assert len(P)==45
    support=[frozenset(Q[i]|Q[j]) for i,j in P];packs=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for z in C:
            if U&support[z]:ok=False;break
            U|=support[z]
        if ok and len(U)==40:packs.append(C)
    assert len(packs)==27
    # All D4 subsystems from orthogonal root-line frames.
    I={r:i for i,r in enumerate(R)};neg={i:I[tuple(-x for x in R[i])] for i in range(240)};rep=sorted({min(i,neg[i]) for i in range(240)});assert len(rep)==120
    O=[set() for _ in range(120)]
    for i,j in itertools.combinations(range(120),2):
        if b.dot(R[rep[i]],R[rep[j]])==0:O[i].add(j);O[j].add(i)
    frames=[]
    for a in range(120):
      for c in sorted(x for x in O[a] if x>a):
        X=O[a]&O[c]
        for d in sorted(x for x in X if x>c):
          for e in sorted(x for x in X&O[d] if x>d):frames.append((a,c,d,e))
    assert len(frames)==122850;RS=set(R);d4f=[]
    for F in frames:
        V=[R[rep[x]] for x in F];ok=False
        for tail in itertools.product((1,-1),repeat=3):
            sg=(1,)+tail;n=[sum(sg[t]*V[t][k] for t in range(4)) for k in range(8)]
            if all(x%2==0 for x in n) and tuple(x//2 for x in n) in RS:ok=True;break
        if ok:d4f.append(F)
    assert len(d4f)==9450;subs=set()
    for F in d4f:
        V=[R[rep[x]] for x in F];S=tuple(i for i,r in enumerate(R) if sum(b.dot(r,v)**2 for v in V)==64);assert len(S)==24;subs.add(S)
    assert len(subs)==3150
    # Selected 90 D4 lattice-pair trichotomy.
    bas=[simple(q,R,fib) for q in Q];BE=sp.Matrix(b.SIMPLES);detE=abs(int(BE.det()));assert detE==256
    rr=defaultdict(Counter);ii=defaultdict(Counter);glue=Counter();patterns=[(0,0,sp.Rational(1,2),sp.Rational(1,2)),(0,sp.Rational(1,2),0,sp.Rational(1,2)),(0,sp.Rational(1,2),sp.Rational(1,2),0)];pid={x:i for i,x in enumerate(patterns)}
    for a,c in itertools.combinations(range(90),2):
        M=sp.Matrix([R[v] for v in bas[a]+bas[c]]);rel=relation(Q,adj,a,c);rank=M.rank();rr[rel][rank]+=1
        if rank<8:ii[rel]['singular']+=1;continue
        idx=abs(int(M.det()))//detE;ii[rel][str(idx)]+=1
        if rel==(0,16):
            C=BE*M.inv();gen=[tuple(frac(x) for x in C.row(r)) for r in range(8)];G={(sp.Rational(0),)*8};change=True
            while change:
                change=False
                for x in list(G):
                    for y in gen:
                        z=tuple(frac(x[k]+y[k]) for k in range(8))
                        if z not in G:G.add(z);change=True
            assert len(G)==4;mp={}
            for z in G:
                if not any(z):continue
                A=tuple(z[:4]);B=tuple(z[4:]);assert A in pid and B in pid;mp[pid[A]]=pid[B]
            glue[tuple(mp[k] for k in range(3))]+=1
    assert rr[(1,3)]==Counter({6:1440});assert ii[(0,4)]==Counter({'1':1080}) and ii[(0,7)]==Counter({'1':1440}) and ii[(0,16)]==Counter({'4':45});assert glue==Counter({(0,1,2):45})
    spreadrel=Counter()
    for C in packs:
        ten=[]
        for z in C:ten.extend(P[z])
        h=Counter(relation(Q,adj,a,c) for a,c in itertools.combinations(ten,2));spreadrel[tuple(sorted(h.items()))]+=1
    assert spreadrel==Counter({(((0,4),40),((0,16),5)):27})
    # Support codes: 90 D4s, 45 orthogonal pairs, and 27 ten-D4 spreads.
    B90=gf2basis([sum(1<<x for x in q) for q in Q]);B45=gf2basis([sum(1<<x for x in s) for s in support]);assert len(B90)==39 and len(B45)==15
    e45=enum(B45);assert e45=={0:1,8:45,12:720,16:6930,20:17376,24:6930,28:720,32:45,40:1}
    spreadrows=[sum(1<<z for z in C) for C in packs];BS=gf2basis(spreadrows);assert len(BS)==21;eS=enum(BS);assert eS[5]==27
    cols=[0]*45
    for r,C in enumerate(packs):
        for z in C:cols[z]|=1<<r
    dual6=set()
    for C in itertools.combinations(range(45),6):
        s=0
        for z in C:s^=cols[z]
        if s==0:dual6.add(frozenset(C))
    assert len(dual6)==120
    GD=nx.Graph();GD.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if support[i].isdisjoint(support[j]):GD.add_edge(i,j)
    T=[frozenset(x) for x in itertools.combinations(range(45),3) if all(not GD.has_edge(a,c) for a,c in itertools.combinations(x,2))];TS=set(T);K=set()
    for A in T:
        N=set(range(45))
        for a in A:N&=set(GD[a])
        for x in itertools.combinations(sorted(N),3):
            Y=frozenset(x)
            if Y in TS and len(A|Y)==6:K.add(frozenset(A|Y))
    assert K==dual6 and len(K)==120
    out={'schema':'w33.pass7182.d4_glue_spread_code.v1','status':'PASS',
      'all_E8_D4':{'antipodal_root_lines':120,'orthogonal_4_frames':122850,'D4_spanning_frames':9450,'D4_subsystems':3150,'frames_per_D4':3,'W_E8_order':696729600,'D4_normalizer_order':221184},
      'selected90_pair_span_ranks':{str(k):dict(v) for k,v in rr.items()},'selected90_pair_lattice_indices':{str(k):dict(v) for k,v in ii.items()},
      'orthogonal_pair_glue':'index 4 diagonal (Z2)^2 glue {(0,0),(v,v),(s,s),(c,c)}','canonical_simple_basis_glue_permutations':{str(k):v for k,v in glue.items()},
      'ten_D4_spreads':27,'spread_pair_pattern':'5 orthogonal index-4 pairs plus 40 disjoint nonorthogonal index-1 pairs; any cross-pair from different orthogonal pairs generates the full E8 lattice',
      'D4_power10_firewall':'There is no ordinary D4^10 direct-sum glue code: the ambient rank is 8, not 40. The ten D4 subspaces are pairwise transverse; two already span rank 8.',
      'D4_support_code':'[40,39,2]_2 full even-weight code','orthogonal_pair_support_code':'[40,15,8]_2','orthogonal_pair_code_enumerator':{str(k):v for k,v in e45.items()},
      'spread_incidence_code':'[45,21,5]_2','spread_code_min_words':27,'spread_code_enumerator':{str(k):v for k,v in eS.items()},
      'spread_code_dual':'[45,24,6]_2','dual_min_words':120,'dual_min_words_equal_induced_K3,3_supports':True,
      'repo_bridge':'The dual [45,24,6] code and its 120 minimum K3,3 words are exactly the Pass5019 Steiner circuit code.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','D4':3150,'spreads':27,'spread_code':'[45,21,5]'}))
if __name__=='__main__':main()
