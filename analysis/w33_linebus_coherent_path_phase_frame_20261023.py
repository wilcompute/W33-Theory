#!/usr/bin/env python3
"""Coherent route-phase witness for the W33 four-bus XOR2 photonic compiler.

A cross-state MZI contributes i per activated butterfly stage, so a
logical edge gets scalar i^weight(port_a xor port_b) under the frozen
line-local ordering. This is a computational route-phase frame, NOT an
invariant physical U(1) gauge connection: reciprocal traversal applies the
same symmetric optical phase rather than an inverse phase.
"""
from __future__ import annotations
import collections,hashlib,json
from pathlib import Path
from itertools import combinations
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import (
    N,ADJ,LINES,EDGE_LINE,permutation_matrix
)

def transport(u,v):
    if u==v or v not in ADJ[u]:raise ValueError('requires adjacent distinct W33 points')
    line=LINES[EDGE_LINE[tuple(sorted((u,v)))]]
    pu,pv=line.index(u),line.index(v)
    mask=pu^pv
    return {'u':u,'v':v,'line':EDGE_LINE[tuple(sorted((u,v)))],
            'mask':mask,'scalar_i_exponent_mod4':mask.bit_count()}

def route_frame(route):
    path=tuple(route)
    if len(path)<2:raise ValueError('at least one optical edge required')
    e=sum(transport(a,b)['scalar_i_exponent_mod4'] for a,b in zip(path,path[1:]))%4
    return e

def one_bus_projective_cocycle():
    """Scalar defect U_a U_b vs U_(a xor b), all in {+1,-1}."""
    items=[]
    for a in range(4):
        for b in range(4):
            lhs=((1j)**a.bit_count())*((1j)**b.bit_count())
            rhs=(1j)**(a^b).bit_count()
            ratio=lhs/rhs
            predicted=(-1)**((a&b).bit_count())
            assert abs(ratio-predicted)<1e-13
            items.append({'a':a,'b':b,'sign':predicted})
    return items

def enumerate_cycle_witnesses():
    # Full W33 triangle census: every triangle is a 4-point-line subset.
    triangles=[]
    for a in range(N):
        for b in ADJ[a]:
            if a>=b:continue
            for c in ADJ[b]:
                if b<c and c in ADJ[a]:
                    triangles.append((a,b,c))
    assert len(triangles)==160
    tri=collections.Counter(route_frame((a,b,c,a)) for a,b,c in triangles)

    # For every nonedge a-b the generalized quadrangle has four common
    # neighbors and therefore multiple length-2 coherent alternatives.
    comparisons=collections.Counter()
    exemplar=None
    nonedges=0
    for a,b in combinations(range(N),2):
        if b in ADJ[a]:continue
        nonedges+=1
        mids=sorted(set(ADJ[a])&set(ADJ[b]))
        assert len(mids)==4
        for m,n in combinations(mids,2):
            ra=(a,m,b);rb=(a,n,b)
            ea,eb=route_frame(ra),route_frame(rb)
            # Relative phase exponent of path A compared to path B.
            delta=(ea-eb)%4
            comparisons[delta]+=1
            if exemplar is None and delta not in (0,):
                exemplar={'endpoints':[a,b],
                    'path_a':list(ra),'phase_exp_a':ea,
                    'path_b':list(rb),'phase_exp_b':eb,
                    'relative_phase_exp_mod4':delta,
                    'relative_complex_amplitude':[int(round((1j**delta).real)),
                                                 int(round((1j**delta).imag))]}
    assert nonedges==540
    assert sum(comparisons.values())==540*6
    return {'nonadjacent_pairs':nonedges,
      'length2_path_comparisons':sum(comparisons.values()),
      'two_path_relative_i_exponent_histogram':dict(sorted(comparisons.items())),
      'triangle_count':len(triangles),'triangle_scalar_i_exponent_histogram':dict(sorted(tri.items())),
      'distinct_interfering_route_witness':exemplar}

def run():
    summary=enumerate_cycle_witnesses()
    summary['projective_cocycle']=one_bus_projective_cocycle()
    summary['schema']='w33.fractal.linebus.coherent_path_phase_frame.v1'
    summary['phase_frame_correction']='For a routed coherent path with exponent e, multiply by i^(-e); requires optical reference or physically implemented correction if paths interfere'
    summary['assumptions']=['Ideal MZI phase gauge, two-bit XOR switch, fixed local port ordering',
       'Optical reciprocal reverse edge has SAME scalar, not inverse: this is not a U(1) connection',
       'Off-chip fiber path length, dispersion, frequency, source phase and device variation ignored',
       'An untracked relative optical phase can corrupt path-encoded quantum interference',
       'Cocycle is a coboundary of chosen scalar phase convention; no nontrivial topological invariant asserted']
    canonical=json.dumps(summary,sort_keys=True,separators=(',',':'))
    summary['sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    return summary

if __name__=='__main__':
    report=run()
    p=ROOT/'data/w33_linebus_coherent_path_phase_frame_20261023.json'
    p.parent.mkdir(exist_ok=True,parents=True)
    p.write_text(json.dumps(report,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
    print('PASS',report['two_path_relative_i_exponent_histogram'],
        'triangles',report['triangle_scalar_i_exponent_histogram'],
        'witness',report['distinct_interfering_route_witness'],'sha',report['sha256'])
