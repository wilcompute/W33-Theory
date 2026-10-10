"""Round34 verified GHZ/CZ quantum-Pauli-frame multi-round simulator.

Exact qutrit SUM/CZ Pauli conjugation for cat ancillas, 159 checks,
independent 2-qudit faults after cat fanout, parity-verification and
data CZ, noisy verifier reports and final cat X measurements.
Tracks data-frame errors and time history for Round33 joint decoder.

CAVEAT: initial |+> and |0> cat states are ideal, local F transforms
are ideal, postselection retry is idealized, no noisy detector decoder
over rejected attempts, no leakage and no quantitative FT threshold.
"""
from pathlib import Path
import sys,json,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe28_qutrit_noisy_extraction import prep,logical_ok,nontrivial
from w33_20261009_toe27_qutrit_ideal_decoder import Radius3
from w33_20261010_toe33_joint_spacetime_decoder import patterns,decode_time
from w33_20261009_toe30_verified_cat_CZ import sum_cnot
OUT=ROOT/'data/w33_20261010_toe34_verified_cat_multiround_circuit.json'
def full_check(row,kind,x,z,rng,pg,pver,pm,stats,max_attempts=25):
 sites=np.flatnonzero(row);h=[int(row[j]) for j in sites];w=len(h)
 for attempt in range(max_attempts):
  ax=np.zeros(2*w-1,dtype=np.int16)
  az=np.zeros(2*w-1,dtype=np.int16)
  for j in range(1,w):
   sum_cnot(ax,az,0,j,1);stats['fanout_gates']+=1
   if rng.random()<pg:
    a,b,c,d=nontrivial(rng)[0]
    ax[0]=(ax[0]+a)%3;az[0]=(az[0]+b)%3
    ax[j]=(ax[j]+c)%3;az[j]=(az[j]+d)%3
    stats['fanout_faults']+=1
  for j in range(1,w):
   v=w+j-1
   for c,exp in ((0,1),(j,-1)):
    sum_cnot(ax,az,c,v,exp);stats['verify_gates']+=1
    if rng.random()<pg:
     a,b,cc,d=nontrivial(rng)[0]
     ax[c]=(ax[c]+a)%3;az[c]=(az[c]+b)%3
     ax[v]=(ax[v]+cc)%3;az[v]=(az[v]+d)%3
     stats['verify_faults']+=1
  reject=False
  for v in range(w,2*w-1):
   report=int(ax[v])
   if rng.random()<pver:report=(report+int(rng.integers(1,3)))%3;stats['verifier_readout_faults']+=1
   if report:reject=True
  stats['cat_attempts']+=1
  if not reject:break
  stats['cat_rejections']+=1
 else:raise RuntimeError('cat verification exceeded attempts')
 syndrome=0
 for a,site in enumerate(sites):
  site=int(site);q=h[a]
  if kind=='WilsonZ':syndrome=(syndrome+q*int(x[site]))%3
  else:syndrome=(syndrome+q*int(z[site]))%3
  # CZ conjugation for cat X -> data Z in temporary Z basis.
  if ax[a]:
   if kind=='WilsonZ':z[site]=(z[site]+q*int(ax[a]))%3
   else:x[site]=(x[site]+q*int(ax[a]))%3
  stats['data_CZ_gates']+=1
  if rng.random()<pg:
   dx,dz,cx,cz=nontrivial(rng)[0]
   if kind=='WilsonZ':
    x[site]=(x[site]+dx)%3;z[site]=(z[site]+dz)%3
   else:
    # Fourier-conjugated frame: X'~Z, Z'~X^-1;
    # signs of physical X check are calibrated to h.
    x[site]=(x[site]+dz)%3;z[site]=(z[site]-dx)%3
   ax[a]=(ax[a]+cx)%3;az[a]=(az[a]+cz)%3
   stats['data_CZ_faults']+=1
  # ancilla logical Z changes X_all eigenvalue; calibrate - sign
 syndrome=(syndrome-int(np.sum(az[:w])))%3
 for a in range(w):
  if rng.random()<pm:
   syndrome=(syndrome+int(rng.integers(1,3)))%3
   stats['cat_final_readout_faults']+=1
 return int(syndrome)
