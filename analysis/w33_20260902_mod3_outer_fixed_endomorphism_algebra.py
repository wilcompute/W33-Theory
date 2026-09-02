#!/usr/bin/env python3
"""Exact outer-fixed endomorphism algebra on the two modular St81 sectors.

Inputs already frozen in the repository prove:
  * the rational St81 multiplicity-three router has outer grading (+,+,-);
  * reduction mod 3 glues the two rational-even chain images into one rank-81
    image E and leaves the rational-odd image O disjoint, so E+O has rank 162;
  * E and O restrict to the same irreducible PSp4(3) Steinberg module and the
    defining-characteristic Schur centralizer is F3;
  * the solved PGSp outer signs are E:-1 and O:+1.

Therefore, after choosing the common building-H1 coordinates on each summand,
End_PSp(E+O) is M2(F3).  The outer involution acts on its multiplicity space by
D=diag(-1,+1), hence on a matrix unit by

    alpha(e_ij) = d_i d_j^{-1} e_ij.

This script materializes that four-dimensional algebra over F3, computes the
fixed subalgebra directly, and cross-checks it against the independently frozen
PGSp Hom table.  It deliberately does NOT assert a canonical ring reduction
M3(Q)->M2(F3): the statement is a degeneration of multiplicity structure in
these explicit chain images, not a denominator-free reduction homomorphism.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BRIDGE=ROOT/'data/PART_W33_20260902_MOD3_EVEN_GLUING_CSS_BRIDGE.json'
HOM=ROOT/'data/PART_W33_20260902_PGSP_MOD3_HOM_SPACES.json'
SIGN=ROOT/'data/PART_W33_20260902_MOD3_OUTER_SIGN_FACTORIZATION.json'
OUT=ROOT/'data/PART_W33_20260902_MOD3_OUTER_FIXED_ENDOMORPHISM_ALGEBRA.json'
P=3


def main():
    b=json.loads(BRIDGE.read_text());h=json.loads(HOM.read_text());s=json.loads(SIGN.read_text())
    assert b['status']=='PASS' and b['mod3']['evenOddCombinedRank']==162
    assert b['mod3']['combinedEvenRank']==81 and b['mod3']['rankOdd']==81
    assert h['status']=='PASS' and h['moduleDimension']==81
    assert h['outerSignsRelativeToBuildingS']['obstructionEven']==-1
    assert h['outerSignsRelativeToBuildingS']['obstructionOdd']==1
    assert s['status']=='PASS' and s['uniformInjectionFactor']==-1

    # Multiplicity coordinate order is (E,O), with -1 represented by 2 in F3.
    D=np.diag([2,1]).astype(np.int64)%P
    Dinv=D.copy() # involution
    units={}
    fixed=[];odd=[];action={}
    for i in range(2):
        for j in range(2):
            E=np.zeros((2,2),dtype=np.int64);E[i,j]=1
            A=(D@E@Dinv)%P
            key=f'e{i}{j}'
            units[key]=E.tolist();action[key]=A.tolist()
            if np.array_equal(A,E):fixed.append(key)
            elif np.array_equal(A,(-E)%P):odd.append(key)
            else:raise AssertionError('matrix unit not an outer eigenvector')
    assert fixed==['e00','e11'] and odd==['e01','e10']

    # Verify matrix-unit multiplication and determine dimensions by direct span.
    vec=lambda M:np.asarray(M,dtype=np.int64).reshape(-1)%P
    allmat=np.stack([vec(units[k]) for k in ['e00','e01','e10','e11']],axis=1)
    fixmat=np.stack([vec(units[k]) for k in fixed],axis=1)
    assert np.linalg.matrix_rank(allmat.astype(float))==4
    assert np.linalg.matrix_rank(fixmat.astype(float))==2
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    A=np.asarray(units[f'e{i}{j}']);B=np.asarray(units[f'e{k}{l}'])
                    C=(A@B)%P
                    expected=np.asarray(units[f'e{i}{l}']) if j==k else np.zeros((2,2),dtype=int)
                    assert np.array_equal(C%P,expected%P)

    # Independent Hom-table cross-check: End_PGSp(E+O) has only the two
    # diagonal scalar channels; cross Homs vanish.
    T=h['HomPGSpDimensions']
    assert T['obstructionEven']['obstructionEven']==1
    assert T['obstructionOdd']['obstructionOdd']==1
    assert T['obstructionEven']['obstructionOdd']==0
    assert T['obstructionOdd']['obstructionEven']==0
    Tp=h['HomPSpDimensions']
    assert all(Tp[a][c]==1 for a in ('obstructionEven','obstructionOdd') for c in ('obstructionEven','obstructionOdd'))

    out={
      'schema':'w33.20260902.mod3-outer-fixed-endomorphism-algebra.v1','status':'PASS','field':'F3',
      'module':'E_81 direct-sum O_81','combinedDimension':162,
      'restrictedGroup':'PSp4(3)','extendedGroup':'PGSp4(3)',
      'PSpEndomorphismAlgebra':{'isomorphism':'M2(F3)','dimension':4,
        'matrixUnits':['e00','e01','e10','e11']},
      'outerMultiplicityMatrix':[[2,0],[0,1]],
      'outerFixedMatrixUnits':fixed,'outerOddMatrixUnits':odd,
      'PGSpEndomorphismAlgebra':{'isomorphism':'F3 direct-sum F3','dimension':2,
        'basis':['e00','e11']},
      'homTableCrossCheck':True,
      'rationalToModularMultiplicityNarrative':{
        'characteristicZero':'three explicit St81 chain images with rational outer multiplicity grading 2_plus + 1_minus',
        'characteristicThree':'the two rational-even images coalesce to E while the rational-odd image survives as independent O',
        'afterOuterExtension':'cross matrix units E<->O are outer-odd and disappear from the PGSp fixed endomorphism algebra'},
      'theorem':'On the explicit 162-dimensional modular obstruction sum E+O, End_PSp is M2(F3). Adjoining the PGSp outer involution acts on multiplicity coordinates by diag(-1,+1); its fixed algebra is exactly the diagonal F3 direct-sum F3, while the two cross matrix units are outer-odd. This agrees independently with the frozen PGSp Hom table.',
      'boundary':'This is a theorem about finite modular representation and explicit chain-image multiplicities. It does not assert a canonical ring homomorphism M3(Q)->M2(F3), nor a physical superselection rule, particle sector, or chirality.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','EndPSp':'M2(F3)','dimPSp':4,'EndPGSp':'F3+F3','dimPGSp':2,'fixed':fixed,'outerOdd':odd},sort_keys=True))

if __name__=='__main__':main()
