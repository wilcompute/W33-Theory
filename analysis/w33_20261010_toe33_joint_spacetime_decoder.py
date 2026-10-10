"""Round33 joint sparse-data-event space-time decoder on native W33 checks.

Batch MAP-like greedy: candidate ONE DATA Pauli insertion at a given
round changes *all future reports* across its *entire correlated check
support*. Compare binomial ternary likelihood + prior event cost.
Distinct from independent-check filtering; not global ML, no gates.
"""
from pathlib import Path
import json,sys,math,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep,logical_ok
from w33_20261009_toe27_qutrit_ideal_decoder import Radius3
from w33_20261010_toe32_phenom_temporal_decoder import filter_checks
OUT=ROOT/'data/w33_20261010_toe33_joint_spacetime_decoder.json'
def patterns(HZ,HX):
 base=[]
 for kind,H,offset in (('X',HZ,0),('Z',HX,80)):
  for j in range(160):
   support=np.flatnonzero(H[:,j])+offset
   for sign in (1,2):
    val=(np.asarray(H[:,j][support-offset],dtype=np.int16)*sign)%3
    base.append((kind,j,sign,support,val))
 assert len(base)==640
 W=max(len(p[3]) for p in base)
 idx=np.zeros((640,W),dtype=np.int16)
 shifts=np.zeros((640,W),dtype=np.int16)
 for i,(_,_,_,s,v) in enumerate(base):
  idx[i,:len(s)]=s;shifts[i,:len(s)]=v
 return base,idx,shifts
def decode_time(history,idx,shifts,pd,pm,max_events=8):
 n,ncheck=history.shape
 predicted=np.zeros((n,ncheck),dtype=np.int16)
 llr=math.log((1-pm)/(pm/2))
 prior=math.log((1-pd)/(pd/2))
 selections=[]
 for turn in range(max_events):
  gains=np.zeros((n,len(idx)),dtype=np.int16)
  for t in range(n):
   prior_values=predicted[t,idx]
   observed=history[t,idx]
   edited=(prior_values+shifts)%3
   gains[t]=np.sum((prior_values!=observed).astype(np.int16)-
                    (edited!=observed).astype(np.int16),axis=1)
  total=np.cumsum(gains[::-1],axis=0)[::-1]
  t,j=np.unravel_index(int(np.argmax(total)),total.shape)
  gain=int(total[t,j])
  if gain*llr<=prior+1e-10:break
  sites=idx[j,shifts[j]!=0];values=shifts[j,shifts[j]!=0]
  predicted[t:,sites]=(predicted[t:,sites]+values)%3
  selections.append((int(t),int(j),gain))
 return predicted[-1],selections
def run(trials=180):
 C,D,f,HZ,HX=prep()
 dx=Radius3(HZ);dz=Radius3(HX)
 idxbase,ids,vals=patterns(HZ,HX)
 weights=np.count_nonzero(np.vstack((HZ,HX)),axis=1)
 rng=np.random.default_rng(320320)
 rows=[]
 for pd,pm,T in ((.0005,.01,5),(.0005,.02,5),(.0005,.04,5)):
  stat=collections.Counter()
  for trial in range(trials):
   x=np.zeros(160,dtype=np.int16);z=np.zeros(160,dtype=np.int16);obs=[]
   true_events=0
   for tick in range(T):
    for arr in (x,z):
     sites=np.flatnonzero(rng.random(160)<pd)
     true_events+=len(sites)
     if len(sites):arr[sites]=(arr[sites]+rng.integers(1,3,size=len(sites)))%3
    true=np.concatenate(((HZ@x)%3,(HX@z)%3))
    errors=np.zeros(159,dtype=np.int16)
    bad=np.flatnonzero(rng.random(159)<pm)
    if len(bad):errors[bad]=rng.integers(1,3,size=len(bad))
    obs.append((true+errors)%3)
   observed=np.asarray(obs,dtype=np.int16)
   true=np.concatenate(((HZ@x)%3,(HX@z)%3))
   raw=observed[-1];individual=filter_checks(observed,weights,pd,pm)
   joint,events=decode_time(observed,ids,vals,pd,pm)
   stat['true_events']+=true_events;stat['estimated_events']+=len(events)
   for name,candidate in [('raw',raw),('individual',individual),('joint',joint),('ideal',true)]:
    stat[name+'_mismatched_checks']+=int(np.count_nonzero(candidate!=true))
    estx,_=dx.decode(candidate[:80]);estz,_=dz.decode(candidate[80:])
    if not logical_ok(x,z,estx,estz,C,D,f):stat[name+'_logical_fail']+=1
  rows.append(dict(p_data_per_channel_round=pd,p_report=pm,rounds=T,trials=trials,
   true_data_events=stat['true_events'],joint_selected_events=stat['estimated_events'],
   mismatched_check_values_total={k:stat[k+'_mismatched_checks'] for k in ('raw','individual','joint','ideal')},
   logical_failures={k:stat[k+'_logical_fail'] for k in ('raw','individual','joint','ideal')}))
  print('ROUND33 DECODER',pm,'checks',rows[-1]['mismatched_check_values_total'],
   'failures',rows[-1]['logical_failures'],flush=True)
 result=dict(status='PASS',code='[[160,1,8]]_3',
  hypothesis='One or a few Pauli X/Z data events per round. Joint sparse-greedy selector scores each candidate error against ALL its affected stabilizers and all future time bins, using actual W33 syndrome columns, rather than independent check filters.',
  data_event_prior='Each channel each data qudit error p=0.0005, nonzero F3 Pauli ± equally likely; log event/no-event ratio log((1-pd)/(pd/2)). Readout error probability pm, wrong ternary outcome symmetric; log correct/wrong ratio log((1-pm)/(pm/2)).',
  greedy_scope='Select one event-time-channel-edge-amplitude candidate with positive log posterior improvement, update entire future predicted check history; stop at no gain or 8 events. This is NOT global maximum likelihood, circuit-level GHZ/CZ propagation, joint full data error probability, or detector-matching decoder with actual gates.',
  outcomes=rows,seed=320320,
  reproducibility='Uses exact Round32 RNG stream and model, compare raw, Round32 independent ternary HMM, joint sparse time-event selector and ideal true syndrome on the SAME 180 trials per setting.',
  caution='Finite seeded Monte Carlo. Compare all channels and stabilizer-equivalent logical recovery; no threshold or physical universal quantum device.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
