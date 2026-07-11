#!/usr/bin/env python3
"""Periodic H^2 classes for a prescribed C2 action and rail transgression."""
from __future__ import annotations
from functools import lru_cache
from fractions import Fraction
import json
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from w33_levi_next5_v5_common import (
    SEEDS, apply_cols, build_w33, coordinates, gf2_nullspace, gf2_rank,
    gf2_row_basis, in_span, point_outer_perm, point_transvection_perm,
    sha256_json, tagged_basis,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_2026_07_11_LEVI_NEXT5_V5_extension.json"


def smith(A: Matrix):
    D,S,T=smith_normal_decomp(DomainMatrix.from_Matrix(A).convert_to(ZZ))
    return D.to_Matrix(),S.to_Matrix(),T.to_Matrix()

def saturated_kernel(A:Matrix)->Matrix:
    D,_S,T=smith(A)
    zero=[i for i in range(min(D.shape)) if D[i,i]==0]
    zero+=list(range(min(D.shape),A.cols))
    B=T[:,zero]
    assert A*B==Matrix.zeros(A.rows,len(zero))
    return B

def perm_matrix_action(B:Matrix,perm:tuple[int,...])->Matrix:
    inv=[0]*len(perm)
    for i,j in enumerate(perm): inv[j]=i
    PB=Matrix([[int(B[inv[r],c]) for c in range(B.cols)] for r in range(B.rows)])
    G=B.T*B
    A=G.inv()*B.T*PB
    assert all(x.q==1 for x in A)
    A=Matrix([[int(x) for x in A.row(r)] for r in range(A.rows)])
    assert B*A==PB and A.T*G*A==G and abs(int(A.det()))==1
    return A

def p2_structure(D:Matrix):
    out=[]
    for i in range(D.rows):
        d=abs(int(D[i,i]))
        if d<=1: continue
        a=0;t=d
        while t%2==0: a+=1;t//=2
        if a: out.append({'snf_index':i,'full_order':d,'p_order':2**a,'odd_part':t})
    return out

def action_in_p2(A:Matrix,S:Matrix,D:Matrix,parts:list[dict]):
    Sinv=S.inv(); Adual=A.inv().T; images=[]
    for part in parts:
        y=Matrix.zeros(D.rows,1); y[part['snf_index'],0]=part['odd_part']
        z=Sinv*y; yp=S*(Adual*z); coord=[]
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
    for k,image in zip(coord,auto):
        if k: out=add_coord(out,scale_coord(k,image,mods),mods)
    return out

def torsion_basis(mods):
    out=[]
    for i,m in enumerate(mods):
        c=[0]*len(mods); c[i]=1 if m==2 else 4; out.append(tuple(c))
    return out

def torsion_mask(coord,mods):
    mask=0
    for i,(x,m) in enumerate(zip(coord,mods)):
        bit=x&1 if m==2 else (x//4)&1
        if bit: mask|=1<<i
    return mask

def coord_from_mask(mask,mods):
    return tuple((1 if m==2 else 4) if (mask>>i)&1 else 0 for i,m in enumerate(mods))
def torsion_cols(auto,mods): return tuple(torsion_mask(apply_auto(auto,b,mods),mods) for b in torsion_basis(mods))
def map_rows(cols,dim):
    return [sum(((cols[c]>>r)&1)<<c for c in range(dim)) for r in range(dim)]
def nullspace_map(cols,dim): return gf2_nullspace(map_rows(cols,dim),dim)

def solve_preimage(cols,target,dim):
    sols=[v for v in range(1<<dim) if apply_cols(cols,v)==target]
    if not sols: return None
    return min(sols,key=lambda x:(x.bit_count(),x))

def common_numerator(coord,parts,S,D,G):
    y=Matrix.zeros(D.rows,1)
    for c,part in zip(coord,parts): y[part['snf_index'],0]=part['odd_part']*c
    v=G.inv()*(S.inv()*y); out=[]
    for x in v:
        y8=x*8; assert y8.q==1; out.append(int(y8)%8)
    return out

def q_num128(coord,parts,S,D,G):
    w=Matrix(common_numerator(coord,parts,S,D,G))
    return int((w.T*G*w)[0])%128

def class_coords(v,image,reps):
    rem,tag=coordinates(v,tagged_basis(image+reps)); assert rem==0
    return tag>>len(image)

def canonical_class_rep(coord,image,reps):
    base=0
    for i,r in enumerate(reps):
        if (coord>>i)&1: base^=r
    span=[0]
    for b in gf2_row_basis(image): span += [x^b for x in tuple(span)]
    candidates=[base^x for x in span]
    return min(candidates,key=lambda x:(x.bit_count(),x))

@lru_cache(maxsize=1)
def analyze():
    geom=build_w33(); M=Matrix(geom.incidence.tolist())
    B=saturated_kernel(M); G=B.T*B; D,S,_T=smith(G)
    parts=p2_structure(D); mods=[p['p_order'] for p in parts]
    assert sorted(mods)==[2]*14+[8]
    perms=[point_transvection_perm(geom.points,v) for v in SEEDS]+[point_outer_perm(geom.points)]
    actions=[perm_matrix_action(B,p) for p in perms]
    autos=[action_in_p2(A,S,D,parts) for A in actions]
    outer=autos[-1]; h_index=mods.index(8); dim=15
    h=tuple(1 if i==h_index else 0 for i in range(dim))
    outer_h=apply_auto(outer,h,mods); five_h=tuple(5 if i==h_index else 0 for i in range(dim))
    ucoord=add_coord(outer_h,scale_coord(-1,five_h,mods),mods); u=torsion_mask(ucoord,mods)
    T=torsion_cols(outer,mods); I=tuple(1<<i for i in range(dim)); N=tuple(T[i]^I[i] for i in range(dim))
    kernel=nullspace_map(N,dim); image=gf2_row_basis(N)
    reps=[]; span=list(image)
    for v in kernel:
        if not in_span(v,span): reps.append(v); span=gf2_row_basis(span+[v])
    assert len(reps)==3
    fixed=1<<h_index
    h1u=class_coords(u,image,reps); h1f=class_coords(fixed,image,reps)
    combined=u^fixed
    gauge=solve_preimage(N,combined,dim)
    assert gauge is not None
    gaugecoord=coord_from_mask(gauge,mods)
    hprime=add_coord(h,gaugecoord,mods)
    fixed_hprime=apply_auto(outer,hprime,mods)==hprime
    order=lambda x: next(k for k in range(1,17) if all(v==0 for v in scale_coord(k,x,mods)))

    classes=[]
    for c in range(1<<len(reps)):
        rep=canonical_class_rep(c,image,reps)
        coord=coord_from_mask(rep,mods)
        qv=Fraction(q_num128(coord,parts,S,D,G),64)
        while qv>=2:qv-=2
        classes.append({
            'class':hex(c),'selected_min_hamming_smith_mask':hex(rep),
            'selected_mask_weight':rep.bit_count(),
            'representative_quadratic_value_mod_2':str(qv),'split':c==0,
            'outer_lift_order':2 if c==0 else 4,
        })

    # In characteristic two the cyclic C2 resolution has the same differential in
    # every positive degree, so H1 and H2 are represented by the same quotient.
    checks={
        'module_type':sorted(mods)==[2]*14+[8],
        'H1_dimension_3':len(kernel)-len(image)==3,
        'H2_dimension_3':len(kernel)-len(image)==3,
        'periodicity_chain_maps_equal':N==tuple(T[i]^I[i] for i in range(dim)),
        'mixed_equals_fixed_line_class':h1u==h1f and h1u!=0,
        'combined_transgression_zero':in_span(combined,image),
        'explicit_gauge_found':gauge is not None and apply_cols(N,gauge)==combined,
        'gauged_order8_generator_fixed':fixed_hprime and order(hprime)==8,
        'scalar5_mixing_still_nonremovable':not in_span(u,image),
        'eight_H2_classes':len(classes)==8 and sum(not x['split'] for x in classes)==7,
        'crossed_product_associativity_condition':all(
            apply_cols(N,int(x['selected_min_hamming_smith_mask'],16))==0
            for x in classes
        ),
    }
    return {
        'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
        'module':{'type':'(Z/2)^14 + Z/8','h_index':h_index,'torsion_dimension':15},
        'periodic_cohomology':{
            'kernel_dimension':len(kernel),'coboundary_dimension':len(image),
            'H1_dimension':3,'H2_dimension':3,
            'H1_representatives':[hex(x) for x in reps],
            'H2_representatives':[hex(x) for x in reps],
            'mixed_class':hex(h1u),'fixed_line_class':hex(h1f),
            'periodicity':'H^(n+2)(C2,M) = H^n(C2,M) for n>=1; in characteristic two both differentials are 1+tau.',
        },
        'transgression':{
            'exact_sequence':'0 -> A[2] -> A -> A/A[2] -> 0',
            'quotient_generator':'h mod A[2]',
            'delta_raw_mask':hex(combined),
            'delta_class':'0x0',
            'reason':'tau(h)-h = u+4h and [u]=[4h], so the two nonzero H1 classes cancel.',
            'minimal_gauge_mask':hex(gauge),'minimal_gauge_weight':gauge.bit_count(),
            'fixed_order8_lift':list(hprime),
        },
        'H2_extension_classes_prescribed_action':classes,
        'representative_convention':(
            'Each H2 class is labeled by a minimum-Hamming mask in the selected '
            'Smith-coordinate basis. The mask, its weight, and the displayed '
            'quadratic value are representative/basis dependent; the cohomology '
            'class and split/non-split status are the invariant content.'
        ),
        'digests':{'outer_action':sha256_json(T),'H2_classes':sha256_json(classes),'fixed_gauge':sha256_json(list(hprime))},
        'theorem':(
            'The C2-module A[2] has periodic H1=H2 of dimension three. The mixed class equals the fixed-line '
            'class and selects a non-split order-four lift for the prescribed nontrivial C2 action, but the connecting transgression of '
            'h mod A[2] vanishes because tau(h)-h=u+4h has zero class. Consequently an explicit order-eight '
            'generator h+v is tau-fixed, even though no gauge removes u while retaining scalar action 5.'
        ),
        'scope_boundary':(
            'This classifies group extensions with the prescribed nontrivial C2 action on the exact '
            '2-torsion module; they are not central extensions. It also computes the connecting map '
            'for the order-eight rail. It does not assert a unique global extension of the integral '
            'Weyl lattice, and Smith-coordinate representative labels are not canonical.'
        )
    }

def main():
    out=analyze();text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    OUT.write_text(text,encoding="utf-8");print(text,end="")
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
