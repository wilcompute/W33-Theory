from __future__ import annotations
import hashlib,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1105_keysight_n7731a_transport.json';HW=ROOT/'hardware'/'w33_pass1105_keysight_n7731a_receipt.json'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x if isinstance(x,bytes) else canon(x)).hexdigest()
def schedule():
 cmds=[]
 for ctx in range(40):
  cal=f'CAL-W33-{ctx:02d}-N7731A';cmds.append({'op':'calibrate','context':ctx,'calibration_id':cal})
  for port in range(4):cmds.append({'op':'route','context':ctx,'mode':(ctx*4+port)%40,'detector_port':port,'calibration_id':cal})
  cmds.append({'op':'acquire','context':ctx,'trials':1000,'calibration_id':cal})
 return cmds
class KeysightN7731AEmulator:
 def __init__(self,idn='Keysight Technologies,N1000A,MY00000000,A.07.00',firmware='A.07.00'):self.idn=idn;self.firmware=firmware;self.io_count=0;self.commands=[];self.stopped=False
 def transact(self,cmd):
  if self.stopped:raise RuntimeError('EMERGENCY_STOPPED')
  self.io_count+=1;self.commands.append(cmd)
  if cmd=='*IDN?':return self.idn
  if cmd==':CONFigure:SWITch:ALL?':return '"N7731A (Switch 1)",ON'
  if cmd.startswith(':CONFigure:SWITch:ACTive ') or cmd.startswith(':CONFigure:PORT:CONNect '):return 'OK'
  if cmd=='ABORt':self.stopped=True;return 'OK'
  raise RuntimeError('UNSUPPORTED_SCPI')
class KeysightN7731ATransport:
 PROFILE='Keysight FlexOTO / N7731A two-channel 1x4 optical switch';ALLOWED_IDN_PREFIX='Keysight Technologies,N1000A,';ALLOWED_FIRMWARE={'A.07.00'}
 def __init__(self,endpoint,dry_run=True):self.endpoint=endpoint;self.dry_run=dry_run
 def identify(self):
  if self.dry_run:return {'idn':'DRY-RUN','firmware':'DRY-RUN','approved':False,'io':False}
  idn=self.endpoint.transact('*IDN?');fw=idn.rsplit(',',1)[-1];return {'idn':idn,'firmware':fw,'approved':idn.startswith(self.ALLOWED_IDN_PREFIX) and fw in self.ALLOWED_FIRMWARE,'io':True}
 def activate(self):return 'DRY-RUN' if self.dry_run else self.endpoint.transact(':CONFigure:SWITch:ACTive "N7731A (Switch 1)",ON')
 def connect_port(self,port):
  cmd=f':CONFigure:PORT:CONNect "DUT Fixture 1","{port+1}","N7731A (Switch 1)","{port+1}"';return {'scpi':cmd,'response':'DRY-RUN' if self.dry_run else self.endpoint.transact(cmd)}
 def verify_switch(self):return 'DRY-RUN' if self.dry_run else self.endpoint.transact(':CONFigure:SWITch:ALL?')
 def emergency_stop(self):return 'DRY-RUN' if self.dry_run else self.endpoint.transact('ABORt')
