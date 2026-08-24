#!/usr/bin/env python3
"""Pass10337-10344: exact no-go for identifying Witting 12+12 Clifford classes with the W33 Hermitian 12+12 norm orbits.

Prior exact results:
* Pass2835: 36 Witting magic rays plus four coordinate axes have orthogonality
  graph W(3,3); M36 is W33 minus one line.
* Pass2797/2830: the 36 rays split into two-qubit Clifford classes 4|8|12|12.
* Pass10105: the chamber-selected Hermitian complex structure splits W33 points
  as 16|12|12 (norm 0|1|2).

The matching sizes tempt an identification of the two 12-ray classes with the
two nonzero Hermitian norm orbits.  This pass tests the stronger statement that
ANY union of the natural Witting/axis blocks can be carried to the Hermitian
16|12|12 partition by a W33 graph automorphism.

There are five atomic blocks of sizes 4 (axes), 4, 8, 12, 12.  Exhausting all
assignments of whole atomic blocks to bins of sizes 16,12,12 gives 10 labelled
possibilities.  Every one is equitable and has colored quotient-degree matrix

   [6 3 3]
   [4 5 3]
   [4 3 5]

(up to swapping the two size-12 bins).

The Hermitian norm partition has

   [6 3 3]
   [4 2 6]
   [4 6 2].

Colored quotient degrees are graph-isomorphism invariants, so NO such W33
automorphism exists.  In particular the Witting 12+12 middle split is not the
Hermitian norm 12+12 split.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass2830_2832_class_separation_yield_three_copy import build_rays,clifford_classes
OUT=ROOT/'data/PART_W33_PASS10337_10344_WITTING_UNITARY_PARTITION_NO_GO.json'
P=3

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def quotient_signature(A,groups):
    rows=[]
    for G in groups:
        c=Counter(tuple(int(sum(A[i,j] for j in H)) for H in groups) for i in G)
        rows.append(c)
    return rows

def single_matrix(sig):
    assert all(len(c)==1 for c in sig)
    return [list(next(iter(c.keys()))) for c in sig]

def main():
    # Witting 36 + axes.
    rays=build_rays();classes=clifford_classes(rays)
    assert [len(c) for c in classes]==[4,8,12,12]
    axes=[np.eye(4,dtype=complex)[i] for i in range(4)]
    R=np.array(rays+axes)
    G=np.abs(R.conj()@R.T)**2
    AW=(G<1e-9).astype(np.uint8);np.fill_diagonal(AW,0)
    assert set(AW.sum(axis=1).tolist())=={12}
    atoms=[set(range(36,40)),set(classes[0]),set(classes[1]),set(classes[2]),set(classes[3])]
    atom_names=['axes4','Clifford4','Clifford8','Clifford12a','Clifford12b']
    assert [len(x) for x in atoms]==[4,4,8,12,12]

    # Hermitian W33 model from Pass10105 convention.
    J=np.array([[0,1],[2,0]],dtype=np.int64)%P
    K=np.block([[J,np.zeros((2,2),dtype=np.int64)],[np.zeros((2,2),dtype=np.int64),J]])%P
    pts=sorted({canon(v) for v in itertools.product(range(P),repeat=4) if any(v)})
    assert len(pts)==40
    def hnorm(v):
        a=np.array(v[:2],dtype=np.int64)%P;b=np.array(v[2:],dtype=np.int64)%P
        return int((2*(a@J@b))%P)
    norms=[hnorm(p) for p in pts];assert Counter(norms)==Counter({0:16,1:12,2:12})
    AS=np.zeros((40,40),dtype=np.uint8)
    for i,x in enumerate(pts):
        xv=np.array(x,dtype=np.int64)
        for j in range(i+1,40):
            yv=np.array(pts[j],dtype=np.int64)
            if int(xv@K@yv)%P==0:AS[i,j]=AS[j,i]=1
    Hgroups=[[i for i,n in enumerate(norms) if n==c] for c in (0,1,2)]
    HQ=single_matrix(quotient_signature(AS,Hgroups))
    assert HQ==[[6,3,3],[4,2,6],[4,6,2]],HQ

    # All whole-atom 16|12|12 coarsenings of the Witting/axis grading.
    assignments=[];matrices=[]
    sizes=[len(a) for a in atoms]
    for assign in itertools.product(range(3),repeat=5):
        sums=[sum(sizes[i] for i,a in enumerate(assign) if a==b) for b in range(3)]
        if sums!=[16,12,12]:continue
        groups=[sorted(set().union(*(atoms[i] for i,a in enumerate(assign) if a==b))) for b in range(3)]
        Q=single_matrix(quotient_signature(AW,groups))
        assignments.append({'assignment':{atom_names[i]:assign[i] for i in range(5)},'quotient':Q})
        matrices.append(Q)
    assert len(assignments)==10
    expected=[[6,3,3],[4,5,3],[4,3,5]]
    assert all(Q==expected for Q in matrices)
    assert expected!=HQ

    # The most tempting coarsening axes4+Clifford4+Clifford8 | 12a | 12b is included.
    tempting=next(x for x in assignments if x['assignment']=={'axes4':0,'Clifford4':0,'Clifford8':0,'Clifford12a':1,'Clifford12b':2})
    assert tempting['quotient']==expected

    out={
      'schema':'w33.pass10337_10344.witting_unitary_partition_no_go.v1','status':'PASS','passes':'10337-10344',
      'inputs':{'Witting_plus_axes':'W33 orthogonality graph, atomic sizes 4 axes + Clifford 4|8|12|12','Hermitian_W33':'norm orbit sizes 16|12|12'},
      'Witting_coarsenings':{'labelled_16_12_12_assignments':10,'all_have_same_quotient_matrix':expected,'tempting_middle12_alignment':tempting},
      'Hermitian_norm_partition':{'quotient_matrix':HQ},
      'theorem':'No W33 graph automorphism can carry any union-of-natural-Witting/axis 16|12|12 coarsening to the Hermitian norm 16|12|12 partition. In particular the two 12-ray Clifford middle classes are not the two nonzero Hermitian norm orbits. The shared 12+12 cardinality is not an objectwise bridge.',
      'interpretation':'M36=W33 minus a line remains exact, but Clifford grading and Hermitian norm grading are transverse structures on the same 40-point W33 graph. Any eventual bridge must mix Clifford classes rather than identify them wholesale.',
      'boundary':'Exact quotient-degree obstruction. It rules out mappings preserving whole Clifford/axis blocks; it does not rule out a finer pointwise intertwiner that cuts across those blocks.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','coarsenings':10,'WittingQ':expected,'HermitianQ':HQ,'same':False}))
    return 0
if __name__=='__main__':raise SystemExit(main())
