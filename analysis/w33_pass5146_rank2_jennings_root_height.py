#!/usr/bin/env python3
"""Pass5146: rank-two root-height/Jennings Hilbert series in the safe p>h range.

For a split maximal unipotent group U(F_p) with p greater than the Coxeter
number h, the nilpotency class is <p, root groups have exponent p, and the
Jennings/dimension filtration agrees with the root-height lower central
filtration.  Jennings monomials therefore give one factor
(1+t^r+...+t^{(p-1)r}) for every positive root of height r.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5146_RANK2_JENNINGS_ROOT_HEIGHT.json'

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c

def profile(p,heights):
    c=[1]
    for r in heights:
        f=[0]*(r*(p-1)+1)
        for a in range(p):f[a*r]=1
        c=mul(c,f)
    return c

def row(name,p,h,heights):
    c=profile(p,heights);N=len(heights);H=sum(heights)
    assert p>h and sum(c)==p**N and c==c[::-1] and len(c)-1==(p-1)*H
    return {'type':name,'p':p,'coxeter_h':h,'positive_root_heights':heights,
            'N_positive_roots':N,'height_sum':H,'group_order':p**N,
            'top_Jennings_degree':(p-1)*H,'loewy_length':(p-1)*H+1,
            'layers':c,'peak':max(c)}

def main():
    rows=[row('A2',5,3,[1,1,2]),row('C2',5,4,[1,1,2,3]),row('G2',7,6,[1,1,2,3,4,5])]
    c2q3=profile(3,[1,1,2,3]);assert c2q3==[1,2,4,5,7,8,9,9,9,8,7,5,4,2,1]
    out={'pass':5146,'status':'THEOREM_RANK2_ROOT_HEIGHT_JENNINGS_SAFE_RANGE',
         'formula':'H_U(t)=product_{alpha>0} sum_{a=0}^{p-1} t^{a ht(alpha)} for p>h.',
         'rows':rows,
         'small_characteristic_repo_anchor':{'type':'C2','p':3,'layers':c2q3,
             'note':'This q=3 profile was independently established in Pass5108; it lies outside the p>h proof range and is recorded only as an exact anchor.'},
         'memory_statement':'In the safe range, the augmentation/Jennings memory layers are determined entirely by the multiset of positive-root heights.',
         'boundary':'The symbolic theorem is asserted only for p>h here. Bad/small characteristic can deform the dimension series and must be checked separately.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