class W33VendorAdapter:
 def __init__(self,transport,manifest_sha,arm_commitment,ttl_ticks=6):self.t=transport;self.manifest_sha=manifest_sha;self.arm_commitment=arm_commitment;self.ttl=ttl_ticks;self.seq=0;self.cals={};self.routes={};self.armed=False;self.events=[];self.stopped=False
 def arm(self,token):
  if sha(token.encode())!=self.arm_commitment:raise RuntimeError('BAD_ARM_TOKEN')
  if self.t.dry_run:raise RuntimeError('DRY_RUN_CANNOT_ARM')
  ident=self.t.identify()
  if not ident['approved']:raise RuntimeError('FIRMWARE_NOT_ALLOWLISTED')
  self.t.activate();self.armed=True;self.ident=ident
 def process(self,seq,manifest_sha,payload):
  if self.stopped:raise RuntimeError('EMERGENCY_STOPPED')
  if seq!=self.seq:raise RuntimeError('REPLAY_OR_SEQUENCE_MISMATCH')
  if manifest_sha!=self.manifest_sha:raise RuntimeError('MANIFEST_MISMATCH')
  op=payload['op'];ctx=payload['context'];cal=payload['calibration_id'];data={}
  if self.t.dry_run:data=self.t.connect_port(payload['detector_port']) if op=='route' else {'mapped_only':True,'operation':op}
  elif op=='calibrate':
   if not self.armed:raise RuntimeError('NOT_ARMED')
   sw=self.t.verify_switch();self.cals[cal]={'context':ctx,'tick':seq,'switch_query':sw};self.routes[ctx]=set();data={'calibration_receipt':cal,'switch_query':sw}
  elif op=='route':
   if not self.armed:raise RuntimeError('NOT_ARMED')
   if cal not in self.cals or self.cals[cal]['context']!=ctx:raise RuntimeError('CALIBRATION_REQUIRED')
   if seq-self.cals[cal]['tick']>self.ttl:raise RuntimeError('CALIBRATION_EXPIRED')
   data=self.t.connect_port(payload['detector_port']);self.routes.setdefault(ctx,set()).add(payload['detector_port'])
  elif op=='acquire':
   if not self.armed:raise RuntimeError('NOT_ARMED')
   if cal not in self.cals or self.cals[cal]['context']!=ctx:raise RuntimeError('CALIBRATION_REQUIRED')
   if self.routes.get(ctx)!=set(range(4)):raise RuntimeError('FOUR_ROUTES_REQUIRED')
   data={'detector_handoff':True,'context':ctx,'trials':payload['trials'],'switch_state':self.t.verify_switch(),'physical_clicks':None}
  else:raise RuntimeError('UNKNOWN_OPERATION')
  ev={'seq':seq,'payload':payload,'data':data};ev['event_hash']=sha(ev);self.events.append(ev);self.seq+=1;return ev
 def emergency_stop(self):self.stopped=True;return self.t.emergency_stop()
def expect_error(fn,code):
 try:fn();return False
 except RuntimeError as e:return str(e)==code
