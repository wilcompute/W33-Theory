#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mm(a,b,q):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(a)))%q for j in range(len(a))) for i in range(len(a)))
def tr(a):return tuple(zip(*a))
def eye(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def inv(a,q):
 n=len(a);A=[list(a[i])+[int(i==j) for j in range(n)] for i in range(n)];r=0
 for c in range(n):
  p=next(i for i in range(r,n) if A[i][c]%q);A[r],A[p]=A[p],A[r];s=pow(A[r][c],-1,q);A[r]=[(s*x)%q for x in A[r]]
  for i in range(n):
   if i!=r and A[i][c]%q:
    f=A[i][c]%q;A[i]=[(A[i][j]-f*A[r][j])%q for j in range(2*n)]
  r+=1
 return tuple(tuple(row[n:]) for row in A)
def scale(s,a,q):return tuple(tuple(s*x%q for x in row) for row in a)
def verify(q):
 m=q-1;J=((0,1,0,0),(m,0,0,0),(0,0,0,1),(0,0,m,0));T=((0,0,1,0),(0,0,0,m),(1,0,0,0),(0,m,0,0))
 Cpf=((1,0,0,0),(0,1,0,m),(1,0,1,0),(0,0,0,1));Cfp=((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,m,0,1))
 Fp=((0,m,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1));Ff=((1,0,0,0),(0,1,0,0),(0,0,0,m),(0,0,1,0))
 roots=[s for s in range(1,q) if s*s%q==m]
 checks={'T2':mm(T,T,q)==eye(4),'multiplier_minus_one':mm(mm(tr(T),J,q),T,q)==scale(m,J,q),'cx_direction_conjugacy':mm(mm(T,Cpf,q),inv(T,q),q)==Cfp,'local_fourier_identity':mm(mm(mm(Fp,inv(Ff,q),q),Cpf,q),mm(inv(Fp,q),Ff,q),q)==Cfp,'square_criterion':bool(roots)==(q%4==1)}
 if roots:checks['rescaled_symplectic']=mm(mm(tr(scale(roots[0],T,q)),J,q),scale(roots[0],T,q),q)==J
 assert all(checks.values());sp=q**4*(q**2-1)*(q**4-1)
 return {'q':q,'minus_one_roots':roots,'Sp4_order':sp,'PSp4_order':sp//2,'projective_class':'inner' if roots else 'outer diagonal','checks':checks}
def main():
 rows=[verify(q) for q in (5,7)];checks={'q5_inner':rows[0]['projective_class']=='inner','q7_outer':rows[1]['projective_class']=='outer diagonal','q5_order':rows[0]['Sp4_order']==9360000,'q7_order':rows[1]['Sp4_order']==276595200}
 assert all(checks.values());out={'schema':'w33.pass2806.transpose_cx_q5_q7.v1','status':'EXACT','identity':'T^2=I, T^TJT=-J, T CX_pf T^-1=CX_fp','criterion':'inner for q=1 mod4, outer diagonal for q=3 mod4','rows':rows,'checks':checks}
 p=ROOT/'data/PART_BT2806_TRANSPOSE_CX_Q5_Q7_results.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
