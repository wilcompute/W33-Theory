#!/usr/bin/env python3
"""Pass 4754 — odd-q distance theorem and involution mod-4 branch.

The proof in PASS4754_oddq_kernel_distance_theorem.md is valid for every odd
prime power q.  This executable companion independently checks q=3,5,7 and
reuses the exact q=5 MILP from Pass 4739.
"""
from __future__ import annotations
import json
from pathlib import Path
from w33_pass4739_w3q_involution_minimum_shell_probe import geometry,gf2_rank,fixed_word,exact_kernel_min
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4754_ODDQ_KERNEL_DISTANCE.json'

def main():
    out={'pass':4754,'cases':{}}
    for q in (3,5,7):
        pts,pidx,lines,lidx,A,J=geometry(q);r=gf2_rank(A)
        J2=np.array([[0,1],[-1,0]],dtype=int)%q
        T=np.block([[J2,np.zeros((2,2),int)],[np.zeros((2,2),int),J2]])%q
        F,ink,skew=fixed_word(q,pts,pidx,lines,lidx,T,A)
        rec={'lines':len(lines),'binary_adjacency_rank':r,'proved_distance_by_general_theorem':q+1,
             'canonical_involution_fixed_lines':len(F),'involution_mask_in_kernel':ink,
             'fixed_lines_pairwise_skew':skew,'q_mod_4':q%4}
        if q in (3,5):
            d,w=exact_kernel_min(A,time_limit=60);assert d==q+1
            rec['independent_exact_MILP_distance']=d;rec['minimum_witness']=list(w)
        out['cases'][str(q)]=rec
    assert out['cases']['3']['canonical_involution_fixed_lines']==4
    assert out['cases']['5']['canonical_involution_fixed_lines']==8
    assert out['cases']['7']['canonical_involution_fixed_lines']==8
    out['theorem']='For every odd prime power q, the binary kernel of the line-intersection adjacency matrix of W(3,q) has minimum distance q+1. Equality words are necessarily q+1 pairwise-skew lines with every outside line meeting the support in 0 or 2 members; an anisotropic-plane conic in the dual Q(4,q) supplies such a word. The canonical projective J-involution fixes q+1 lines for q=3 mod 4 but q+3 lines for q=1 mod 4, so it lies in the minimum shell exactly on the first branch.'
    out['prior_art_boundary']='Related binary line/neighborhood codes of Sp(4,q) and O(5,q) for odd q were studied by Bagchi-Brouwer-Wilbrink (1991). This repository result claims the explicit kernel-distance proof and involution-branch formulation used here; no literature novelty claim is made without a full prior-art comparison.'
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
