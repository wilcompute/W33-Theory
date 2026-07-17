#!/usr/bin/env python3
"""Pass 401: critical-group/SNF anatomy of the Heisenberg bulk graphs."""
from __future__ import annotations
import argparse, hashlib, json, sys
from collections import Counter
from math import comb
from pathlib import Path
import numpy as np
import flint
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from w33_pass400_404_common import reduced_laplacian
OUT=ROOT/"data"/"w33_pass401_critical_group_bockstein.json"

def nmod_array(mat,cols=None):
 if cols is None:cols=mat.ncols()
 return np.array([[int(mat[i,j]) for j in range(cols)] for i in range(mat.nrows())],dtype=object)
def null_basis(arr,p):
 N,d=flint.nmod_mat((np.asarray(arr,dtype=object)%p).tolist(),p).nullspace();return nmod_array(N,d)
def rank_mod(arr,p):return flint.nmod_mat((np.asarray(arr,dtype=object)%p).tolist(),p).rank()
def solve_many_mod(M,R,p):
 M=np.asarray(M,dtype=object);R=np.asarray(R,dtype=object);m,n=M.shape;k=R.shape[1];aug=np.concatenate([M%p,R%p],axis=1);RR,_=flint.nmod_mat(aug.tolist(),p).rref();rr=nmod_array(RR);Y=np.zeros((n,k),dtype=object)
 for row in range(RR.nrows()):
  piv=[j for j in range(n) if int(rr[row,j])%p]
  if not piv:
   if any(int(rr[row,n+j])%p for j in range(k)):raise AssertionError("inconsistent modular lifting system")
   continue
  pivot=piv[0]
  for j in range(k):Y[pivot,j]=int(rr[row,n+j])%p
 if np.any((M@Y-R)%p):raise AssertionError("modular solve verification failed")
 return Y
