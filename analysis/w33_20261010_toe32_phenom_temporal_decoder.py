"""TOE32 phenomenological noisy temporal syndrome filtering on [[160,1,8]]3.

Full 159 W33 check vectors, independent iid qutrit Pauli data
flips and imperfect ternary measurement reports; compare raw final
with per-check approximate temporal HMM, followed by existing
radius-3 exact data-only decoders.

NOT gate-level, cat verifier or true spacetime matching decoder.
"""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep,logical_ok
from w33_20261009_toe27_qutrit_ideal_decoder import Radius3
OUT=ROOT/'data/w33_20261010_toe32_phenom_temporal_decoder.json'
def filter_checks(reports,weights,pd,pm):
 nsteps,nchecks=reports.shape
 probs=np.zeros((nchecks,3),dtype=np.float64);probs[:,0]=1.
 for t in range(nsteps):
  rho=np.minimum(.49,weights*pd)
  prev=probs
  probs=(1.-rho[:,None])*prev+rho[:,None]*(1.-prev)/2
  observed=reports[t]
  emit=np.full((nchecks,3),pm/2,dtype=float)
  emit[np.arange(nchecks),observed]=1-pm
  probs*=emit
  probs/=probs.sum(axis=1,keepdims=True)
 return probs.argmax(axis=1).astype(np.int16)
def run(trials=180):
 C,D,f,HZ,HX=prep()
 dx=Radius3(HZ);dz=Radius3(HX)
 S=np.vstack((HZ,HX)).astype(np.int16)
 weights=np.count_nonzero(S,axis=1)
 rng=np.random.default_rng(320320)
 rows=[]
 for pd,pm,T in ((.0005,.01,5),(.0005,.02,5),(.0005,.04,5)):
  raw_bad=sm_bad=raw_fail=sm_fail=ideal_fail=0
  final_wrong_raw=final_wrong_hmm=0
  for trial in range(trials):
   x=np.zeros(160,dtype=np.int16);z=np.zeros(160,dtype=np.int16)
   obs=[]
   for tick in range(T):
    for arr in (x,z):
     flipped=np.flatnonzero(rng.random(160)<pd)
     if len(flipped):
      arr[flipped]=(arr[flipped]+rng.integers(1,3,size=len(flipped)))%3
    sx=(HZ@x)%3;sz=(HX@z)%3
    true=np.concatenate((sx,sz))
    error=np.zeros(len(true),dtype=np.int16)
    fidx=np.flatnonzero(rng.random(len(true))<pm)
    if len(fidx):error[fidx]=rng.integers(1,3,size=len(fidx))
    obs.append((true+error)%3)
   truth=np.concatenate(((HZ@x)%3,(HX@z)%3))
   observed=np.asarray(obs,dtype=np.int16)
   raw=observed[-1];filtered=filter_checks(observed,weights,pd,pm)
   final_wrong_raw+=int(np.count_nonzero(raw!=truth))
   final_wrong_hmm+=int(np.count_nonzero(filtered!=truth))
   raw_bad+=bool(np.any(raw!=truth));sm_bad+=bool(np.any(filtered!=truth))
   def recovered(guess):
    a,_=dx.decode(guess[:80]);b,_=dz.decode(guess[80:])
    return logical_ok(x,z,a,b,C,D,f)
   raw_fail+=not recovered(raw);sm_fail+=not recovered(filtered)
   ideal_fail+=not recovered(truth)
  rows.append(dict(p_data_per_channel_per_round=pd,p_measurement_per_check=pm,rounds=T,trials=trials,
   average_wrong_final_check_values_raw=final_wrong_raw/trials,
   average_wrong_final_check_values_temporal=final_wrong_hmm/trials,
   shots_with_any_wrong_check_raw=raw_bad,shots_with_any_wrong_check_temporal=sm_bad,
   logical_recovery_failures_raw=raw_fail,logical_recovery_failures_temporal=sm_fail,
   ideal_syndrome_recovery_failures=ideal_fail))
  print('TOE32 temporal',pm,'bad checks',final_wrong_raw,final_wrong_hmm,'logical fail',raw_fail,sm_fail,'ideal',ideal_fail,flush=True)
 assert all(r['average_wrong_final_check_values_temporal']<r['average_wrong_final_check_values_raw'] for r in rows)
 result=dict(status='PASS',model='5-round iid data-X/Z errors on 160 links (each channel probability pd, nonzero F3 Pauli uniform); 80 Wilson-Z+79 Gauss-X check reports independently incorrect with probability pm, shifted by ±1 equiprobably. Independent 3-state forward Bayesian filter per check with assumed symmetric change probability weight*pd; truth couples checks through same data errors, thus filter is APPROXIMATE, not exact MAP on code.',
  runs=rows,source_check_geometry='Native 80 weight8 and 79 weight4 rows of [[160,1,8]]_3',
  important_limit='Does not simulate GHZ/CZ gates, cat postselection, non-Pauli noise, coherent leakage, causal syndrome circuitry or fault-tolerant spacetime matching. Independently filtering check histories can output inconsistent measured syndromes, therefore decoder may still fail. Seeded finite Monte Carlo cannot establish noise threshold.',
  acceptance='Compared both reported syndrome accuracy and full radius3 decoder stabilizer-equivalent logical recovery, plus ideal-syndrome reference.')
 OUT.write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':run()
