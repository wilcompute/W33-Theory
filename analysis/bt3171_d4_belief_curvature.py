#!/usr/bin/env python3
"""Pass 3171: non-Abelian belief curvature of the sparse D4 posterior.

The 3,381 pair-correction factors live on 69 shared measured triangles and 7x7 ordered
nonidentity D4 labels.  Their gauge-invariant obstruction is the commutator.  For D4 every
commutator lies in the centre {1,r^2}; therefore one bit is a complete curvature syndrome.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3171_D4_BELIEF_CURVATURE_results.json'
# element (a,b) means r^a s^b, r^4=s^2=1 and srs=r^-1.
ELS=[(a,b) for b in (0,1) for a in range(4)]; ID=(0,0); CENTRAL=(2,0)
NON=[e for e in ELS if e!=ID]
NAME={(0,0):'1',(1,0):'r',(2,0):'r2',(3,0):'r3',(0,1):'s',(1,1):'rs',(2,1):'r2s',(3,1):'r3s'}

def mul(x,y):
    a,b=x;c,d=y
    return ((a+((-1)**b)*c)%4,(b+d)%2)

def inv(x):
    return next(y for y in ELS if mul(x,y)==ID and mul(y,x)==ID)

def comm(x,y): return mul(mul(mul(x,y),inv(x)),inv(y))

def conj(g,x): return mul(mul(g,x),inv(g))

def cclass(x):
    return tuple(sorted({NAME[conj(g,x)] for g in ELS}))

def main():
    table=[]; hist=Counter(); by_class=defaultdict(lambda:Counter())
    for a,b in itertools.product(NON,repeat=2):
        k=comm(a,b); assert k in (ID,CENTRAL)
        bit=int(k==CENTRAL);hist[bit]+=1
        by_class[(cclass(a),cclass(b))][bit]+=1
        table.append({'left':NAME[a],'right':NAME[b],'commutator':NAME[k],'curvature_bit':bit})
    assert hist[0]==25 and hist[1]==24
    measured_pairs=69
    out={'schema':'w33.pass3171.d4_belief_curvature.v1','group_order':8,
      'nonidentity_labels':7,'shared_measured_edge_pairs':measured_pairs,
      'pair_correction_factors':measured_pairs*49,
      'commutator_image':['1','r2'],'curvature_syndrome_bits':1,
      'ordered_label_pair_census':{'flat':hist[0],'curved':hist[1]},
      'full_factor_census':{'flat':measured_pairs*hist[0],'curved':measured_pairs*hist[1]},
      'theorem':'the D4 derived subgroup is {1,r2}; conjugation fixes both elements, so the commutator bit is gauge invariant and complete',
      'conjugacy_block_census':[
        {'left_class':list(k[0]),'right_class':list(k[1]),'flat':v[0],'curved':v[1]}
        for k,v in sorted(by_class.items(),key=lambda kv:(kv[0][0],kv[0][1]))],
      'ordered_table':table,
      'boundary':'Exact group theory and exact factor counts. A nonzero curvature bit is an interaction diagnostic, not a measured optical field strength.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ('pair_correction_factors','ordered_label_pair_census','full_factor_census','theorem')},indent=2))
if __name__=='__main__':main()
