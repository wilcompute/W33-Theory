#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
from w33_pass543_547_common import charpoly_prime
from w33_pass553_five_point_core_geometry import A

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass561_noise_aware_orientation_latch.json'
OVERLAY=ROOT/'hardware'/'w33_pass561_noise_aware_orientation_latch.json'
ALPHA_5SIGMA=5.733031437583866e-7

def embedding_vector(coeff):
    z=np.exp(2j*np.pi/5)
    vals=[]
    for u in (1,2,3,4):
        v=sum(coeff[j]*z**(u*j) for j in range(4))
        vals.append(float(v.real))
    return np.array(vals)

def quartic_levels():
    fibres={}
    for m in range(4096):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A))
        cp=tuple(charpoly_prime(5,offs)[0]);fibres[cp]=fibres.get(cp,0)+1
    items=sorted(fibres,key=lambda x:json.dumps(x,separators=(',',':')))
    levels=sorted({cp[4] for cp in items})
    target=items[55][4]
    vecs=np.stack([embedding_vector(e) for e in levels])
    ti=levels.index(target);d2=np.sum((vecs-vecs[ti])**2,axis=1);d2[ti]=np.inf
    ni=int(np.argmin(d2))
    return levels,target,vecs,ti,ni,float(d2[ni])

def quartic_budget(sigma,d2,alpha=ALPHA_5SIGMA):
    # Four-coordinate union bound; Euclidean error < dmin/2.
    per_mode=math.ceil(32*sigma*sigma*math.log(8/alpha)/d2)
    return per_mode,4*per_mode

def orientation_budget(eta,visibility,dark,alpha=ALPHA_5SIGMA):
    c=eta*visibility*(1-2*dark)
    C=c**12
    direct=math.ceil(2*math.log(1/alpha)/(C*C))
    per_channel=math.ceil(2*math.log(12/alpha)/(c*c))
    sequential=12*per_channel
    return {'single_channel_contrast':c,'direct_twelvefold_contrast':C,'direct_parity_shots':direct,'sequential_shots_per_channel':per_channel,'sequential_total_shots':sequential,'improvement_factor':direct/sequential}

def monte_carlo(levels,vecs,ti,profile,sigma=50.0,alpha=.01,trials=20000,seed=561):
    rng=np.random.default_rng(seed)
    d2=np.sum((vecs-vecs[ti])**2,axis=1);d2[ti]=np.inf;mind2=float(np.min(d2))
    nq,_=quartic_budget(sigma,mind2,alpha)
    obs=vecs[ti]+rng.normal(0,sigma/math.sqrt(nq),size=(trials,4))
    dist=np.sum((obs[:,None,:]-vecs[None,:,:])**2,axis=2)
    qerr=float(np.mean(np.argmin(dist,axis=1)!=ti))
    o=orientation_budget(**profile,alpha=alpha);c=o['single_channel_contrast'];C=o['direct_twelvefold_contrast']
    nd=o['direct_parity_shots'];pd=(1+C)/2
    direct_counts=rng.binomial(nd,pd,size=trials);derr=float(np.mean(direct_counts<=nd/2))
    nc=o['sequential_shots_per_channel'];pc=(1+c)/2
    channel_counts=rng.binomial(nc,pc,size=(trials,12));channel_error=channel_counts<=nc/2
    serr=float(np.mean(np.sum(channel_error,axis=1)%2==1))
    return {'alpha':alpha,'trials':trials,'seed':seed,'quartic_sigma':sigma,'quartic_shots_per_mode':nq,'quartic_empirical_error':qerr,'direct_parity_shots':nd,'direct_empirical_error':derr,'sequential_shots_per_channel':nc,'sequential_empirical_error':serr}

def overlay_payload(profiles,quartic):
    return {'schema':'w33.hardware.pass561.noise_aware_orientation_latch.v1','carrier':'2048-bin BT1653 guard-shell compiler','upstream':'hardware/w33_pass556_q5_semilinear_control_plane.json','readout_contract':{'quartic_gate':'four Galois embedding accumulators with nearest-level decoding','orientation_direct':'single 12-fold parity correlator','orientation_recommended':'twelve independently repeated frame-sign channels followed by a classical parity latch'},'design_rule':{'quartic':'N_mode >= 32 sigma^2 log(8/alpha)/d_min^2','direct_orientation':'N >= 2 log(1/alpha)/C_12^2','sequential_orientation':'n_channel >= 2 log(12/alpha)/c_1^2; total=12 n_channel'},'profiles':profiles,'quartic':quartic,'boundary':'Shot counts are conditional on the stated independent sub-Gaussian and binary-contrast models. They are compiler design bounds, not measured device performance.'}

