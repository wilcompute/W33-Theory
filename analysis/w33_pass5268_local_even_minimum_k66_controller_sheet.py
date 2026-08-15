#!/usr/bin/env python3
"""Pass5268 (outside-box): every q5 local even minimum is an adjacent-edge pair in K6,6.

The q=5 P-component code is

  C = Cut(K6) tensor Cut(K6) = [225,25,25]_2.

Write s_i, i=1..6, for the six minimum star cuts of Cut(K6), each of
weight five.  The 36 minimum tensor atoms are a_ij=s_i tensor s_j and
are naturally the 36 edges of K6,6.

Pass5259 proves that the even subcode has minimum 40 and exactly 180 minimum
words.  Here the complete geometry is explicit.  The weight-eight words of
Cut(K6) are precisely s_j+s_k for unordered pairs j!=k.  Hence every simple
tensor of factor weights 5x8 is

  s_i tensor (s_j+s_k) = a_ij + a_ik,

and every 8x5 word is the transposed version.  These are exactly unordered
pairs of K6,6 edges sharing one endpoint.  There are

  12 * C(6,2) = 180,

so this accounts for the entire minimum shell with no leftovers.

Global bridge.  Two chamber stars based at the same W point have the same
25-component P footprint.  In each active P component their local atoms share
the endpoint representing that W point, so their difference is one of the
weight-40 adjacent-edge words above.  Their symmetric difference therefore has
25 active P blocks, each of weight40, total apartment weight1000; this is the
sharp d_block(K0)=25 witness of Pass5262.

Pass5217 labels the 25 P atoms in a chosen q5 chamber star by the root-controller
projection (a,b,c,d)->(a,c) in F5^2.  Thus the sharp K0 witness is a full
5x5 controller sheet: one adjacent-atom transition over every (a,c) site.
This is an exact code/controller coordinate statement, not a claim of physical
time evolution.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5268_LOCAL_EVEN_MINIMUM_K66_CONTROLLER_SHEET.json'

def cuts_K6():
    # Canonical cuts delta(S)=delta(S^c), represented by bitsets on the 15 edges.
    E=list(itertools.combinations(range(6),2));out={}
    for m in range(1,1<<6):
        if m==(1<<6)-1:continue
        z=0
        for e,(i,j) in enumerate(E):
            if ((m>>i)&1)^((m>>j)&1):z|=1<<e
        out[z]=m
    return sorted(out)

def main():
    C=cuts_K6();hist={w:sum(x.bit_count()==w for x in C) for w in sorted({x.bit_count() for x in C})}
    assert hist=={0:1,5:6,8:15,9:10}
    stars=[x for x in C if x.bit_count()==5];w8=[x for x in C if x.bit_count()==8]
    assert len(stars)==6 and len(w8)==15
    assert {a^b for a,b in itertools.combinations(stars,2)}==set(w8)
    # Formal tensor shell counts; supports lie in 15x15 coordinates.
    def tensor(a,b):
        z=0
        for i in range(15):
            if (a>>i)&1:
                for j in range(15):
                    if (b>>j)&1:z|=1<<(15*i+j)
        return z
    atoms={(i,j):tensor(stars[i],stars[j]) for i in range(6) for j in range(6)}
    mins=set()
    for i in range(6):
        for j,k in itertools.combinations(range(6),2):mins.add(atoms[i,j]^atoms[i,k])
    for j in range(6):
        for i,k in itertools.combinations(range(6),2):mins.add(atoms[i,j]^atoms[k,j])
    assert len(mins)==180 and {x.bit_count() for x in mins}=={40}
    out={'pass':5268,'status':'THEOREM_Q5_LOCAL_EVEN_MINIMUM_IS_K66_ADJACENT_EDGE_PAIR',
      'factor_code_weight_histogram':hist,
      'minimum_atoms':36,
      'atom_geometry':'edges of K6,6, indexed a_ij=s_i tensor s_j',
      'even_minimum_weight':40,'even_minimum_words':180,
      'classification':'Every weight40 word is a_ij+a_ik or a_ij+a_kj; equivalently an unordered pair of K6,6 edges sharing one endpoint.',
      'count':'12*C(6,2)=180',
      'global_K0_witness':'Difference of two chamber stars based at the same W point: 25 active P blocks, one local adjacent-atom word of weight40 in each, total weight1000.',
      'controller_sheet':'Under Pass5217, the 25 active blocks of a chosen star are indexed by (a,c) in F5^2. The K0 block-minimum witness is therefore a full 5x5 sheet of adjacent-atom transitions.',
      'boundary':'Exact code/controller coordinate theorem. No optical dynamics or physical transition mechanism is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
