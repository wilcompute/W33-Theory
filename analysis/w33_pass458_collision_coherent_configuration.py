#!/usr/bin/env python3
"""Pass 458: coherent-configuration and Terwilliger anatomy of the genuine q=5 collision."""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass458_collision_coherent_configuration.json'
Q=5
OFFSETS=[
 (0,3,4,1,1,0,2,0,1,1,2,2),
 (0,2,3,0,2,2,4,1,0,3,3,2),
]

def graphs():
 q=Q
 elems=[(a,b,c) for a in range(q) for b in range(q) for c in range(q)]
 idx={g:i for i,g in enumerate(elems)}
 vecs=[(a,b) for a in range(q) for b in range(q) if (a,b)!=(0,0)]
 pairs=[];used=set()
 for v in vecs:
  nv=(-v[0]%q,-v[1]%q);key=tuple(sorted((v,nv)))
  if key not in used: used.add(key);pairs.append(key)
 def mul(g,h):
  return ((g[0]+h[0])%q,(g[1]+h[1])%q,(g[2]+h[2]-g[0]*h[1]+h[0]*g[1])%q)
 out=[]
 for offs in OFFSETS:
  S=[]
  for (v,nv),c in zip(pairs,offs): S.extend([(v[0],v[1],c),(nv[0],nv[1],-c%q)])
  A=np.zeros((125,125),dtype=np.int16)
  for i,g in enumerate(elems):
   for s in S:A[i,idx[mul(g,s)]]=1
  out.append(A)
 return out

def rooted_refinement(A):
 n=len(A);colors=np.where(np.arange(n)==0,0,np.where(A[0]>0,1,2)).astype(np.int32)
 history=[]
 while True:
  r=int(colors.max())+1
  sig=np.empty((n,r+1),dtype=np.int32);sig[:,0]=colors
  for c in range(r):sig[:,c+1]=A[:,colors==c].sum(axis=1)
  _,inv=np.unique(sig,axis=0,return_inverse=True)
  history.append(sorted(Counter(inv.tolist()).values()))
  if np.array_equal(inv,colors):break
  colors=inv.astype(np.int32)
 return {'iterations':len(history),'rank':int(colors.max())+1,'cell_sizes':sorted(Counter(colors.tolist()).values()),'history':history}

def two_wl(A,max_iter=8):
    n=len(A)
    C=np.where(np.eye(n,dtype=bool),0,np.where(A>0,1,2)).astype(np.int32)
    ranks=[3]
    first_sizes=None
    for _ in range(max_iter):
        r=int(C.max())+1
        codes=(C[:,:,None].astype(np.int64)*r+C[None,:,:].astype(np.int64)).transpose(0,2,1).reshape(n*n,n)
        codes.sort(axis=1)
        sig=np.concatenate([C.reshape(-1,1).astype(np.int64),codes],axis=1)
        _,inv=np.unique(sig,axis=0,return_inverse=True)
        N=inv.reshape(n,n).astype(np.int32)
        ranks.append(int(N.max())+1)
        if first_sizes is None:
            first_sizes=sorted(Counter(inv.tolist()).values())
        if np.array_equal(N,C):
            C=N
            break
        C=N
    sizes=Counter(C.reshape(-1).tolist())
    return {
      'iterations':len(ranks)-1,'rank':int(C.max())+1,'rank_history':ranks,
      'first_refinement_relation_sizes':first_sizes,
      'stable_relation_size_multiset':sorted(sizes.values()),
      'thin_regular_scheme':set(sizes.values())=={n} and len(sizes)==n,
    }

def terwilliger_word_data(A,p=101,max_length=9):
    n=len(A)
    E0=np.diag((np.arange(n)==0).astype(np.int64))
    E1=np.diag((A[0]>0).astype(np.int64))
    E2=np.eye(n,dtype=np.int64)-E0-E1
    gens=[A.astype(np.int64)%p,E0%p,E1%p,E2%p]
    basis=[];pivots=[];front=[np.eye(n,dtype=np.int64)%p]
    mod_basis_insert(front[0].reshape(-1),basis,pivots,p)
    dims=[1]
    for _ in range(max_length):
        new=[]
        for X in front:
            for G in gens:
                Y=(X@G)%p
                if mod_basis_insert(Y.reshape(-1),basis,pivots,p):new.append(Y)
        front=new;dims.append(len(basis))
    word=A.astype(np.int64)@A.astype(np.int64)@E1@A.astype(np.int64)@E1
    return {'word_space_dimensions_through_length_9':dims,'trace_AA1A1':int(np.trace(word)),'prime':p}

