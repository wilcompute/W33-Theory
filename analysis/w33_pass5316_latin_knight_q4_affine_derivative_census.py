#!/usr/bin/env python3
"""Pass5316: affine-derivative fingerprint of all 576 order-4 Latin squares.

Use the *explicit* toroidal-knight -> Q4 labeling frozen in
w33_self_entangled_qutrit_q4_router.py.  Pull every order-4 Latin square back to
F2^4 and encode its four symbols as F2^2.  For each Q4 bit direction d, compute
the symbol derivative

    Delta_d L(x) = L(x+e_d) + L(x)  in F2^2.

The Klein/V4 isotopy class is characterized exactly by all four derivatives
being constant, equivalently by L:F2^4->F2^2 being affine.  The cyclic/C4 class
is never affine: 192 squares have exactly one constant Q4 derivative (48 for
each bit direction) and 240 have none.

This refines Pass5311's same-symbol knight-edge census without identifying any
cardinality with a symmetry group.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

from analysis.w33_pass5311_order4_latin_toroidal_q4_census import (
    all_latin, flat, intercalates, knight_edges,
)
from analysis.w33_self_entangled_qutrit_q4_router import KNIGHT_TO_Q4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5316_LATIN_KNIGHT_Q4_AFFINE_DERIVATIVE_CENSUS.json'

BITS_TO_CELL={bits:cell for cell,bits in KNIGHT_TO_Q4.items()}
assert len(BITS_TO_CELL)==16

def derivative_values(sq,dim):
    vals=[];seen=set()
    for bits,cell in BITS_TO_CELL.items():
        nb=list(bits);nb[dim]^=1;nb=tuple(nb)
        edge=tuple(sorted((bits,nb)))
        if edge in seen:continue
        seen.add(edge)
        r,c=cell;r2,c2=BITS_TO_CELL[nb]
        vals.append(sq[r][c]^sq[r2][c2])
    assert len(vals)==8
    return tuple(vals)

def constant_mask(sq):
    m=0
    for d in range(4):
        v=derivative_values(sq,d)
        if len(set(v))==1:m|=1<<d
    return m

def same_symbol_knight_edges(sq):
    s=flat(sq)
    return sum(s[a]==s[b] for a,b in knight_edges())

def affine_certificate(sq):
    # Coordinates are ordered exactly as KNIGHT_TO_Q4 bits.  In characteristic
    # two an F2^2-valued function is affine iff its four first derivatives are
    # constant.  Reconstruct it from the origin and the four derivative columns.
    origin=(0,0,0,0);r0,c0=BITS_TO_CELL[origin];b=sq[r0][c0]
    cols=[]
    for d in range(4):
        v=derivative_values(sq,d)
        if len(set(v))!=1:return False,None
        cols.append(v[0])
    for bits,cell in BITS_TO_CELL.items():
        y=b
        for d,bit in enumerate(bits):
            if bit:y^=cols[d]
        r,c=cell
        if y!=sq[r][c]:return False,None
    return True,tuple(cols)

def main():
    L=all_latin();assert len(L)==576
    detailed=Counter()
    affine_cols=Counter()
    for sq in L:
        mask=constant_mask(sq);cc=mask.bit_count();ic=intercalates(sq);same=same_symbol_knight_edges(sq)
        ok,cols=affine_certificate(sq)
        assert ok==(cc==4)
        if ok:affine_cols[cols]+=1
        detailed[(ic,same,cc,mask)]+=1

    want=Counter({
      (4,8,0,0):192,
      (12,16,4,15):96,
      (12,0,4,15):48,
      (4,0,0,0):48,
      (4,16,1,1):48,
      (4,16,1,2):48,
      (4,16,1,4):48,
      (4,16,1,8):48,
    })
    assert detailed==want
    assert sum(n for (ic,_,cc,_),n in detailed.items() if ic==12 and cc==4)==144
    assert sum(n for (ic,_,cc,_),n in detailed.items() if ic==4 and cc==1)==192
    assert sum(n for (ic,_,cc,_),n in detailed.items() if ic==4 and cc==0)==240
    assert len(affine_cols)>0 and sum(affine_cols.values())==144

    out={
      'pass':5316,
      'status':'THEOREM_KLEIN144_EXACTLY_AFFINE_Q4_COLORINGS_CYCLIC432_DERIVATIVE_DEFECT',
      'latin_squares':576,
      'explicit_q4_labeling':'analysis/w33_self_entangled_qutrit_q4_router.py::KNIGHT_TO_Q4',
      'symbol_field':'F2^2 via labels 0,1,2,3 and xor',
      'klein_V4_class':{
        'count':144,'intercalates':12,'constant_q4_derivatives':4,'mask':15,
        'characterization':'exactly the Latin squares whose pulled-back symbol map F2^4 -> F2^2 is affine'},
      'cyclic_C4_class':{
        'count':432,'intercalates':4,
        'constant_derivative_split':{'0':240,'1':192},
        'one_constant_direction_masks':{'1':48,'2':48,'4':48,'8':48},
        'no_cases_with_2_or_3_constant_directions':True},
      'joint_refinement':{str(k):v for k,v in sorted(detailed.items())},
      'relation_to_pass5311':'The five Pass5311 common grid/Q4 orbits are refined by affine derivative data: the two V4 orbits are affine; the C4 orbits have derivative defect 3 or 4.',
      'boundary':'This is a finite coloring/code theorem for the fixed published knight-to-Q4 labeling. Counts 144,192,240 are not assigned physical meaning.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
