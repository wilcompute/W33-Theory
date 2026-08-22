#!/usr/bin/env python3
"""Pass7322: identify the Pass7183 affine-area voltage as the commutator form of H27."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import w33_pass7183_c3_affine_area_cocycle as a

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7322_HEISENBERG_AREA_EXTENSION.json'
F=[(x,y) for x in range(3) for y in range(3)]
def add(u,v):return ((u[0]+v[0])%3,(u[1]+v[1])%3)
def neg(u):return ((-u[0])%3,(-u[1])%3)
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
def sigma(u,v):return (-det(u,v))%3
def star(x,y):
    u,z=x;v,w=y
    return (add(u,v),(z+w+sigma(u,v))%3)
def inv(x):
    u,z=x;return (neg(u),(-z)%3)
def comm(x,y):return star(star(star(x,y),inv(x)),inv(y))

def main():
    C,sh,hol,hist=a.build_voltage();V=[(u,z) for u in F for z in range(3)];e=((0,0),0)
    # sigma is a normalized group 2-cocycle.
    assert all(sigma((0,0),u)==sigma(u,(0,0))==0 for u in F)
    assert all((sigma(u,v)+sigma(add(u,v),w)-sigma(v,w)-sigma(u,add(v,w)))%3==0 for u,v,w in itertools.product(F,repeat=3))
    assert all(star(star(x,y),z)==star(x,star(y,z)) for x,y,z in itertools.product(V,repeat=3))
    assert all(star(x,x)==star(x,x) and star(star(x,x),x)==e for x in V) # exponent 3
    center=[x for x in V if all(star(x,y)==star(y,x) for y in V)]
    derived={comm(x,y) for x,y in itertools.product(V,repeat=2)}
    assert center==[((0,0),z) for z in range(3)] and set(center)==derived
    # The commutator of horizontal lifts is exactly determinant area.
    assert all(comm((u,0),(v,0))==((0,0),det(u,v)) for u,v in itertools.product(F,repeat=2))
    # Match the Pass7183 edge voltage up to its certified global sign/affine gauge.
    pts=F;zero={frozenset(t) for t,h in hol.items() if h==0};canon=set()
    for tri in itertools.combinations(range(9),3):
        u,v,w=[pts[i] for i in tri]
        if (det(u,v)+det(v,w)+det(w,u))%3==0:canon.add(frozenset(tri))
    matches=[]
    for rest in itertools.permutations(range(1,9)):
        p=(0,)+rest
        if {frozenset(p[i] for i in L) for L in zero}!=canon:continue
        for eps in (1,2):
            if all(sh[i,j]==eps*det(pts[p[i]],pts[p[j]])%3 for i in range(9) for j in range(9) if i!=j):matches.append((p,eps))
    assert len(matches)==48
    out={'schema':'w33.pass7322.heisenberg_area_extension.v1','status':'PASS',
      'extension':'1 -> C3 -> H27 -> C3^2 -> 1','order':27,'exponent':3,'center_order':3,'derived_order':3,
      'section_2_cocycle':'sigma(u,v)=-det(u,v)','horizontal_commutator':'[(u,0),(v,0)]=(0,det(u,v))',
      'pass7183_voltage':'up to affine gauge and global sign, psi(u,v)=det(u,v)',
      'triangle_holonomy':'det(v-u,w-u), the alternating commutator area',
      'theorem':'The Pass7183 C3 voltage is not merely graph-isomorphic to H27: its alternating area form is exactly the commutator form of the extraspecial Heisenberg central extension used by the qutrit Pauli model.',
      'firewall':'This C3 Heisenberg cocycle is distinct from the earlier E8 Z12 edge-phase cocycle, whose triangle residues are odd mod 12.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','center':3,'derived':3,'commutator':'det'}))
if __name__=='__main__':main()
