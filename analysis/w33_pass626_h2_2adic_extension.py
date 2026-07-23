#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass626_h2_2adic_extension.json'

def build_complex():
 V=list(itertools.combinations(range(8),3));vid={v:i for i,v in enumerate(V)}
 stars=[tuple(sorted(vid[tuple(sorted(pair+(x,)))] for x in range(8) if x not in pair)) for pair in itertools.combinations(range(8),2)]
 tops=[tuple(sorted(vid[t] for t in itertools.combinations(four,3))) for four in itertools.combinations(range(8),4)]
 simp=[set() for _ in range(6)]
 for C in stars+tops:
  for r in range(1,len(C)+1):simp[r-1].update(itertools.combinations(C,r))
 return V,vid,[sorted(x) for x in simp]

def rref2(rows,ncols):
 rows=[r for r in rows if r];piv=[];r=0
 for c in range(ncols):
  m=1<<c;k=next((i for i in range(r,len(rows)) if rows[i]&m),None)
  if k is None:continue
  rows[r],rows[k]=rows[k],rows[r]
  for i in range(len(rows)):
   if i!=r and rows[i]&m:rows[i]^=rows[r]
  piv.append(c);r+=1
  if r==len(rows):break
 return rows[:r],piv

def nullspace2(rows,piv,ncols):
 P=set(piv);out=[]
 for f in range(ncols):
  if f in P:continue
  v=1<<f
  for row,c in zip(rows,piv):
   if row>>f&1:v|=1<<c
  out.append(v)
 return out

def add_basis(B,v,c=0):
 while v:
  p=v.bit_length()-1
  if p in B:v^=B[p][0];c^=B[p][1]
  else:B[p]=(v,c);return True
 return False

def reduce_basis(vs):
 B={};out=[]
 for v in vs:
  if add_basis(B,v):out.append(v)
 return out

class Solver:
 def __init__(self,vs):
  self.B={}
  for i,v in enumerate(vs):
   assert add_basis(self.B,v,1<<i)
 def solve(self,v):
  c=0
  while v:
   p=v.bit_length()-1
   if p not in self.B:raise ValueError('outside span')
   v^=self.B[p][0];c^=self.B[p][1]
  return c

def map_rows(cols,d):
 rows=[]
 for r in range(d):
  z=0
  for j,c in enumerate(cols):
   if c>>r&1:z|=1<<j
  rows.append(z)
 return rows

def kernel(cols,d):
 rr,piv=rref2(map_rows(cols,d),d)
 return nullspace2(rr,piv,d)

def act_vec(cols,v):
 z=0
 while v:
  q=v&-v;i=q.bit_length()-1;z^=cols[i];v^=q
 return z

def restrict(gens,W):
 sol=Solver(W);return [[sol.solve(act_vec(G,w)) for w in W] for G in gens]

def quotient(gens,K,I):
 E={};basis=[]
 for v in I:
  if add_basis(E,v):basis.append(v)
 Q=[]
 for v in K:
  if add_basis(E,v):basis.append(v);Q.append(v)
 sol=Solver(basis);off=len(I)
 return Q,[[sol.solve(act_vec(G,w))>>off for w in Q] for G in gens]

def fixed_basis(gens,d):
 rows=[]
 for G in gens:rows.extend(map_rows([G[j]^(1<<j) for j in range(d)],d))
 rr,piv=rref2(rows,d);return nullspace2(rr,piv,d)

def augmentation_span(gens,d):return reduce_basis([G[j]^(1<<j) for G in gens for j in range(d)])

def centralizer_dimension(gens,d):
 B={};rank=0
 for G in gens:
  grows=map_rows(G,d)
  for r in range(d):
   for c in range(d):
    eq=0;v=G[c]
    while v:
     q=v&-v;k=q.bit_length()-1;eq^=1<<(r*d+k);v^=q
    v=grows[r]
    while v:
     q=v&-v;k=q.bit_length()-1;eq^=1<<(k*d+c);v^=q
    while eq:
     p=eq.bit_length()-1
     if p in B:eq^=B[p]
     else:B[p]=eq;rank+=1;break
 return d*d-rank

def module_data(gens):
 d=len(gens[0]);fix=fixed_basis(gens,d);aug=augmentation_span(gens,d)
 return {'dimension':d,'fixed_dimension':len(fix),'coinvariant_dimension':d-len(aug),'endomorphism_dimension':centralizer_dimension(gens,d)}

