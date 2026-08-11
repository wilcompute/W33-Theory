#!/usr/bin/env python3
"""Passes 4833/4838 — prove C_Levi <= C_378 <= C_399 objectwise.

The 405 local logical generators are reconstructed from the literal K6 cells.
A binary Levi cycle toggles the three sheet logicals over every selected
(point-packet, quotient-line) incidence. Even degree at packet vertices kills
all hot triples; even degree at quotient-line vertices kills the 27 outer line
parities. Thus the physical Levi cycle code lies in the zero-outer-syndrome
[2025,378,14]_2 kernel, hence in [2025,399,14]_2.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4756_4758_4760_dependency_cube_reconstruction import build_all
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4833_4838_LEVI_SUBCODE_CODE399.json'

def rank_masks(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)

def main():
    D=build_all();B=build_bundle();packets=B['packets'];K5=B['K5'];rm=D['rmasks'];U=D['cube_unions'];cubeR=D['cube_residues'];N=np.asarray(D['selected_incidence']);phiU=D['phiU'];phiR=D['phiR']
    hot={tuple(sorted(e)) for e in B['hot']};cold={tuple(sorted(e)) for e in B['cold']};router=hot|cold
    owner=[]
    for T in B['projected']:
        h=[i for i,S in enumerate(K5) if set(T)<=S];assert len(h)==1;owner.append(h[0])
    packet_of={s:p for p,T in enumerate(packets) for s in T}
    union_to_R={}
    for R in cubeR:
        u=0
        for r in R:u|=rm[r]
        union_to_R[u]=tuple(R)
    cells={}
    for ui,u in enumerate(U):
        s=phiU[ui];R=union_to_R[u];inc=set(np.flatnonzero(N[s]).tolist());assert {phiR[r] for r in R}==inc
        p=packet_of[s];F=sorted(i for i,S in enumerate(K5) if p in S);groups={f:sorted(v for v in inc if owner[v]==f) for f in F}
        H={tuple(sorted(groups[f])) for f in F};blocks={}
        for a,b in itertools.combinations(F,2):blocks[(a,b)]=sorted(tuple(sorted((x,y))) for x in groups[a] for y in groups[b])
        cells[s]={'packet':p,'fibers':F,'hot':sorted(H),'blocks':blocks}
    pedges=sorted(router);pei={e:i for i,e in enumerate(pedges)};bit=lambda e:1<<pei[e]
    logical={};logical_index={};j=0
    for s,C in sorted(cells.items()):
        h0,h1,h2=C['hot'];F=C['fibers']
        for L in F:
            gm=bit(h0)^bit(h1)^bit(h2);pair=tuple(sorted(set(F)-{L}))
            for e in C['blocks'][pair]:gm^=bit(e)
            assert gm.bit_count()==7;logical[(s,L)]=gm;logical_index[(s,L)]=j;j+=1
    assert j==405 and rank_masks(logical.values())==405
    coldmask=sum(1<<pei[e] for e in cold)
    assert rank_masks([g&coldmask for g in logical.values()])==405  # cold puncture injective on the whole logical carrier

    # Levi graph, with point-packets 0..44 and quotient lines 45..71.
    ledges=sorted((p,L) for L,S in enumerate(K5) for p in S);assert len(ledges)==135
    Levi=nx.Graph();Levi.add_nodes_from(range(72));Levi.add_edges_from((p,45+L) for p,L in ledges)
    CB=nx.cycle_basis(Levi);assert len(CB)==64
    levi_words=[];levi_logical=[]
    for cyc in CB:
        inc=[]
        for a,b in zip(cyc,cyc[1:]+cyc[:1]):
            if a>=45:a,b=b,a
            assert a<45<=b;inc.append((a,b-45))
        coeff=0;phys=0
        for p,L in inc:
            for s in packets[p]:
                coeff ^= 1<<logical_index[(s,L)]
                phys ^= logical[(s,L)]
        # line parities vanish and all hot bits vanish.
        for L in range(27):
            q=sum((coeff>>idx)&1 for (s,ll),idx in logical_index.items() if ll==L)&1
            assert q==0
        assert all(not ((phys>>pei[e])&1) for e in hot)
        levi_logical.append(coeff);levi_words.append(phys)
    assert rank_masks(levi_logical)==rank_masks(levi_words)==64

    out={'passes':[4833,4838],'ambient_code':'[2025,399,14]_2','kernel_code':'[2025,378,14]_2','Levi_code':'[2025,64,96]_2 = 0^405 + Rep_12(H1(Levi(GQ(4,2));F2))',
      'exact_inclusions':['C_Levi <= C_378','C_378 <= C_399'],
      'dimensions':{'Levi':64,'kernel':378,'code399':399,'intersection_Levi_code399':64,'sum_Levi_code399':399,'quotient_code399_over_Levi':335},
      'cold_puncture':{'code399_dimension_after_deleting_405_hot_coordinates':399,'injective':True,'verified_full_logical_cold_rank':405},
      'module_statement':'C_Levi is a PGSp-invariant subcode. No PGSp-invariant complement/direct-summand claim is inferred.',
      'theorem':'The binary Levi cycle code embeds objectwise as a 64-dimensional PGSp-invariant subcode of the zero-outer-syndrome [2025,378,14]_2 kernel and hence of [2025,399,14]_2. Cold puncturing is injective on the full 405-dimensional local logical carrier, hence on code399.',
      'boundary':'Exact binary-code inclusion and dimension theorem. No invariant module splitting is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
