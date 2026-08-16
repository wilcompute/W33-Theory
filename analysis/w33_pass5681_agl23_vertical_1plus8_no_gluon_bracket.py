#!/usr/bin/env python3
"""Pass5681 bonkers: the vertical bad9 really is 1+8 -- but the 8 is not an SU(3) adjoint.

The nine E6 vertical fibers are the nine points of AG(2,3).  Its full affine group

    AGL(2,3) = F3^2 : GL(2,3),  |G|=9*48=432

is 2-transitive on those sites.  Therefore the nine-point permutation module splits
as

    C^9 = 1 + V_8

with the augmentation module V_8 irreducible over C.

The dimension eight tempts an SU(3)-adjoint / eight-gluon reading.  This pass tests the
actual representation structure instead of the count.  If V_8 were to carry a Lie
algebra structure compatible with the full affine symmetry, there must be a nonzero
G-equivariant alternating bracket

    Lambda^2 V_8 -> V_8.

Character theory gives its multiplicity exactly zero.

There is also an exact graph-cochain interpretation.  Oriented edges of the complete
nine-site 1-skeleton form Lambda^2 C^9 (dimension 36).  The incidence boundary has
rank eight and cycle space dimension 28.  Since C^9=1+V_8,

    Lambda^2 C^9 = V_8 + Lambda^2 V_8,

and the boundary is the V_8 summand, leaving

    Z_1(K9) ~= Lambda^2 V_8,  dim=28.

So the 1+8+28 gauge-complex pattern is genuine.  The eight modes are local affine
site/gauge-parameter modes; the absence of an equivariant alternating 8x8->8 bracket
rules out identifying them with the su(3) adjoint while retaining the full AGL(2,3)
symmetry.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5681_AGL23_VERTICAL_1PLUS8_NO_GLUON_BRACKET.json'
Q=3


def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))


def agl_permutations():
    pts=[(x,y) for x in range(Q) for y in range(Q)]; idx={p:i for i,p in enumerate(pts)}
    GL=[]
    for a,b,c,d in itertools.product(range(Q),repeat=4):
        if (a*d-b*c)%Q:
            GL.append((a,b,c,d))
    assert len(GL)==48
    perms=[]
    for a,b,c,d in GL:
        for tx,ty in pts:
            p=[]
            for x,y in pts:
                u=(a*x+b*y+tx)%Q;v=(c*x+d*y+ty)%Q
                p.append(idx[(u,v)])
            perms.append(tuple(p))
    perms=sorted(set(perms));assert len(perms)==432
    return pts,perms


def main():
    pts,G=agl_permutations()
    chi=[];chi2=[]
    for g in G:
        fixed=sum(i==g[i] for i in range(9))
        g2=compose(g,g); fixed2=sum(i==g2[i] for i in range(9))
        chi.append(fixed-1);chi2.append(fixed2-1)
    chi=np.array(chi,dtype=int);chi2=np.array(chi2,dtype=int)
    assert int(np.dot(chi,chi))==432 # irreducible augmentation module
    wedge=(chi*chi-chi2)//2
    sym=(chi*chi+chi2)//2
    bracket_num=int(np.dot(wedge,chi));sym_num=int(np.dot(sym,chi))
    assert bracket_num==0
    assert sym_num==2*432

    # Oriented edge boundary of K9.
    ed=list(itertools.combinations(range(9),2));assert len(ed)==36
    D=np.zeros((9,36),dtype=int)
    for j,(u,v) in enumerate(ed):D[u,j]=-1;D[v,j]=1
    rank=int(np.linalg.matrix_rank(D));assert rank==8
    cycle=36-rank;assert cycle==28==8*7//2

    # 2-transitivity check: one orbit on ordered distinct site pairs.
    pairs=[(i,j) for i in range(9) for j in range(9) if i!=j]
    seed=pairs[0]
    orb={(g[seed[0]],g[seed[1]]) for g in G}
    assert len(orb)==72==len(pairs)

    out={
      'pass':5681,
      'status':'VERTICAL_BAD9_IS_1_PLUS_IRREDUCIBLE8_BUT_FULL_AFFINE_SYMMETRY_FORBIDS_AN_SU3_LIE_BRACKET',
      'group':{'name':'AGL(2,3)','order':432,'site_action':'2-transitive on 9 AG(2,3) points'},
      'site_module':'C^9 = 1 + V8',
      'V8':{'dimension':8,'irreducible':True,'character_histogram':{str(k):v for k,v in sorted(Counter(chi).items())}},
      'cochain_complex':{
        'oriented_edges_dim':36,
        'incidence_rank':8,
        'cycle_space_dim':28,
        'representation_identity':'Lambda^2(C^9)=V8 + Lambda^2(V8), with Z1(K9) ~= Lambda^2(V8)'
      },
      'alternating_bracket_test':{
        'multiplicity_of_V8_in_Lambda2_V8':0,
        'Hom_G(Lambda2 V8,V8)_dimension':0,
        'consequence':'no nonzero AGL(2,3)-equivariant antisymmetric bilinear bracket V8 x V8 -> V8'
      },
      'symmetric_comparison':{'multiplicity_of_V8_in_Sym2_V8':2},
      'physics_conclusion':'The 8 is a real structural augmentation/gauge-parameter sector, and 28 is its exterior-square cycle sector. The dimension-eight match to the SU(3) adjoint fails the required Lie-bracket test under the full affine symmetry.',
      'physics_boundary':'Breaking AGL(2,3) to a smaller group could change the Hom space; this pass rules out only the symmetry-preserving eight-gluon identification and does not derive a Yang-Mills gauge group.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
