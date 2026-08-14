#!/usr/bin/env python3
"""Pass5214: exact connected-L gluing on a q=5 minimum P footprint.

Fix a W point p.  The 25 P components in the point footprint each contain 36
P-minimum atoms.  A P-heavy-free weight-625 candidate with this footprint picks
one atom in each component.  Evaluate the 10 fundamental triangle syndromes in
each of the 9750 L/opposite-line charts on those atom choices.

The resulting finite CSP has a remarkable exact reduction:
  * 17,250 nontrivial syndrome equations involve one atom group;
  * 7,500 involve two atom groups;
  * no equation involves three or more of the 25 groups.
The unary equations leave exactly six choices in every group, precisely the
atoms incident with p.  Label those six atoms by the six W-lines through p.
For every pair of the 25 groups, the aggregate binary equations leave exactly
six allowed pairs, and they are exactly (ell,ell) for the six line labels.
Thus all 25 groups must choose the same line.  There are exactly six global
solutions, the six chamber stars based at p.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from functools import reduce
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5214_Q5_CONNECTEDL_POINT_FOOTPRINT_GLUING.json'

def p_component_assignment(G):
    P=[loc for t,loc in G['charts'] if t=='P'];nA=len(G['apartments'])
    par=list(range(len(P)));owner=[-1]*nA
    def find(x):
        while par[x]!=x:par[x]=par[par[x]];x=par[x]
        return x
    def union(a,b):
        a=find(a);b=find(b)
        if a!=b:par[b]=a
    for ci,loc in enumerate(P):
        for a in loc.values():
            if owner[a]<0:owner[a]=ci
            else:union(ci,owner[a])
    roots={};acid=[]
    for a in range(nA):
        r=find(owner[a]);roots.setdefault(r,len(roots));acid.append(roots[r])
    return acid,len(roots)

def atoms(G,acid):
    byflag=[[] for _ in G['flags']]
    for a,es in enumerate(G['apt_edges']):
        for e in es:byflag[e].append(a)
    byline=defaultdict(list)
    for e,(p,l) in enumerate(G['flags']):byline[l].append(e)
    A=[];meta=[]
    for l,es in byline.items():
        for e,f in itertools.combinations(es,2):
            B=set(byflag[e]);inter=[a for a in byflag[f] if a in B]
            C=defaultdict(list)
            for a in inter:C[acid[a]].append(a)
            assert len(C)==5 and set(map(len,C.values()))=={25}
            for c,S in C.items():A.append(frozenset(S));meta.append((l,e,f,c))
    assert len(A)==11700 and len(set(A))==11700
    return A,meta,byflag

def atom_L_syndromes(G,A):
    aa=[[] for _ in G['apartments']]
    for i,S in enumerate(A):
        for a in S:aa[a].append(i)
    assert set(map(len,aa))=={4}
    L=[loc for t,loc in G['charts'] if t=='L'];syn=[0]*len(A);bit=0
    for loc in L:
        for i,j in itertools.combinations(range(1,6),2):
            aps=[loc[tuple(sorted(e))] for e in ((0,i),(0,j),(i,j))]
            z=Counter()
            for a in aps:
                for u in aa[a]:z[u]^=1
            for u,v in z.items():
                if v:syn[u]|=1<<bit
            bit+=1
    assert bit==97500
    return syn,bit

def main():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    A,meta,byflag=atoms(G,acid);syn,nb=atom_L_syndromes(G,A)
    byp=defaultdict(list)
    for e,(p,l) in enumerate(G['flags']):byp[p].append(e)
    p=0;flags=byp[p];assert len(flags)==6
    com_atoms=defaultdict(list)
    for i,(_,e,f,c) in enumerate(meta):com_atoms[c].append(i)
    C=sorted({meta[i][3] for i in range(len(A)) if set(A[i])<=set(byflag[flags[0]])})
    # Faster invariant check: a chamber star has exactly 25 P atoms.
    if len(C)!=25:
        C=sorted({acid[a] for a in byflag[flags[0]]})
    assert len(C)==25 and all(len(com_atoms[c])==36 for c in C)
    ALL=(1<<36)-1
    bitgroups={}
    for gi,c in enumerate(C):
        for ch,u in enumerate(com_atoms[c]):
            x=syn[u]
            while x:
                lb=x&-x;b=lb.bit_length()-1;x-=lb
                bitgroups.setdefault(b,{}).setdefault(gi,0)
                bitgroups[b][gi]|=1<<ch
    arity=Counter();Dom=[ALL]*25;binary=[]
    for b,D in bitgroups.items():
        non=[(g,m) for g,m in D.items() if m not in (0,ALL)]
        const=sum(1 for m in D.values() if m==ALL)&1
        arity[len(non)]+=1
        if len(non)==1:
            g,m=non[0];Dom[g]&=m if const else (ALL^m)
        elif len(non)==2:binary.append((non,const))
        else:assert False,(b,len(non))
    assert arity==Counter({1:17250,2:7500})
    assert all(d.bit_count()==6 for d in Dom)
    pcompat=[];labels=[]
    for gi,c in enumerate(C):
        Ls=com_atoms[c];S=[];lab={}
        for ch,u in enumerate(Ls):
            if not ((Dom[gi]>>ch)&1):continue
            l,e,f,_=meta[u];pe=G['flags'][e][0];pf=G['flags'][f][0]
            assert p in (pe,pf);S.append(u);lab[ch]=l
        assert len(S)==6 and set(lab.values())==set(G['flags'][e][1] for e in flags)
        pcompat.append(S);labels.append(lab)
    # Aggregate all binary checks by group pair.
    rel={}
    for non,const in binary:
        (g1,m1),(g2,m2)=non
        if g1>g2:(g1,m1),(g2,m2)=(g2,m2),(g1,m1)
        allowed=rel.get((g1,g2),{(a,b) for a in labels[g1] for b in labels[g2]})
        rel[(g1,g2)]={ab for ab in allowed if (((m1>>ab[0])&1)^((m2>>ab[1])&1)^const)==0}
    assert len(rel)==300
    line_set=set(G['flags'][e][1] for e in flags)
    for (g1,g2),R in rel.items():
        LR={(labels[g1][a],labels[g2][b]) for a,b in R}
        assert LR=={(l,l) for l in line_set}
    # Six explicit global solutions, all chamber stars.
    sols=[]
    for l in sorted(line_set):
        U=[]
        for gi,c in enumerate(C):
            ch=next(ch for ch,ll in labels[gi].items() if ll==l);U.append(com_atoms[c][ch])
        assert reduce(int.__xor__,[syn[u] for u in U],0)==0
        e=next(e for e in flags if G['flags'][e][1]==l)
        union=set().union(*(A[u] for u in U));assert union==set(byflag[e])
        sols.append({'line':l,'chamber':e,'atoms':len(U),'apartments':len(union)})
    out={'pass':5214,'status':'THEOREM_Q5_FIXED_POINT_FOOTPRINT_L_GLUING_IS_SIX_CHAMBER_STARS',
      'q':5,'fixed_point':p,'P_footprint_components':25,'atoms_per_component':36,
      'L_charts':9750,'fundamental_L_triangle_checks':nb,
      'constraint_arity':{'unary':17250,'binary':7500,'higher':0},
      'unary_survivors_per_component':6,
      'unary_survivors':'exactly the six P atoms incident with the fixed footprint point',
      'binary_group_pairs':300,'binary_allowed_pairs_per_group_pair':6,
      'binary_relation':'after labeling survivors by the six W-lines through p, every pair constraint is exactly equality of line labels',
      'global_solutions':6,'solutions':sols,
      'conclusion':'For a fixed q5 point footprint, every P-heavy-free weight-625 apartment word satisfying all L triangle checks is one of the six chamber stars based at that point.',
      'bridge_needed_for_full_shell':'To classify all P-heavy-free weight-625 words globally, combine with an independent theorem that every weight-25 nonzero P-footprint is a W-point footprint.',
      'boundary':'This proves the L gluing exactly on a fixed point footprint. It does not classify non-point weight-25 footprints unless the footprint minimum-shell theorem is supplied independently, and it does not eliminate P-heavy equality candidates.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
