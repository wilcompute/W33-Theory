#!/usr/bin/env python3
"""Pass5284: complete q=5 K0 block-minimum WORD shell.

Pass5262 proves the zero-P residual K0 has P-block distance 25. Pass5269 proves
that every block-minimum support is one of the 156 W-point footprints. This pass
computes the residual restricted to one point footprint and classifies every word
on that support.

For a fixed W point p, the common P footprint of its six chamber stars contains
25 P components. In each component use a 24-dimensional basis of the even local
subcode, obtained as differences of one minimum atom with the other independent
minimum atoms. The resulting 600 local variables map to the connected-L syndrome
space with rank 596, so the restricted K0 kernel has dimension 4 and exactly 15
nonzero words. All 15 use all 25 blocks (by d_block(K0)=25), and direct apartment
reconstruction identifies them exactly with the C(6,2)=15 pairwise differences
of the six chamber stars based at p. Every such word has local weight 40 in every
active block and global apartment weight 1000.

By point transitivity and Pass5269's support classification, the complete K0
block-minimum word shell therefore has 156*15=2340 words, all of Hamming weight
1000. This is a q=5 theorem; it does not classify higher block-weight K0 words.
"""
from __future__ import annotations
import itertools, json
from collections import defaultdict, Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5214_q5_connectedL_point_footprint_gluing import (
    p_component_assignment, atoms, atom_L_syndromes,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5284_Q5_K0_BLOCK_MINIMUM_WORD_SHELL.json'

def indep(rows):
    piv={}; ans=[]
    for i,x in enumerate(rows):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y; ans.append(i); break
    return ans

def null_deps(cols):
    piv={}; deps=[]
    for i,x in enumerate(cols):
        c=1<<i
        while x:
            p=x.bit_length()-1
            if p in piv:
                y,d=piv[p]; x^=y; c^=d
            else:
                piv[p]=(x,c); break
        if not x:deps.append(c)
    return deps,len(piv)

def xor_selected(vecs,mask):
    z=0; i=0
    while mask:
        lb=mask&-mask; i=lb.bit_length()-1; z^=vecs[i]; mask-=lb
    return z

def main():
    G=build_W(5); acid,nc=p_component_assignment(G); assert nc==325
    AA,meta,byflag=atoms(G,acid); syn,nb=atom_L_syndromes(G,AA); assert nb==97500
    byc=defaultdict(list)
    for u,m in enumerate(meta): byc[m[3]].append(u)
    p=0; flags=[e for e,(pp,l) in enumerate(G['flags']) if pp==p]; assert len(flags)==6
    footprints=[{acid[a] for a in byflag[e]} for e in flags]
    assert all(S==footprints[0] for S in footprints)
    C=sorted(footprints[0]); assert len(C)==25

    aptcols=[]; syncols=[]; colblock=[]
    for c in C:
        U=byc[c]; assert len(U)==36
        rows=[]
        for u in U:
            z=0
            for a in AA[u]: z|=1<<a
            rows.append(z)
        I=indep(rows); assert len(I)==25
        B=[U[i] for i in I]; anchor=B[0]
        ar=rows[I[0]]
        for j,u in enumerate(B[1:],1):
            aptcols.append(rows[I[j]]^ar)
            syncols.append(syn[u]^syn[anchor])
            colblock.append(c)
    assert len(aptcols)==len(syncols)==25*24==600
    deps,r=null_deps(syncols)
    assert r==596 and len(deps)==4

    words=set()
    for m in range(1,1<<4):
        coeff=0
        for i,d in enumerate(deps):
            if (m>>i)&1: coeff^=d
        w=xor_selected(aptcols,coeff)
        assert w and w.bit_count()==1000
        bc=Counter(acid[a] for a in range(len(G['apartments'])) if (w>>a)&1)
        assert len(bc)==25 and set(bc)==set(C) and set(bc.values())=={40}
        words.add(w)
    assert len(words)==15

    stars=[]
    for e in flags:
        z=0
        for a in byflag[e]: z|=1<<a
        assert z.bit_count()==625
        stars.append(z)
    pairdiff={stars[i]^stars[j] for i,j in itertools.combinations(range(6),2)}
    assert len(pairdiff)==15 and pairdiff==words

    out={
      'pass':5284,
      'status':'THEOREM_Q5_COMPLETE_K0_BLOCK_MINIMUM_WORD_SHELL',
      'K0_dimension':560,
      'block_distance':25,
      'minimum_supports':156,
      'fixed_point_footprint_blocks':25,
      'restricted_even_variables':600,
      'restricted_connected_L_rank':596,
      'restricted_kernel_dimension':4,
      'nonzero_words_per_minimum_support':15,
      'identification_per_support':'Exactly the C(6,2)=15 differences of the six chamber stars based at that W point.',
      'local_weight_per_active_block':40,
      'apartment_weight_per_K0_block_minimum_word':1000,
      'complete_K0_block_minimum_words':2340,
      'fiber_description':'Each of the 156 W-point supports carries a 4-dimensional binary kernel whose 15 nonzero vectors are the 15 chamber-star pair differences.',
      'boundary':'Complete q5 K0 block-minimum word-shell theorem only; no claim about higher block-weight K0 shells or all q.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
