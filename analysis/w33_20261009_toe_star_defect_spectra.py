"""TOE bridge application: what the FULL finite symplectic symmetry permits
as quadratic 'mass' operators on its irreducible 81 harmonic cycles.
Exact 160x160 K projector, all 80 single-star selectors, and all 3160
pair configurations; no claim physical masses or spontaneous selection.
"""
from pathlib import Path
from collections import defaultdict,Counter
import json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1081_1086_core import build_w33
from w33_pass1083_levi_frame_steinberg_intertwiner import levi_cycle_kernel
def main():
 pts,idx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33()
 assert len(flags)==160
 K,dist=levi_cycle_kernel(flags)
 assert np.array_equal(K@K,160*K)
 stars=[sorted(i for i,(p,l) in enumerate(flags) if p==v) for v in range(40)]
 stars += [sorted(i for i,(p,l) in enumerate(flags) if l==v) for v in range(40)]
 assert all(len(s)==4 for s in stars)
 for S in stars:
  Q=K[np.ix_(S,S)]
  assert np.array_equal(Q,108*np.eye(4,dtype=np.int64)-27*np.ones((4,4),dtype=np.int64))
 rels=defaultdict(list)
 rows={}
 for a in range(80):
  for b in range(a+1,80):
   if a<40 and b<40:
    typ='point_point_collinear' if any(a in L and b in L for L in lines) else 'point_point_far'
   elif a>=40 and b>=40:
    typ='line_line_intersect' if set(lines[a-40])&set(lines[b-40]) else 'line_line_skew'
   else:
    typ='point_line_incident' if a in lines[b-40] else 'point_line_nonincident'
   S=sorted(set(stars[a])|set(stars[b]))
   Q=K[np.ix_(S,S)]
   # Sign pattern K is exact, eigenval rational algebraic; charpoly is
   # computable in integers and invariant within each 2-point orbit.
   rvals=np.linalg.eigvalsh(Q/160)
   rounded=tuple(round(float(v),9) for v in rvals if v>1e-7)
   rels[typ].append((a,b,rounded,len(S)))
 for typ,rec in sorted(rels.items()):
  unique=sorted(set((v,k) for a,b,v,k in rec))
  assert len(unique)==1,(typ,len(unique),unique[:4])
  a,b,es,k=rec[0]
  S=sorted(set(stars[a])|set(stars[b]))
  Q=sp.Matrix(K[np.ix_(S,S)].tolist())
  z=sp.Symbol('z'); char=sp.factor(Q.charpoly(z).as_expr())
  rows[typ]=dict(count=len(rec),representative=[a,b],union_flag_count=k,
    nonzero_eigenvalues_of_two_star_harmonic_operator=es,
    characteristic_polynomial_of_integer_K_union=sp.sstr(char))
  print('DEFECT',typ,'count',len(rec),'eigen',es,'char',char,flush=True)
 assert sum(v['count'] for v in rows.values())==3160
 out=dict(status='PASS',harmonic_cycle_dimension=81,
  full_group_invariant_mass_nogo='The 81 real harmonic cycles form the complex irreducible Steinberg module of PSp(4,3), established in prior BT1688 / Pass20260901. By Schur lemma every exactly PSp-invariant complex-linear Hermitian quadratic mass operator on this module is scalar. Therefore unbroken full symmetry CANNOT produce multiple masses or choose 3 generations within these 81 modes. Breaking the symmetry or adding distinct representations/dynamics is necessary.',
  canonical_projector='The previous 160x160 signed chamber-distance matrix K satisfies K²=160K, K^T=K, rank(K)=81, so P=K/160 is the Euclidean projector onto the Levi 81 cycle space.',
  all80_single_stars={'count':80,'principal_block_exact':'K_{star,star}=108 I4-27 J4','nonzero_eigenvalue_of_P Pstar P':'27/40 repeated 3','remaining_harmonic_eigenvalue':'0 repeated 78'},
  all3160_distinct_vertex_pairs=rows,
  physical_interpretation='A CHOSEN point or line selector supports an exactly 3-dimensional quadratic deformation of the otherwise degenerate 81 harmonic sector. Two chosen selectors produce relation-dependent spectra with fixed algebraic ratios. These are conditional geometry-defined Hamiltonians, not derived particle masses. A dynamical symmetry-breaking potential must select the point/line for actual physics.',
  caution='A finite graph with a selected site and an arbitrary coefficient lambda is not a predictive mass/energy theory, and the 3 excited directions are not automatically the Standard Model generations.')
 (ROOT/'data/w33_20261009_toe_star_defect_spectra.json').write_text(json.dumps(out,indent=2)+'\n')
 print('MASS SELECTOR all80 and all3160 cert',flush=True)
if __name__=='__main__':main()
