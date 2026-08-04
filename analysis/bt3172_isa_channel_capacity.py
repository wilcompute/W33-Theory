#!/usr/bin/env python3
"""Pass 3172: treat an opcode decoder as an exact finite communication channel.

For a fixed frame x and a uniformly selected opcode G, the observed next frame Y=Gx
carries H(Y|x) bits about the opcode.  Averaging over all 81 frames gives an exact
information-per-dispatch metric that is independent of the older self-loop/duplicate-edge
collision cost.  It exposes whether a larger ISA buys real control bandwidth.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3172_ISA_CHANNEL_CAPACITY_results.json'
LIN={
'F_p':((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),
'F_f':((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0)),
'CX_pf':((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),
'CX_fp':((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1))}
I=np.eye(4,dtype=np.int8)
M={k:np.array(v,dtype=np.int8) for k,v in LIN.items()}; T={k:np.zeros(4,dtype=np.int8) for k in LIN}
for i in range(4):
    M[f'Z{i}']=I.copy(); v=np.zeros(4,dtype=np.int8);v[i]=1;T[f'Z{i}']=v
VECS=np.array(list(itertools.product(range(3),repeat=4)),dtype=np.int8)
SETS={
'current4':['F_p','CX_pf','CX_fp','Z1'],
'low_collision4':['CX_fp','CX_pf','F_f','Z0'],
'fast6':['F_f','CX_pf','CX_fp','Z0','Z1','Z3']}

def entropy_mults(mult,total):
    return -sum((m/total)*math.log2(m/total) for m in mult)

def metrics(names):
    hs=[]; patterns=Counter(); duplicate_loss=0
    for x in VECS:
        ys=[tuple(((M[n]@x+T[n])%3).tolist()) for n in names]
        c=Counter(ys); pat=tuple(sorted(c.values(),reverse=True));patterns[pat]+=1
        hs.append(entropy_mults(pat,len(names))); duplicate_loss+=len(names)-len(c)
    ideal=math.log2(len(names)); avg=sum(hs)/81
    return {'opcodes':names,'ideal_bits_per_dispatch':ideal,'average_bits_per_dispatch':avg,
            'normalized_capacity':avg/ideal,'minimum_bits_per_dispatch':min(hs),
            'maximum_bits_per_dispatch':max(hs),'duplicate_destination_events':duplicate_loss,
            'multiplicity_pattern_histogram':{'x'.join(map(str,k)):v for k,v in sorted(patterns.items())}}

def main():
    rows={k:metrics(v) for k,v in SETS.items()}
    rows['comparisons']={
      'low4_minus_current_bits':rows['low_collision4']['average_bits_per_dispatch']-rows['current4']['average_bits_per_dispatch'],
      'fast6_minus_current_bits':rows['fast6']['average_bits_per_dispatch']-rows['current4']['average_bits_per_dispatch'],
      'fast6_absolute_gain_fraction':rows['fast6']['average_bits_per_dispatch']/rows['current4']['average_bits_per_dispatch']-1,
      'interpretation':'collisions are a control-channel ambiguity, but absolute and normalized capacity are different objectives'}
    out={'schema':'w33.pass3172.isa_channel_capacity.v1','frames':81,'results':rows,
      'boundary':'Exact for uniform opcodes and uniform frame averaging. Program distributions, physical decoder energy and error rates are not inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
