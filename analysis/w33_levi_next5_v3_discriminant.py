#!/usr/bin/env python3
"""Full PSp(4,3):2 action on the 2-primary chiral discriminant module."""
from __future__ import annotations

from collections import deque
from fractions import Fraction
import json

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from w33_levi_next5_v3_common import (
    build_w33, group_closure_cols, point_outer_perm,
    point_transvection_perm, sha256_json,
)

SEEDS=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
       (1,1,0,0),(1,0,1,0),(0,1,0,1),(1,1,1,1)]


def smith(A: Matrix):
    D,S,T=smith_normal_decomp(DomainMatrix.from_Matrix(A).convert_to(ZZ))
    return D.to_Matrix(),S.to_Matrix(),T.to_Matrix()


def saturated_kernel(A:Matrix)->Matrix:
    D,S,T=smith(A)
    zero=[i for i in range(min(D.shape)) if D[i,i]==0]
    zero += list(range(min(D.shape),A.cols))
    B=T[:,zero]
    assert A*B==Matrix.zeros(A.rows,len(zero))
    return B


def perm_matrix_action(B:Matrix, perm:tuple[int,...])->Matrix:
    inverse=[0]*len(perm)
    for i,j in enumerate(perm): inverse[j]=i
    PB=Matrix([[int(B[inverse[r],c]) for c in range(B.cols)] for r in range(B.rows)])
    G=B.T*B
    A=G.inv()*B.T*PB
    assert all(x.q==1 for x in A)
    A=Matrix([[int(x) for x in A.row(r)] for r in range(A.rows)])
    assert B*A==PB and A.T*G*A==G and abs(int(A.det()))==1
    return A


def p2_structure(D:Matrix):
    rows=[]
    for i in range(D.rows):
        d=abs(int(D[i,i]))
        if d<=1: continue
        a=0;t=d
        while t%2==0:a+=1;t//=2
        if a: rows.append({'snf_index':i,'full_order':d,'p_order':2**a,'odd_part':t})
    return rows


def action_in_p2(A:Matrix,S:Matrix,D:Matrix,parts:list[dict]):
    Sinv=S.inv(); Adual=A.inv().T
    images=[]
    for part in parts:
        y=Matrix.zeros(D.rows,1); y[part['snf_index'],0]=part['odd_part']
        z=Sinv*y
        yp=S*(Adual*z)
        coord=[]
        for target in parts:
            mod=target['p_order']; odd=target['odd_part']%mod
            val=int(yp[target['snf_index'],0])%mod
            coord.append((val*pow(odd,-1,mod))%mod)
        images.append(tuple(coord))
    return tuple(images)


def add_coord(a,b,mods): return tuple((x+y)%m for x,y,m in zip(a,b,mods))
def scale_coord(k,a,mods): return tuple((k*x)%m for x,m in zip(a,mods))

def apply_auto(auto,coord,mods):
    out=(0,)*len(mods)
    for k,img in zip(coord,auto):
        if k: out=add_coord(out,scale_coord(k,img,mods),mods)
    return out


def common_numerator(coord,parts,S,D,G,Sinv=None,Ginv=None):
    """Return numerator w modulo 8 for dual element with denominator 8."""
    y=Matrix.zeros(D.rows,1)
    for c,part in zip(coord,parts):
        y[part['snf_index'],0]=part['odd_part']*c
    Sinv = S.inv() if Sinv is None else Sinv
    Ginv = G.inv() if Ginv is None else Ginv
    v=Ginv*(Sinv*y)
    w=[]
    for x in v:
        y8=x*8
        assert y8.q==1
        w.append(int(y8)%8)
    return w


def q_num128(coord,parts,S,D,G,Sinv=None,Ginv=None):
    w=Matrix(common_numerator(coord,parts,S,D,G,Sinv,Ginv))
    return int((w.T*G*w)[0])%128


def bil_num64(a,b,parts,S,D,G,Sinv=None,Ginv=None):
    wa=Matrix(common_numerator(a,parts,S,D,G,Sinv,Ginv));wb=Matrix(common_numerator(b,parts,S,D,G,Sinv,Ginv))
    return int((wa.T*G*wb)[0])%64


