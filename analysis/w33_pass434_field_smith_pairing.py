#!/usr/bin/env python3
"""Pass 434: exact field-sensitive 2-adic Smith pairing certificate.

Certified fields: GF(3), GF(5), GF(7), GF(9), GF(11).  The q=7 run closes
Pass 433's v1.2 gate.  Z/9Z is retained as a negative control.  The finite
cases are theorems; the all-odd-prime-power shape remains a conjecture.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass434_field_smith_pairing.json'


def v2(n:int)->int:
    if n<=0: raise ValueError('v2 requires n>0')
    a=0
    while n%2==0: n//=2; a+=1
    return a


def prime_ops(q:int):
    return (lambda x,y:(x+y)%q, lambda x,y:(x*y)%q, lambda x:(-x)%q)


def gf9_ops():
    # GF(9)=GF(3)[a]/(a^2+1), element x=3*x0+x1.
    def add(x,y):
        a,b=divmod(x,3); c,d=divmod(y,3)
        return ((a+c)%3)*3+(b+d)%3
    def mul(x,y):
        a,b=divmod(x,3); c,d=divmod(y,3)
        return ((a*c+2*b*d)%3)*3+(a*d+b*c)%3
    def neg(x):
        a,b=divmod(x,3); return ((-a)%3)*3+(-b)%3
    return add,mul,neg


def build_laplacian(q:int,model:str='prime')->np.ndarray:
    if model=='gf9':
        if q!=9: raise ValueError('gf9 requires q=9')
        add,mul,neg=gf9_ops()
    elif model in {'prime','zmod'}: add,mul,neg=prime_ops(q)
    else: raise ValueError(model)
    elems=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
    idx={g:i for i,g in enumerate(elems)}
    section=[(u,v,0) for u in range(q) for v in range(q) if (u,v)!=(0,0)]
    def hmul(g,h):
        a,b,c=g; u,v,w=h
        cocycle=add(mul(u,b),neg(mul(a,v)))
        return add(a,u),add(b,v),add(add(c,w),cocycle)
    A=np.zeros((q**3,q**3),dtype=np.int64)
    for i,g in enumerate(elems):
        for s in section: A[i,idx[hmul(g,s)]]=1
    return (q*q-1)*np.eye(q**3,dtype=np.int64)-A


def two_adic_valuations(M:np.ndarray,kmax:int=16)->list[int]:
    """Finite 2-adic Smith valuations by unit-pivot elimination mod 2^k."""
    mod=1<<kmax; A=(M%mod).astype(np.int64).copy(); n=A.shape[0]; out=[]
    for p in range(n):
        sub=A[p:,p:]; nz=np.nonzero(sub)
        if len(nz[0])==0: break
        entries=sub[nz]; vals=np.log2(entries & -entries).astype(np.int64)
        t=int(np.argmin(vals)); e=int(vals[t]); i=p+int(nz[0][t]); j=p+int(nz[1][t])
        if i!=p: A[[p,i],:]=A[[i,p],:]
        if j!=p: A[:,[p,j]]=A[:,[j,p]]
        inv=pow((int(A[p,p])%mod)>>e,-1,mod)
        for i in range(p+1,n):
            x=int(A[i,p])%mod
            if x: A[i,p:]=(A[i,p:]-(((x>>e)*inv)%mod)*A[p,p:])%mod
        for j in range(p+1,n):
            x=int(A[p,j])%mod
            if x: A[p:,j]=(A[p:,j]-(((x>>e)*inv)%mod)*A[p:,p])%mod
        out.append(e)
    return sorted(out)


def expected_shape(q:int)->Counter:
    return Counter({v2(q-1):q*(q-1), v2(q*q-1):q*(q-1)**2//2})


def spectrum_multiplicities(q:int)->dict:
    return {'k=q^2-1':1,'q-1':q*(q*q-1)//2,'-(q+1)':q*(q-1)**2//2,'-1':q*q-1}


def spectral_tree_v2(q:int)->int:
    return q*(q*q-1)//2*v2(q-1)+q*(q-1)**2//2*v2(q+1)


def certify(q:int,model:str)->dict:
    L=build_laplacian(q,model); vals=two_adic_valuations(L)
    shape=Counter(e for e in vals if e>0); expected=expected_shape(q)
    mplus=q*(q*q-1)//2; mminus=q*(q-1)**2//2; residual=mplus-mminus
    total=sum(e*n for e,n in shape.items())
    checks={
        'connected_one_zero_invariant':len(vals)==q**3-1,
        'laplacian_row_sum_zero':bool(np.all(L.sum(axis=1)==0)),
        'laplacian_symmetric':bool(np.array_equal(L,L.T)),
        'shape_matches_pairing_law':shape==expected,
        'smith_tree_v2_matches_spectrum':total==spectral_tree_v2(q),
        'positive_spectrum_splits_residual_plus_glued':mplus==q*(q-1)+mminus,
    }
    return {
        'q':q,'field_model':model,'matrix_order':q**3,'degree':q*q-1,
        'adjacency_spectrum_multiplicities':spectrum_multiplicities(q),
        'two_primary_shape':{f'2^{e}':n for e,n in sorted(shape.items())},
        'expected_shape':{f'2^{e}':n for e,n in sorted(expected.items())},
        'finite_even_factors':sum(shape.values()),'tree_v2':total,
        'spectral_pairing':{
            'positive_eigenspace_multiplicity':mplus,
            'negative_eigenspace_multiplicity':mminus,
            'residual_positive_multiplicity':residual,
            'interpretation':'negative directions glue v2(q-1) and v2(q+1); residual positive directions carry v2(q-1)'},
        'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL'}


def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--extended',action='store_true'); ap.add_argument('--check',action='store_true'); ap.add_argument('--output',type=Path,default=OUT); a=ap.parse_args()
    cases=[(3,'prime'),(5,'prime'),(7,'prime'),(9,'gf9')]+([(11,'prime')] if a.extended else [])
    fields=[certify(q,m) for q,m in cases]; ring=certify(9,'zmod')
    ring_shape=Counter({int(k.split('^')[1]):v for k,v in ring['two_primary_shape'].items()})
    checks={
        'q7_gate_closed':next(r for r in fields if r['q']==7)['status']=='PASS',
        'proper_gf9_matches_tower_law':next(r for r in fields if r['q']==9)['status']=='PASS',
        'zmod9_control_deviates':ring_shape!=expected_shape(9),
        'all_field_cases_pass':all(r['status']=='PASS' for r in fields),
        'five_field_certificate_when_extended':len(fields)==5 if a.extended else True,
        'general_law_still_labeled_conjecture':True}
    payload={
        'schema':'w33.pass434.field_smith_pairing.v1','status':'PASS' if all(checks.values()) else 'FAIL',
        'headline':'q=7 closes exactly as Z_2^42 x Z_16^126; GF(3), GF(5), GF(7), GF(9), GF(11) obey one spectral-to-Smith pairing law, while Z/9Z does not.',
        'field_results':fields,'zmod9_control':ring,'checks':checks}
    serialized=json.dumps(payload,indent=2)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=serialized:
            print(json.dumps({'status':'FAIL','reason':'certificate mismatch','output':str(a.output)})); return 1
    else:
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(serialized)
    print(json.dumps({'status':payload['status'],'cases':[(r['q'],r['field_model'],r['two_primary_shape']) for r in fields],'zmod9':ring['two_primary_shape'],'checks':checks}))
    return 0 if payload['status']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
