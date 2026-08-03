#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import combinations, product, permutations
import hashlib, json

P=1_000_003
TYPE_A=[(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1)]
MASK_NAMES={m:''.join(map(str,m)) for m in TYPE_A}
CHANNELS=('011','101','110')
MATCHINGS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
CHANNEL_TO_MATCHING=dict(zip(CHANNELS,MATCHINGS))

def inv3(a):
 a%=3
 if a==1:return 1
 if a==2:return 2
 raise ZeroDivisionError

def canon(v):
 for x in v:
  if x%3:
   c=inv3(x);return tuple((c*y)%3 for y in v)
 raise ValueError

def points():
 return sorted({canon(v) for v in product(range(3),repeat=4) if any(v)})

def symp(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3

def build():
 pts=points();adj=[[False]*40 for _ in range(40)]
 for i,j in combinations(range(40),2):
  if symp(pts[i],pts[j])==0:adj[i][j]=adj[j][i]=True
 lines=[tuple(q) for q in combinations(range(40),4) if all(adj[i][j] for i,j in combinations(q,2))]
 through=defaultdict(list);edge_line={}
 for li,line in enumerate(lines):
  for p in line:through[p].append(li)
  for a,b in combinations(line,2):edge_line[tuple(sorted((a,b)))]=li
 centers={}
 for x,y in combinations(range(40),2):
  if not adj[x][y]:
   cs=tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]));assert len(cs)==4
   centers[(x,y)]=cs
 flags=sorted((p,li) for li,line in enumerate(lines) for p in line);flag_index={f:i for i,f in enumerate(flags)}
 return adj,lines,through,edge_line,centers,flag_index

def path_edges(x,y,c,edge_line):
 a=edge_line[tuple(sorted((x,c)))];b=edge_line[tuple(sorted((c,y)))]
 return [(x,a),(c,a),(c,b),(y,b)]

def xor_paths(paths):
 cnt=Counter()
 for path in paths:
  for e in path:cnt[e]^=1
 return frozenset(e for e,v in cnt.items() if v)

def is_cycle(es):
 if len(es)!=8:return False
 deg=Counter();graph=defaultdict(list)
 for p,l in es:
  a=('p',p);b=('l',l);deg[a]+=1;deg[b]+=1;graph[a].append(b);graph[b].append(a)
 if len(deg)!=8 or any(v!=2 for v in deg.values()):return False
 seen={next(iter(deg))};stack=list(seen)
 while stack:
  u=stack.pop()
  for v in graph[u]:
   if v not in seen:seen.add(v);stack.append(v)
 return len(seen)==8

def sparse_row(es,flag_index):
 graph=defaultdict(list);edge_for={}
 for p,l in es:
  a=('p',p);b=('l',l);graph[a].append(b);graph[b].append(a);edge_for[frozenset((a,b))]=(p,l)
 for u in graph:graph[u].sort()
 start=min(graph);prev=None;cur=start;nxt=graph[start][0];row={}
 for _ in range(8):
  f=edge_for[frozenset((cur,nxt))];row[flag_index[f]]=1 if cur[0]=='p' else -1
  prev,cur=cur,nxt
  if cur==start:break
  nxt=next(x for x in graph[cur] if x!=prev)
 assert len(row)==8
 return tuple(sorted(row.items()))

def gf_rank(rows,ncols=160,p=P):
 piv={}
 for row in rows:
  r={c:v%p for c,v in row if v%p}
  while r:
   c=min(r)
   if c not in piv:
    z=pow(r[c],p-2,p);piv[c]={k:(v*z)%p for k,v in r.items()};break
   z=r[c]
   for k,v in piv[c].items():
    nv=(r.get(k,0)-z*v)%p
    if nv:r[k]=nv
    elif k in r:del r[k]
 return len(piv)

def digest(rows):
 h=hashlib.sha256()
 for row in rows:
  h.update(';'.join(f'{c}:{v}' for c,v in row).encode());h.update(b'\n')
 return h.hexdigest()

def permute_bits(mask,p):
 out=[0]*4
 for i,b in enumerate(mask):out[p[i]]=b
 return tuple(out)

