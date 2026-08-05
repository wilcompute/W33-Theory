#!/usr/bin/env python3
"""A real proof-carrying canary from the star-complement search surface."""
from __future__ import annotations
import argparse,hashlib,itertools,json,random
from pathlib import Path
import numpy as np
import sympy as sp

PAIRS=[(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13)]
EXPECTED_STAGE_COUNTS=[22,784]
EXPECTED_PROOF='a07611183bd01fad1b60134aebba7dc3a8ec0ce7bc29fd7c46ea8c4146010b50'
EXPECTED_RECORD='2a984b9a2f51646691657a8dfe5d01b9e33496f75500ba9b79abdd5a68385390'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def bitperm(x,perm):
 y=0
 for r,old in enumerate(perm):
  if (x>>old)&1:y|=1<<r
 return y
def canon_state(rows,out_edges):
 t=len(rows);best=None;pats=[sum(((1 if leaf in rows[r] else 0)<<r) for r in range(t)) for leaf in range(14)]
 for perm in itertools.permutations(range(t)):
  pair_desc=tuple(sorted(tuple(sorted((bitperm(pats[a],perm),bitperm(pats[b],perm)))) for a,b in PAIRS));inv={old:new for new,old in enumerate(perm)};edges=tuple(sorted(tuple(sorted((inv[a],inv[b]))) for a,b in out_edges));key=(edges,pair_desc)
  if best is None or key<best:best=key
 return best
def build_graph(rows,out_edges):
 n=1+14+len(rows);A=np.zeros((n,n),dtype=np.uint8)
 for leaf in range(14):A[0,1+leaf]=A[1+leaf,0]=1
 for a,b in PAIRS:A[1+a,1+b]=A[1+b,1+a]=1
 for r,neighbors in enumerate(rows):
  v=15+r
  for leaf in neighbors:A[v,1+leaf]=A[1+leaf,v]=1
 for a,b in out_edges:A[15+a,15+b]=A[15+b,15+a]=1
 return A
def valid_extension(rows,out_edges,leafset,adjacent_outs):
 new_index=len(rows);nr=rows+[frozenset(leafset)];ne=set(out_edges);ne.update(tuple(sorted((new_index,o))) for o in adjacent_outs);ne=frozenset(ne);A=build_graph(nr,ne);common=A@A
 for i in range(len(A)):
  if int(A[i].sum())>14:return None
  for j in range(i+1,len(A)):
   if int(common[i,j])>(1 if A[i,j] else 4):return None
 return nr,ne
def extend(states):
 out={}
 for rows,edges in states.values():
  t=len(rows)
  for leafset in itertools.combinations(range(14),4):
   for mask in range(1<<t):
    cand=valid_extension(rows,edges,leafset,[o for o in range(t) if (mask>>o)&1])
    if cand is not None:out.setdefault(canon_state(*cand),cand)
 return out
def stage2():
 rows=[frozenset({0,2,4,6})];edges=frozenset();states={canon_state(rows,edges):(rows,edges)};counts=[]
 for _ in range(2):states=extend(states);counts.append(len(states))
 assert counts==EXPECTED_STAGE_COUNTS;return list(states.values()),counts
def exact_inverse_numerator(A):
 M=2*sp.eye(len(A))-sp.Matrix(A.tolist());Q=M.inv();den=1
 for x in Q:den=sp.ilcm(den,int(x.q))
 return [[int(Q[i,j]*den) for j in range(Q.cols)] for i in range(Q.rows)],int(den)
def qform(num,x,y):return sum(x[i]*num[i][j]*y[j] for i in range(len(x)) for j in range(len(y)))
def admissible_columns(A):
 num,den=exact_inverse_numerator(A);out=[]
 for leaves in itertools.combinations(range(1,15),4):
  leafmask=sum(1<<i for i in leaves)
  for outside in range(16):
   mask=leafmask|sum(((outside>>j)&1)<<(15+j) for j in range(4));x=tuple((mask>>i)&1 for i in range(19));Cx=[sum(int(A[i,j])*x[j] for j in range(19)) for i in range(19)]
   if any(Cx[i]>(1 if x[i] else 4) for i in range(19)):continue
   if qform(num,x,x)==2*den:out.append(x)
 return out,num,den
def compatibility(columns,num,den):
 n=len(columns);adj=[0]*n
 for i in range(n):
  for j in range(i+1,n):
   x,y=columns[i],columns[j];inner=qform(num,x,y);common=sum(a*b for a,b in zip(x,y))
   if (inner==-den and common<=1) or (inner==0 and common<=4):adj[i]|=1<<j;adj[j]|=1<<i
 return adj
