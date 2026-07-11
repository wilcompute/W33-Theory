"""Bounded 17-channel frame reducer and typed runtime route compiler."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
from w33_levi_next5_v5_common import sha256_json
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
    for s in frames:
        syn=sum((i+1)*c for i,c in enumerate(s.counts));slot=syn%27;ln=s.frame%6;root=bundles[slot]['roots'][ln];ctl=controls[(syn+17*s.frame)%72]
        assert root in payload and ctl in controls
        out.append({'frame':s.frame,'point40':(s.frame+syn)%40,'line27':bundles[slot]['label'],'line27_slot':slot,'control_root72':ctl,'payload_lane':ln,'payload_root240':root,'overflow':s.overflow,'count_digest':sha256_json(s.counts)})
    return out

def rtl_contract(root:Path):
    p=root/'hardware/holonet_v5_frame_reducer.sv';text=p.read_text();need=['module holonet_v5_frame_reducer','s_axis_tvalid','s_axis_tready','m_axis_tvalid','m_axis_tready','count0','count15','overflow']
    return {'path':str(p.relative_to(root)),'required_tokens':all(x in text for x in need),'sha256':hashlib.sha256(text.encode()).hexdigest()}
