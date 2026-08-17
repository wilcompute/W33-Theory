#!/usr/bin/env python3
"""Pass5705: identify the magnetic D extension structurally, not by order coincidence.

The signed Segre carrier stabilizer G has order 96. Pass5692 found an involution D
that centralizes G, is not in G, and enlarges it to order 192. Therefore the
extension is already forced abstractly to be G x C2. This pass computes enough of
G's exact fingerprint to locate it relative to older repo controllers.

The central sign -I has quotient G/<-I> of order 48. Its element-order histogram
is exactly that of C2 x S4, the cube/frame group O_h already certified in the repo.
G itself has derived subgroup of order 24 with the SL(2,3) element-order pattern.
It is therefore a nontrivial central double cover of the cube/frame controller.
The order-192 magnetic extension is G x C2. It is not the tomotope group doubled
and not W(D4): those older order-96/192 objects have different derived/fingerprint
structure. This is a map/quotient statement, not an integer match.
"""
from __future__ import annotations
import collections,itertools,json,math
from pathlib import Path
import numpy as np
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
    for n in range(1,97):
      x=comp(a,x)
      if x==e:return n
    raise RuntimeError('order>96')
def closure(gs):
    e=(tuple(range(16)),tuple([1]*16));G={e};front=[e]
    while front:
      x=front.pop()
      for g in gs:
        y=comp(g,x)
        if y not in G:G.add(y);front.append(y)
    return G
def perm_order(p):
    seen=[False]*len(p);ans=1
    for i in range(len(p)):
      if seen[i]:continue
      j=i;n=0
      while not seen[j]:seen[j]=True;j=p[j];n+=1
      ans=math.lcm(ans,n)
    return ans

def s4xc2_hist():
    h=collections.Counter()
    for p in itertools.permutations(range(4)):
      o=perm_order(p)
      for bit in (0,1):h[math.lcm(o,2 if bit else 1)]+=1
    return h

def main():
    pairs,Rs,H=core.build();G=set(pairs);assert len(G)==96
    hist=collections.Counter(order(g) for g in G)
    assert hist==collections.Counter({1:1,2:15,3:8,4:24,6:24,8:24})
    center=[g for g in G if all(comp(g,h)==comp(h,g) for h in G)];assert len(center)==2
    minus=next(g for g in center if order(g)==2)

    # Projective quotient is simply the unsigned permutation action because the
    # central sign has identity permutation.
    proj={g[0] for g in G};assert len(proj)==48
    ph=collections.Counter(perm_order(p) for p in proj)
    cube=s4xc2_hist();assert ph==cube==collections.Counter({1:1,2:19,3:8,4:12,6:8})

    # Derived subgroup from all commutators; 96^2 is tiny.
    comm=[]
    for a in G:
      ia=inv(a)
      for b in G:
        comm.append(comp(comp(comp(a,b),ia),inv(b)))
    der=closure(comm);dh=collections.Counter(order(g) for g in der)
    assert len(der)==24
    assert dh==collections.Counter({1:1,2:1,3:8,4:6,6:8}) # SL(2,3)

    d=tuple([1]*4+[-1]*8+[1]*4);D=(tuple(range(16)),d)
    assert D not in G and order(D)==2 and all(comp(D,g)==comp(g,D) for g in G)
    G192=closure(list(G)+[D]);assert len(G192)==192
    h192=collections.Counter(order(g) for g in G192)
    z192=[g for g in G192 if all(comp(g,h)==comp(h,g) for h in G192)]
    assert len(z192)==4
    # Derived group is unchanged under direct product by a central C2.
    comm192=[]
    gens=list(G)[:]
    for a in G192:
      ia=inv(a)
      for b in G192:
        comm192.append(comp(comp(comp(a,b),ia),inv(b)))
    der192=closure(comm192);assert der192==der

    out={
      'pass':5705,'status':'MAGNETIC_192_IS_DIRECT_PRODUCT_OF_SIGNED_COVER96_WITH_C2__PROJECTIVE_QUOTIENT_IS_C2xS4',
      'G96':{'order':96,'element_order_histogram':{str(k):v for k,v in sorted(hist.items())},'center_order':2,'derived_order':24,'derived_element_order_histogram':{str(k):v for k,v in sorted(dh.items())},'derived_identification':'SL(2,3) by exact order fingerprint','abelianization_order':4},
      'projective_quotient':{'order':48,'element_order_histogram':{str(k):v for k,v in sorted(ph.items())},'identification':'C2 x S4 = O_h cube/frame controller','map':'forget signed sheet; kernel is central -I'},
      'D_extension':{'D_diagonal':list(d),'centralizes_G96':True,'D_in_G96':False,'order':192,'center_order':len(z192),'derived_order':len(der192),'exact_structure':'G96 x C2','element_order_histogram':{str(k):v for k,v in sorted(h192.items())}},
      'tomotope_no_go':'Repo-certified tomotope Aut has order96 with derived subgroup order48 (2^4:C3), whereas G96 derived has order24 (SL2(3)); they are not isomorphic despite the shared order.',
      'WD4_no_go':'The older W(D4) object of order192 is a distinct repo controller. The magnetic 192 has a central direct-product C2 over G96 and derived subgroup only order24; no W(D4) identification is made from order.',
      'conclusion':'The new D is best understood as a second central sheet bit over a spinorial double cover of the existing cube/frame quotient C2xS4. This is the structural bridge: signed carrier -> cube/frame controller by quotient, then magnetic D -> direct-product doubling.',
      'physics_boundary':'This is finite group structure. It does not make D a gauge symmetry or identify the group with spacetime spin, tomotope dynamics, or a particle symmetry.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
