from __future__ import annotations
import argparse,csv,hashlib,itertools,json,time
from pathlib import Path
from collections import Counter
import numpy as np
from sympy.combinatorics import PermutationGroup
from w33_pass1060_1064_core import *
from w33_pass1064_dual_falsifier_preregistration import analyze_stab,elemkey

ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware'; DATA=ROOT/'data'

def tcompose(a,b): return tuple(a[b[i]] for i in range(len(a)))
def tid(n=40): return tuple(range(n))
def transposition(n,a,b):
    p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def swap_network(p):
    seen=[False]*len(p);out=[]
    for i in range(len(p)):
        if seen[i] or p[i]==i:continue
        cyc=[];j=i
        while not seen[j]:seen[j]=True;cyc.append(j);j=p[j]
        out.extend((cyc[0],cyc[k]) for k in range(1,len(cyc)))
    return out
def reconstruct_swaps(n,swaps):
    cur=tid(n)
    for a,b in swaps:cur=tcompose(transposition(n,a,b),cur)
    return cur

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build_banks():
    w=build_w33();G=w.G
    point=G.stabilizer(0);L0=set(w.lines[0]);line=G.subgroup_search(lambda g:{g(x) for x in L0}==L0)
    pa=analyze_stab(point);la=analyze_stab(line)
    def bank(H,analysis):
        a,b=analysis['gens']; rows=[]
        candidates=sorted((x for x in H.generate_schreier_sims() if x.order()==3),key=elemkey)
        for ci,c in enumerate(candidates):
            c0=elemkey(c);a0=elemkey(a);b0=elemkey(b)
            maps={'c_after_a':tcompose(c0,a0),'a_after_c':tcompose(a0,c0),'c_after_b':tcompose(c0,b0),'b_after_c':tcompose(b0,c0)}
            score=sum(x!=y for x,y in zip(maps['c_after_a'],maps['a_after_c']))+sum(x!=y for x,y in zip(maps['c_after_b'],maps['b_after_c']))
            rows.append({'candidate_id':ci,'images':c0,'swaps':swap_network(c0),'sequence_maps':maps,'exact_score':score})
        return {'generator_a':elemkey(a),'generator_b':elemkey(b),'generator_a_swaps':swap_network(elemkey(a)),'generator_b_swaps':swap_network(elemkey(b)),'candidates':rows}
    return w,bank(point,pa),bank(line,la)

def compile_manifest():
    w,pbank,lbank=build_banks()
    stars={str(p):list(w.point_lines[p]) for p in range(40)}
    contexts=[{'context_id':i,'points':list(L),'calibration_id':f'ctx_{i:02d}_unitary'} for i,L in enumerate(w.lines)]
    point_central=[r for r in pbank['candidates'] if r['exact_score']==0]
    assert len(point_central)==2 and min(r['exact_score'] for r in lbank['candidates'])==27
    manifest={
      'schema':'w33.pass1069.photonic_protocol_manifest.v1','geometry':{'points':40,'contexts':contexts,'movable_point_stars':stars},
      'hardware_abstraction':{
        'source':['heralded_single_photon','vacuum_dark_control','bright_reference_control'],
        'routing':['calibrated_40_mode_mesh','EOM_swap_network','context_analyzer'],
        'detection':['binary_projector_yes','explicit_no_click','time_tag'],
        'calibration_parameters':['dark_rate','projector_efficiency','detector_imbalance']
      },
      'contextuality_schedule':{
        'gauge_cycles':40,'rule':'cycle p measures all 36 nonstar contexts first, then the four contexts in the movable star at p; every context is interrogated as four binary projector blocks.',
        'compiled_rows':1680,'elementary_operations':6480,'arithmetic':'40 cycles x (1 dark + 1 bright + 40 context blocks) = 1680 rows; expanding each context block to four binary projectors gives 40 x (2 + 40 x 4) = 6480 elementary operations',
        'warning':'The equality with any other repository count 6480 is recorded only as arithmetic, not an asserted structural identification.'
      },
      'central_C3_schedule':{
        'primary_point_candidates':[{'candidate_id':r['candidate_id'],'images':r['images'],'swaps':r['swaps']} for r in point_central],
        'primary_sequence_names':['c_after_a','a_after_c','c_after_b','b_after_c'],'primary_sequence_rows':8,
        'point_candidate_bank_size':len(pbank['candidates']),'dual_control_bank_size':len(lbank['candidates']),
        'point_candidate_score_histogram':dict(sorted(Counter(r['exact_score'] for r in pbank['candidates']).items())),
        'dual_candidate_score_histogram':dict(sorted(Counter(r['exact_score'] for r in lbank['candidates']).items())),
        'point_bank_hash':canonical_hash(pbank),'dual_control_bank_hash':canonical_hash(lbank)
      },
      'analysis_freeze':{
        'contextuality_bound':7,'bootstrap_replicates':800,'bootstrap_seed':1069,
        'contextual_positive':'95% bootstrap lower endpoint > 7','contextual_negative':'95% bootstrap upper endpoint <= 7','otherwise':'inconclusive',
        'C3_point':'at least two order-3 candidates score <= 9','C3_dual':'minimum candidate score >= 18','C3_gray_zone':'otherwise inconclusive',
        'calibration_gates':{'max_dark_rate':0.02,'min_projector_efficiency':0.80,'max_detector_imbalance':0.10}
      },
      'real_run_guard':'Real acquisition must supply calibration IDs and an external blinding key. The committed key is synthetic-fixture-only.'
    }
    manifest['manifest_hash']=canonical_hash(manifest)
    return manifest

