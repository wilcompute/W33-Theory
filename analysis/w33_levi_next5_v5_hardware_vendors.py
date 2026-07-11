"""Vendor-normalized time-tag adapters with fail-closed loss telemetry.

The SDK-facing doubles in this module intentionally mirror the documented
vendor return shapes.  The normalized runtime uses channels 0..16, while the
Swabian API uses positive physical channels starting at one.
"""
from dataclasses import dataclass
from typing import Iterable
import json
SYNC=16

@dataclass(frozen=True)
class Tag:
    t:int; ch:int; frame:int|None=None; event_type:int=0
    def check(self):
        if self.t<0 or not 0<=self.ch<=SYNC: raise ValueError((self.t,self.ch))

class SwabianAdapter:
    def __init__(self,module,limit=1_000_000,physical_channels=None):
        self.module=module;self.limit=limit
        self.physical_channels=tuple(range(1,18) if physical_channels is None else physical_channels)
        if len(self.physical_channels)!=17 or len(set(self.physical_channels))!=17 or any(c<=0 for c in self.physical_channels):
            raise ValueError('Swabian physical channel map must contain 17 distinct positive channels')
        self.normalized={physical:i for i,physical in enumerate(self.physical_channels)}
        self.tagger=module.createTimeTagger()
        self.stream=module.TimeTagStream(self.tagger,n_max_events=limit,channels=list(self.physical_channels))
    def read(self):
        b=self.stream.getData();ts=list(map(int,b.getTimestamps()));ch=list(map(int,b.getChannels()))
        et=list(map(int,b.getEventTypes())) if hasattr(b,'getEventTypes') else [0]*len(ts)
        if not len(ts)==len(ch)==len(et):raise ValueError('inconsistent vendor arrays')
        missed_values=list(map(int,b.getMissedEvents())) if hasattr(b,'getMissedEvents') else [0]*len(ts)
        if len(missed_values)!=len(ts):raise ValueError('inconsistent missed-event array')
        missed=sum(max(0,x) for x in missed_values)
        overflow_member=getattr(b,'hasOverflows',False)
        vendor_overflow=bool(overflow_member() if callable(overflow_member) else overflow_member)
        event_fault=any(e!=0 for e in et)
        over=vendor_overflow or len(ts)>=self.limit or missed>0 or event_fault
        out=[]
        for t,c,e in zip(ts,ch,et):
            if e!=0:continue
            if c not in self.normalized:raise ValueError(f'unmapped Swabian channel {c}')
            out.append(Tag(t,self.normalized[c],event_type=e))
        for x in out:x.check()
        return out,missed,over
    def read_clean(self):
        out,missed,fault=self.read()
        if fault:raise RuntimeError(f'Swabian acquisition fault (missed={missed})')
        return out,missed,fault
    def close(self):
        if hasattr(self.stream,'stop'):self.stream.stop()
        if hasattr(self.module,'freeTimeTagger'):self.module.freeTimeTagger(self.tagger)

class QuTAGAdapter:
    def __init__(self,sdk):self.sdk=sdk.QuTAG() if hasattr(sdk,'QuTAG') else sdk
    def read(self):
        try:raw=self.sdk.getLastTimestamps(True)
        except TypeError:raw=self.sdk.getLastTimestamps(reset=True)
        if not isinstance(raw,tuple) or len(raw) not in (2,3):raise ValueError('bad quTAG tuple')
        ts,ch=map(list,raw[:2]);valid=int(raw[2]) if len(raw)==3 else len(ts)
        if valid<0 or valid>len(ts) or valid>len(ch):raise ValueError('invalid quTAG valid count')
        buffer_full=valid>0 and valid==len(ts)==len(ch)
        ts,ch=ts[:valid],ch[:valid]
        out=[Tag(int(t),int(c)) for t,c in zip(ts,ch)]
        for x in out:x.check()
        if hasattr(self.sdk,'getDataLost'):lost=int(bool(self.sdk.getDataLost()))
        elif hasattr(self.sdk,'getLostEvents'):lost=int(bool(self.sdk.getLostEvents()))
        else:lost=0
        return out,lost,bool(lost or buffer_full)
    def read_clean(self):
        out,lost,fault=self.read()
        if fault:raise RuntimeError(f'quTAG acquisition fault (lost={lost})')
        return out,lost,fault

class NDJSON:
    def __init__(self,lines:Iterable[str]):self.lines=lines
    def __iter__(self):
        for line in self.lines:
            if not line.strip():continue
            r=json.loads(line);x=Tag(int(r['timestamp_ps']),int(r['channel']),r.get('frame'),int(r.get('event_type',0)));x.check();yield x

class Buf:
    def __init__(self,tags,missed=0):self.tags=tags;self.missed=missed
    def getTimestamps(self):return [x.t for x in self.tags]
    def getChannels(self):return [x.ch+1 for x in self.tags]
    def getEventTypes(self):return [x.event_type for x in self.tags]
    def getMissedEvents(self):return [self.missed if i==0 else 0 for i in range(len(self.tags))]
    @property
    def hasOverflows(self):return self.missed>0
class SStream:
    def __init__(self,tags):self.tags=tags
    def getData(self):return Buf(self.tags)
    def stop(self):pass
class SModule:
    def __init__(self,tags):self.tags=tags
    def createTimeTagger(self):return object()
    def TimeTagStream(self,_tagger,n_max_events,channels):
        assert n_max_events>len(self.tags) and set(channels)==set(range(1,18));return SStream(self.tags)
    def freeTimeTagger(self,_):pass
class QFake:
    def __init__(self,tags,lost=0):self.tags=tags;self.lost=lost
    def getLastTimestamps(self,reset=True):
        assert reset
        return [x.t for x in self.tags]+[0],[x.ch for x in self.tags]+[0],len(self.tags)
    def getDataLost(self):return bool(self.lost)
