"""Round16: exhaustive physical-field charge twins in the frozen
176-state actual Z6-II benchmark; R/oscillator selection firewall.
Same all nine U1 charges, twist, G, fixed-point translations does
not imply equal corrected-R selection or worldsheet amplitudes.

Includes explicit n81/n83 swap on the known n17*n82 cubic.
"""
import json,sys
from pathlib import Path
from collections import defaultdict,Counter
from itertools import combinations
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
def certificate():
 raw,prior,fields,support,q=P.load()
 def key(f):return (tuple(f['q']),int(f['k']),tuple(f['G']),tuple(f['fixed_point_translation']))
 groups=defaultdict(list)
 for name,f in fields.items():groups[key(f)].append(name)
 twins=[sorted(names) for names in groups.values() if len(names)>1]
 pairs=list(sum(([list(z) for z in combinations(ns,2)] for ns in twins),[]))
 type_diff=Counter()
 for n,m in pairs:
  a,b=fields[n],fields[m]
  type_diff['oscillator_count_different']+=int(a['oscillator_count']!=b['oscillator_count'])
  type_diff['corrected_R_different']+=int(P.corrected_r(a)!=P.corrected_r(b))
  type_diff['nonR_different']+=int(a['nonR']!=b['nonR'])
  type_diff['weights_different']+=int(a['weights']!=b['weights'])
 assert sorted(['n_81','n_83']) in twins
 others=['n_17','n_82']
 contrast={}
 for n in ('n_81','n_83'):
  f=fields[n]
  mono=[n,*others]
  charge=[str(sum(q[name][j] for name in mono)) for j in range(9)]
  contrast[n]=dict(cubic_fields=mono,charge_sum=charge,
   necessary_corrected_R_nonR=P.selection(mono,fields),
   corrected_R=[str(z) for z in P.corrected_r(f)],
   oscillator_count=f['oscillator_count'],
   fixed_point_translation=f['fixed_point_translation'])
 assert contrast['n_81']['necessary_corrected_R_nonR'] and not contrast['n_83']['necessary_corrected_R_nonR']
 assert contrast['n_81']['charge_sum']==['0']*9 and contrast['n_83']['charge_sum']==['0']*9
 return dict(status='PASS',total_fields=len(fields),
   distinct_full_signature_groups=len(groups),groups_with_twins=len(twins),
   twin_pairs=len(pairs),twin_group_size_histogram=dict(Counter(str(len(ns)) for ns in twins)),
   twin_difference_stats=dict(type_diff),
   complete_twin_groups=twins,
   benchmark_cubic_contrast=contrast,
   theorem='Field-name equivalence under q,k,G and fixed_point_translation is not equivalence under corrected R/oscillator data. Exhaustive source-anchored grouping and the n81 vs n83 cubic demonstrate precisely where naive charge-only Yukawa counting fails.',
   limitations='Even passing R and fixed point congruences does not prove nonzero string worldsheet coupling; full constructing elements, space group, Rule4/5/6, instantons and FI-corrected F/D flatness remain open.')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_charge_twins_all176.json').write_text(json.dumps(z,indent=2)+'\n')
 print('HETEROTIC TWINS',z['groups_with_twins'],z['twin_pairs'],z['twin_difference_stats'])
