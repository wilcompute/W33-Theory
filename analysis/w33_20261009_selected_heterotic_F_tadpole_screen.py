"""Heterotic selected 3-VEV supports: potential F-TERM TADPOLES.
A term W=c*X*monomial(VEV) with X outside chosen support
produces F_X=c*monomial(VEV) at X=0 (unless cancellations).
Use actual 176 benchmark data, exact U1 charge and corrected
R/nonR filters via previous Pass11797 selection.

For two highest-priority N83 supports, enumerate ALL parity-even
non-Abelian singlet outsiders; odd outsiders are parity excluded
as support is even, while nonsinglets need nontrivial invariant
contractions and are NOT tested. Exponents<=72 in MILP.
This is necessary-rule danger census, NOT proof couplings generated.
"""
import json,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
import w33_20261009_three_singlet_corrected_R_screen as S
def certificate():
 raw,prior,fields,support,charges=P.load()
 triads=[['n_51','n_79','n_83'],['n_65','n_79','n_83']]
 base=prior['all176_field_parities']
 outs=[n for n,f in fields.items() if f['dim']=='1,1,1,1' and charges[n][1]==0 and base[n]==0]
 out=[]
 for triple in triads:
  setup=S.make_solver(charges,fields,triple)
  hits=[];undecided=[]
  for n in outs:
   if n in set(support)|set(triple):continue
   record,status=S.solve_target([n],fields,charges,setup)
   if record:hits.append(dict(outside=n,**record))
   elif status!=2:undecided.append([n,status])
  assert not undecided,undecided
  out.append(dict(triple=triple,even_outside_singlets_checked=len(outs)-sum(n in set(support)|set(triple) for n in outs),
                  F_tadpole_rule_permitted_outsiders=len(hits),
                  shortest_necessary_tadpole_exponents=sorted(hits,key=lambda r:r['degree'])[:14],
                  full_permitted_outsider_list=[h['outside'] for h in hits]))
 return dict(status='PASS',source='Pass11797 complete 176-sector model, prior 13 VEV support, integer corrected-R three-singlet solver',
  selected_supports=out,
  interpretation='A positive integer holomorphic U1/R/nonR singlet insertion X*VEVs is a necessary-rule F_X tadpole candidate, not an actual amplitude. Unless physical coefficient is nonzero and not cancelled, cannot conclude failure of F-flatness.',
  caveats='Non-Abelian outsider F terms, fixed-point/space-group, oscillator, Rule4/5/6, actual coefficients and unrestricted degrees all untested. The source finite C catalogs from round12 show zero outsider one-field terms for these VEV supports, which is not exhaustive.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_selected_heterotic_F_tadpole_screen.json').write_text(json.dumps(d,indent=2)+'\n')
 print('FTERM SCREEN',[(x['triple'],x['even_outside_singlets_checked'],x['F_tadpole_rule_permitted_outsiders'],[(z['outside'],z['degree']) for z in x['shortest_necessary_tadpole_exponents'][:5]]) for x in d['selected_supports']])
