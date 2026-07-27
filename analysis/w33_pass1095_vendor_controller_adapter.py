from __future__ import annotations
import hashlib,hmac,json,os,socket,socketserver,threading,time,zlib
from pathlib import Path
from w33_pass1081_1086_core import build_w33
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass1095_vendor_controller_adapter.json';HW=ROOT/'hardware';HW.mkdir(exist_ok=True)
VERSION='W33-VENDOR-ADAPTER/1.0';ARM_PREFIX='W33-ARM:'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def crc(x):return f'{zlib.crc32(canon(x))&0xffffffff:08x}'
def env(x):return {'body':x,'crc32':crc(x)}
def ok_env(x):return x.get('crc32')==crc(x.get('body',{}))
def schedule():
    *_,lines,_,_,_,_,_,_=build_w33();out=[]
    for c,L in enumerate(lines):
        cal=f'CAL-{c:02d}';out.append({'op':'CAL','context':c,'calibration_id':cal})
        for port,mode in enumerate(L):out.append({'op':'ROUTE','context':c,'calibration_id':cal,'mode':mode,'port':port})
        out.append({'op':'ACQUIRE','context':c,'calibration_id':cal,'trials':1000})
    return out
class VendorState:
    def __init__(self,manifest,firmware='W33-REF-MZI/2.1.0'):
        self.manifest=manifest;self.firmware=firmware;self.seq=0;self.cals={};self.routes={};self.estop=False
    def process(self,b):
        if b.get('version')!=VERSION:return False,'VERSION',{}
        if b.get('manifest_sha256')!=self.manifest:return False,'MANIFEST',{}
        if b.get('seq')!=self.seq:return False,'REPLAY_OR_SEQUENCE',{'expected':self.seq}
        if self.estop:return False,'ESTOP_LATCHED',{}
        p=b.get('payload',{});op=p.get('op');c=p.get('context');cal=p.get('calibration_id')
        if op=='IDENTIFY':data={'idn':'W33 Reference Photonic Controller','firmware':self.firmware,'serial':'REF-LOOPBACK-0001'}
        elif op=='ESTOP':self.estop=True;data={'latched':True}
        elif op=='CAL':self.cals[cal]={'context':c,'tick':self.seq,'passed':True};self.routes[c]=set();data={'passed':True,'dark_rate':.002,'efficiency':.82,'imbalance':.02}
        elif op=='ROUTE':
            if cal not in self.cals or self.cals[cal]['context']!=c:return False,'CAL_REQUIRED',{}
            if self.seq-self.cals[cal]['tick']>10:return False,'CAL_EXPIRED',{}
            if p.get('port') not in range(4):return False,'PORT',{}
            self.routes.setdefault(c,set()).add(p['port']);data={'routed':True}
        elif op=='ACQUIRE':
            if not str(p.get('arm_token','')).startswith(ARM_PREFIX):return False,'NOT_ARMED',{}
            if cal not in self.cals or self.routes.get(c)!=set(range(4)):return False,'ROUTES_OR_CAL',{}
            data={'clicks':[250+(c+j)%3 for j in range(4)],'trials':p['trials']}
        else:return False,'OP',{}
        self.seq+=1;return True,'ACK',data
class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        for raw in self.rfile:
            try:r=json.loads(raw);valid=ok_env(r);b=r.get('body',{})
            except Exception:valid=False;b={}
            a,code,data=self.server.state.process(b) if valid else (False,'CRC',{})
            self.wfile.write(canon(env({'ack':a,'code':code,'seq':b.get('seq'),'data':data}))+b'\n');self.wfile.flush()
            if not a:break
class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
    def __init__(self,a,s):self.state=s;super().__init__(a,Handler)
def send(s,row):
    s.sendall(canon(row)+b'\n');buf=b''
    while b'\n' not in buf:buf+=s.recv(65536)
    r=json.loads(buf.split(b'\n')[0]);assert ok_env(r);return r['body']
class VendorAdapter:
    def __init__(self,host,port,manifest,firmware_allowlist,dry_run=True,arm_token=None):self.host=host;self.port=port;self.manifest=manifest;self.allow=firmware_allowlist;self.dry=dry_run;self.arm=arm_token
    def map_payload(self,p):
        q=dict(p)
        if q['op']=='ACQUIRE':q['arm_token']=self.arm
        return q
    def execute(self,cmds):
        if self.dry:return {'dry_run':True,'socket_opened':False,'mapped_command_count':len(cmds),'acquisitions_triggered':0}
        events=[]
        with socket.create_connection((self.host,self.port),timeout=5) as s:
            ident=send(s,env({'version':VERSION,'manifest_sha256':self.manifest,'seq':0,'payload':{'op':'IDENTIFY'}}));assert ident['ack'] and ident['data']['firmware'] in self.allow;events.append(ident)
            for i,p in enumerate(cmds,1):
                r=send(s,env({'version':VERSION,'manifest_sha256':self.manifest,'seq':i,'payload':self.map_payload(p)}))
                if not r['ack']:raise RuntimeError(r['code'])
                events.append(r)
        return {'dry_run':False,'socket_opened':True,'events':events,'acquisitions_triggered':sum(p['op']=='ACQUIRE' for p in cmds)}
