#!/usr/bin/env python3
"""Pass 423: inverse compiler from Pass-418 defect coordinates to hardware causes."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import numpy as np

from w33_pass410_414_common import certificate,write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass423_hardware_inverse_compiler.json'
ATLAS_OUT=ROOT/'data'/'w33_pass423_hardware_component_atlas.json'
SOURCE=ROOT/'data'/'w33_pass418_defect_atlas.json'

def vertex(i:int)->tuple[int,int,int]:return (i//9,(i//3)%3,i%3)

def build_dictionary(entries:list[dict])->tuple[np.ndarray,list[dict]]:
    n=len(entries);cols=[];components=[]
    def add(name,family,ids,action):
        v=np.zeros(n);v[ids]=1;v/=np.linalg.norm(v);cols.append(v)
        components.append({'component_id':len(components),'name':name,'family':family,'coordinate_ids':ids,'service_action':action})
    byfam={f:[] for f in ('mode_gain','native_coupler','distance_two_crosstalk','phase_fibre_pair')}
    for e in entries:byfam[e['family']].append(e)
    for e in byfam['mode_gain']:add(f'detector_gain_mode_{e["vertices"][0]}','detector_gain',[e['coordinate_id']],'recalibrate detector/mode gain')
    for e in byfam['native_coupler']:add(f'native_coupler_{e["vertices"][0]}_{e["vertices"][1]}','native_coupler',[e['coordinate_id']],'rebalance native beamsplitter/coupler')
    for e in byfam['distance_two_crosstalk']:add(f'parasitic_crosstalk_{e["vertices"][0]}_{e["vertices"][1]}','parasitic_crosstalk',[e['coordinate_id']],'isolate or retune distance-two leakage path')
    # A local phase trim explains one pair; a fibre delay explains all three pairs in one z-fibre.
    phase=byfam['phase_fibre_pair']
    for e in phase:add(f'phase_trim_{e["vertices"][0]}_{e["vertices"][1]}','phase_trim',[e['coordinate_id']],'retune local phase plate')
    groups={}
    for e in phase:
        u,v=e['vertices'];x,y,_=vertex(u);x2,y2,_=vertex(v);assert (x,y)==(x2,y2)
        groups.setdefault((x,y),[]).append(e['coordinate_id'])
    for (x,y),ids in sorted(groups.items()):
        add(f'delay_register_fibre_{x}_{y}','delay_register',sorted(ids),'recalibrate shared delay register for this three-bin fibre')
    return np.column_stack(cols),components

def omp(y:np.ndarray,D:np.ndarray,max_terms:int=8,tol:float=1e-10)->tuple[list[int],np.ndarray,float]:
    support=[];coef=np.zeros(0);res=y.copy()
    for _ in range(max_terms):
        scores=np.abs(D.T@res);scores[support]=-1;j=int(np.argmax(scores));support.append(j)
        coef=np.linalg.lstsq(D[:,support],y,rcond=None)[0];res=y-D[:,support]@coef
        if np.linalg.norm(res)<tol:break
    return support,coef,float(np.linalg.norm(res))

def trial(name:str,ids:list[int],amps:list[float],D:np.ndarray,components:list[dict])->dict:
    y=D[:,ids]@np.array(amps);support,coef,res=omp(y,D,max_terms=len(ids)+3)
    return {'name':name,'injected_components':[components[i]['name'] for i in ids],'recovered_components':[components[i]['name'] for i in support],'coefficients':[round(float(x),12) for x in coef],'residual_norm':round(res,14),'exact_support':set(ids)==set(support)}

def build_payload()->tuple[dict,dict]:
    source=json.loads(SOURCE.read_text());entries=source['entries'];D,components=build_dictionary(entries)
    lookup={c['name']:i for i,c in enumerate(components)}
    injected=[lookup['detector_gain_mode_4'],lookup['native_coupler_0_9'],lookup['parasitic_crosstalk_2_18'],lookup['delay_register_fibre_1_2']]
    trials=[trial('mixed_four_fault',injected,[2.0,-1.5,0.75,3.0],D,components)]
    # Model-selection boundary: one pair -> phase trim; all three -> shared delay.
    phase_id=next(i for i,c in enumerate(components) if c['family']=='phase_trim')
    coord=components[phase_id]['coordinate_ids'][0]
    delay_id=next(i for i,c in enumerate(components) if c['family']=='delay_register' and coord in c['coordinate_ids'])
    trials.append(trial('single_pair_prefers_trim',[phase_id],[1.0],D,components))
    trials.append(trial('three_pair_pattern_prefers_delay',[delay_id],[1.0],D,components))
    rng=np.random.default_rng(423);sparse=[];all_sparse=True
    primitive=[i for i,c in enumerate(components) if c['family']!='delay_register']
    for t in range(24):
        ids=sorted(rng.choice(primitive,size=3,replace=False).tolist());amps=rng.choice([-2.,-1.,1.5,3.],size=3).tolist();r=trial(f'random_{t}',ids,amps,D,components);all_sparse &= r['exact_support'];sparse.append(r)
    atlas={'schema':'w33.pass423.hardware_component_atlas.v1','source_atlas_sha256':source['certificate_sha256'],'coordinate_count':len(entries),'component_count':len(components),'components':components}
    atlas['certificate_sha256']=certificate(atlas)
    checks={
      'source_has_378_coordinates':len(entries)==378,
      'dictionary_has_387_components':len(components)==387,
      'nine_delay_registers':sum(c['family']=='delay_register' for c in components)==9,
      'each_delay_has_three_phase_coordinates':all(len(c['coordinate_ids'])==3 for c in components if c['family']=='delay_register'),
      'mixed_fault_exact':trials[0]['exact_support'] and trials[0]['residual_norm']==0,
      'single_pair_selects_phase_trim':trials[1]['recovered_components']==[components[phase_id]['name']],
      'triple_selects_delay':trials[2]['recovered_components']==[components[delay_id]['name']],
      'all_24_sparse_trials_exact':all_sparse,
    };checks={k:bool(v) for k,v in checks.items()}
    payload={'schema':'w33.pass423.hardware_inverse_compiler.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
       'inverse_map':'the 374 centered Pass-418 coordinates compile into detector, native-coupler, parasitic-crosstalk, local-phase, and shared-delay hypotheses',
       'identifiability':'primitive single-coordinate causes are exact; the three-coordinate fibre signature distinguishes a shared delay fault from three independent phase trims by sparsity',
       'decoder':'normalized matched filtering with orthogonal matching pursuit exactly recovers the tested noiseless sparse faults',
       'boundary':'this is a hardware-cause dictionary and model-selection layer; empirical priors and component transfer functions must be calibrated on the physical device'},
      'component_atlas_path':'data/w33_pass423_hardware_component_atlas.json','deterministic_trials':trials,'random_sparse_trials':sparse,'recommended_workflow':['subtract four Pass-418 orbit means','run inverse compiler','service highest-confidence sparse component set','rerun twirled calibration and compare residual'],'checks':checks}
    payload['certificate_sha256']=certificate(payload);return payload,atlas

def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--atlas',type=Path,default=ATLAS_OUT);a=ap.parse_args();p,at=build_payload();pt=json.dumps(p,indent=2,sort_keys=True)+'\n';tt=json.dumps(at,indent=2,sort_keys=True)+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=pt:raise SystemExit('Pass 423 certificate drift')
  if not a.atlas.exists() or a.atlas.read_text()!=tt:raise SystemExit('Pass 423 atlas drift')
 else:write_json(a.output,p);write_json(a.atlas,at)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