def color_order(P,adj):
 vs=[];q=P
 while q:b=q&-q;vs.append(b.bit_length()-1);q^=b
 order=[];bounds=[];un=set(vs);color=0
 while un:
  color+=1;avail=set(un)
  while avail:
   v=min(avail);order.append(v);bounds.append(color);un.remove(v);avail.remove(v);avail={u for u in avail if not ((adj[v]>>u)&1)}
 return order,bounds
def maximum_clique(adj):
 best=[];nodes=0
 def expand(R,P):
  nonlocal best,nodes;nodes+=1
  if not P:
   if len(R)>len(best):best=R[:]
   return
  order,bounds=color_order(P,adj)
  for q in range(len(order)-1,-1,-1):
   if len(R)+bounds[q]<=len(best):return
   v=order[q]
   if (P>>v)&1:expand(R+[v],P&adj[v]);P&=~(1<<v)
 expand([], (1<<len(adj))-1);return best,nodes
def vertices(P,n):return [v for v in range(n) if (P>>v)&1]
def greedy_coloring(adj,P):
 classes=[]
 for v in sorted(vertices(P,len(adj)),key=lambda x:(-(adj[x]&P).bit_count(),x)):
  for c in classes:
   if all(not ((adj[v]>>u)&1) for u in c):c.append(v);break
  else:classes.append([v])
 return classes
def prove(adj,P,K,memo=None):
 if memo is None:memo={}
 key=(P,K)
 if key in memo:return {'ref':memo[key]}
 i=len(memo);memo[key]=i;colors=greedy_coloring(adj,P)
 if len(colors)<=K:return {'id':i,'kind':'color','K':K,'classes':colors}
 v=max(vertices(P,len(adj)),key=lambda x:((adj[x]&P).bit_count(),-x));return {'id':i,'kind':'branch','K':K,'vertex':v,'include':prove(adj,P&adj[v],K-1,memo),'exclude':prove(adj,P&~(1<<v),K,memo)}
def verify(adj,P,K,node,seen=None):
 if seen is None:seen={}
 if 'ref' in node:return seen.get(node['ref'])==(P,K)
 i=node.get('id')
 if i in seen or node.get('K')!=K:return False
 seen[i]=(P,K)
 if node.get('kind')=='color':
  cs=node.get('classes',[]);flat=[]
  if len(cs)>K:return False
  for c in cs:
   if len(c)!=len(set(c)) or any((adj[u]>>v)&1 for u,v in itertools.combinations(c,2)):return False
   flat.extend(c)
  return sorted(flat)==vertices(P,len(adj)) and len(flat)==len(set(flat))
 if node.get('kind')=='branch':
  v=node.get('vertex');return isinstance(v,int) and ((P>>v)&1) and verify(adj,P&adj[v],K-1,node['include'],seen) and verify(adj,P&~(1<<v),K,node['exclude'],seen)
 return False
def run():
 states,counts=stage2();combs=list(itertools.combinations(range(14),4));rng=random.Random(3559);valid=tries=0;found=None
 while found is None:
  rows,edges=states[rng.randrange(len(states))];leafset=combs[rng.randrange(len(combs))];mask=rng.randrange(4);tries+=1;cand=valid_extension(rows,edges,leafset,[o for o in range(2) if (mask>>o)&1])
  if cand is None:continue
  valid+=1;nr,ne=cand;A=build_graph(nr,ne);ev=np.linalg.eigvalsh(A.astype(float))
  if float(ev[-2])<2.0-1e-9:found=(nr,ne,A,leafset,mask,float(ev[-2]))
 assert valid==37 and tries==106
 nr,ne,A,leafset,mask,lam=found;cols,num,den=admissible_columns(A);adj=compatibility(cols,num,den);clique,nodes=maximum_clique(adj);proof=prove(adj,(1<<len(adj))-1,len(clique));assert verify(adj,(1<<len(adj))-1,len(clique),proof)
 row={'stage_counts':counts,'valid_candidates_tested':valid,'random_draws':tries,'leafset':list(leafset),'mask':mask,'lambda2':lam,'canonical_state':canon_state(nr,ne),'compatibility_vertices':len(cols),'maximum_clique':len(clique),'search_nodes':nodes,'proof_sha256':digest(proof),'upper_proof':proof,'witness':clique};row['record_sha256']=hashlib.sha256(canon(row).encode()).hexdigest();assert row['proof_sha256']==EXPECTED_PROOF and row['record_sha256']==EXPECTED_RECORD;return row
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--json',type=Path);args=ap.parse_args();row=run()
 if args.json:args.json.parent.mkdir(parents=True,exist_ok=True);args.json.write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')
 print('PASS_REAL_STAR_PROOF_CANARY',row['record_sha256'],{'compatibility_vertices':row['compatibility_vertices'],'maximum_clique':row['maximum_clique'],'proof_sha256':row['proof_sha256']})
if __name__=='__main__':main()
