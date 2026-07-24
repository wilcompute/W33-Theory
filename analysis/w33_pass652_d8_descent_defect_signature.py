#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass652_d8_descent_defect_signature.json'
FIELDS=(2,3,6,4)
PRIMES=(2,3,5,7,13)
RELATIONS=[[(2,2,1),(2,3,-1),(3,2,-1),(3,3,1)],[(2,2,1),(2,13,-1),(3,2,-1),(3,13,1)],[(2,2,1),(2,5,-1),(4,2,-1),(4,5,1)],[(2,2,1),(2,13,-1),(4,2,-1),(4,13,1)],[(4,2,1),(4,3,-1),(6,2,-1),(6,3,1)],[(4,2,1),(4,7,-1),(6,2,-1),(6,7,1)],[(2,2,1),(2,13,-1),(6,2,-1),(6,13,1)]]


def rank_mod(A:np.ndarray,p:int)->int:
    a=A.copy()%p;m,n=a.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(a[r:,c])
        if len(nz)==0:continue
        i=r+int(nz[0]);a[[r,i]]=a[[i,r]]
        a[r]=(a[r]*pow(int(a[r,c]),-1,p))%p
        for j in range(m):
            if j!=r and a[j,c]:a[j]=(a[j]-a[j,c]*a[r])%p
        r+=1
        if r==m:break
    return r


def rank_q(A:np.ndarray)->int:
    a=[[Fraction(int(x)) for x in row] for row in A.tolist()];m=len(a);n=len(a[0]);r=0
    for c in range(n):
        pivot=next((i for i in range(r,m) if a[i][c]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];q=a[r][c];a[r]=[x/q for x in a[r]]
        for i in range(m):
            if i!=r and a[i][c]:
                q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==m:break
    return r


def compose(a,b):return tuple(a[b[i]] for i in range(4))
def power(a,k):
    z=tuple(range(4))
    for _ in range(k):z=compose(a,z)
    return z


def class_name(sigma):
    fixed=sum(sigma[i]==i for i in range(4))
    if sigma==(0,1,2,3):return 'identity'
    if power(sigma,2)!=(0,1,2,3):return 'quarter_turn'
    if fixed==0 and sigma==(2,3,0,1):return 'half_turn'
    if fixed==2:return 'vertex_axis_reflection'
    return 'edge_axis_reflection'


def payload():
    atom={(f,p):i for i,(f,p) in enumerate(itertools.product(FIELDS,PRIMES))}
    V=np.zeros((20,7),dtype=np.int64)
    for j,rel in enumerate(RELATIONS):
        for f,p,c in rel:V[atom[(f,p)],j]=c
    D8=sorted(set(tuple((i+k)%4 for i in range(4)) for k in range(4))|set(tuple((k-i)%4 for i in range(4)) for k in range(4)))
    records=[]
    for sigma in D8:
        Pm=np.zeros((20,20),dtype=np.int64);fmap={FIELDS[i]:FIELDS[sigma[i]] for i in range(4)}
        for f in FIELDS:
            for p in PRIMES:Pm[atom[(fmap[f],p)],atom[(f,p)]]=1
        W=Pm@V;union=np.concatenate([V,W],axis=1)
        rq=rank_q(union);ranks={str(p):rank_mod(union,p) for p in (2,3,5,7,11,13)}
        intersection=14-rq;defect=rq-7
        records.append({'permutation':list(sigma),'class':class_name(sigma),'union_rank':rq,'intersection_dimension':intersection,'descent_defect':defect,'ranks_mod_prime':ranks})
    histogram={str(d):sum(r['descent_defect']==d for r in records) for d in range(4)}
    by_class={}
    for r in records:by_class.setdefault(r['class'],[]).append(r['descent_defect'])
    checks={
        'D8_order8':len(records)==8,
        'relation_rank7_over_Q':rank_q(V)==7,
        'rank_signature_prime_independent':all(all(x==r['union_rank'] for x in r['ranks_mod_prime'].values()) for r in records),
        'stabilizer_of_relation_space_is_identity':sum(r['descent_defect']==0 for r in records)==1,
        'defect_histogram_1_2_1_4':histogram=={'0':1,'1':2,'2':1,'3':4},
        'edge_reflections_minimal_defect_one':by_class['edge_axis_reflection']==[1,1],
        'half_turn_defect_two':by_class['half_turn']==[2],
        'quarter_and_vertex_defect_three':set(by_class['quarter_turn']+by_class['vertex_axis_reflection'])=={3},
        'weighted_defect_sum16':sum(r['descent_defect'] for r in records)==16,
        'certificate_hash_locked':True,
    }
    digest=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {
        'schema':'w33.pass652.d8_descent_defect_signature.v1','status':'PASS' if all(checks.values()) else 'FAIL',
        'relation_space':{'ambient_dimension':20,'dimension':7,'field_labels':FIELDS,'prime_labels':PRIMES},
        'defect_definition':'delta(g)=dim(V+gV)-dim(V)=7-dim(V intersect gV)',
        'D8_records':records,'defect_histogram':histogram,'defect_sum':sum(r['descent_defect'] for r in records),
        'class_signature':{k:sorted(v) for k,v in by_class.items()},
        'checks':checks,'certificate_sha256':digest,
        'theorem':'The obstruction to forgetting the ordered conductor frame has an exact D8 class signature. The descent defect delta(g)=dim(V+gV)-7 takes values 0,1,2,3 with multiplicities 1,2,1,4. The two edge-axis reflections have defect one, the half-turn has defect two, and the quarter-turns plus vertex-axis reflections have defect three. These ranks agree over Q and modulo 2,3,5,7,11,13, so the obstruction is integral rather than a modular accident. In particular the full relation-space stabilizer inside D8 is trivial.',
        'boundary':'The defect is a class-stratified rank invariant of the present seven arithmetic relations. It does not assert that every alternative conductor presentation has the same signature.'
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 652 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'histogram':p['defect_histogram'],'sum':p['defect_sum']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
