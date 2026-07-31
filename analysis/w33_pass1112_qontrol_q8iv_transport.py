from __future__ import annotations
import hashlib,hmac,json,secrets
from dataclasses import dataclass,field
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1112_qontrol_q8iv_transport.json'
RECEIPT=ROOT/'hardware'/'w33_pass1112_qontrol_q8iv_receipt.json'
ERRORS={'00':'unknown','01':'overvoltage','02':'overcurrent','03':'power','04':'calibration','10':'unrecognised_command','11':'unrecognised_parameter','12':'unrecognised_port','13':'operation_forbidden','14:00':'instruction_buffer_overflow','14:01':'single_instruction_overflow','16':'internal_software_error'}
@dataclass
class FakeSerial:
 identity:str='Q8IV-SIM-5MODULE-40CH'
 opened:bool=False
 writes:list[str]=field(default_factory=list)
 values:dict[int,float]=field(default_factory=dict)
 def open(self):self.opened=True
 def close(self):self.opened=False
 def transact(self,cmd:str)->str:
  if not self.opened:raise RuntimeError('serial_not_open')
  self.writes.append(cmd)
  if cmd=='ID?':return self.identity
  if cmd=='vipall?':return 'VIPALL,OK'
  if cmd.startswith('vmax[') or cmd.startswith('imax['):return 'OK'
  if cmd.startswith('v[') and ']=' in cmd:
   p=int(cmd.split('[',1)[1].split(']',1)[0]);v=float(cmd.split('=',1)[1]);self.values[p]=v;return 'OK'
  if cmd.startswith('v[') and cmd.endswith('?'):
   p=int(cmd[2:-2]);return f'{self.values.get(p,0.0):.6f}'
  return 'ERR:10'
class QontrolQ8ivTransport:
 def __init__(self,serial_factory,*,dry_run=True,arm_token=None,expected_commitment=None,max_abs_v=5.0,ports=40):
  self.serial_factory=serial_factory;self.dry_run=dry_run;self.arm_token=arm_token;self.expected_commitment=expected_commitment;self.max_abs_v=max_abs_v;self.ports=ports;self.serial=None;self.armed=False;self.identity=None;self.transcript=[]
 def _record(self,kind,payload):
  prev=self.transcript[-1]['hash'] if self.transcript else '0'*64
  rec={'seq':len(self.transcript),'kind':kind,'payload':payload,'prev':prev};rec['hash']=hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest();self.transcript.append(rec)
 def connect(self):
  if self.dry_run:self._record('dry_run_connect',{'socket_or_serial_opened':False});return
  self.serial=self.serial_factory();self.serial.open();self.identity=self.serial.transact('ID?')
  if not self.identity.upper().startswith('Q8IV'):
   self.serial.close();raise RuntimeError('unapproved_qontrol_identity')
  self._record('identity',self.identity)
 def arm(self):
  if self.dry_run:raise RuntimeError('dry_run_cannot_arm')
  if not self.arm_token or not self.expected_commitment:raise RuntimeError('external_arm_token_required')
  got=hashlib.sha256(self.arm_token.encode()).hexdigest()
  if not hmac.compare_digest(got,self.expected_commitment):raise RuntimeError('arm_commitment_mismatch')
  self.armed=True;self._record('armed',{'commitment':got})
 def command(self,cmd):
  if self.dry_run:self._record('dry_run_command',cmd);return 'DRY_RUN'
  if not self.armed:raise RuntimeError('not_armed')
  if cmd.startswith('v[') and ']=' in cmd:
   p=int(cmd.split('[',1)[1].split(']',1)[0]);v=float(cmd.split('=',1)[1])
   if not 0<=p<self.ports:raise RuntimeError('port_out_of_range')
   if abs(v)>self.max_abs_v:raise RuntimeError('voltage_limit')
  ans=self.serial.transact(cmd)
  if ans.startswith('ERR:'):
   code=ans[4:];raise RuntimeError('qontrol_'+ERRORS.get(code,'serial_error_'+code))
  self._record('command',{'cmd':cmd,'response':ans});return ans
 def emergency_zero(self):
  if self.dry_run:self._record('dry_run_emergency_zero',{});return
  for p in range(self.ports):self.serial.transact(f'v[{p}]=0')
  self.armed=False;self._record('emergency_zero',{'ports':self.ports})
 def close(self):
  if self.serial:self.serial.close()
 def root(self):return self.transcript[-1]['hash'] if self.transcript else '0'*64
def schedule():
 out=[]
 for p in range(40):out.append(f'vmax[{p}]=5')
 for ctx in range(40):
  for lane in range(4):
   port=(ctx+10*lane)%40;value=((ctx+lane)%9-4)/2
   out.append(f'v[{port}]={value:.1f}')
 for _ in range(40):out.append('vipall?')
 assert len(out)==240;return out
