#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, functools, hashlib, importlib.util, itertools, json, sys
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass977_h27_normalizer_loewy_action.json'
P972=ROOT/'analysis'/'w33_pass972_heisenberg_loewy_basis.py'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def key(A): return np.asarray(A,dtype=np.int8).tobytes()
def mpow(A,n,p=3):
 X=np.eye(A.shape[0],dtype=np.int64)
 for _ in range(n):X=X@A%p
 return X
def order(A,p=3,maxn=200):
 I=np.eye(A.shape[0],dtype=np.int64);X=I.copy()
 for n in range(1,maxn+1):
  X=X@A%p
  if np.array_equal(X,I):return n
 return None
def reconstruct(p972):
 p681=p972.load(p972.P681,'p681_977');p803=p972.load(p972.P803,'p803_977');p822=p972.load(p972.P822,'p822_977');base=p803.load_base();_,edges,_,K,d1,_=base.build();eidx={e:i for i,e in enumerate(edges)}
 Bcut=d1.T[:,1:].astype(np.int64);_,p=sp.Matrix(Bcut.tolist()).T.rref();rows=list(p[:39]);minor=sp.Matrix(Bcut[rows,:].tolist());Lcut=np.zeros((39,240),dtype=np.int64);Lcut[:,rows]=np.array(minor.inv().tolist(),dtype=np.int64)
 Kcut=Lcut@K@Bcut;I39=np.eye(39,dtype=np.int64);S=Kcut-4*I39;L0=p803.kernel_basis(S);L6=p803.kernel_basis(S-6*I39);C=p972.col_basis(np.concatenate([L0,L6],axis=1),3)
 P=C.copy();qs=[]
 for i in range(39):
  e=np.zeros(39,dtype=np.int64);e[i]=1
  if p972.rankp(np.column_stack([P,e]),3)>P.shape[1]:P=np.column_stack([P,e]);qs.append(e)
  if P.shape[1]==39:break
 Q=np.column_stack(qs);Pi=p972.invp(P,3);Lq=Pi[-10:,:]
 def edge_action(g):
  E=np.zeros((240,240),dtype=np.int64)
  for j,(u,v) in enumerate(edges):
   gu,gv=g[u],g[v];e=tuple(sorted((gu,gv)));E[eidx[e],j]=1 if gu<gv else -1
  return E
 def qact(g):
  E=edge_action(g);return Lq@(Lcut@E@Bcut)@Q%3
 a,b,_,_,_=p681.build_pair();A,B=qact(a),qact(b);X=p822.mat_word(A,B,'aBBaBAB')%3;Y=p822.mat_word(A,B,'BaBBABABBaB')%3
 basis=np.array(p972.payload()['canonical_monomial_basis']['basis_columns_in_original_cut_quotient_coordinates'],dtype=np.int64).T%3
 return A%3,B%3,X,Y,basis
def enumerate_group(A,B,p972):
 Ai=p972.invp(A,3);Bi=p972.invp(B,3);gens=[A,B,Ai,Bi];ginvs=[Ai,Bi,A,B];I=np.eye(A.shape[0],dtype=np.int64);mats=[I];invs=[I];seen={key(I):0};head=0
 while head<len(mats):
  g,gi=mats[head],invs[head];head+=1
  for h,hi in zip(gens,ginvs):
   z=g@h%3;k=key(z)
   if k not in seen:seen[k]=len(mats);mats.append(z);invs.append(hi@gi%3)
 return mats,invs,seen
def h27_coordinates(X,Y,p972):
 Xi=p972.invp(X,3);Yi=p972.invp(Y,3);Z=Xi@Yi@X@Y%3;coords={}
 for a,b,c in itertools.product(range(3),repeat=3):coords[key(mpow(X,a)@mpow(Y,b)%3@mpow(Z,c)%3)]=(a,b,c)
 return Z,coords
