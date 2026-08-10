#!/usr/bin/env python3
"""Pass 4757 — exact low-error sectors and noise response of the residue Hamiltonian.

For H=-sum_R S_R, S_R=prod_{i in R} Z_i over the 270 four-line residues,
the syndrome of a line-error set is the XOR of the 40 column syndromes.
We enumerate every error set through weight six. H10 has distance 12, so
weights <=5 are unique coset leaders; at weight six the only collisions are
complementary 6+6 halves of the forty weight-12 H10 words. This gives an exact
coset-leader/microcanonical census through radius six.

We also derive the exact independent-bit-flip mean and variance from the
residue overlap census 23895/10800/1620 for intersection sizes 0/1/2.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4757_HAMILTONIAN_LOW_ENERGY_NOISE.json'

def mask(S):return sum(1<<i for i in S)
def basis(vals):
    piv={};out=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(y);break
    return out
def span(B):
    S={0}
    for b in B:S|={x^b for x in list(S)}
    return S

def main():
    _,_,lines,A,_,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270
    rm=[mask(r) for r in residues]
    overlap=Counter((rm[i]&rm[j]).bit_count() for i,j in itertools.combinations(range(270),2))
    assert overlap==Counter({0:23895,1:10800,2:1620})

    syn=[]
    for i in range(40):
        s=0
        for j,r in enumerate(residues):
            if i in r:s|=1<<j
        syn.append(s)
    assert Counter(x.bit_count() for x in syn)==Counter({27:40})

    raw={}
    for w in range(7):
        C=Counter()
        for E in itertools.combinations(range(40),w):
            s=0
            for i in E:s^=syn[i]
            C[s.bit_count()]+=1
        raw[w]=C

    # Enumerate H10 exactly and resolve the weight-6 doubletons.
    rows=[mask(np.flatnonzero(A[i])) for i in range(40)]
    H=span(basis(rows));assert len(H)==1024
    W=Counter(x.bit_count() for x in H);assert W[12]==40 and min(k for k in W if k)>0
    w12=[x for x in H if x.bit_count()==12];assert len(w12)==40
    dup=Counter();seen=set()
    for h in w12:
        S=[i for i in range(40) if (h>>i)&1];SS=set(S)
        for C in itertools.combinations(S,6):
            a=tuple(C);b=tuple(sorted(SS-set(C)));pair=tuple(sorted((a,b)))
            key=(h,pair)
            if key in seen:continue
            seen.add(key);s=0
            for i in C:s^=syn[i]
            dup[s.bit_count()]+=1
    assert sum(dup.values())==18480
    assert dup==Counter({84:9720,90:4320,96:4320,108:120})
    distinct={w:Counter(c) for w,c in raw.items()};distinct[6]=raw[6]-dup
    assert sum(distinct[6].values())==3819900

    aggregate=Counter()
    for C in distinct.values():aggregate.update(C)
    # Exact within coset-leader radius <=6; do not call this the complete
    # Hamiltonian spectrum because the covering radius has not been proved <=6.
    assert aggregate[0]==1 and aggregate[27]==40 and aggregate[48]==540 and aggregate[54]==240

    # Effective two-defect interaction: Delta E = 2*syndrome weight.
    pair={'skew_W33_lines':{'count':540,'violated_checks':48,'energy_cost':96,'binding_vs_two_singles':-12},
          'meeting_W33_lines':{'count':240,'violated_checks':54,'energy_cost':108,'binding_vs_two_singles':0}}

    out={'pass':4757,'hamiltonian':{'terms':270,'ground_syndrome_weight':0,'ground_configuration_degeneracy':1024,'single_defect_cost':54},
      'coset_leader_microcanonical_through_weight6':{str(w):{str(k):v for k,v in sorted(C.items())} for w,C in distinct.items()},
      'weight6_collision_pairs_by_syndrome_weight':{str(k):v for k,v in sorted(dup.items())},
      'distinct_syndromes_with_leader_weight_at_most6':sum(aggregate.values()),
      'aggregate_syndrome_weight_census_radius6':{str(k):v for k,v in sorted(aggregate.items())},
      'two_defect_sector':pair,
      'independent_bit_flip_response':{
        'let_a':'a=1-2p',
        'mean_H':'-270 a^4',
        'variance_H':'270(1-a^8) + 21600(a^6-a^8) + 3240(a^4-a^8)',
        'derivation':'two checks with support intersection s have <S_R S_T>=a^(8-2s); unordered pair census is s=0:23895, s=1:10800, s=2:1620'},
      'boundary':'The radius-6 table is an exact coset-leader sector, not a proof of the complete 2^30 syndrome weight enumerator. The p-response is for an independent classical bit-flip ensemble, not a thermal-equilibrium claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
