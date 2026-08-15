#!/usr/bin/env python3
"""Pass5310: two nonisomorphic order-192 tesseract/D4 groups share the tomotope quotient.

The full signed-permutation symmetry of Q4 has order384.  It has two natural
index-two subgroups of order192:
  R = determinant +1 signed permutations (orientation-preserving tesseract),
  D = even sign-change subgroup = W(D4).
They are NOT isomorphic: R has 48 elements of order8 and D has none.
Nevertheless both centers are the antipodal map -I and both central quotients
have order96 and structure (C2)^4:S3.  Pass5309 identifies D/Z(D) with the
published tomotope group; here we independently verify the same semidirect
module for R/Z(R).  Thus the tomotope is a common central quotient of two
different order-192 double covers.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5310_TESSERACT_D4_TOMOTOPE_DOUBLECOVERS.json'

def key(g):return tuple(g.array_form)
def hist(G):return {str(k):v for k,v in sorted(Counter(int(g.order()) for g in G.generate_schreier_sims()).items())}
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1

def signed_groups():
    V=list(itertools.product((-1,1),repeat=4));vi={v:i for i,v in enumerate(V)}
    R=[];D=[];B=[]
    for p in itertools.permutations(range(4)):
        sp=-1 if parity(p) else 1
        for s in itertools.product((-1,1),repeat=4):
            arr=Permutation([vi[tuple(s[i]*x[p[i]] for i in range(4))] for x in V]);B.append(arr)
            if sp*math.prod(s)==1:R.append(arr)
            if math.prod(s)==1:D.append(arr)
    return V,vi,PermutationGroup(B),PermutationGroup(R),PermutationGroup(D)

def antipodal_quotient(G,V,vi):
    P=[];seen=set()
    for i,v in enumerate(V):
        if i in seen:continue
        j=vi[tuple(-x for x in v)];P.append(tuple(sorted((i,j))));seen|={i,j}
    pi={p:i for i,p in enumerate(P)}
    return PermutationGroup([Permutation([pi[tuple(sorted((g(a),g(b))))] for a,b in P]) for g in G.generators])

def find_v16(G):
    for cl in G.conjugacy_classes():
        g=next(iter(cl))
        if int(g.order())!=2:continue
        V=G.normal_closure([g])
        if V.order()==16 and V.center().order()==16 and V.abelian_invariants()==[2,2,2,2]:return V
    raise AssertionError('no normal V16')

def quotient_action(G,V):
    nz=[x for x in V.generate_schreier_sims() if int(x.order())!=1];idx={key(x):i for i,x in enumerate(nz)}
    return PermutationGroup([Permutation([idx[key((~g)*x*g)] for x in nz]) for g in G.generators])

def cp(cycles):
    a=list(range(12))
    for cyc in cycles:
        for x,y in zip(cyc,cyc[1:]+cyc[:1]):a[x-1]=y-1
    return Permutation(a)

def main():
    V,vi,B,R,D=signed_groups();assert (B.order(),R.order(),D.order())==(384,192,192)
    assert R.center().order()==D.center().order()==2
    assert hist(R)=={'1':1,'2':43,'3':32,'4':36,'6':32,'8':48}
    assert hist(D)=={'1':1,'2':43,'3':32,'4':84,'6':32}
    assert hist(R)!=hist(D)
    # Their intersection is a third order-96 group, not the tomotope quotient.
    Rk={key(x):x for x in R.generate_schreier_sims()};Dk={key(x):x for x in D.generate_schreier_sims()}
    I=PermutationGroup([Rk[k] for k in Rk.keys()&Dk.keys()]);assert I.order()==96
    assert I.center().order()==2 and I.derived_subgroup().order()==32 and I.abelian_invariants()==[3]

    Rq=antipodal_quotient(R,V,vi);Dq=antipodal_quotient(D,V,vi)
    assert Rq.order()==Dq.order()==96
    want={'1':1,'2':27,'3':32,'4':36};assert hist(Rq)==hist(Dq)==want
    for Q in (Rq,Dq):
        W=find_v16(Q);A=quotient_action(Q,W)
        assert A.order()==6 and A.center().order()==1 and A.derived_subgroup().order()==3
        assert sorted(map(len,A.orbits()))==[3,3,3,6]

    # Published tomotope group has the same exact 96-group invariants/module fingerprint.
    T=PermutationGroup([
      cp([(5,10),(6,9),(7,12),(8,11)]),cp([(1,6),(2,5),(3,8),(4,7)]),
      cp([(5,9),(6,10),(7,11),(8,12)]),cp([(5,8),(6,7),(9,12),(10,11)])])
    assert T.order()==96 and hist(T)==want
    WT=find_v16(T);AT=quotient_action(T,WT)
    assert AT.order()==6 and sorted(map(len,AT.orbits()))==[3,3,3,6]

    out={'pass':5310,'status':'THEOREM_TESSERACT_ROTATION_AND_WD4_ARE_DISTINCT_192_DOUBLE_COVERS_OF_TOMOTOPE96',
      'full_tesseract_symmetry_order':384,
      'rotation_group':{'order':192,'center':2,'derived':96,'element_orders':hist(R)},
      'WD4':{'order':192,'center':2,'derived':96,'element_orders':hist(D)},
      'nonisomorphism_certificate':'The rotation group has 48 elements of order8; W(D4) has none.',
      'intersection':{'order':96,'center':2,'derived':32,'abelianization':'C3','note':'This intersection is not the tomotope group.'},
      'central_quotients':{'rotation_over_center':96,'WD4_over_center':96,'common_element_orders':want,
        'normal_module':'(C2)^4','quotient_action':'S3','nonzero_module_orbits':[3,3,3,6]},
      'tomotope':'Gamma(T) has the same (C2)^4:S3 structure; Pass5309 gives the stronger explicit permutation-action identification W(D4)/Z ~= Gamma(T).',
      'conclusion':'The user-noted tesseract rotation scale 192 is real, but the Hoffman 192 is W(D4), a different double cover. The tomotope order96 is the common quotient where the distinction disappears.',
      'boundary':'Equal quotient structure does not identify the two order192 covers themselves.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
