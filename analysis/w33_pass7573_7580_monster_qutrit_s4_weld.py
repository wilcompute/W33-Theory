#!/usr/bin/env python3
"""Pass7573-7580: weld the historical qutrit/MUB residual controller into the
same S4 direction quotient carried by the Monster 9+3360 port.

The repo already proved that the E6/F3 sign layer leaves a 12-element affine-flag
stabilizer D12 and that its action on the four qutrit striations is 1+3.  This
pass rebuilds that group directly from its closed affine formula and identifies
its striation image as the point stabilizer S3 inside the Monster direction S4.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7573_7580_MONSTER_QUTRIT_S4_WELD.json'
P=3
DIRS=((0,1),(1,0),(1,1),(1,2)) # vertical plus slopes 0,1,2
POINT=(2,2)

def canon(v):
    if v==(0,0): raise ValueError('zero direction')
    z=v[0] if v[0] else v[1]
    s=1 if z==1 else 2
    return ((s*v[0])%3,(s*v[1])%3)
def mv(A,v):return ((A[0][0]*v[0]+A[0][1]*v[1])%3,(A[1][0]*v[0]+A[1][1]*v[1])%3)
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))%3 for j in range(2)) for i in range(2))
def add(a,b):return ((a[0]+b[0])%3,(a[1]+b[1])%3)
def perm(A):return tuple(DIRS.index(canon(mv(A,v))) for v in DIRS)
def comp(g,h):
    A,b=g;C,d=h
    return mm(A,C),add(mv(A,d),b)
ID=(((1,0),(0,1)),(0,0))
def order(g):
    x=ID
    for n in range(1,30):
        x=comp(g,x)
        if x==ID:return n
    raise AssertionError('order bound')

def main():
    # Historical closed form: A=[[a,0],[c,d]], shift=(a-1,c+d-1),
    # with a,d nonzero.  It fixes p=(2,2) and the vertical striation.
    H=[]
    for a,d,c in itertools.product((1,2),(1,2),range(3)):
        A=((a,0),(c,d));b=((a-1)%3,(c+d-1)%3);g=(A,b)
        assert add(mv(A,POINT),b)==POINT
        assert perm(A)[0]==0
        H.append(g)
    assert len(H)==12 and len(set(H))==12
    assert Counter(order(g) for g in H)=={1:1,2:7,3:2,6:2}

    image={perm(A) for A,b in H}; assert len(image)==6
    kernel=[g for g in H if perm(g[0])==(0,1,2,3)];assert len(kernel)==2
    # The six induced permutations fix direction 0 and are every permutation of
    # the remaining three directions: exactly the S3 point stabilizer in S4.
    assert {tuple(p[i] for i in (1,2,3)) for p in image}==set(itertools.permutations((1,2,3)))

    # Full GL(2,3) direction action is S4 with scalar kernel {+-I}.
    gl=[]
    for a,b,c,d in itertools.product(range(3),repeat=4):
        if (a*d-b*c)%3:
            gl.append(((a,b),(c,d)))
    assert len(gl)==48
    full={perm(A) for A in gl}; assert len(full)==24
    scalars=[A for A in gl if perm(A)==(0,1,2,3)];assert len(scalars)==2

    out={
      'schema':'w33.pass7573_7580.monster_qutrit_s4_weld.v1','status':'PASS','passes':'7573-7580',
      'affine_plane':'AG(2,3)','qutrit_striations':4,
      'monster_direction_group':'GL(2,3)/{+-I}=PGL(2,3)=S4','monster_direction_group_order':24,
      'historical_sign_residual':{'order':12,'structure':'D12','fixed_affine_flag':{'point':[2,2],'direction':'x=constant / vertical'},'element_orders':{'1':1,'2':7,'3':2,'6':2}},
      'direction_action':{'image_order':6,'kernel_order':2,'image':'S3','orbits':[1,3],'identification':'the exact point-stabilizer S3 < S4 of the distinguished qutrit striation'},
      'commuting_square':'D12 -> S3 < S4 <- AGL(2,3), where S4 is the same four-direction quotient used by the Monster 9+3360 fiber product',
      'theorem':'The qutrit full-sign residual controller does not merely have an S3-shaped striation action: it lands exactly in the point stabilizer of the same S4 on four affine directions that couples the Monster 9-sheet to the D4(3) 3360-sheet.',
      'prior_art_boundary':'The D12 affine-flag stabilizer and its 1+3 striation action were already in the February E6/F3 sign analysis. New here is the exact identification with the S3 point stabilizer inside the Pass7509 Monster direction S4.',
      'claim_boundary':'Finite qutrit phase-space/controller equivariance only; no physical Monster symmetry is inferred for a device.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','D12':12,'direction_image':'S3','ambient':'S4'}))
if __name__=='__main__':main()
