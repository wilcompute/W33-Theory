#!/usr/bin/env python3
"""Pass5144: all-q root-coset Gram / theta-Cayley bridge.

For the maximal-unipotent controller U(q), let H be the 0/1 incidence matrix
between U(q) elements and the 4q^3 right cosets of the four positive-root
subgroups.  Two distinct group elements lie in a common root coset exactly when
they are adjacent in the Pass5132 theta Cayley graph.  Every element lies in
four root cosets.  Therefore, integrally and for every finite q,

    H H^T = 4 I + A_theta.

This promotes the q=3 observation from Pass5107 to the complete controller
family and identifies the rational coset-incidence defect with the theta -4
eigenspace.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,I4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5144_ROOT_COSET_GRAM_THETA_BRIDGE.json'

MINUS4={2:1,3:12,4:72,5:220}  # exact multiplicities from Pass5137


def anchor(q):
    U,R,F=roots(q);idx={g:i for i,g in enumerate(U)}
    cosets=set()
    for H in R:
        for g in U:
            cosets.add(frozenset(idx[mm(g,h,F)] for h in H))
    assert len(cosets)==4*q**3
    assert {len(C) for C in cosets}=={q}

    row_deg=[0]*len(U);pair_mult={}
    for C in cosets:
        for u in C:row_deg[u]+=1
        for a,b in itertools.combinations(sorted(C),2):
            e=(a,b);pair_mult[e]=pair_mult.get(e,0)+1
    assert set(row_deg)=={4}
    assert set(pair_mult.values())=={1}

    # Independent Cayley edge construction.
    e=I4();conn=[]
    for H in R:
        for h in H:
            if h!=e:conn.append(h)
    cayley=set()
    for i,g in enumerate(U):
        for h in conn:
            j=idx[mm(g,h,F)]
            if i!=j:cayley.add(tuple(sorted((i,j))))
    assert cayley==set(pair_mult)
    assert len(cayley)==2*q**4*(q-1)

    null=MINUS4[q];rank=q**4-null
    return {'q':q,'rows_U':q**4,'root_coset_columns':4*q**3,'row_weight':4,
            'column_weight':q,'theta_edges':len(cayley),'gram_identity_exact':True,
            'theta_minus4_multiplicity':null,'rational_incidence_rank':rank,
            'rational_cokernel_free_rank':null}


def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={
      'pass':5144,
      'status':'THEOREM_ALL_Q_ROOT_COSET_GRAM_THETA_BRIDGE',
      'identity':'H H^T = 4 I + A_theta over Z',
      'all_q_proof':'Each U(q) element belongs to one coset of each of the four positive-root subgroups. Distinct elements share a root coset iff their quotient lies in one nonidentity positive-root subgroup; different root subgroups meet only in identity, so the shared coset is unique. Thus Gram diagonal entries are 4 and off-diagonal entries are exactly theta adjacency.',
      'spectral_corollary':'Over characteristic zero, ker(H^T)=E_{-4}(A_theta), so rank(H)=q^4-mult_theta(-4).',
      'anchors':A,
      'q3_weld':'At q=3 this is the 81x108 Pass5107 matrix: rank_Q=69 and the free 12-dimensional cokernel is exactly the theta -4 sector. The additional Smith Z/3 torsion from Pass5121 is invisible over Q and remains a genuinely arithmetic defect.',
      'q5_prediction_target':'At q=5 the exact Pass5137 spectrum forces rank_Q(H)=405 and free rational defect dimension 220; an integral Smith census can now target torsion on top of this fixed free part.',
      'boundary':'The identity is integral and all-q. The displayed -4 multiplicities/ranks are certified here only for q=2,3,4,5 via Pass5137; no all-q rank formula is asserted.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
