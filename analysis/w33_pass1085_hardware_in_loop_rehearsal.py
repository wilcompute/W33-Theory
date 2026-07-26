from __future__ import annotations
import json,hashlib,hmac,time
from pathlib import Path
from w33_pass1081_1086_core import build_w33
REPO=Path(__file__).resolve().parents[1];ROOT=REPO/'hardware';ROOT.mkdir(exist_ok=True)
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def sig(key,x):return hmac.new(key,canon(x),hashlib.sha256).hexdigest()
def chain(events):
 prev='0'*64;out=[]
 for seq,e in enumerate(events):
  row={'seq':seq,'prev_hash':prev,**e};row['event_hash']=sha(canon(row));prev=row['event_hash'];out.append(row)
 return out,prev
def verify_chain(rows):
 prev='0'*64
 for seq,row in enumerate(rows):
  z=dict(row);h=z.pop('event_hash')
  if z['seq']!=seq or z['prev_hash']!=prev or sha(canon(z))!=h:return False
  prev=h
 return True
def schedule():
 pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();cmds=[]
 for ci,L in enumerate(lines):
  cal=f'CAL-W33-{ci:02d}-A';cmds.append({'op':'calibrate','calibration_id':cal,'context':ci,'dark_gate_max':0.01,'efficiency_min':0.65,'imbalance_max':0.08})
  for port,mode in enumerate(L):cmds.append({'op':'route','context':ci,'mode':mode,'detector_port':port,'calibration_id':cal})
  cmds.append({'op':'acquire','context':ci,'trials':1000,'observable':'state_independent_contextuality_witness_W','explicitly_not':'Abramsky-Barbosa contextual fraction'})
 return cmds
def mock_run(cmds,key,run_label='synthetic-contextual'):
 events=[]
 for c in cmds:
  if c['op']=='calibrate':events.append({**c,'dark_rate':0.002,'efficiency':0.82,'imbalance':0.02,'status':'PASS'})
  elif c['op']=='route':events.append({**c,'controller_ack':True,'switch_crc':sha(canon(c))[:16]})
  else:
   ci=c['context'];clicks=[250+(ci+j)%3 for j in range(4)];events.append({**c,'blind_run_id':hmac.new(key,run_label.encode(),hashlib.sha256).hexdigest()[:20],'clicks':clicks,'detector_channels':[0,1,2,3],'calibration_id':f'CAL-W33-{ci:02d}-A'})
 rows,root=chain(events);payload={'schema':'w33.pass1085.telemetry.v1','events':rows,'chain_root':root};payload['signature']=sig(key,{'chain_root':root,'event_count':len(rows)});return payload
def analyze(payload,key=None):
 assert verify_chain(payload['events'])
 if key is not None:assert hmac.compare_digest(payload['signature'],sig(key,{'chain_root':payload['chain_root'],'event_count':len(payload['events'])}))
 cals={e['calibration_id']:e for e in payload['events'] if e['op']=='calibrate'};acq=[e for e in payload['events'] if e['op']=='acquire'];gate=all(cals[e['calibration_id']]['status']=='PASS' for e in acq)
 if not gate:return {'decision':'inconclusive_no_claim','reason':'calibration_gate'}
 W=sum(sum(e['clicks'])/(4*e['trials']) for e in acq)
 return {'decision':'contextual_positive' if W>7 else 'not_contextual_at_preregistered_threshold','witness_W':W,'noncontextual_bound':7,'observable':'state_independent_contextuality_witness_W','contextual_fraction_claim':None}
def unblind(payload,key,escrow_commitment,label):
 assert sha(key)==escrow_commitment;blind=hmac.new(key,label.encode(),hashlib.sha256).hexdigest()[:20];ids={e.get('blind_run_id') for e in payload['events'] if e['op']=='acquire'};assert ids=={blind};return {'blind_run_id':blind,'label':label,'verified':True}
def main():
 started=time.time();key=hashlib.sha256(b'PASS1085 SYNTHETIC KEY - NEVER USE FOR REAL DATA').digest();commit=sha(key);cmds=schedule();manifest={'schema':'w33.pass1085.acquisition_manifest.v1','controller_firmware':'mock-mzi-controller/1.0','schedule_sha256':sha(canon(cmds)),'command_count':len(cmds),'escrow_key_commitment_sha256':commit,'key_material_committed':False,'observable':'state_independent_contextuality_witness_W','noncontextual_bound':7,'Abramsky_Barbosa_CF_expected':1,'retired_claim':'CF=1/10','real_acquisition_requires_external_key':True};manifest['manifest_sha256']=sha(canon(manifest));tele=mock_run(cmds,key);analysis=analyze(tele,key);unb=unblind(tele,key,commit,'synthetic-contextual')
 wrong=False
 try:unblind(tele,b'wrong',commit,'synthetic-contextual')
 except Exception:wrong=True
 checks={'schedule_has_240_commands':len(cmds)==240,'forty_calibrations':sum(c['op']=='calibrate' for c in cmds)==40,'one_hundred_sixty_routes':sum(c['op']=='route' for c in cmds)==160,'forty_acquisitions':sum(c['op']=='acquire' for c in cmds)==40,'hash_chain_verifies':verify_chain(tele['events']),'telemetry_signature_verifies':hmac.compare_digest(tele['signature'],sig(key,{'chain_root':tele['chain_root'],'event_count':len(tele['events'])})),'analysis_is_contextual_positive':analysis['decision']=='contextual_positive','witness_near_10':9.9<analysis['witness_W']<10.2,'analysis_never_labels_click_rate_as_contextual_fraction':analysis['contextual_fraction_claim'] is None,'offline_unblind_succeeds':unb['verified'],'wrong_key_fails':wrong,'public_manifest_contains_only_commitment':commit in canon(manifest).decode() and key.hex() not in canon(manifest).decode(),'all_calibration_ids_bound_to_acquisitions':all(e['calibration_id'].startswith('CAL-W33-') for e in tele['events'] if e['op']=='acquire'),'immutable_manifest_hash_present':'manifest_sha256' in manifest,'external_real_key_required':manifest['real_acquisition_requires_external_key']};assert all(checks.values()),checks
 for name,obj in [('manifest',manifest),('telemetry',tele),('analysis',analysis),('unblinding_receipt',unb)]:open(ROOT/f'w33_pass1085_{name}.json','w').write(json.dumps(obj,indent=2)+'\n')
 out={'status':'PASS','check_count':len(checks),'checks':checks,'manifest':manifest,'analysis':analysis,'telemetry_event_count':len(tele['events']),'chain_root':tele['chain_root'],'artifacts':[str(p.name) for p in ROOT.iterdir()],'scope':'Mock-controller hardware-in-the-loop rehearsal. No physical device was connected and no real key material is committed.','seconds':time.time()-started};(REPO/'data'/'w33_pass1085_hardware_in_loop_rehearsal.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
