"""TOE95 exact 468-pair H27-equivariant F1/F2 extension obstruction.

Unlike TOE94's fixed one/two-edge paths, each of four oriented affine
edge orbit seeds may map to ANY F3 1-chain on all 135 Schlaefli edges.
Require vertex-boundary commutation and that 16 H27 face-orbit
representatives (36 triangles + 324 squares) map to boundaries in each
TOE83 square-orbit-pair target complex. Every admissible pair is tested
INDIVIDUALLY: the target normalizer does not fully preserve the source.
"""
from __future__ import annotations
import itertools
from collections import Counter
import json
from pathlib import Path
import numpy as np
from analysis.w33_20261015_toe86_geometry_integral_routing import native,H,D,IDX,mul,IDENTITY
from analysis.w33_20261015_toe93_affine_H27_chain import graph,inv

ROOT=Path(__file__).resolve().parents[1]
tri,edges,ei,perms,orbits=native()
points,addresses,internal,_,_,_=graph()
source_edges=sorted(tuple(sorted((IDX[addresses[u]],IDX[addresses[v]]))) for u,v in internal)
assert len(source_edges)==len(set(source_edges))==108
source_adj=[set() for _ in H]
for u,v in source_edges:source_adj[u].add(v);source_adj[v].add(u)
faces_tri=[list(t)+[t[0]] for t in itertools.combinations(range(27),3)
           if t[1] in source_adj[t[0]] and t[2] in source_adj[t[0]] and t[2] in source_adj[t[1]]]
squares=set()
for u,v in itertools.combinations(range(27),2):
    if v in source_adj[u]:continue
    for a,b in itertools.combinations(sorted(source_adj[u]&source_adj[v]),2):
        squares.add(frozenset(tuple(sorted(z)) for z in ((u,a),(a,v),(v,b),(b,u))))
def walk_square(s):
    adj={}
    for a,b in s:adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
    x=min(adj);y=min(adj[x]);w=[x,y]
    while len(w)<4:w.append(next(z for z in adj[w[-1]] if z!=w[-2]))
    assert w[-1] in adj[x]
    return w+[x]
faces=faces_tri+[walk_square(x) for x in sorted(squares,key=lambda x:sorted(x))]
def signature(w):return tuple(sorted(tuple(sorted((a,b))) for a,b in zip(w,w[1:])))
visited=set();representatives=[]
for w in faces:
    if signature(w) in visited:continue
    orbit={signature([p[x] for x in w]) for p in perms}
    visited.update(orbit);representatives.append(w)
assert len(faces_tri)==36 and len(squares)==324 and len(representatives)==16 and len(visited)==360

src_directions={H[v] for u,v in source_edges if u==0}
assert len(src_directions)==8
seeds=[]
for d in sorted(src_directions):
    if inv(d) not in seeds:seeds.append(d)
assert len(seeds)==4
seed_index={d:i for i,d in enumerate(seeds)}
seed_inverse={inv(d):i for i,d in enumerate(seeds)}

def arc(u,v):
    x,y=H[u],H[v];delta=mul(inv(x),y)
    if delta in seed_index:return seed_index[delta],u,1
    assert delta in seed_inverse
    return seed_inverse[delta],v,2

def oriented_walk(w):
    vector=np.zeros(135,dtype=np.int16)
    for u,v in zip(w,w[1:]):
        j=ei[tuple(sorted((u,v)))]
        vector[j]=(vector[j]+(1 if u<v else 2))%3
    return vector

def target_face_span(pair):
    basis={}
    def insert(v):
        v=v.copy()
        while np.any(v):
            j=int(np.flatnonzero(v)[0])
            if j not in basis:
                basis[j]=(v*(1 if v[j]==1 else 2))%3
                return
            v=(v-v[j]*basis[j])%3
    for t in tri:insert(oriented_walk([*t,t[0]]))
    for o in pair:
        for sq in orbits[o]:
            undirected=[edges[j] for j in sq]
            adj={}
            for u,v in undirected:adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
            x=min(adj);y=min(adj[x]);w=[x,y]
            while len(w)<4:w.append(next(z for z in adj[w[-1]] if z!=w[-2]))
            insert(oriented_walk(w+[x]))
    assert len(basis) in (83,95)
    qdim=135-len(basis);nonpivot=[j for j in range(135) if j not in basis]
    Q=np.zeros((qdim,135),dtype=np.int16)
    for j in range(135):
        v=np.zeros(135,dtype=np.int16);v[j]=1
        for p in sorted(basis):
            if v[p]:v=(v-v[p]*basis[p])%3
        Q[:,j]=v[nonpivot]
    assert np.all((Q@np.stack(list(basis.values())).T)%3==0)
    return len(basis),Q

