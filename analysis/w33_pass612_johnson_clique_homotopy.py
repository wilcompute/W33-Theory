#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass612_johnson_clique_homotopy.json'
def build_complex():
 V=list(itertools.combinations(range(8),3));vid={v:i for i,v in enumerate(V)}
 stars=[]
 for pair in itertools.combinations(range(8),2):stars.append(tuple(sorted(vid[tuple(sorted(pair+(x,)))] for x in range(8) if x not in pair)))
 tops=[]
 for four in itertools.combinations(range(8),4):tops.append(tuple(sorted(vid[t] for t in itertools.combinations(four,3))))
 maximal=stars+tops;simp=[set() for _ in range(6)]
 for C in maximal:
  for r in range(1,len(C)+1):simp[r-1].update(itertools.combinations(C,r))
 return V,stars,tops,simp
def elementary_collapse(simp):
 active=[set(x) for x in simp];seq=[]
 while True:
  found=None
  for k in range(5,0,-1):
   co=collections.defaultdict(list)
   for tau in sorted(active[k]):
    for i in range(len(tau)):co[tau[:i]+tau[i+1:]].append(tau)
   for sigma in sorted(co):
    ts=co[sigma]
    if sigma not in active[k-1] or len(ts)!=1:continue
    tau=ts[0];maximal=True
    for j in range(k+1,6):
     if any(set(tau).issubset(u) for u in active[j]):maximal=False;break
    if maximal:found=(k-1,sigma,tau);break
   if found:break
  if not found:break
  k,sigma,tau=found;active[k].remove(sigma);active[k+1].remove(tau);seq.append(found)
 return active,seq
def free_reduce(word):
 s=[]
 for x in word:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inverse_word(word):return tuple(-x for x in reversed(word))
def wedge_reduce(active):
 edges=sorted(active[1]);triangles=sorted(active[2]);adj=[[] for _ in range(56)]
 for i,j in edges:adj[i].append(j);adj[j].append(i)
 parent=[None]*56;parent[0]=-1;q=collections.deque([0]);tree=set()
 while q:
  i=q.popleft()
  for j in sorted(adj[i]):
   if parent[j] is None:parent[j]=i;tree.add(tuple(sorted((i,j))));q.append(j)
 non_tree=[e for e in edges if e not in tree];gid={e:k+1 for k,e in enumerate(non_tree)}
 def letter(a,b):
  e=tuple(sorted((a,b)))
  if e in tree:return None
  return gid[e] if a<b else -gid[e]
 rels=[]
 for i,j,k in triangles:rels.append(free_reduce(x for x in (letter(i,j),letter(j,k),letter(k,i)) if x is not None))
 activeg=set(range(1,len(non_tree)+1));seq=[];empty=0
 while True:
  found=None
  for ri,w in enumerate(rels):
   counts=collections.Counter(abs(x) for x in w)
   for g in sorted(counts):
    if counts[g]==1 and g in activeg:found=(ri,g);break
   if found:break
  if found is None:break
  ri,g=found;w=rels[ri];p=next(i for i,x in enumerate(w) if abs(x)==g);x=w[p];A=w[:p];B=w[p+1:]
  rhs=free_reduce(inverse_word(A)+inverse_word(B)) if x==g else free_reduce(B+A)
  activeg.remove(g);new=[]
  for sj,u in enumerate(rels):
   if sj==ri:continue
   v=[]
   for z in u:
    if abs(z)!=g:v.append(z)
    elif z==g:v.extend(rhs)
    else:v.extend(inverse_word(rhs))
   v=free_reduce(v)
   if v:new.append(v)
   else:empty+=1
  rels=new;seq.append((g,w,rhs))
 return tree,non_tree,activeg,rels,empty,seq
def boundary_ranks(simp,p):
 lists=[sorted(x) for x in simp];idx=[{s:i for i,s in enumerate(x)} for x in lists];ranks=[]
 for k in range(1,6):
  A=np.zeros((len(lists[k-1]),len(lists[k])),dtype=np.int64)
  for j,s in enumerate(lists[k]):
   for i in range(len(s)):A[idx[k-1][s[:i]+s[i+1:]],j]=1 if i%2==0 else -1
  A%=p;m,n=A.shape;r=0
  for c in range(n):
   nz=np.flatnonzero(A[r:,c])
   if len(nz)==0:continue
   i=r+int(nz[0]);A[[r,i]]=A[[i,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
   for u in np.flatnonzero(A[:,c]):
    if u!=r:A[u]=(A[u]-A[u,c]*A[r])%p
   r+=1
   if r==m:break
  ranks.append(r)
 return ranks
def payload():
 V,stars,tops,simp=build_complex();active,collapses=elementary_collapse(simp);tree,non_tree,gens,rels,empty,tietze=wedge_reduce(active)
 h=hashlib.sha256()
 for row in collapses:h.update(repr(row).encode())
 for row in tietze:h.update(repr(row).encode())
 f=[len(x) for x in simp];remaining=[len(x) for x in active];ranks={str(p):boundary_ranks(simp,p) for p in (2,3,5,7,11)}
 betti={p:[f[k]-(ranks[p][k-1] if k else 0)-(ranks[p][k] if k<5 else 0) for k in range(6)] for p in ranks}
 checks={'maximal_cliques_28_stars_70_tops':len(stars)==28 and len(tops)==70,'f_vector_56_420_840_490_168_28':f==[56,420,840,490,168,28],'Euler_characteristic126':sum((-1)**i*f[i] for i in range(6))==126,'518_elementary_collapses_to_2_complex':len(collapses)==518 and remaining==[56,420,490,0,0,0],'spanning_tree55_free_edges365':len(tree)==55 and len(non_tree)==365,'365_Tietze_generator_eliminations':len(tietze)==365 and not gens,'125_trivial_2_cells_remain':empty==125 and rels==[],'homology_1_0_125_0_0_0_mod_tested_primes':all(v==[1,0,125,0,0,0] for v in betti.values()),'collapse_transcript_hash_is_sha256':len(h.hexdigest())==64}
 return {'schema':'w33.pass612.johnson_clique_homotopy.v1','status':'PASS' if all(checks.values()) else 'FAIL','complex':{'name':'full clique complex of J(8,3)','maximal_star_5_simplices':28,'maximal_top_3_simplices':70,'f_vector':f,'Euler_characteristic':126},'reduction':{'elementary_simplicial_collapses':len(collapses),'postcollapse_f_vector':remaining,'tree_edges':len(tree),'free_edge_generators':len(non_tree),'Tietze_eliminations':len(tietze),'remaining_trivial_2_cells':empty,'transcript_sha256':h.hexdigest()},'homology':{'integral':{'H0':'Z','H1':'0','H2':'Z^125','H3':'0','H4':'0','H5':'0'},'modular_boundary_ranks':ranks,'modular_Betti_numbers':betti},'theorem':'The full clique complex of J(8,3) is homotopy equivalent to a wedge of 125 two-spheres. An explicit sequence of 518 elementary simplicial collapses reduces it to a 2-complex, after which 365 elementary presentation eliminations remove every edge generator and leave 125 trivially attached 2-cells.','checks':checks,'boundary':'The wedge theorem is a homotopy-equivalence certificate assembled from simplicial collapses and elementary Tietze transformations. It is stronger than homology alone; no claim of a pure simplicial collapse directly to the wedge triangulation is made.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 612 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'homotopy':'wedge_125_S2'}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
