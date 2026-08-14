#!/usr/bin/env python3
"""Pass5180 (bonkers): P-component minimum atoms are q-labelled line-panel edges.

Pass5177 identifies the P/opposite-point apartment components with
Cut(K_{q+1}) tensor Cut(K_{q+1}); Pass5179 classifies their q^2-weight minimum
words as the (q+1)^2 simple tensors of factor vertex stars.

This producer reconnects those algebraic atoms to chamber geometry.  For every
finite anchor q=2,3,4,5 it constructs W(3,q), the P-component partition of the
apartments, and every chamber-star restriction.  The resulting exact pattern is:

  * each chamber star meets q^2 P components, in q^2 apartments per component;
  * every P component has exactly (q+1)^2 nonzero chamber-star restrictions;
  * each such minimum atom is realized by exactly two chamber stars;
  * the two chambers share the same line;
  * every unordered same-line chamber pair occurs as an atom in exactly q P
    components;
  * for one chamber, each of its q line-panel partners occurs in exactly q of
    the chamber's q^2 active P components.

Thus the P minimum-atom carrier is a q-fold labelled cover of the line-panel
edge set.  At q=5 there are 325*36=11700 atoms = 5*(156*C(6,2)).

Combining with the exhaustive Pass5177 heavy-shell certificate gives an exact
reduction of the unresolved P-heavy-free weight-625 equality sector: it consists
of exactly 25 nonzero P components, each carrying one of its 36 minimum atoms.
Equivalently it is a 25-atom selection in this q-labelled line-panel carrier,
subject to the connected L-side theta constraints.  This specifically isolates
the L-heavy-only exotic sector; it does not prove that sector empty.
"""
from __future__ import annotations
import json
from collections import defaultdict,Counter,deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5180_P_TENSOR_ATOM_LINE_PANEL_REDUCTION.json'


def p_components(G):
    charts=[loc for typ,loc in G['charts'] if typ=='P']
    nA=len(G['apartments']); owners=[[] for _ in range(nA)]
    for ci,loc in enumerate(charts):
        for a in loc.values(): owners[a].append(ci)
    assert {len(x) for x in owners}=={2}
    adj=[set() for _ in charts]
    for u,v in owners:
        adj[u].add(v);adj[v].add(u)
    cid=[-1]*len(charts); comps=[]
    for s in range(len(charts)):
        if cid[s]>=0: continue
        k=len(comps); cid[s]=k; C=[];Q=[s]
        while Q:
            u=Q.pop();C.append(u)
            for v in adj[u]:
                if cid[v]<0: cid[v]=k;Q.append(v)
        comps.append(C)
    apt_comp=[cid[owners[a][0]] for a in range(nA)]
    assert all(cid[owners[a][0]]==cid[owners[a][1]] for a in range(nA))
    return comps,apt_comp


