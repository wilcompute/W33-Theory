#!/usr/bin/env python3
"""Pass 439: torsion-sensitive photonic field/ring fault-channel falsifier."""
from __future__ import annotations
import argparse,json,math,random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass439_torsion_sensitive_photonic_fault_channel.json'
N=16
FIELD={8:72,16:288}
RING={2:6,8:60,16:216}


def template(shape:dict[int,int],visibility:float=1.0,dark:float=0.0,jitter:float=0.0)->list[float]:
    total=sum(shape.values());out=[]
    for n in range(N):
        s=0.0
        for period,weight in shape.items():
            attenuation=math.exp(-0.5*(2*math.pi*jitter/period)**2)
            s+=weight*attenuation*math.cos(2*math.pi*n/period)
        out.append((1-2*dark)*visibility*s/total)
    return out


def fit_scale(y:list[float],t:list[float])->tuple[float,float]:
    alpha=sum(a*b for a,b in zip(y,t))/sum(b*b for b in t)
    residual=math.sqrt(sum((a-alpha*b)**2 for a,b in zip(y,t)))
    return residual,alpha


def dft_bin(y:list[float],k:int)->float:
    re=sum(y[n]*math.cos(2*math.pi*k*n/N) for n in range(N))
    im=-sum(y[n]*math.sin(2*math.pi*k*n/N) for n in range(N))
    return 2*math.hypot(re,im)/N


def ideal_features(shape:dict[int,int])->dict:
    y=template(shape)
    return {'trace':[round(x,12) for x in y],
      'dft':{str(k):round(dft_bin(y,k),12) for k in range(N//2+1) if dft_bin(y,k)>1e-12}}


def run_census(shots:int=16384)->dict:
    rng=random.Random(439);field_t=template(FIELD);ring_t=template(RING);rows=[]
    for truth,shape in [('field',FIELD),('ring',RING)]:
      for visibility in (0.55,0.70,0.85,1.0):
       for dark in (0.0,0.01,0.03):
        for jitter in (0.0,0.10,0.25):
         signal=template(shape,visibility,dark,jitter);probs=[min(1,max(0,(1+x)/2)) for x in signal]
         counts=[sum(1 for _ in range(shots) if rng.random()<p) for p in probs]
         y=[2*c/shots-1 for c in counts]
         ef,af=fit_scale(y,field_t);er,ar=fit_scale(y,ring_t)
         predicted='field' if ef<er else 'ring'
         rows.append({'truth':truth,'predicted':predicted,'visibility':visibility,'dark':dark,'jitter':jitter,
           'field_residual':ef,'ring_residual':er,'field_scale':af,'ring_scale':ar,
           'margin':abs(ef-er),'nyquist_bin':dft_bin(y,8)})
    worst=min(rows,key=lambda x:x['margin'])
    return {'shots_per_phase':shots,'scenario_count':len(rows),
      'correct':sum(x['truth']==x['predicted'] for x in rows),
      'minimum_residual_margin':round(worst['margin'],12),
      'worst_case':{k:(round(v,12) if isinstance(v,float) else v) for k,v in worst.items()},
      'maximum_field_nyquist':round(max(x['nyquist_bin'] for x in rows if x['truth']=='field'),12),
      'minimum_ring_nyquist':round(min(x['nyquist_bin'] for x in rows if x['truth']=='ring'),12)}


def build_payload()->dict:
    field=ideal_features(FIELD);ring=ideal_features(RING);census=run_census()
    checks={'field_has_no_period2_peak':'8' not in field['dft'],
      'ring_has_period2_peak':abs(ring['dft']['8']-0.042553191489)<1e-12,
      'field_expected_peaks':field['dft']=={'1':0.8,'2':0.2},
      'ring_expected_peaks':ring['dft']=={'1':0.765957446809,'2':0.212765957447,'8':0.042553191489},
      'all_72_scenarios_classified':census['correct']==census['scenario_count']==72,
      'positive_minimum_margin':census['minimum_residual_margin']>0.016,
      'ring_nyquist_separated_in_census':census['minimum_ring_nyquist']>census['maximum_field_nyquist'],
      'synthetic_not_physical_claim':True}
    return {'schema':'w33.pass439.torsion_sensitive_photonic_fault_channel.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'protocol':{'phase_steps':16,'observable':'binary Ramsey/echo contrast','field_periods':FIELD,'ring_periods':RING,
      'classifier':'least residual after a fitted visibility scale','telemetry':'emit model label, residual margin, and Nyquist amplitude in a distance-three protected frame'},
      'ideal':{'field':field,'ring':ring},'census':census,
      'boundary':'deterministic synthetic shot-noise model; laboratory visibility, dark counts, phase jitter, and correlated drift require calibration',
      'checks':checks}


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 439 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'correct':p['census']['correct']}));return 0 if p['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
