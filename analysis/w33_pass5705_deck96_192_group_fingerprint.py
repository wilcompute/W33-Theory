#!/usr/bin/env python3
"""Pass5705: identify the magnetic D extension structurally, not by order coincidence.

The signed Segre carrier stabilizer G has order 96. Pass5692 found an involution D
that centralizes G, is not in G, and enlarges it to order 192. Therefore the
extension is forced abstractly to be G x C2.

This pass also proves the structural bridge to an older repo controller. The
central sheet sign -I has quotient P=G/<-I> of order 48. P contains a central C2
and an explicit complementary subgroup of order 24 with the S4 order spectrum,
so P ~= C2 x S4 = O_h, the cube/frame controller. The derived subgroup G' has
order 24; its elements of orders 1,2,4 form a closed Q8 and the quotient by Q8 is
C3 acting nontrivially. Hence G' ~= Q8:C3 ~= SL(2,3).

The magnetic 192 is G x C2. It is not the tomotope group doubled and is not W(D4):
those older order-96/192 objects have different derived structure. This is a
quotient/direct-product theorem, not an integer match.
"""
from __future__ import annotations
import collections,itertools,json,math
from pathlib import Path
import w33_pass5630_deck_bdg_commutant_mass_ratio_unprotected as core
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5705_DECK96_192_GROUP_FINGERPRINT.json'

def comp(a,b):
    p,s=a;q,t=b
    return (tuple(p[q[i]] for i in range(16)),tuple(t[i]*s[q[i]] for i in range(16)))
def inv(a):
    p,s=a;ip=[0]*16;ss=[0]*16
    for i,j in enumerate(p):ip[j]=i
    for j in range(16):ss[j]=s[ip[j]]
    return tuple(ip),tuple(ss)
def order(a):
    e=(tuple(range(16)),tuple([1]*16));x=e
    for n in range(1,193):
      x=comp(a,x)
      if x==e:return n
    raise RuntimeError('order too large')
def closure(gs):
    e=(tuple(range(16)),tuple([1]*16));G={e};front=[e]
    while front:
      x=front.pop()
      for g in gs:
        y=comp(g,x)
        if y not in G:G.add(y);front.append(y)
    return G

def pcomp(a,b):return tuple(a[b[i]] for i in range(16))
def pinv(a):
    z=[0]*16
    for i,j in enumerate(a):z[j]=i
    return tuple(z)
def porder(p):
    seen=[False]*16;ans=1
    for i in range(16):
      if seen[i]:continue
      j=i;n=0
      while not seen[j]:seen[j]=True;j=p[j];n+=1
      ans=math.lcm(ans,n)
    return ans
def pclosure(gs):
    e=tuple(range(16));G={e};front=[e]
    while front:
      x=front.pop()
      for g in gs:
        y=pcomp(g,x)
        if y not in G:G.add(y);front.append(y)
    return G

def s4_hist():
    return collections.Counter(porder(tuple(p)) for p in itertools.permutations(range(4)))
def c2xs4_hist():
    h=collections.Counter()
    for p in itertools.permutations(range(4)):
      o=porder(tuple(p)+(tuple(range(12)) if False else ())) if False else None
      # compute S4 order directly
      seen=[False]*4;oo=1
      for i in range(4):
        if seen[i]:continue
        j=i;n=0
        while not seen[j]:seen[j]=True;j=p[j];n+=1
        oo=math.lcm(oo,n)
      for bit in (0,1):h[math.lcm(oo,2 if bit else 1)]+=1
    return h

