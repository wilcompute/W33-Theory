#!/usr/bin/env python3
"""Local 165-carrier inside the Suzuki/Leech W33 incidence tower.

Starting from the already certified 32760-point 2.Suz tight orbit and the
135135 orbit of full 40-point symplectic 4-spaces, fix a tight point p.  The
165 full W33 4-spaces through p form the classical U5(2) rank-three graph:

    SRG(165,36,3,9) = point graph of GQ(4,8).

Adjacency is intrinsic in the 12-dimensional F3 model: two 4-spaces through p
are adjacent iff their vector-space intersection has dimension 2.  Relative to
one base W33 U, its 36 neighbors group as 9 x 4 according to the nine
NON-isotropic projective lines through p in PG(U)=PG(3,3); the four isotropic
lines through p are the W(3,3) lines and do not occur as intersection lines.

The adjacency spectrum is 36^1, 3^120, (-9)^44.  Thus the 165-dimensional
permutation module splits as 1 + 44 + 120 = 45 + 120.  The repository already
has 45 cubic tritangent planes and 120 Steiner triangles in the local E6
27-36-45 carrier.  This file records the exact dimension match but deliberately
does NOT assert an equivariant identification of those old carriers with these
U5(2) eigenspaces until an intertwiner is constructed.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_suzuki_local_165_gq48_spectral_bridge.json'

def load_tower():
    p=ROOT/'analysis'/'w33_suzuki_w33_e6_incidence_tower.py'
    s=importlib.util.spec_from_file_location('suztower',p)
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def srg_params(A):
    n=len(A); deg=A.sum(1); assert len(set(map(int,deg)))==1; k=int(deg[0])
    la=set(); mu=set()
    for i in range(n):
        for j in range(i+1,n):
            z=int(np.logical_and(A[i],A[j]).sum())
            (la if A[i,j] else mu).add(z)
    assert len(la)==len(mu)==1
    return n,k,next(iter(la)),next(iter(mu))


def main(write=True):
    t=load_tower()
    A=t.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m1')
    B=t.parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m2')
    orb=t.subspace_orbit(t.U1,[A,B]); assert len(orb)==135135
    P=sorted(t.projective_points(t.U1)); p=np.array(P[0],dtype=np.int64)
    through=[]
    for U in orb.values():
        if t.rankp(np.vstack([U,p]))==4: through.append(U)
    assert len(through)==165

    G=np.zeros((165,165),dtype=bool)
    for i,j in itertools.combinations(range(165),2):
        d=t.intersection_dim(through[i],through[j])
        assert d in (1,2,4)
        if d==2:G[i,j]=G[j,i]=True
    assert srg_params(G)==(165,36,3,9)

    # Find the base U1 inside the 165 and resolve its 36 neighbors into the
    # projective intersection lines through p.
    ku=t.rref_key(t.U1); ibase=next(i for i,U in enumerate(through) if t.rref_key(U)==ku)
    line_counts=Counter(); line_iso={}
    Upts=t.projective_points(t.U1)
    for j in np.flatnonzero(G[ibase]):
        V=through[int(j)]; I=tuple(sorted(Upts & t.projective_points(V)))
        assert len(I)==4
        line_counts[I]+=1
        x=np.array(I[0],dtype=np.int64)
        y=next(np.array(q,dtype=np.int64) for q in I[1:] if t.rankp(np.vstack([x,q]))==2)
        line_iso[I]=int((x@t.J@y.T)%3)==0
    assert len(line_counts)==9 and set(line_counts.values())=={4}
    assert not any(line_iso.values())

    # In a 4D symplectic space there are 13 projective lines through a point:
    # q+1=4 isotropic W33 lines and q^2=9 non-isotropic lines.
    assert 9*4==36

    # Exact spectrum from the SRG quadratic x^2-(lambda-mu)x-(k-mu)=0.
    # x^2+6x-27=(x-3)(x+9), and trace/dimension determine multiplicities.
    spectrum={'36':1,'3':120,'-9':44}
    assert 1+120+44==165 and 1+44==45

    out={
      'schema':'w33.suzuki_local_165_gq48_spectral_bridge.v1','status':'PASS',
      'headline':'The 165 full Suzuki/Leech W33 4-spaces through a fixed tight-set point form SRG(165,36,3,9), the U5(2) polar graph / point graph of GQ(4,8). Its spectrum is 36^1 + 3^120 + (-9)^44, hence the permutation module splits as (1+44)+120 = 45+120.',
      'construction':{'vertices':165,'adjacency':'intersection vector dimension 2','srg':[165,36,3,9]},
      'local_neighborhood':{'neighbors':36,'intersection_lines_through_base_point':9,'neighbors_per_intersection_line':4,'all_nine_intersection_lines_nonisotropic':True,'W33_isotropic_lines_through_point':4},
      'spectrum':spectrum,
      'module_dimensions':{'trivial_plus_minus9':45,'plus3':120,'identity':'165=1+44+120=45+120'},
      'external_identification':'Classical rank-3 U5(2) graph; point graph of GQ(4,8). ATLAS degree-165 representation has suborbit lengths 1,36,128.',
      'repo_crosscheck':{'cubic_tritangents':45,'Steiner_triangles':120,'sources':['analysis/w33_pass4659_internal_e6_27_36_45_triangle.py','analysis/w33_pass4964_4965_4967_double_six_spread_transceiver.py']},
      'boundary':'The equality 45+120 with the old tritangent/Steiner carrier sizes is exact and representation-theoretically suggestive, but this certificate does not claim an equivariant identification. A concrete intertwiner or common group action is still required.',
      'checks':{'orbit_135135':True,'through_point_165':True,'srg_165_36_3_9':True,'nine_by_four_local_chart':True,'spectrum_multiplicities':True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