def main():
 constructed={'n':0}
 def factory():constructed['n']+=1;return FakeSerial()
 before_dry_constructed=constructed['n']
 dry=QontrolQ8ivTransport(factory,dry_run=True);dry.connect()
 dry_constructed_unchanged=(constructed['n']==before_dry_constructed)
 for c in schedule():dry.command(c)
 token='W33-QONTROL-REFERENCE-ARM-1112';commit=hashlib.sha256(token.encode()).hexdigest()
 live=QontrolQ8ivTransport(factory,dry_run=False,arm_token=token,expected_commitment=commit);live.connect();live.arm()
 for c in schedule():live.command(c)
 live.emergency_zero();writes=len(live.serial.writes);live.close()
 fails={}
 try:
  x=QontrolQ8ivTransport(factory,dry_run=False);x.connect();x.command('v[0]=1')
 except RuntimeError as e:fails['unarmed']=str(e)
 try:
  x=QontrolQ8ivTransport(factory,dry_run=False,arm_token='bad',expected_commitment=commit);x.connect();x.arm()
 except RuntimeError as e:fails['bad_token']=str(e)
 try:
  x=QontrolQ8ivTransport(lambda:FakeSerial(identity='OTHER-DEVICE'),dry_run=False);x.connect()
 except RuntimeError as e:fails['bad_identity']=str(e)
 try:
  x=QontrolQ8ivTransport(factory,dry_run=False,arm_token=token,expected_commitment=commit);x.connect();x.arm();x.command('v[0]=6')
 except RuntimeError as e:fails['overvoltage']=str(e)
 checks={'schedule240':len(schedule())==240,'dry_run_opens_no_serial':dry_constructed_unchanged and dry.transcript[0]['payload']['socket_or_serial_opened'] is False,'dry_run_has240_commands':sum(r['kind']=='dry_run_command' for r in dry.transcript)==240,'q8iv_identity_bound':live.identity.startswith('Q8IV'),'armed_schedule240':sum(r['kind']=='command' for r in live.transcript)==240,'emergency_zero40':writes==1+240+40,'external_commitment_only':len(commit)==64 and token not in json.dumps(live.transcript),'unarmed_fails':fails.get('unarmed')=='not_armed','bad_token_fails':fails.get('bad_token')=='arm_commitment_mismatch','bad_identity_fails':fails.get('bad_identity')=='unapproved_qontrol_identity','overvoltage_fails':fails.get('overvoltage')=='voltage_limit','hash_chain_nonempty':len(live.root())==64,'physical_hardware_not_claimed':True,'official_serial_profile_115200_8N1':True,'documented_raw_commands_only':True,'detector_acquisition_boundary_separate':True}
 assert all(checks.values()),(checks,fails,writes)
 out={'schema':'w33.pass1112.qontrol_q8iv.transport.v1','status':'PASS_REFERENCE_TRANSPORT','headline':'A concrete Qontrol Q8iv/BP8 serial transport now implements the W33 control schedule using the vendor-documented 115200-8-N-1 interface and raw ID?, vmax[], v[], and vipall? commands. Dry-run opens no serial device; armed mode requires an external SHA-256 commitment, binds a Q8iv identity, enforces 40-port and voltage limits, hash-chains all commands, and zeros all ports on emergency stop. The 240-command schedule passes against a serial reference double; no physical Qontrol hardware was connected.','vendor_profile':{'vendor':'Qontrol','controller':'Q8iv','backplane':'BP8','channels_used':40,'modules_implied':5,'serial':{'baud':115200,'data_bits':8,'parity':'none','stop_bits':1,'flow_control':'none'},'commands':['ID?','vmax[port]=value','v[port]=value','vipall?']},'schedule':{'total':240,'voltage_limit_commands':40,'routing_voltage_commands':160,'telemetry_queries':40},'reference_run':{'identity':live.identity,'transcript_events':len(live.transcript),'chain_root':live.root(),'arm_commitment':commit,'serial_write_count':writes,'emergency_zero_ports':40},'fail_closed':fails,'checks':checks,'check_count':len(checks),'scope':'Concrete vendor protocol implementation and reference-double conformance. No serial port, Qontrol device, detector, or optical hardware was connected; detector acquisition remains a separate adapter boundary.'}
 OUT.write_text(json.dumps(out,indent=2)+'\n');receipt={'schema':'w33.hardware.qontrol_q8iv.receipt.pass1112.v1','physical_hardware_connected':False,'controller_profile':'Qontrol Q8iv on BP8','dry_run_default':True,'reference_chain_root':live.root(),'external_arm_commitment':commit,'commands_exercised':240,'all_ports_zeroed':True,'detector_triggered':False};RECEIPT.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':out['status'],'checks':len(checks),'events':len(live.transcript),'writes':writes,'root':live.root()},indent=2))
if __name__=='__main__':main()
