#!/usr/bin/env python3
"""Fixed Jordan-frame obstruction: 24D W33 positive adjacency eigenspace is
absolutely irreducible under PSp4(3), so it cannot be three invariant
8D Albert Peirce off-diagonal modules with three fixed idempotents.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
def main():
 pts,lines,N,idx,norm,omega=geometry();A=N@N.T-4*np.eye(40,dtype=np.int64)
 G=(A==1)
 assert np.array_equal(A@A,8*np.eye(40,dtype=np.int64)-2*A+4*np.ones((40,40),dtype=np.int64))
 E=np.eye(40,dtype=np.int64);J=np.ones((40,40),dtype=np.int64)
 ev=np.linalg.eigvalsh(A)
 spectrum={str(v):int(np.count_nonzero(abs(ev-v)<1e-9)) for v in (12,2,-4)}
 assert spectrum=={'12':1,'2':24,'-4':15},spectrum
 # full PSp4(3), 8 transvections generate 25920.
 bas=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
      (1,0,1,0),(0,1,0,1),(1,1,1,0),(0,1,1,1)]
 gens=[]
 for a in bas:
  p=bytes(idx[norm(tuple((x[k]+omega(x,a)*a[k])%3 for k in range(4)))] for x in pts)
  assert len(set(p))==40
  gens.append(p)
 ident=bytes(range(40));seen={ident};front=[ident];fix=[]
 while front:
  nxt=[]
  for p in front:
   if p[0]==0:fix.append(p)
   for g in gens:
    t=bytes(g[p[i]] for i in range(40))
    if t not in seen:seen.add(t);nxt.append(t)
  front=nxt
  assert len(seen)<=25920
 assert len(seen)==25920 and len(fix)==648
 remaining=set(range(40));orbits=[]
 while remaining:
  i=min(remaining);o={p[i] for p in fix}
  assert o<=remaining
  orbits.append(len(o));remaining-=o
 assert sorted(orbits)==[1,12,27]
 out={'status':'PASS_FIXED_ALBERT_JORDAN_FRAME_PSp4_3_NO_GO',
      'PSp4_3_order':25920,'point_stabilizer_order':648,
      'point_stabilizer_orbit_sizes':sorted(orbits),
      'point_permutation_rank':3,
      'point_adjacency_spectrum':spectrum,
      'positive_24D_module_absolutely_irreducible':True,
      'reason':'A rank-three transitive permutation action has commutant spanned by I,A,J; the three distinct eigenspaces 1+15+24 each occur with multiplicity 1, hence are absolutely irreducible.',
      'Albert_dimension':27,
      'fixed_frame_Peirce_offdiag_dimensions':[8,8,8],
      'no_go':'There is no PSp4(3)-equivariant embedding of the irreducible 24D route carrier as the off-diagonal 8+8+8 sum of a Jordan frame fixed pointwise by PSp4(3); the Peirce blocks would be proper nonzero invariant submodules.',
      'scope':'Only embeddings preserving a labelled Jordan frame, or a frame set (PSp4(3) simple so cannot permute 3 labels nontrivially). Non-frame exceptional Jordan embeddings and symmetry-breaking actions are NOT excluded; existing repo clock Albert construction is independent and not invalidated.'}
 (ROOT/'data/w33_20261103_albert_fixed_frame_irrep_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
 print('ALBERT_NO_GO',json.dumps(out)[:3500],flush=True)
 return out
if __name__=='__main__':main()
