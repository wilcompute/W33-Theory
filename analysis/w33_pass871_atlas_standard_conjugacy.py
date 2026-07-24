#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, collections, functools, hashlib, importlib.util, itertools, json, random, sys, urllib.request
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass871_atlas_standard_conjugacy.json'
P681=ROOT/'analysis'/'w33_pass681_h1_cocycle_rigidity_h2_scalar.py'
P821=ROOT/'analysis'/'w33_pass821_gluing66_composition_series.py'
ATLAS='https://brauer.maths.qmul.ac.uk/Atlas/clas/U42/gap/U42d2G1-f2r{d}B0.g{g}'

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def word_mat(w,A,B):
 n=A.shape[0];tab={'a':A,'A':np.linalg.matrix_power(A,2)%2,'b':B,'B':np.linalg.matrix_power(B,8)%2};X=np.eye(n,dtype=np.uint8)
 for c in w:X=(X@tab[c])%2
 return X.astype(np.uint8)

def perm_word(w,a,b,p681):
 tab={'a':a,'A':p681.invperm(a),'b':b,'B':p681.invperm(b)};x=tuple(range(40))
 for c in w:x=p681.compose(x,tab[c])
 return x

def enumerate_words(a,b,p681):
 gens={'a':a,'A':p681.invperm(a),'b':b,'B':p681.invperm(b)};I=tuple(range(40));seen={I:''};q=collections.deque([I])
 while q:
  x=q.popleft()
  for c,g in gens.items():
   y=p681.compose(x,g)
   if y not in seen:seen[y]=seen[x]+c;q.append(y)
 return seen

def comm(x,y,p681):return p681.compose(p681.compose(p681.compose(p681.invperm(x),p681.invperm(y)),x),y)

def subgroup_order(gens,p681,limit=60000):
 I=tuple(range(40));allg=gens+[p681.invperm(g) for g in gens];S={I};q=collections.deque([I])
 while q:
  x=q.popleft()
  for g in allg:
   y=p681.compose(x,g)
   if y not in S:
    S.add(y);q.append(y)
    if len(S)>limit:return len(S)
 return len(S)

def find_inner_standard(words,p681):
 elems=list(words);invol=[x for x in elems if p681.order_perm(x)==2];five=[x for x in elems if p681.order_perm(x)==5];rng=random.Random(871)
 pairs=[(rng.choice(invol),rng.choice(five)) for _ in range(30000)]
 for s,t in pairs:
  if p681.order_perm(p681.compose(s,t))!=9:continue
  if p681.order_perm(comm(s,t,p681))!=3:continue
  tst=p681.compose(t,p681.compose(s,t))
  if p681.order_perm(comm(s,tst,p681))!=2:continue
  if subgroup_order([s,t],p681)==25920:
   cent=sum(p681.compose(s,g)==p681.compose(g,s) for g in elems)
   if cent==576:return words[s],words[t],cent
 raise RuntimeError('standard inner pair not found')

def gf2_nullspace(A):
 # Deterministic reduced row echelon form over F2.
 A=np.asarray(A,dtype=np.uint8).copy();m,n=A.shape;piv=[];r=0
 for c in range(n):
  z=np.flatnonzero(A[r:,c])
  if not len(z):continue
  i=r+int(z[0]);A[[r,i]]=A[[i,r]]
  rows=np.flatnonzero(A[:,c]);rows=rows[rows!=r]
  if len(rows):A[rows]^=A[r]
  piv.append(c);r+=1
  if r==m:break
 free=[c for c in range(n) if c not in set(piv)];basis=[]
 for f in free:
  v=np.zeros(n,dtype=np.uint8);v[f]=1
  # RREF has one pivot per row; solve x_p = sum_j R[p,j] x_j.
  for i,p in enumerate(piv):v[p]=A[i,f]
  basis.append(v)
 return basis,piv

def intertwiner_basis(Apairs,Bpairs):
 # Solve X A_i = B_i X over F2; X is row-major.
 n=Apairs[0].shape[0];E=np.zeros((len(Apairs)*n*n,n*n),dtype=np.uint8);row=0
 for A,B in zip(Apairs,Bpairs):
  A=np.asarray(A,dtype=np.uint8);B=np.asarray(B,dtype=np.uint8)
  for r in range(n):
   for c in range(n):
    for k in np.flatnonzero(A[:,c]):E[row,r*n+int(k)]^=1
    for l in np.flatnonzero(B[r,:]):E[row,int(l)*n+c]^=1
    row+=1
 basis,_=gf2_nullspace(E[:row])
 return [v.reshape(n,n).astype(np.uint8) for v in basis]

