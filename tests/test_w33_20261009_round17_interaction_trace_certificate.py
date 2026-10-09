"""Round17: exact short-time coefficient identities and native orbit witnesses."""
import sys,json,itertools,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261009_round17_interaction_trace_certificate as m
def test_doublon_projection_formula_by_direct_two_boson_matrix():
 n=4
 A=np.zeros((n,n),dtype=complex)
 for x,y,z in [(0,1,complex(.6,.8)),(1,2,1),(2,3,1),(3,0,1)]:
  A[x,y]=z;A[y,x]=z.conjugate()
 states=list(itertools.combinations_with_replacement(range(n),2))
 loc={pair:i for i,pair in enumerate(states)}
 D=np.zeros((len(states),len(states)),dtype=complex)
 for col,(i,j) in enumerate(states):
  occ={i:2} if i==j else {i:1,j:1}
  for x,nx in occ.items():
   for y in range(n):
    if not A[y,x]:continue
    bag=[i,j];bag.remove(x);bag.append(y)
    row=loc[tuple(sorted(bag))]
    D[row,col]+=math.sqrt(nx*(occ.get(y,0)+1))*A[y,x]
 rows=[loc[(x,x)] for x in range(n)]
 q=np.diag([int(i==j) for i,j in states]).astype(complex)
 Ap=[np.linalg.matrix_power(A,k) for k in range(7)]
 G=[]
 for order in range(7):
  expected=np.linalg.matrix_power(D,order)[np.ix_(rows,rows)]
  g=sum(math.comb(order,k)*(Ap[k]*Ap[order-k]) for k in range(order+1))
  assert np.allclose(g,expected,atol=1e-9)
  G.append(g)
 for order in (4,6):
  coeff2=sum(np.trace(np.linalg.multi_dot([q if i in slots else D for i in range(order)]))
   for slots in itertools.combinations(range(order),2))
  small=order/2*sum(np.trace(G[a]@G[order-2-a]) for a in range(order-1))
  assert np.allclose(small,coeff2,atol=1e-8)
def test_native_five_orbit_witnesses_two_primes():
 from w33_20261008_5state_ritz import geometry
 edges,*_=geometry()
 reps=json.loads((ROOT/"data/w33_20261009_PSp_orbits_isotropic_triplets.json").read_text())["orbits"]
 original_mod,original_max=m.MOD,m.NMAX
 try:
  m.NMAX=20
  for prime in (1000003,1000033):
   m.MOD=prime
   rows=[m.coeffs_for_orbit(edges,o["representative"]) for o in reps]
   linear=[r[0] for r in rows]
   onebody=[r[2] for r in rows]
   assert len({tuple(sorted(s.items())) for s in onebody})==1
   assert len({(s["17"],s["19"]) for s in linear})==5
   assert len({s["17"] for s in linear})>1
   expected_17 = ([438086,438086,110922,221378,327630] if prime==1000003 else [146937,146937,525553,328325,344165])
   expected_19 = ([466015,404698,14902,764696,185564] if prime==1000003 else [70412,7637,26776,920814,645036])
   assert [s["17"] for s in linear] == expected_17
   assert [s["19"] for s in linear] == expected_19
 finally:
  m.MOD,m.NMAX=original_mod,original_max
