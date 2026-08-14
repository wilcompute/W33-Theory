#!/usr/bin/env python3
"""Pass5180 (bonkers): P-minimum atoms resolve line-panel chamber overlaps.

Pass5177 gives the P/opposite-point chart decomposition into tensor components
C_q=Cut(K_{q+1}) tensor Cut(K_{q+1}), and Pass5179 classifies the q^2-weight
minimum words of each component. This pass identifies those abstract minimum
words geometrically inside the apartment code.

For every chamber star we compute its restrictions to P components. The q^2
nonzero restrictions all have weight q^2, hence are P-component minimum atoms.
Across all chamber stars there are exactly as many distinct restrictions as the
full tensor minimum shell predicts. Therefore every P minimum atom occurs this
way. Each distinct atom occurs in exactly two chamber stars; the two chambers
share a line panel. Each same-line chamber pair owns exactly q atoms.
"""
from __future__ import annotations
import json
from collections import Counter,defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5180_P_ATOM_PANEL_RESOLUTION.json'

def p_component_assignment(G):
    P=[loc for t,loc in G['charts'] if t=='P'];nA=len(G['apartments'])
    parent=list(range(len(P)));o1=[-1]*nA
    def find(x):
        while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        a=find(a);b=find(b)
        if a!=b:parent[b]=a
    for ci,loc in enumerate(P):
        for a in loc.values():
            if o1[a]<0:o1[a]=ci
            else:union(ci,o1[a])
    roots={};acid=[]
    for a in range(nA):
        r=find(o1[a])
        if r not in roots:roots[r]=len(roots)
        acid.append(roots[r])
    return acid,len(roots)

def anchor(q):
    G=build_W(q);acid,nc=p_component_assignment(G)
    byflag=[[] for _ in G['flags']]
    for a,es in enumerate(G['apt_edges']):
        for e in es:byflag[e].append(a)

    atom_owners=defaultdict(list)
    for e,A in enumerate(byflag):
        pieces=defaultdict(list)
        for a in A:pieces[acid[a]].append(a)
        assert len(pieces)==q*q
        assert {len(v) for v in pieces.values()}=={q*q}
        for cid,v in pieces.items():atom_owners[(cid,tuple(sorted(v)))].append(e)

    predicted_atoms=nc*(q+1)**2
    assert len(atom_owners)==predicted_atoms
    assert {len(v) for v in atom_owners.values()}=={2}
    pair_mult=Counter()
    for owners in atom_owners.values():
        e,f=owners
        pe,le=G['flags'][e];pf,lf=G['flags'][f]
        assert le==lf and pe!=pf
        pair_mult[tuple(sorted((e,f)))]+=1
    assert set(pair_mult.values())=={q}

    flags_by_line=defaultdict(list)
    for e,(p,l) in enumerate(G['flags']):flags_by_line[l].append(e)
    panel_pairs=sum(len(es)*(len(es)-1)//2 for es in flags_by_line.values())
    assert len(pair_mult)==panel_pairs
    assert predicted_atoms==q*panel_pairs

    # Exact pair-star intersection resolution follows from the common atoms.
    sample_pair=next(iter(pair_mult))
    e,f=sample_pair;inter=set(byflag[e])&set(byflag[f])
    assert len(inter)==q**3
    C=Counter(acid[a] for a in inter)
    assert len(C)==q and set(C.values())=={q*q}

    return {'q':q,'P_components':nc,'P_atoms':predicted_atoms,
      'chambers':len(G['flags']),'atoms_per_chamber_star':q*q,
      'atom_weight':q*q,'atom_owner_multiplicity':2,
      'same_line_chamber_pairs':panel_pairs,'atoms_per_same_line_pair':q,
      'pair_star_intersection_weight':q**3,'pair_resolution_piece_weight':q*q,
      'all_chamber_restrictions_exhausted':True,'all_atom_owners_checked':True}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5180,'status':'THEOREM_P_ATOM_LINE_PANEL_RESOLUTION',
      'statement':'P-component minimum atoms form a q-fold resolution of pairs of distinct chambers on one line panel. Every P atom lies in exactly two chamber stars sharing that line; every such chamber pair owns exactly q atoms; every chamber star is the disjoint union of q^2 atoms.',
      'counts':{
        'P_components':'q^2(q^2+1)/2','atoms_per_component':'(q+1)^2',
        'total_P_atoms':'q^2(q^2+1)(q+1)^2/2',
        'same_line_chamber_pairs':'q(q^2+1)(q+1)^2/2',
        'atoms_per_pair':'q','atoms_per_chamber_star':'q^2','atom_weight':'q^2'},
      'star_factorization':'For chamber e, its q same-line panel neighbours f each contribute all q atoms over {e,f}; these q^2 atoms partition Star(e).',
      'proof_bridge':'Every chamber-star restriction is a weight-q^2 P-component word, hence a tensor minimum atom by Pass5179. The exhaustive q=2,3,4,5 anchors show that these restrictions contain exactly the predicted total number of tensor minimum atoms, each twice, with same-line owners. The family count agrees identically with the P tensor shell and panel incidence formulas.',
      'anchors':A,
      'q5_use':'A P-heavy-free weight-625 word consists of exactly 25 disjoint P-atoms. A chamber star is the special 25-atom pattern formed by all five atom copies over each of the five line-panel edges incident with one chamber.',
      'boundary':'The q=2,3,4,5 identification is exact and exhaustive. The displayed family incidence formulas are structural consequences of the tensor and panel counts; the connected L-side constraints still decide which 25-atom q5 unions are genuine full-code words.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
