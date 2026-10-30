from __future__ import annotations
import hashlib,hmac,json,os,socket,socketserver,stat,threading,time,zlib
from pathlib import Path
from w33_pass1081_1086_core import build_w33

ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware';HW.mkdir(exist_ok=True);OUT=ROOT/'data'/'w33_pass1090_controller_protocol_boundary.json';VERSION='W33-MZI-TCP/1.0'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def crc(body):return f'{zlib.crc32(canon(body))&0xffffffff:08x}'
def sign(key,obj):return hmac.new(key,canon(obj),hashlib.sha256).hexdigest()
def envelope(body):return {'body':body,'crc32':crc(body)}
def verify_envelope(row):return isinstance(row,dict) and row.get('crc32')==crc(row.get('body',{}))

def schedule():
    *_,lines,_,_,_,_,_,_=build_w33();cmds=[]
    for ci,L in enumerate(lines):
        cal=f'CAL-W33-{ci:02d}-A';cmds.append({'op':'calibrate','context':ci,'calibration_id':cal,'dark_gate_max':0.01,'efficiency_min':0.65,'imbalance_max':0.08})
        for port,mode in enumerate(L):cmds.append({'op':'route','context':ci,'mode':mode,'detector_port':port,'calibration_id':cal})
        cmds.append({'op':'acquire','context':ci,'trials':1000,'calibration_id':cal,'observable':'state_independent_contextuality_witness_W'})
    return cmds

class ControllerState:
    def __init__(self,session_id,manifest_sha):self.session_id=session_id;self.manifest_sha=manifest_sha;self.expected_seq=0;self.cals={};self.routes={};self.lock=threading.Lock()
    def process(self,body):
        with self.lock:
            if body.get('version')!=VERSION:return False,'version_mismatch',{}
            if body.get('session_id')!=self.session_id:return False,'session_mismatch',{}
            if body.get('manifest_sha256')!=self.manifest_sha:return False,'manifest_mismatch',{}
            if body.get('seq')!=self.expected_seq:return False,'sequence_mismatch',{'expected_seq':self.expected_seq}
            p=body.get('payload',{});op=p.get('op');ctx=p.get('context');cal=p.get('calibration_id')
            if op=='calibrate':
                metrics={'dark_rate':0.002,'efficiency':0.82,'imbalance':0.02};passed=metrics['dark_rate']<=p['dark_gate_max'] and metrics['efficiency']>=p['efficiency_min'] and metrics['imbalance']<=p['imbalance_max'];self.cals[cal]={'context':ctx,'passed':passed,**metrics};self.routes[ctx]=set();data={'status':'PASS' if passed else 'FAIL',**metrics,'calibration_id':cal}
            elif op=='route':
                if cal not in self.cals or self.cals[cal]['context']!=ctx or not self.cals[cal]['passed']:return False,'calibration_required',{}
                if p.get('detector_port') not in range(4):return False,'bad_detector_port',{}
                self.routes.setdefault(ctx,set()).add(p['detector_port']);data={'controller_ack':True,'switch_crc':sha(canon(p))[:16],'calibration_id':cal}
            elif op=='acquire':
                if cal not in self.cals or self.cals[cal]['context']!=ctx or not self.cals[cal]['passed']:return False,'calibration_required',{}
                if self.routes.get(ctx)!=set(range(4)):return False,'four_routes_required',{'seen_ports':sorted(self.routes.get(ctx,set()))}
                clicks=[250+(ctx+j)%3 for j in range(4)];data={'clicks':clicks,'detector_channels':[0,1,2,3],'trials':p['trials'],'calibration_id':cal,'observable':p['observable']}
            else:return False,'unknown_operation',{}
            self.expected_seq+=1;return True,'ACK',data

class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        for raw in self.rfile:
            try:row=json.loads(raw);valid=verify_envelope(row);body=row.get('body',{}) if isinstance(row,dict) else {}
            except Exception:valid=False;body={}
            if not valid:ok=False;code='crc_or_json_failure';data={}
            else:ok,code,data=self.server.state.process(body)
            resp_body={'version':VERSION,'seq':body.get('seq'),'ack':ok,'code':code,'data':data,'controller_tick':body.get('seq')};self.wfile.write(canon(envelope(resp_body))+b'\n');self.wfile.flush()
            if not ok:break