def parameter_intertwiner_checks():
 d4=[]
 for p in permutations(range(4)):
  E={frozenset((0,1)),frozenset((1,2)),frozenset((2,3)),frozenset((3,0))}
  if {frozenset((p[a],p[b])) for a,b in E}==E:d4.append(p)
 assert len(d4)==8
 rows=[]
 for m in TYPE_A:
  omitted=m.index(0)
  for ch,M in CHANNEL_TO_MATCHING.items():rows.append((MASK_NAMES[m],ch,omitted,M))
 assert len(rows)==12 and len({(o,M) for _,_,o,M in rows})==12
 for p in d4:
  for m in TYPE_A:assert permute_bits(m,p).index(0)==p[m.index(0)]
 return {'d4_order':8,'chart_count':12,'bijection':True,'d4_face_equivariance':True}

def main():
 adj,lines,through,edge_line,centers,flag_index=build()
 rows={(m,r):[] for m in TYPE_A for r in range(3)}
 per_rectangle_distinct=True;rectangles=0
 for c in range(40):
  for li,lj in combinations(through[c],2):
   A=tuple(sorted(set(lines[li])-{c}));B=tuple(sorted(set(lines[lj])-{c}))
   for aa in combinations(A,2):
    for bb in combinations(B,2):
     re=[tuple(sorted(e)) for e in [(aa[0],bb[0]),(aa[1],bb[0]),(aa[1],bb[1]),(aa[0],bb[1])]]
     pm=defaultdict(list)
     for gauges in product(*(centers[e] for e in re)):
      cy=xor_paths([path_edges(x,y,g,edge_line) for (x,y),g in zip(re,gauges)])
      if is_cycle(cy):
       m=tuple(1 if g==c else 0 for g in gauges)
       if m in TYPE_A:pm[m].append((tuple(sorted(cy)),sparse_row(cy,flag_index)))
     local=[]
     for m in TYPE_A:
      vals=sorted(pm[m],key=lambda z:z[0]);assert len(vals)==3
      for r,(_,row) in enumerate(vals):rows[(m,r)].append(row);local.append(row)
     per_rectangle_distinct &= len(set(local))==12
     rectangles+=1
 assert rectangles==2160
 atlas={};allrows=[]
 for m in TYPE_A:
  for r,ch in enumerate(CHANNELS):
   rr=rows[(m,r)];allrows+=rr
   atlas[f'{MASK_NAMES[m]}_{ch}']={'rows':len(rr),'rank':gf_rank(rr),'sha256':digest(rr),'row_weight_set':sorted({len(x) for x in rr})}
 checks={'rectangles_2160':rectangles==2160,'twelve_operator_atlas':len(atlas)==12,'all_rows_2160':all(x['rows']==2160 for x in atlas.values()),'all_rank_81':all(x['rank']==81 for x in atlas.values()),'all_row_weight_8':all(x['row_weight_set']==[8] for x in atlas.values()),'all_hashes_distinct':len({x['sha256'] for x in atlas.values()})==12,'per_rectangle_twelve_distinct':per_rectangle_distinct,'union_rank_81':gf_rank(allrows)==81}
 checks.update(parameter_intertwiner_checks())
 boolchecks={k:v for k,v in checks.items() if isinstance(v,bool)}
 assert all(boolchecks.values()),[k for k,v in boolchecks.items() if not v]
 out={'schema':'w33.bt2809.selector_face_pairing_intertwiner.v1','status':'COMPLETE_EXACT','rectangles':rectangles,'operator_shape':[2160,160],'parameter_map':{ch:[list(x) for x in M] for ch,M in CHANNEL_TO_MATCHING.items()},'atlas':atlas,'union_rank':gf_rank(allrows),'checks':checks,'check_count':len(boolchecks),'boundary':'Exact parameter-space and operator-atlas intertwiner. It does not assert that a global S4 action on tetrahedral coordinates lifts to bare coordinate permutations of W33; signed monomial lifts are a separate group-theoretic layer.'}
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
