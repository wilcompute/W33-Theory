#!/usr/bin/env python3
from __future__ import annotations
import json
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT2917_RANK7_FRAME_ENGINE_results.json'

def enc(s):
    a,b,c,d=s; return 27*a+9*b+3*c+d

def dec(r):
    return (r//27,(r%27)//9,(r%9)//3,r%3)

def add(a,b): return (a+b)%3
def step(s,op):
    xp,zp,xf,zf=s
    if op==0: return ((-zp)%3,xp,xf,zf)
    if op==1: return (xp,(zp-zf)%3,(xf+xp)%3,zf)
    if op==2: return ((xp+xf)%3,zp,xf,(zf-zp)%3)
    return (xp,(zp+1)%3,xf,zf)

def main():
    states=list(product(range(3),repeat=4))
    transitions={}
    for state in states:
        assert dec(enc(state))==state
        for op in range(4):
            target=step(state,op)
            assert dec(enc(target))==target
            transitions[f'{enc(state)}:{op}']=enc(target)
    per_op=[len({transitions[f'{r}:{op}'] for r in range(81)}) for op in range(4)]
    checks={
      '81_unique_codes':len({enc(s) for s in states})==81,
      'code_range_0_80':{enc(s) for s in states}==set(range(81)),
      'decode_inverse':all(dec(enc(s))==s for s in states),
      '324_transitions':len(transitions)==324,
      'four_bijections':per_op==[81,81,81,81],
      'seven_bit_lower_bound':2**6<81<=2**7,
    }
    assert all(checks.values())
    out={'schema':'w33.pass2917.rank7_frame_engine.v1','status':'EXACT_LOGIC_REMOTE_SYNTHESIS_PENDING',
         'check_count':len(checks),'checks':checks,'state_bits':7,'unused_codes':47,
         'transition_entries':324,'transition_payload_bits':2268,'per_operation_image_sizes':per_op,
         'rtl':'rtl/w33_pass2917_rank7_frame_engine.sv',
         'boundary':'Truth-table equivalence is exact; cell count and timing require observed synthesis and place-and-route.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(f"PASS {len(checks)}/{len(checks)}")
if __name__=='__main__':main()