def admissible_pairs():
    mask=lambda inds:sum(1<<i for i in inds)
    orbit_masks=[[mask(s) for s in orb] for orb in orbits]
    supports=[mask(p) for t in tri for p in itertools.combinations(
        [ei[e] for e in itertools.combinations(t,2)],2)]
    assert len(supports)==135
    coverage=[sum(1<<j for j,p in enumerate(supports)
                  if any((p&s).bit_count()%2 for s in orb)) for orb in orbit_masks]
    full=(1<<135)-1
    selected=[(i,j) for i,j in itertools.combinations(range(40),2)
              if (coverage[i]|coverage[j])==full]
    assert len(selected)==468
    return selected

boundary=np.zeros((27,135),dtype=np.int16)
for j,(u,v) in enumerate(edges):boundary[u,j]=2;boundary[v,j]=1
actions=[]
for g in H:
    p=perms[IDX[g]]
    rows=[];signs=[]
    for u,v in edges:
        x,y=p[u],p[v]
        rows.append(ei[tuple(sorted((x,y)))])
        signs.append(1 if x<y else 2)
    actions.append((np.asarray(rows,dtype=np.int16),np.asarray(signs,dtype=np.int16)))

def solve_pair(pair):
    face_rank,Q=target_face_span(pair)
    q=135-face_rank;n=4*135;m=108+q*len(representatives)
    A=np.zeros((m,n+1),dtype=np.int16)
    for o,d in enumerate(seeds):
        A[27*o:27*(o+1),o*135:(o+1)*135]=boundary
        A[27*o,n]=2;A[27*o+IDX[d],n]=1
    projection=[(Q[:,rows]*signs)%3 for rows,signs in actions]
    for f,walk in enumerate(representatives):
        start=108+q*f
        for u,v in zip(walk,walk[1:]):
            o,g,sign=arc(u,v)
            A[start:start+q,o*135:(o+1)*135]=(
                A[start:start+q,o*135:(o+1)*135]+sign*projection[g])%3
    # Exact F3 Gaussian elimination on the coefficient matrix, applying
    # operations to the RHS too. Any remaining 0|nonzero row refutes F1.
    rank=0
    for col in range(n):
        if rank==m:break
        nz=np.flatnonzero(A[rank:,col])
        if not len(nz):continue
        j=int(rank+nz[0]);A[[rank,j]]=A[[j,rank]]
        if A[rank,col]==2:A[rank]=(2*A[rank])%3
        rr=np.flatnonzero(A[rank+1:,col])+rank+1
        for chunk in np.array_split(rr,max(1,(len(rr)+255)//256)):
            if len(chunk):
                A[chunk]=(A[chunk]-A[chunk,col,None]*A[rank][None,:])%3
        rank+=1
    contradictions=int(np.count_nonzero((A[rank:,:n]==0).all(axis=1)&(A[rank:,n]!=0)))
    return {'pair':list(pair),'target_face_rank':face_rank,'equation_count':m,
            'unknown_edge_coefficients':n,'coefficient_rank':rank,
            'contradiction_rows':contradictions,'extension_exists':contradictions==0}

def certificate():
    census=[solve_pair(p) for p in admissible_pairs()]
    grouped=Counter((r['target_face_rank'],r['coefficient_rank'],r['extension_exists']) for r in census)
    assert grouped=={(83,180,False):36,(95,143,False):432},grouped
    assert all(r['contradiction_rows']>0 for r in census)
    return {
       'source':'TOE93 affine 27-point H27 identification, 108 edges; 36 triangles and 324 chordless squares in 16 H27 face orbits',
       'target':'Each of 468 admissible two-orbit TOE83 Schlaefli/CSS face complexes, tested separately; F3 target boundary span rank 83 or 95',
       'method':'Four unrestricted target F3 135-edge seed chains, H27-translated to all source edges. Impose 4 vertex-boundary equations and 16 face-orbit quotient equations; exact row reduction mod 3.',
       'tested_pair_count':len(census),'solvable_pair_count':0,
       'rank83_pair_count':36,'rank95_pair_count':432,
       'coefficient_rank_by_target_face_rank':{'83':180,'95':143},
       'example_selected_pair':next(r for r in census if r['pair']==[0,10]),
       'all_pairs_reduced_systems':census,
       'scope':'No H27-equivariant boundary-preserving F1 for fixed affine F0 and the stated 360 face cells into any of these 468 targets. It is not a no-go for other F0, different cell sets, ancillas, other target codes, or a physical quantum channel.'}
if __name__=='__main__':
    z=certificate()
    print('TOE95 F1 NO-GO',z['tested_pair_count'],z['solvable_pair_count'],
          z['coefficient_rank_by_target_face_rank'])
    (ROOT/'data/w33_20261017_toe95_allpairs.json').write_text(json.dumps(z,sort_keys=True,indent=2)+'\n')
