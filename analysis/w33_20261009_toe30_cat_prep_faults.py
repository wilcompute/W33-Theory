"""Round30 exact qutrit GHZ fanout and transversal single-fault hooks.

Enumerate all nontrivial Pauli faults at each initialization, cat
fanout SUM and data SUM. Minimize data error support modulo measured
stabilizer. Does NOT certify the physical syndrome observable, flagged
cat verification, ancilla readout or repeated-round FT.
"""
from pathlib import Path
import json,sys,collections,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep
OUT=ROOT/'data/w33_20261009_toe30_cat_prep_singlefault.json'
PAULIS=[tuple((v//3**j)%3 for j in range(4)) for v in range(1,81)]
ONE=[(v%3,v//3) for v in range(1,9)]
def sum_gate(x,z,control,target,h):
 x[target]=(x[target]+h*x[control])%3
 z[control]=(z[control]-h*z[target])%3
def trial(h,kind,stage,location,pauli):
 w=len(h);ax=[0]*w;az=[0]*w;dx=[0]*w;dz=[0]*w
 if stage=='initial':
  x,z=pauli
  ax[location]=x;az[location]=z
  start_prep=1
 elif stage=='fanout':
  start_prep=location+2
  ax[0],az[0],ax[location+1],az[location+1]=pauli
 else:
  start_prep=w
 for leaf in range(start_prep,w):
  sum_gate(ax,az,0,leaf,1)
 if stage=='data':
  data,cat=location,location
  dx[data],dz[data],ax[cat],az[cat]=pauli
  start_data=location+1
 else:
  start_data=0
 for j in range(start_data,w):
  if kind=='WilsonZ':
   # SUM^h data control -> cat target
   ax[j]=(ax[j]+int(h[j])*dx[j])%3
   dz[j]=(dz[j]-int(h[j])*az[j])%3
  else:
   # SUM^h cat control -> data target
   dx[j]=(dx[j]+int(h[j])*ax[j])%3
   az[j]=(az[j]-int(h[j])*dz[j])%3
 raw=sum(x!=0 or z!=0 for x,z in zip(dx,dz))
 eff=min(sum(((dx[j]+(a*h[j] if kind=='GaussX' else 0))%3)!=0 or
             ((dz[j]+(a*h[j] if kind=='WilsonZ' else 0))%3)!=0 for j in range(w))
          for a in range(3))
 return raw,eff
def local(kind,h):
 w=len(h);counts=collections.Counter();worst=collections.defaultdict(int)
 for j in range(w):
  for xz in ONE:
   raw,eff=trial(h,kind,'initial',j,xz)
   counts[('initial',eff)]+=1;worst['initial']=max(worst['initial'],eff)
 for j in range(w-1):
  for f in PAULIS:
   raw,eff=trial(h,kind,'fanout',j,f)
   counts[('fanout',eff)]+=1;worst['fanout']=max(worst['fanout'],eff)
 for j in range(w):
  for f in PAULIS:
   raw,eff=trial(h,kind,'data',j,f)
   counts[('data',eff)]+=1;worst['data']=max(worst['data'],eff)
 return worst,counts
def run():
 C,D,f,W,G=prep()
 aggregates={}
 for typ,mat in [('WilsonZ',W),('GaussX',G)]:
  Wm=collections.defaultdict(int);count=collections.Counter()
  for row in mat:
   h=np.asarray(row)[np.flatnonzero(row)]
   maxs,cts=local(typ,h)
   for k,v in maxs.items():Wm[k]=max(Wm[k],v)
   count.update(cts)
  aggregates[typ]=dict(
   checks=len(mat),max_logical_equivalent_data_weight={k:int(v) for k,v in Wm.items()},
   fault_count_by_stage_and_effective_weight={f'{a}:{b}':int(v) for (a,b),v in sorted(count.items())},
   enumerated_single_faults=sum(count.values()))
  print('CAT30',typ,'n',len(mat),'max',dict(Wm),'faults',sum(count.values()),flush=True)
 # With a fanout cat for Wilson Z, the ancilla Z errors can only occur
 # on root and one leaf per single fanout gate Pauli error -> <=2 data Z.
 # For Gauss X, root X can spread broadly but global uniform X is
 # the Gauss stabilizer, and remaining support <=2 modulo that star.
 assert aggregates['WilsonZ']['max_logical_equivalent_data_weight']['fanout']<=2
 assert aggregates['GaussX']['max_logical_equivalent_data_weight']['fanout']<=2
 assert max(aggregates['WilsonZ']['max_logical_equivalent_data_weight'].values())<=2
 assert max(aggregates['GaussX']['max_logical_equivalent_data_weight'].values())<=2
 rec=dict(status='PASS',code='[[160,1,8]]_3',complete_check_count=159,
  exhaustive_Pauli_fault_enumeration=aggregates,
  qutrit_cat_resource_preparation='Prepare GHZ_w by root |+> and w-1 leaves |0>, then fanout SUM(root->leaf) for each leaf. Enumerate all 8 one-qutrit preparation Pauli errors for every cat input and all 80 nonidentity two-qutrit Pauli errors inserted after each fanout or transversal data-coupling SUM.',
  layout='Wilson Z checks: data controls, GHZ-cat targets; Gauss X checks: GHZ-cat controls, data targets. Ancilla-data operations transversal, one per cat qutrit. For each final data Pauli error, minimize support over multiplication by the measured check stabilizer. This tests hook *support*, NOT measurement correctness.',
  limitation='This does not demonstrate that the chosen GHZ state and data-CNOT directions correctly project the desired qutrit stabilizer eigenvalue! In particular global cat entanglement and final basis readout must be tested by a proper qutrit stabilizer/Clifford simulation. Cat verification, correlated measurement errors, multiple faults, detector history, and actual logical failure probability are missing. Thus no verified fault-tolerant measurement circuit or threshold.',
  scientific_context='Upgrades Round29 one-fault transversal-data-only statement to include fanout preparation errors and cat input errors at Pauli-frame level, conditional on the logical measurement scheme being validated separately.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
