#!/usr/bin/env python3
"""Passes 4545/4549 -- explicit cubic-surface transport and 27x36 incidence intertwiner.

Pass 4525 gave an explicit permutation isomorphism from the 27 nonzero singular
vectors of the apartment-dual O^-(6,2) quotient to the repository's 27 cubic-
surface lines.  Pass 4527 did the same for the 36 anisotropic vectors and the 36
Schlaefli double-sixes.  This pass transports those quotient observables into
classical (a_i,b_i,c_ij) language and computes the incidence operator between
the two existing cubic-surface carriers.

Let R be the 27 x 36 binary/integer incidence matrix whose (line,double-six)
entry is one when the cubic line belongs to the 12-line support of the double-
six.  Exact enumeration gives:

  every line occurs in 16 double-sixes;
  every double-six contains 12 lines;
  two meeting cubic lines occur together in 8 double-sixes;
  two skew cubic lines occur together in 6 double-sixes;
  adjacent double-sixes (support intersection 4) meet in 4 lines;
  nonadjacent double-sixes meet in 6 lines.

If A27 is cubic-line MEET adjacency SRG(27,10,1,5), and A36 is double-six
adjacency by support intersection four SRG(36,15,6,6), then

  R R^T = 10 I + 2 A27 + 6 J,
  R^T R = 6 I - 2 A36 + 6 J,
  3 A27 R + R A36 = 20 J.

Hence on centered permutation modules, 3 A27 R + R A36=0.  R has rank 21 over
Q: the trivial line plus the common 20-dimensional constituent survive, while
the 6-dimensional Schlaefli constituent and 15-dimensional double-six
constituent are killed.  This is an exact representation-theoretic transport,
not a parameter-only coincidence.
"""
from __future__ import annotations

import importlib.util,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4545_4549_SCHLAFLI_DOUBLE_SIX_INTERTWINER.json'


def load_cds():
    p=ROOT/'tools'/'compute_double_sixes.py'
    spec=importlib.util.spec_from_file_location('cds4549',p)
    mod=importlib.util.module_from_spec(spec);assert spec.loader is not None;spec.loader.exec_module(mod)
    return mod


def main()->int:
    mod=load_cds();roots=mod.construct_e8_roots();orbits=mod.compute_we6_orbits(roots)
    orb27=[o for o in orbits if len(o)==27][0]
    r=roots[orb27];gram=np.rint(r@r.T).astype(int)
    meet=(gram==0);skew=(gram==1);np.fill_diagonal(meet,False);np.fill_diagonal(skew,False)
    assert set(map(int,meet.sum(1)))=={10}

    k6=mod.find_k_cliques(skew,6);assert len(k6)==72
    ds=[]
    for ai,A in enumerate(k6):
        SA=set(A)
        for bi in range(ai+1,len(k6)):
            B=k6[bi];SB=set(B)
            if SA&SB:continue
            if all(sum(bool(skew[a,b]) for b in B)==1 for a in A) and all(sum(bool(skew[a,b]) for a in A)==1 for b in B):
                ds.append((tuple(A),tuple(B)))
    assert len(ds)==36
    supp=[frozenset(A)|frozenset(B) for A,B in ds]
    R=np.zeros((27,36),dtype=int)
    for j,S in enumerate(supp):
        for i in S:R[i,j]=1
    assert set(map(int,R.sum(1)))=={16} and set(map(int,R.sum(0)))=={12}

    line_pair=Counter()
    for i,j in itertools.combinations(range(27),2):
        line_pair[(bool(meet[i,j]),int(np.dot(R[i],R[j])))] += 1
    assert line_pair==Counter({(False,6):216,(True,8):135})

    A36=np.zeros((36,36),dtype=int);ds_inter=Counter()
    for i,j in itertools.combinations(range(36),2):
        z=len(supp[i]&supp[j]);ds_inter[z]+=1
        if z==4:A36[i,j]=A36[j,i]=1
    assert ds_inter==Counter({6:360,4:270})
    assert set(map(int,A36.sum(1)))=={15}

    I27=np.eye(27,dtype=int);I36=np.eye(36,dtype=int)
    J27=np.ones((27,27),dtype=int);J36=np.ones((36,36),dtype=int);J2736=np.ones((27,36),dtype=int)
    A27=meet.astype(int)
    assert np.array_equal(R@R.T,10*I27+2*A27+6*J27)
    assert np.array_equal(R.T@R,6*I36-2*A36+6*J36)
    assert np.array_equal(3*A27@R+R@A36,20*J2736)
    assert np.linalg.matrix_rank(R)==21

    # Deterministic classical labeling from the first complete double-six.
    A,B=ds[0];match={}
    for a in A:
        q=[b for b in B if skew[a,b]];assert len(q)==1;match[a]=q[0]
    aa=list(A);bb=[match[x] for x in aa]
    rem=sorted(v for v in range(27) if v not in set(A)|set(B));duad={}
    for v in rem:
        q=[i for i in range(6) if meet[v,aa[i]]];assert len(q)==2;duad[tuple(sorted(q))]=v
    labels={}
    for i,v in enumerate(aa):labels[v]=f'a{i}'
    for i,v in enumerate(bb):labels[v]=f'b{i}'
    for ij,v in duad.items():labels[v]=f'c{ij[0]}{ij[1]}'
    assert len(labels)==27

    iso27=[0,6,7,12,25,3,17,13,24,14,22,26,4,19,5,8,23,20,9,2,16,11,15,21,10,18,1]
    new_to_classical=[labels[iso27[i]] for i in range(27)]
    assert sorted(new_to_classical)==sorted(labels.values())

    out={
      'passes':[4545,4549],
      'incidence':{
        'shape':[27,36],'row_sum_double_sixes_per_line':16,'column_sum_lines_per_double_six':12,
        'meeting_line_pair_common_double_sixes':8,'skew_line_pair_common_double_sixes':6,
        'double_six_pair_intersection_counts':{'4':270,'6':360},'rank_over_Q':21},
      'matrix_identities':{
        'RRt':'10 I27 + 2 A27 + 6 J27',
        'RtR':'6 I36 - 2 A36 + 6 J36',
        'adjacency_intertwiner':'3 A27 R + R A36 = 20 J27x36',
        'centered_intertwiner':'3 A27 R + R A36 = 0 on centered modules'},
      'rational_constituents':{
        '27_line_module':'1 + 20 + 6','36_double_six_module':'1 + 20 + 15',
        'R_survives':'1 + 20','R_kills_on_27_side':6,'R_kills_on_36_side':15,
        'nontrivial_singular_value_squared':12,'trivial_singular_value_squared':192},
      'transport':{
        'pass4525_new_singular_index_to_classical_label':new_to_classical,
        'classical_label_convention':'deterministic first double-six; a0..a5, b0..b5, c_ij'},
      'boundary':'Exact finite cubic-surface incidence and representation transport. It transports the apartment-derived orthogonal quotient into the existing Schlaefli carriers; no physical interpretation follows.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
