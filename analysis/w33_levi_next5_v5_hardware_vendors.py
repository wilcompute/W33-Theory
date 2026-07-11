"""Vendor-normalized time-tag adapters with fail-closed loss telemetry."""
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
    def __init__(self,module,limit=1_000_000):
        self.module=module;self.limit=limit;self.tagger=module.createTimeTagger()
        self.stream=module.TimeTagStream(self.tagger,n_max_events=limit,channels=list(range(17)))
    def read(self):
        b=self.stream.getData();ts=list(map(int,b.getTimestamps()));ch=list(map(int,b.getChannels()))
        et=list(map(int,b.getEventTypes())) if hasattr(b,'getEventTypes') else [0]*len(ts)
        if not len(ts)==len(ch)==len(et):raise ValueError('inconsistent vendor arrays')
        missed=int(b.getMissedEvents()) if hasattr(b,'getMissedEvents') else 0
        over=bool(b.hasOverflows()) if hasattr(b,'hasOverflows') else len(ts)>=self.limit or missed>0
        out=[Tag(t,c,event_type=e) for t,c,e in zip(ts,ch,et)]
        for x in out:x.check()
        return out,missed,over
    def close(self):
        if hasattr(self.stream,'stop'):self.stream.stop()
        if hasattr(self.module,'freeTimeTagger'):self.module.freeTimeTagger(self.tagger)

class QuTAGAdapter:
    def __init__(self,sdk):self.sdk=sdk.QuTAG() if hasattr(sdk,'QuTAG') else sdk
    def read(self):
        try:raw=self.sdk.getLastTimestamps(True)
        except TypeError:raw=self.sdk.getLastTimestamps(reset=True)
        if not isinstance(raw,tuple) or len(raw) not in (2,3):raise ValueError('bad quTAG tuple')
        ts,ch=map(list,raw[:2]);valid=int(raw[2]) if len(raw)==3 else len(ts);ts,ch=ts[:valid],ch[:valid]
        out=[Tag(int(t),int(c)) for t,c in zip(ts,ch)]
        for x in out:x.check()
        lost=int(self.sdk.getLostEvents()) if hasattr(self.sdk,'getLostEvents') else 0
        return out,lost,lost>0

class NDJSON:
    def __init__(self,lines:Iterable[str]):self.lines=lines
    def __iter__(self):
        for line in self.lines:
            if not line.strip():continue
            r=json.loads(line);x=Tag(int(r['timestamp_ps']),int(r['channel']),r.get('frame'),int(r.get('event_type',0)));x.check();yield x

class Buf:
    def __init__(self,tags,missed=0):self.tags=tags;self.missed=missed
    def getTimestamps(self):return [x.t for x in self.tags]
    def getChannels(self):return [x.ch for x in self.tags]
    def getEventTypes(self):return [x.event_type for x in self.tags]
    def getMissedEvents(self):return self.missed
    def hasOverflows(self):return self.missed>0
class SStream:
    def __init__(self,tags):self.tags=tags
    def getData(self):return Buf(self.tags)
    def stop(self):pass
class SModule:
    def __init__(self,tags):self.tags=tags
    def createTimeTagger(self):return object()
    def TimeTagStream(self,_tagger,n_max_events,channels):
        assert n_max_events>=len(self.tags) and set(channels)==set(range(17));return SStream(self.tags)
    def freeTimeTagger(self,_):pass
class QFake:
    def __init__(self,tags,lost=0):self.tags=tags;self.lost=lost
    def getLastTimestamps(self,reset=True):assert reset;return [x.t for x in self.tags],[x.ch for x in self.tags],len(self.tags)
    def getLostEvents(self):return self.lost
