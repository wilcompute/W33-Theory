#!/usr/bin/env python3
"""Pass10161-10168 outside-box: exact zeta9 action on the six-step chamber filtration.

Correct the parallel claim that zeta9 is a unit of O_K for K=Q3(i) and acts as
a Singer-like C3 permutation on chamber/Fano data.

zeta9 is NOT in K.  It lies in L=K(zeta9) and is a unit of O_L.  Multiplication
by zeta9=1+t is nevertheless K-linear on the rank-6 K-space L and preserves every
O_K-lattice t^j O_L because it is an O_L unit.

Modulo 3 we have O_L/3 ~= F9[t]/(t^6).  In the power basis, multiplication by
1+t is U=I+N where N raises t-adic degree.  Hence:

  U(t^j R)=t^j R for every j,
  U acts as IDENTITY on every associated-graded quotient t^jR/t^{j+1}R,
  N=U-I is the nontrivial extension/raising operator between adjacent layers,
  U^3=I+N^3 != I and U^9=I.

Thus the order-nine clock is stored in unipotent extension data ACROSS the six
layers, not as a permutation of the six chamber vertices and not as a C3 Singer
cycle on a Fano/Heawood graph.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10161_10168_ZETA9_FILTERED_ACTION.json'
P=3

def rankp(A):
    A=np.array(A,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
    return r

def main():
    n=6;I=np.eye(n,dtype=np.int64)%P
    # N e_j=e_{j+1}: multiplication by t in basis 1,t,...,t^5.
    N=np.zeros((n,n),dtype=np.int64)
    for j in range(n-1):N[j+1,j]=1
    U=(I+N)%P
    assert not np.any(np.linalg.matrix_power(N,6)%P)
    assert np.any(np.linalg.matrix_power(N,5)%P)
    U3=np.linalg.matrix_power(U,3)%P;U9=np.linalg.matrix_power(U,9)%P
    assert np.array_equal(U3,(I+np.linalg.matrix_power(N,3))%P)
    assert not np.array_equal(U3,I) and np.array_equal(U9,I)
    # Exact order.
    assert not np.array_equal(U,I)
    # Each tail ideal V_j=span(e_j,...,e_5) is invariant.
    ideals=[]
    for j in range(n):
        B=I[:,j:]
        UB=U@B%P
        assert rankp(np.column_stack([B,UB]))==B.shape[1]
        # On the one-dimensional quotient V_j/V_{j+1}, diagonal coefficient is 1.
        assert int(U[j,j])==1
        ideals.append({'j':j,'dimension_over_F9':n-j,'graded_action':'identity'})
    out={
      'schema':'w33.pass10161_10168.zeta9_filtered_action.v1','status':'PASS','passes':'10161-10168','outside_box':True,
      'field_correction':{'K':'Q3(i)','L':'K(zeta9)','zeta9_in_K':False,'zeta9_in_L':True,'zeta9_unit_of_O_L':True,'meaning':'multiplication by zeta9 is K-linear on L and fixes each lattice t^j O_L setwise'},
      'residue_action':{'ring':'F9[t]/(t^6)','U':'I+N','N':'degree-raising regular nilpotent, N^6=0','U_order':9,'U3':'I+N^3 != I','U9':'I','filtered_ideals':ideals},
      'associated_graded':{'six_F9_layers':6,'action_of_U':'identity on every t^j/t^{j+1}','nontrivial_clock_data':'N=U-I connects higher filtration degree; the order-nine information lives in extensions between layers'},
      'parallel_claim_corrections':['zeta9 is not in O_{Q3(i)}; it is an O_L unit','zeta9 fixes the six selected chamber vertices rather than cycling them','the induced action on each graded F9 layer is identity, not a Singer C3','there is no derived Fano/Heawood C3 action from this chamber fixation alone'],
      'theorem':'Multiplication by zeta9 fixes the entire six-step lattice chamber vertexwise and acts trivially on its associated graded, while U=1+N has exact order 9 on the filtered residue module. The cyclotomic clock is therefore unipotent extension data across the filtration, not a permutation clock on the chamber vertices.',
      'boundary':'Exact local/residue algebra statement. It does not rule out unrelated C3 actions elsewhere in the repo; it rules out deriving one from the vertexwise zeta9 chamber action asserted here.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','U_order':9,'graded_action':'identity','chamber_vertex_action':'fixed'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