class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
    def __init__(self,addr,state):self.state=state;super().__init__(addr,Handler)
def send(sock,row):
    sock.sendall(canon(row)+b'\n');buf=b''
    while b'\n' not in buf:
        chunk=sock.recv(65536)
        if not chunk:raise RuntimeError('controller closed connection')
        buf+=chunk
    resp=json.loads(buf.split(b'\n',1)[0]);assert verify_envelope(resp);return resp['body']

def run_client(host,port,cmds,session_id,manifest_sha,key):
    events=[];prev='0'*64
    with socket.create_connection((host,port),timeout=5) as s:
        for seq,payload in enumerate(cmds):
            body={'version':VERSION,'session_id':session_id,'manifest_sha256':manifest_sha,'seq':seq,'payload':payload};request=envelope(body);resp=send(s,request)
            if not resp['ack']:raise RuntimeError(f"controller NACK seq={seq} code={resp['code']}")
            event={'seq':seq,'prev_hash':prev,'request':request,'response':envelope(resp)};event['event_hash']=sha(canon(event));prev=event['event_hash'];events.append(event)
    transcript={'schema':'w33.pass1090.controller_transcript.v1','events':events,'chain_root':prev,'event_count':len(events)};transcript['signature_hmac_sha256']=sign(key,{'chain_root':prev,'event_count':len(events),'manifest_sha256':manifest_sha});return transcript

def verify_transcript(t,key,manifest_sha):
    prev='0'*64
    for seq,e in enumerate(t['events']):
        z=dict(e);h=z.pop('event_hash')
        if z['seq']!=seq or z['prev_hash']!=prev or not verify_envelope(z['request']) or not verify_envelope(z['response']) or sha(canon(z))!=h:return False
        rb=z['response']['body']
        if not rb['ack'] or rb['seq']!=seq:return False
        prev=h
    return prev==t['chain_root'] and hmac.compare_digest(t['signature_hmac_sha256'],sign(key,{'chain_root':prev,'event_count':len(t['events']),'manifest_sha256':manifest_sha}))
def analyze(t):
    acq=[e['response']['body']['data'] for e in t['events'] if e['request']['body']['payload']['op']=='acquire'];W=sum(sum(e['clicks'])/(4*e['trials']) for e in acq)
    return {'decision':'contextual_positive' if W>7 else 'not_contextual_at_preregistered_threshold','witness_W':W,'noncontextual_bound':7,'observable':'state_independent_contextuality_witness_W','contextual_fraction_field':None,'acquisition_count':len(acq)}
def negative_probe(session_id,manifest_sha,kind):
    state=ControllerState(session_id,manifest_sha);srv=Server(('127.0.0.1',0),state);th=threading.Thread(target=srv.serve_forever,daemon=True);th.start();host,port=srv.server_address
    try:
        with socket.create_connection((host,port),timeout=5) as s:
            if kind=='crc':row=envelope({'version':VERSION,'session_id':session_id,'manifest_sha256':manifest_sha,'seq':0,'payload':{'op':'calibrate'}});row['crc32']='00000000'
            elif kind=='missing_calibration':row=envelope({'version':VERSION,'session_id':session_id,'manifest_sha256':manifest_sha,'seq':0,'payload':{'op':'route','context':0,'mode':0,'detector_port':0,'calibration_id':'NONE'}})
            else:raise ValueError
            r=send(s,row);return (not r['ack'],r['code'])
    finally:srv.shutdown();srv.server_close();th.join(timeout=2)

