#!/usr/bin/env python3
"""Pass5312: H/Z ~= Latin-even, but their natural degree-12 actions are inequivalent.

Pass5300 proves the abstract/affine-module bridge H/Z(H) ~= L+, where L+ is
the even-parastrophe subgroup of the Klein V4 Latin autoparatopy group, both
order288.  Here we compare natural 12-point representations.

H/Z acts on the 12 moving Hoffman cover cells.  L+ acts on the twelve labels
(row 0..3, column 0..3, symbol 0..3).  Both are transitive degree12 actions,
but their point stabilizers are nonisomorphic order24 groups, so the actions
are not permutation-equivalent.

Separately, the Klein autotopy group (no coordinate parastrophes) has order96
and is abstractly (C2)^4:S3, the same group as the tomotope, but on the 12 Latin
labels it has three orbits of size4, whereas the tomotope action is transitive.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5300_hoffman576_latin_group_bridge import q5_hoffman

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5312_HOFFMAN_LATIN_DEGREE12_ACTION_OBSTRUCTION.json'
S4=list(itertools.permutations(range(4)));S3=list(itertools.permutations(range(3)))

def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))&1
def hist(G):return {str(k):v for k,v in sorted(Counter(int(g.order()) for g in G.generate_schreier_sims()).items())}

def latin_label_group(even=False,autotopy_only=False):
    ans=[]
    pis=[(0,1,2)] if autotopy_only else S3
    for pi in pis:
      if even and parity(pi):continue
      for a in S4:
       for b in S4:
        mp={};ok=True
        for r in range(4):
         for c in range(4):
          old=(r,c,r^c);R=a[old[pi[0]]];C=b[old[pi[1]]];t=old[pi[2]];s=R^C
          if t in mp and mp[t]!=s:ok=False;break
          mp[t]=s
         if not ok:break
        if not(ok and len(mp)==4 and len(set(mp.values()))==4):continue
        maps=[a,b,tuple(mp[i] for i in range(4))];arr=[None]*12
        for newrole in range(3):
          oldrole=pi[newrole]
          for x in range(4):arr[4*oldrole+x]=4*newrole+maps[newrole][x]
        ans.append(Permutation(arr))
    return PermutationGroup(ans)

def inv(G):return {'order':G.order(),'center':G.center().order(),'derived':G.derived_subgroup().order(),'abelianization':G.abelian_invariants(),'element_orders':hist(G)}

def main():
    H,H13,_,_=q5_hoffman();assert H13.order()==288
    orbs=sorted(H13.orbits(),key=len);assert list(map(len,orbs))==[1,12]
    O=sorted(orbs[1]);HR=PermutationGroup([Permutation([O.index(g(x)) for x in O]) for g in H13.generators]);assert HR.order()==288 and HR.is_transitive()
    HS=HR.stabilizer(0);assert HS.order()==24

    L=latin_label_group(even=True);assert L.order()==288 and L.is_transitive()
    LS=L.stabilizer(0);assert LS.order()==24
    assert inv(HR)==inv(L)
    assert inv(HS)!=inv(LS)
    assert inv(HS)=={'order':24,'center':2,'derived':4,'abelianization':[2,3],'element_orders':{'1':1,'2':7,'3':8,'6':8}}
    assert inv(LS)=={'order':24,'center':1,'derived':12,'abelianization':[2],'element_orders':{'1':1,'2':9,'3':8,'4':6}}

    A=latin_label_group(autotopy_only=True);assert A.order()==96
    assert sorted(map(len,A.orbits()))==[4,4,4]
    assert inv(A)=={'order':96,'center':1,'derived':48,'abelianization':[2],'element_orders':{'1':1,'2':27,'3':32,'4':36}}

    out={'pass':5312,'status':'THEOREM_HOFFMAN_LATIN_AFFINE_ISOMORPHISM_DOES_NOT_IDENTIFY_NATURAL_DEGREE12_ACTIONS',
      'abstract_order288_bridge':'Pass5300: H/Z(H) ~= Klein even-parastrophe group L+ on the F2^4 affine module.',
      'hoffman_degree12':{'orbits':[12],'point_stabilizer':inv(HS)},
      'latin_even_degree12':{'objects':'4 row + 4 column + 4 symbol labels','orbits':[12],'point_stabilizer':inv(LS)},
      'obstruction':'The order24 point stabilizers are nonisomorphic, so the two transitive degree12 permutation representations of the abstract order288 group are inequivalent.',
      'latin_autotopy96':{'invariants':inv(A),'natural_12label_orbits':[4,4,4]},
      'tomotope96_boundary':'The Latin autotopy96 is abstractly the same (C2)^4:S3 type as Gamma(T), but its natural label action is 4+4+4, whereas the published tomotope action is transitive on12.',
      'conclusion':'The Pass5300 Latin bridge belongs to the 16-cell affine module; the Pass5309 tomotope bridge belongs to the 12-moving-Hoffman-cell action. These representations must not be conflated.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
