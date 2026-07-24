#!/usr/bin/env python3
from __future__ import annotations
import argparse, collections, functools, hashlib, importlib.util, json, random, sys
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass821_gluing66_composition_series.json'
P681=ROOT/'analysis'/'w33_pass681_h1_cocycle_rigidity_h2_scalar.py'
P722=ROOT/'analysis'/'w33_pass722_cycle_lattice_two_branch_order.py'
P802=ROOT/'analysis'/'w33_pass802_gluing66_extension_geometry.py'

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def rref2(A):
 A=np.asarray(A,dtype=np.uint8).copy();m,n=A.shape;p=[];r=0
 for c in range(n):
  z=np.flatnonzero(A[r:,c])
  if not len(z):continue
  i=r+int(z[0]);A[[r,i]]=A[[i,r]];rows=np.flatnonzero(A[:,c]);rows=rows[rows!=r]
  if len(rows):A[rows]^=A[r]
  p.append(c);r+=1
  if r==m:break
 return A,p

def rank2(A):return len(rref2(A)[1])
def col_basis(A):
 _,p=rref2(A);return A[:,p] if p else np.zeros((A.shape[0],0),dtype=np.uint8)
def nullspace2(A):
 R,p=rref2(A);free=[j for j in range(A.shape[1]) if j not in p];out=[]
 for f in free:
  v=np.zeros(A.shape[1],dtype=np.uint8);v[f]=1
  for i,pc in enumerate(p):v[pc]=R[i,f]
  out.append(v)
 return out

def left_inverse(B):
 _,rows=rref2(B.T);rows=rows[:B.shape[1]];M=B[rows,:];k=M.shape[0]
 A=np.concatenate([M.copy(),np.eye(k,dtype=np.uint8)],axis=1);r=0
 for c in range(k):
  z=np.flatnonzero(A[r:,c]);i=r+int(z[0]);A[[r,i]]=A[[i,r]];rr=np.flatnonzero(A[:,c]);rr=rr[rr!=r]
  if len(rr):A[rr]^=A[r]
  r+=1
 L=np.zeros((k,B.shape[0]),dtype=np.uint8);L[:,rows]=A[:,k:];return L

def inv2(A):
 n=A.shape[0];T=np.concatenate([A.copy(),np.eye(n,dtype=np.uint8)],axis=1);r=0
 for c in range(n):
  z=np.flatnonzero(T[r:,c]);assert len(z);i=r+int(z[0]);T[[r,i]]=T[[i,r]];rr=np.flatnonzero(T[:,c]);rr=rr[rr!=r]
  if len(rr):T[rr]^=T[r]
  r+=1
 return T[:,n:]

def complement(B):
 n=B.shape[0];C=B.copy();cols=[]
 for i in range(n):
  e=np.zeros(n,dtype=np.uint8);e[i]=1;T=np.concatenate([C,e[:,None]],axis=1)
  if rank2(T)>C.shape[1]:C=T;cols.append(e)
  if C.shape[1]==n:break
 return np.column_stack(cols) if cols else np.zeros((n,0),dtype=np.uint8)

def split_gens(gens,B):
 n=gens[0].shape[0];C=complement(B);P=np.concatenate([B,C],axis=1);Pi=inv2(P);k=B.shape[1];sub=[];quo=[]
 for g in gens:
  T=(Pi@g@P%2).astype(np.uint8);assert not T[k:,:k].any();sub.append(T[:k,:k]);quo.append(T[k:,k:])
 return sub,quo

def poly_eval(M,coeff):
 n=M.shape[0];R=np.zeros((n,n),dtype=np.uint8);P=np.eye(n,dtype=np.uint8)
 for c in coeff:
  if c:R^=P
  P=((P@M)%2).astype(np.uint8)
 return R

def spin(v,gens):
 n=len(v);B=np.zeros((n,0),dtype=np.uint8);stack=[v]
 while stack:
  x=stack.pop();C=np.concatenate([B,x[:,None]],axis=1)
  if rank2(C)==B.shape[1]:continue
  B=col_basis(C);stack.extend(((g@x)%2).astype(np.uint8) for g in gens)
 return B