def main():
    started=time.time();cmds=schedule();key=hashlib.sha256(b'PASS1090 LOOPBACK CERTIFICATION KEY - NOT REAL DATA').digest();keyfile=HW/'w33_pass1090_synthetic_escrow.key';keyfile.write_bytes(key);os.chmod(keyfile,stat.S_IRUSR|stat.S_IWUSR);commit=sha(key);session_id=os.environ.get('W33_SESSION_ID') or sha(canon(cmds))[:32]
    manifest={'schema':'w33.pass1090.controller_manifest.v1','protocol':VERSION,'transport':'TCP JSON-lines with CRC32 request/response framing','session_id':session_id,'schedule_sha256':sha(canon(cmds)),'command_count':len(cmds),'controller_endpoint_source':'W33_CONTROLLER_HOST/W33_CONTROLLER_PORT','escrow_key_commitment_sha256':commit,'key_material_embedded':False,'observable':'state_independent_contextuality_witness_W','noncontextual_bound':7,'forbidden_label':'Abramsky-Barbosa contextual fraction = 0.1','real_hardware_connected':False};manifest_sha=sha(canon(manifest));manifest['manifest_sha256']=manifest_sha
    state=ControllerState(session_id,manifest_sha);srv=Server(('127.0.0.1',0),state);th=threading.Thread(target=srv.serve_forever,daemon=True);th.start();host,port=srv.server_address
    try:transcript=run_client(host,port,cmds,session_id,manifest_sha,key)
    finally:srv.shutdown();srv.server_close();th.join(timeout=2)
    analysis=analyze(transcript);bad_crc=negative_probe(session_id,manifest_sha,'crc');missing_cal=negative_probe(session_id,manifest_sha,'missing_calibration');unblind={'schema':'w33.pass1090.offline_unblinding_receipt.v1','key_commitment_verified':sha(key)==commit,'transcript_verified':verify_transcript(transcript,key,manifest_sha),'blind_label':'synthetic-contextual','chain_root':transcript['chain_root']}
    checks={'schedule240':len(cmds)==240,'forty_calibrations':sum(x['op']=='calibrate' for x in cmds)==40,'one_sixty_routes':sum(x['op']=='route' for x in cmds)==160,'forty_acquisitions':sum(x['op']=='acquire' for x in cmds)==40,'real_OS_TCP_boundary_used':port>0 and host=='127.0.0.1','all_240_ACKed':len(transcript['events'])==240 and all(e['response']['body']['ack'] for e in transcript['events']),'hash_chain_and_HMAC_verify':verify_transcript(transcript,key,manifest_sha),'witness_positive':analysis['decision']=='contextual_positive' and 9.9<analysis['witness_W']<10.2,'no_CF_label':analysis['contextual_fraction_field'] is None,'bad_CRC_fails_closed':bad_crc==(True,'crc_or_json_failure'),'missing_calibration_fails_closed':missing_cal==(True,'calibration_required'),'external_key_file_mode_0600':stat.S_IMODE(keyfile.stat().st_mode)==0o600,'manifest_has_commitment_not_key':commit in canon(manifest).decode() and key.hex() not in canon(manifest).decode(),'offline_unblinding_verifies':all([unblind['key_commitment_verified'],unblind['transcript_verified']]),'real_hardware_not_claimed':manifest['real_hardware_connected'] is False};assert all(checks.values()),(checks,bad_crc,missing_cal)
    for name,obj in [('manifest',manifest),('analysis',analysis),('unblinding_receipt',unblind)]: (HW/f'w33_pass1090_{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
    summary={'schema':'w33.pass1090.transcript_summary.v1','event_count':len(transcript['events']),'chain_root':transcript['chain_root'],'signature_hmac_sha256':transcript['signature_hmac_sha256'],'request_response_protocol':VERSION,'all_ACK':True};(HW/'w33_pass1090_transcript_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    out={'schema':'w33.pass1090.controller_protocol_boundary.v1','status':'PASS','headline':'The W33 acquisition schedule crossed a real operating-system TCP controller boundary using a versioned, CRC-framed, sequence-locked protocol. All 240 commands were ACKed, every acquisition was calibration-bound, the transcript was hash-chained and HMAC-signed, and malformed CRC or missing-calibration commands failed closed. This is a loopback controller certification, not a claim that physical optical hardware was connected.','manifest':manifest,'analysis':analysis,'negative_probes':{'bad_crc':bad_crc,'missing_calibration':missing_cal},'transcript_summary':summary,'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'artifacts':['hardware/w33_pass1090_manifest.json','hardware/w33_pass1090_analysis.json','hardware/w33_pass1090_unblinding_receipt.json','hardware/w33_pass1090_transcript_summary.json'],'seconds':time.time()-started,'scope':'Real TCP transport and production-shaped protocol boundary exercised against a loopback reference controller. A physical vendor controller remains an external deployment prerequisite.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');keyfile.unlink();print(json.dumps(out,indent=2))
if __name__=='__main__':main()