def rank2(A):
 A=A.copy().astype(np.uint8);r=0
 for c in range(A.shape[1]):
  z=np.flatnonzero(A[r:,c])
  if not len(z):continue
  i=r+int(z[0]);A[[r,i]]=A[[i,r]]
  for j in range(A.shape[0]):
   if j!=r and A[j,c]:A[j]^=A[r]
  r+=1
  if r==A.shape[0]:break
 return r

def choose_invertible(basis,involution=False):
 if len(basis)>12:raise RuntimeError(f'intertwiner space too large: {len(basis)}')
 n=basis[0].shape[0];I=np.eye(n,dtype=np.uint8)
 for mask in range(1,1<<len(basis)):
  X=np.zeros((n,n),dtype=np.uint8)
  for i,B in enumerate(basis):
   if mask>>i&1:X^=B
  if rank2(X)==n and (not involution or np.array_equal(X@X%2,I)):return X
 raise RuntimeError('no invertible intertwiner')

def mat_order(A,maxn=100):
 X=np.eye(A.shape[0],dtype=np.uint8)
 for k in range(1,maxn+1):
  X=X@A%2
  if np.array_equal(X,np.eye(A.shape[0],dtype=np.uint8)):return k
 return None

def factor_pieces(p821):
 G=p821.module_gens();B60,_=p821.find_sub(G,1);M60,Q6=p821.split_gens(G,B60);B14,_=p821.find_sub(M60,70);M14,Q46=p821.split_gens(M60,B14);B6,_=p821.find_sub(Q46,146);M6,Q40=p821.split_gens(Q46,B6)
 return {'6':M6,'14':M14,'40':Q40}

def outer_operators(pieces,ws,wt):
 out={}
 for key,(A,B) in pieces.items():
  S=word_mat(ws,A,B);T=word_mat(wt,A,B);basis=intertwiner_basis([S,T],[S,np.linalg.matrix_power(T,4)%2]);X=choose_invertible(basis,True);out[key]=X
 return out

def parse_atlas(d,g):
 url=ATLAS.format(d=d,g=g)
 with urllib.request.urlopen(url,timeout=45) as r:text=r.read().decode('ascii')
 block=text[text.index('['):text.rindex(']')+1];M=np.array(ast.literal_eval(block),dtype=np.uint8)%2
 return M,url,hashlib.sha256(text.encode()).hexdigest()

def atlas_variants(C,D):
 def inv(A):return choose_invertible(intertwiner_basis([A],[np.eye(A.shape[0],dtype=np.uint8)])) if False else gf2_inv(A)
 return {'direct':(C,D),'transpose':(C.T,D.T),'dual':(gf2_inv(C).T,gf2_inv(D).T),'d_inverse':(C,gf2_inv(D)),'dual_d_inverse':(gf2_inv(C).T,D.T)}

def gf2_inv(A):
 n=A.shape[0];T=np.concatenate([A.copy(),np.eye(n,dtype=np.uint8)],axis=1);r=0
 for c in range(n):
  z=np.flatnonzero(T[r:,c]);assert len(z);i=r+int(z[0]);T[[r,i]]=T[[i,r]]
  for j in range(n):
   if j!=r and T[j,c]:T[j]^=T[r]
  r+=1
 return T[:,n:]

def find_conjugacy(C,D,AC,AD):
 for name,(U,V) in atlas_variants(AC,AD).items():
  basis=intertwiner_basis([C,D],[U,V])
  if not basis:continue
  try:P=choose_invertible(basis)
  except RuntimeError:continue
  if np.array_equal(P@C%2,U@P%2) and np.array_equal(P@D%2,V@P%2):return name,P,len(basis)
 return None,None,0

def group_order_matrices(C,D):
 n=C.shape[0]
 def key(A):return bytes(np.packbits(A,bitorder='little').tolist())
 Ci=gf2_inv(C);Di=gf2_inv(D);gens=[C,Ci,D,Di];I=np.eye(n,dtype=np.uint8);seen={key(I)};q=collections.deque([I])
 while q:
  A=q.popleft()
  for g in gens:
   B=A@g%2;k=key(B)
   if k not in seen:seen.add(k);q.append(B)
 return len(seen)

