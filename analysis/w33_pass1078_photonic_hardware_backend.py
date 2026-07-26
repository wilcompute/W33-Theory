from __future__ import annotations
import csv,hashlib,hmac,json,time
from pathlib import Path
from w33_pass1060_1064_core import build_w33

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1078_photonic_hardware_backend.json'
HW=ROOT/'hardware'
SYNTH_KEY=b'W33-PASS1078-SYNTHETIC-ONLY-NOT-FOR-EXPERIMENT'

def canon_json(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def sign(payload,key):return hmac.new(key,canon_json(payload),hashlib.sha256).hexdigest()
def target_permutation(context,n=40):
    rest=[x for x in range(n) if x not in context];order=list(context)+rest;p=[0]*n
    for port,mode in enumerate(order):p[mode]=port
    return p
def adjacent_swap_network(p):
    arr=list(range(len(p)));target=sorted(arr,key=lambda x:p[x]);swaps=[];pos={x:i for i,x in enumerate(arr)}
    for out,label in enumerate(target):
        i=pos[label]
        while i>out:
            a,b=arr[i-1],arr[i];arr[i-1],arr[i]=b,a;pos[a]=i;pos[b]=i-1;swaps.append((i-1,i));i-=1
    assert [p[x] for x in arr]==sorted(p);return swaps
def layer_swaps(swaps):
    layers=[]
    for s in swaps:
        for layer in layers:
            used={x for pair in layer for x in pair}
            if s[0] not in used and s[1] not in used:layer.append(s);break
        else:layers.append([s])
    return layers
def compile_context(context):
    p=target_permutation(context);sw=adjacent_swap_network(p);layers=layer_swaps(sw)
    return {'context':list(context),'permutation':p,'adjacent_swaps':[list(x) for x in sw],'mesh_depth':len(layers),'mzi_count':len(sw),'layers':[[{'ports':list(pair),'theta':'pi/2','phi':'0','component':'balanced_MZI_swap'} for pair in layer] for layer in layers],'detector_ports':[0,1,2,3]}
def calibration_ok(row):return row['dark_rate']<=0.01 and row['efficiency']>=0.65 and row['imbalance']<=0.08
def sequential_decision(blocks,min_blocks=10,max_blocks=100,bound=7.0):
    for i,b in enumerate(blocks[:max_blocks],1):
        if not calibration_ok(b):return {'decision':'inconclusive_no_claim','stop_block':i,'reason':'calibration_gate'}
        if i<min_blocks:continue
        if b['ci_low']>bound:return {'decision':'contextual_positive','stop_block':i,'reason':'lower_CI_above_bound'}
        if b['ci_high']<bound:return {'decision':'noncontextual_negative','stop_block':i,'reason':'upper_CI_below_bound'}
    return {'decision':'inconclusive_no_claim','stop_block':min(len(blocks),max_blocks),'reason':'no_preregistered_boundary_crossing'}
def blinded_id(label,key):return hmac.new(key,label.encode(),hashlib.sha256).hexdigest()[:20]
def unblind(index,key,signature):
    if not hmac.compare_digest(sign({'index':index},key),signature):raise ValueError('bad signature')
    return {row['blind_id']:row['label'] for row in index}
def parse_real_csv(path):
    required=['block_id','detector','clicks','trials','dark_rate','efficiency','imbalance'];rows=[]
    with open(path,newline='',encoding='utf-8') as f:
        r=csv.DictReader(f)
        if r.fieldnames!=required:raise ValueError(f'expected columns {required}')
        for row in r:
            z={'block_id':row['block_id'],'detector':int(row['detector']),'clicks':int(row['clicks']),'trials':int(row['trials']),'dark_rate':float(row['dark_rate']),'efficiency':float(row['efficiency']),'imbalance':float(row['imbalance'])}
            if not(0<=z['clicks']<=z['trials'] and 0<=z['detector']<4):raise ValueError('invalid count/channel')
            rows.append(z)
    return rows
def main():
    started=time.time();HW.mkdir(exist_ok=True);w=build_w33();compiled=[compile_context(L) for L in w.lines];macros=[]
    for p in range(40):
        star=list(w.point_lines[p]);nonstar=[i for i in range(40) if i not in star];macros.append({'gauge_point':p,'calibrations':['vacuum_dark','bright_reference'],'context_order':nonstar+star,'star_contexts':star,'projectors_per_context':4})
    elementary=sum(2+len(m['context_order'])*m['projectors_per_context'] for m in macros)
    resources={'contexts':40,'gauge_cycles':40,'elementary_operations':elementary,'max_mesh_depth':max(c['mesh_depth'] for c in compiled),'max_mzi_count':max(c['mzi_count'] for c in compiled),'total_context_mzi_count':sum(c['mzi_count'] for c in compiled),'detector_channels':4,'time_bin_delay_slots':40,'switch_control_bits_per_mzi':2}
    schedule_surface={'schema':'w33.pass1078.mesh_schedule.v1','contexts':compiled,'macros':macros,'resources':resources};schedule_hash=sha(canon_json(schedule_surface))
    manifest={'schema':'w33.pass1078.signed_manifest.v1','mode':'synthetic_validation_only','schedule_sha256':schedule_hash,'backend':'40-mode adjacent-MZI rectangular mesh','real_data_schema':['block_id','detector','clicks','trials','dark_rate','efficiency','imbalance'],'stopping_rule':{'min_blocks':10,'max_blocks':100,'noncontextual_bound':7.0,'calibration_fail':'inconclusive_no_claim'},'external_key_required_for_real_acquisition':True}
    manifest_sig=sign(manifest,SYNTH_KEY);index=[{'label':x,'blind_id':blinded_id(x,SYNTH_KEY)} for x in ['contextual_hessian','noncontextual_hessian','contextual_dual','noncontextual_dual']];index_sig=sign({'index':index},SYNTH_KEY)
    common={'dark_rate':0.002,'efficiency':0.82,'imbalance':0.02};pos=[{**common,'ci_low':6.5+0.07*i,'ci_high':7.2+0.07*i} for i in range(15)];neg=[{**common,'ci_low':7.1-0.08*i,'ci_high':7.6-0.08*i} for i in range(15)];bad=[{**common,'ci_low':7.3,'ci_high':7.8} for _ in range(12)];bad[4]['dark_rate']=0.02
    fixtures={'positive':sequential_decision(pos),'negative':sequential_decision(neg),'bad_calibration':sequential_decision(bad)}
    csvpath=HW/'w33_pass1078_real_data_fixture.csv'
    with open(csvpath,'w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(manifest['real_data_schema'])
        for d in range(4):wr.writerow(['fixture-block-000',d,80+d,100,0.002,0.82,0.02])
    parsed=parse_real_csv(csvpath)
    checks={'forty_contexts_compiled':len(compiled)==40,'all_contexts_route_to_ports_0_1_2_3':all(sorted(c['permutation'][x] for x in c['context'])==[0,1,2,3] for c in compiled),'all_meshes_reconstruct_exact_permutations':all(c['mzi_count']==len(c['adjacent_swaps']) for c in compiled),'forty_gauge_cycles':len(macros)==40,'elementary_operation_count_is_6480':elementary==6480,'manifest_signature_verifies':hmac.compare_digest(sign(manifest,SYNTH_KEY),manifest_sig),'offline_unblinding_verifies_signature':len(unblind(index,SYNTH_KEY,index_sig))==4,'positive_fixture_stops_positive':fixtures['positive']['decision']=='contextual_positive','negative_fixture_stops_negative':fixtures['negative']['decision']=='noncontextual_negative','bad_calibration_fails_closed':fixtures['bad_calibration']['decision']=='inconclusive_no_claim','real_csv_schema_ingests_four_detector_rows':len(parsed)==4};assert all(checks.values()),(checks,fixtures,resources)
    (HW/'w33_pass1078_mesh_manifest.json').write_text(json.dumps({**manifest,'synthetic_signature_hmac_sha256':manifest_sig},indent=2)+'\n');(HW/'w33_pass1078_blinded_index.json').write_text(json.dumps({'index':index,'synthetic_signature_hmac_sha256':index_sig,'warning':'synthetic fixture only; do not use this key for real acquisition'},indent=2)+'\n');(HW/'w33_pass1078_macro_schedule.json').write_text(json.dumps({'schedule_sha256':schedule_hash,'macros':macros,'resources':resources},indent=2)+'\n')
    out={'schema':'w33.pass1078.photonic_hardware_backend.v1','status':'PASS','headline':'The preregistered W33 protocol now has a deterministic 40-mode adjacent-MZI backend, exact resource accounting, HMAC-signed manifests, strict real-data CSV ingestion, sequential stopping rules, and a separate signature-checked offline unblinding path.','resources':resources,'schedule_sha256':schedule_hash,'manifest_signature':manifest_sig,'synthetic_fixtures':fixtures,'check_count':len(checks),'checks':checks,'hardware_artifacts':['hardware/w33_pass1078_mesh_manifest.json','hardware/w33_pass1078_macro_schedule.json','hardware/w33_pass1078_blinded_index.json','hardware/w33_pass1078_real_data_fixture.csv'],'scope':'Executable control-plane backend and synthetic validation. No physical optical mesh, detector calibration, acquisition duration, or experimental statistical power is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','resources':resources,'fixtures':fixtures,'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
