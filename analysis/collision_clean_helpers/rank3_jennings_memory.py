#!/usr/bin/env python3
"""Pass5137: rank-three protected-memory/Jennings root-height extension."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5137_RANK3_JENNINGS_MEMORY.json'
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
    c=profile(heights,p);return {'type':name,'p':p,'positive_root_heights':heights,'positive_roots':len(heights),'regular_module_dimension':p**len(heights),'nilpotence_top_degree':len(c)-1,'layers':c,'layer_count':len(c),'central_layer_index':(len(c)-1)//2,'central_layer_dimension':c[(len(c)-1)//2],'palindromic':True}
def main():
    a=row('A3',[1,1,1,2,2,3],5);c=row('C3',[1,1,1,2,2,3,3,4,5],7)
    assert a['regular_module_dimension']==15625 and a['central_layer_dimension']==931 and a['layer_count']==41
    assert c['regular_module_dimension']==40353607 and c['central_layer_dimension']==925601 and c['layer_count']==133
    out={'pass':5137,'status':'THEOREM_SAFE_CHARACTERISTIC_RANK3_JENNINGS_MEMORY','general_rule':'If Jennings dimension-series weights of the maximal unipotent p-group are the positive-root heights, gr_J F_p[U] has Hilbert series product over positive roots of (1+t^ht+...+t^((p-1)ht)). The defining-characteristic Steinberg restriction is one regular U-module, so this is its protected-memory radical profile.','examples':{'A3_p5':a,'C3_p7':c},'boundary':'Safe-characteristic algebraic filtration only; augmentation depth is not physical time/latency and bad-prime cases require separate verification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