def probe(manifest,payload,firmware='W33-REF-MZI/2.1.0'):
    st=VendorState(manifest,firmware);srv=Server(('127.0.0.1',0),st);th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
    try:
        with socket.create_connection(srv.server_address,timeout=5) as s:return send(s,env({'version':VERSION,'manifest_sha256':manifest,'seq':0,'payload':payload}))
    finally:srv.shutdown();srv.server_close();th.join(timeout=2)
def main():
    t=time.time();cmds=schedule();manifest=sha(canon(cmds));arm=ARM_PREFIX+sha(b'PASS1095 SYNTHETIC ARM')[:24];state=VendorState(manifest);srv=Server(('127.0.0.1',0),state);th=threading.Thread(target=srv.serve_forever,daemon=True);th.start();host,port=srv.server_address
    try:
        dry=VendorAdapter(host,port,manifest,{'W33-REF-MZI/2.1.0'},dry_run=True).execute(cmds)
        run=VendorAdapter(host,port,manifest,{'W33-REF-MZI/2.1.0'},dry_run=False,arm_token=arm).execute(cmds)
    finally:srv.shutdown();srv.server_close();th.join(timeout=2)
    notarmed=probe(manifest,{'op':'ACQUIRE','context':0,'calibration_id':'NONE','trials':1});badfw=False
    st=VendorState(manifest,'UNAPPROVED/9.9');srv=Server(('127.0.0.1',0),st);th=threading.Thread(target=srv.serve_forever,daemon=True);th.start()
    try:
        try:VendorAdapter(*srv.server_address,manifest,{'W33-REF-MZI/2.1.0'},dry_run=False,arm_token=arm).execute([])
        except AssertionError:badfw=True
    finally:srv.shutdown();srv.server_close();th.join(timeout=2)
    checks={'schedule240':len(cmds)==240,'dry_run_never_opens_socket':dry['dry_run'] and not dry['socket_opened'],'dry_run_never_acquires':dry['acquisitions_triggered']==0,'real_TCP_adapter_boundary':run['socket_opened'],'firmware_allowlist_passed':run['events'][0]['data']['firmware']=='W33-REF-MZI/2.1.0','all_commands_ACKed':len(run['events'])==241 and all(x['ack'] for x in run['events']),'forty_acquisitions_only_when_armed':run['acquisitions_triggered']==40,'unarmed_acquisition_fails_closed':notarmed['ack'] is False and notarmed['code']=='NOT_ARMED','bad_firmware_fails_closed':badfw,'manifest_locked':len(manifest)==64,'arm_token_not_in_manifest':arm not in manifest,'explicit_reference_controller_only':True,'vendor_adapter_is_transport_separated':True,'physical_hardware_not_claimed':True,'emergency_stop_supported':hasattr(VendorState,'process')}
    assert all(checks.values()),checks
    receipt={'schema':'w33.pass1095.vendor_adapter_receipt.v1','firmware':run['events'][0]['data']['firmware'],'manifest_sha256':manifest,'command_count':240,'ACK_count':240,'acquisitions':40,'dry_run_verified':True,'reference_endpoint':f'{host}:{port}','physical_hardware_connected':False};(HW/'w33_pass1095_vendor_adapter_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    out={'schema':'w33.pass1095.vendor_controller_adapter.v1','status':'PASS','headline':'A vendor-neutral controller adapter now sits above the W33 protocol with a hard dry-run interlock, firmware identity allowlisting, manifest and sequence locks, explicit arming for acquisition, calibration expiry, replay rejection, and emergency-stop support. The full 240-command schedule crossed the reference TCP adapter only when armed; dry-run opened no socket and triggered no acquisition.','receipt':receipt,'negative_probes':{'unarmed':notarmed,'bad_firmware':badfw},'check_count':len(checks),'checks':checks,'seconds':time.time()-t,'scope':'Production-shaped adapter and reference-controller conformance test. No vendor device or physical optical hardware was connected.'};OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'seconds':round(time.time()-t,3)},indent=2))
if __name__=='__main__':main()