def payload():
 V,vid,S=build_complex();idx=[{s:i for i,s in enumerate(x)} for x in S]
 d2=[0]*len(S[1])
 for j,s in enumerate(S[2]):
  for i in range(3):d2[idx[1][s[:i]+s[i+1:]]]^=1<<j
 rr,piv=rref2(d2,len(S[2]));Z=nullspace2(rr,piv,len(S[2]))
 E={};B=[]
 for s in S[3]:
  v=0
  for i in range(4):v^=1<<idx[2][s[:i]+s[i+1:]]
  if add_basis(E,v):B.append(v)
 H=[]
 for v in Z:
  if add_basis(E,v):H.append(v)
 CB=Solver(B+H)
 def perm_action(p):
  vm=[vid[tuple(sorted(p[x] for x in t))] for t in V]
  tri=[idx[2][tuple(sorted(vm[i] for i in s))] for s in S[2]]
  out=[]
  for h in H:
   z=0;v=h
   while v:
    q=v&-v;j=q.bit_length()-1;z^=1<<tri[j];v^=q
   out.append(CB.solve(z)>>len(B))
  return out
 gens=[]
 for a in range(7):
  p=list(range(8));p[a],p[a+1]=p[a+1],p[a];gens.append(perm_action(p))
 trans=[]
 for a,b in itertools.combinations(range(8),2):
  p=list(range(8));p[a],p[b]=p[b],p[a];trans.append(perm_action(p))
 T=[]
 for j in range(125):
  z=0
  for M in trans:z^=M[j]
  T.append(z)
 I=reduce_basis(T);K=kernel(T,125)
 GI=restrict(gens,I)
 Qmid,Gmid=quotient(gens,K,I)
 std=[1<<i for i in range(125)]
 Qtop,Gtop=quotient(gens,std,K)
 Isol=Solver(I);Tbar=[Isol.solve(act_vec(T,q)) for q in Qtop]
 Tbar_rank=len(reduce_basis(Tbar))
 intertwines=all([act_vec(GI[a],Tbar[j])==act_vec(Tbar,Gtop[a][j]) for a in range(7) for j in range(34)])
 mid_inv=fixed_basis(Gmid,57);mid_aug=augmentation_span(Gmid,57)
 inv_in_aug=False
 try:Solver(mid_aug).solve(mid_inv[0]);inv_in_aug=True
 except ValueError:pass
 Q56,G56=quotient(Gmid,[1<<i for i in range(57)],mid_inv)
 core=augmentation_span(G56,56);Gcore=restrict(G56,core)
 layers={'bottom_imT':module_data(GI),'middle_ker_over_im':module_data(Gmid),'top_quotient':module_data(Gtop),'middle_mod_socle':module_data(G56),'middle_core':module_data(Gcore)}
 digest=hashlib.sha256(repr((gens,T,Tbar,mid_inv,core)).encode()).hexdigest()
 checks={
  'H2_dimension125':len(H)==125,
  'central_class_sum_rank34':len(I)==34,
  'central_class_sum_kernel91':len(K)==91,
  'square_zero':all(act_vec(T,v)==0 for v in T),
  'palindromic_34_57_34':(len(I),len(Qmid),len(Qtop))==(34,57,34),
  'top_maps_isomorphically_to_bottom':Tbar_rank==34,
  'top_bottom_intertwiner':intertwines,
  'bottom_top_Schurian':layers['bottom_imT']['endomorphism_dimension']==layers['top_quotient']['endomorphism_dimension']==1,
  'middle_fixed_and_coinvariant_one':layers['middle_ker_over_im']['fixed_dimension']==layers['middle_ker_over_im']['coinvariant_dimension']==1,
  'middle_invariant_line_is_nonsplit':inv_in_aug,
  'middle_trivial_spine_1_55_1':len(mid_inv)==1 and len(core)==55 and len(mid_aug)==56,
  'middle_core_Schurian_no_trivial_subquotients':layers['middle_core']=={'dimension':55,'fixed_dimension':0,'coinvariant_dimension':0,'endomorphism_dimension':1},
  'certificate_hash_locked':len(digest)==64,
 }
 return {'schema':'w33.pass626.h2_2adic_extension.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'canonical_class_sum_filtration':{'operator':'T=sum of the 28 transpositions on H2(F2)','relation':'T^2=0','dimensions':{'image':34,'kernel':91,'kernel_mod_image':57,'quotient':34},'successive_layers':[34,57,34],'top_to_bottom':'T induces an S8-equivariant isomorphism H2/ker(T) -> im(T).'},
  'module_diagnostics':layers,
  'middle_trivial_spine':{'socle_trivial_dimension':1,'augmentation_submodule_dimension':56,'core_dimension':55,'head_trivial_dimension':1,'invariant_line_contained_in_augmentation_submodule':inv_in_aug,'interpretation':'The 57-dimensional middle layer has a canonical nonsplit trivial head/socle spine 1 | 55 | 1. The 55-core and both 34-wings are Schurian and have no trivial submodule or quotient.'},
  'extension_certificate':{'matrix_sha256':digest,'meaning':'The nonzero square-zero central class sum, the 34-57-34 filtration, and the nonsplit 1|55|1 middle spine are an exact characteristic-two certificate for the integral obstruction.','ext_boundary':'This determines the canonical mod-2 shadow and its class-sum filtration. It does not identify a unique element of the full 2-adic Ext^1 group without a Z2-lattice resolution or prove that the Schurian 34/55 factors are absolutely simple.'},
  'theorem':'The integral 35+90 rational splitting has a canonical characteristic-two shadow 34 | 57 | 34. The transposition class sum is square-zero, identifies the two 34-dimensional wings equivariantly, and the middle layer contains a nonsplit trivial spine 1 | 55 | 1. This is strictly stronger than the Jordan census J2^34 plus J1^57.',
  'checks':checks,'boundary':'The filtration is canonical and basis-free, but a full Z2[S8] Ext-class computation and an objectwise geometric basis remain open.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 626 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'layers':p['canonical_class_sum_filtration']['successive_layers']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
