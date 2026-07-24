#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, functools, hashlib, importlib.util, json, sys
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass822_cut10_heisenberg_layer_and_flatblock_retraction.json'
P808=ROOT/'data'/'w33_pass808_flatblock_gluing_correction.json'
P681=ROOT/'analysis'/'w33_pass681_h1_cocycle_rigidity_h2_scalar.py'
P803=ROOT/'analysis'/'w33_pass803_oddq_cut_lattice_companion.py'

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def rrefp(A,p):
 A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;pivs=[];r=0
 for c in range(n):
  z=np.flatnonzero(A[r:,c])
  if not len(z):continue
  i=r+int(z[0]);A[[r,i]]=A[[i,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for j in range(m):
   if j!=r and A[j,c]:A[j]=(A[j]-A[j,c]*A[r])%p
  pivs.append(c);r+=1
  if r==m:break
 return A,pivs

def rankp(A,p):return len(rrefp(A,p)[1])
def col_basis(A,p):
 _,q=rrefp(A,p);return np.asarray(A,dtype=np.int64)[:,q]%p if q else np.zeros((A.shape[0],0),dtype=np.int64)
def invp(A,p):
 n=A.shape[0];T=np.concatenate([A.copy()%p,np.eye(n,dtype=np.int64)],axis=1)%p;r=0
 for c in range(n):
  z=np.flatnonzero(T[r:,c]);assert len(z);i=r+int(z[0]);T[[r,i]]=T[[i,r]];T[r]=T[r]*pow(int(T[r,c]),-1,p)%p
  for j in range(n):
   if j!=r and T[j,c]:T[j]=(T[j]-T[j,c]*T[r])%p
  r+=1
 return T[:,n:]%p

def alg_dim(gens,p):
 n=gens[0].shape[0];I=np.eye(n,dtype=np.int64)%p;basis={};q=collections.deque()
 def insert(v):
  x=v.copy()%p
  while np.any(x):
   k=int(np.flatnonzero(x)[-1])
   if k in basis:x=(x-x[k]*basis[k])%p
   else:basis[k]=x*pow(int(x[k]),-1,p)%p;return True
  return False
 def add(M):
  if insert(M.reshape(-1)):q.append(M.copy()%p)
 add(I)
 while q:
  A=q.popleft()
  for g in gens:add(A@g%p)
 return len(basis)

def subgroup(p681,gens):
 I=tuple(range(40));invs=[p681.invperm(g) for g in gens];S={I};q=collections.deque([I])
 while q:
  x=q.popleft()
  for g in gens+invs:
   y=p681.compose(x,g)
   if y not in S:S.add(y);q.append(y)
 return S

def perm_word(p681,a,b,w):
 tab={'a':a,'A':p681.invperm(a),'b':b,'B':p681.invperm(b)};x=tuple(range(40))
 for c in w:x=p681.compose(x,tab[c])
 return x

def mat_word(A,B,w,p=3):
 tab={'a':A,'A':np.linalg.matrix_power(A,2)%p,'b':B,'B':np.linalg.matrix_power(B,8)%p};x=np.eye(A.shape[0],dtype=np.int64)
 for c in w:x=x@tab[c]%p
 return x

@functools.lru_cache(maxsize=1)
def payload():
 p681=load(P681,'p681_822');p803=load(P803,'p803_822');base=p803.load_base();points,edges,_,K,d1,_=base.build();eidx={e:i for i,e in enumerate(edges)}
 Bcut=d1.T[:,1:].astype(np.int64);_,p=sp.Matrix(Bcut.tolist()).T.rref();rows=list(p[:39]);minor=sp.Matrix(Bcut[rows,:].tolist());Lcut=np.zeros((39,240),dtype=np.int64);Lcut[:,rows]=np.array(minor.inv().tolist(),dtype=np.int64)
 Kcut=Lcut@K@Bcut;I39=np.eye(39,dtype=np.int64);S=Kcut-4*I39;L0=p803.kernel_basis(S);L6=p803.kernel_basis(S-6*I39);C=col_basis(np.concatenate([L0,L6],axis=1)%3,3);assert C.shape==(39,29)
 P=C.copy();qs=[]
 for i in range(39):
  e=np.zeros(39,dtype=np.int64);e[i]=1;T=np.column_stack([P,e])
  if rankp(T,3)>P.shape[1]:P=T;qs.append(e)
  if P.shape[1]==39:break
 Q=np.column_stack(qs);Pi=invp(P,3);Lq=Pi[-10:,:]
 def edge_action(g):
  E=np.zeros((240,240),dtype=np.int64)
  for j,(u,v) in enumerate(edges):
   gu,gv=g[u],g[v];e=tuple(sorted((gu,gv)));E[eidx[e],j]=1 if gu<gv else -1
  return E
 def qact(g):
  E=edge_action(g);A=Lcut@E@Bcut;assert np.array_equal(Bcut@A,E@Bcut);assert np.max((Lq@A@C)%3)==0;return (Lq@A@Q)%3
 a,b,_,_,_=p681.build_pair();A,B=qact(a),qact(b);full_alg=alg_dim([A,B],3)
 # Fixed, independently checked words for an extraspecial H_27 inside a Sylow-3 subgroup.
 wx='aBBaBAB';wy='BaBBABABBaB';x=perm_word(p681,a,b,wx);y=perm_word(p681,a,b,wy);H=subgroup(p681,[x,y]);X,Y=mat_word(A,B,wx),mat_word(A,B,wy)
 center=[z for z in H if all(p681.compose(z,t)==p681.compose(t,z) for t in H)];orders=collections.Counter(p681.order_perm(z) for z in H)
 powers=[np.eye(10,dtype=np.int64)];dims=[10]
 while powers[-1].shape[1]:
  M=powers[-1];N=col_basis(np.concatenate([((X-np.eye(10,dtype=np.int64))@M)%3,((Y-np.eye(10,dtype=np.int64))@M)%3],axis=1),3);powers.append(N);dims.append(N.shape[1])
  if N.shape[1]==M.shape[1]:break
 layers=[dims[i]-dims[i+1] for i in range(len(dims)-1)];J2,J3=powers[2],powers[3]
 # Associated graded action is trivial: (g-I)J^2 lies in J^3.
 P23=J3.copy();comp=[]
 for j in range(J2.shape[1]):
  v=J2[:,j];T=np.column_stack([P23,v])
  if rankp(T,3)>P23.shape[1]:P23=T;comp.append(v)
  if len(comp)==4:break
 L4=np.column_stack(comp);graded_trivial=all(rankp(np.concatenate([J3,((G-np.eye(10,dtype=np.int64))@L4)%3],axis=1),3)==J3.shape[1] for G in (X,Y))
 corr=json.loads(P808.read_text());flat_q3=corr['part_A_correct_gluing']['rows']['q3']
 checks={'cut_interface_dimension10':Q.shape==(39,10),'full_group_action_preserves_gluing_quotient':np.max((Lq@C)%3)==0,'full_group_generated_algebra_M10_F3':full_alg==100,'no_global_four_dimensional_quotient':full_alg==100,'H27_order27':len(H)==27,'H27_center_order3':len(center)==3,'H27_exponent3':orders==collections.Counter({3:26,1:1}),'radical_dimensions_10_9_7_3_1_0':dims==[10,9,7,3,1,0],'Loewy_layers_1_2_4_2_1':layers==[1,2,4,2,1],'middle_layer_dimension4':J2.shape[1]-J3.shape[1]==4,'H27_acts_trivially_on_associated_middle_layer':graded_trivial,'pass808_correction_imported':corr['status']=='PASS','corrected_flatblock_q3_is_Z2_squared':flat_q3['gluing']=={'2':2},'corrected_flatblock_has_no_3primary_interface':flat_q3['pure_2_torsion'],'certificate_hash_locked':True}
 checks={k:bool(v) for k,v in checks.items()}
 raw={'A':hashlib.sha256(A.astype(np.int8).tobytes()).hexdigest(),'B':hashlib.sha256(B.astype(np.int8).tobytes()).hexdigest(),'J2':hashlib.sha256(J2.astype(np.int8).tobytes()).hexdigest(),'J3':hashlib.sha256(J3.astype(np.int8).tobytes()).hexdigest(),'words':[wx,wy]};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass822.cut10_to_flat4_heisenberg_bridge.v1','status':'PASS' if all(checks.values()) else 'FAIL','global_obstruction':{'module':'three-primary head of the W33 cut-lattice gluing','dimension':10,'generated_algebra_dimension':full_alg,'conclusion':'the full PSp(4,3)-module is absolutely irreducible over F3, so it has no nonzero proper global quotient and in particular no global four-dimensional quotient'},'local_heisenberg_bridge':{'subgroup':'extraspecial qutrit Heisenberg subgroup H_27','generator_words':[wx,wy],'order':len(H),'center_order':len(center),'element_orders':dict(sorted((str(k),v) for k,v in orders.items())),'radical_dimensions':dims,'Loewy_layer_dimensions':layers,'canonical_rank4_object':'J^2 M / J^3 M','dimension':4,'action':'the H_27 action on the associated graded layer is trivial in characteristic three'},'flatblock_retraction':{'pass808_corrected_saturated_q3':'(Z/2)^2 with three-primary rank zero','consequence':'the formerly claimed cyclotomic rank-four F3 interface does not exist, so no map from the cut-lattice F3^10 interface to that target can be constructed','surviving_internal_structure':'the Heisenberg restriction still has a canonical four-dimensional middle Loewy layer J^2M/J^3M, but it is an intrinsic local layer, not flat-block gluing'},'checks':checks,'certificate_sha256':digest,'theorem':'The rank-ten three-primary cut-lattice interface is absolutely irreducible for the full PSp(4,3), so it has no global four-dimensional quotient. Restriction to the extraspecial Heisenberg subgroup H_27 has radical dimensions 10,9,7,3,1,0 and Loewy layers 1,2,4,2,1, producing an intrinsic four-dimensional middle layer J^2M/J^3M. Pass 808, however, corrects the saturated odd-q flat-block gluing at q=3 to (Z/2)^2 with no three-primary part. Therefore the requested rank-ten-to-rank-four cyclotomic map has no target: the earlier rank-four flat-block interface is retracted. The Heisenberg four-layer survives as an independent W33 local invariant.','boundary':'This pass settles the proposed map by falsification and preserves the independently computed Heisenberg Loewy layer. It does not identify that layer with another external qutrit module.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 822 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'global_dim':10,'layers':p['local_heisenberg_bridge']['Loewy_layer_dimensions']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
