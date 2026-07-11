#!/usr/bin/env python3
"""Vendor adapters, FPGA reduction, and explicit 40-27-72-240 replay."""
from functools import lru_cache
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(HERE))
OUT=ROOT/'data/PART_2026_07_11_LEVI_NEXT5_V5_hardware.json'
from w33_levi_next5_v5_common import sha256_json
from w33_levi_next5_v5_hardware_vendors import SwabianAdapter,QuTAGAdapter,Buf,SModule,QFake
from w33_levi_next5_v5_hardware_core import Reducer,Summary,software,stream,route,rtl_contract
import w33_levi_next5_v5_lanes as lanes

@lru_cache(maxsize=1)
def analyze():
    tags=stream();sample=tags[:128]
    sw=SwabianAdapter(SModule(sample),256);swt,sm,so=sw.read_clean();sw.close();qt,ql,qo=QuTAGAdapter(QFake(sample)).read_clean()
    expected=software(tags);red=Reducer();actual=[];i=cycle=0
    while i<len(tags) or red.pending is not None:
        ready=cycle%29 not in (0,1,2);valid=i<len(tags) and red.ready;x=tags[i] if valid else None;y=red.cycle(valid,x,ready)
        if valid:i+=1
        if y is not None:actual.append(y)
        cycle+=1
    tail=red.flush()
    if tail is not None:actual.append(tail)
    lane=lanes.analyze();routes=route(actual,lane)
    changed=Summary(actual[0].frame,actual[0].counts,actual[0].first+1,actual[0].last,actual[0].overflow)
    timestamp_sensitive=route([changed],lane)[0]!=routes[0]
    qloss=QuTAGAdapter(QFake(tags[:4],1));_,lost,qprobe=qloss.read()
    try:qloss.read_clean();qclosed=False
    except RuntimeError:qclosed=True
    probe=SwabianAdapter(SModule(tags[:4]),8)
    probe.stream=type('X',(),{'getData':lambda self:Buf(tags[:4],2),'stop':lambda self:None})();_,miss,sprobe=probe.read();probe.close()
    sclosed=False;probe=SwabianAdapter(SModule(tags[:4]),8)
    probe.stream=type('X',(),{'getData':lambda self:Buf(tags[:4],2),'stop':lambda self:None})()
    try:probe.read_clean()
    except RuntimeError:sclosed=True
    finally:probe.close()
    rtl=rtl_contract(ROOT);checks={
        'swabian_sdk_contract':[(x.t,x.ch,x.event_type) for x in swt]==[(x.t,x.ch,x.event_type) for x in sample] and sm==0 and not so,
        'qutag_sdk_contract':[(x.t,x.ch) for x in qt]==[(x.t,x.ch) for x in sample] and ql==0 and not qo,
        'vendor_loss_is_fail_closed':qprobe and sprobe and qclosed and sclosed and lost==1 and miss==2,
        'bounded_reference_reducer_matches_software':actual==expected,'backpressure_exercised':red.backpressure>0,
        'stream_over_one_million_events':len(tags)>1_000_000,
        'timestamp_changes_route':timestamp_sensitive,
        'all_w33_points_exercised':len({x['point40'] for x in routes})==40,
        'all_162_payload_addresses_exercised':len({(x['payload_lane'],x['schlafli_slot27']) for x in routes})==162,
        'typed_positive_control_routes':all(0<=x['payload_root240']<240 and x['control_pairing']==1 for x in routes),
        'rtl_frame_snapshot_contract_present':rtl['required_tokens']}
    return {'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
        'vendor_adapters':{'swabian':{'api':'createTimeTagger + TimeTagStreamBuffer arrays/members','physical_channels':[1,17],'normalized_channels':[0,16],'sample_events':len(swt),'missed':sm},'qutag':{'api':'getLastTimestamps(reset) + getDataLost','sample_events':len(qt),'lost':ql},'scope_boundary':'CI uses documentation-shaped SDK doubles. read_clean rejects missed/lost/full-buffer telemetry; no physical instrument is attached.'},
        'reference_reducer':{'execution':'Python cycle model, not RTL or FPGA execution','input_events':len(tags),'frames':len(actual),'cycles':cycle,'backpressure_cycles':red.backpressure,'accepted_events':red.accepted,'summary_digest':sha256_json([[x.frame,x.counts,x.first,x.last,x.overflow] for x in actual])},
        'rtl':{'execution':'Icarus compile/smoke in CI; two completed frames, including output backpressure','contract':rtl},
        'runtime_replay':{'chain':'frame summary -> timestamp-derived W33 point address || Schlaefli payload address -> positive E6 control -> typed E8 payload','mapping_scope':'The W33 40-action and Schlaefli 27-action are parallel typed projections. No W33-to-Schlaefli subgraph or incidence morphism is asserted.','frames':len(routes),'w33_points_covered':len({x['point40'] for x in routes}),'payload_addresses_covered':len({(x['payload_lane'],x['schlafli_slot27']) for x in routes}),'sample':routes[:4],'route_digest':sha256_json(routes)},
        'theorem':'Documentation-shaped vendor tags feed a bounded Python reference reducer; clean acquisitions produce timestamp-sensitive W33 addresses and separate Schlaefli/E6/E8 typed routes, while loss and overflow are rejected. The companion RTL is independently compile/smoke-tested with stable completed-frame snapshots.'}
def main():
    out=analyze();text=json.dumps(out,indent=2,sort_keys=True)+"\n"
    OUT.write_text(text,encoding='utf-8');print(text,end='')
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
