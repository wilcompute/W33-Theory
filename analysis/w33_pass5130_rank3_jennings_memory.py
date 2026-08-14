#!/usr/bin/env python3
"""Pass5130: rank-three protected-memory/Jennings root-height extension.

Pass5122 identified the regular Sylow-unipotent restriction of the defining-
characteristic Steinberg carrier with a Jennings augmentation filtration. In
the safe range where the dimension-series weights equal positive-root
heights, the associated-graded Hilbert series is
  product_{alpha>0} (1+t^ht(alpha)+...+t^((p-1)ht(alpha))).
This pass moves beyond rank two with exact A3,p=5 and C3,p=7 profiles.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5130_RANK3_JENNINGS_MEMORY.json'

def profile(heights,p):
    c=[1]
    for h in heights:
        f=[0]*((p-1)*h+1)
        for a in range(p):f[a*h]=1
        z=[0]*(len(c)+len(f)-1)
        for i,x in enumerate(c):
            if x:
                for j,y in enumerate(f):
                    if y:z[i+j]+=x*y
        c=z
    assert c==c[::-1] and sum(c)==p**len(heights)
    return c

def row(name,heights,p):
    c=profile(heights,p);return {'type':name,'p':p,'positive_root_heights':heights,
      'positive_roots':len(heights),'regular_module_dimension':p**len(heights),
      'nilpotence_top_degree':len(c)-1,'layers':c,'layer_count':len(c),
      'central_layer_index':(len(c)-1)//2,'central_layer_dimension':c[(len(c)-1)//2],
      'palindromic':True,'hilbert_factorization':' * '.join(f'(1+t^{h}+...+t^{(p-1)*h})' for h in heights)}

def main():
    A3=[1,1,1,2,2,3]
    C3=[1,1,1,2,2,3,3,4,5]
    a=row('A3',A3,5);c=row('C3',C3,7)
    assert a['regular_module_dimension']==15625 and a['central_layer_dimension']==931 and a['layer_count']==41
    assert c['regular_module_dimension']==40353607 and c['central_layer_dimension']==925601 and c['layer_count']==133
    out={'pass':5130,'status':'THEOREM_SAFE_CHARACTERISTIC_RANK3_JENNINGS_MEMORY',
      'general_rule':'If the Jennings dimension-series weights of the maximal unipotent p-group are the positive-root heights, gr_J F_p[U] has Hilbert series product over positive roots of (1+t^ht+...+t^((p-1)ht)). The defining-characteristic Steinberg restriction is one regular U-module, so this is its protected-memory radical profile.',
      'examples':{'A3_p5':a,'C3_p7':c},
      'synthesis':'The rank-two C2 memory exponents 1,1,2,3 were not isolated: rank-three A3 and C3 produce the corresponding full positive-root-height multisets as exact memory-depth weights.',
      'boundary':'The algebraic regular-module/Jennings statement is exact in the stated safe range. No physical time, latency, or energy scale is assigned to augmentation depth; bad-prime cases require separate dimension-series verification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
