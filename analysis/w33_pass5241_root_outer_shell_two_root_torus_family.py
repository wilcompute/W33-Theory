#!/usr/bin/env python3
"""Pass5241: root outer shell over the two-root (a,c) quotient.

The canonical U(q) state law is
 (a,b,c,d)(A,B,C,D)=(a+A,b+B,c+C-Ab,d+D-2Ac+A^2b).
The commuting root subgroups H1 and H3 act on the right by changing only b,d.
Hence their q^2 subgroup has right cosets exactly the fibers of

  pi(a,b,c,d)=(a,c) in F_q^2.

Pass5217 identifies these fibers objectwise with the 25 P atoms in a q=5
chamber star.  Here we combine this quotient with Pass5143's symbolic root
metric.  In characteristic >3 the distance-four shell has a,b nonzero and,
for normalized u=c/(ab), v=d/(a^2b), is the complement of the <=3-move curves.
For every fixed nonzero (a,c), b<->u is a bijection of F_q^*, and the missing-v
count summed over u is (q-4)^2.  Thus every nonzero (a,c) torus fiber contains
exactly (q-4)^2 distance-four states; fibers on the coordinate cross contain
none.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5241_ROOT_OUTER_SHELL_TWO_ROOT_TORUS_FAMILY.json'

def mul(x,y,q):
    a,b,c,d=x;A,B,C,D=y
    return ((a+A)%q,(b+B)%q,(c+C-A*b)%q,(d+D-2*A*c+A*A*b)%q)

def bfs(q):
    gens=[]
    for t in range(1,q):gens += [(t,0,0,0),(0,t,0,0),(0,0,t,0),(0,0,0,t)]
    z=(0,0,0,0);D={z:0};Q=deque([z])
    while Q:
        x=Q.popleft()
        for g in gens:
            y=mul(x,g,q)
            if y not in D:D[y]=D[x]+1;Q.append(y)
    return D

def anchor(q):
    D=bfs(q);shell=Counter(D.values());fib=Counter((x[0],x[2]) for x,d in D.items() if d==4)
    assert shell[4]==(q-1)**2*(q-4)**2
    assert len(fib)==(q-1)**2
    assert all(a and c for a,c in fib)
    assert set(fib.values())=={(q-4)**2}
    return {'q':q,'shell4':shell[4],'nonzero_ac_fibers':len(fib),'states_per_nonzero_ac_fiber':(q-4)**2}

def main():
    A={str(q):anchor(q) for q in (5,7,11,13)}
    out={'pass':5241,'status':'THEOREM_CHAR_GT3_ROOT_OUTER_SHELL_UNIFORM_TWO_ROOT_TORUS',
      'field_range':'finite fields of characteristic >3',
      'two_root_subgroup':'V=<H1,H3>, |V|=q^2; right cosets are exactly fixed-(a,c) fibers.',
      'quotient':'U(q)/V is coordinatized by (a,c) in F_q^2.',
      'q5_P_atom_connection':'Pass5217 identifies the 25 fixed-(a,c) fibers objectwise with the 25 P-minimum atoms in a chamber star.',
      'outer_shell_projection':'distance four projects exactly onto (F_q^*)^2; the coordinate cross a=0 or c=0 contains no distance-four state.',
      'uniform_fiber_size':'(q-4)^2 distance-four states in every nonzero (a,c) fiber.',
      'shell4':'(q-1)^2(q-4)^2',
      'proof':'For fixed nonzero a,c, b maps bijectively to normalized u=c/(ab); d maps bijectively to v=d/(a^2b). Pass5143 counts exactly (q-4)^2 normalized pairs outside the <=3-move curves.',
      'prime_anchors':A,
      'boundary':'The two-root quotient and characteristic>3 metric statement are algebraic. The literal equality-coordinate/P-atom identification is objectwise certified at q=5 by Pass5217; extending the geometric atom language to every characteristic requires the corresponding residue identification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
