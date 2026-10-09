"""Necessary corrected R/nonR cubic-coupling structure for all
16 heterotic singlet-support candidates; exact charge arithmetic.

For F_{n81}, find EVERY degree<=2 support insertion monomial
n81*(VEV_i VEV_j), including repeated powers and all old FI
support plus three added singlets. Require all nine exact U1
charges zero and Pass11797 corrected selection. Search uses
the exact rational field q; no optimization or truncated degree
heuristic at degree2. Direct finite source C-coupling availability
separately noted, never asserted to give amplitude.

If unique lowest-degree term n81*n17*n82, conditional small-field
F-flatness obstruction holds in a uniformly scaled analytic family
only when coefficient nonzero and no tuned cancellations from
terms of the SAME order. Additional degree>=4 terms cannot cancel
the leading homogeneous coefficient along a fixed generic ray.

Model FI backgrounds do not necessarily admit scaling to zero
because of anomalous D FI; the scaling theorem is conditional.
"""
import json,sys,itertools
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
def certificate():
 raw,prior,fields,support,q=P.load()
 data=json.loads((ROOT/'data/w33_20261009_three_singlet_corrected_R_screen.json').read_text())['results']
 allcases=[]
 for row in data:
  triple=row['triple']
  avail=sorted(set(support)|set(triple))
  target='n_81'
  solutions=[]
  for n in avail:
   for m in avail:
    if n>m:continue
    fields3=[target,n,m]
    total=[sum((q[f][j] for f in fields3),F(0)) for j in range(9)]
    if all(z==0 for z in total) and P.selection(fields3,fields):
     solutions.append(fields3)
  allcases.append(dict(triple=triple,n81_is_VEV=('n_81' in avail),
     exact_cubic_necessary_monomials=solutions,number_cubic_necessary_monomials=len(solutions)))
 hist=dict(Counter(str(z['number_cubic_necessary_monomials']) for z in allcases))
 expected=['n_81','n_17','n_82']
 assert all(expected in x['exact_cubic_necessary_monomials'] for x in allcases)
 return dict(status='PASS',supports=16,
  exact_degree3_monomial_histogram=hist,
  all_supports=allcases,
  known_cubic_n81_n17_n82_present_in_all=True,
  exact_source_recovered_necessary_rule='Each cubic field multiset has all nine exact U1 charges zero and corrected gamma-aware R and nonR passes, without invoking finite degree exports or MILP.',
  formal_F_obstruction='If n81*n17*n82 is the only allowed leading cubic and its worldsheet coefficient lambda !=0, then along any field scaling VEV=epsilon*v with v17*v82 !=0, F81=lambda*epsilon²*v17*v82+O(epsilon³) cannot vanish for all sufficiently small nonzero epsilon. This is an order-by-order analytic statement, not global F-flatness.',
  limitation='Additional genuine worldsheet selection could forbid the cubic, and other terms may cancel at finite VEV. FI D-term may not allow epsilon->0 scaling; full CFT coefficients, constructing elements, nondiscrete rules, non-Abelian D/F flatness remain unavailable.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_heterotic_n81_cubic_census.json').write_text(json.dumps(d,indent=2)+'\n')
 print('HETEROTIC CUBIC',d['exact_degree3_monomial_histogram'],[(x['triple'],x['number_cubic_necessary_monomials']) for x in d['all_supports']])
