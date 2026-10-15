"""TOE83: exact H27-invariant square-face CSS surgery on the native 27-line E6 complex.

Rebuilds the 27 Heisenberg addresses and 45 native tritangent triangles
from the five directions of TOE77/TOE82. Enumerates all 1080 squares,
their 40 H27 orbits, and exhaustively checks all 780 orbit pairs.
Checks ranks and exact minimum X/Z distances over F2 and F3.
This is finite combinatorics, not a fault-tolerant physical implementation.
"""
from __future__ import annotations
import itertools
import collections
from itertools import product,combinations
from collections import Counter,defaultdict
import json
from pathlib import Path

def certificate():
    H=list(product(range(3),repeat=3)); idx={h:i for i,h in enumerate(H)}
    def mul(x,y):
     a,b,c=x;A,B,C=y
     return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    D=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
    faces=sorted({tuple(sorted(idx[mul(g,t)] for t in ((0,0,0),d,mul(d,d)))) for d in D for g in H})
    assert len(faces)==45
    edges=sorted({tuple(sorted(e)) for f in faces for e in combinations(f,2)})
    assert len(edges)==135
    ei={e:i for i,e in enumerate(edges)}
    face_masks=[sum(1<<ei[e] for e in combinations(f,2)) for f in faces]
    adj={v:set() for v in range(27)}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    squares=set()
    for u,v in combinations(range(27),2):
     if v in adj[u]:continue
     for a,b in combinations(sorted(adj[u]&adj[v]),2):
      square=frozenset((tuple(sorted((u,a))),tuple(sorted((a,v))),tuple(sorted((v,b))),tuple(sorted((b,u)))))
      assert len(square)==4
      squares.add(tuple(sorted(ei[e] for e in square)))
    assert len(squares)==1080
    squares=sorted(squares); square_set=set(squares)
    perms=[[idx[mul(g,h)] for h in H] for g in H]
    orbits=[];unseen=set(squares)
    while unseen:
     s=min(unseen);orb={tuple(sorted(ei[tuple(sorted((p[edges[i][0]],p[edges[i][1]])))] for i in s)) for p in perms}
     assert orb<=square_set
     unseen-=orb
     orbits.append(sorted(orb))
    orbits.sort(key=lambda o:(len(o),o[0]))
    def bitrow(s):return sum(1<<i for i in s)
    orbit_masks=[[bitrow(s) for s in o] for o in orbits]
    pair_supports=[]
    for f in faces:
     f_edges=[ei[e] for e in combinations(f,2)]
     pair_supports += [(bitrow(t),f) for t in combinations(f_edges,2)]
    assert len(pair_supports)==135
    def rank(rows):
     piv={}
     for v in rows:
      while v:
       k=v.bit_length()-1
       if k in piv:v^=piv[k]
       else:piv[k]=v;break
     return len(piv)
    base_rank=rank(face_masks)
    assert base_rank==45
    vertex_rows=[bitrow([ei[e] for e in edges if v in e]) for v in range(27)]
    assert rank(vertex_rows)==26
    allpair=(1<<135)-1
    coverage=[]
    for o in orbit_masks:
     coverage.append(sum(1<<j for j,(p,_) in enumerate(pair_supports) if any((p&s).bit_count()%2 for s in o)))
    stats=[{'orbit':i,'size':len(o),'pair_hits':coverage[i].bit_count(),'face_rank_gain':rank(face_masks+orbit_masks[i])-45} for i,o in enumerate(orbits)]
    print('BASE',len(orbits),Counter(len(o) for o in orbits),'hits',Counter(s['pair_hits'] for s in stats),flush=True)
    # Greedy and exact search up to 4 orbits to kill all weight-two logicals.
    solutions=[]
    for k in range(1,5):
     for inds in combinations(range(len(orbits)),k):
      cov=0
      for i in inds:cov|=coverage[i]
      if cov==allpair:
       rows=face_masks+[s for i in inds for s in orbit_masks[i]]
       r=rank(rows)
       if r<109:
        solutions.append((k,r,inds))
     if solutions:
      break
    if not solutions:
     # fallback greedy, always strictly improve coverage
     picked=[];cov=0
     while cov!=allpair:
      candidates=[( (cov|coverage[i]).bit_count()-cov.bit_count(),i) for i in range(len(orbits)) if i not in picked]
      gain,i=max(candidates)
      assert gain>0
      picked.append(i);cov|=coverage[i]
     solutions=[(len(picked),rank(face_masks+[s for i in picked for s in orbit_masks[i]]),tuple(picked))]
    solutions.sort()
    assert len(orbits)==40 and set(len(o) for o in orbits)=={27}
    assert len(solutions)==468 and all(s[0]==2 for s in solutions)
    assert min(s[1] for s in solutions)==83
    print('SOLUTIONS',len(solutions),'BEST',solutions[:12],flush=True)
    # Inspect rank-minimal, maximum-k and fewest-orbit candidates
    best=min(solutions,key=lambda t:(t[1],t[0],t[2]))
    norb,r,inds=best
    selected=face_masks+[s for i in inds for s in orbit_masks[i]]
    assert rank(selected)==r and 135-26-r>0
    assert all(any((p&s).bit_count()%2 for s in selected) for p,_ in pair_supports)
    # Search weight-4 binary X logical: 2+2 edge pairs from different triangles.
    x4=None
    for j,(a,fa) in enumerate(pair_supports):
     for b,fb in pair_supports[j+1:]:
      if fa==fb:continue
      x=a|b
      if all((x&s).bit_count()%2==0 for s in selected) and rank(vertex_rows+[x])==27:
       x4=x;break
     if x4 is not None:break
    # Search surviving weight-four Z cycle (unselected squares) via rank.
    z4=next((bitrow(s) for s in squares if rank(selected+[bitrow(s)])==r+1),None)
    # Binary X no odd weight because each triangle meets X support evenly.
    assert x4 is None and z4 is not None
    print('SELECTED',inds,'rank',r,'k',135-26-r,'x4',x4 is not None,'z4',z4 is not None,flush=True)
    out={'status':'COMPUTED','native_27_vertices':27,'native_135_edges':135,'native_45_faces':45,'square_count':len(squares),'H27_orbit_sizes':dict(Counter(len(o) for o in orbits)),'orbit_stats':stats,'fewest_orbit_solution_count':len(solutions),'selected_orbits':list(inds),'added_square_count':sum(len(orbits[i]) for i in inds),'rank_faces':r,'logical_qubits':135-26-r,'all_135_weight2_X_supports_eliminated':True,'binary_X_distance_lower_bound':4,'weight4_X_logical_witness_edges':[edges[i] for i in range(135) if x4 and (x4>>i)&1] if x4 else None,'weight4_Z_logical_witness_edges':[edges[i] for i in range(135) if z4 and (z4>>i)&1] if z4 else None,'candidate_solutions':[{'orbit_count':k,'face_rank':rankv,'orbits':list(ii)} for k,rankv,ii in solutions[:25]],'orbit_representatives':[[list(edges[i]) for i in orb[0]] for orb in orbits]}
    print('DONE',out['binary_X_distance_lower_bound'],flush=True)
    orbit_metadata=out
    a=locals().copy()
    faces=a['faces'];edges=a['edges'];ei=a['ei'];orbits=a['orbits'];inds=a['inds']
    selected=a['selected']; pair_supports=a['pair_supports']; vertex_rows=a['vertex_rows']
    rank=a['rank'];squares=a['squares'];bitrow=a['bitrow']
    # Binary pair syndromes in selected square-check rows
    checks=[bitrow(s) for i in inds for s in orbits[i]]
    syn=[sum(1<<j for j,s in enumerate(checks) if (p&s).bit_count()%2) for p,f in pair_supports]
    lookup=collections.defaultdict(list)
    for j,v in enumerate(syn):lookup[v].append(j)
    x6=None
    for i in range(135):
     if x6 is not None:break
     for j in range(i+1,135):
      for k in lookup.get(syn[i]^syn[j],()):
       if k<=j:continue
       if len({pair_supports[t][1] for t in (i,j,k)})<3:continue
       x=pair_supports[i][0]|pair_supports[j][0]|pair_supports[k][0]
       if rank(vertex_rows+[x])==27:
        x6=x;break
      if x6 is not None:break
    assert x6 is not None and x6.bit_count()==6
    assert all((x6&s).bit_count()%2==0 for s in selected)
    print('BINARY EXACT dX=6 witness', [edges[i] for i in range(135) if (x6>>i)&1],flush=True)
    # independent ternary boundary matrices and rank
    def rank3(rows):
     """Field-3 rank, using leading pivots (order-independent insertion)."""
     piv={}
     for row in rows:
      v=[int(x)%3 for x in row]
      while True:
       k=next((j for j,t in enumerate(v) if t),None)
       if k is None:break
       if k in piv:
        scale=v[k];w=piv[k]
        v=[(u-scale*z)%3 for u,z in zip(v,w)]
       else:
        if v[k]==2:v=[(-t)%3 for t in v]
        piv[k]=v
        break
     return len(piv)
    def oriented_row(walk):
     out=[0]*135
     for u,v in zip(walk,walk[1:]):
      e=(u,v) if u<v else (v,u)
      out[ei[e]]+=(1 if u<v else -1)
     assert sum(x!=0 for x in out)==len(walk)-1
     return out
    def square_walk(s):
     es=[edges[i] for i in s]
     ns=collections.defaultdict(set)
     for u,v in es:ns[u].add(v);ns[v].add(u)
     assert len(ns)==4 and all(len(x)==2 for x in ns.values())
     v=min(ns);u=min(ns[v]);walk=[v,u]
     while len(walk)<4:
      walk.append(next(x for x in ns[walk[-1]] if x!=walk[-2]))
     assert walk[-1] in ns[v]
     return walk+[v]
    face_rows=[oriented_row([f[0],f[1],f[2],f[0]]) for f in faces]
    square_rows=[oriented_row(square_walk(s)) for i in inds for s in orbits[i]]
    vertex=[[(-1 if u==v else 1 if w==v else 0) for u,w in edges] for v in range(27)]
    assert rank3(vertex)==26 and rank3(face_rows)==45
    assert all(sum(x*y for x,y in zip(f,v))%3==0 for f in face_rows+square_rows for v in vertex)
    r3=rank3(face_rows+square_rows)
    assert r3==83
    print('TERNARY rank faces',r3,'k',135-26-r3,flush=True)
    # Search weight 2 and 3 ternary cocycles, exploiting disjoint triangles.
    rows3=face_rows+square_rows
    w2=0;w3=0
    for f in faces:
     ee=[ei[e] for e in itertools.combinations(f,2)]
     for inds2 in itertools.combinations(ee,2):
      for coeff in itertools.product((1,2),repeat=2):
       x=[0]*135
       for i,c in zip(inds2,coeff):x[i]=c
       if all(sum(x[j]*r[j] for j in inds2)%3==0 for r in rows3):
        w2+=1
     for coeff in itertools.product((1,2),repeat=3):
      x=[0]*135
      for i,c in zip(ee,coeff):x[i]=c
      if all(sum(x[j]*r[j] for j in ee)%3==0 for r in rows3):
       w3+=1
    assert w2==w3==0
    print('TERNARY weight2/3 candidates',w2,w3,flush=True)
    # A ternary weight4 X candidate must have two nonzero entries on each of two distinct triangles.
    pairs3=[]
    for f in faces:
     ee=[ei[e] for e in itertools.combinations(f,2)]
     for pair in itertools.combinations(ee,2):
      for coeff in itertools.product((1,2),repeat=2):
       if all(sum(c*r[i] for i,c in zip(pair,coeff))%3==0 for r in face_rows):
        pairs3.append((f,pair,coeff,tuple(sum(c*r[i] for i,c in zip(pair,coeff))%3 for r in square_rows)))
    assert len(pairs3)==270
    lookup3=collections.defaultdict(list)
    for t in pairs3:lookup3[t[3]].append(t)
    w4=next(((a,b) for j,a in enumerate(pairs3) for b in pairs3[j+1:] if a[0]!=b[0] and all((u+v)%3==0 for u,v in zip(a[3],b[3]))),None)
    assert w4 is None
    print('TERNARY weight4 candidate',bool(w4),flush=True)
    out={'binary':{'X_distance':6,'Z_distance':4,'n':135,'k':135-26-rank(selected),'X_weight6_witness':[list(edges[i]) for i in range(135) if (x6>>i)&1]},'ternary':{'rank_faces':r3,'k':135-26-r3,'X_weight2_candidates':w2,'X_weight3_candidates':w3,'X_weight4_candidate':bool(w4)},'selected_orbits':list(inds)}

    triples3=[]
    for f in faces:
     ee=[ei[e] for e in itertools.combinations(f,2)]
     for coeff in itertools.product((1,2),repeat=3):
      if all(sum(c*r[i] for i,c in zip(ee,coeff))%3==0 for r in face_rows):
       triples3.append((f,tuple(ee),coeff,tuple(sum(c*r[i] for i,c in zip(ee,coeff))%3 for r in square_rows)))
    assert len(triples3)==90
    def neg(s):return tuple((-x)%3 for x in s)
    pair_by_syn=collections.defaultdict(list)
    for a in pairs3:pair_by_syn[a[3]].append(a)
    w5=next(((t,p) for t in triples3 for p in pair_by_syn.get(neg(t[3]),[]) if t[0]!=p[0]),None)
    print('TERNARY weight5 candidate',bool(w5),flush=True)
    # Three 2-edge faces (or two 3-edge faces) at weight 6
    pair2_by_syn=collections.defaultdict(list)
    for i,p in enumerate(pairs3):
     for q in pairs3[i+1:]:
      if p[0]!=q[0]:
       s=tuple((x+y)%3 for x,y in zip(p[3],q[3]))
       pair2_by_syn[s].append((p,q))
    w6=next(((p,q,t) for t in pairs3 for p,q in pair2_by_syn.get(neg(t[3]),[]) if len({p[0],q[0],t[0]})==3),None)
    if w6 is None:
     w6=next(((t,u) for j,t in enumerate(triples3) for u in triples3[j+1:] if t[0]!=u[0] and t[3]==neg(u[3])),None)
    print('TERNARY weight6 candidate',bool(w6),flush=True)
    if w6:
     xx=[0]*135
     for block in w6:
      for i,c in zip(block[1],block[2]):xx[i]=c
     assert sum(bool(x) for x in xx)==6
     assert all(sum(x*y for x,y in zip(xx,r))%3==0 for r in rows3)
     assert rank3(vertex+[xx])==27
     print('TERNARY dX=6 witness',[(edges[i],xx[i]) for i in range(135) if xx[i]],flush=True)
    z4ternary=next((s for s in squares if rank3(rows3+[oriented_row(square_walk(s))])==r3+1),None)
    assert z4ternary is not None
    print('TERNARY dZ=4 witness', [edges[i] for i in z4ternary],flush=True)
    assert w5 is None and w6 is not None
    out['ternary'].update({'X_weight5_candidate':False,'X_distance':6,'Z_distance':4,'X_weight6_witness':[[*edges[i],xx[i]] for i in range(135) if xx[i]],'Z_weight4_witness':[list(edges[i]) for i in z4ternary]})
    orbit_metadata["rank_distribution_covering_two_orbit_pairs"]=dict(Counter(t[1] for t in solutions))
    orbit_metadata["second_homology_dimension"]=45+sum(len(orbits[i]) for i in inds)-r
    orbit_metadata["selected_orbit_representatives"]=[orbit_metadata["orbit_representatives"][i] for i in inds]
    assert orbit_metadata["second_homology_dimension"]==16
    out["orbit_metadata"]=orbit_metadata
    return out

if __name__ == "__main__":
    result=certificate()
    root=Path(__file__).resolve().parents[1]
    path=root / "data/w33_20261015_toe83_h27_square_css_surgery.json"
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("TOE83 verified:",result["binary"],result["ternary"])
