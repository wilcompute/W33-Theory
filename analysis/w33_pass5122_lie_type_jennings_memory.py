#!/usr/bin/env python3
"""Pass5122: Steinberg/Jennings root-height memory for rank-two Lie types.

In defining characteristic the Steinberg module is projective of dimension |U|;
restriction to a Sylow p-subgroup U is therefore one free regular k[U] module.
In the safe prime-field range where the Jennings dimension series agrees with
the positive-root height filtration, the augmentation Hilbert series is the
product of one truncated p-string at each positive-root height.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5122_LIE_TYPE_JENNINGS_MEMORY.json'

def coefficients(p,heights):
    a=[1]
    for h in heights:
        f=[0]*(h*(p-1)+1)
        for k in range(p):f[k*h]=1
        b=[0]*(len(a)+len(f)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(f):b[i+j]+=x*y
        a=b
    return a

def row(name,p,heights):
    c=coefficients(p,heights)
    return {'type':name,'p':p,'positive_root_heights':heights,'positive_roots':len(heights),
            'group_algebra_dimension':p**len(heights),'augmentation_layers':c,
            'nilpotence_index':len(c),'coefficient_sum':sum(c),
            'hilbert_factors':['1+t^%d+...+t^%d'%(h,(p-1)*h) for h in heights]}

def main():
    A2=row('A2',3,[1,1,2]);C2=row('C2',5,[1,1,2,3]);G2=row('G2',7,[1,1,2,3,4,5])
    assert A2['augmentation_layers']==[1,2,4,4,5,4,4,2,1]
    assert C2['coefficient_sum']==625 and G2['coefficient_sum']==117649
    q3=[1,2,4,5,7,8,9,9,9,8,7,5,4,2,1]
    out={'pass':5122,'status':'THEOREM_SAFE_CHARACTERISTIC_RANK2_STEINBERG_JENNINGS_MEMORY',
         'module_theorem':'For a split finite group of Lie type in defining characteristic, the Steinberg module restricts to one regular module on a Sylow/maximal unipotent p-subgroup U (projective restriction plus dim(St)=|U|).',
         'jennings_formula':'In the stated safe prime-field range, Hilb gr_J(F_p[U]) = product_{positive roots alpha} (1+t^ht(alpha)+...+t^((p-1)ht(alpha))).',
         'safe_examples':{'A2_p3':A2,'C2_p5':C2,'G2_p7':G2},
         'q3_C2_exceptional_anchor':{'p':3,'heights':[1,1,2,3],'layers':q3,'status':'exactly computed in Pass5108; same root-height factorization holds at this boundary prime'},
         'primary_references':['S. A. Jennings, Trans. AMS 50 (1941), 175-185, The Structure of the Group Ring of a p-Group Over a Modular Field','Steinberg defining-characteristic projectivity/regular Sylow restriction; modern Sylow-regular terminology: Malle-Zalesski, Steinberg-like characters for finite simple groups'],
         'boundary':'The root-height product is promoted here in the safe prime-field range (A2 p>2, C2 p>3, G2 p>5) plus the separately computed C2,p=3 anchor. No blanket bad-prime formula or hardware latency interpretation is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
