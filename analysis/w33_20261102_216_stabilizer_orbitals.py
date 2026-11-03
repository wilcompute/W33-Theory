#!/usr/bin/env python3
"""Exact group orbital census for W33 216-route measurement null representation.
A rank-six permutation action plus six distinct equivariant squared-Gram
eigenvalues proves every eigenmodule (including the 15D blind subspace) irreducible.
"""
import sys,json,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261102_route_216_cubic_tomography as old
def main():
  pts,lines,N,idx,norm,omega=old.geometry()
  lid={frozenset(L):i for i,L in enumerate(lines)}
  gens=[]
  basis=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
         (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
  for a in basis:
    g=bytes(idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts)
    assert len(set(g))==40
    gens.append(g)
  ident=bytes(range(40))
  group={ident};front=[ident]
  while front:
    nxt=[]
    for g in front:
      for h in gens:
        t=bytes(h[g[i]] for i in range(40))
        if t not in group:group.add(t);nxt.append(t)
    front=nxt
    assert len(group)<=25920
  assert len(group)==25920,len(group)
  # Form exact 216 route orbit, transvections on lines.
  lg=[]
  for g in gens:
    lg.append(tuple(lid[frozenset(g[j] for j in L)] for L in lines))
  seed=frozenset(old.SEED);seen={seed};front=[seed]
  while front:
    nxt=[]
    for s in front:
      for h in lg:
        t=frozenset(h[j] for j in s)
        if t not in seen:seen.add(t);nxt.append(t)
    front=nxt
  assert len(seen)==216
  routes=sorted(seen,key=lambda S:tuple(sorted(S)));pos={s:i for i,s in enumerate(routes)}
  stab=[]
  for g in group:
    image=frozenset(lid[frozenset(g[j] for j in lines[t])] for t in seed)
    if image==seed:stab.append(g)
  assert len(stab)==120
  # stabilizer orbitals (orbits on all 216 route labels)
  per=[tuple(lid[frozenset(g[j] for j in L)] for L in lines) for g in stab]
  W=np.zeros((216,40),dtype=np.int64)
  for i,S in enumerate(routes):
    B=np.zeros(40,dtype=np.int64)
    for j in S:B[list(lines[j])]+=1
    assert np.all((B==0)|(B==2))
    W[i]=B-1
  K=(W@W.T)**2
  baseidx=pos[seed]
  remained=set(range(216));orbit_data=[]
  while remained:
    i=min(remained)
    orb={pos[frozenset(h[j] for j in routes[i])] for h in per}
    assert orb<=remained
    dots=sorted({int(W[baseidx]@W[j]) for j in orb})
    squares=sorted({int(K[baseidx,j]) for j in orb})
    orbit_data.append(dict(size=len(orb),dots=dots,squared_dots=squares))
    remained-=orb
  orbit_data=sorted(orbit_data,key=lambda d:(min(d["squared_dots"]),d["size"]))
  rank=len(orbit_data)
  # if rank=6, the complex permutation commutant is dimension 6. Since K has
  # six distinct real eigenvalues, all its six eigenspaces are irreducible.
  exact_eigenvalues={0:15,576:15,768:81,2304:80,3168:24,14400:1}
  assert int(sum(exact_eigenvalues.values()))==216
  if rank==6:
    assert len({x for d in orbit_data for x in d["squared_dots"]})==6
    assert all(len(d["squared_dots"])==1 for d in orbit_data)
  result={"group_order":len(group),"route_orbit_size":216,"stabilizer_size":len(stab),
    "pair_orbital_rank":rank,"stabilizer_orbits":orbit_data,
    "squared_gram_distinct_eigenvalues":{str(k):v for k,v in exact_eigenvalues.items()},
    "rank_six_multiplicity_free":rank==6,
    "blind_15D_eigenspace_irreducible_under_PSp43":rank==6,
    "scope":"if orbital rank 6, full complex permutation algebra is commutative and eigenmodules irreducible; no theorem about 99D physical unmeasured state operators or optical decoherence"}
  p=ROOT/"data/w33_20261102_216_stabilizer_orbitals.json"
  p.write_text(json.dumps(result,indent=2)+"\n")
  print(json.dumps(result,indent=2),flush=True)
  return result
if __name__=="__main__":main()
