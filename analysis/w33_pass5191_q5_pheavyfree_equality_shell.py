#!/usr/bin/env python3
"""Pass5191: q=5 P-heavy-free weight-625 words are exactly chamber stars.

Pass5177/5179/5180 reduce a P-heavy-free weight-625 word to 25 distinct
P-component minimum atoms.  Each atom has 25 apartments and is owned by two
chambers on one line panel.  This pass computes the exact atom-to-L-chart
incidence design and closes the remaining P-heavy-free gluing problem.

At q=5:
  * 11700 P atoms, 9750 L charts;
  * every atom meets 50 distinct L charts, once each;
  * every L chart meets 60 atoms;
  * for atoms from distinct P components, L-chart codegrees are 0,1,5,25;
  * each atom has row profile 0^9560,1^1950,5^150,25^4;
  * codegree 25 occurs exactly between the five atom labels over one fixed
    same-line chamber pair.

For a selected 25-atom set X (one atom per P component), let w_C be the number
of selected atoms incident with L chart C.  A genuine apartment-code word has
local L cuts of weights 0,5,8,9.  Therefore

  sum_C C(w_C,2) = 2500 + 12 h8 + 18 h9.

On the other hand there are only 300 atom pairs.  At most 50 can have codegree
25 (partition 25 atoms into owner-pair groups of size <=5); every other pair has
codegree <=5.  Hence the same sum is at most

  50*25 + 250*5 = 2500.

Thus h8=h9=0.  Equality forces five complete owner-pair groups of five atoms,
and every cross-group atom pair has codegree five.  The group-level incidence
matrix shows this occurs exactly when the five owner chamber-pairs lie on one
line panel.  On one representative K6 panel, exhaustive testing of all C(15,5)
owner-pair choices against every L-chart cut leaves exactly six choices: the
six vertex stars.  By line transitivity, the global P-heavy-free shell consists
exactly of the 936 chamber stars.

SciPy is used only for sparse exact integer matrix multiplication.  All entries
are small integers, so no floating arithmetic enters the certificate.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import scipy.sparse as sp
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5180_p_atom_panel_resolution import p_component_assignment

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5191_Q5_PHEAVYFREE_EQUALITY_SHELL.json'
PAIRS6=list(itertools.combinations(range(6),2))


def main():
    q=5;G=build_W(q);nA=len(G['apartments'])
    acid,ncomp=p_component_assignment(G);assert ncomp==325
    P=[loc for t,loc in G['charts'] if t=='P']
    L=[loc for t,loc in G['charts'] if t=='L'];assert len(L)==9750

    byflag=[[] for _ in G['flags']]
    for a,es in enumerate(G['apt_edges']):
        for e in es:byflag[e].append(a)

    atom_owners=defaultdict(list)
    for e,A in enumerate(byflag):
        pieces=defaultdict(list)
        for a in A:pieces[acid[a]].append(a)
        for c,v in pieces.items():atom_owners[(c,tuple(sorted(v)))].append(e)
    atoms=list(atom_owners);assert len(atoms)==11700
    assert {len(v) for v in atom_owners.values()}=={2}
    acomp=np.array([x[0] for x in atoms],dtype=np.int16)

    # Apartment -> two L-chart/local-edge incidences.
    ownersL=[[] for _ in range(nA)]
    for li,loc in enumerate(L):
        for k,p in enumerate(PAIRS6):ownersL[loc[p]].append((li,k))
    assert {len(x) for x in ownersL}=={2}

    rows=[];cols=[]
    for ai,(_,aa) in enumerate(atoms):
        seen=set()
        for a in aa:
            for li,_ in ownersL[a]:
                assert li not in seen;seen.add(li);rows.append(ai);cols.append(li)
        assert len(seen)==50
    B=sp.csr_matrix((np.ones(len(rows),dtype=np.int16),(rows,cols)),shape=(11700,9750))
    assert set(np.asarray(B.sum(axis=1)).ravel())=={50}
    assert set(np.asarray(B.sum(axis=0)).ravel())=={60}
    Gram=(B@B.T).tocsr()

    # Distinct-P-component exact codegree scheme.
    profiles=Counter()
    for i in range(11700):
        r=Gram.getrow(i);c=Counter()
        for j,v in zip(r.indices,r.data):
            if j==i or acomp[j]==acomp[i]:continue
            c[int(v)]+=1
        z=11664-sum(c.values())
        profiles[(z,c[1],c[5],c[25])]+=1
    assert profiles=={(9560,1950,150,4):11700}

    owner_pair=[tuple(sorted(atom_owners[a])) for a in atoms]
    pair_atoms=defaultdict(list)
    for ai,p in enumerate(owner_pair):pair_atoms[p].append(ai)
    assert len(pair_atoms)==2340 and {len(v) for v in pair_atoms.values()}=={5}
    # Every codegree-25 neighbor is exactly another label over the same pair.
    for i in range(11700):
        n25={j for j,v in zip(Gram.getrow(i).indices,Gram.getrow(i).data)
             if j!=i and acomp[j]!=acomp[i] and int(v)==25}
        assert n25==set(pair_atoms[owner_pair[i]])-{i}

    # Group incidence vectors.  Cross total 125 means all 25 cross atom pairs
    # have codegree 5 (they cannot have 25 across distinct owner groups).
    groups=list(pair_atoms);gidx={g:i for i,g in enumerate(groups)}
    grow=[];gcol=[];gdat=[]
    for gi,g in enumerate(groups):
        s=np.asarray(B[pair_atoms[g]].sum(axis=0)).ravel()
        nz=np.flatnonzero(s)
        grow.extend([gi]*len(nz));gcol.extend(nz.tolist());gdat.extend(s[nz].astype(np.int16).tolist())
    BG=sp.csr_matrix((np.array(gdat,dtype=np.int16),(grow,gcol)),shape=(2340,9750))
    GG=(BG@BG.T).tocsr()

    # Every owner pair has a unique underlying line (the owners are chambers on it).
    pair_line={}
    for g in groups:
        l0=G['flags'][g[0]][1];l1=G['flags'][g[1]][1];assert l0==l1;pair_line[g]=l0
    for gi,g in enumerate(groups):
        n125={j for j,v in zip(GG.getrow(gi).indices,GG.getrow(gi).data) if j!=gi and int(v)==125}
        same={gidx[h] for h in groups if h!=g and pair_line[h]==pair_line[g]}
        assert n125==same and len(n125)==14

    # On one K6 line, equality reduces to five of the 15 owner pairs.  Build
    # each group's exact local-L mask and test every one of the 3003 choices.
    line0=0
    flags=[e for e,(p,l) in enumerate(G['flags']) if l==line0];assert len(flags)==6
    gpairs=[tuple(sorted(x)) for x in itertools.combinations(flags,2)];assert len(gpairs)==15
    cut_masks=set()
    for mask in range(1<<5):
        S={i for i in range(5) if (mask>>i)&1};z=0
        for k,(i,j) in enumerate(PAIRS6):
            if (i in S)!=(j in S):z|=1<<k
        cut_masks.add(z)
    assert Counter(x.bit_count() for x in cut_masks)=={0:1,5:6,8:15,9:10}

    group_masks={}
    for gp in gpairs:
        D=defaultdict(int)
        for ai in pair_atoms[gp]:
            for a in atoms[ai][1]:
                for li,k in ownersL[a]:D[li]^=1<<k
        group_masks[gp]=D
    valid=[]
    for comb in itertools.combinations(gpairs,5):
        D=defaultdict(int)
        for gp in comb:
            for li,m in group_masks[gp].items():D[li]^=m
        if all(m in cut_masks for m in D.values()):valid.append(comb)
    assert len(valid)==6
    expected=[]
    for e in flags:
        expected.append(frozenset(tuple(sorted((e,f))) for f in flags if f!=e))
    assert {frozenset(x) for x in valid}==set(expected)

    out={
      'pass':5191,'status':'THEOREM_Q5_PHEAVYFREE_WEIGHT625_SHELL_IS_CHAMBER_STARS',
      'atom_L_design':{'atoms':11700,'L_charts':9750,'atom_degree':50,'L_chart_degree':60,
        'distinct_P_component_atom_codegrees':[0,1,5,25],
        'per_atom_profile':{'0':9560,'1':1950,'5':150,'25':4}},
      'pair_moment_identity':'For a genuine 25-atom word, sum_L C(w_L,2)=2500+12 h8+18 h9.',
      'pair_moment_upper_bound':'At most 50 atom pairs have codegree25; the other 250 pairs have codegree<=5, so the sum is <=2500.',
      'heavy_consequence':'h8=h9=0 on the L side; therefore a P-heavy-free weight625 word is heavy-free on both sides.',
      'equality_structure':'The 25 atoms are five complete 5-label owner-pair groups, all on one line panel.',
      'panel_exhaustion':{'candidate_five_pair_sets':3003,'valid_L_cut_sets':6,'valid_sets':'exactly the six K6 vertex stars'},
      'minimum_shell_consequence':'Every q5 weight625 apartment-code word that is P-heavy-free is one of the 936 chamber stars.',
      'remaining_equality_frontier':'Any exotic q5 weight625 word must be P-heavy. Pass5177 then forces P active-chart defect at least 10.',
      'boundary':'This closes the P-heavy-free equality sector, not the P-heavy sector and not the sub-625 distance frontier.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