def to_2torsion_cols(auto,parts):
    """15D F2 action on A[2], basis 1 for order2 and 4h for order8."""
    mods=[p['p_order'] for p in parts]; n=len(parts)
    basis=[]
    for i,m in enumerate(mods):
        c=[0]*n;c[i]=1 if m==2 else 4;basis.append(tuple(c))
    def encode(c):
        mask=0
        for i,m in enumerate(mods):
            bit=(c[i]%2) if m==2 else ((c[i]//4)&1)
            if bit:mask|=1<<i
        return mask
    cols=[]
    for b in basis:
        im=apply_auto(auto,b,mods)
        assert all((x in (0,1) if m==2 else x in (0,4)) for x,m in zip(im,mods))
        cols.append(encode(im))
    return tuple(cols)


def analyze():
    geom=build_w33(); M=Matrix(geom.incidence.tolist())
    B=saturated_kernel(M); assert B.shape==(40,15)
    G=B.T*B
    D,S,T=smith(G)
    diag=[abs(int(D[i,i])) for i in range(15)]
    perms=[point_transvection_perm(geom.points,v) for v in SEEDS]+[point_outer_perm(geom.points)]
    lattice=[perm_matrix_action(B,p) for p in perms]
    parts=p2_structure(D);mods=[p['p_order'] for p in parts]
    assert sorted(mods)==[2]*14+[8]
    autos=[action_in_p2(A,S,D,parts) for A in lattice]
    n=len(parts); zero=(0,)*n
    gens=[]
    for i,m in enumerate(mods):
        c=[0]*n;c[i]=1;gens.append(tuple(c))
    Sinv=S.inv();Ginv=G.inv()
    qbasis=[q_num128(c,parts,S,D,G,Sinv,Ginv) for c in gens]
    bbasis=[[bil_num64(a,b,parts,S,D,G,Sinv,Ginv) for b in gens] for a in gens]
    preserve=[]
    for auto in autos:
        ok=True
        images=[apply_auto(auto,g,mods) for g in gens]
        for i in range(n):
            if q_num128(images[i],parts,S,D,G,Sinv,Ginv)!=qbasis[i]:ok=False
            for j in range(n):
                if bil_num64(images[i],images[j],parts,S,D,G,Sinv,Ginv)!=bbasis[i][j]:ok=False
        preserve.append(ok)
    twocols=[to_2torsion_cols(a,parts) for a in autos]
    psp_order=len(group_closure_cols(twocols[:5],15,25920))
    ext_order=len(group_closure_cols(twocols[:5]+[twocols[-1]],15,51840))
    h=mods.index(8); hcoord=gens[h]; fourh=list(zero);fourh[h]=4;fourh=tuple(fourh)
    outer_h=apply_auto(autos[-1],hcoord,mods)
    psp_h=[apply_auto(a,hcoord,mods) for a in autos[:-1]]
    orbit={hcoord}; queue=deque([hcoord])
    while queue:
        x=queue.popleft()
        for a in autos[:5]:
            y=apply_auto(a,x,mods)
            if y not in orbit: orbit.add(y); queue.append(y)
    outer_squared=apply_auto(autos[-1],apply_auto(autos[-1],hcoord,mods),mods)==hcoord
    def classify(image):
        elem=tuple(image[i] if i!=h else 0 for i in range(n)); z=image[h]
        if all(x==0 for x in elem) and z==1:return 'fixed'
        if all(x==0 for x in elem) and z==7:return 'inverted'
        return 'mixed'
    fixed4=all(apply_auto(a,fourh,mods)==fourh for a in autos)
    qh=Fraction(qbasis[h],64)
    while qh>=2: qh-=2
    checks={
      'trade_rank_15':B.shape==(40,15),
      'p2_type_2_14_plus_8':sorted(mods)==[2]*14+[8],
      'all_generators_quadratic_isometries':all(preserve),
      'psp_action_faithful_25920':psp_order==25920,
      'outer_extends_to_51840':ext_order==51840,
      'four_h_fixed_by_full_group':fixed4,
      'qh_11_over_8':qh==Fraction(11,8),
      'outer_action_is_involution':outer_squared,
      'h_orbit_size_2880':len(orbit)==2880,
    }
    def image_record(auto): return [list(x) for x in auto]
    return {
      'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'lattice':{'rank':15,'gram_snf':diag,'p2_structure':'(Z/2)^14 + Z/8'},
      'canonical_parts':parts,
      'quadratic':{'q_h':str(qh),'q_numerator_mod128':qbasis[h],'fixed_line':'<4h>'},
      'actions':{
        'PSp_generators':[image_record(a) for a in autos[:-1]],
        'outer':image_record(autos[-1]),
        'outer_h_image':list(outer_h),
        'outer_h_classification':classify(outer_h),
        'psp_h_classifications':[classify(x) for x in psp_h],
        'h_orbit_size':len(orbit),
        'order_on_2_torsion':{'PSp43':psp_order,'extension':ext_order},
      },
      'digests':{'trade_basis':sha256_json([[int(B[r,c]) for c in range(15)] for r in range(40)]),'actions':sha256_json(autos)},
      'theorem':'Every native generator lifts to a quadratic automorphism of (Z/2)^14+Z/8; <4h> is fixed, the U14- quotient action is faithful, and the outer action on h is classified explicitly.'
    }


def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
