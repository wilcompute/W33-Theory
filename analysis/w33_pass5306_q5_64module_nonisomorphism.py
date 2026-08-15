#!/usr/bin/env python3
"""Pass5306: the two q5 64-dimensional modules are NOT PSp4(5)-isomorphic.

Two dimension-64 objects had appeared:
  R = ker_2(N)/<1>, the relation module among the 156 local PG(3,2) fibers;
  H = Hull(C_F), the 64-dimensional hull of the q5 footprint code.

Equal dimensions invited an intertwiner search.  A single conjugacy invariant kills
that shortcut.  For a symplectic transvection, the fixed-space dimension is 4 on
R but 24 on H.  Therefore R and H cannot be isomorphic as PSp4(5)-modules, and no
invertible equivariant 64x64 intertwiner exists.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import p_component_assignment
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5306_Q5_64MODULE_NONISOMORPHISM.json'

def basis(rows):
    piv={};B=[]
    for x in rows:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;B.append(x);break
    return B

def rank(rows):return len(basis(rows))
def deps(cols):
    piv={};D=[]
    for i,x0 in enumerate(cols):
        x=x0;c=1<<i
        while x:
            p=x.bit_length()-1
            if p in piv:y,d=piv[p];x^=y;c^=d
            else:piv[p]=(x,c);break
        if not x:D.append(c)
    return D,len(piv)

def pbits(x,p):
    z=0
    while x:
        lb=x&-x;i=lb.bit_length()-1;x-=lb;z|=1<<p[i]
    return z

def main():
    G=build_W(5);acid,nc=p_component_assignment(G);assert nc==325
    blocks=[set() for _ in range(325)]
    for a,A in enumerate(G['apartments']):blocks[acid[a]].update(A)
    # W point-line incidence: dependencies among the 156 line columns give ker N.
    linecols=[]
    for L in G['lines']:
        z=0
        for p in L:z|=1<<p
        linecols.append(z)
    R,rN=deps(linecols);assert rN==91 and len(R)==65
    # Footprint code row basis and its hull.
    F=[]
    for p in range(156):
        z=0
        for c,B in enumerate(blocks):
            if p in B:z|=1<<c
        F.append(z)
    FB=basis(F);assert len(FB)==65
    gram=[]
    for i in range(65):
        z=0
        for j in range(65):
            if (FB[i]&FB[j]).bit_count()&1:z|=1<<j
        gram.append(z)
    HC,rg=deps(gram);assert rg==1 and len(HC)==64
    Hull=[]
    for c in HC:
        z=0
        for i in range(65):
            if (c>>i)&1:z^=FB[i]
        Hull.append(z)
    assert rank(Hull)==64
    # One standard symplectic transvection.
    pts=G['pts'];pi={p:i for i,p in enumerate(pts)};v=(1,0,0,0)
    def norm(x):
        for a in x:
            if a:
                s=pow(a,-1,5);return tuple(s*y%5 for y in x)
        raise ValueError
    def sp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%5
    pp=[]
    for x in pts:
        a=sp(x,v);pp.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
    lk={tuple(sorted(L)):i for i,L in enumerate(G['lines'])}
    lp=[lk[tuple(sorted(pp[p] for p in L))] for L in G['lines']]
    bk={tuple(sorted(B)):i for i,B in enumerate(blocks)}
    bp=[bk[tuple(sorted(pp[p] for p in B))] for B in blocks]
    # Fixed quotient dimension on R/<1>: rank differences modulo the constant line vector.
    one=(1<<156)-1
    dR=[x^pbits(x,lp) for x in R]
    rank_mod_constant=rank(dR+[one])-1
    fixed_R=64-rank_mod_constant
    dH=[x^pbits(x,bp) for x in Hull]
    fixed_H=64-rank(dH)
    assert fixed_R==4 and fixed_H==24
    out={'pass':5306,'status':'THEOREM_Q5_RELATION64_AND_FOOTPRINT_HULL64_ARE_NOT_ISOMORPHIC_PSP4_MODULES',
      'relation_module':'ker_2(N)/<1>','relation_dimension':64,
      'footprint_hull_dimension':64,
      'test_element':'standard symplectic transvection',
      'fixed_dimension_relation_module':fixed_R,'fixed_dimension_footprint_hull':fixed_H,
      'conclusion':'Fixed-space dimension is an isomorphism invariant, so no PSp4(5)-equivariant invertible 64x64 intertwiner exists.',
      'consequence_for_frontier':'The all-odd rank/generation theorem cannot be closed by simply identifying the two q5 dimension-64 modules.',
      'boundary':'Negative module theorem; it does not rule out non-equivariant vector-space bijections or other indirect maps.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