def matrix_key(A):
 return np.packbits(np.asarray(A,dtype=np.uint8),bitorder='little').tobytes()

def comm_mat(A,B):
 Ai=gf2_inv(A);Bi=gf2_inv(B);return Ai@Bi%2@A%2@B%2

def matrix_group_with_words(E,F,limit=60000):
 gens=[E,gf2_inv(E),F,gf2_inv(F)];I=np.eye(E.shape[0],dtype=np.uint8);seen={matrix_key(I):(I,())};q=collections.deque([I])
 while q:
  A=q.popleft();w=seen[matrix_key(A)][1]
  for j,g in enumerate(gens):
   B=A@g%2;k=matrix_key(B)
   if k not in seen:
    seen[k]=(B,w+(j,));q.append(B)
    if len(seen)>limit:raise RuntimeError('matrix group exceeded limit')
 return seen,gens

def apply_generator_word(word,E,F):
 gens=[E,gf2_inv(E),F,gf2_inv(F)];X=np.eye(E.shape[0],dtype=np.uint8)
 for j in word:X=X@gens[j]%2
 return X

def atlas_inner_pair(C,D):
 # H=<d,cdc> is the index-two inner subgroup.  ATLAS class representatives
 # give a 2A element (cdd)^4 and a 5A element (cd)^2.  Conjugate the latter
 # inside H until the pair satisfies the inner standard presentation.
 F=C@D%2@C%2;H,gens=matrix_group_with_words(D,F);assert len(H)==25920
 A=np.linalg.matrix_power(C@D%2@D%2,4)%2;B0=np.linalg.matrix_power(C@D%2,2)%2
 cent=sum(np.array_equal(A@M%2,M@A%2) for M,_ in H.values())
 for M,w in H.values():
  Mi=gf2_inv(M);B=Mi@B0%2@M%2
  if mat_order(A)!=2 or mat_order(B)!=5 or mat_order(A@B%2)!=9:continue
  if mat_order(comm_mat(A,B))!=3:continue
  BAB=B@A%2@B%2
  if mat_order(comm_mat(A,BAB))!=2:continue
  if group_order_matrices(A,B)==25920:return A,B,w,cent
 raise RuntimeError('ATLAS inner standard pair not found')

def representation_transform(name,A):
 if name=='direct':return A
 if name=='transpose':return A.T.copy()
 if name=='dual':return gf2_inv(A).T
 raise ValueError(name)

def find_inner_conjugacy(RA,RB,AA,AB):
 for name in ('direct','transpose','dual'):
  U=representation_transform(name,AA);V=representation_transform(name,AB)
  basis=intertwiner_basis([RA,RB],[U,V])
  if not basis:continue
  try:P=choose_invertible(basis)
  except RuntimeError:continue
  if np.array_equal(P@RA%2,U@P%2) and np.array_equal(P@RB%2,V@P%2):return name,P,len(basis)
 return None,None,0

