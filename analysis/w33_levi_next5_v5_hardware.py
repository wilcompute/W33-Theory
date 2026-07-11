#!/usr/bin/env python3
"""Vendor adapters, FPGA reduction, and explicit 40-27-72-240 replay."""
from functools import lru_cache
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(HERE))
from w33_levi_next5_v5_common import sha256_json
from w33_levi_next5_v5_hardware_vendors import SwabianAdapter,QuTAGAdapter,Buf,SModule,QFake
from w33_levi_next5_v5_hardware_core import Reducer,software,stream,route,rtl_contract
import w33_levi_next5_v5_lanes as lanes

@lru_cache(maxsize=1)
def analyze():
    tags=stream();sample=tags[:128]
    sw=SwabianAdapter(SModule(sample),256);swt,sm,so=sw.read();sw.close();qt,ql,qo=QuTAGAdapter(QFake(sample)).read()
    expected=software(tags);red=Reducer();actual=[];i=cycle=0
    while i<len(tags) or red.pending is not None:
        ready=cycle%29 not in (0,1,2);valid=i<len(tags) and red.ready;x=tags[i] if valid else None;y=red.cycle(valid,x,ready)
        if valid:i+=1
        if y is not None:actual.append(y)
        cycle+=1
    tail=red.flush()
    if tail is not None:actual.append(tail)
    routes=route(actual,lanes.analyze())
    _,lost,qprobe=QuTAGAdapter(QFake(tags[:4],3)).read();probe=SwabianAdapter(SModule(tags[:4]),8)
    probe.stream=type('X',(),{'getData':lambda self:Buf(tags[:4],2),'stop':lambda self:None})();_,miss,sprobe=probe.read();probe.close()
    rtl=rtl_contract(ROOT);checks={
        'swabian_sdk_contract':[(x.t,x.ch,x.event_type) for x in swt]==[(x.t,x.ch,x.event_type) for x in sample] and sm==0 and not so,
        'qutag_sdk_contract':[(x.t,x.ch) for x in qt]==[(x.t,x.ch) for x in sample] and ql==0 and not qo,
        'vendor_loss_is_fail_closed':qprobe and sprobe and lost==3 and miss==2,
        'bounded_reducer_matches_software':actual==expected,'backpressure_exercised':red.backpressure>0,
        'stream_over_one_million_events':len(tags)>1_000_000,
        'all_frames_routed_40_27_72_240':len(routes)==len(actual)==256 and all(not x['overflow'] for x in routes),
        'all_payload_roots_typed':all(0<=x['payload_root240']<240 for x in routes),'rtl_contract_present':rtl['required_tokens']}
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
        'vendor_adapters':{'swabian':{'api':'createTimeTagger + TimeTagStream.getData','sample_events':len(swt),'missed':sm},'qutag':{'api':'getLastTimestamps(reset)','sample_events':len(qt),'lost':ql},'scope_boundary':'CI injects deterministic SDK doubles; real instruments are optional runtime dependencies and missed/lost events are fatal telemetry.'},
        'fpga':{'input_events':len(tags),'frames':len(actual),'cycles':cycle,'backpressure_cycles':red.backpressure,'accepted_events':red.accepted,'rtl':rtl,'summary_digest':sha256_json([[x.frame,x.counts,x.first,x.last,x.overflow] for x in actual])},
        'runtime_replay':{'chain':'timestamp -> frame -> W33 point40 -> Schlaefli line27 -> E6 root72 -> typed E8 root240','frames':len(routes),'sample':routes[:4],'route_digest':sha256_json(routes)},
        'theorem':'Vendor-normalized tags are reduced with bounded state and every completed frame is replayed through an explicit 40-27-72-240 typed route; loss, overflow, and backpressure are fail-closed.'}
def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
