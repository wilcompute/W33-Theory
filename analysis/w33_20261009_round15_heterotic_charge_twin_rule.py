"""Exact orbifolder benchmark n81/n83 'charge twin' selection
firewall, full twisted-sector / fixed-point labeling, and
non-prime Z6-II necessary space-group congruences.

n81 and n83 share all nine U1 charges, the same twist sector
k=5, G data and constructing fixed-point translation. Different
oscillator counts and RQ vectors make their cubic couplings
to n17 n82 obey different corrected R rules. This is an
ACTUAL source-metadata selection difference, not a numerical
CFT amplitude.

Evaluate universally necessary Z6-II point/twist congruences
k_sum mod 6, SU3 integer translation mod3 and SO4 translation
mod2 (assuming conventional G2xSU3xSO4 lattice coordinates).
The k5+k2+k5 candidate passes these broad necessary filters,
but worldsheet Rules4/5/6, representatives of fixed-point
conjugacy classes, instanton saddles and actual lambda remain
unknown. No F-flatness no-go without amplitude.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,gzip,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
def charge_sum(ns,q):
 return [str(sum((q[n][i] for n in ns),F(0))) for i in range(9)]
def certificate():
 raw,prior,field,sup,q=P.load()
 a='n_81';b='n_83';fi=('n_17','n_82')
 assert q[a]==q[b] and field[a]['k']==field[b]['k']==5
 assert field[a]['fixed_point_translation']==field[b]['fixed_point_translation']
 assert field[a]['G']==field[b]['G']
 assert field[a]['oscillator_count']!=field[b]['oscillator_count']
 rows=[]
 for first in (a,b):
  names=[first,*fi]
  k=[int(field[n]['k']) for n in names]
  trans=[[F(z) for z in field[n]['fixed_point_translation']] for n in names]
  twos=[int(z)%2 for z in [sum(k[j]*trans[j][i] for j in range(3)) for i in (4,5)]]
  three=[int(sum(k[j]*trans[j][i] for j in range(3)))%3 for i in (2,3)]
  r=[sum(P.corrected_r(field[n])[i] for n in names) for i in range(3)]
  rres=[str((r[i]+1)%m) for i,m in enumerate((6,3,2))]
  row=dict(fields=names,point_twist_sum_mod6=sum(k)%6,
   hypercharge_and_eight_other_U1_exact_zero=(charge_sum(names,q)==['0']*9),
   source_raw_twist_sectors=k,source_fixed_point_translations=[[str(x) for x in vec] for vec in trans],
   SO4_Z2xZ2_necessary_residues=twos,SU3_Z3_necessary_residues=three,
   corrected_R_residues_for_superpotential=rres,
   corrected_R_nonR_passes=P.selection(names,field),
   oscillator_counts=[int(field[n]['oscillator_count']) for n in names])
  assert row['point_twist_sum_mod6']==0
  assert row['hypercharge_and_eight_other_U1_exact_zero']
  assert twos==[0,0] and three==[0,0]
  rows.append(row)
 assert rows[0]['corrected_R_nonR_passes'] and not rows[1]['corrected_R_nonR_passes']
 return dict(status='PASS',
   source_sha256=hashlib.sha256((ROOT/'data/w33_pass11797_full_benchmark_metadata.json.gz').read_bytes()).hexdigest(),
   distinct_orbifold='Z6-II cp2 Codex benchmark SM_20260917_1558, not parallel Z6-I SU9 family-level examples',
   exact_charge_twins=[a,b],twins_same_all_nine_U1_and_twist_and_fixed_point=True,
   discriminating_superpotential_triples=rows,
   conclusion='The n81 and n83 fields have indistinguishable nine Abelian charges and fixed-point translation, but their corrected R vectors/oscillator levels differ: n81*n17*n82 passes recorded necessary rules, n83*n17*n82 fails. Both pass simpler twist/point-lattice congruence checks. The actual n81 coupling amplitude remains entirely undetermined.',
   scope='Fixed-point congruences interpreted in conventional six-coordinate G2xSU3xSO4 basis and are only necessary, not complete space-group representative products. Oscillator Rules4/5/6 and actual CFT amplitudes not computed; cannot certify supersymmetric physical vacuum or nonzero lambda.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round15_heterotic_charge_twin_rule.json').write_text(json.dumps(d,indent=2)+'\n')
 print('HETEROTIC TWINS',[(r['fields'],r['corrected_R_residues_for_superpotential'],r['corrected_R_nonR_passes']) for r in d['discriminating_superpotential_triples']])
