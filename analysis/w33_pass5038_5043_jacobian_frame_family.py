#!/usr/bin/env python3
"""Pass5038-5043: Jacobian/H1 bridge, apartment robustness, local groups, and three continuations."""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from math import lcm
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp
from analysis.w33_pass4992_4999_common import build_base,build_group,closure
ROOT=Path(__file__).resolve().parents[1]
def rank_mod(M,p):
 A=[[int(x)%p for x in row] for row in np.asarray(M,dtype=object)];n=len(A);m=len(A[0]);r=0
 for c in range(m):
  k=next((i for i in range(r,n) if A[i][c]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];z=pow(A[r][c],-1,p);A[r]=[(x*z)%p for x in A[r]]
  for i in range(n):
   if i!=r and A[i][c]:z=A[i][c];A[i]=[(A[i][j]-z*A[r][j])%p for j in range(m)]
  r+=1
  if r==n:break
 return r
def comp(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inv(g):
 z=[0]*len(g)
 for i,j in enumerate(g):z[j]=i
 return tuple(z)
def order(g):
 seen=[0]*len(g);o=1
 for i in range(len(g)):
  if not seen[i]:
   j=i;n=0
   while not seen[j]:seen[j]=1;n+=1;j=g[j]
   if n:o=lcm(o,n)
 return o
def gen(S):
 I=tuple(range(len(S[0]))) if S else tuple(range(40));G={I};Q=[I]
 while Q:
  a=Q.pop()
  for g in S:
   b=comp(g,a)
   if b not in G:G.add(b);Q.append(b)
 return G
def conj(g,h):return comp(comp(g,h),inv(g))
def profile(H):
 cen={g for g in H if all(comp(g,h)==comp(h,g) for h in H)};comm={comp(comp(comp(inv(g),inv(h)),g),h) for g in H for h in H};der=gen(list(comm))
 return {'order':len(H),'orders':dict(Counter(order(g) for g in H)),'center':len(cen),'derived':len(der)}
def gf2_basis_columns(A,target):
 piv={};sel=[]
 for j in range(A.shape[1]):
  x=0
  for i,b in enumerate(np.asarray(A[:,j],dtype=int)&1):
   if b:x|=1<<i
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;sel.append(j);break
  if len(sel)==target:return sel
 return sel
def build_X(W,L):
 flags=[(p,l) for l,Q in enumerate(L) for p in Q];fi={f:i for i,f in enumerate(flags)};pl={}
 for l,Q in enumerate(L):
  for a,b in itertools.combinations(Q,2):pl[tuple(sorted((a,b)))]=l
 aps=[c for c in itertools.combinations(range(40),4) if W.subgraph(c).number_of_edges()==4 and set(dict(W.subgraph(c).degree()).values())=={2}];X=np.zeros((160,1620),dtype=np.int8)
 for k,ps in enumerate(aps):
  H=W.subgraph(ps);s=min(ps);a=min(H.neighbors(s));b=next(x for x in H.neighbors(a) if x!=s);c=next(x for x in H.neighbors(b) if x!=a);cy=[s,a,b,c]
  for i in range(4):p,q=cy[i],cy[(i+1)%4];l=pl[tuple(sorted((p,q)))];X[fi[(p,l)],k]=1;X[fi[(q,l)],k]=-1
 return flags,aps,X
def qcheck(q):
 def norm(v):
  v=tuple(x%q for x in v);i=next(i for i,x in enumerate(v) if x);a=pow(v[i],-1,q);return tuple(a*x%q for x in v)
 def sy(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%q
 P=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)});G=nx.Graph();G.add_nodes_from(range(len(P)))
 for i,j in itertools.combinations(range(len(P)),2):
  if sy(P[i],P[j])==0:G.add_edge(i,j)
 L=sorted({tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==q+1});flags=[(p,l) for l,Q in enumerate(L) for p in Q];fi={f:i for i,f in enumerate(flags)};pl={}
 for l,Q in enumerate(L):
  for a,b in itertools.combinations(Q,2):pl[tuple(sorted((a,b)))]=l
 aps=[c for c in itertools.combinations(range(len(P)),4) if G.subgraph(c).number_of_edges()==4 and set(dict(G.subgraph(c).degree()).values())=={2}];X=np.zeros((len(flags),len(aps)),dtype=int)
 for k,ps in enumerate(aps):
  H=G.subgraph(ps);s=min(ps);a=min(H.neighbors(s));b=next(x for x in H.neighbors(a) if x!=s);c=next(x for x in H.neighbors(b) if x!=a);cy=[s,a,b,c]
  for i in range(4):p,r=cy[i],cy[(i+1)%4];l=pl[tuple(sorted((p,r)))];X[fi[(p,l)],k]=1;X[fi[(r,l)],k]=-1
 adj=[[] for _ in flags]
 for i,(p,l) in enumerate(flags):
  for j,(r,m) in enumerate(flags):
   if i!=j and (p==r or l==m):adj[i].append(j)
 D=np.full((len(flags),len(flags)),-1,dtype=int)
 for s in range(len(flags)):
  D[s,s]=0;Qd=deque([s])
  while Qd:
   u=Qd.popleft()
   for v in adj[u]:
    if D[s,v]<0:D[s,v]=D[s,u]+1;Qd.append(v)
 R=np.array([[(-1)**D[i,j]*q**(4-D[i,j]) for j in range(len(flags))] for i in range(len(flags))],dtype=int)
 return {'points':len(P),'lines':len(L),'chambers':len(flags),'apartments':len(aps),'rank':int(np.linalg.matrix_rank(X.astype(float))),'XXT_R':bool(np.array_equal(X@X.T,R)),'R2':bool(np.array_equal(R@R,len(flags)*R))}
