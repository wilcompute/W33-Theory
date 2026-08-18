#!/usr/bin/env python3
"""Pass7162 addendum: compare the code's S3 wr C2 outer action with natural E8 root-coordinate actions.

This is an object-level firewall against interpreting length 248 as the E8 adjoint basis merely
because dim(E8)=248.  We compare the actual permutation G-set on code coordinates (using the
canonical weighted column-block lift) with four natural coordinate-permutation extensions of
the same six-point S3 wr C2 action to the standard 8-coordinate E8 root model.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import w33_pass7147_7153_pgl2_hexad_code_closure as h

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7162_E8_OUTER_CHARACTER_AUDIT.json'

def pmask(mask,g):
    z=0
    for i in range(6):
        if (mask>>i)&1: z|=1<<g[i]
    return z

def roots_e8_doubled():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for a in (-2,2):
            for b in (-2,2):
                v=[0]*8;v[i]=a;v[j]=b;R.append(tuple(v))
    for s in itertools.product((-1,1),repeat=8):
        if sum(x<0 for x in s)%2==0:R.append(tuple(s))
    assert len(R)==240 and len(set(R))==240
    return tuple(R)

def block_swap_bit(g,T0,T1):
    return int(g[T0[0]] in T1)

def parity_perm(g):
    inv=sum(g[i]>g[j] for i in range(6) for j in range(i+1,6))
    return inv&1

def extend8(g,bit):
    return tuple(g)+(7,6) if bit else tuple(g)+(6,7)

def apply8(v,g8):
    out=[0]*8
    for i in range(8):out[g8[i]]=v[i]
    return tuple(out)

def orbits(items,G,act):
    unseen=set(items); sizes=[]
    while unseen:
        x=next(iter(unseen));O={act(x,g) for g in G};assert O<=set(items)
        unseen-=O;sizes.append(len(O))
    return sorted(sizes)

def main():
    P9,sets,union,cm,triple_masks,outer,C,dual,shell,triple_pts,one,both,Aperm,Fperm=h.build_hexad()
    G=tuple(outer);assert len(G)==72
    T0=tuple(i for i in range(6) if (triple_masks[0]>>i)&1);T1=tuple(i for i in range(6) if (triple_masks[1]>>i)&1)
    # Canonical weighted block lift of the outer action to 248 coordinates: each multiplicity copy is carried in parallel.
    distinct=tuple(sorted(cm))
    mask_orbs=orbits(distinct,G,lambda m,g:pmask(m,g))
    # Actual coordinate orbits split each mask orbit into multiplicity-many parallel copies.
    seen=set(); coord_orbits=[]
    while len(seen)<len(distinct):
        m=next(x for x in distinct if x not in seen);O={pmask(m,g) for g in G};seen|=O
        mult=cm[m];assert all(cm[x]==mult for x in O)
        coord_orbits += [len(O)]*mult
    coord_orbits=sorted(coord_orbits);assert sum(coord_orbits)==248
    code_char=Counter()
    for g in G:
        fixed=sum(cm[m] for m in distinct if pmask(m,g)==m)
        code_char[fixed]+=1
    roots=roots_e8_doubled();axes=tuple(('a',i) for i in range(8));rootlabels=tuple(('r',r) for r in roots);labels=rootlabels+axes
    def act_label(x,g8):
        if x[0]=='a':return ('a',g8[x[1]])
        return ('r',apply8(x[1],g8))
    variants={}
    for name,bitfun in {
      'fix_last2':lambda g:0,
      'swap_last2_on_blockswap':lambda g:block_swap_bit(g,T0,T1),
      'swap_last2_on_parity':lambda g:parity_perm(g),
      'swap_last2_on_blockswap_xor_parity':lambda g:block_swap_bit(g,T0,T1)^parity_perm(g),
    }.items():
        G8=tuple(extend8(g,bitfun(g)) for g in G)
        assert len(set(G8))==72
        eorbs=orbits(labels,G8,act_label);assert sum(eorbs)==248
        echar=Counter()
        for g8 in G8:
            fixed=sum(act_label(x,g8)==x for x in labels);echar[fixed]+=1
        variants[name]={
          'root_plus_axis_orbit_sizes':eorbs,
          'character_fixedpoint_distribution':dict(sorted(echar.items())),
          'same_orbit_multiset_as_code':eorbs==coord_orbits,
          'same_fixedpoint_character_distribution_as_code':echar==code_char,
        }
    assert not any(v['same_orbit_multiset_as_code'] for v in variants.values())
    assert not any(v['same_fixedpoint_character_distribution_as_code'] for v in variants.values())
    out={
      'schema':'w33.pass7162.e8_outer_character_audit.v1','status':'PASS',
      'code_outer_group':'S3 wr C2','group_order':72,
      'code_coordinate_orbit_sizes_under_parallel_outer_lift':coord_orbits,
      'code_fixedpoint_character_distribution':dict(sorted(code_char.items())),
      'E8_model':'240 standard E8 roots in doubled coordinates plus 8 coordinate-axis labels',
      'natural_extension_variants':variants,
      'conclusion':'REJECTED: none of four natural coordinate-permutation S3 wr C2 extensions makes the code 248-coordinate G-set isomorphic to the E8 240-roots-plus-8-axes G-set.',
      'scope':'This rejects these natural A2^2-style coordinate embeddings only; it is not a theorem that no abstract S3 wr C2 subgroup of W(E8) can reproduce some weaker character coincidence.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
