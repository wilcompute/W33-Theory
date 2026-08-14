#!/usr/bin/env python3
"""Pass5110: all-q chamber-generator kernel = binary Levi cut space.

Let Gamma be the Levi incidence graph of W(3,q).  Chamber generators are indexed
by E(Gamma), and an apartment contains an even number (0 or 2) of chambers at
every panel vertex.  Hence every vertex-star cut lies in the kernel of the map
from chamber coefficients to apartment words.  Since Gamma is connected, its
cut space has dimension |V|-1.  Pass5066 gives apartment-code rank q^4, while
|E|-(|V|-1)=q^4, so equality of dimensions proves the kernel theorem.

The executable part rebuilds q=2,3,4,5 and verifies every panel relation plus
the exact chamber-star ranks.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5110_CHAMBER_KERNEL_CUTSPACE.json'

def rank2(rows):
    piv={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)

def anchor(q):
    G=build_W(q);stars=chamber_stars(G);E=len(G['flags']);V=len(G['pts'])+len(G['lines'])
    byp=[[] for _ in G['pts']];byl=[[] for _ in G['lines']]
    for c,(p,l) in enumerate(G['flags']):byp[p].append(c);byl[l].append(c)
    panels=byp+byl
    assert len(panels)==V and {len(x) for x in panels}=={q+1}
    for P in panels:
        z=0
        for c in P:z^=stars[c]
        assert z==0
    r=rank2(stars)
    assert r==q**4 and E-(V-1)==q**4
    return {'q':q,'panels':V,'chambers':E,'apartments':len(G['apartments']),
            'chamber_star_rank':r,'kernel_dimension':E-r,'cut_space_dimension':V-1,
            'all_panel_relations_zero':True}

def main():
    out={'pass':5110,'status':'THEOREM_ALL_Q_CHAMBER_KERNEL_IS_CUT_SPACE',
         'statement':'ker(chamber coefficients -> apartment code)=Cut(Levi;F2)',
         'proof':'Panel stars map to zero. They span the connected Levi cut space of dimension |V|-1. Since apartment-code rank=q^4 and |E|-(|V|-1)=q^4, the inclusion is equality.',
         'dimension_identity':'(q+1)^2(q^2+1)-[2(q+1)(q^2+1)-1]=q^4',
         'consequence':'Every codeword has chamber-generator representatives forming one Levi cut coset; a minimum-cardinality representative is cut-minimal.',
         'anchors':{str(q):anchor(q) for q in (2,3,4,5)},
         'boundary':'Uses the all-q rank q^4 theorem from Pass5066. This is a binary generator-gauge theorem, not a new distance proof by itself.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