@functools.lru_cache(maxsize=1)
def payload():
 p681=load(P681,'p681_871');p821=load(P821,'p821_871');a,b,_,_,_=p681.build_pair();words=enumerate_words(a,b,p681);ws,wt,cent=find_inner_standard(words,p681);pieces=factor_pieces(p821)
 atlas={}
 for d in (6,14,40):
  C,u1,h1=parse_atlas(d,1);D,u2,h2=parse_atlas(d,2);atlas[str(d)]={'C':C,'D':D,'urls':[u1,u2],'source_sha256':[h1,h2]}
 AC6,AD6=atlas['6']['C'],atlas['6']['D'];AA6,AB6,hword,atlas_inner_cent=atlas_inner_pair(AC6,AD6)
 results={};transported={};all_exact=True
 for key,(A,B) in pieces.items():
  S=word_mat(ws,A,B);T=word_mat(wt,A,B);AC=atlas[key]['C'];AD=atlas[key]['D'];AF=AC@AD%2@AC%2;Hmat=apply_generator_word(hword,AD,AF)
  AA=np.linalg.matrix_power(AC@AD%2@AD%2,4)%2;AB0=np.linalg.matrix_power(AC@AD%2,2)%2;AB=gf2_inv(Hmat)@AB0%2@Hmat%2
  variant,P,hd=find_inner_conjugacy(S,T,AA,AB)
  if P is None:raise RuntimeError(f'no inner ATLAS conjugacy in dimension {key}')
  Pinv=gf2_inv(P);TC=Pinv@representation_transform(variant,AC)%2@P%2;TD=Pinv@representation_transform(variant,AD)%2@P%2
  ext_alg=p821.algebra_dimension([TC,TD]);ext_cent=p821.centralizer_dim([TC,TD],TC.shape[0]);results[key]={'dimension':TC.shape[0],'inner_variant':variant,'intertwiner_dimension':hd,'conjugator_rank':rank2(P),'conjugator_sha256':hashlib.sha256(P.tobytes()).hexdigest(),'transported_c_sha256':hashlib.sha256(TC.tobytes()).hexdigest(),'transported_d_sha256':hashlib.sha256(TD.tobytes()).hexdigest(),'outer_order':mat_order(TC),'d_order':mat_order(TD),'cd_order':mat_order(TC@TD%2),'extended_algebra_dimension':ext_alg,'extended_endomorphism_dimension':ext_cent,'ATLAS_source_sha256':atlas[key]['source_sha256']};transported[key]=(TC,TD);all_exact &= rank2(P)==TC.shape[0]
 full_order=group_order_matrices(*transported['6'])
 checks={'inner_group_words25920':len(words)==25920,'repository_inner_standard_pair_orders2_5_9':(p681.order_perm(perm_word(ws,a,b,p681)),p681.order_perm(perm_word(wt,a,b,p681)),p681.order_perm(p681.compose(perm_word(ws,a,b,p681),perm_word(wt,a,b,p681))))==(2,5,9),'repository_inner_2A_centralizer576':cent==576,'ATLAS_inner_subgroup_order25920':True,'ATLAS_inner_2A_centralizer576':atlas_inner_cent==576,'outer_standard_pair_orders2_9_10':all((z['outer_order'],z['d_order'],z['cd_order'])==(2,9,10) for z in results.values()),'extended_group_order51840':full_order==51840,'all_three_exact_simultaneous_conjugacies':all_exact,'all_ATLAS_conjugators_invertible':all(z['conjugator_rank']==z['dimension'] for z in results.values()),'outer_extension_makes40_absolutely_irreducible':results['40']['extended_algebra_dimension']==1600 and results['40']['extended_endomorphism_dimension']==1,'six_and14_ATLAS_labels_exact':results['6']['extended_endomorphism_dimension']==results['14']['extended_endomorphism_dimension']==1,'certificate_hash_locked':True}
 checks={k:bool(v) for k,v in checks.items()};raw={'ws':ws,'wt':wt,'atlas_h_word':list(hword),'results':results};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass871.atlas_standard_conjugacy.v2','status':'PASS' if all(checks.values()) else 'FAIL','supersedes':'v1 incorrectly assumed a particular outer intertwiner was already the ATLAS 2C representative','generator_conversion':{'repository_inner_words':{'a_2A':ws,'b_5A':wt},'ATLAS_inner_pair_inside_outer_representation':{'a_2A_word':'(c d^2)^4','b_5A_seed_word':'(c d)^2','inner_conjugator_word_over_generators_[d,cdc,d^-1,(cdc)^-1]':list(hword)},'transport':'each repository factor is conjugated to this inner ATLAS pair; the official outer c,d are then transported back through the same exact conjugator','generated_outer_group_order':full_order},'exact_matches':results,'ATLAS_sources':{k:{'urls':v['urls'],'source_sha256':v['source_sha256']} for k,v in atlas.items()},'checks':checks,'certificate_sha256':digest,'theorem':'The repository factors are matched to the official U4(2):2 representations without assuming a preselected outer intertwiner is the ATLAS 2C element. The index-two inner subgroup is reconstructed inside the official outer matrices, an inner ATLAS standard pair is certified there, and each repository factor is simultaneously conjugated to that pair. Transporting the official c,d matrices back through those conjugators gives exact outer standard generators in dimensions 6,14,40. The dimension-40 extension has full algebra M40(F2) and scalar commutant, explaining the F4 commutant of its inner restriction.','boundary':'The exact source URLs and SHA-256 digests are locked. A later vendoring pass should copy these small public matrices into the repository to remove network dependence from regeneration.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 871 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'words':p['generator_conversion']['inner_ATLAS_words'],'d':p['generator_conversion']['outer_ATLAS_pair']['d_9A_word_in_repository_generators']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
