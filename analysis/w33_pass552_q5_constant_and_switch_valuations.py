#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from w33_pass543_547_common import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass552_q5_constant_and_switch_valuations.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2);C=CycPrime(5)
# O^+=Z[pi], pi=2-(zeta+zeta^-1), pi^2=5*pi-5. Pairs are c+d*pi.
def pmul(x,y,mod=None):
 c,d=x;e,f=y;z=(c*e-5*d*f,c*f+d*e+5*d*f)
 return z if mod is None else (z[0]%mod,z[1]%mod)
def padd(x,y,mod=None):
 z=(x[0]+y[0],x[1]+y[1]);return z if mod is None else (z[0]%mod,z[1]%mod)
def pneg(x,mod=None):z=(-x[0],-x[1]);return z if mod is None else (z[0]%mod,z[1]%mod)
def pconj(x):c,d=x;return(c+5*d,-d)
def pnorm(x):return pmul(x,pconj(x))[0]
def ppow(x,n):
 r=(1,0)
 while n:
  if n&1:r=pmul(r,x)
  x=pmul(x,x);n//=2
 return r
def pdiv(x,y):
 z=pmul(x,pconj(y));n=pnorm(y)
 if z[0]%n or z[1]%n:raise ArithmeticError((x,y,z,n))
 return(z[0]//n,z[1]//n)
def to_pi(x):
 assert x[1]==0 and x[2]==x[3]
 a,b=x[0]-x[2],-x[2]
 return(a+2*b,-b)
def divisible_pi(x,k):
 r=k//2
 if k%2==0:return x[0]%(5**r)==0 and x[1]%(5**r)==0
 return x[0]%(5**(r+1))==0 and x[1]%(5**r)==0
def vpi(x,limit=100):
 if x==(0,0):return 10**9
 for k in range(limit+1):
  if not divisible_pi(x,k+1):return k
 raise ArithmeticError('valuation limit')
def normalize(offs):
 cp,ts,D=charpoly_prime(5,offs);pi=(0,1)
 q=[pdiv(to_pi(cp[k]),ppow(pi,k)) for k in range(6)]
 init=[(0,0) if not any(ts[m-1]) else pdiv(to_pi(ts[m-1]),ppow(pi,m)) for m in range(1,6)]
 return q,init,D,cp,ts
def seq_mod(q,init,N,mod):
 out=[(a%mod,b%mod) for a,b in init]
 for m in range(6,N+1):
  s=(0,0)
  for j in range(1,6):s=padd(s,pmul(q[j],out[m-j-1],mod),mod)
  out.append(pneg(s,mod))
 return out
def vp(n,p=5):
 if n==0:return 10**9
 v=0
 while n%p==0:n//=p;v+=1
 return v
def constant_vpi_formula(m):
 if m==1:return 10**9
 if m%4==0:return 0
 if m%2==0:return 1+2*vp(m//2)
 r=m%20
 if r==1:return 3
 if r in (3,7,11,19):return 1
 if r in (9,13,17):return 2
 if r==5:return 2+2*vp(m)
 if r==15:return 1+2*vp(m)
 raise AssertionError(r)
def mzero(n):return [[(0,0) for _ in range(n)] for _ in range(n)]
def meye(n):
 M=mzero(n)
 for i in range(n):M[i][i]=(1,0)
 return M
def mm(A,B,mod):
 n=len(A);R=mzero(n)
 for i in range(n):
  for k in range(n):
   if A[i][k]!=(0,0):
    for j in range(n):
     if B[k][j]!=(0,0):R[i][j]=padd(R[i][j],pmul(A[i][k],B[k][j],mod),mod)
 return R
def mpow(A,n,mod):
 R=meye(len(A))
 while n:
  if n&1:R=mm(R,A,mod)
  A=mm(A,A,mod);n//=2
 return R
def companion(q):
 M=mzero(5)
 for i in range(1,5):M[i][i-1]=(1,0)
 for i in range(5):M[i][4]=pneg(q[5-i])
 return M
def matrix_diff_vpi(A,B,maxk=30):
 vals=[]
 for i in range(len(A)):
  for j in range(len(A)):
   vals.append(vpi((A[i][j][0]-B[i][j][0],A[i][j][1]-B[i][j][1]),maxk))
 return min(vals)
def traceM(A,mod):
 s=(0,0)
 for i in range(len(A)):s=padd(s,A[i][i],mod)
 return s

def payload():
 qC,iC,DC,cpC,tsC=normalize((1,)*12);qA,iA,DA,cpA,tsA=normalize(A)
 support={(i,j) for i in range(5) for j in range(5) if any(DC[i][j])}
 expected_support={(0,0),(1,1),(1,4),(4,1),(2,2),(2,3),(3,2),(3,3)}
 singleton=pdiv(to_pi(DC[0][0]),(0,1))
 def block_data(i,j):
  tr=C.add(DC[i][i],DC[j][j]);de=C.sub(C.mul(DC[i][i],DC[j][j]),C.mul(DC[i][j],DC[j][i]))
  return pdiv(to_pi(tr),(0,1)),pdiv(to_pi(de),ppow((0,1),2))
 blocks=[block_data(1,4),block_data(2,3)]
 maxm=50000;mod=5**9;sC=seq_mod(qC,iC,maxm,mod)
 formula_ok=True
 for m,x in enumerate(sC,1):
  pred=constant_vpi_formula(m)
  if pred>=10**8:
   if x!=(0,0):formula_ok=False;break
  elif not divisible_pi(x,pred) or divisible_pi(x,pred+1):formula_ok=False;break
 M=companion(qA);I=meye(5);lift=[]
 for j in range(4):
  exponent=312*(5**j);modj=5**(j+5);P=mpow(M,exponent,modj);val=matrix_diff_vpi(P,I,20);lift.append({'j':j,'exponent':exponent,'matrix_minus_identity_vpi':val})
 period_levels=[]
 for k in range(1,8):
  period=312*(5**((k)//2));modk=5**((k+1)//2+2);s=seq_mod(qA,iA,period,modk)
  zeros=sum(divisible_pi(x,k) for x in s)
  period_levels.append({'precision_pi_power':k,'period':period,'zero_residues':zeros})
 seqA=recurrence_traces(cpA,tsA,1000,C);automaton_match=True
 for m,x in enumerate(seqA,1):
  direct=10**9 if not any(x) else (vlam(x,C)-2*m)//2
  if direct>=10**8:continue
  found=None
  for k in range(0,12):
   period=312*(5**(((k+1)//2)));modk=5**((k+1)//2+3)
   T=mpow(M,m%period if m%period else period,modk);tr=traceM(T,modk)
   if not divisible_pi(tr,k+1):found=k;break
  if found!=direct:automaton_match=False;break
 checks={
  'constant_exact_block_support':support==expected_support,
  'constant_normalized_singleton_minus2':singleton==(-2,0),
  'constant_two_quadratic_blocks':blocks==[((1,0),(-25,5)),((1,0),(-32,7))],
  'constant_formula_50000':formula_ok,
  'odd_mod_pi_order312':matrix_diff_vpi(mpow(M,312,5**6),I,20)==1,
  'odd_order_lifts_by_two_pi_levels':[x['matrix_minus_identity_vpi'] for x in lift]==[1,3,5,7],
  'odd_period_formula_first7':[x['period'] for x in period_levels]==[312,1560,1560,7800,7800,39000,39000],
  'odd_automaton_matches_exact_1000':automaton_match,
 }
 return {
  'schema':'w33.pass552.q5_constant_and_switch_valuations.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'constant_family':{
   'normalized_block_factorization':{'singleton':singleton,'quadratic_blocks':[{'trace':a,'determinant':b} for a,b in blocks]},
   'all_m_formula':'For m=1 the trace is zero. Put delta=v_lambda(tr D^m)-2m=2 v_pi(S_m). If 4|m, delta=0. If m=2r with r odd, delta=2+4v5(r). For odd m: residues 3,7,11,19 mod20 give delta=2; 9,13,17 give 4; 1 gives 6; residue 5 gives 4+4v5(m); residue 15 gives 2+4v5(m).',
   'proof_mechanism':'The exact 1+2+2 block decomposition gives five Hensel root branches reducing to all elements of F5. Teichmuller decomposition and the principal-unit LTE v_pi(u^(5n)-1)=v_pi(u^n-1)+2 yield the displayed residue table and v5 lifts.',
   'verified_modular_window':maxm
  },
  'odd_switch_family':{
   'normalized_companion_mod_pi':'y^5+3y+2 over F5','companion_order_mod_pi':312,
   'order_lifting':lift,
   'precision_periods':period_levels,
   'all_m_algorithm':'For precision k, tr(M^m) modulo pi^k depends only on m modulo P_k=312*5^ceil((k-1)/2). The pi-adic valuation is the largest k for which that periodic trace is zero. Matrix powering gives an exact logarithmic-in-m decision procedure at every requested precision.',
   'interpretation':'Unlike the constant family, the zero residues form a branching 5-adic tree; a single short congruence formula would erase real arithmetic structure.'
  },
  'checks':checks,
  'boundary':'The constant-family formula is closed for all m. The odd-switch result is an exact all-precision periodic automaton and order-lifting theorem, not a compact scalar residue formula or a proof that no such formula exists.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 552 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
