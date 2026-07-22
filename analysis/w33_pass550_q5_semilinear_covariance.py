#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from pathlib import Path
from w33_pass543_547_common import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass550_q5_semilinear_covariance.json'
p=5;C=CycPrime(5);P=classes(5);IDX={v:i for i,v in enumerate(P)}
A=(1,1,2,2,2,3,3,2,3,2,3,2)

def det(g):a,b,c,d=g;return (a*d-b*c)%p
def gm(g,h):
 a,b,c,d=g;e,f,u,v=h
 return ((a*e+b*u)%p,(a*f+b*v)%p,(c*e+d*u)%p,(c*f+d*v)%p)
def gv(g,x):a,b,c,d=g;return ((a*x[0]+b*x[1])%p,(c*x[0]+d*x[1])%p)
def inv(g):
 a,b,c,d=g;q=pow(det(g),-1,p)
 return (d*q%p,-b*q%p,-c*q%p,a*q%p)
def gl():return [g for g in itertools.product(range(p),repeat=4) if det(g)]
def sl():return [g for g in gl() if det(g)==1]

def section_dict(offs):
 s={}
 for v,c in zip(P,offs):s[v]=c%p;s[((-v[0])%p,(-v[1])%p)]=(-c)%p
 return s

def act_section(g,offs):
 s=section_dict(offs);gi=inv(g);d=det(g)
 return tuple(d*s[gv(gi,w)]%p for w in P)

def ctranspose(M):return [[C.conj(M[j][i]) for j in range(p)] for i in range(p)]
def conjM(M):return [[C.conj(x) for x in row] for row in M]
def smat(k,M):return [[C.smul(k,x) for x in row] for row in M]

def weyl(a,b):
 M=[[C.zero() for _ in range(p)] for _ in range(p)]
 for x in range(p):M[(x+a)%p][x]=C.from_exp((2*x*b+a*b)%p)
 return M

def qdiag(r):
 M=[[C.zero() for _ in range(p)] for _ in range(p)]
 for x in range(p):M[x][x]=C.from_exp(r*x*x)
 return M

def closure(gens):
 S={(1,0,0,1)};front=list(S)
 while front:
  x=front.pop()
  for y in gens:
   z=gm(x,y)
   if z not in S:S.add(z);front.append(z)
 return S

def payload():
 F=[[C.from_exp(i*j) for j in range(p)] for i in range(p)]
 Q=qdiag(1);Ft=ctranspose(F);Qt=ctranspose(Q)
 fmat=(0,3,3,0);qmat=(1,0,1,1)
 allv=list(itertools.product(range(p),repeat=2))
 fourier_ok=all(matmul(matmul(F,weyl(*v),C),Ft,C)==smat(5,weyl(*gv(fmat,v))) for v in allv)
 shear_ok=all(matmul(matmul(Q,weyl(*v),C),Qt,C)==weyl(*gv(qmat,v)) for v in allv)
 sigma_ok={d:all([[C.sigma(d,x) for x in row] for row in weyl(*v)]==weyl(*gv((1,0,0,d),v)) for v in allv) for d in (1,2,3,4)}
 conj_ok=all(conjM(weyl(*v))==weyl(*gv((1,0,0,4),v)) for v in allv)
 SL=sl();GL=gl();generated=closure([fmat,qmat])
 decompositions=all(det(gm(g,(1,0,0,pow(det(g),-1,p))))==1 for g in GL)
 tests=[(0,)*12,(1,)+(0,)*11,(1,)*12,A,(0,1,2,3,4,0,1,2,3,4,0,1)]
 covariance=True;real=True
 for offs in tests:
  cp0=charpoly_prime(5,offs)[0]
  real&=all(C.conj(x)==x for x in cp0)
  for g in GL:
   cp1=charpoly_prime(5,act_section(g,offs))[0]
   if cp1!=[C.sigma(det(g),x) for x in cp0]:covariance=False;break
 fixed_cps=set()
 for mask in range(1<<12):
  offs=tuple(a*(4 if (mask>>i)&1 else 1)%5 for i,a in enumerate(A))
  fixed_cps.add(tuple(charpoly_prime(5,offs)[0]))
 sigma2_fixed=sum(tuple(C.sigma(2,x) for x in cp)==cp for cp in fixed_cps)
 checks={
  'gl_order480_four_det_fibres120':len(GL)==480 and all(sum(det(g)==d for g in GL)==120 for d in (1,2,3,4)),
  'sl_generated_by_fourier_and_shear':generated==set(SL) and len(generated)==120,
  'fourier_exact_all_weyl':fourier_ok,
  'shear_exact_all_weyl':shear_ok,
  'galois_diagonal_exact_all_weyl':all(sigma_ok.values()),
  'complex_conjugation_is_det_minus1':conj_ok,
  'all_gl_decompose_sl_times_diag':decompositions,
  'charpoly_covariance_all480_test_family':covariance,
  'hermitian_charpolys_real':real,
  'fixed_profile_has_no_sigma2_fixed_charpoly':len(fixed_cps)==98 and sigma2_fixed==0,
 }
 return {
  'schema':'w33.pass550.q5_semilinear_covariance.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'generator_covariance':{
    'fourier':{'matrix_on_phase_space':fmat,'identity':'F W(v) F*=5 W(fv)'},
    'quadratic_phase':{'matrix_on_phase_space':qmat,'identity':'Q W(v) Q*=W(qv)'},
    'galois':{'matrix':'diag(1,d)','identity':'sigma_d(W(a,b))=W(a,d b)'},
    'classification':{'det1':'unitary Clifford','det4':'antiunitary Clifford (complex conjugation times a unitary)','det2_det3':'genuine Galois-semilinear Clifford'}
  },
  'global_law':{'formula':'chi_{g.c}(x)=sigma_det(g)(chi_c(x)) for g in GL(2,5)','group_order':480,'determinant_fibre_size':120,'test_sections':len(tests)},
  'forced_fusions':{'det_minus1':'All Hermitian characteristic polynomials are conjugation-fixed, so determinant -1 covariance forces spectral fusion whenever it joins two section orbits.','det_2_3':'These give Galois mates, not equality unless the polynomial is sigma_2-fixed.','fixed_magnitude_exact_charpolys':len(fixed_cps),'sigma2_fixed_in_fixed_profile':sigma2_fixed,'conclusion':'The Pass-540 exceptional pair is not explained by a missing representation or by determinant-2/3 Galois fixation; its equality is an additional nonlinear collision.'},
  'checks':checks,'boundary':'Operator identities are exact on all 25 Weyl operators. Full characteristic-polynomial covariance is theorem-level from those generators and is independently checked on five separating sections under all 480 matrices.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 550 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