def main():
 started=time.time();cmds=schedule();manifest={'schema':'w33.pass1105.keysight_n7731a.manifest.v1','profile':KeysightN7731ATransport.PROFILE,'command_count':len(cmds),'physical_hardware_connected':False};msha=sha(manifest);token='PASS1105-EXTERNAL-ARM-TOKEN';commit=sha(token.encode());dry_ep=KeysightN7731AEmulator();dry=W33VendorAdapter(KeysightN7731ATransport(dry_ep,True),msha,commit)
 for i,c in enumerate(cmds):dry.process(i,msha,c)
 ep=KeysightN7731AEmulator();ad=W33VendorAdapter(KeysightN7731ATransport(ep,False),msha,commit);ad.arm(token)
 for i,c in enumerate(cmds):ad.process(i,msha,c)
 bad_arm=expect_error(lambda:W33VendorAdapter(KeysightN7731ATransport(KeysightN7731AEmulator(),False),msha,commit).arm('WRONG'),'BAD_ARM_TOKEN');bad_fw=expect_error(lambda:W33VendorAdapter(KeysightN7731ATransport(KeysightN7731AEmulator(idn='Keysight Technologies,N1000A,MY0,A.06.00'),False),msha,commit).arm(token),'FIRMWARE_NOT_ALLOWLISTED');replay=expect_error(lambda:ad.process(0,msha,cmds[0]),'REPLAY_OR_SEQUENCE_MISMATCH');unarmed=W33VendorAdapter(KeysightN7731ATransport(KeysightN7731AEmulator(),False),msha,commit);unarmed_acq=expect_error(lambda:unarmed.process(0,msha,{'op':'acquire','context':0,'trials':1,'calibration_id':'NONE'}),'NOT_ARMED');expired=W33VendorAdapter(KeysightN7731ATransport(KeysightN7731AEmulator(),False),msha,commit,ttl_ticks=1);expired.arm(token);expired.process(0,msha,{'op':'calibrate','context':0,'calibration_id':'C'});expired.process(1,msha,{'op':'route','context':0,'mode':0,'detector_port':0,'calibration_id':'C'});expired_cal=expect_error(lambda:expired.process(2,msha,{'op':'route','context':0,'mode':1,'detector_port':1,'calibration_id':'C'}),'CALIBRATION_EXPIRED');stop=W33VendorAdapter(KeysightN7731ATransport(KeysightN7731AEmulator(),False),msha,commit);stop.arm(token);stop.emergency_stop();estop=expect_error(lambda:stop.process(0,msha,cmds[0]),'EMERGENCY_STOPPED');acq=[e for e in ad.events if e['payload']['op']=='acquire']
 checks={'schedule240':len(cmds)==240,'forty_calibrations':sum(c['op']=='calibrate' for c in cmds)==40,'one_sixty_routes':sum(c['op']=='route' for c in cmds)==160,'forty_acquisition_handoffs':len(acq)==40,'dry_run_zero_IO':dry_ep.io_count==0,'dry_run_never_arms':not dry.armed,'dry_run_has_no_clicks':all(e['data'].get('physical_clicks') is None for e in dry.events if e['payload']['op']=='acquire'),'official_profile_commands_emitted':any(x.startswith(':CONFigure:PORT:CONNect ') for x in ep.commands) and ':CONFigure:SWITch:ALL?' in ep.commands,'all_240_commands_processed':len(ad.events)==240,'approved_firmware_bound':ad.ident['approved'],'external_arm_commitment_verified':ad.armed,'wrong_arm_token_fails_closed':bad_arm,'unapproved_firmware_fails_closed':bad_fw,'replay_fails_closed':replay,'unarmed_acquisition_fails_closed':unarmed_acq,'expired_calibration_fails_closed':expired_cal,'emergency_stop_fails_closed':estop,'no_physical_measurement_claim':all(x['data']['physical_clicks'] is None for x in acq)};assert all(checks.values()),checks
 receipt={'schema':'w33.pass1105.keysight_n7731a.receipt.v1','status':'PASS','profile':KeysightN7731ATransport.PROFILE,'manifest_sha256':msha,'arm_commitment_sha256':commit,'processed_commands':len(ad.events),'scpi_io_count':ep.io_count,'scpi_transcript_sha256':sha(ep.commands),'acquisition_handoffs':len(acq),'physical_hardware_connected':False,'physical_click_data_recorded':False};HW.write_text(json.dumps(receipt,indent=2)+'\n');out={'schema':'w33.pass1105.keysight_n7731a_transport.v1','status':'PASS','headline':'A concrete Keysight FlexOTO/N7731A SCPI switch transport now implements the vendor boundary behind the W33 adapter. It preserves dry-run, firmware allowlisting, external arming, immutable manifests, sequence locks, calibration expiry, four-port routing, replay rejection, and emergency stop. The 240-command schedule passed against a reference SCPI endpoint; acquisitions are explicit detector-service handoffs, not fabricated switch measurements.','device_profile':{'vendor':'Keysight','instrument_family':'FlexOTO','switch_module':'N7731A two-channel 1x4 optical switch','documented_SCPI_surfaces':['*IDN?',':CONFigure:SWITch:ACTive',':CONFigure:SWITch:ALL?',':CONFigure:PORT:CONNect']},'receipt':receipt,'negative_probes':{'wrong_arm_token':bad_arm,'unapproved_firmware':bad_fw,'replay':replay,'unarmed_acquisition':unarmed_acq,'expired_calibration':expired_cal,'emergency_stop':estop},'check_count':len(checks),'checks':checks,'seconds':time.time()-started,'scope':'Device-specific command encoder and interlock conformance test against a reference endpoint. No Keysight instrument, detector, or optical hardware was connected.'};OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'processed':len(ad.events),'io':ep.io_count},indent=2))
if __name__=='__main__':main()
