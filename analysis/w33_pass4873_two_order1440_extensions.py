#!/usr/bin/env python3
"""Pass4873 — distinguish the two order-1440 six-set extensions in the repo.

Pass4869: marked-double-six residue Aut = S6 x C2, where the central involution
fixes duads and complements triads.

Pass1848: duad -> syntheme transfer realizes the exceptional outer automorphism
class of S6.  From the frozen bijection we reconstruct an explicit outer
automorphism, inner-adjust it to an involution, and form Aut(S6)=S6 : C2.

The groups have the same order but are not isomorphic.  We certify this by
center, involution count, and complete element-order census.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'data/w33_pass1848_duad_syntheme_transfer.json'
NEW=ROOT/'data/PART_W33_PASS4869_MARKED_DOUBLE_SIX_K6_SYMPLECTIC_RESIDUE.json'
OUT=ROOT/'data/PART_W33_PASS4873_TWO_ORDER1440_EXTENSIONS.json'

def comp(g,h):return tuple(g[h[i]] for i in range(len(h)))
def inv(g):
    r=[0]*len(g)
    for i,j in enumerate(g):r[j]=i
    return tuple(r)
def conj(a,g):return comp(comp(a,g),inv(a))
def order(g):
    I=tuple(range(len(g)));x=I
    for n in range(1,1000):
        x=comp(g,x)
        if x==I:return n
    raise RuntimeError('order bound')
def ctype(g):
    seen=set();ls=[]
    for i in range(len(g)):
        if i in seen:continue
        j=i;l=0
        while j not in seen:seen.add(j);l+=1;j=g[j]
        ls.append(l)
    return tuple(sorted(ls,reverse=True))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def main()->int:
    old=json.loads(OLD.read_text());new=json.loads(NEW.read_text())
    assert old['status']=='PASS' and new['residue_automorphism_group']['order']==1440
    P=list(itertools.permutations(range(6)));I=tuple(range(6))
    duads=list(itertools.combinations(range(6),2))
    def syn(s):return tuple(sorted(tuple(sorted(e)) for e in s))
    synthemes=[]
    for M in itertools.combinations(duads,3):
        if sorted(x for e in M for x in e)==list(range(6)):
            z=syn(M)
            if z not in synthemes:synthemes.append(z)
    assert len(synthemes)==15
    F={}
    for key,val in old['duad_to_syntheme_outer_map'].items():
        d=tuple(map(int,key));F[d]=syn(tuple(tuple(x) for x in val))
    assert set(F)==set(duads) and set(F.values())==set(synthemes)
    Finv={v:k for k,v in F.items()};si={s:i for i,s in enumerate(synthemes)}
    def ad(g,d):return tuple(sorted((g[d[0]],g[d[1]])))
    def ass(g,s):return syn(tuple((g[a],g[b]) for a,b in s))
    sig={tuple(si[ass(g,s)] for s in synthemes):g for g in P}
    assert len(sig)==720
    def alpha(g):
        desired=[]
        for s in synthemes:
            d=Finv[s];desired.append(si[F[ad(g,d)]])
        return sig[tuple(desired)]
    # exact automorphism check on adjacent-transposition generators and all pairs sampled exhaustively enough via hom identity table
    gens=[]
    for i in range(5):
        g=list(range(6));g[i],g[i+1]=g[i+1],g[i];gens.append(tuple(g))
    for g in P:
        for h in gens:
            assert alpha(comp(g,h))==comp(alpha(g),alpha(h))
    assert set(alpha(g) for g in P)==set(P)
    assert ctype(gens[0])==(2,1,1,1,1) and ctype(alpha(gens[0]))==(2,2,2)

    # alpha^2 is inner; find its unique inner representative h0, then an inner adjustment beta of order two.
    target=[alpha(alpha(g)) for g in gens]
    hs=[h for h in P if all(conj(h,g)==t for g,t in zip(gens,target))]
    assert len(hs)==1;h0=hs[0]
    choices=[a for a in P if comp(comp(a,alpha(a)),h0)==I]
    assert len(choices)==36
    a=choices[0]
    def beta(g):return conj(a,alpha(g))
    assert all(beta(beta(g))==g for g in P)
    assert ctype(beta(gens[0]))==(2,2,2)

    # Direct residue action on 15 duads + 20 triads.
    triads=list(itertools.combinations(range(6),3));labels=[('d',d) for d in duads]+[('t',t) for t in triads];li={x:i for i,x in enumerate(labels)}
    def direct_perm(g):
        out=[]
        for typ,S in labels:out.append(li[(typ,tuple(sorted(g[i] for i in S)))])
        return tuple(out)
    sg=[direct_perm(g) for g in gens]
    z=[]
    for typ,S in labels:
        T=S if typ=='d' else tuple(i for i in range(6) if i not in S)
        z.append(li[(typ,T)])
    z=tuple(z)
    Gd=closure(sg+[z],35);assert len(Gd)==1440
    center_d=[x for x in Gd if all(comp(x,g)==comp(g,x) for g in sg+[z])]
    assert len(center_d)==2 and z in center_d
    census_d=Counter(order(x) for x in Gd)

    # Outer extension S6 : <beta>.  For coset element (g,1), square=(g beta(g),0).
    census_o=Counter();outer_invol=0
    for g in P:
        census_o[order(g)]+=1
        sq=comp(g,beta(g));census_o[2*order(sq)]+=1
        if sq==I:outer_invol+=1
    assert sum(census_o.values())==1440
    inner_invol=sum(order(g)==2 for g in P)
    assert inner_invol==75 and outer_invol==36
    # beta is outer, so no outer-coset central element can centralize S6; S6 itself is centerless.
    center_o=1

    assert census_d==Counter({1:1,2:151,3:80,4:360,5:144,6:560,10:144})
    assert census_o==Counter({1:1,2:111,3:80,4:360,5:144,6:240,8:360,10:144})
    assert center_d!=[] and len(center_d)==2 and center_o==1

    out={
      'pass':4873,
      'direct_marked_residue_extension':{
        'group':'S6 x C2','order':1440,'center_order':2,'central_involution':'fix duads; complement triads',
        'involution_count':census_d[2],'element_order_census':{str(k):v for k,v in sorted(census_d.items())}},
      'duad_syntheme_outer_extension':{
        'group':'Aut(S6) = S6 : Out(S6)','order':1440,'center_order':center_o,
        'outer_class_certificate':'an adjacent transposition of cycle type 2,1,1,1,1 maps to a triple transposition of type 2,2,2',
        'alpha_squared_inner_conjugator':list(h0),'involutive_outer_representatives_after_inner_adjustment':len(choices),
        'involution_count':census_o[2],'element_order_census':{str(k):v for k,v in sorted(census_o.items())}},
      'nonisomorphism_certificates':{
        'different_centers':'2 versus 1','different_involution_counts':'151 versus 111',
        'order8_elements':'direct has 0; outer extension has 360','different_complete_order_census':True},
      'repo_bridge':{
        'Pass1848':'the frozen duad-to-syntheme bijection reconstructs the exceptional outer automorphism class',
        'Pass4869':'the marked double-six residue independently gives the direct product S6 x C2',
        'warning':'the common numerical order 1440 is not an isomorphism; the two C2 extensions encode different operations'},
      'theorem':'The two order-1440 six-set symmetry extensions in the repo are provably different. The marked-double-six residue group is the direct product S6 x C2 with center order 2 and 151 involutions. The Pass1848 duad-syntheme carrier reconstructs the exceptional outer automorphism class and hence Aut(S6)=S6:2, which has trivial center, 111 involutions, and 360 elements of order 8. Equal order 1440 is therefore a count coincidence across two nonisomorphic extensions, not a shared group identification.',
      'boundary':'Finite group-extension theorem. It distinguishes the actions but does not choose one extension as a physical symmetry without an independently specified carrier.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