def mod_basis_insert(v,basis,pivots,p=101):
 v=np.asarray(v,dtype=np.int64).copy()%p
 for pivot,row in zip(pivots,basis):
  if v[pivot]:v=(v-v[pivot]*row)%p
 nz=np.flatnonzero(v)
 if not len(nz):return False
 pivot=int(nz[0]);v=(v*pow(int(v[pivot]),-1,p))%p
 for k,row in enumerate(basis):
  if row[pivot]:basis[k]=(row-row[pivot]*v)%p
 pos=np.searchsorted(pivots,pivot);pivots.insert(pos,pivot);basis.insert(pos,v)
 return True

def terwilliger_dimension(A,p=101,cap=250):
 n=len(A);d=A[0]@A
 E0=np.diag((np.arange(n)==0).astype(np.int64))
 E1=np.diag((A[0]>0).astype(np.int64))
 E2=np.eye(n,dtype=np.int64)-E0-E1
 gens=[np.eye(n,dtype=np.int64),A.astype(np.int64),E0,E1,E2]
 mats=[];basis=[];pivots=[];queue=[]
 for G in gens:
  if mod_basis_insert(G.reshape(-1),basis,pivots,p):mats.append(G%p);queue.append(len(mats)-1)
 fixed_gens=[A.astype(np.int64)%p,E0%p,E1%p,E2%p]
 qi=0
 while qi<len(queue):
  X=mats[queue[qi]];qi+=1
  for G in fixed_gens:
   for Y in ((X@G)%p,(G@X)%p):
    if mod_basis_insert(Y.reshape(-1),basis,pivots,p):
     mats.append(Y);queue.append(len(mats)-1)
     if len(mats)>=cap:return {'dimension_lower_bound':len(mats),'capped':True,'prime':p}
 return {'dimension':len(mats),'capped':False,'prime':p}

def build_payload():
    As=graphs()
    root=[rooted_refinement(A) for A in As]
    wl2=[two_wl(A) for A in As]
    ter=[terwilliger_word_data(A) for A in As]
    checks={
      'rooted_first_refinement_distinguishes':root[0]['history'][0]!=root[1]['history'][0],
      'two_wl_first_rank_19_vs_18':[x['rank_history'][1] for x in wl2]==[19,18],
      'two_wl_stabilizes_at_thin_rank_125':all(x['rank']==125 and x['thin_regular_scheme'] for x in wl2),
      'terwilliger_word_trace_distinguishes':[x['trace_AA1A1'] for x in ter]==[622,650],
      'terwilliger_dimension_growth_agrees_through_9':ter[0]['word_space_dimensions_through_length_9']==ter[1]['word_space_dimensions_through_length_9'],
    }
    return {
      'schema':'w33.pass458.collision_coherent_configuration.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'rooted_equitable_refinements':root,'two_wl_coherent_closures':wl2,'terwilliger_word_algebras':ter,
      'headline':'The Smith-identical q=5 collision separates at the first 2-WL coherent refinement (rank 19 versus 18) and by the rooted Terwilliger trace tr(A^2 E1 A E1)=622 versus 650; both closures ultimately become the same-size thin rank-125 regular scheme.',
      'interpretation':'The full coherent closure remembers the underlying regular Heisenberg action, while the marked adjacency union sits differently inside it. The first missing invariant is therefore a rooted local incidence character, not another global spectrum or Smith invariant.',
      'boundary':'The complete 125-color intersection tensor is canonically the thin regular group scheme and was not serialized; the certificate records the exact WL rank history, relation sizes, and a separating Terwilliger trace word.',
      'checks':checks,
    }
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 458 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'terwilliger_traces':[x['trace_AA1A1'] for x in p['terwilliger_word_algebras']],'wl2_histories':[x['rank_history'] for x in p['two_wl_coherent_closures']]}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