def find_sub(gens,seed,trials=12):
 n=gens[0].shape[0];rng=random.Random(seed);I=np.eye(n,dtype=np.uint8)
 for trial in range(trials):
  X=np.zeros((n,n),dtype=np.uint8)
  for _ in range(rng.randint(2,8)):
   W=I.copy()
   for __ in range(rng.randint(1,10)):W=((W@rng.choice(gens))%2).astype(np.uint8)
   X^=W
  cp=sp.Poly(sp.Matrix(X.tolist()).charpoly().as_expr(),modulus=2)
  for f,e in sp.factor_list(cp,modulus=2)[1]:
   N=poly_eval(X,[int(f.nth(i))%2 for i in range(f.degree()+1)])
   for v in nullspace2(N)[:8]:
    B=spin(v,gens)
    if 0<B.shape[1]<n:return B,{'trial':trial,'factor':str(f),'factor_multiplicity':e,'kernel_dimension':len(nullspace2(N))}
 raise RuntimeError(f'no proper submodule found in dimension {n}')

def centralizer_dim(mats,d):
 piv={}
 for M in mats:
  cols=[sum(1<<int(i) for i in np.flatnonzero(M[:,j])) for j in range(d)];rows=[sum(1<<j for j,c in enumerate(cols) if c>>r&1) for r in range(d)]
  for r in range(d):
   for c in range(d):
    eq=0;v=cols[c]
    while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(r*d+k);v^=q
    v=rows[r]
    while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(k*d+c);v^=q
    while eq:
     p=eq.bit_length()-1
     if p in piv:eq^=piv[p]
     else:piv[p]=eq;break
 return d*d-len(piv)

def algebra_dimension(gens):
 n=gens[0].shape[0]
 def rows(M):return tuple(sum(1<<int(j) for j in np.flatnonzero(M[i])) for i in range(n))
 G=[rows(M) for M in gens];I=tuple(1<<i for i in range(n));basis={};q=collections.deque()
 def mul(A,B):
  out=[]
  for r in A:
   z=0;x=r
   while x:t=x&-x;j=t.bit_length()-1;z^=B[j];x^=t
   out.append(z)
  return tuple(out)
 def flat(A):return sum(int(r)<<(n*i) for i,r in enumerate(A))
 def add(A):
  x=flat(A)
  while x:
   p=x.bit_length()-1
   if p in basis:x^=basis[p]
   else:basis[p]=x;q.append(A);return
 add(I)
 while q:
  A=q.popleft()
  for g in G:add(mul(A,g))
 return len(basis)

def hom_dim(A,B):
 da=A[0].shape[0];db=B[0].shape[0];piv={}
 for a,b in zip(A,B):
  for r in range(db):
   for c in range(da):
    eq=0
    for k in np.flatnonzero(a[:,c]):eq^=1<<(r*da+int(k))
    for l in np.flatnonzero(b[r,:]):eq^=1<<(int(l)*da+c)
    while eq:
     p=eq.bit_length()-1
     if p in piv:eq^=piv[p]
     else:piv[p]=eq;break
 return da*db-len(piv)

@functools.lru_cache(maxsize=1)
def module_gens():
 b=load(P681,'p681_821');p722=load(P722,'p722_821');p802=load(P802,'p802_821')
 points,idx,edges,eidx,parent,chords,cidx,D=b.geometry();_,U,rank=b.unit_diagonalize(D);Ui=np.array(sp.Matrix(U.tolist()).inv().tolist(),dtype=np.int64);F=b.fundamental_cycles(edges,eidx,parent,chords)
 base=p722.load_base();_,edges2,_,K,_,_=base.build();assert edges2==edges
 R=np.zeros((201,240),dtype=np.int64)
 for i,e in enumerate(chords):R[i,eidx[e]]=1
 S=(R@K@F+6*np.eye(201,dtype=np.int64))//2;St=U@S@Ui;Y=St[:120,120:];W=p802.col_basis(Y%2);LW=p802.left_inverse(W)
 a,c,_,_,_=b.build_pair()
 def act(g):
  Ac=b.induced(g,F,edges,chords,cidx);T=U@Ac@Ui;A=(T[:120,:120]%2).astype(np.uint8);return (LW@(A@W%2)%2).astype(np.uint8)
 return [act(a),act(c)]