def bockstein_three_levels(M,p):
 X=null_basis(M,p);Y=null_basis(M.T,p);n1=X.shape[1];MX=M@X;assert np.all(MX%p==0);C1=np.vectorize(lambda v:(int(v)//p)%p,otypes=[object])(MX);B1=(Y.T@C1)%p;K=null_basis(B1,p);Z=null_basis(B1.T,p);n2=K.shape[1];X0=(X@K)%p;MX0=M@X0;assert np.all(MX0%p==0);rhs=np.vectorize(lambda v:-(int(v)//p)%p,otypes=[object])(MX0);cor=solve_many_mod(M,rhs,p);X1=X0+p*cor;MX1=M@X1;assert np.all(MX1%(p*p)==0);C2=np.vectorize(lambda v:(int(v)//(p*p))%p,otypes=[object])(MX1);B2=(Z.T@((Y.T@C2)%p))%p;r2=rank_mod(B2,p);n3=n2-r2
 return n1,n2,n3,{"beta1_rank":rank_mod(B1,p),"beta2_rank":r2,"right_kernel_dimension":n1,"left_kernel_dimension":Y.shape[1]}
def exact_snf(q):
 M=flint.fmpz_mat(reduced_laplacian(q).tolist());S=M.snf();return [abs(int(S[i,i])) for i in range(S.nrows())]
def valuations(diag,p):
 out=[]
 for d in diag:
  e=0
  while d%p==0:d//=p;e+=1
  out.append(e)
 return out
def q_primary_formula(q):
 c=comb(q+2,3);n1=q**3-1-c;n2=c-2;n3=q**2-2
 return {"cumulative":[n1,n2,n3],"elementary_counts":{str(q):n1-n2,str(q**2):n2-n3,str(q**3):n3},"q_adic_order_exponent":q**3+q**2-5}
def two_primary_formula(q):
 def v2(x):
  e=0
  while x%2==0:x//=2;e+=1
  return e
 a,b=v2(q-1),v2(q+1);lo=q*(q-1);hi=q*(q-1)**2//2
 return {"a_v2_q_minus_1":a,"b_v2_q_plus_1":b,"elementary_counts":{str(2**a):lo,str(2**(a+b)):hi},"cumulative":[(lo if j<=a else 0)+(hi if j<=a+b else 0) for j in range(1,a+b+1)]}
def spanning_tree_order(q):
 mp=q*(q*q-1)//2;mm=q*(q-1)*(q-1)//2;return q**(q**3+q**2-5)*(q-1)**mp*(q+1)**mm
def tree_prime_valuation(q,p):
 mp=q*(q*q-1)//2;mm=q*(q-1)*(q-1)//2
 def vp(x):
  e=0
  while x%p==0:x//=p;e+=1
  return e
 return (q**3+q**2-5)*vp(q)+mp*vp(q-1)+mm*vp(q+1)
def build_payload():
 snf={q:exact_snf(q) for q in (3,5)};snfc={str(q):{str(k):v for k,v in sorted(Counter(snf[q]).items())} for q in snf};bock={}
 for q,primes in ((3,(2,3)),(5,(2,3,5)),(7,(2,3,7))):
  M=reduced_laplacian(q);bock[str(q)]={}
  for p in primes:
   n1,n2,n3,d=bockstein_three_levels(M,p);bock[str(q)][str(p)]={"cumulative_divisibility_counts_p_p2_p3":[n1,n2,n3],"tree_order_p_valuation":tree_prime_valuation(q,p),**d}
 checks={}
 for q in (3,5):
  diag=snf[q];checks[f"q{q}_snf_order_matches_tree_formula"]=int(np.prod(np.array(diag,dtype=object)))==spanning_tree_order(q);qv=valuations(diag,q);checks[f"q{q}_q_primary_matches_formula"]=[sum(e>=j for e in qv) for j in (1,2,3)]==q_primary_formula(q)["cumulative"];tv=valuations(diag,2);mx=max(tv);checks[f"q{q}_two_primary_matches_formula"]=[sum(e>=j for e in tv) for j in range(1,mx+1)]==two_primary_formula(q)["cumulative"]
 q7q=bock["7"]["7"]["cumulative_divisibility_counts_p_p2_p3"];checks["q7_q_primary_bockstein_matches_formula"]=q7q==q_primary_formula(7)["cumulative"];q72=bock["7"]["2"]["cumulative_divisibility_counts_p_p2_p3"];checks["q7_two_primary_first_three_levels"]=q72==two_primary_formula(7)["cumulative"][:3];checks["q7_two_primary_fourth_level_forced_by_order_and_annihilator"]=tree_prime_valuation(7,2)-sum(q72)==two_primary_formula(7)["cumulative"][3];checks["q7_three_primary_is_elementary"]=bock["7"]["3"]["cumulative_divisibility_counts_p_p2_p3"]==[168,0,0];checks={k:bool(v) for k,v in checks.items()}
 p={"schema":"w33.pass401.critical_group_bockstein.v1","status":"PASS" if all(checks.values()) else "FAIL","exact_full_smith_forms":snfc,"exact_q3_critical_group":"Z/3^8 + Z/9 + (Z/27)^7 + (Z/2)^6 + (Z/8)^6","exact_q5_primary_description":{"5_primary":"(Z/5)^56 + (Z/25)^10 + (Z/125)^23","2_primary":"(Z/4)^20 + (Z/8)^40","3_primary":"(Z/3)^40"},"q7_certified_primary_description":{"7_primary":"(Z/7)^176 + (Z/49)^35 + (Z/343)^47","2_primary":"(Z/2)^42 + (Z/16)^126","3_primary":"(Z/3)^168","method":"two Bockstein pages plus exact order and the cubic Laplacian annihilator"},"prime_q_q_primary_law":{"status":"conjectured for every odd prime; exactly certified at q=3,5,7","formula":"(Z/q)^(q^3+1-2*C(q+2,3)) + (Z/q^2)^(C(q+2,3)-q^2) + (Z/q^3)^(q^2-2)","instances":{str(q):q_primary_formula(q) for q in (3,5,7)}},"odd_q_two_primary_law":{"status":"conjectured for odd q; exact at q=3,5 and Bockstein/order-certified at q=7","formula":"(Z/2^a)^(q(q-1)) + (Z/2^(a+b))^(q(q-1)^2/2), a=v2(q-1), b=v2(q+1)","instances":{str(q):two_primary_formula(q) for q in (3,5,7)}},"annihilator":"on the degree-zero lattice, q^4(q^2-1) is in the Laplacian ideal via (L-q^2I)(L-q(q-1)I)(L-q(q+1)I)=0","bockstein_certificates":bock,"checks":checks};canonical=json.dumps(p,sort_keys=True,separators=(",",":")).encode();p["certificate_sha256"]=hashlib.sha256(canonical).hexdigest();return p
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ap.add_argument("--output",type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit("Pass 401 frozen certificate is stale")
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({"status":p["status"],"checks":sum(p["checks"].values()),"total":len(p["checks"])}));return 0 if p["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
