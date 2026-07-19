#!/usr/bin/env python3
"""Pass 470: graph-specific integral conductor-coupling tower for the Z/9 Laplacian.

Unlike Pass 466, which recovers Smith multiplicities from kernel growth, this pass
records the actual successive integral Schur-complement matrices produced by
p-adic unit elimination.  The small top matrices directly predict the exponent-6
gap and the 11/7 top layers before any second-difference reconstruction.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass470_integral_conductor_coupling.json'

def heisenberg_reduced_laplacian(modulus:int)->np.ndarray:
    inv2=pow(2,-1,modulus)
    elems=[(a,b,c) for a in range(modulus) for b in range(modulus) for c in range(modulus)]
    idx={g:i for i,g in enumerate(elems)}
    section=[(a,b,0) for a in range(modulus) for b in range(modulus) if (a,b)!=(0,0)]
    n=len(elems); A=np.zeros((n,n),dtype=np.int64)
    for i,(a,b,c) in enumerate(elems):
        for x,y,z in section:
            h=((a+x)%modulus,(b+y)%modulus,(c+z+inv2*(a*y-b*x))%modulus)
            A[i,idx[h]]=1
    L=(modulus*modulus-1)*np.eye(n,dtype=np.int64)-A
    return L[:-1,:-1]

def matrix_hash(a:np.ndarray)->str:
    return hashlib.sha256(a.astype('<i8',copy=False).tobytes()).hexdigest()

def rank_mod_p(a:np.ndarray,p:int)->int:
    b=(a.copy()%p).astype(np.int64);m,n=b.shape;r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if b[i,c]%p),None)
        if piv is None:continue
        if piv!=r:b[[r,piv],:]=b[[piv,r],:]
        b[r,:]=(b[r,:]*pow(int(b[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and b[i,c]%p:b[i,:]=(b[i,:]-b[i,c]*b[r,:])%p
        r+=1
        if r==m:break
    return r

def elimination_tower(matrix:np.ndarray,p:int,max_level:int)->tuple[list[int],list[dict]]:
    modulus=p**max_level;a=matrix.astype(np.int64,copy=True)%modulus
    counts=[];records=[]
    for level in range(max_level):
        start=a.copy();size=a.shape[0];rank=0
        while rank<size:
            loc=np.argwhere((a[rank:,rank:]%p)!=0)
            if loc.size==0:break
            i=rank+int(loc[0,0]);j=rank+int(loc[0,1])
            if i!=rank:a[[rank,i],:]=a[[i,rank],:]
            if j!=rank:a[:,[rank,j]]=a[:,[j,rank]]
            inv=pow(int(a[rank,rank]),-1,modulus)
            a[rank,:]=(a[rank,:]*inv)%modulus
            factors=a[:,rank].copy();factors[rank]=0
            a=(a-factors[:,None]*a[rank:rank+1,:])%modulus
            a[rank,rank+1:]=0;rank+=1
        counts.append(rank)
        rec={
          'level':level,'current_modulus':modulus,'matrix_size':size,
          'unit_rank_mod3':rank,'matrix_rank_mod3_crosscheck':rank_mod_p(start,p),
          'matrix_sha256':matrix_hash(start),
          'entry_gcd_with_modulus':int(np.gcd.reduce(np.append(start.ravel(),modulus))),
        }
        if level>=6:
            rec['matrix_rows']=start.tolist()
        records.append(rec)
        rem=a[rank:,rank:]
        if rem.size==0:return counts,records
        if np.any(rem%p):raise AssertionError('nondivisible remainder')
        modulus//=p;a=(rem//p)%modulus
    if a.size:raise AssertionError(('unresolved',a.shape))
    return counts,records

def build_payload()->dict:
    L=heisenberg_reduced_laplacian(9)
    counts,tower=elimination_tower(L,3,10)
    top={r['level']:r for r in tower if r['level']>=6}
    m6=np.array(top[6]['matrix_rows'],dtype=np.int64)
    m7=np.array(top[7]['matrix_rows'],dtype=np.int64)
    m8=np.array(top[8]['matrix_rows'],dtype=np.int64)
    checks={
      'exact_pass448_counts':counts==[99,154,162,80,10,205,0,11,7],
      'level6_matrix_is_18_by_18':m6.shape==(18,18),
      'level6_zero_mod3':bool(np.all(m6%3==0)),
      'level6_not_zero_mod9':bool(np.any(m6%9!=0)),
      'level7_matrix_is_exact_divided_coupling':m7.shape==(18,18),
      'level7_rank11_direct':rank_mod_p(m7,3)==11,
      'level8_matrix_is_7_by_7':m8.shape==(7,7),
      'level8_rank7_direct':rank_mod_p(m8,3)==7,
      'top_layers_predicted_without_kernel_differences':[top[6]['unit_rank_mod3'],top[7]['unit_rank_mod3'],top[8]['unit_rank_mod3']]==[0,11,7],
      'tower_dimension_accounting':sum(counts)==728,
    }
    return {
      'schema':'w33.pass470.integral_conductor_coupling.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'graph':{'vertices':729,'reduced_laplacian_size':728,'characteristic_prime':3,'base_ring':'Z/9Z'},
      'exact_exponent_counts_including_units':{str(i):c for i,c in enumerate(counts)},
      'coupling_tower':tower,
      'top_conductor_theorem':(
        'After exact p-adic unit elimination, the level-6 residual is an 18x18 integral coupling '
        'matrix divisible by 3, so its mod-3 rank is zero and no exponent-6 elementary divisor '
        'terminates there.  Dividing this same matrix by 3 produces the level-7 coupling matrix '
        'of rank 11; its 7-dimensional remainder produces a full-rank level-8 matrix.  Thus the '
        'top Smith multiplicities 0,11,7 are read directly from the integral coupling matrices, '
        'not reconstructed from kernel-growth second differences.'),
      'boundary':(
        'This is a graph-specific exact integral decomposition for Z/9.  A closed symbolic formula '
        'for the entire coupling tower over Z/p^n remains open.'),
      'checks':checks,
    }

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 470 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
