"""String necessary selection-rule MILP for all 16 three-singlet
holomorphic integer charge witnesses found in round11 discovery.

Uses full nine rational U1 charges AND actual orbifolder Pass11797
nonR[6,3,2,2] and corrected R[6,3,2] residues, with optional
old support charge-neutral mesons x=(n9,n54), y=(n37,n38).
They change R charges while carrying zero U1 charge.

THIS IS ONLY THE RECOVERED DISCRETE-CHARGE SELECTION FILTER:
space-group Rule5 gamma, oscillator and actual CFT amplitudes, full
F-flatness may forbid remaining monomials. Exponent search bounded
by 72 for each charged field and x<=2,y<=5 (exhaust modular cycles).
Every positive witness rechecked with source Pass11797 selection().
"""
import sys,json,math
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
from w33_20261009_three_even_singlets_integer_search import FI
NEUTRAL=[['n_9','n_54'],['n_37','n_38']]
def make_solver(charges,fields,extranames):
 names=FI+list(extranames);gen=[[n] for n in names]+NEUTRAL
 assert len(gen)==10
 # all rational values scaled by common integer 6*charge_den
 vals=[]
 for keys in gen:
  qvec=[sum((charges[n][j] for n in keys),F(0)) for j in range(9)]
  nr=[sum((F(fields[n]['nonR'][j]) for n in keys),F(0)) for j in range(4)]
  rr=[sum((P.corrected_r(fields[n])[j] for n in keys),F(0)) for j in range(3)]
  vals.append(qvec+nr+rr)
 scale=math.lcm(*(x.denominator for col in vals for x in col))
 assert scale>=1
 orders=[6,3,2,2,6,3,2]
 constraint=np.zeros((16,17),dtype=float)
 for j,col in enumerate(vals):
  constraint[:,j]=[int(x*scale) for x in col]
 for j,ord_ in enumerate(orders):
  constraint[9+j,10+j]=-scale*ord_
 low=np.r_[np.zeros(10),np.full(7,-10000.)]
 high=np.r_[np.full(8,72.),np.array([2.,5.]),np.full(7,10000.)]
 c=np.r_[np.ones(8),np.array([2.,2.]),np.zeros(7)]
 return names,gen,constraint,scale,c,low,high
def solve_target(target,fields,charges,setup):
 names,gen,mat,scale,c,lo,hi=setup
 tar=[sum((charges[n][j] for n in target),F(0)) for j in range(9)]
 tar +=[sum((F(fields[n]['nonR'][j]) for n in target),F(0)) for j in range(4)]
 tar +=[sum((P.corrected_r(fields[n])[j] for n in target),F(0)) for j in range(3)]
 goal=[-int(x*scale) for x in tar]
 for i in range(3):goal[13+i]-=scale
 result=milp(c,integrality=np.ones(17),bounds=Bounds(lo,hi),
   constraints=LinearConstraint(mat,goal,goal),
   options={'time_limit':2.,'mip_rel_gap':0.})
 if result.status!=0 or result.x is None:return None,result.status
 z=np.rint(result.x).astype(np.int64)
 assert np.max(abs(mat@z-np.array(goal)))==0
 actual=list(target)
 for p,g in zip(z[:10],gen):actual+=g*int(p)
 assert P.selection(actual,fields),(names,target,z[:10])
 return dict(degree=int(c@z),charged_exponents={names[i]:int(z[i]) for i in range(8) if z[i]},
    neutral_x_power=int(z[8]),neutral_y_power=int(z[9]),
    full_monomial_fields=actual),result.status
def certificate():
 raw,prior,fields,support,charges=P.load()
 seeds=json.load(open(ROOT/'data/w33_20261009_three_even_singlets_integer_search.json'))['triple_up_rank3_integer_witnesses']
 basis=json.load(open(ROOT/'data/w33_pass11793_order_four_matter_action.json'))['candidate_three_family_Higgs_basis']
 UP=[(a,b,basis['H_u'][0]) for a in basis['Q'] for b in basis['u_c']]
 down=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11799']['mass_sectors']['d']
 COL=[(a,b) for a in down['rows'] for b in down['columns']]
 output=[]
 for idx,entry in enumerate(seeds):
  keys=entry['triple']
  setup=make_solver(charges,fields,keys)
  u=[];unres=0
  for i,target in enumerate(UP):
   hit,status=solve_target(target,fields,charges,setup)
   if hit:u.append(dict(target_index=i,target=list(target),**hit))
   elif status not in (2,):unres+=1
  uids={r['target_index'] for r in u}
  mu=[[int(3*i+j in uids) for j in range(3)] for i in range(3)]
  urank=P.matching_rank(mu)
  crec=[];crank=None
  if urank>=2:
   for i,target in enumerate(COL):
    hit,status=solve_target(target,fields,charges,setup)
    if hit:crec.append(dict(target_index=i,target=list(target),**hit))
    elif status not in (2,):unres+=1
   ids={r['target_index'] for r in crec}
   mc=[[int(10*i+j in ids) for j in range(10)] for i in range(7)]
   crank=P.matching_rank(mc)
  output.append(dict(triple=keys,up_rank_after_integer_nonR_R=urank,
    selected_up_witnesses=u,colored_rank_after_R_when_up_rank2plus=crank,
    selected_colored_witnesses=crec,undecided_MILP=unres))
  print('R FILTER',idx+1,'up',urank,'color',crank,'undecided',unres,flush=True)
 hist=dict(Counter(str(x['up_rank_after_integer_nonR_R']) for x in output))
 return dict(status='PASS',tested_triples=len(output),triple_integer_U1_rank3_before_R=len(seeds),
   up_rank_after_R_histogram=hist,
   candidates_with_up_rank3_after_R=[x for x in output if x['up_rank_after_integer_nonR_R']==3],
   unresolved_MILP=sum(x['undecided_MILP'] for x in output),results=output,
   sufficient_for_actual_physics=False,
   theorem='Every retained positive witness is exactly U1 neutral, has nonnegative integral charged/neutral insertion powers, and passes Pass11797 corrected R/nonR necessary selection. These are NOT sufficient for actual string superpotential coupling, hidden fixed-point lattice or F-flatness.',
   search_boundaries='Charged exponents <=72 per field, neutral meson x<=2,y<=5 exhaust their R periodicities, quotient residue multipliers bounded +/-10000, each MILP allowed 2s. Negative cases are bounded search only.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_three_singlet_corrected_R_screen.json').write_text(json.dumps(d,separators=(',',':'))+'\n')
 print('R COMPLETE',d['up_rank_after_R_histogram'],'unresolved',d['unresolved_MILP'])
