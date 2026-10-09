"""Complete source-native necessary cubic screen of the 176-field
Z6-II benchmark: point-group twist and exact antisymmetric contractions
of repeated identical commuting superfields.
No worldsheet vertex operators or instanton correlator in source.
"""
from pathlib import Path
import sys,json,math
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P

def field_mononomials():
 raw,prior,fields,support,q=P.load()
 names=sorted(fields);den=math.lcm(*(x.denominator for v in q.values() for x in v))
 vec=[tuple(int(x*den) for x in q[n]) for n in names];lookup=defaultdict(list)
 for i in range(len(vec)):
  for j in range(i,len(vec)):
   lookup[tuple(vec[i][z]+vec[j][z] for z in range(9))].append((i,j))
 neutral=[]
 for k,v in enumerate(vec):
  for i,j in lookup[tuple(-x for x in v)]:
   if j<=k:neutral.append((names[i],names[j],names[k]))
 return fields,neutral

def local_symmetrization_zero(m,fields):
 dims=[tuple(int(x) for x in fields[n]['dim'].split(',')) for n in m]
 # Distinct field names commute. Every SU2 invariant of two fundamental
 # doublets is epsilon_ab, hence identical field pair epsilon Phi Phi =0.
 reasons=[]
 for slot,name in ((1,'visible_SU2_antisymmetric_doublet'),(3,'hidden_SU2_antisymmetric_doublet')):
  ids=[i for i,d in enumerate(dims) if abs(d[slot])==2]
  if len(ids)==2 and m[ids[0]]==m[ids[1]]:reasons.append(name)
 # SU3 3^3 and 3bar^3 singlets require epsilon_abc. The epsilon kills
 # an identical pair of commuting fields.
 vals=[d[0] for d in dims]
 if len(set(vals))==1 and abs(vals[0])==3 and len(set(m))<3:
  reasons.append('SU3_triple_epsilon_identical_fields')
 # SU4 invariant 4*4*6 is anti in the 4s; identical 4 fields kill it.
 v4=[d[2] for d in dims]
 if sorted(map(abs,v4))==[4,4,6] and v4.count(4)>=2:
  ids=[i for i,d in enumerate(dims) if d[2]==4]
  if len(ids)==2 and m[ids[0]]==m[ids[1]]:reasons.append('SU4_4_4_6_antisym')
 if sorted(map(abs,v4))==[4,4,6] and v4.count(-4)>=2:
  ids=[i for i,d in enumerate(dims) if d[2]==-4]
  if len(ids)==2 and m[ids[0]]==m[ids[1]]:reasons.append('SU4_bar4_bar4_6_antisym')
 return reasons

def main():
 fields,neutral=field_mononomials()
 R=[m for m in neutral if P.selection(m,fields)]
 twist=[m for m in R if sum(fields[n]['k'] for n in m)%6==0]
 rejected_twist=[m for m in R if m not in set(twist)]
 vanished={','.join(m):local_symmetrization_zero(m,fields) for m in twist if local_symmetrization_zero(m,fields)}
 survivors=[m for m in twist if ','.join(m) not in vanished]
 print('HET',len(neutral),len(R),'pointgroup',len(twist),'antisymvanish',len(vanished),'candidates',len(survivors),flush=True)
 print('HET examples twist',rejected_twist[:5],'sym',list(vanished.items())[:8],flush=True)
 fkeys=set.union(*(set(v) for v in fields.values()))
 missing=['full_constructing_element_group_word','vertex_operator_pictures','worldsheet_instanton_actions','oscillator_polarization_vectors','gamma_eigenphase_full_sector']
 out=dict(status='PASS',frozen_model='Z6-II 176-field benchmark (distinct from parallel Z6-I Pass11818-11825)',field_count=len(fields),
  exact_nine_U1_charge_neutral_cubics=len(neutral),R_nonR_necessary=len(R),
  pointgroup_twist_sum0_mod6=len(twist),pointgroup_rejected=[list(m) for m in rejected_twist],
  forced_commuting_identical_field_antisymmetric_zeros=vanished,
  additional_antisymmetry_vanishing_count=len(vanished),
  remaining_necessary_not_sufficient_cubic_candidates=len(survivors),
  examples_remaining=[list(m) for m in survivors[:20]],missing_full_amplitude_metadata=missing,
  present_merged_field_metadata=sorted(fkeys),
  rule='Only gauge-neutral+corrected R/nonR+sum of twist k=0 mod6+necessary invariant tensor symmetry, not space-group product, full oscillator/gamma/instanton correlator. Identical chiral superfields commute; epsilon Phi Phi=0. No surviving amplitude is claimed nonzero.',
  synthesis='A failed necessary rule proves zero. Passing the finite rules never proves nonzero coupling; the frozen metadata cannot determine the complete complex CFT amplitude.')
 (ROOT/'data/w33_20261009_round20_heterotic_amplitude_obstructions.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