def run(trials=60):
 C,D,f,HZ,HX=prep();dx=Radius3(HZ);dz=Radius3(HX)
 pats,idx,shifts=patterns(HZ,HX)
 rng=np.random.default_rng(340034);scenarios=[]
 for pg,pv,pm in ((0.,0.,0.),(.0001,.001,.001),(.0004,.003,.003)):
  stat=collections.Counter()
  for tr in range(trials):
   x=np.zeros(160,dtype=np.int16);z=np.zeros(160,dtype=np.int16)
   history=[]
   for tick in range(3):
    readings=[]
    for kind,H in (('WilsonZ',HZ),('GaussX',HX)):
     for row in H:
      readings.append(full_check(row,kind,x,z,rng,pg,pv,pm,stat))
    history.append(readings)
   y=np.asarray(history,dtype=np.int16)
   truth=np.concatenate(((HZ@x)%3,(HX@z)%3))
   raw=y[-1]
   joint,_=decode_time(y,idx,shifts,pd=max(pg*.9,1e-6),pm=max(pm*2,.0001))
   for name,estimated in (('raw',raw),('joint',joint),('ideal',truth)):
    stat[name+'_wrong_final_syndrome']+=int(np.count_nonzero(estimated!=truth))
    a,_=dx.decode(estimated[:80]);b,_=dz.decode(estimated[80:])
    stat[name+'_logical_fail']+=int(not logical_ok(x,z,a,b,C,D,f))
  row=dict(two_qutrit_Pauli_fault_probability_after_each_gate=pg,
   verifier_ternary_readout_error_probability=pv,
   each_cat_final_X_readout_error_probability=pm,
   trials=trials,rounds=3,
   full_round_checks=159,
   logical_failures={k:stat[k+'_logical_fail'] for k in ('raw','joint','ideal')},
   wrong_final_syndrome_totals={k:stat[k+'_wrong_final_syndrome'] for k in ('raw','joint','ideal')},
   circuit_event_totals={k:int(v) for k,v in stat.items() if not k.endswith('_logical_fail') and not k.endswith('_wrong_final_syndrome')})
  scenarios.append(row)
  print('CAT MULTI',pg,'logical',row['logical_failures'],'faults',sum(v for k,v in row['circuit_event_totals'].items() if k.endswith('_faults')),flush=True)
 assert scenarios[0]['logical_failures']=={'raw':0,'joint':0,'ideal':0}
 result=dict(status='PASS',code='[[160,1,8]]_3',
   noise_model='Independent uniform 80 nonidentity 2-qutrit Pauli faults after each cat fanout SUM, parity-verifier SUM and transversal data CZ; independent ternary verifier report flips and final individual cat X readout flips. All syndrome reports are recorded sequentially with potentially changing data errors, for three rounds.',
   check_count={'WilsonZ':80,'GaussX':79},data_CZ_gates_per_accepted_round=956,
   Fourier_basis_changes='Assumed IDEAL. Gauss X checks are modeled by transformed temporary basis, with physical data X↔Z frame mapping.',
   cat_input_states='Assumed ideal |+> root and |0> leaves and |0> verifier ancilla. Noise injected after gates, rather than all state preparation steps.',
   relative_gate_measurement='Physical Pauli frames propagate exactly through SUM/CZ, while syndrome readouts are ideal check eigenvalues at the time of each data-CZ interaction, modified by cat Z errors and stochastic X readout flips. Cat retries are performed before coupling to data.',
   outcomes=scenarios,
   ceiling='NOT a full fault-tolerant syndrome extraction theorem: two-fault noise accepted, ideal basis rotations, ideal cat source preparations, no measurement crosstalk or leakage, no detector-history decoder for rejected attempts, approximate greedy joint decoder. Seeded finite Monte Carlo does not yield threshold.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
