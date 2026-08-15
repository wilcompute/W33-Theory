#!/usr/bin/env python3
"""Pass5262: q=5 zero-footprint block distance 25 and full apartment distance 625.

The authoritative Pass5238-5245 packet proves C_F=[325,65,25]_2, closes the
weight-625 equality shell, and reduces every strict counterexample to zero
P-component parity.  Pass5259 strengthens the strict reduction: the even local
P-component tensor code has minimum 40, so any word of apartment weight <625
would lie in K0 and use at most 15 P blocks.  Pass5260 identifies K0 as the
560-dimensional kernel of the connected-L syndrome map on the 7800-dimensional
even-block P-side space.

This pass proves d_block(K0)=25.  Reconstruct the 325 local even spaces from the
36 minimum atoms in each P component, apply the exact connected-L triangle
syndrome, and compute a basis of K0.  For the Pass5230 seed weight-8 footprint
dual check D, the projection of K0 to the 8 blocks of D has rank 134.  Deleting
ANY one block of D leaves rank 134.  Therefore no K0 word can meet D in exactly
one nonzero block.  Pass5230 proves the full 24375-word weight-8 shell is one
symplectic orbit, so this no-singleton property holds for every shell check.

Let S be the P-block support of a nonzero K0 word, w=|S|, and t_D=|S cap D|.
No t_D equals one, hence C(t_D,2)>=t_D/2.  The shell has coordinate replication
r=600 and maximum pair codegree lambda=25, so

  300 w <= sum_D C(t_D,2) <= 25 C(w,2),

which gives w>=25.  Sharpness: the symmetric difference of two chamber stars
based at the same W point lies in K0 and has exactly 25 active P components,
each of local weight 40.

Consequently d_block(K0)=25.  But every hypothetical apartment word below 625
would have block support <=15, impossible.  Thus the q=5 apartment code has
minimum distance 625.  The equality shell was already classified in Pass5238,
so its minimum words are exactly the 936 chamber stars.
"""
from __future__ import annotations
import json
from collections import defaultdict, Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import (
    p_component_assignment, atoms, atom_L_syndromes,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5262_Q5_ZEROP_BLOCK_DISTANCE25_FULL_DISTANCE.json'
SEED=(119,124,183,188,209,302,317,318)

def rank_ints(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def independent_indices(rows):
    piv={};ans=[]
    for i,x in enumerate(rows):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;ans.append(i);break
    return ans

def null_dependencies(cols):
    """Return exact dependency basis among binary column vectors stored as ints."""
    piv={};deps=[]
    for i,x in enumerate(cols):
        c=1<<i
        while x:
            p=x.bit_length()-1
            if p in piv:
                y,d=piv[p];x^=y;c^=d
            else:
                piv[p]=(x,c);break
        if not x:deps.append(c)
    return deps,len(piv)

def projection_rank(deps,blocks):
    mask=0
    for c in blocks:mask|=((1<<24)-1)<<(24*c)
    return rank_ints([d&mask for d in deps])

def main():
    G=build_W(5); acid,nc=p_component_assignment(G)
    assert nc==325
    AA,meta,byflag=atoms(G,acid)
    syn,nb=atom_L_syndromes(G,AA)
    assert len(AA)==11700 and nb==97500
    bycomp=defaultdict(list)
    for u,m in enumerate(meta):bycomp[m[3]].append(u)
    assert set(map(len,bycomp.values()))=={36}

    cols=[]
    for c in range(325):
        U=bycomp[c]
        rows=[]
        for u in U:
            z=0
            for a in AA[u]:z|=1<<a
            rows.append(z)
        bi=independent_indices(rows)
        assert len(bi)==25
        B=[U[i] for i in bi]; anchor=B[0]
        # Every minimum atom has odd weight 25.  Differences with one anchor
        # form a 24-dimensional basis of the local even subcode.
        cols.extend(syn[u]^syn[anchor] for u in B[1:])
    assert len(cols)==7800
    deps,r=null_dependencies(cols)
    assert r==7240 and len(deps)==560

    r8=projection_rank(deps,SEED)
    r7=[projection_rank(deps,[c for c in SEED if c!=j]) for j in SEED]
    assert r8==134 and r7==[134]*8

    # Sharp 25-block witness: two chamber stars based at one W point.
    fp=[e for e,(p,l) in enumerate(G['flags']) if p==0]
    assert len(fp)==6
    W=set(byflag[fp[0]])^set(byflag[fp[1]])
    bc=Counter(acid[a] for a in W)
    assert len(W)==1000 and len(bc)==25 and set(bc.values())=={40}

    replication=600;lam=25
    lower=1+replication//lam
    assert lower==25
    out={
      'pass':5262,
      'status':'THEOREM_Q5_FULL_APARTMENT_CODE_DISTANCE625_AND_MINIMUM_SHELL',
      'zero_footprint_residual':{'dimension':560,'P_blocks':325,
        'local_even_dimension':24,'connected_L_rank_on_even_space':7240},
      'weight8_seed':list(SEED),
      'seed_projection_rank':r8,
      'seed_delete_one_projection_ranks':r7,
      'global_no_singleton_reason':'Pass5230: all 24375 weight-8 footprint-dual supports form one symplectic orbit; K0 is automorphism invariant.',
      'shell_parameters':{'checks':24375,'replication':600,'max_pair_codegree':25},
      'block_moment_inequality':'300*w <= sum_D binom(t_D,2) <= 25*binom(w,2), because t_D is never 1.',
      'zero_footprint_block_distance':25,
      'sharp_block_witness':{'construction':'difference of two chamber stars based at the same W point','active_P_blocks':25,'local_weight_per_active_block':40,'apartment_weight':1000},
      'strict_reduction':'Pass5259: every hypothetical q5 apartment word of weight<625 belongs to K0 and has at most15 active P blocks.',
      'strict_conclusion':'No q5 apartment-code word has weight<625.',
      'apartment_code':'[73125,625,625]_2',
      'minimum_shell':'Exactly the 936 chamber stars, using the authoritative Pass5238 equality-shell classification.',
      'boundary':'This is a q=5 theorem. It does not prove the all-q distance q^4 theorem.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
