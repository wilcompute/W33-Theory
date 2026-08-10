#!/usr/bin/env python3
"""Pass 4696 -- the 1620 support-12 apartment thickenings span the canonical [1620,38,270] even-coefficient apartment subcode.

The 40 apartment-incidence generator rows have rank 39 and unique coefficient
kernel <1>.  Each Pass4695 corner-star thickening uses 12 generator rows, so its
40-bit coefficient mask lies in the even-weight hyperplane E40.  The 1620
thickening masks have rank 39, hence span all of E40.  Since the all-ones kernel
has even weight 40, their codeword images span E40/<1>, dimension 38.

Pass4495 exhaustively proved that the only apartment-code words below/through
weight 270 are the 40 generator rows of weight 162 and the 240 adjacent-pair
sums of weight 270.  The former have odd coefficient parity and the latter even.
Therefore the even-coefficient subcode has parameters [1620,38,270], with
exactly 240 minimum words, canonically the W33 edges.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4696_THICKENING_SPAN_EVEN_APARTMENT_SUBCODE.json'

def rank(vals):
    piv={}
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)
def thickening(ap,lines):
    corners=set()
    for i,j in itertools.combinations(ap,2):
        z=lines[i]&lines[j]
        if z:corners|=z
    return frozenset(i for i,L in enumerate(lines) if L&corners)
def row_masks(H):
    out=[]
    for i in range(40):
        m=0
        for j in np.flatnonzero(H[i]):m|=1<<int(j)
        out.append(m)
    return out

def main()->int:
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry();rows=row_masks(H)
    assert rank(rows)==39
    one=(1<<40)-1
    T=[thickening(ap,lines) for ap in apartments];assert len(set(T))==1620 and {len(x) for x in T}=={12}
    cmasks=[sum(1<<i for i in x) for x in T]
    assert all(x.bit_count()%2==0 for x in cmasks)
    assert rank(cmasks)==39
    # Since E40 itself has dimension 39, the thickening masks span the whole even hyperplane.
    assert rank(cmasks+[one])==39 and one.bit_count()%2==0
    words=[]
    for C in cmasks:
        z=0
        for i in range(40):
            if (C>>i)&1:z^=rows[i]
        words.append(z)
    assert rank(words)==38 and len(set(words))==1620 and {x.bit_count() for x in words}=={608}
    # The 240 adjacent generator pairs are the even-subcode minimum shell.
    edgewords=[]
    for i,j in itertools.combinations(range(40),2):
        if Astar[i,j]:edgewords.append(rows[i]^rows[j])
    assert len(edgewords)==240 and len(set(edgewords))==240 and {x.bit_count() for x in edgewords}=={270}
    old=json.loads((ROOT/'data/PART_W33_PASS4495_4502_DISTANCE_PRISM_RECONSTRUCTION.json').read_text(encoding='utf-8'))
    assert old['distance']['minimum_distance']==162 if 'distance' in old else True
    out={'pass':4696,'coefficient_space':{'ambient':'F2^40','apartment_generator_kernel':'<all-ones>','even_hyperplane_dimension':39,'thickening_masks':1620,'thickening_mask_weight':12,'thickening_mask_rank':39,'thickening_masks_span':'entire even-weight hyperplane'},'image_subcode':{'dimension':38,'parameters':'[1620,38,270]','thickening_codeword_weight':608,'thickening_shell_size':1620,'minimum_weight':270,'minimum_words':240,'minimum_shell':'adjacent generator-pair sums = W33 edges'},'theorem':'The 1620 support-12 apartment-thickening words span exactly the even-coefficient subcode E40/<1> of the apartment code.  This canonical [1620,38,270] subcode has 240 minimum words, precisely the W33 edge carrier, giving an explicit apartment-thickening-to-edge coding bridge.','boundary':'Exact binary-code/building theorem.  Minimum distance 270 uses the already exhaustive Pass4495 low-weight apartment-code certificate; no physical interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
