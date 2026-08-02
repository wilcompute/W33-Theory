from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
import itertools,json,hashlib,collections
Q=3
def norm(v):
 v=tuple(x%3 for x in v)
 for x in v:
  if x:return tuple((pow(x,-1,3)*y)%3 for y in v)
def sp(u,v):return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%3
pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)}
edges=[(i,j) for i,j in itertools.combinations(range(40),2) if sp(pts[i],pts[j])==0];ei={e:i for i,e in enumerate(edges)}
M=json.load(open(ROOT/'data/w33_pass2551_canonical_frame_ordering.json'));emap=M['edge_map_canonical_to_frozen'];inv=[0]*240
for c,o in enumerate(emap):inv[o]=c
def trans(v):
 v=norm(v);out=[]
 for x in pts:
  z=sp(x,v);out.append(pi[norm(tuple((x[i]+z*v[i])%3 for i in range(4)))])
 return out
def outerp():return [pi[norm((x[0],x[1],2*x[2],2*x[3]))] for x in pts]
def edgeperm(p):
 out=[0]*240
 for old_i in range(240):
  ci=inv[old_i];a,b=edges[ci];cj=ei[tuple(sorted((p[a],p[b])))];out[old_i]=emap[cj]
 return out
def inverse(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return q
pg=[trans(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]+[outerp()]
eg=[edgeperm(p) for p in pg];eg+=list(map(inverse,eg[:]))
def orbit(S):
 S=tuple(sorted(S));seen={S};q=[S]
 for X in q:
  for g in eg:
   Y=tuple(sorted(g[i] for i in X))
   if Y not in seen:seen.add(Y);q.append(Y)
 return seen
cert=json.load(open(ROOT/'data/w33_pass2550_global_u6_lower_shadow_singleton_orbits.json'));samples=cert['singleton_verifier']['witnesses']
assigned={};orbits=[]
for rec in samples:
 S=tuple(rec['support'])
 if S in assigned:continue
 O=orbit(S);idx=len(orbits)
 for T in O:assigned[T]=idx
 orbits.append({'representative':list(min(O)),'witness':list(S),'orbit_size':len(O),'stabilizer_order':51840//len(O),'sample_members':0})
for rec in samples:orbits[assigned[tuple(rec['support'])]]['sample_members']+=1
out={'sample_singletons':len(samples),'distinct_pgsp_orbits_hit':len(orbits),'certified_singleton_lower_bound':sum(o['orbit_size'] for o in orbits),'orbit_size_histogram':dict(collections.Counter(o['orbit_size'] for o in orbits)),'orbits':orbits}
json.dump(out,open(ROOT/'data/w33_pass2550_singleton_sample_orbits.rebuilt.json','w'),indent=2,sort_keys=True);print({k:out[k] for k in out if k!='orbits'})
