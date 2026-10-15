"""TOE84: faithful Heisenberg logical Clifford action on the TOE83 code.

Uses the native 27 Heisenberg vertices, 45 tritangent triangles and the
two H27-invariant 27-square orbits frozen in TOE83. Verifies exact monomial
edge-chain actions preserving X and Z checks, then calculates the ranks of
(g-I) on the 26-dimensional logical homology over F2 and F3.
A logical Clifford automorphism is not a local hardware implementation.
"""
from __future__ import annotations
from itertools import product,combinations
from collections import Counter,defaultdict,deque
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
def certificate():
    D=json.loads((ROOT/'data/w33_20261015_toe83_h27_square_css_surgery.json').read_text(encoding='utf8'))
    M=D['orbit_metadata']; selected=M['selected_orbit_representatives']
    H=list(product(range(3),repeat=3));idx={x:i for i,x in enumerate(H)}
    def mul(x,y):
     a,b,c=x;A,B,C=y
     return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    directions=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    faces=sorted({tuple(sorted(idx[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for g in H for d in directions})
    edges=sorted({tuple(sorted(e)) for f in faces for e in combinations(f,2)})
    assert len(faces)==45 and len(edges)==135
    ei={e:i for i,e in enumerate(edges)}
    perms=[[idx[mul(g,h)] for h in H] for g in H]
    square_orbits=[]
    for rep in selected:
     s=[tuple(e) for e in rep]
     orbit={tuple(sorted(tuple(sorted((p[u],p[v]))) for u,v in s)) for p in perms}
     assert len(orbit)==27
     square_orbits.append(sorted(orbit))
    assert len(set(square_orbits[0])&set(square_orbits[1]))==0
    squares=sorted(set(square_orbits[0])|set(square_orbits[1]))
    assert len(squares)==54
    def walk_from_edges(ee):
     ns=defaultdict(set)
     for u,v in ee:ns[u].add(v);ns[v].add(u)
     assert len(ns)==4 and all(len(x)==2 for x in ns.values())
     v=min(ns);u=min(ns[v]);walk=[v,u]
     while len(walk)<4:walk.append(next(x for x in ns[walk[-1]] if x!=walk[-2]))
     return walk+[v]
    def oriented(walk):
     row=[0]*135
     for u,v in zip(walk,walk[1:]):
      row[ei[tuple(sorted((u,v)))]]+=(1 if u<v else -1)
     return row
    face3=[oriented([a,b,c,a]) for a,b,c in faces]
    square3=[oriented(walk_from_edges(s)) for s in squares]
    boundary3=face3+square3
    def bits(row):return sum(1<<i for i,x in enumerate(row) if x%2)
    boundary2=[bits(r) for r in boundary3]
    def rank2(rows):
     piv={}
     for v in rows:
      while v:
       k=v.bit_length()-1
       if k in piv:v^=piv[k]
       else:piv[k]=v;break
     return len(piv)
    def rank3(rows):
     piv={}
     for row in rows:
      v=[x%3 for x in row]
      while True:
       k=next((i for i,x in enumerate(v) if x),None)
       if k is None:break
       if k in piv:v=[(a-v[k]*b)%3 for a,b in zip(v,piv[k])]
       else:
        if v[k]==2:v=[(-x)%3 for x in v]
        piv[k]=v;break
     return len(piv)
    assert rank2(boundary2)==rank3(boundary3)==83
    adj={v:set() for v in range(27)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    parents={0:None};queue=deque([0]);tree=set()
    while queue:
     u=queue.popleft()
     for v in sorted(adj[u]):
      if v not in parents:
       parents[v]=u;queue.append(v);tree.add(tuple(sorted((u,v))))
    assert len(parents)==27 and len(tree)==26
    def path(u,v):
     anc=set();x=u
     while x is not None:anc.add(x);x=parents[x]
     y=v;tail=[]
     while y not in anc:tail.append(y);y=parents[y]
     prefix=[];x=u
     while x!=y:prefix.append(x);x=parents[x]
     return prefix+[y]+list(reversed(tail))
    cycles3=[]
    for u,v in edges:
     if (u,v) in tree:continue
     cycles3.append(oriented(path(u,v)+[u]))
    assert len(cycles3)==109 and rank3(cycles3)==109
    cycles2=[bits(x) for x in cycles3]
    logical2=[];base=boundary2[:];r=83
    for x in cycles2:
     if rank2(base+[x])>r:logical2.append(x);base.append(x);r+=1
    assert r==109 and len(logical2)==26
    logical3=[];base=boundary3[:];r=83
    for x in cycles3:
     if rank3(base+[x])>r:logical3.append(x);base.append(x);r+=1
    assert r==109 and len(logical3)==26
    rowset3={tuple(x) for x in boundary3}|{tuple(-v for v in x) for x in boundary3}
    rowset2=set(boundary2)
    def edge_map(p):
     q=[];sgn=[]
     for u,v in edges:
      x,y=p[u],p[v]
      q.append(ei[tuple(sorted((x,y)))])
      sgn.append(1 if x<y else -1)
     return q,sgn
    def act3(x,q,sgn):
     out=[0]*135
     for i,v in enumerate(x):
      if v:out[q[i]]=(out[q[i]]+sgn[i]*v)%3
     return out
    def act2(x,q):
     y=0
     while x:
      low=x&-x;i=low.bit_length()-1
      y^=1<<q[i];x^=low
     return y
    vertex3=[[(-1 if u==v else 1 if w==v else 0) for u,w in edges] for v in range(27)]
    assert rank3(vertex3)==26
    vertex_set3={tuple(x%3 for x in row) for row in vertex3}
    result=[]
    for h,p in zip(H,perms):
     q,sgn=edge_map(p)
     assert {tuple(act3(row,q,sgn)) for row in vertex3}==vertex_set3
     assert {tuple(act3(row,q,sgn)) for row in boundary3} <= {tuple(v%3 for v in row) for row in rowset3}
     assert {act2(row,q) for row in boundary2}==rowset2
     delta2=[act2(x,q)^x for x in logical2]
     delta3=[[(a-b)%3 for a,b in zip(act3(x,q,sgn),x)] for x in logical3]
     r2=rank2(boundary2+delta2)-83
     r3=rank3(boundary3+delta3)-83
     result.append({'h':list(h),'rank_g_minus_identity_F2':r2,'rank_g_minus_identity_F3':r3})
    out={'code':'[[135,26,6,4]]_2 and [[135,26,6,4]]_3','H27_order':27,'physical_monomial_chain_automorphisms_verified':27,'logical_action_kernel_F2':[r['h'] for r in result if r['rank_g_minus_identity_F2']==0],'logical_action_kernel_F3':[r['h'] for r in result if r['rank_g_minus_identity_F3']==0],'rank_distribution':dict(Counter(f"{r['rank_g_minus_identity_F2']},{r['rank_g_minus_identity_F3']}" for r in result)),'all_elements':result,'H2_dimension':16}
    assert len(out["logical_action_kernel_F2"])==len(out["logical_action_kernel_F3"])==1
    # Characteristic-three logical rank distinguishes one maximal commuting
    # Pauli direction among the four projective lines of H27/Z(H27).
    identity=(0,0,0)
    rank16={tuple(r['h']) for r in result if r['rank_g_minus_identity_F3']==16}
    clock=rank16|{identity}
    assert len(clock)==9
    assert all(mul(x,y) in clock and mul(x,y)==mul(y,x)
               for x in clock for y in clock)
    center={(0,0,c) for c in range(3)}
    polarizations=set()
    for h in H:
        if h in center:continue
        powers=(identity,h,mul(h,h))
        subgroup=frozenset(mul(z,v) for z in center for v in powers)
        assert len(subgroup)==9
        polarizations.add(subgroup)
    assert len(polarizations)==4 and frozenset(clock) in polarizations
    assert clock=={(0,b,c) for b in range(3) for c in range(3)}
    out['ternary_rank16_polarization']=[list(h) for h in sorted(clock)]
    out['maximal_abelian_polarization_count']=4
    out['modular_clock_boundary']='The code singles out a maximal commuting H27 subgroup by rank over F3; this is a finite Pauli/MUB polarization, not a physical time direction.'
    return out

if __name__ == "__main__":
    result=certificate()
    path=ROOT/'data/w33_20261015_toe84_h27_logical_clifford.json'
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print('TOE84 verified:',result['rank_distribution'],result['logical_action_kernel_F3'])
