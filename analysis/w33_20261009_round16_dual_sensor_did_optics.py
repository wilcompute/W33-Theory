"""Round16 blinded paired active/sham experiment with two synchronized
detectors and a negative-control reference, allowing pump/gate/route-
correlated downstream electronics shams common to both detectors.

Per pair choose independent z optical active order and r triple sign.
Observe fully clipped science S_{j,s} and reference C_{j,s}.
D_j=(S_j1-C_j1)-(S_j2-C_j2), score X=sum z_j r_j D_j.
Sharp null: untreated (S-C) potential differences independent of z.
If direct SWITCH-dependent mismatch science-minus-control per reading
<=eta and at most K arbitrary corrupted raw individual detector shots:
 |X| <= 2 eta M + 4T K + 4T sqrt(2 M ln(2/alpha))
with type-I alpha. Hoeffding bound derives because |D_j|<=4T.

The reference cancels only artifacts of similar detector response:
a science-only electronic leak above eta still breaks identification.
Synthetic controls, not physical optical evidence.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def threshold(M,T,eta,K,alpha):
 return 2*eta*M+4*T*K+4*T*math.sqrt(2*M*math.log(2/alpha))
def trial(seed,mode,M=8000,T=.15,eta=.0005,K=14,alpha=.01):
 rng=np.random.default_rng(seed)
 z=rng.choice(np.array([-1.,1.]),size=M)
 r=rng.choice(np.array([-1.,1.]),size=M)
 active=np.stack(((z+1)/2,(1-z)/2),axis=1)
 noise=lfilter([1.],[1.,-.86],rng.normal(size=2*M)*.012*np.sqrt(1-.86**2)).reshape(M,2)
 base=noise+.01*rng.normal(size=(M,2))
 common=(.035 if mode!='null' else 0)*r[:,None]*active
 science=base+common+.005*rng.normal(size=(M,2))
 reference=base+common+.005*rng.normal(size=(M,2))
 if mode=='optical':science+=.095*r[:,None]*active
 # Direct mismatch between detectors due to optical-switch electronics
 science+=.6*eta*active
 ix=rng.choice(4*M,size=K,replace=False)
 stream=np.concatenate([science.flatten(),reference.flatten()])
 stream[ix]=1e8 *rng.choice(np.array([-1.,1.]),size=K)
 science=np.clip(stream[:2*M].reshape(M,2),-T,T)
 reference=np.clip(stream[2*M:].reshape(M,2),-T,T)
 D=(science-reference)[:,0]-(science-reference)[:,1]
 score=float(np.dot(z*r,D));cut=threshold(M,T,eta,K,alpha)
 return dict(reject=abs(score)>cut,score=score,cutoff=cut)
def certificate():
 out={}
 for i,mode in enumerate(('null','electronics_sham','optical')):
  rows=[trial(88940+20000*i+j,mode) for j in range(18)]
  out[mode]=dict(n=len(rows),rejections=sum(x['reject'] for x in rows),
    median_signed_score=float(np.median([x['score'] for x in rows])),
    threshold=rows[0]['cutoff'])
 assert out['null']['rejections']==0
 assert out['electronics_sham']['rejections']==0
 assert out['optical']['rejections']==18
 return dict(status='PASS',pairs=8000,detectors=2,raw_shots=32000,
   maximum_arbitrarily_corrupted_raw_readings=14,
   clip_T=.15,independently_calibrated_switch_mismatch_eta=.0005,
   alpha=.01,synthetic=out,
   theorem='Conditional sharp-null Rademacher/Hoeffding score for sensor-difference DID: |X|>2 eta M+4TK+4T sqrt(2M ln(2/alpha)) rejects at level alpha with independent z, arbitrary serial clean drift and <=K raw faults. Science-only switch leakage >eta invalidates the bound.',
   identification_boundary='Two detector negative control and randomized optical path cannot by itself establish a specific quartic optical gate. Shared electronics artifacts cancel only if matched. Independent leakage calibration, detector-swap and hardware audit required; all numbers synthetic.')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_dual_sensor_did_optics.json').write_text(json.dumps(z,indent=2)+'\n')
 print('DUAL-SENSOR',[(x,y['rejections'],y['median_signed_score'],y['threshold']) for x,y in z['synthetic'].items()])