def main():
    pairs,_Rs,_H=core.build();G=set(pairs);assert len(G)==96
    hist=collections.Counter(order(g) for g in G)
    assert hist==collections.Counter({1:1,2:15,3:8,4:24,6:24,8:24})
    center=[g for g in G if all(comp(g,h)==comp(h,g) for h in G)];assert len(center)==2
    minus=next(g for g in center if order(g)==2)

    proj={g[0] for g in G};assert len(proj)==48
    ph=collections.Counter(porder(p) for p in proj)
    assert ph==c2xs4_hist()==collections.Counter({1:1,2:19,3:8,4:12,6:8})
    pcenter=[g for g in proj if all(pcomp(g,h)==pcomp(h,g) for h in proj)];assert len(pcenter)==2
    z=next(g for g in pcenter if porder(g)==2)
    # Find an explicit index-two complement H24 with the exact S4 spectrum.
    S4H=None;els=sorted(proj)
    target_s4=collections.Counter({1:1,2:9,3:8,4:6})
    for a in els:
      for b in els:
        H=pclosure([a,b])
        if len(H)==24 and z not in H and collections.Counter(porder(x) for x in H)==target_s4:
          S4H=H;break
      if S4H is not None:break
    assert S4H is not None
    assert len({pcomp(c,h) for c in pcenter for h in S4H})==48

    # Derived subgroup from all commutators.
    comm=[]
    for a in G:
      ia=inv(a)
      for b in G:comm.append(comp(comp(comp(a,b),ia),inv(b)))
    der=closure(comm);dh=collections.Counter(order(g) for g in der)
    assert len(der)==24 and dh==collections.Counter({1:1,2:1,3:8,4:6,6:8})
    Q8={g for g in der if order(g) in (1,2,4)}
    assert len(Q8)==8 and closure(list(Q8))==Q8
    # Unique involution excludes D8/C2^3; an element of order3 acts nontrivially,
    # otherwise Q8 x C3 would contain order12 elements.
    assert sum(order(g)==2 for g in Q8)==1 and not any(order(g)==12 for g in der)
    assert len(der)//len(Q8)==3

    d=tuple([1]*4+[-1]*8+[1]*4);D=(tuple(range(16)),d)
    assert D not in G and order(D)==2 and all(comp(D,g)==comp(g,D) for g in G)
    G192=closure(list(G)+[D]);assert len(G192)==192
    h192=collections.Counter(order(g) for g in G192)
    assert h192==collections.Counter({1:1,2:31,3:8,4:48,6:56,8:48})
    z192=[g for g in G192 if all(comp(g,h)==comp(h,g) for h in G192)];assert len(z192)==4
    comm192=[]
    for a in G192:
      ia=inv(a)
      for b in G192:comm192.append(comp(comp(comp(a,b),ia),inv(b)))
    der192=closure(comm192);assert der192==der

    out={
      'pass':5705,'status':'MAGNETIC_192_IS_G96xC2__PROJECTIVE_QUOTIENT_IS_EXACT_C2xS4__DERIVED_IS_SL2_3',
      'G96':{'order':96,'element_order_histogram':{str(k):v for k,v in sorted(hist.items())},'center_order':2,'derived_order':24,'derived_element_order_histogram':{str(k):v for k,v in sorted(dh.items())},'abelianization_order':4},
      'derived_group_proof':{'Q8_order':8,'Q8_unique_involution':True,'quotient_order':3,'order12_elements':0,'identification':'Q8:C3 with nontrivial C3 action = binary tetrahedral SL(2,3)'},
      'projective_quotient':{'order':48,'element_order_histogram':{str(k):v for k,v in sorted(ph.items())},'center_order':2,'explicit_S4_complement_order':24,'exact_structure':'C2 x S4 = O_h cube/frame controller','map':'forget signed sheet; kernel is central -I'},
      'D_extension':{'D_diagonal':list(d),'centralizes_G96':True,'D_in_G96':False,'order':192,'center_order':len(z192),'derived_order':len(der192),'exact_structure':'G96 x C2','element_order_histogram':{str(k):v for k,v in sorted(h192.items())}},
      'tomotope_no_go':'Repo-certified tomotope Aut has order96 with derived subgroup order48 (2^4:C3), whereas G96 derived is SL2(3) of order24; they are not isomorphic despite the shared order.',
      'WD4_no_go':'The older W(D4) object of order192 is a distinct repo controller. The magnetic 192 is a central direct-product doubling of G96 with derived subgroup only order24; no W(D4) identification is made from order.',
      'conclusion':'The structural bridge is exact: signed G96 -> C2 x S4 by quotienting the central sheet sign, then adjoining magnetic D produces G96 x C2. D is a second central sheet bit over a spinorial/binary-tetrahedral derived core.',
      'physics_boundary':'This is finite group structure. It does not make D a gauge symmetry or identify the group with spacetime spin, tomotope dynamics, or a particle symmetry.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