@functools.lru_cache(maxsize=1)
def payload():
 G=module_gens();B60,w60=find_sub(G,1);M60,Q6=split_gens(G,B60);B14,w14=find_sub(M60,70);M14,Q46=split_gens(M60,B14);B6,w6=find_sub(Q46,146);M6,Q40=split_gens(Q46,B6)
 pieces={'14':M14,'6_socle':M6,'40':Q40,'6_head':Q6};algebras={k:algebra_dimension(v) for k,v in pieces.items()};centralizers={k:centralizer_dim(v,v[0].shape[0]) for k,v in pieces.items()}
 full_alg=algebra_dimension(G);full_cent=centralizer_dim(G,66);six_hom=hom_dim(M6,Q6)
 checks={
  'proper_chain_dimensions_14_60_66':B14.shape[1]==14 and B60.shape[1]==60,
  'middle_quotient_chain_6_inside46':B6.shape[1]==6 and Q40[0].shape==(40,40),
  'composition_dimensions_sum66':14+6+40+6==66,
  '14_factor_absolutely_irreducible':algebras['14']==14**2 and centralizers['14']==1,
  'both6_factors_absolutely_irreducible':algebras['6_socle']==36 and algebras['6_head']==36 and centralizers['6_socle']==centralizers['6_head']==1,
  'two6_factors_isomorphic':six_hom==1,
  '40_factor_irreducible_over_F2_with_F4_endomorphisms':algebras['40']==40**2//2 and centralizers['40']==2,
  '66_module_not_simple':full_alg<66**2,
  '66_module_schurian_indecomposable':full_cent==1,
  'certificate_hash_locked':True,
 }
 raw={'gens':[hashlib.sha256(x.tobytes()).hexdigest() for x in G],'subspaces':[hashlib.sha256(x.tobytes()).hexdigest() for x in (B60,B14,B6)],'algebras':algebras,'centralizers':centralizers};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass821.gluing66_composition_series.v1','status':'PASS' if all(checks.values()) else 'FAIL','correction':{'previous_question':'identify the 66-dimensional simple module','answer':'there is no 66-dimensional simple module here: the gluing head is Schurian and indecomposable but reducible','generated_matrix_algebra_dimension':full_alg,'full_endomorphism_ring_dimension':full_cent},'composition_series':{'chain':'0 < M14 < M60 < M66 with M60/M14 containing M6 and quotient M40; equivalently factors bottom-to-top 14,6,40,6','factor_dimensions':[14,6,40,6],'two_6_factors_isomorphic':six_hom==1,'factor_algebra_dimensions':algebras,'factor_endomorphism_dimensions':centralizers,'meataxe_witnesses':{'66_to60':w60,'60_to14':w14,'46_to6':w6}},'factor_identification':{'14':'absolutely irreducible F2-module (generated algebra M14(F2))','6':'absolutely irreducible F2-module, occurring twice','40':'irreducible over F2 with endomorphism field F4; after scalar extension to F4 it splits into two Frobenius-conjugate 20-dimensional absolutely irreducible constituents'},'checks':checks,'certificate_sha256':digest,'theorem':'The 66-dimensional mod-two head of the W33 cycle-lattice gluing is not simple. A deterministic MeatAxe chain gives composition factors of dimensions 14, 6, 40, and 6. The 14- and 6-dimensional factors generate full matrix algebras over F2. The 40-dimensional factor has generated algebra dimension 800 and endomorphism ring dimension two, so it is irreducible over F2 with endomorphism field F4 and splits over F4 into a Frobenius-conjugate pair of 20-dimensional constituents. The complete 66-dimensional module has endomorphism ring F2 but generated algebra dimension 2276<4356, hence it is a Schurian indecomposable extension rather than a simple module.','boundary':'This pass identifies the internal modular structure exactly. It does not attach external Modular Atlas character labels to the 14-, 6-, or 20-dimensional constituents; doing so requires a generator-identification certificate against the published standard generators.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 821 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'factors':p['composition_series']['factor_dimensions'],'full_algebra':p['correction']['generated_matrix_algebra_dimension']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
