#!/usr/bin/env python3
"""Pass7885-7892: Lagrangian atlas of the corrected Leech 3-adic linking module.

For C=(Z/9)^2 x (Z/3)^2 with its standard perfect alternating linking form,
enumerate every maximal isotropic subgroup L (|L|=sqrt(|C|)=27).  There are 148:
144 of type Z/9 x Z/3 and four elementary (Z/3)^3.  Under projection to the top
T=C/3C, the 144 mixed Lagrangians land three-to-one on the 48 nonradical isotropic
projective lines of the canonical rank-2 form from Pass7861.  The four elementary
Lagrangians land on the four projective radical points.  Thus the 3-adic bulk is a
three-sheet lift of the 4 x 12 Hesse-line atlas, plus four exceptional radical lifts.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7885_7892_LEECH_LAGRANGIAN_3ADIC_ATLAS.json'
E=[(a,b,c,d) for a in range(9) for b in range(9) for c in range(3) for d in range(3)]
zero=(0,0,0,0)

def add(x,y):return ((x[0]+y[0])%9,(x[1]+y[1])%9,(x[2]+y[2])%3,(x[3]+y[3])%3)
def smul(n,x):return ((n*x[0])%9,(n*x[1])%9,(n*x[2])%3,(n*x[3])%3)
def order(x):
    for n in (1,3,9):
        if smul(n,x)==zero:return n
    raise AssertionError
def pair(x,y):return (x[0]*y[1]-x[1]*y[0]+3*(x[2]*y[3]-x[3]*y[2]))%9

def canon(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError
def top(x):return (x[0]%3,x[1]%3,x[2]%3,x[3]%3)
def proj_image(H):return frozenset(canon(top(x)) for x in H if top(x)!=(0,0,0,0))
def span3(gs):
    H=set()
    for cs in itertools.product(range(3),repeat=len(gs)):
        z=zero
        for a,g in zip(cs,gs):z=add(z,smul(a,g))
        H.add(z)
    return frozenset(H)

def line(u,v):
    return frozenset(canon(tuple((a*u[i]+b*v[i])%3 for i in range(4)))
                     for a in range(3) for b in range(3) if (a,b)!=(0,0))
def kform(u,v):return (u[0]*v[1]-u[1]*v[0])%3

def main():
    O=Counter(order(x) for x in E);assert O==Counter({9:648,3:80,1:1})
    o9=[x for x in E if order(x)==9];o3=[x for x in E if order(x)==3]

    mixed=set()
    for x in o9:
        X={smul(a,x) for a in range(9)}
        for y in o3:
            if y in X or pair(x,y)!=0:continue
            H=frozenset(add(u,smul(b,y)) for u in X for b in range(3))
            assert len(H)==27;mixed.add(H)
    assert len(mixed)==144

    soc=[x for x in E if smul(3,x)==zero and x!=zero]
    elementary=set()
    for gs in itertools.combinations(soc,3):
        if any(pair(gs[i],gs[j])!=0 for i,j in itertools.combinations(range(3),2)):continue
        H=span3(gs)
        if len(H)==27:elementary.add(H)
    assert len(elementary)==4 and not (mixed&elementary)
    L=mixed|elementary;assert len(L)==148

    im_m=Counter(proj_image(H) for H in mixed);im_e=Counter(proj_image(H) for H in elementary)
    assert len(im_m)==48 and set(im_m.values())=={3} and all(len(S)==4 for S in im_m)
    assert len(im_e)==4 and set(im_e.values())=={1} and all(len(S)==1 for S in im_e)

    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    rad=frozenset(u for u in P if all(kform(u,v)==0 for v in P));assert len(rad)==4
    all_lines={line(u,v) for u,v in itertools.combinations(P,2)};assert len(all_lines)==130
    iso={S for S in all_lines if all(kform(u,v)==0 for u,v in itertools.combinations(S,2))}
    assert len(iso)==49 and rad in iso
    nonrad_iso=iso-{rad};assert len(nonrad_iso)==48 and set(im_m)==nonrad_iso
    assert {next(iter(S)) for S in im_e}==set(rad)

    # The 36 nonradical top points split into four K9/AG(2,3) fibres indexed by
    # the projective direction of their first coordinate pair.  Each of the 48
    # mixed-image lines has three nonradical points and one radical point; the
    # radical point is exactly its affine parallel-class label.
    non=[u for u in P if u not in rad]
    def qdir(u):return canon((u[0],u[1],0,0))[:2]
    comps={d:[u for u in non if qdir(u)==d] for d in sorted({qdir(u) for u in non})};assert len(comps)==4 and set(map(len,comps.values()))=={9}
    for pts in comps.values():
        pts=set(pts);tr=[(S&pts,next(iter(S&rad))) for S in nonrad_iso if S&pts]
        assert len(tr)==12 and all(len(T)==3 for T,_ in tr)
        assert len({T for T,_ in tr})==12
        for u,v in itertools.combinations(pts,2):assert sum(u in T and v in T for T,_ in tr)==1
        pc=Counter(r for _,r in tr);assert set(pc.values())=={3} and set(pc)==set(rad)

    out={
      'schema':'w33.pass7885_7892.leech_lagrangian_3adic_atlas.v1','status':'PASS','passes':'7885-7892',
      'module':'(Z/9)^2 x (Z/3)^2','maximal_isotropic_order':27,'Lagrangians_total':148,
      'Lagrangian_types':{'Z9xZ3':144,'Z3^3':4},
      'top_projection':{'mixed_images':48,'mixed_lifts_per_image':3,'mixed_image_type':'nonradical isotropic projective line','elementary_images':4,'elementary_image_type':'radical projective point'},
      'canonical_rank2_projective_geometry':{'radical_points':4,'isotropic_lines_total':49,'nonradical_isotropic_lines':48,'nonradical_points':36,'affine_planes':4,'AG23_lines_each':12},
      'three_adic_resolution':'144 = 3 x 48: every Hesse/AG(2,3) line in the four-plane top geometry has exactly three mixed Lagrangian lifts; the four radical points have one exceptional elementary Lagrangian lift each.',
      'theorem':'The Leech order-9 linking module has exactly 148 Lagrangians. Its mixed Lagrangians form a canonical three-sheet cover of the 48 affine lines in the four AG(2,3) planes singled out by multiplication by 3, while four elementary Lagrangians sit over the four radical points.',
      'claim_boundary':'Exact finite symplectic-abelian-group geometry. The three sheets are not assigned a physical phase without an additional equivariant identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Lagrangians':148,'mixed':144,'elementary':4,'cover':'3 x 48 + 4'}))
if __name__=='__main__':main()
