#!/usr/bin/env python3
"""Pass5319: natural W(D4)/Z action on tesseract square-face pairs is tomotope96.

A tesseract has 24 square 2-faces.  Pair each face with its antipode, leaving 12
antipodal square-face pairs.  The even-sign signed-permutation group D=W(D4)
of order192 acts on these 12 objects; its central antipode -I is exactly the
kernel, so the induced action has order96.

This pass gives an explicit 12-point relabeling under which that natural action
is exactly the published Monson--Pellicer--Williams tomotope permutation group.
Thus Pass5309's Hoffman quotient acquires a concrete D4/tesseract realization:

    W(D4)/<-I> acting on 12 antipodal square-face pairs ~= Gamma(T).

The orientation-preserving tesseract group is a different order192 cover and is
kept separate (Pass5310/5320).
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup

from analysis.w33_pass5310_tesseract_rotation_d4_tomotope_doublecovers import signed_groups,cp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5319_D4_TESSERACT_FACEPAIRS_TOMOTOPE_ACTION.json'
CONJ=(0,1,4,5,8,9,11,10,7,6,3,2) # natural face-pair label -> published tomotope label

def key(g,n):return tuple(g(i) for i in range(n))
def gset(G,n):return {key(g,n) for g in G.generate_schreier_sims()}

def build_face_pairs(V,vi):
    faces=[];meta=[]
    for fixed in itertools.combinations(range(4),2):
      for signs in itertools.product((-1,1),repeat=2):
        F=frozenset(i for i,x in enumerate(V) if all(x[fixed[j]]==signs[j] for j in range(2)))
        assert len(F)==4;faces.append(F);meta.append((fixed,signs))
    assert len(set(faces))==24
    fi={F:i for i,F in enumerate(faces)}
    def anti_face(i):
        A=frozenset(vi[tuple(-a for a in V[v])] for v in faces[i]);return fi[A]
    pairs=[];seen=set();labels=[]
    for i in range(24):
        if i in seen:continue
        j=anti_face(i);assert meta[i][0]==meta[j][0]
        pairs.append(tuple(sorted((i,j))));seen|={i,j}
        labels.append({'fixed_coordinates':list(meta[i][0]),'sign_class':[list(meta[i][1]),list(meta[j][1])]})
    assert len(pairs)==12
    return faces,pairs,labels

def induced(G,faces,pairs):
    fi={F:i for i,F in enumerate(faces)};pi={p:i for i,p in enumerate(pairs)}
    def fimg(g,i):return fi[frozenset(g(v) for v in faces[i])]
    def pimg(g,p):
        a,b=p;return pi[tuple(sorted((fimg(g,a),fimg(g,b))))]
    return PermutationGroup([Permutation([pimg(g,p) for p in pairs]) for g in G.generators])

def published_tomotope():
    return PermutationGroup([
      cp([(5,10),(6,9),(7,12),(8,11)]),cp([(1,6),(2,5),(3,8),(4,7)]),
      cp([(5,9),(6,10),(7,11),(8,12)]),cp([(5,8),(6,7),(9,12),(10,11)])])

def conjugate_group(G,p):
    n=len(p);pinv=[0]*n
    for i,j in enumerate(p):pinv[j]=i
    gens=[]
    for g in G.generators:
        gens.append(Permutation([p[g(pinv[y])] for y in range(n)]))
    return PermutationGroup(gens)

def main():
    V,vi,B,R,D=signed_groups();assert D.order()==192 and D.center().order()==2
    faces,pairs,labels=build_face_pairs(V,vi)
    D12=induced(D,faces,pairs);assert D12.order()==96 and sorted(map(len,D12.orbits()))==[12]
    T=published_tomotope();assert T.order()==96
    C=conjugate_group(D12,CONJ)
    assert gset(C,12)==gset(T,12)

    # Kernel of D -> D12 is exactly the central antipodal involution.
    ker=[g for g in D.generate_schreier_sims() if all(
        tuple(sorted((
          next(i for i,F in enumerate(faces) if F==frozenset(g(v) for v in faces[a])),
          next(i for i,F in enumerate(faces) if F==frozenset(g(v) for v in faces[b]))
        )))==pairs[k] for k,(a,b) in enumerate(pairs))]
    assert len(ker)==2

    out={'pass':5319,'status':'THEOREM_WD4_ANTIPODAL_SQUARE_FACE_PAIR_ACTION_IS_PUBLISHED_TOMOTOPE96',
      'tesseract_square_faces':24,'antipodal_square_face_pairs':12,
      'WD4_order':192,'WD4_center_order':2,'induced_action_order':96,
      'action_kernel':'central antipode -I','published_tomotope_order':96,
      'explicit_degree12_conjugator':list(CONJ),
      'pair_labels':labels,
      'statement':'After the displayed relabeling, W(D4)/<-I> acting on the 12 antipodal square-face pairs is exactly the published tomotope degree-12 permutation group.',
      'bridge':'This geometrizes Pass5309: the Hoffman W(D4) quotient and the natural D4 square-face-pair quotient realize the same tomotope action.',
      'boundary':'The orientation-preserving tesseract rotation group is not W(D4), despite also having order192; its natural 12-object action is treated separately in Pass5320.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
