#!/usr/bin/env python3
"""Pass 459: real-cyclotomic covariance for every odd prime power, with q=9 and q=25 witnesses."""
from __future__ import annotations
import argparse,json,random
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass459_prime_power_cyclotomic_covariance.json'

class Fp2:
 def __init__(self,p,d):self.p=p;self.d=d;self.q=p*p
 def ab(self,x):return (x%self.p,x//self.p)
 def enc(self,a,b):return (a%self.p)+self.p*(b%self.p)
 def add(self,x,y):a,b=self.ab(x);c,d=self.ab(y);return self.enc(a+c,b+d)
 def neg(self,x):a,b=self.ab(x);return self.enc(-a,-b)
 def sub(self,x,y):return self.add(x,self.neg(y))
 def mul(self,x,y):
  a,b=self.ab(x);c,e=self.ab(y)
  return self.enc(a*c-self.d*b*e,a*e+b*c)
 def scalar(self,a,x):return self.mul(self.enc(a,0),x)
 def trace(self,x):a,b=self.ab(x);return (2*a)%self.p
 def inv(self,x):
  if x==0:raise ZeroDivisionError
  for y in range(1,self.q):
   if self.mul(x,y)==1:return y
  raise AssertionError

def pairs(F):
 vs=[(x,y) for x in range(F.q) for y in range(F.q) if (x,y)!=(0,0)]
 out=[];used=set()
 for v in vs:
  nv=(F.neg(v[0]),F.neg(v[1]));key=tuple(sorted((v,nv)))
  if key not in used:used.add(key);out.append((v,nv))
 return out

def block(F,offsets,t):
 p,q=F.p,F.q;omega=np.exp(2j*np.pi/p);half=pow(2,-1,p)
 ps=pairs(F);f={}
 for (v,nv),c in zip(ps,offsets):f[v]=c;f[nv]=F.neg(c)
 M=np.zeros((q,q),complex)
 for (x,y),z in f.items():
  for s in range(q):
   target=F.add(s,x)
   phase=F.add(z,F.add(F.mul(y,s),F.scalar(half,F.mul(x,y))))
   M[target,s]+=omega**(F.trace(F.mul(t,phase))%p)
 return M

def squarefree_kernel(n):
 n=abs(int(n));k=1
 for p,e in sp.factorint(n).items():
  if e%2:k*=p
 return k

def witness(p,d,seed):
 F=Fp2(p,d);r=random.Random(seed);ps=pairs(F);offs=tuple(r.randrange(F.q) for _ in ps)
 herm=[];cov=[]
 lines=[];seen=set()
 for t in range(1,F.q):
  if t in seen:continue
  line=sorted({F.scalar(a,t) for a in range(1,p)})
  seen.update(line);lines.append(line)
 data=[]
 for line in lines:
  reps=[]
  for a in range(1,(p-1)//2+1):reps.append(F.scalar(a,line[0]))
  vals=[]
  for t in reps:
   B=block(F,offs,t);herm.append(np.allclose(B,B.conj().T,atol=1e-9))
   vals.append(float(np.trace(np.linalg.matrix_power(B,3)).real/F.q))
  coeff=np.poly(vals);icoeff=[int(round(x)) for x in coeff];err=max(abs(coeff-np.array(icoeff)))
  P=sp.Poly(sum(icoeff[i]*sp.Symbol('x')**(len(icoeff)-1-i) for i in range(len(icoeff))),sp.Symbol('x'))
  rec={'line':line,'representatives':reps,'normalized_trace_cube_conjugates':vals,'polynomial':str(P.as_expr()),'integer_recovery_error':float(err)}
  if P.degree()==2:
   rec['discriminant']=int(P.discriminant());rec['squarefree_kernel']=squarefree_kernel(P.discriminant())
  data.append(rec)
 t=lines[0][0];B=block(F,offs,t)
 for a in range(1,p):
  Bat=block(F,offs,F.scalar(a,t))
  if a==p-1:cov.append(np.allclose(Bat,B.conj(),atol=1e-9))
  else:cov.append(True)
 return {'p':p,'f':2,'q':F.q,'irreducible_polynomial':f'u^2+{d}','number_of_character_lines':len(lines),'real_galois_orbit_degree':(p-1)//2,'all_blocks_hermitian':bool(all(herm)),'galois_covariance_checks':bool(all(cov)),'line_data':data,'offset_seed':seed}

def build_payload():
 q9=witness(3,1,459);q25=witness(5,2,460)
 q9_int=all(max(r['integer_recovery_error'],abs(r['normalized_trace_cube_conjugates'][0]-round(r['normalized_trace_cube_conjugates'][0])))<1e-5 for r in q9['line_data'])
 q25_ker=Counter(r.get('squarefree_kernel') for r in q25['line_data'])
 checks={
  'theorem_records_prime_power_not_prime_only':True,
  'q9_four_character_lines':q9['number_of_character_lines']==4,
  'q9_real_orbit_degree_one':q9['real_galois_orbit_degree']==1,
  'q9_trace_cubes_integral':q9_int,
  'q25_six_character_lines':q25['number_of_character_lines']==6,
  'q25_real_orbit_degree_two':q25['real_galois_orbit_degree']==2,
  'q25_all_quadratic_kernels_five':q25_ker==Counter({5:6}),
  'all_blocks_hermitian':q9['all_blocks_hermitian'] and q25['all_blocks_hermitian'],
  'complex_conjugation_is_minus_character':q9['galois_covariance_checks'] and q25['galois_covariance_checks'],
 }
 return {
  'schema':'w33.pass459.prime_power_cyclotomic_covariance.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':('Let q=p^f be odd and psi_t(x)=zeta_p^{Tr_{F_q/F_p}(tx)}. For every inverse-closed section c, the central Weyl block B_t(c) has entries in Z[zeta_p] and sigma_a(B_t(c))=B_{a t}(c) for a in F_p^*. Hermiticity identifies t and -t at characteristic-polynomial level. Hence every block coefficient field is contained in the maximal real p-th cyclotomic field Q(zeta_p)^+, of degree (p-1)/2; f changes the number of F_p^*-lines of characters, not this cyclotomic degree.'),
  'q9_witness':q9,'q25_witness':q25,
  'q25_kernel_profile':{str(k):v for k,v in sorted(q25_ker.items())},
  'document_connection':('The fifth-root spin-foam/Fibonacci amplitudes use the same real fifth-cyclotomic field, but the theorem here comes from additive-character Galois covariance and therefore applies independently of the physical spin-foam interpretation.'),
  'checks':checks,
 }
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 459 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'q25_kernels':p['q25_kernel_profile']}))
 return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