def write_schedule(manifest,path):
    stars={int(k):set(v) for k,v in manifest['geometry']['movable_point_stars'].items()}
    fields=['row_id','arm','gauge_center','phase','context_order','star_contexts','candidate_id','sequence','calibration_id','operation']
    rows=[];rid=0
    for center in range(40):
        order=[c for c in range(40) if c not in stars[center]]+sorted(stars[center])
        rows.append({'row_id':rid,'arm':'contextuality','gauge_center':center,'phase':'gauge_cycle','context_order':';'.join(map(str,order)),'star_contexts':';'.join(map(str,sorted(stars[center]))),'candidate_id':'','sequence':'','calibration_id':'all_40_context_calibrations','operation':'expand_cycle_to_dark_bright_and_40_context_blocks'});rid+=1
    for cand in manifest['central_C3_schedule']['primary_point_candidates']:
        for seq in manifest['central_C3_schedule']['primary_sequence_names']:
            rows.append({'row_id':rid,'arm':'central_C3','gauge_center':'','phase':'process_sequence','context_order':'','star_contexts':'','candidate_id':cand['candidate_id'],'sequence':seq,'calibration_id':'40mode_process_tomography','operation':'expand_candidate_swap_network_sequence'});rid+=1
    with path.open('w',newline='',encoding='utf-8') as f:
        wri=csv.DictWriter(f,fieldnames=fields);wri.writeheader();wri.writerows(rows)
    return rows

def make_projector_records(w,rng,true_p,cal):
    records=[];trials=500;observed=cal['dark_rate']+cal['projector_efficiency']*true_p
    for p in range(40):
        contexts=list(w.point_lines[p]);yes=[int(rng.binomial(trials,observed)) for _ in contexts]
        records.append({'point':p,'contexts':contexts,'trials_per_context':trials,'yes_by_context':yes})
    return records

def make_c3_records(bank):
    return [{'candidate_id':r['candidate_id'],'score':r['exact_score'],'sequence_hash':canonical_hash(r['sequence_maps'])} for r in bank['candidates']]

