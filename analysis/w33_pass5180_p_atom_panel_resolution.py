#!/usr/bin/env python3
"""Pass5180 (bonkers): P-minimum atoms resolve line-panel chamber overlaps.

Pass5177 gives the P/opposite-point chart decomposition into tensor components
C_q=Cut(K_{q+1}) tensor Cut(K_{q+1}), and Pass5179 classifies the q^2-weight
minimum words of each component.  This pass identifies those abstract minimum
words geometrically inside the apartment code.

For a chamber e=(p,l), restrict its q^4-apartment chamber-star support to P
components.  Exactly q^2 components are nonzero and each restriction has weight
q^2, hence is a P-component minimum atom.  If e,f are distinct chambers on the
same line panel l, then |Star(e) intersect Star(f)|=q^3.  Its restriction to P
components consists of exactly q common atoms of weight q^2.  Conversely every
P minimum atom lies in exactly two chamber stars and those chambers share a
line panel.  Thus P-atoms form a q-fold resolution of same-line chamber pairs.

A chamber star is therefore the disjoint union of q^2 P-atoms: for each of its
q panel-neighbour chambers, all q atoms lying over that pair.
"""
from __future__ import annotations
import itertools,json
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

def anchor(q,exhaust_pairs=True):
    G=build_W(q);acid,nc=p_component_assignment(G);nA=len(G['apartments'])
    byflag=[[] for _ in G['flags']]
    for a,es in enumerate(G['apt_edges']):
        for e in es:byflag[e].append(a)
    # Every chamber star splits into q^2 equal P pieces.
    star_profiles=[]
    for e in range(len(G['flags'])):
        C=Counter(acid[a] for a in byflag[e])
        assert len(C)==q*q and set(C.values())=={q*q}
        star_profiles.append(tuple(sorted(C)))
    # Same-line chamber pairs have q common P pieces of q^2 apartments.
    flags_by_line=defaultdict(list)
    for e,(p,l) in enumerate(G['flags']):flags_by_line[l].append(e)
    panel_pairs=0
    sample_limit=None if exhaust_pairs else 12
    checked=0
    for es in flags_by_line.values():
        for e,f in itertools.combinations(es,2):
            panel_pairs+=1
            if sample_limit is not None and checked>=sample_limit:continue
            A=set(byflag[e]);inter=[a for a in byflag[f] if a in A]
            assert len(inter)==q**3
            C=Counter(acid[a] for a in inter)
            assert len(C)==q and set(C.values())=={q*q}
            checked+=1
    total_atoms=nc*(q+1)**2
    expected_pairs=len(G['lines'])*(q*(q+1)//2)
    assert panel_pairs==expected_pairs
    assert total_atoms==q*panel_pairs
    return {'q':q,'P_components':nc,'P_atoms':total_atoms,
      'chambers':len(G['flags']),'atoms_per_chamber_star':q*q,
      'atom_weight':q*q,'same_line_chamber_pairs':panel_pairs,
      'atoms_per_same_line_pair':q,'pair_star_intersection_weight':q**3,
      'pair_resolution_weight':q*q,
      'pair_checks_exhaustive':exhaust_pairs,'pair_checks_performed':checked}

def main():
    # q=5 all-pair enumeration is unnecessarily expensive; the family proof and
    # all smaller fields are exhaustive, while q5 checks a transitivity-sized sample.
    A={str(q):anchor(q,exhaust_pairs=(q<5)) for q in (2,3,4,5)}
    out={'pass':5180,'status':'THEOREM_P_ATOM_LINE_PANEL_RESOLUTION',
      'statement':'P-component minimum atoms form a q-fold resolution of pairs of distinct chambers on one line panel. Every atom lies in exactly two chamber stars sharing that line; every such chamber pair owns exactly q atoms; every chamber star is the disjoint union of q^2 atoms.',
      'counts':{
        'P_components':'q^2(q^2+1)/2',
        'atoms_per_component':'(q+1)^2',
        'total_P_atoms':'q^2(q^2+1)(q+1)^2/2',
        'same_line_chamber_pairs':'q(q^2+1)(q+1)^2/2',
        'atoms_per_pair':'q',
        'atoms_per_chamber_star':'q^2',
        'atom_weight':'q^2'},
      'star_factorization':'For chamber e, its q same-line panel neighbours f each contribute all q atoms over the pair {e,f}; these q^2 atoms partition Star(e).',
      'proof_bridge':'Pass5179 identifies every nonzero q^2 P-component restriction as a tensor minimum atom. The P-component incidence plus the generalized-quadrangle panel count gives the q-fold ownership and the total-incidence identities.',
      'anchors':A,
      'q5_use':'A P-heavy-free weight-625 word consists of exactly 25 disjoint P-atoms. A chamber star is the special 25-atom pattern formed by all five atom copies over each of the five panel edges incident with one chamber.',
      'boundary':'This is a P-side structural theorem. The connected L-side constraints decide which 25-atom P-heavy-free unions are genuine full-code words; no claim that every such union is a chamber star is made here.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
