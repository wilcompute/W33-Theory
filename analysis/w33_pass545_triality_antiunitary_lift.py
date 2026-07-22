#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from fractions import Fraction as Q
from pathlib import Path
from w33_pass543_547_common import *
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass545_triality_antiunitary_lift.json'
def mmq(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mvq(A,v):return tuple(sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A)))
def tq(A):return [list(x) for x in zip(*A)]
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def ctranspose(A,C):return [[C.conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]
def conjM(A,C):return [[C.conj(x) for x in row] for row in A]
def payload():
 C=CycPrime(3);V=(1,0,0,0);Sp=(1,1,1,1);Sm=(1,1,1,2);DV=difference_prime(3,V);DP=difference_prime(3,Sp);DM=difference_prime(3,Sm)
 cpV=charpoly_prime(3,V)[0];cpP=charpoly_prime(3,Sp)[0];cpM=charpoly_prime(3,Sm)[0]
 W=[[C.from_exp(i*j) for j in range(3)] for i in range(3)];WW=matmul(W,ctranspose(W,C),C)
 anti=matmul(matmul(W,conjM(DP,C),C),ctranspose(W,C),C);unit=matmul(matmul(W,DP,C),ctranspose(W,C),C);threeDM=[[C.smul(3,x) for x in row] for row in DM]
 T=[[Q(x,2) for x in r] for r in [[1,1,1,-1],[1,1,-1,1],[1,-1,1,1],[1,-1,-1,-1]]]
 VS={tuple(Q(s if i==j else 0) for i in range(4)) for j in range(4) for s in (-1,1)};SS=[set(),set()]
 for a in itertools.product((-1,1),repeat=4):SS[sum(x<0 for x in a)%2].add(tuple(Q(x,2) for x in a))
 checks={
  'triality_T_order3':mmq(mmq(T,T),T)==eye(4),
  'triality_cycles_weight_sets':{mvq(T,x) for x in VS}==SS[0] and {mvq(T,x) for x in SS[0]}==SS[1] and {mvq(T,x) for x in SS[1]}==VS,
  'fourier_scaled_unitary':WW==[[C.smul(3,C.one()) if i==j else C.zero() for j in range(3)] for i in range(3)],
  'exact_antiunitary_intertwiner':anti==threeDM,
  'plain_unitary_fourier_fails':unit!=threeDM,
  'halfspin_charpolys_equal':cpP==cpM,
  'vector_charpoly_distinct':cpV!=cpP,
  'support_obstructs_internal_triality':sum(x!=0 for x in V)!=sum(x!=0 for x in Sp),
 }
 return {'schema':'w33.pass545.triality_antiunitary_lift.v1','status':'PASS' if all(checks.values()) else 'FAIL','section_triality':{'T':[[str(x) for x in row] for row in T],'cycle':['8v','8s+','8s-','8v'],'outer_reason':'SL(2,3) preserves support, whereas T sends support one to support four.'},'heisenberg_lift':{'operator':'normalized qutrit Fourier transform composed with complex conjugation','exact_identity':'W conjugate(D_+) W^*=3 D_-','halfspin_charpoly':cpP,'vector_charpoly':cpV,'conclusion':'The two half-spin blocks fuse by an antiunitary Clifford symmetry. The vector block cannot join because its characteristic polynomial is different.'},'checks':checks,'boundary':'This lifts the half-spin transposition, not the full order-three triality as a similarity of qutrit blocks.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 545 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
