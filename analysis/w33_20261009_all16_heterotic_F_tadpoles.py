"""Necessary-rule conditional F-term danger audit for ALL 16
integer-compatible tri-singlet Higgs candidate supports.

Full Pass11797 field metadata + recovered gamma-corrected R/nonR.
For each of 16 supports, enumerate parity-even U1Y-zero fully
non-Abelian singlet outsiders X, solve integer holomorphic
W = X*VEVs with FI5, additions3 and neutral x,y.
Each positive witness gives a possible F_X tadpole, NOT a nonzero
CFT amplitude. All possible outsider F terms plus support F
terms remain to be computed.

Special n81*n17*n82 is the pre-existing low-degree necessary
term from Pass11797, present for every support as a monomial
on the enlarged field universe; if its actual coefficient is
nonzero, it demands cancellation of F equations wherever
n17,n82 are nonzero (whether n81 VEV or not).
"""
from pathlib import Path
from collections import Counter
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
import w33_20261009_three_singlet_corrected_R_screen as S
def certificate():
 raw,prior,fields,support,charges=P.load()
 orig=json.loads((ROOT/'data/w33_20261009_three_singlet_corrected_R_screen.json').read_text())['results']
 parity=prior['all176_field_parities']
 outsiders=[n for n,f in fields.items() if f['dim']=='1,1,1,1' and charges[n][1]==0 and parity[n]==0]
 assert P.selection(['n_81','n_17','n_82'],fields)
 results=[]
 for row in orig:
  triple=row['triple'];VEV=set(support)|set(triple)
  setup=S.make_solver(charges,fields,triple)
  candidates=[];undecided=[]
  for n in outsiders:
   if n in VEV:continue
   witness,status=S.solve_target([n],fields,charges,setup)
   if witness:candidates.append(dict(outside=n,degree=witness['degree'],charged=witness['charged_exponents'],x=witness['neutral_x_power'],y=witness['neutral_y_power']))
   elif status not in (2,):undecided.append([n,status])
  assert not undecided
  results.append(dict(triple=triple,n_parity_even_outside_singlets_tested=len([n for n in outsiders if n not in VEV]),
    n_F_tadpole_necessary_candidates=len(candidates),min_total_exponent_degree=min([x['degree'] for x in candidates],default=None),
    previously_known_n81_n17_n82_candidate_status='n81 is a positive VEV field' if 'n_81' in VEV else ('n81 outsider, F81 dangerous IF coefficient nonzero'),
    candidate_mononomials=sorted(candidates,key=lambda x:(x['degree'],x['outside']))))
  print('F TERMS',len(results),triple,'outsider',len(candidates),flush=True)
 return dict(status='PASS',candidate_supports=len(results),
  histogram_num_tadpole_possible_outsiders=dict(Counter(str(x['n_F_tadpole_necessary_candidates']) for x in results)),
  full_results=results,
  conditional_F_n81='For all supports n17,n82 are nonzero; the earlier recognized necessary monomial lambda*n81*n17*n82 implies a nonzero contribution lambda*n17*n82 to F81. When n81 condenses, F17/F82 also receive lambda terms. This is a conditional obstruction only if the CFT coefficient lambda is generated and higher-degree contributions fail to cancel.',
  true_proof_boundary='No F-flatness theorem, no nonzero lambda amplitude, no complete worldsheet/Rule4/5/6 test. The candidate counts are U1 and corrected discrete R/nonR holomorphic integer necessary masks, with charged powers bounded72. Nonsinglet outsider F terms not enumerated.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_all16_heterotic_F_tadpoles.json').write_text(json.dumps(d,indent=2)+'\n')
 print('FINISHED',d['histogram_num_tadpole_possible_outsiders'])