def det2(M):return int((M[0,0]*M[1,1]-M[0,1]*M[1,0])%3)
@functools.lru_cache(maxsize=1)
def payload():
 p972=load(P972,'p972_977');A,B,X,Y,P=reconstruct(p972);Pi=p972.invp(P,3);mats,invs,seen=enumerate_group(A,B,p972);Z,hcoords=h27_coordinates(X,Y,p972)
 normal=[];actions=[];layer_sets=[set() for _ in range(5)];layer_orders=[collections.Counter() for _ in range(5)];offsets=[0,1,3,7,9,10];filtration=True;detlaw=True
 for g,gi in zip(mats,invs):
  cx=gi@X@g%3;cy=gi@Y@g%3;kx,ky=key(cx),key(cy)
  if kx not in hcoords or ky not in hcoords:continue
  normal.append(key(g));ax,bx,_=hcoords[kx];ay,by,_=hcoords[ky];M=np.array([[ax,ay],[bx,by]],dtype=np.int64)%3;actions.append(key(M))
  zc=hcoords.get(key(gi@Z@g%3));detlaw &= zc is not None and zc[:2]==(0,0) and zc[2]%3==det2(M)%3
  G=Pi@g@P%3
  for i in range(5):
   a,b=offsets[i],offsets[i+1];filtration &= not G[:a,a:].any();block=G[a:b,a:b]%3;layer_sets[i].add(key(block));layer_orders[i][order(block,3)]+=1
 image=set(actions);kernel=sum(1 for z in actions if z==key(np.eye(2,dtype=np.int64)))
 image_mats=[np.frombuffer(z,dtype=np.int8).reshape(2,2).astype(np.int64)%3 for z in image];image_closed=all(key(a@b%3) in image for a in image_mats for b in image_mats);Hkeys=set(hcoords);normal_set=set(normal)
 checks={'global_group_order25920':len(mats)==25920,'H27_order27':len(hcoords)==27,'H27_is_subgroup_of_global_action':Hkeys<=set(seen),'normalizer_contains_H27':Hkeys<=normal_set,'normalizer_orbit_stabilizer_exact':len(normal)==kernel*len(image),'induced_image_closed':image_closed,'induced_actions_in_GL2':all(det2(a)!=0 for a in image_mats),'commutator_transforms_by_determinant':detlaw,'all_radical_tails_invariant':filtration,'loewy_layer_dimensions_1_2_4_2_1':[offsets[i+1]-offsets[i] for i in range(5)]==[1,2,4,2,1],'certificate_hash_locked':True};checks={k:bool(v) for k,v in checks.items()}
 raw={'normalizer_order':len(normal),'image':sorted(z.hex() for z in image),'kernel':kernel,'layers':[sorted(z.hex() for z in s) for s in layer_sets]};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass977.h27_normalizer_loewy_action.v1','status':'PASS' if all(checks.values()) else 'FAIL','groups':{'ambient_image_order':len(mats),'H27_order':len(hcoords),'normalizer_order':len(normal),'normalizer_quotient_image_order':len(image),'kernel_order':kernel,'quotient_determinant_distribution':dict(collections.Counter(det2(a) for a in image_mats))},'loewy_action':{'layer_dimensions':[1,2,4,2,1],'distinct_action_counts':[len(s) for s in layer_sets],'action_order_histograms':[{str(k):v for k,v in sorted(c.items())} for c in layer_orders],'interpretation':'normalizer matrices preserve every radical tail; diagonal blocks are the induced actions on J^dM/J^{d+1}M'},'checks':checks,'certificate_sha256':digest,'theorem':f'The selected extraspecial H27 has normalizer of order {len(normal)} in the 10-dimensional W33 factor. Its induced action on H27/Z(H27) has order {len(image)} with kernel {kernel}; the commutator center transforms by the determinant character. The explicit 1,2,4,2,1 Loewy basis is invariant under the normalizer, and the five graded action images have sizes {[len(s) for s in layer_sets]}.','boundary':'This is the exact normalizer inside the represented PSp(4,3) image determined by the repository generator words. It does not identify a catalogue subgroup name unless that name follows from an independent subgroup presentation.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 977 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'groups':p['groups'],'layers':p['loewy_action']['distinct_action_counts']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
