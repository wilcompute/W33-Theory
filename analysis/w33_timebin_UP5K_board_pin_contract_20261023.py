#!/usr/bin/env python3
"""Fail-closed real-board PCF gate for W33 time-bin recursion controller.

Never infer physical package pads from unpinned nextpnr PNR. Requires
board-datasheet-backed manifest, exact port enumeration, PCF uniqueness,
and cross-checked voltage-domain notes supplied by hardware operator.
This cannot certify physical I/O electrical safety or replace FPGA tests.
"""
import argparse,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RTL='hardware/w33_single_photon_timebin_recursion_guard.sv'
NETLIST='data/w33_single_photon_timebin_recursion_guard_ice40_20261023.json'
def pins_from_yosys_json(netlist):
    data=json.loads(Path(netlist).read_text())
    module=data['modules']['w33_single_photon_timebin_recursion_guard']
    result=[]
    for name,obj in module['ports'].items():
        bits=obj['bits'];offset=int(obj.get('offset',0))
        if len(bits)==1:result.append(name)
        else:result.extend(f'{name}[{i+offset}]' for i in range(len(bits)))
    if len(result)!=len(set(result)):raise ValueError('duplicate ports')
    return sorted(result)
def make_manifest(netlist):
    pins=pins_from_yosys_json(netlist)
    return {'schema':'w33.timebin.fpga_board_port_contract.v1',
      'module':'w33_single_photon_timebin_recursion_guard',
      'fpga_family':'iCE40UP5K','package':'sg48',
      'unassigned_ports':pins,'io_count':len(pins),
      'real_board_product':None,'board_document_identifier':None,
      'board_document_sha256':None,'board_io_voltage':None,
      'status':'INCOMPLETE: NO ACTUAL PINS CLAIMED',
      'safety':'Electrical I/O voltage, level shifting, optoelectronic actuators and timing must be approved separately'}
def parse_pcf(path):
    out={};used={}
    for n,line in enumerate(Path(path).read_text().splitlines(),1):
        line=line.split('#',1)[0].strip()
        if not line:continue
        tok=line.split()
        if len(tok)!=3 or tok[0]!='set_io':raise ValueError(f'unsupported PCF command at line {n}')
        key,pin=tok[1:]
        if key in out:raise ValueError(f'duplicate port {key}')
        if pin in used:raise ValueError(f'pin reused {pin} for {key} and {used[pin]}')
        if not re.fullmatch(r'[A-Za-z0-9_]+(?:\[\d+\])?',key):raise ValueError('illegal pin expression')
        out[key]=pin;used[pin]=key
    return out
def approve(netlist,manifest_path,pcf_path):
    manifest=json.loads(Path(manifest_path).read_text())
    if manifest.get('status')!='APPROVED_BY_HARDWARE_OPERATOR':
        raise ValueError('Board metadata not APPROVED_BY_HARDWARE_OPERATOR')
    for f in ('real_board_product','board_document_identifier','board_document_sha256','board_io_voltage'):
        if not manifest.get(f):raise ValueError(f'missing actual board evidence: {f}')
    if len(manifest['board_document_sha256'])!=64:raise ValueError('board document SHA256 invalid')
    expected=pins_from_yosys_json(netlist)
    if sorted(manifest['unassigned_ports'])!=expected:raise ValueError('netlist/manifest mismatch')
    assigned=parse_pcf(pcf_path)
    if sorted(assigned)!=expected:
        missing=sorted(set(expected)-set(assigned))
        unexpected=sorted(set(assigned)-set(expected))
        raise ValueError(f'unpinned IO missing={missing}; unexpected={unexpected}')
    assert len(set(assigned.values()))==len(assigned)
    return {'schema':'w33.timebin.pcf_syntax_verified.v1',
      'board':manifest['real_board_product'],'ports':len(assigned),
      'pcf_sha256':hashlib.sha256(Path(pcf_path).read_bytes()).hexdigest(),
      'level':'SYNTACTIC_ONLY; requires vendor pad legality, voltage-domain, timing, hold and board bringup'}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--netlist',type=Path,default=ROOT/NETLIST)
    ap.add_argument('--manifest',type=Path)
    ap.add_argument('--pcf',type=Path)
    ap.add_argument('--out',type=Path,default=ROOT/'data/w33_timebin_UP5K_board_pin_contract_20261023.json')
    args=ap.parse_args()
    if args.manifest and args.pcf: obj=approve(args.netlist,args.manifest,args.pcf)
    elif args.manifest or args.pcf:ap.error('--pcf and --manifest required together')
    else:obj=make_manifest(args.netlist)
    args.out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    print('PASS contract generated; physical board approved:',obj.get('status')=='APPROVED_BY_HARDWARE_OPERATOR')
