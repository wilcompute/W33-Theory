"""Bounded 17-channel frame reducer and typed runtime route compiler."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
from w33_levi_next5_v5_common import build_w33, e8_roots, ip, sha256_json
from w33_levi_next5_v5_hardware_vendors import Tag,SYNC
MAX=(1<<24)-1

@dataclass(frozen=True)
class Summary:
    frame:int;counts:tuple[int,...];first:int;last:int;overflow:bool

class Reducer:
    def __init__(self):self.frame=0;self.counts=[0]*16;self.first=None;self.pending=None;self.overflow=False;self.accepted=0;self.backpressure=0
    @property
    def ready(self):return self.pending is None
    def cycle(self,valid,tag,out_ready):
        emitted=None
        if self.pending is not None:
            if out_ready:emitted,self.pending=self.pending,None
            else:self.backpressure+=1
        if valid:
            if tag is None:raise ValueError('missing tag')
            if not self.ready:self.backpressure+=1;return emitted
            tag.check();self.accepted+=1
            if tag.ch==SYNC:
                self.pending=Summary(self.frame,tuple(self.counts),self.first if self.first is not None else tag.t,tag.t,self.overflow)
                self.frame+=1;self.counts=[0]*16;self.first=None;self.overflow=False
            else:
                if self.first is None:self.first=tag.t
                if self.counts[tag.ch]==MAX:self.overflow=True
                else:self.counts[tag.ch]+=1
        return emitted
    def flush(self):out,self.pending=self.pending,None;return out

def software(tags):
    out=[];counts=[0]*16;first=None;frame=0;overflow=False
    for x in tags:
        x.check()
        if x.ch==SYNC:
            out.append(Summary(frame,tuple(counts),first if first is not None else x.t,x.t,overflow));frame+=1;counts=[0]*16;first=None;overflow=False
        else:
            if first is None:first=x.t
            if counts[x.ch]==MAX:overflow=True
            else:counts[x.ch]+=1
    return out

def stream(frames=256,per=4096):
    out=[];t=0
    for f in range(frames):
        for i in range(per):
            ch=(5*i+3*f+(i>>5))&15;t+=37+((i+7*f)%11);out.append(Tag(t,ch,f))
        t+=211;out.append(Tag(t,SYNC,f))
    return out

def route(frames,lane):
    bundles=lane['routing']['classical_line_bundles'];controls=lane['decomposition']['control_root_indices']
    payload={x for o in lane['decomposition']['payload_root_indices'] for x in o};out=[]
    w33=build_w33();roots=e8_roots()
    for s in frames:
        if s.overflow:raise RuntimeError(f'refusing overflowed frame {s.frame}')
        if len(s.counts)!=16 or s.first>s.last:raise ValueError('invalid frame summary')
        syn=sum((i+1)*c for i,c in enumerate(s.counts));duration=s.last-s.first
        point=(s.first+3*s.last+7*syn+11*s.frame)%40
        payload_address=(s.frame+2*duration+syn)%162
        ln,slot=divmod(payload_address,27);root=bundles[slot]['roots'][ln]
        positive=[c for c in controls if ip(roots[root],roots[c])==1]
        if len(positive)!=16:raise AssertionError('payload/control signature drift')
        ctl=positive[(s.first+s.last+syn+s.frame)%len(positive)]
        assert root in payload and ctl in controls and ip(roots[root],roots[ctl])==1
        out.append({'frame':s.frame,'first_timestamp_ps':s.first,'last_timestamp_ps':s.last,
            'point40':point,'point40_coordinate':w33.points[point],
            'schlafli_line27':bundles[slot]['label'],'schlafli_slot27':slot,
            'control_root72':ctl,'control_pairing':1,'payload_lane':ln,
            'payload_root240':root,'overflow':False,'count_digest':sha256_json(s.counts)})
    return out

def rtl_contract(root:Path):
    p=root/'hardware/holonet_v5_frame_reducer.sv';text=p.read_text();need=['module holonet_v5_frame_reducer','s_axis_tvalid','s_axis_tready','m_axis_tvalid','m_axis_tready','frame_counts','accum_overflow','frame_counter','count0','count15','overflow']
    return {'path':str(p.relative_to(root)),'required_tokens':all(x in text for x in need),'sha256':hashlib.sha256(text.encode()).hexdigest()}
