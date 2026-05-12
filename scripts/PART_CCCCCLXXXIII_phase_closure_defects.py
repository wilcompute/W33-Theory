#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from typing import Iterable

FANO = {
    1: (1,0,0), 2: (0,1,0), 3: (0,0,1), 4: (1,1,0),
    5: (1,0,1), 6: (0,1,1), 7: (1,1,1),
}

@dataclass(frozen=True)
class Atom:
    phase12: int
    color7: int
    face10: int
    bivector_id: int
    occupied: bool = True

@dataclass(frozen=True)
class ClosureLedger:
    d12: int
    d10: int
    d7: tuple[int,int,int]
    dcl: tuple[int,...]
    coherent: bool

def xor3(vals: Iterable[tuple[int,int,int]]) -> tuple[int,int,int]:
    a=b=c=0
    for x,y,z in vals:
        a ^= x; b ^= y; c ^= z
    return (a,b,c)

def closure_ledger(cycle: Iterable[Atom]) -> ClosureLedger:
    atoms=[a for a in cycle if a.occupied]
    d12=sum(a.phase12 for a in atoms)%12
    d10=sum(a.face10 for a in atoms)%10
    d7=xor3(FANO[a.color7] for a in atoms)
    odd=[]
    counts={}
    for a in atoms:
        counts[a.bivector_id]=counts.get(a.bivector_id,0)+1
    for k,v in sorted(counts.items()):
        if v%2: odd.append(k)
    dcl=tuple(odd)
    return ClosureLedger(d12=d12,d10=d10,d7=d7,dcl=dcl,coherent=(d12==0 and d10==0 and d7==(0,0,0) and len(dcl)==0))

def closure_score(cycles: Iterable[Iterable[Atom]]) -> float:
    ledgers=[closure_ledger(c) for c in cycles]
    if not ledgers: return 0.0
    return sum(1 for x in ledgers if x.coherent)/len(ledgers)

def main() -> None:
    coherent=[Atom(3,1,5,11),Atom(9,2,5,11),Atom(0,4,0,12),Atom(0,4,0,12)]
    defective=[Atom(3,1,5,11),Atom(4,2,5,12)]
    payload={
        'coherent': asdict(closure_ledger(coherent)),
        'defective': asdict(closure_ledger(defective)),
        'score': closure_score([coherent, defective]),
    }
    print(json.dumps(payload, indent=2))

if __name__=='__main__': main()