def main():
 b=build_base();W=b['W'];L=b['L'];flags,aps,X=build_X(W,L);assert len(flags)==160 and len(aps)==1620 and np.linalg.matrix_rank(X.astype(float))==81
 B=np.zeros((80,160),dtype=np.uint8)
 for j,(p,l) in enumerate(flags):B[p,j]=1;B[40+l,j]=1
 assert rank_mod(B,2)==79;A=np.block([[np.zeros((80,80),dtype=np.uint8),B],[B.T,np.zeros((160,160),dtype=np.uint8)]]);assert rank_mod(A,2)==158;Ar=np.delete(np.delete(A,0,axis=0),0,axis=1);assert rank_mod(Ar,2)==158
 out38={'pass':5038,'status':'PASS','incidence_rank_F2':79,'cycle_dimension':81,'full_mod2_rank':158,'reduced_mod2_nullity':81,'isomorphism':'K(SubLevi)/2K = H1(Levi;F2)'}
 C=X.T@X;profiles=[Counter(abs(int(C[i,j])) for j in range(1620) if j!=i) for i in range(1620)];assert len({tuple(sorted(z.items())) for z in profiles})==1 and profiles[0]==Counter({0:1187,1:288,2:96,3:32,4:16})
 def bound(r):
  z=r-1;s=8
  for a,n in [(4,16),(3,32),(2,96),(1,288)]:k=min(z,n);s+=a*k;z-=k
  return s
 assert bound(46)==159 and bound(47)==162;gone=set(np.flatnonzero(X[0]));remain=[j for j in range(1620) if j not in gone];assert len(gone)==81 and np.linalg.matrix_rank(X[:,remain].astype(float))==80
 sel=gf2_basis_columns(X,81);sv=np.linalg.svd(X[:,sel].astype(float),compute_uv=False);out39={'pass':5039,'status':'PASS','identity':'XXT=160P','correlations':{'4':16,'3':32,'2':96,'1':288,'0':1187},'all_safe_through':46,'bound46':159,'bound47':162,'failure_example_removed':81,'failure_remaining_rank':80,'basis81':sel,'basis_condition':float(sv[0]/sv[-1])}
 gg=build_group(b);P=closure(gg['LpP'],40);PG=closure(gg['LpF'],40);base=frozenset(aps[0]);H16={g for g in P if frozenset(g[x] for x in base)==base};H32={g for g in PG if frozenset(g[x] for x in base)==base};assert len(H16)==16 and len(H32)==32;I=tuple(range(40))
 subs16={frozenset(gen([g])) for g in H16}
 for g in H16:
  for h in H16:subs16.add(frozenset(gen([g,h])))
 V4=[set(H) for H in subs16 if len(H)==4 and Counter(order(x) for x in H)==Counter({1:1,2:3})];C4=[set(H) for H in subs16 if len(H)==4 and Counter(order(x) for x in H)==Counter({1:1,2:1,4:2})];splits=[]
 for V in V4:
  if all({conj(g,h) for h in V}==V for g in H16):
   for D in C4:
    if V&D=={I} and len(gen(list(V)+list(D)))==16:splits.append((V,D))
 assert splits and len({c for c in splits[0][1] if all(conj(c,v)==v for v in splits[0][0])})==2
 def image_on_base(H):
  bs=sorted(base);bi={p:i for i,p in enumerate(bs)};return {tuple(bi[g[p]] for p in bs) for g in H}
 assert len(image_on_base(H16))==len(image_on_base(H32))==8;K32={g for g in H32 if all(g[p]==p for p in base)};assert len(K32)==4 and Counter(order(x) for x in K32)==Counter({1:1,2:3});subs32=set()
 for g in H32:
  for h in H32:subs32.add(frozenset(gen([g,h])))
 comps=[set(H) for H in subs32 if len(H)==8 and set(H)&K32=={I} and Counter(order(x) for x in H)==Counter({1:1,2:5,4:2})];assert len(comps)==8;actker={g for g in comps[0] if all(conj(g,k)==k for k in K32)};assert len(actker)==4
 line_index={frozenset(Q):i for i,Q in enumerate(L)};base_lines=frozenset(line_index[frozenset(Q)] for Q in L if len(set(Q)&set(base))==2);p0=min(base);l0=min(l for l in base_lines if p0 in L[l])
 def lp(g,l):return line_index[frozenset(g[x] for x in L[l])]
 localsizes={}
 for tag,H in [('P',H16),('PG',H32)]:hp={g for g in H if g[p0]==p0};hl={g for g in H if lp(g,l0)==l0};localsizes[tag]={'point':profile(hp),'line':profile(hl),'flag':profile(hp&hl)}
 out40={'pass':5040,'status':'PASS','inner':profile(H16),'inner_model':'V4:C4 with action image C2','outer':profile(H32),'outer_model':'V4:D8 split with action image C2','outer_complements':8,'locals':localsizes}
 lev=nx.Graph();lev.add_nodes_from(range(80))
 for j,(p,l) in enumerate(flags):lev.add_edge(p,40+l,idx=j)
 tree=nx.minimum_spanning_tree(lev);te={frozenset(e) for e in tree.edges()};chords=[d['idx'] for u,v,d in lev.edges(data=True) if frozenset((u,v)) not in te];assert len(chords)==81;CC=X[chords,:];basis=gf2_basis_columns(CC,81);det=int(sp.Matrix(CC[:,basis].tolist()).det(method='domain-ge'));assert abs(det)==1
 out41={'pass':5041,'status':'PASS','coordinates':[81,1620],'rank':81,'unimodular_minor':det,'basis_columns':basis,'index':1};assert nx.girth(lev)==8;out42={'pass':5042,'status':'PASS','parameters':[160,81,8],'minimum_words':1620,'minimum_geometry':'apartments'}
 q2=qcheck(2);q3=qcheck(3);assert q2=={'points':15,'lines':15,'chambers':45,'apartments':90,'rank':16,'XXT_R':True,'R2':True};assert q3=={'points':40,'lines':40,'chambers':160,'apartments':1620,'rank':81,'XXT_R':True,'R2':True}
 out43={'pass':5043,'status':'PASS','formulas':{'points_lines':'(q+1)(q^2+1)','chambers':'(q+1)^2(q^2+1)','cycle_rank':'q^4','apartments':'q^4(q+1)^2(q^2+1)/8','apartments_per_chamber':'q^4','R':'(-1)^ell q^(4-ell)'},'q2':q2,'q3':q3,'odd_q':'dim K(SubLevi_q)/2K = q^4'}
 outs={5038:out38,5039:out39,5040:out40,5041:out41,5042:out42,5043:out43};names={5038:'PART_W33_PASS5038_SUBDIVISION_JACOBIAN_H1_MOD2.json',5039:'PART_W33_PASS5039_APARTMENT_FRAME_ROBUSTNESS.json',5040:'PART_W33_PASS5040_APARTMENT_LOCAL_GROUPS.json',5041:'PART_W33_PASS5041_INTEGRAL_APARTMENT_GENERATION.json',5042:'PART_W33_PASS5042_MINIMUM_CYCLES.json',5043:'PART_W33_PASS5043_Q_GENERAL_BUILDING_FAMILY.json'}
 for k,v in outs.items():(ROOT/'data'/names[k]).write_text(json.dumps(v,indent=2)+'\n')
 print(json.dumps(outs,indent=2))
if __name__=='__main__':main()
