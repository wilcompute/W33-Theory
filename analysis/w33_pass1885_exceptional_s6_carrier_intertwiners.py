#!/usr/bin/env python3
"""Pass 1885: exact S6 branching and literal V9 carrier maps."""
from __future__ import annotations
import collections,functools,hashlib,importlib.util,itertools,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';COMP=ROOT/'data/w33_pass1837_middle_layer_compression.json';OUT=ROOT/'data/w33_pass1885_exceptional_s6_carrier_intertwiners.json'

def load_common():
 s=importlib.util.spec_from_file_location('w33common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def porder(p):
 seen=set();o=1
 for i in range(len(p)):
  if i not in seen:
   j=i;n=0
   while j not in seen:seen.add(j);n+=1;j=p[j]
   o=math.lcm(o,n)
 return o
def ctype(p):
 seen=set();a=[]
 for i in range(len(p)):
  if i not in seen:
   j=i;n=0
   while j not in seen:seen.add(j);n+=1;j=p[j]
   a.append(n)
 return tuple(sorted(a,reverse=True))
def partitions(n,m=None):
 if n==0:yield ();return
 m=n if m is None else min(m,n)
 for a in range(m,0,-1):
  for t in partitions(n-a,a):yield (a,)+t
def shape_boxes(part):return {(r,c) for r,n in enumerate(part) for c in range(n)}
def partition_shape(B):
 if not B:return ()
 rows={}
 for r,c in B:rows.setdefault(r,set()).add(c)
 lens=[]
 for r in range(max(rows)+1):
  cs=rows.get(r,set())
  if cs and cs!=set(range(max(cs)+1)):return None
  lens.append(len(cs))
 while lens and lens[-1]==0:lens.pop()
 return tuple(lens) if all(lens[i]>=lens[i+1] for i in range(len(lens)-1)) else None
def connected(S):
 if not S:return False
 seen={next(iter(S))};q=list(seen)
 while q:
  r,c=q.pop()
  for z in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
   if z in S and z not in seen:seen.add(z);q.append(z)
 return seen==S
def no_square(S):return not any({(r,c),(r+1,c),(r,c+1),(r+1,c+1)}<=S for r,c in S)
@functools.lru_cache(None)
def hooks(part,k):
 B=shape_boxes(part);out=[]
 for sub in itertools.combinations(B,k):
  S=set(sub);new=partition_shape(B-S)
  if new is not None and connected(S) and no_square(S):out.append((new,len({r for r,c in S})-1))
 return tuple(out)
@functools.lru_cache(None)
def chi(part,cyc):
 if not cyc:return int(sum(part)==0)
 return sum((-1)**h*chi(new,cyc[1:]) for new,h in hooks(part,cyc[0]))
def canonical_hash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def matrix_hash(A):return hashlib.sha256(json.dumps(A.tolist(),separators=(',',':')).encode()).hexdigest()
def reduce_matrix(A,d):
 g=d
 for x in A.ravel():g=math.gcd(g,abs(int(x)))
 return A//g,d//g
def main():
 c=load_common();d=c.build_geometry();edges=d['edges'];eidx=d['eidx'];octets=d['octets']
 def signed(pp):
  ep=[];es=[]
  for a,b in edges:
   x,y=pp[a],pp[b];ep.append(eidx[tuple(sorted((x,y)))]);es.append(1 if x<y else -1)
  return tuple(ep),tuple(es)
 gens=[]
 for a in d['acts']+[d['outer']]:
  pp,ep,lp,fp,op,os=a;sep,ses=signed(pp);assert sep==ep;gens.append((pp,ep,ses,op))
 idp=tuple(range(40));seen={idp:(tuple(range(240)),(1,)*240,tuple(range(45)))};q=collections.deque([idp])
 while q:
  pp=q.popleft();ep,es,op=seen[pp]
  for gp,ge,gs,go in gens:
   np_=compose(gp,pp)
   if np_ not in seen:
    seen[np_]=(tuple(ge[ep[i]] for i in range(240)),tuple(gs[ep[i]]*es[i] for i in range(240)),tuple(go[op[i]] for i in range(45)));q.append(np_)
 assert len(seen)==51840
 pack=json.loads(COMP.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F};fi={frozenset(x):i for i,x in enumerate(F)}
 stab=[]
 for pp,(ep,es,op) in seen.items():
  if {frozenset(op[i] for i in x) for x in F}==Fset:
   fp=tuple(fi[frozenset(op[i] for i in x)] for x in F);stab.append((pp,ep,es,op,fp))
 assert len(stab)==720 and {x[4] for x in stab}==set(itertools.permutations(range(6)))
 graph=d['graph'];tri=[z for z in itertools.combinations(range(40),3) if graph.subgraph(z).number_of_edges()==3]
 B1=np.zeros((40,240),dtype=np.int64);B2=np.zeros((240,len(tri)),dtype=np.int64)
 for j,(a,b) in enumerate(edges):B1[a,j]=-1;B1[b,j]=1
 for k,(a,b,z) in enumerate(tri):B2[eidx[(b,z)],k]=1;B2[eidx[(a,z)],k]=-1;B2[eidx[(a,b)],k]=1
 L=B1.T@B1+B2@B2.T;I=np.eye(240,dtype=np.int64)
 spreads=[]
 for pp,(ep,es,op) in seen.items():
  if porder(pp)==2 and sum(i==pp[i] for i in range(40))==0 and sum(i==op[i] for i in range(45))==15 and sum(i==ep[i] for i in range(240))==20 and sum(es[i] for i in range(240) if ep[i]==i)==-20:spreads.append((ep,es))
 assert len(spreads)==36
 S=np.zeros((240,240),dtype=np.int64)
 for ep,es in spreads:
  for i,j in enumerate(ep):S[j,i]+=es[i]
 p4=L@(L-10*I)@(L-16*I)
 projectors={
  '15':(L@(L-4*I)@(L-10*I),1152),
  '24':(-L@(L-4*I)@(L-16*I),360),
  '30':(-p4@S,3456),
  '81':(-(L-4*I)@(L-10*I)@(L-16*I),640),
  '90':(p4@(12*I+S),3456)}
 def tr_projector(ep,es,num,den):
  z=sum(int(es[i])*int(num[i,ep[i]]) for i in range(240));assert z%den==0;return z//den
 module_chars={k:{} for k in projectors};class_sizes=collections.Counter()
 for pp,ep,es,op,fp in stab:
  ct=ctype(fp);class_sizes[ct]+=1
  for name,(num,den) in projectors.items():module_chars[name].setdefault(ct,tr_projector(ep,es,num,den));assert module_chars[name][ct]==tr_projector(ep,es,num,den)
 parts=list(partitions(6));dims={p:chi(p,(1,1,1,1,1,1)) for p in parts};decomp={}
 for name,ch in module_chars.items():
  z={}
  for p in parts:
   n=sum(class_sizes[t]*ch[t]*chi(p,t) for t in class_sizes);assert n%720==0
   if n:z[p]=n//720
  decomp[name]=z;assert sum(dims[p]*m for p,m in z.items())==int(name)
 R=[int(x) for x in pack['residual_vertices']];ri={v:i for i,v in enumerate(R)};mapping={int(k):v for k,v in pack['residual_to_duad_index'].items()};duads=list(itertools.combinations(range(6),2))
 AJ=np.zeros((15,15),dtype=np.int64)
 for i,v in enumerate(R):
  for j,w in enumerate(R):
   if i!=j and len(set(duads[mapping[v]])&set(duads[mapping[w]]))==1:AJ[i,j]=1
 E9n=(AJ-8*np.eye(15,dtype=np.int64))@(AJ-2*np.eye(15,dtype=np.int64))
 M=np.zeros((240,15),dtype=np.int64)
 for pp,ep,es,op,fp in stab:M[ep[3],ri[op[R[1]]]]+=es[3]
 A24,d24=reduce_matrix(projectors['24'][0]@M@E9n,projectors['24'][1]*40)
 A90,d90=reduce_matrix(projectors['90'][0]@M@E9n,projectors['90'][1]*40)
 def left(A,ep,es):
  z=np.zeros_like(A);z[np.array(ep),:]=np.array(es)[:,None]*A;return z
 equiv=True
 for pp,ep,es,op,fp in stab:
  qr=tuple(ri[op[v]] for v in R)
  equiv &= np.array_equal(left(A24,ep,es),A24[:,np.array(qr)]) and np.array_equal(left(A90,ep,es),A90[:,np.array(qr)])
 checks={'stabilizer_order_720':len(stab)==720,'branch_dimensions':all(sum(dims[p]*m for p,m in decomp[n].items())==int(n) for n in decomp),'V9_only_in_24_90':[((4,2) in decomp[n]) for n in ('15','24','30','81','90')]==[False,True,False,False,True],'map24_rank9':np.linalg.matrix_rank(A24)==9,'map90_rank9':np.linalg.matrix_rank(A90)==9,'maps_half_integral':d24==d90==2,'map_grams_equal':np.array_equal(A24.T@A24,A90.T@A90),'map_gram_4E9':np.array_equal(A24.T@A24,4*E9n),'map_images_orthogonal':np.array_equal(A24.T@A90,np.zeros((15,15),dtype=np.int64)),'all_720_equivariant':equiv}
 out={'schema':'w33.pass1885.exceptional_s6_carrier_intertwiners.v1','status':'PASS','subgroup_order':720,'subgroup_description':'setwise stabilizer of the canonical six 5-point fibers; induced action on the fibers is S6','s6_class_sizes':{str(k):v for k,v in sorted(class_sizes.items())},'restricted_characters':{n:{str(k):v for k,v in sorted(ch.items())} for n,ch in module_chars.items()},'branching_by_partition':{n:{str(k):v for k,v in z.items()} for n,z in decomp.items()},'separator_V9_partition':'(4, 2)','separator_V9_multiplicities':{'15':0,'24':1,'30':0,'81':0,'90':1},'sign_twisted_V9_partition':'(2, 2, 1, 1)','sign_twisted_V9_multiplicities':{'15':0,'24':0,'30':1,'81':1,'90':1},'explicit_maps':{'construction':'Reynolds-average the seed e_3 e_1^T, apply E9=(AJ-8I)(AJ-2I)/40 and the exact L1/spread-class projectors. The reduced maps are A24=N24/2 and A90=N90/2.','seed_edge_index':3,'seed_residual_index':1,'denominator':2,'N24_sha256':matrix_hash(A24),'N90_sha256':matrix_hash(A90),'N24_entry_counts':{str(k):int(np.sum(A24==k)) for k in (-1,0,1)},'N90_entry_counts':{str(k):int(np.sum(A90==k)) for k in (-1,0,1)},'ranks':{'N24':int(np.linalg.matrix_rank(A24)),'N90':int(np.linalg.matrix_rank(A90))},'gram_identity':'N24^T N24 = N90^T N90 = 4 E9_num, E9=E9_num/40','orthogonality':'N24^T N90 = 0','equivariance_checks':720},'checks':{k:bool(v) for k,v in checks.items()},'theorem':'Under the exceptional S6 separator, the natural 9-dimensional V_(4,2) occurs once in the 24-sector and once in the 90-sector, and in none of the 15,30,81 sectors. Literal half-integral signed incidence maps realize both copies, with primitive ternary numerators of rank nine, equal Gram, orthogonal images, and all 720 intertwining equations exact.','boundary':'Branching and real intertwiners do not create a complex structure. The 81-sector remains parity-obstructed and contains only the sign-twisted nine-dimensional constituent.'}
 assert all(checks.values()),{k:v for k,v in checks.items() if not v};out['sha256_without_hash_field']=canonical_hash(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':'PASS','branching':out['branching_by_partition'],'sha256':out['sha256_without_hash_field']},indent=2));return out
if __name__=='__main__':main()