def payload():
    levels,target,vecs,ti,ni,d2=quartic_levels()
    sigmas=[25.0,50.0,100.0,250.0]
    qb={str(int(s)):{'per_mode':quartic_budget(s,d2)[0],'four_mode_total':quartic_budget(s,d2)[1]} for s in sigmas}
    profiles={
      'conservative':{'eta':.90,'visibility':.95,'dark':1e-3},
      'nominal':{'eta':.95,'visibility':.98,'dark':1e-4},
      'aspirational':{'eta':.99,'visibility':.995,'dark':1e-5},
    }
    ob={name:orientation_budget(**p) for name,p in profiles.items()}
    for name,x in ob.items():
        if x['direct_parity_shots']<=x['sequential_total_shots']:
            x['selected_architecture']='direct_twelvefold_parity';x['selected_total_shots']=x['direct_parity_shots']
        else:
            x['selected_architecture']='repeated_channel_parity';x['selected_total_shots']=x['sequential_total_shots']
    mc=monte_carlo(levels,vecs,ti,profiles['nominal'])
    quartic={'distinct_levels':len(levels),'target_coefficients':target,'nearest_competitor_coefficients':levels[ni],'minimum_four_embedding_distance_squared':d2,'five_sigma_budgets_by_single_shot_sigma':qb}
    ov=overlay_payload(ob,quartic);OVERLAY.parent.mkdir(parents=True,exist_ok=True);OVERLAY.write_text(json.dumps(ov,sort_keys=True,separators=(',',':'))+'\n')
    checks={
      'seventy_distinct_quartic_levels':len(levels)==70,
      'exact_minimum_embedding_distance_squared':abs(d2-3750)<1e-6,
      'all_budgets_positive':all(x['four_mode_total']>0 for x in qb.values()) and all(x['sequential_total_shots']>0 for x in ob.values()),
      'conservative_selects_repeated_channels':ob['conservative']['selected_architecture']=='repeated_channel_parity',
      'nominal_selects_direct_parity':ob['nominal']['selected_architecture']=='direct_twelvefold_parity',
      'aspirational_selects_direct_parity':ob['aspirational']['selected_architecture']=='direct_twelvefold_parity',
      'hybrid_selector_is_pointwise_minimum':all(x['selected_total_shots']==min(x['direct_parity_shots'],x['sequential_total_shots']) for x in ob.values()),
      'monte_carlo_quartic_below_test_alpha':mc['quartic_empirical_error']<=mc['alpha'],
      'monte_carlo_direct_below_test_alpha':mc['direct_empirical_error']<=mc['alpha'],
      'monte_carlo_sequential_below_test_alpha':mc['sequential_empirical_error']<=mc['alpha'],
      'overlay_written':OVERLAY.exists(),
    }
    return {'schema':'w33.pass561.noise_aware_orientation_latch.v1','status':'PASS' if all(checks.values()) else 'FAIL','confidence':{'alpha_five_sigma':ALPHA_5SIGMA,'bounds':'Hoeffding/sub-Gaussian union bounds'},'quartic_gate':quartic,'orientation_profiles':ob,'recommended_architecture':'Use an adaptive compiler selector: direct twelvefold parity when calibrated contrast is high; repeated per-channel signs plus a classical parity latch when loss makes c^12 too small.','monte_carlo_validation':mc,'hardware_overlay':str(OVERLAY.relative_to(ROOT)),'checks':checks,'boundary':'The result is exact under the declared stochastic model. Detection efficiency, visibility, dark probability, and single-shot quartic noise are assumptions swept explicitly; no experimental feasibility claim is made.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 561 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'nominal_sequential':p['orientation_profiles']['nominal']['sequential_total_shots'],'nominal_direct':p['orientation_profiles']['nominal']['direct_parity_shots']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
