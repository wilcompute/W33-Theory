#!/usr/bin/env python3
"""Pass5188: q=5 P components are exactly the minimum words of C(W)^perp.

Let N be the 156x156 point-line incidence matrix of W(3,5), and let C be its
binary line code (column span of N in point coordinates).  Pass5130 proves
rank_2(N)=91, so dim C^perp=65.

Pass5187 identifies the 325 P components with the 325 dual grids H union H^perp.
Every W line meets every dual grid in 0 or 2 points, hence each dual-grid vector
lies in ker(N^T)=C^perp.  This producer rebuilds the q=5 geometry and proves that
the 156x325 point/dual-grid incidence matrix B has rank_2 65.  Therefore

    im_F2(B) = ker_F2(N^T) = C^perp.

The minimum distance is 12 and the minimum shell is exactly the 325 dual grids.
A short intrinsic lower bound works for any W(3,q): if a nonzero point set S has
even intersection with every W line, choose p in S.  Each of the q+1 lines
through p forces a second S-point.  Choose one such neighbour x; each of the q
other lines through x forces a further point, all new by the generalized-
quadrangle girth property.  Hence |S|>=2(q+1).

At equality every selected point has selected degree exactly q+1 and every W
line contains 0 or 2 selected points.  The selected point graph is therefore
(q+1)-regular, triangle-free, on 2(q+1) vertices.  Mantel equality forces
K_{q+1,q+1}.  In W(3,q) its two independent sides are the hyperbolic line
{p,r}^{perp perp} and its polar, so the support is a dual grid.  At q=5 these
are precisely the 325 P-component carriers from Pass5187.
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5180_p_tensor_atom_line_panel_reduction import p_components

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5188_Q5_DUAL_GRID_CODE_EXACT.json'


def rank_bits(rows):
    piv={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in piv:r^=piv[p]
            else:piv[p]=r;break
    return len(piv)


def main():
    q=5;G=build_W(q);comps,apt_comp=p_components(G)
    assert len(G['pts'])==len(G['lines'])==156 and len(comps)==325

    # Point -> P-component footprints; these are the rows of B.
    foot=[set() for _ in G['flags']]
    for a,es in enumerate(G['apt_edges']):
        c=apt_comp[a]
        for f in es:foot[f].add(c)
    point_flags=defaultdict(list)
    for f,(p,l) in enumerate(G['flags']):point_flags[p].append(f)
    point_foot={}
    for p,fs in point_flags.items():
        vals={frozenset(foot[f]) for f in fs};assert len(vals)==1
        point_foot[p]=next(iter(vals))
    B_rows=[]
    for p in range(156):
        z=0
        for c in point_foot[p]:z|=1<<c
        B_rows.append(z)
    rankB=rank_bits(B_rows);assert rankB==65

    # Ordinary point-line incidence N, represented by point rows in line coords.
    N_rows=[]
    for p in range(156):
        z=0
        for l,L in enumerate(G['lines']):
            if p in L:z|=1<<l
        N_rows.append(z)
    rankN=rank_bits(N_rows);assert rankN==91
    assert rankB+rankN==156

    # Component block point masks and exact binary orthogonality N^T B=0.
    block_points=[set() for _ in comps]
    for p,S in point_foot.items():
        for c in S:block_points[c].add(p)
    assert {len(B) for B in block_points}=={12}
    intersection_hist={}
    for B in block_points:
        for L in G['lines']:
            z=len(B&set(L));intersection_hist[z]=intersection_hist.get(z,0)+1
            assert z in (0,2)
    assert intersection_hist=={0:39000,2:11700}

    # The 325 block masks are distinct, all weight 12, and span the 65D kernel.
    block_masks=[]
    for B in block_points:
        z=0
        for p in B:z|=1<<p
        block_masks.append(z)
    assert len(set(block_masks))==325 and {z.bit_count() for z in block_masks}=={12}
    assert rank_bits(block_masks)==65

    out={
      'pass':5188,
      'status':'THEOREM_Q5_DUAL_GRID_CODE_EQUALS_BINARY_INCIDENCE_DUAL',
      'q':5,
      'point_line_incidence':{'shape':[156,156],'rank_F2':rankN,'line_code_dimension':rankN,'dual_dimension':156-rankN},
      'P_component_incidence':{'shape':[156,325],'rank_F2':rankB,'dual_grid_columns':325,'column_weight':12},
      'orthogonality':'N^T B=0 over F2; every W line meets every P-component dual grid in 0 or 2 points.',
      'equality':'im_F2(B)=ker_F2(N^T)=C(W)^perp by inclusion and the common dimension 65.',
      'code_parameters':'[156,65,12]_2',
      'minimum_distance_proof':'Any nonzero even-on-every-W-line point set has at least 2(q+1)=12 points by the two-step GQ forcing argument.',
      'minimum_shell':'Equality forces a 6-regular triangle-free graph on 12 selected points, hence K_6,6; in W(3,5) this is a hyperbolic polar-pair dual grid. Thus A_12=325 and the minimum words are exactly the 325 P-component carriers.',
      'line_intersection_histogram':{str(k):v for k,v in sorted(intersection_hist.items())},
      'bicycle_connection':'Pass5130 gives the q=5 Levi binary bicycle dimension 129=2*65-1. The P-component dual-grid code materializes one canonical 65-dimensional incidence-dual half of that bicycle construction.',
      'boundary':'Exact q=5 binary code theorem. No all-odd-q spanning claim is made, and this does not by itself classify the 25-atom apartment-code equality shell.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
