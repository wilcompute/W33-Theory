from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import itertools,json,networkx as nx
Q=3
def normalize(v):
 w=tuple(int(x)%Q for x in v)
 for x in w:
  if x:
   z=pow(x,-1,Q);return tuple((z*y)%Q for y in w)
 raise ValueError
def symp(u,v):return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%Q
points=sorted({normalize(v) for v in itertools.product(range(Q),repeat=4) if any(v)});pidx={p:i for i,p in enumerate(points)}
A=[[0]*40 for _ in range(40)]
for i,u in enumerate(points):
 for j in range(i+1,40):
  if symp(u,points[j])==0:A[i][j]=A[j][i]=1
line_sets=set()
for i in range(40):
 for j in range(i+1,40):
  if not A[i][j]:continue
  u,v=points[i],points[j];span=set()
  for a,b in itertools.product(range(3),repeat=2):
   w=tuple((a*u[k]+b*v[k])%3 for k in range(4))
   if any(w):span.add(pidx[normalize(w)])
  line_sets.add(tuple(sorted(span)))
lines=sorted(line_sets);lidx={L:i for i,L in enumerate(lines)};edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i][j]];eidx={e:i for i,e in enumerate(edges)}
seen=set();octets=[]
for left in itertools.combinations(range(40),4):
 if any(A[a][b] for a,b in itertools.combinations(left,2)):continue
 right=tuple(v for v in range(40) if all(A[v][u] for u in left))
 if len(right)!=4 or any(A[a][b] for a,b in itertools.combinations(right,2)):continue
 key=tuple(sorted((tuple(left),tuple(right))))
 if key not in seen:seen.add(key);octets.append(key)
octets=sorted(octets);can_inc=[]
for u,v in edges:
 O=[oi for oi,(L,R) in enumerate(octets) if (u in L and v in R) or (u in R and v in L)];assert len(O)==3;can_inc.append(tuple(O))
oldcols=[int(x) for x in open(ROOT/'data/w33_pass1848_syndrome_columns.txt')];old_inc=[tuple(i for i in range(45) if (c>>i)&1) for c in oldcols]
def og(inc):
 G=nx.Graph();G.add_nodes_from(range(45))
 for T in inc:G.add_edges_from(itertools.combinations(T,2))
 return G
m=nx.vf2pp_isomorphism(og(can_inc),og(old_inc));assert m is not None;oct_map=[m[i] for i in range(45)];old_by={tuple(sorted(T)):e for e,T in enumerate(old_inc)};edge_map=[old_by[tuple(sorted(oct_map[o] for o in T))] for T in can_inc];assert sorted(edge_map)==list(range(240))
frames=[];match=[]
for a,La in enumerate(lines):
 for b in range(a+1,40):
  Lb=lines[b]
  if not set(La).isdisjoint(Lb):continue
  mm=[]
  for x in La:
   ys=[y for y in Lb if A[x][y]];assert len(ys)==1;mm.append(eidx[tuple(sorted((x,ys[0])))])
  frames.append((a,b));match.append(tuple(sorted(mm)))
frozen=json.load(open(ROOT/'data/w33_pass2551_canonical_frame_ordering.json'));oldrows=[tuple(sorted(x)) for x in frozen['frozen_frame_edges']];oldrowidx={r:i for i,r in enumerate(oldrows)};frame_map=[oldrowidx[tuple(sorted(edge_map[e] for e in mm))] for mm in match];assert len(set(frame_map))==540
fidx={f:i for i,f in enumerate(frames)}
def trans(v):
 v=normalize(v);out=[]
 for x in points:
  c=symp(x,v);out.append(pidx[normalize(tuple((x[i]+c*v[i])%3 for i in range(4)))])
 return tuple(out)
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def fp(p):
 lp=tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines)
 return tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
cgens=[fp(trans(v)) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))];cgens+=list(map(inv,cgens));invfm=[0]*540
for c,o in enumerate(frame_map):invfm[o]=c
oldgens=[]
for g in cgens:
 ogp=[0]*540
 for oi in range(540):ogp[oi]=frame_map[g[invfm[oi]]]
 oldgens.append(tuple(ogp))
seenp={tuple(range(540))};q=[tuple(range(540))]
for h in q:
 for g in oldgens:
  x=tuple(g[h[i]] for i in range(540))
  if x not in seenp:seenp.add(x);q.append(x)
assert len(q)==25920
with open(ROOT/'data/w33_pass2551_frame_action.in','w') as f:
 f.write(f'540 240 {len(oldgens)}\n')
 for r in oldrows:f.write(' '.join(map(str,r))+'\n')
 for g in oldgens:f.write(' '.join(map(str,g))+'\n')
json.dump({'canonical_points':[list(x) for x in points],'canonical_lines':[list(x) for x in lines],'canonical_octets':[[list(a),list(b)] for a,b in octets],'edge_map_canonical_to_frozen':edge_map,'octet_map_canonical_to_frozen':oct_map,'frame_map_canonical_to_frozen':frame_map,'frozen_frame_edges':[list(x) for x in oldrows],'frozen_generators':[list(x) for x in oldgens]},open(ROOT/'data/w33_pass2551_canonical_frame_ordering.rebuilt.json','w'),separators=(',',':'))
