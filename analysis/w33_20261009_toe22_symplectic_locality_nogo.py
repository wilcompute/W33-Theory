"""Exact locality obstruction: full Sp4(3) plus F3^4 translations makes
any undirected translation-invariant uniform positive hopping on F3^4
either trivial or complete. No invariant four-axis nearest-neighbor torus.
"""
from pathlib import Path
import itertools,json,math
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe22_symplectic_locality_nogo.json'
def omega(x,y):
 return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def canon(v):
 for a in v:
  if a:return tuple(x*pow(a,-1,3)%3 for x in v)
 raise ValueError
def run():
 V=list(itertools.product(range(3),repeat=4))
 rays=sorted({canon(v) for v in V if any(v)})
 assert len(V)==81 and len(rays)==40
 base=(1,0,0,0);seen={base};queue=deque([base])
 while queue:
  x=queue.popleft()
  for a in rays:
   w=omega(x,a)
   for s in (1,2):
    y=tuple((x[i]+s*w*a[i])%3 for i in range(4))
    if y not in seen:seen.add(y);queue.append(y)
 assert len(seen)==80
 k=80
 def p(t):return (1+k*math.exp(-(k+1)*t/k))/(k+1)
 def dim(t):
  q=k*math.exp(-(k+1)*t/k)
  return 2*t*(k+1)/k*q/(1+q)
 values=[dict(t=t,heat=p(t),running_dimension=dim(t)) for t in (.25,1,2,4,8,20)]
 out={'status':'PASS','carrier':'F3^4 as 81-site affine translation group',
  'number_translation_states':81,'nonzero_translation_directions':80,
  'symplectic_nonzero_orbit_size':len(seen),
  'theorem':'Sp(4,3) acts transitively on ALL 80 nonzero vectors of F3^4 (direct BFS using 40 transvection generators). Every translation-invariant Cayley hopping graph invariant under full Sp4(3) is therefore either edgeless or complete K81: its nonzero displacement set must be a union of Sp-orbits, and there is only one nontrivial orbit. Any four-axis sparse lattice or finite 4D torus requires choosing a basis/axis orbit and BREAKS this symmetry, or a different representation/geometry.',
  'complete_graph_laplacian_eigenvalues':{'zero':1,'81_over_80':80},
  'heat_formula':'P(t)=(1+80 exp(-81t/80))/81 for normalized Laplacian',
  'samples':values,
  'family_extension':'For the natural Sp(4,q) action on affine Fq^4, Witt transitivity gives one orbit of all q^4-1 nonzero displacement vectors; full Sp-invariant translation hopping is likewise complete K_(q^4).',
  'prior':'Prior q-family Levi heat-kernel and Cartesian W33 power tests addressed different graphs. This new affine-translation locality obstruction concerns full unbroken Sp4 action.',
  'physical_boundary':'This does not forbid local Lorentzian physics if symplectic symmetry is broken, represented internally, gauge-redundant or implemented nonlinearly on an expanded carrier. It forbids only the naive fully symmetric translation Cayley kinetic construction.'}
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('SPACETIME',len(seen),'directions; complete K81',flush=True)
 return out
if __name__=='__main__':run()
