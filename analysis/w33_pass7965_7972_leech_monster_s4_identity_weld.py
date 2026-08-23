#!/usr/bin/env python3
"""Pass7965-7972: literal Leech four-AG(2,3) to Monster/qutrit S4 direction weld.

Pass7861 labels the four canonical Leech affine planes by the projective direction
of the first F3^2 coordinate. Pass7573 labels the Monster/qutrit striations by the
same PG(1,3) coordinate set. Strict linking isometries use SL2(3), hence A4 on
four directions; genuine linking similitudes allow GL2(3) and hence the full S4.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass7573_7580_monster_qutrit_s4_weld import DIRS as MONSTER_DIRS
OUT=ROOT/'data/PART_W33_PASS7965_7972_LEECH_MONSTER_S4_IDENTITY_WELD.json'
DIRS=((0,1),(1,0),(1,1),(1,2))

def canon(v):
    if v==(0,0):raise ValueError
    z=v[0] if v[0] else v[1];s=1 if z==1 else 2
    return ((s*v[0])%3,(s*v[1])%3)
def mv(A,v):return ((A[0][0]*v[0]+A[0][1]*v[1])%3,(A[1][0]*v[0]+A[1][1]*v[1])%3)
def perm(A):return tuple(DIRS.index(canon(mv(A,v))) for v in DIRS)

def main():
    assert tuple(MONSTER_DIRS)==DIRS
    gl=[];sl=[]
    for a,b,c,d in itertools.product(range(3),repeat=4):
        det=(a*d-b*c)%3
        if det:
            A=((a,b),(c,d));gl.append(A)
            if det==1:sl.append(A)
    assert len(gl)==48 and len(sl)==24
    pgl={perm(A) for A in gl};psl={perm(A) for A in sl}
    assert len(pgl)==24 and len(psl)==12
    G=PermutationGroup([Permutation(list(p)) for p in pgl]);H=PermutationGroup([Permutation(list(p)) for p in psl])
    assert int(G.order())==24 and int(H.order())==12
    assert sorted(int(x.order()) for x in G.generate_schreier_sims()).count(4)==6
    kernel=[A for A in gl if perm(A)==(0,1,2,3)];assert len(kernel)==2
    # The determinant-one image is A4; the simultaneous determinant -1 Leech
    # similitude coset supplies all odd permutations and upgrades it to S4.
    assert all(sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])%2==0 for p in psl)
    assert any(sum(1 for i in range(4) for j in range(i+1,4) if p[i]>p[j])%2 for p in pgl)
    out={
      'schema':'w33.pass7965_7972.leech_monster_s4_identity_weld.v1','status':'PASS','passes':'7965-7972',
      'common_direction_set':'PG(1,3) = {(0:1),(1:0),(1:1),(1:2)}','coordinate_identification':'identity',
      'Leech_strict_isometries':{'linear_group':'SL2(3)','projective_image':'PSL2(3)=A4','order':12},
      'Leech_linking_similitudes':{'linear_group':'GL2(3)','scalar_kernel':'{+-I}','projective_image':'PGL2(3)=S4','order':24},
      'Monster_dependency':'Pass7573-7580: the Monster 9-sheet/qutrit direction quotient is GL2(3)/{+-I}=S4 on exactly the same DIRS tuple.',
      'theorem':'The four canonical Leech AG(2,3) planes and the four Monster/qutrit affine striations carry the same coordinate PGL2(3) action on PG(1,3). The weld is therefore literal on direction labels: strict Leech isometries give A4, and linking similitudes supply the odd coset completing the Monster S4.',
      'claim_boundary':'Exact finite controller identification; it does not assert that the Monster acts on the Leech order-9 quotient through this S4 without the already established local subgroup port.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','strict':'A4','similitude':'S4','identity_weld':True}))
if __name__=='__main__':main()