def anchor(q):
    G=build_W(q); comps,apt_comp=p_components(G)
    expected_components=q*q*(q*q+1)//2
    assert len(comps)==expected_components

    # Group every chamber-star support by P component without materializing bitsets.
    local=[defaultdict(list) for _ in G['flags']]
    for a,edges in enumerate(G['apt_edges']):
        c=apt_comp[a]
        for f in edges: local[f][c].append(a)

    assert {len(x) for x in local}=={q*q}
    assert {len(v) for x in local for v in x.values()}=={q*q}

    # A minimum atom is identified by (component, exact apartment subset).
    atom_flags=defaultdict(list)
    for f,x in enumerate(local):
        for c,aa in x.items(): atom_flags[(c,tuple(sorted(aa)))].append(f)

    expected_atoms=expected_components*(q+1)**2
    assert len(atom_flags)==expected_atoms
    assert {len(fs) for fs in atom_flags.values()}=={2}

    pair_mult=Counter()
    for fs in atom_flags.values():
        i,j=fs
        pi,li=G['flags'][i]; pj,lj=G['flags'][j]
        assert li==lj and pi!=pj
        pair_mult[tuple(sorted((i,j)))] += 1
    assert set(pair_mult.values())=={q}

    # Every same-line chamber pair is represented and represented exactly q times.
    same_line_pairs=0
    for L in G['lines']:
        same_line_pairs += (q+1)*q//2
    assert len(pair_mult)==same_line_pairs
    assert expected_atoms==q*same_line_pairs

    # From a fixed chamber, its q line-panel partners each recur q times among
    # its q^2 active P-component atoms.
    partner_profiles=[]
    for f,x in enumerate(local):
        P=Counter()
        for c,aa in x.items():
            fs=atom_flags[(c,tuple(sorted(aa)))]
            g=fs[0] if fs[1]==f else fs[1]
            P[g]+=1
        assert len(P)==q and set(P.values())=={q}
        assert all(G['flags'][g][1]==G['flags'][f][1] for g in P)
        partner_profiles.append(tuple(sorted(P.values())))

    chamber_count=len(G['flags'])
    component_star_degree=chamber_count*q*q//expected_components
    assert component_star_degree==2*(q+1)**2

    return {
      'q':q,
      'chambers':chamber_count,
      'P_components':expected_components,
      'minimum_atoms_per_component':(q+1)**2,
      'total_P_minimum_atoms':expected_atoms,
      'same_line_chamber_pairs':same_line_pairs,
      'atom_cover_multiplicity_over_line_pair':q,
      'chamber_active_P_components':q*q,
      'apartments_per_active_component_in_star':q*q,
      'chamber_partner_count_on_line':q,
      'components_per_partner':q,
      'chamber_stars_through_component':component_star_degree,
      'atom_realizing_chamber_stars':2
    }


def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    q=5
    heavy_path=ROOT/'data/PART_W33_PASS5177_Q5_TENSOR_HEAVY_SHELL.json'
    heavy=json.loads(heavy_path.read_text())
    assert heavy['status']=='THEOREM_Q5_P_SIDE_EXOTIC_COAREA_DEFECT_AT_LEAST_10'
    assert heavy['P_side_weight625_knapsack']['minimum_zero_cost_solution']=='25 P-component minimum words of weight 25'
    out={
      'pass':5180,
      'status':'THEOREM_P_TENSOR_ATOM_LINE_PANEL_COVER_AND_Q5_EQUALITY_REDUCTION',
      'all_q_atom_geometry':{
        'P_components':'q^2(q^2+1)/2',
        'minimum_atoms_per_component':'(q+1)^2',
        'atom_carrier':'q-fold labelled cover of unordered same-line chamber pairs',
        'atom_count_identity':'[q^2(q^2+1)/2](q+1)^2 = q * [(q+1)(q^2+1) C(q+1,2)]',
        'atom_realizers':'Each minimum P atom is the common component restriction of exactly two chamber stars sharing one line.',
        'star_footprint':'A chamber star uses q^2 P components. Its q line-panel partners each occur in exactly q of those component atoms.'
      },
      'anchors':A,
      'q5':{
        'P_components':325,
        'minimum_atoms_per_component':36,
        'atom_pool':11700,
        'line_panel_pairs':2340,
        'labels_per_line_panel_pair':5,
        'chamber_stars':936,
        'components_per_star':25,
        'stars_through_component':72,
        'P_heavy_free_weight625_reduction':'exactly 25 distinct P components, one weight-25 minimum atom in each; all connected L-side theta constraints remain to be imposed'
      },
      'consequence':'The unresolved L-heavy-only q5 weight-625 sector is a finite 25-atom compatibility problem on a q-labelled line-panel carrier, not an unconstrained apartment-coordinate search.',
      'boundary':'This is an exact reduction, not an emptiness proof. P-heavy weight-625 candidates and the reduced L-heavy-only compatibility problem remain logically possible until separately excluded.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
