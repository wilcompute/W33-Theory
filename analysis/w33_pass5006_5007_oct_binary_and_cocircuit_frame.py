#!/usr/bin/env python3
"""Pass5006/5007: the binary octahedron frame projects 90->30 with a
60-kernel, and the 240 minimum six-line reader failures form a tight frame for
the complete 24-dimensional line-reader nullspace.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4992_4999_common import build_base,gf2_rank_int,gf2_rank_matrix

O6=ROOT/'data/PART_W33_PASS5006_OCTAHEDRON_BINARY_60_90_30_EXTENSION.json'
O7=ROOT/'data/PART_W33_PASS5007_MINIMUM_COCIRCUIT_24_TIGHT_FRAME.json'

def main()->int:
    b=build_base();E=b['E'];spreads=b['spreads'];iso=b['iso_ds_sp'];res=b['residual'];Q=b['Q'];pair_items=sorted(b['pair_to_res'].items())
    # --------------------------------------------------------------- Pass5006
    edge_line=[]
    for a,c in E:
        z=spreads[iso[a]]&spreads[iso[c]];assert len(z)==1;edge_line.append(next(iter(z)))
    def project(mask):
        y=0;x=int(mask)
        while x:
            lb=x&-x;k=lb.bit_length()-1;y^=1<<edge_line[k];x^=lb
        return y
    O=np.zeros((270,360),dtype=np.uint8);imgs=[]
    for r,(bp,items) in enumerate(pair_items):
        m=0
        for q,V in items:m^=q
        x=m
        while x:
            lb=x&-x;O[r,lb.bit_length()-1]=1;x^=lb
        imgs.append(project(m))
    assert gf2_rank_matrix(O)==90 and len(set(imgs))==270 and {x.bit_count() for x in imgs}=={4}
    rimg=gf2_rank_int(imgs);assert rimg==30
    sqimg=gf2_rank_int(project(m) for m,V in res);assert sqimg==30
    AQ=nx.to_numpy_array(Q,nodelist=range(40),dtype=np.uint8);assert gf2_rank_matrix(AQ)==10
    for x in imgs:
        v=np.array([(x>>i)&1 for i in range(40)],dtype=np.uint8);assert not np.any((AQ@v)%2)
    out6={
      'pass':5006,'binary_oct_frame':{'shape':[270,360],'rank':90},
      'shared_line_projection':{'distinct_row_images':270,'image_weight':4,'image_rank':30,
        'image':'exactly the residual-square image = Q43 adjacency-code orthogonal complement'},
      'kernel_dimension':60,'exact_sequence':'0 -> K60 -> O90 -> C_Q43^perp(30) -> 0 over F2',
      'theorem':'Reducing the 270-octahedron edge frame modulo two gives a 90-dimensional code. The canonical shared-line projection maps it onto the 30-dimensional orthogonal complement of the Q(4,3) adjacency code, with exact kernel dimension60. Every octahedron maps to one of the 270 overlap-four spread intersections, so the modular rank90 admits a literal 60->90->30 geometric resolution rather than a dimension-only analogy.',
      'boundary':'No identification of the 60-kernel with an unrelated real carrier is made here.'}
    O6.write_text(json.dumps(out6,indent=2,sort_keys=True)+'\n')

    # --------------------------------------------------------------- Pass5007
    L=b['L'];W=b['W'];C=b['C'].astype(int)
    Z=np.zeros((40,40),dtype=int)
    for j,Lj in enumerate(L):
        for p in Lj:Z[p,j]=1
    edges=sorted(tuple(sorted(e)) for e in W.edges());assert len(edges)==240
    D=np.zeros((240,40),dtype=int)
    for r,(p,q) in enumerate(edges):D[r]=Z[p]-Z[q]
    assert np.linalg.matrix_rank(D)==24 and np.max(np.abs(D@C.T))==0
    S=D.T@D;eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh(S.astype(float)))
    assert eigs==Counter({0:16,60:24})
    supports={frozenset(np.flatnonzero(row)) for row in D};assert len(supports)==240 and {len(s) for s in supports}=={6}
    assert 40-np.linalg.matrix_rank(C.T)==24
    out7={
      'pass':5007,'indexing':'240 W33 point-graph edges / collinear point pairs',
      'signed_cocircuit_matrix':'D_(p,q)=point-pencil(p)-point-pencil(q), shape240x40',
      'support_size':6,'distinct_supports':240,'rank':24,'annihilates_raw_line_reader':True,
      'line_reader_left_nullity':24,'spans_entire_left_nullspace':True,
      'frame_operator_spectrum':{'60':24,'0':16},'parseval_scaling':'1/sqrt(60)',
      'theorem':'The 240 global minimum six-line cocircuits are canonically indexed by the 240 edges of the W33 point graph. With the natural pencil-difference signs they span the entire 24-dimensional left nullspace of the 40-line reader and form an equal-norm tight frame with D^T D eigenvalues 60^24 and 0^16. Thus the minimum line-sensor failure modes are themselves a W33 edge-gradient realization of the full 24-dimensional reader-null sector.',
      'boundary':'The 24-dimensional nullspace statement concerns sensor-coefficient relations of the line reader; it is not automatically a physical gauge-field identification.'}
    O7.write_text(json.dumps(out7,indent=2,sort_keys=True)+'\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