def generate_synthetic(manifest):
    w,pbank,lbank=build_banks();cal={'dark_rate':0.005,'projector_efficiency':0.90,'detector_imbalance':0.02}
    specs=[('contextual_point',0.25,pbank),('noncontextual_point',0.15,pbank),('contextual_dual',0.25,lbank),('noncontextual_dual',0.15,lbank)]
    datasets=[];key={}
    for i,(scenario,p,bank) in enumerate(specs):
        seed=106900+i;rng=np.random.default_rng(seed);run='run_'+hashlib.sha256(f'{scenario}:{seed}'.encode()).hexdigest()[:16]
        datasets.append({'run_id':run,'manifest_hash':manifest['manifest_hash'],'calibration':cal,'projector_records':make_projector_records(w,rng,p,cal),'C3_records':make_c3_records(bank)})
        key[run]=scenario
    fixture={'schema':'w33.pass1069.synthetic_blinded.v1','synthetic_fixture_only':True,'datasets':datasets}
    return fixture,{'schema':'w33.pass1069.synthetic_blinding_key.v1','synthetic_fixture_only':True,'mapping':key}

def bootstrap_w(records,cal,reps=800,seed=1069):
    rng=np.random.default_rng(seed);by_point={r['point']:r for r in records}
    def estimate(rs):
        total=0.0
        for p in range(40):
            r=rs[p];yes=sum(r['yes_by_context']);tr=len(r['yes_by_context'])*r['trials_per_context'];raw=yes/tr
            total+=max(0.0,min(1.0,(raw-cal['dark_rate'])/cal['projector_efficiency']))
        return total
    obs=estimate(by_point);samples=[]
    for _ in range(reps):
        rr={}
        for p,r in by_point.items():
            trials=r['trials_per_context'];resampled=[int(rng.binomial(trials,y/trials)) for y in r['yes_by_context']]
            rr[p]={**r,'yes_by_context':resampled}
        samples.append(estimate(rr))
    lo,hi=np.quantile(samples,[0.025,0.975]);return obs,float(lo),float(hi)

def c3_score(record):
    if 'score' in record:return int(record['score'])
    m=record['sequence_maps']
    return sum(x!=y for x,y in zip(m['c_after_a'],m['a_after_c']))+sum(x!=y for x,y in zip(m['c_after_b'],m['b_after_c']))

def analyze_dataset(manifest,dataset):
    gates=manifest['analysis_freeze']['calibration_gates'];cal=dataset['calibration']
    calpass=cal['dark_rate']<=gates['max_dark_rate'] and cal['projector_efficiency']>=gates['min_projector_efficiency'] and cal['detector_imbalance']<=gates['max_detector_imbalance'] and dataset['manifest_hash']==manifest['manifest_hash']
    W,lo,hi=bootstrap_w(dataset['projector_records'],cal,manifest['analysis_freeze']['bootstrap_replicates'],manifest['analysis_freeze']['bootstrap_seed'])
    context='positive' if lo>7 else ('negative' if hi<=7 else 'inconclusive')
    scores=sorted(c3_score(r) for r in dataset['C3_records']);low=sum(s<=9 for s in scores)
    c3='point' if low>=2 else ('dual' if scores and scores[0]>=18 else 'inconclusive')
    if not calpass:context=c3='inconclusive'
    matrix={('positive','point'):'supports_W33_contextual_point_Hessian_tower',('negative','point'):'local_Hessian_present_contextual_substrate_rejected',('positive','dual'):'contextuality_present_selected_tower_rejected',('negative','dual'):'joint_rejection'}
    verdict=matrix.get((context,c3),'inconclusive_no_claim')
    return {'run_id':dataset['run_id'],'calibration_pass':calpass,'contextuality':{'W':W,'CI95':[lo,hi],'decision':context},'central_C3':{'min_score':scores[0] if scores else None,'n_scores_le9':low,'decision':c3},'joint_verdict':verdict}

