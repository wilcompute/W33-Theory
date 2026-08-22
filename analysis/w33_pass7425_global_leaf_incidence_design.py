#!/usr/bin/env python3
"""Pass7425: exact incidence algebra of the 2240 Eisenstein W33 leaves on 1120 E8 A2 subsystems.

This is a small exact audit built from already-certified Pass7401-7424 data:
- global A2 association scheme valencies (1,120,648,270,81) and eigenmatrix P;
- 2240 leaves, 40 A2s per leaf, 80 leaves through each A2;
- 8 leaves through each orthogonal A2 pair;
- the leaf stabilizer induces Aut(W(3,3)), transitive on its 540 noncollinear pairs.
"""
from fractions import Fraction
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7425_GLOBAL_LEAF_INCIDENCE_DESIGN.json'

P=[
 [1,120,648,270,81],
 [1,20,-12,-30,21],
 [1,8,-24,18,-3],
 [1,-4,12,-6,-3],
 [1,-40,-24,30,33],
]
MULT=[1,84,300,700,35]
VAL=[1,120,648,270,81]


def main():
    leaves=2240; points=1120; block=40; rep=80
    assert leaves*block==points*rep==89600
    # A leaf is W(3,3): among the 39 companions of one point, 12 are orthogonal/collinear
    # and 27 are nonorthogonal/noncollinear.  The leaf stabilizer is transitive on those
    # 27, so all 540 noncollinear pairs in a leaf lie in one global nonorthogonal orbital.
    orth_pair_rep=8
    fixed_point_pair_incidences=rep*(block-1)
    nonorth_inc=fixed_point_pair_incidences-120*orth_pair_rep
    assert nonorth_inc==2160
    candidates={648: Fraction(nonorth_inc,648),270:Fraction(nonorth_inc,270),81:Fraction(nonorth_inc,81)}
    integral={k:int(v) for k,v in candidates.items() if v.denominator==1}
    assert integral=={270:8}
    pair_reps=[rep,8,0,8,0]
    # B^T B = 80 I + 8(A_orth + A_270).
    eig=[]
    for row in P:
        eig.append(pair_reps[0]+pair_reps[1]*row[1]+pair_reps[3]*row[3])
    assert eig==[3200,0,288,0,0]
    rank=sum(m for m,e in zip(MULT,eig) if e)
    assert rank==301
    centered=[0,eig[1],eig[2],eig[3],eig[4]]
    # subtracting the row mean kills only the trivial constituent
    centered[0]=0
    assert centered==[0,0,288,0,0]
    centered_row_norm=Fraction(288*300,2240)
    assert centered_row_norm==Fraction(270,7)
    # Global unordered pair-incidence audit.
    global_pair_inc=leaves*(block*(block-1)//2)
    rhs=(points*120//2)*8+(points*270//2)*8
    assert global_pair_inc==rhs==1747200
    out={
      'schema':'w33.pass7425.global_leaf_incidence_design.v1','status':'PASS',
      'points_A2':points,'leaves_W33':leaves,'A2_per_leaf':block,'leaves_per_A2':rep,
      'global_A2_relation_valencies':VAL,
      'pair_replication_by_relation':[80,8,0,8,0],
      'nonorthogonal_relation_in_a_leaf':'the unique global valency-270 relation',
      'proof_of_relation_selection':'Aut(W33) is transitive on leaf noncollinear pairs; fixed-point double counting gives 2160 nonorthogonal leaf incidences, and among global valencies 648,270,81 only 270 divides 2160 integrally, giving replication 8.',
      'incidence_gram':'B^T B = 80 I + 8(A_120 + A_270)',
      'incidence_gram_eigenvalues_by_global_A2_constituent':[3200,0,288,0,0],
      'real_rank_B':rank,
      'real_column_module':'1 + V_300',
      'centered_frame':'C^T C = 288 P_{V300}',
      'centered_row_norm_squared':'270/7',
      'unordered_pair_incidence_total':global_pair_inc,
      'theorem':'The 2240 Eisenstein W33 leaves form a two-relation tactical design inside the 1120-point E8 A2 association scheme: two A2s share a leaf iff they are in the orthogonality relation (valency 120) or the valency-270 relation, and then they lie in exactly eight leaves. After centering, the 2240 leaf indicators are a tight frame for the irreducible 300-dimensional A2 constituent.',
      'boundary':'Finite Weyl/association-scheme theorem. No physical ensemble or continuum interpretation.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rank':rank,'nonzero_eigs':[3200,288]}))
if __name__=='__main__':main()
