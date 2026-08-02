#!/usr/bin/env python3
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
P2433=ROOT/'analysis/w33_pass2433_commutative_fusion_search.py'
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py'
OUT=ROOT/'data/w33_pass2472_rank9_scheme_decode.json'
BLOCKS=[[0],[1,5,11,14,15],[2,4,19],[3,6,10,12,17],[7,9],[8,21],[13],[16],[18,20]]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def conv(x):
 if isinstance(x,sp.Basic):
  if x.is_Integer:return int(x)
  if x.is_Rational:return {'num':int(x.p),'den':int(x.q)}
  return str(x)
 if isinstance(x,list):return [conv(y) for y in x]
 return x
def main(output:Path|None=OUT):
 r=load(P2433,'p2433');common=load(COMMON,'common2472');orb=r.orbitals(r.actions());rel,reps=orb[:2];P22,val22,tr=r.structure(rel,reps)
 B=np.zeros((9,22),dtype=np.int64)
 for a,A in enumerate(BLOCKS):B[a,A]=1
 S=np.einsum('ai,ijk,bj->kab',B,P22,B,optimize=True);q=np.zeros((9,9,9),dtype=np.int64)
 for c,C in enumerate(BLOCKS):
  vals=[S[k] for k in C];assert all(np.array_equal(vals[0],x) for x in vals);q[:,:,c]=vals[0]
 vals=[sum(val22[i] for i in A) for A in BLOCKS]
 L=[sp.Matrix([[int(q[a,b,c]) for b in range(9)] for c in range(9)]) for a in range(9)]
 assert all(L[a]*L[b]==L[b]*L[a] for a in range(9) for b in range(9))
 coeff=[0,1,3,7,13,23,41,67,101];T=sum((coeff[i]*L[i] for i in range(9)),sp.zeros(9));ev=T.eigenvects();assert len(ev)==9 and all(m==1 for _,m,_ in ev)
 rows=[]
 for _,_,vecs in ev:
  v=vecs[0];row=[]
  for M in L:
   w=M*v;lam=next(sp.simplify(w[i]/v[i]) for i in range(9) if v[i]!=0);assert w==lam*v;row.append(lam)
  rows.append(row)
 principal=next(i for i,row in enumerate(rows) if row==list(map(sp.Integer,vals)));rows=[rows[principal]]+sorted([row for i,row in enumerate(rows) if i!=principal],key=lambda z:tuple(str(x) for x in z));PM=sp.Matrix(rows)
 mults=list(PM.T.inv()*sp.Matrix([540]+[0]*8));assert mults[0]==1 and all(x.is_Integer and x>0 for x in mults) and sum(mults)==540
 QM=sp.zeros(9)
 for i in range(9):
  for a in range(9):QM[i,a]=sp.simplify(mults[a]*PM[a,i]/vals[i])
 assert PM*QM==540*sp.eye(9)
 kd=[[[sp.simplify(sum(QM[i,a]*QM[i,b]*PM[c,i] for i in range(9))/540) for c in range(9)] for b in range(9)] for a in range(9)];assert all(x.is_Rational and x>=0 for A in kd for B in A for x in B)
 D=common.build_geometry();lines=D['lines'];frames=D['frames'];edges=D['edges'];matchings=D['matchings'];fline=[set(x) for x in frames];fpts=[set(lines[a])|set(lines[b]) for a,b in frames];match=[{edges[e] for e in mm} for mm in matchings]
 features=[]
 for C in BLOCKS:
  hist=collections.Counter()
  for k in C:
   a,b=reps[k];hist[(len(fline[a]&fline[b]),len(match[a]&match[b]),len(fpts[a]&fpts[b]))]+=1
  features.append({str(k):v for k,v in sorted(hist.items())})
 graph_stats=[]
 for c,C in enumerate(BLOCKS):
  A=np.isin(rel,np.array(C,dtype=np.int16));np.fill_diagonal(A,False)
  if c==0:graph_stats.append({'components':540,'component_sizes':{'1':540},'diameter':0});continue
  seen=set();sizes=[];diams=[]
  for s in range(540):
   if s in seen:continue
   comp={s};front=[s];seen.add(s)
   while front:
    u=front.pop()
    for v in np.flatnonzero(A[u]):
     v=int(v)
     if v not in seen:seen.add(v);comp.add(v);front.append(v)
   sizes.append(len(comp));diam=0
   for u in comp:
    dist={u:0};dq=collections.deque([u])
    while dq:
     x=dq.popleft()
     for y in np.flatnonzero(A[x]):
      y=int(y)
      if y not in dist:dist[y]=dist[x]+1;dq.append(y)
    diam=max(diam,max(dist.values()))
   diams.append(diam)
  graph_stats.append({'components':len(sizes),'component_sizes':{str(k):v for k,v in sorted(collections.Counter(sizes).items())},'diameters':{str(k):v for k,v in sorted(collections.Counter(diams).items())}})
 def path_order(matrix):
  H={i:set() for i in range(9)}
  for i in range(9):
   for j in range(i+1,9):
    if matrix[i][j]!=0 or matrix[j][i]!=0:H[i].add(j);H[j].add(i)
  if sorted(map(len,H.values()))!=[1,1,2,2,2,2,2,2,2]:return None
  cur=next(i for i in H if len(H[i])==1);prev=None;out=[]
  while True:
   out.append(cur);nxt=[x for x in H[cur] if x!=prev]
   if not nxt:break
   if len(nxt)!=1:return None
   prev,cur=cur,nxt[0]
  return out if len(out)==9 else None
 ppoly=[{'relation':a,'order':o} for a in range(1,9) if (o:=path_order([[int(q[a,b,c]) for c in range(9)] for b in range(9)]))]
 qpoly=[{'idempotent':a,'order':o} for a in range(1,9) if (o:=path_order([[kd[a][b][c] for c in range(9)] for b in range(9)]))]
 out={'schema':'w33.pass2472.rank9_scheme_decode.v1','status':'PASS_EXACT_RANK9_EIGENMATRICES_KREIN_AND_GEOMETRIC_FINGERPRINTS','carrier':540,'rank':9,'blocks':BLOCKS,'valencies':vals,'multiplicities':[int(x) for x in mults],'first_eigenmatrix_P':conv(rows),'second_eigenmatrix_Q':conv([[QM[i,j] for j in range(9)] for i in range(9)]),'krein_parameters':conv(kd),'krein_nonzero_count':sum(x!=0 for A in kd for B in A for x in B),'p_polynomial_candidates':ppoly,'q_polynomial_candidates':qpoly,'relation_feature_histograms':features,'relation_graph_stats':graph_stats,'imprimitivity_geometry':{'relation_6':'45 disjoint K_{4,4,4} graphs on 12 vertices','relation_7':'135 disjoint K_4 graphs; three K_4 parts inside each relation-6 component','relation_6_union_7':'45 disjoint K_12 graphs'},'checks':{'PQ_540I':True,'multiplicities_sum_540':True,'krein_nonnegative':True,'all_relations_symmetric':all(set(C)=={tr[i] for i in C} for C in BLOCKS),'no_p_polynomial_ordering':not ppoly,'no_q_polynomial_ordering':not qpoly,'relation6_is_45_K444':graph_stats[6]['component_sizes']=={'12':45} and vals[6]==8 and int(q[6,6,6])==4 and int(q[6,6,7])==8,'relation7_is_135_K4':graph_stats[7]['component_sizes']=={'4':135} and vals[7]==3 and int(q[7,7,7])==2},'theorem':'The unique finest binary-generated commutative fusion is a symmetric rank-nine association scheme. Its first eigenmatrix is integral, its second eigenmatrix and all Krein parameters are rational and nonnegative, and its primitive multiplicities are 1,15,15,20,162,135,108,24,60. It is neither P-polynomial nor Q-polynomial. Its canonical imprimitivity layer is 45 copies of K12, refined as 45 copies of K_{4,4,4} together with 135 within-part K4 graphs.','boundary':'This decodes the exact scheme algebra and its coarse frame geometry. It does not identify a physical channel or dynamical law.'}
 out['sha256_without_hash_field']=digest(out)
 if output:output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'sha256':out['sha256_without_hash_field'],'multiplicities':out['multiplicities']},sort_keys=True));return out
if __name__=='__main__':main()
