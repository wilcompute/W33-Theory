#!/usr/bin/env python3
"""Pass 456: exact anatomy of the four q=5 spectral collisions from Pass 447."""
from __future__ import annotations
import argparse,itertools,json,random
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass456_q5_collision_anatomy.json'
Q=5

def setup():
    q=Q;elems=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)];idx={e:i for i,e in enumerate(elems)}
    vecs=[(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)]
    pairs=[];used=set()
    for v in vecs:
        nv=(-v[0]%q,-v[1]%q);key=tuple(sorted((v,nv)))
        if key not in used:used.add(key);pairs.append(key)
    def hmul(g,h):return ((g[0]+h[0])%q,(g[1]+h[1])%q,(g[2]+h[2]-g[0]*h[1]+h[0]*g[1])%q)
    def matrices(offsets):
        S=[]
        for (v,nv),c in zip(pairs,offsets):S += [(v[0],v[1],c),(nv[0],nv[1],-c%q)]
        A=np.zeros((125,125),dtype=np.int64)
        for i,g in enumerate(elems):
            for s in S:A[i,idx[hmul(g,s)]]=1
        return A,24*np.eye(125,dtype=np.int64)[:-1,:-1]-A[:-1,:-1]
    return vecs,pairs,matrices

def full_function(pairs,offsets):
    f={}
    for (v,nv),c in zip(pairs,offsets):f[v]=c;f[nv]=-c%Q
    return f

def orbit_contains(vecs,pairs,left,right):
    f=full_function(pairs,left);q=Q
    GL=[]
    for a,b,c,d in itertools.product(range(q),repeat=4):
        det=(a*d-b*c)%q
        if det:GL.append((a,b,c,d,det))
    def inv(A):
        a,b,c,d,det=A;u=pow(det,-1,q);return (d*u%q,-b*u%q,-c*u%q,a*u%q)
    def mv(M,v):a,b,c,d=M;return ((a*v[0]+b*v[1])%q,(c*v[0]+d*v[1])%q)
    target=tuple(right)
    for A in GL:
        ai=inv(A);det=A[4]
        for r,s in itertools.product(range(q),repeat=2):
            vals=[]
            for v,nv in pairs:
                pre=mv(ai,v);vals.append((det*f[pre]+r*v[0]+s*v[1])%q)
            if tuple(vals)==target:return True
    return False

def padic_counts(matrix,prime,max_level):
    modulus=prime**max_level;a=matrix.astype(np.int64,copy=True)%modulus;counts=[]
    for _ in range(max_level):
        n=a.shape[0];rank=0
        while rank<n:
            loc=np.argwhere((a[rank:,rank:]%prime)!=0)
            if loc.size==0:break
            i=rank+int(loc[0,0]);j=rank+int(loc[0,1])
            if i!=rank:a[[rank,i],:]=a[[i,rank],:]
            if j!=rank:a[:,[rank,j]]=a[:,[j,rank]]
            a[rank,:]=(a[rank,:]*pow(int(a[rank,rank]),-1,modulus))%modulus
            factors=a[:,rank].copy();factors[rank]=0
            a=(a-factors[:,None]*a[rank:rank+1,:])%modulus;a[rank,rank+1:]=0;rank+=1
        counts.append(rank);rem=a[rank:,rank:]
        if rem.size==0:return counts
        if np.any(rem%prime):raise AssertionError('p-adic elimination failure')
        modulus//=prime;a=(rem//prime)%modulus
    raise AssertionError((prime,a.shape[0]))

def weld(size,primary):
    vals=[1]*size
    for p,counts in primary.items():
        exps=[]
        for e,m in enumerate(counts):exps += [e]*m
        for i,e in enumerate(sorted(exps)):vals[i]*=p**e
    return {str(v):m for v,m in sorted(Counter(vals).items()) if v>1}

def local_profile(A):
    A2=A@A
    return {str(k):v for k,v in sorted(Counter(int(A2[0,j]) for j in range(1,125) if not A[0,j]).items())}

def build_payload():
    vecs,pairs,matrices=setup();r=random.Random(447);groups=defaultdict(list)
    for sample in range(400):
        offsets=tuple(r.randrange(Q) for _ in pairs);A,_=matrices(offsets)
        key=tuple(np.round(np.linalg.eigvalsh(A.astype(float)),6));groups[key].append((sample,offsets))
    collisions=[rows for rows in groups.values() if len(rows)>1]
    records=[];genuine=None
    for rows in collisions:
        (i,a),(j,b)=rows;equiv=orbit_contains(vecs,pairs,a,b)
        rec={'samples':[i,j],'offsets':[list(a),list(b)],'affine_aut_equivalent':equiv}
        records.append(rec)
        if not equiv:genuine=(a,b,rec)
    a,b,rec=genuine;A0,L0=matrices(a);A1,L1=matrices(b)
    iso=nx.is_isomorphic(nx.from_numpy_array(A0),nx.from_numpy_array(A1))
    x=sp.symbols('x');cp=sp.factor(sp.Matrix(A0).charpoly(x).as_expr());tree=abs(int(sp.diff(cp,x).subs(x,24)))//125;fac=sp.factorint(tree)
    groups_smith=[]
    for L in (L0,L1):
        primary={int(p):padic_counts(L,int(p),8 if p<=5 else 2) for p in fac}
        groups_smith.append(weld(124,primary))
    rec.update({
      'graph_isomorphic':iso,'characteristic_polynomial':str(cp),
      'spanning_tree_prime_factorization':{str(p):int(e) for p,e in fac.items()},
      'critical_groups':groups_smith,'critical_groups_equal':groups_smith[0]==groups_smith[1],
      'nonneighbor_common_neighbor_profiles':[local_profile(A0),local_profile(A1)],
      'profiles_distinguish_graphs':local_profile(A0)!=local_profile(A1),
    })
    checks={
      'reproduced_396_distinct':len(groups)==396,
      'collision_profile_392_singletons_4_pairs':Counter(map(len,groups.values()))==Counter({1:392,2:4}),
      'four_collision_pairs':len(collisions)==4,
      'three_pairs_are_affine_orbit_repeats':sum(r['affine_aut_equivalent'] for r in records)==3,
      'one_pair_affine_inequivalent':sum(not r['affine_aut_equivalent'] for r in records)==1,
      'genuine_pair_nonisomorphic':not iso,
      'genuine_pair_cospectral':bool(np.allclose(np.linalg.eigvalsh(A0),np.linalg.eigvalsh(A1))),
      'genuine_pair_smith_identical':groups_smith[0]==groups_smith[1],
      'local_profile_distinguishes':local_profile(A0)!=local_profile(A1),
    }
    return {
      'schema':'w33.pass456.q5_collision_anatomy.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'sample_seed':447,'samples':400,'distinct_spectra':len(groups),'collision_profile':{str(k):v for k,v in Counter(map(len,groups.values())).items()},
      'collisions':records,
      'headline':(
        'Of the four Pass-447 spectral collisions, three are repeats inside the 12,000-element affine automorphism orbit. '
        'The fourth is a pair of nonisomorphic 125-vertex Cayley graphs that are cospectral and have the same complete '
        'critical group. Smith torsion therefore fails to separate the first genuine q=5 collision.'),
      'genuine_pair_critical_group':groups_smith[0],
      'checks':checks,
    }
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 456 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