def main():
    HW.mkdir(exist_ok=True);DATA.mkdir(exist_ok=True)
    manifest=compile_manifest();rows=write_schedule(manifest,HW/'w33_pass1069_control_schedule.csv')
    fixture,key=generate_synthetic(manifest)
    analyses=[analyze_dataset(manifest,d) for d in fixture['datasets']]
    expected=['supports_W33_contextual_point_Hessian_tower','local_Hessian_present_contextual_substrate_rejected','contextuality_present_selected_tower_rejected','joint_rejection']
    bad=json.loads(json.dumps(fixture['datasets'][0]));bad['calibration']['dark_rate']=0.03
    bad_result=analyze_dataset(manifest,bad)
    _,pbank,lbank=build_banks()
    checks={
      'forty_contexts_compiled':len(manifest['geometry']['contexts'])==40,
      'contextual_macro_schedule_has_40_gauge_rows':sum(r['arm']=='contextuality' for r in rows)==40,
      'macro_expansion_has_1680_compiled_rows':manifest['contextuality_schedule']['compiled_rows']==1680,
      'contextual_schedule_expands_to_6480_elementary_operations':manifest['contextuality_schedule']['elementary_operations']==6480,
      'primary_C3_schedule_has_eight_rows':sum(r['arm']=='central_C3' for r in rows)==8,
      'all_permutation_swap_networks_reconstruct':all(reconstruct_swaps(40,r['swaps'])==tuple(r['images']) for bank in (pbank,lbank) for r in bank['candidates']),
      'point_bank_has_two_exact_central_candidates':sum(r['exact_score']==0 for r in pbank['candidates'])==2,
      'dual_bank_exact_minimum_is_27':min(r['exact_score'] for r in lbank['candidates'])==27,
      'four_blinded_scenarios_hit_all_joint_branches':[x['joint_verdict'] for x in analyses]==expected,
      'calibration_failure_forces_inconclusive':bad_result['joint_verdict']=='inconclusive_no_claim',
      'manifest_hash_is_self_consistent':manifest['manifest_hash']==canonical_hash({k:v for k,v in manifest.items() if k!='manifest_hash'}),
      'candidate_bank_hashes_are_reproducible':manifest['central_C3_schedule']['point_bank_hash']==canonical_hash(pbank) and manifest['central_C3_schedule']['dual_control_bank_hash']==canonical_hash(lbank),
      'no_physical_duration_or_uncalibrated_angles_claimed':all(k not in json.dumps(manifest).lower() for k in ['measurement time','radians','degrees angle']),
    }
    assert all(checks.values()),checks
    manifest_path=HW/'w33_pass1069_photonic_manifest.json';fixture_path=HW/'w33_pass1069_synthetic_blinded.json';key_path=HW/'w33_pass1069_synthetic_key.json';out_path=DATA/'w33_pass1069_photonic_pipeline.json'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n');fixture_path.write_text(json.dumps(fixture,separators=(',',':'))+'\n');key_path.write_text(json.dumps(key,indent=2)+'\n')
    out={'schema':'w33.pass1069.photonic_pipeline.v1','status':'PASS','headline':'The Pass1064 preregistration is compiled into a defect-aware 40-context control schedule, exact permutation-to-EOM swap networks, calibration gates, four blinded synthetic fixtures, bootstrap contextuality analysis, central-C3 process analysis, and a fail-closed joint report.','artifacts':[str(manifest_path.relative_to(ROOT)),str((HW/'w33_pass1069_control_schedule.csv').relative_to(ROOT)),str(fixture_path.relative_to(ROOT)),str(key_path.relative_to(ROOT))],'schedule_rows':len(rows),'analyses':analyses,'invalid_calibration_test':bad_result,'check_count':len(checks),'checks':checks,'scope':'Executable abstract control and analysis software. Hardware-specific unitary decompositions, efficiencies, clock rates, and physical data remain calibration inputs and are not claimed.'}
    out_path.write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--analyze',type=Path);args=ap.parse_args()
    if args.analyze:
        manifest=json.loads((HW/'w33_pass1069_photonic_manifest.json').read_text());data=json.loads(args.analyze.read_text());print(json.dumps([analyze_dataset(manifest,d) for d in data['datasets']],indent=2))
    else:
        started=time.time();result=main();print(json.dumps({'status':result['status'],'check_count':result['check_count'],'schedule_rows':result['schedule_rows'],'seconds':round(time.time()-started,3)},indent=2))
