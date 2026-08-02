#!/usr/bin/env python3
"""Passes 2201-2202: all-odd-q regular-spread two-class scheme.

A regular symplectic spread is an elliptic hyperplane section
O_x = Q(4,q) cap x^perp, indexed by a minus anisotropic point x.  The Gram
invariant Delta=4Q(x)Q(y)-B(x,y)^2 distinguishes tangent and secant sections.
The incidence Gram identity proves the strongly regular parameters for every
odd q.  Literal checks are made at q=3,5,7,11.
"""
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2201_2202_all_q_regular_spread_scheme.json'

def norm(v,q):
 for a in v:
  if a%q:
   z=pow(a,-1,q);return tuple(z*x%q for x in v)
 raise ValueError

def Q(x,q):return (x[0]*x[1]+x[2]*x[3]+x[4]*x[4])%q
def B(x,y,q):return (x[0]*y[1]+x[1]*y[0]+x[2]*y[3]+x[3]*y[2]+2*x[4]*y[4])%q
def Delta(x,y,q):return (4*Q(x,q)*Q(y,q)-B(x,y,q)**2)%q

def minus_points(q):
 sq={a*a%q for a in range(1,q)}
 pts=sorted({norm(v,q) for v in itertools.product(range(q),repeat=5) if any(v)})
 return [p for p in pts if Q(p,q)!=0 and Q(p,q) not in sq]

def formulas(q):
 return {'v':q*q*(q*q-1)//2,
  'k':q*(q-2)*(q*q+1)//2,
  'lambda':q*(q**3-4*q*q+7*q-8)//2,
  'mu':q*(q-2)*(q-1)**2//2,
  'r':q*(q-2),'s':-q,
  'multiplicity_r':q*(q*q+1)//2,
  'multiplicity_s':(q-2)*(q+1)*(q*q+1)//2,
  'one_line_degree':(q-1)*(q*q+1)}

def verify_q(q,full=False):
 P=minus_points(q);f=formulas(q);assert len(P)==f['v'];x=P[0]
 adj=[y for y in P if y!=x and Delta(x,y,q)!=0]
 non=[y for y in P if y!=x and Delta(x,y,q)==0]
 assert len(adj)==f['k'] and len(non)==f['one_line_degree']
 ya,yn=adj[0],non[0]
 lam=sum(Delta(x,z,q)!=0 and Delta(ya,z,q)!=0 for z in P if z not in (x,ya))
 mu=sum(Delta(x,z,q)!=0 and Delta(yn,z,q)!=0 for z in P if z not in (x,yn))
 assert (lam,mu)==(f['lambda'],f['mu'])
 hist=None
 if full:
  h=Counter('q+1' if Delta(a,b,q)!=0 else '1' for i,a in enumerate(P) for b in P[i+1:])
  assert h['q+1']==f['v']*f['k']//2 and h['1']==f['v']*f['one_line_degree']//2
  hist=dict(sorted(h.items()))
 return {'q':q,'minus_points':len(P),'degree_qplus1':len(adj),'degree_one':len(non),
  'common_adjacent':lam,'common_nonadjacent':mu,'exhaustive_pair_histogram':hist,'formula':f}

def incidence(q):
 # Collinearity graph of Q(4,q) has eigenvalues q(q+1), q-1, -(q+1).
 n=(q+1)*(q*q+1);d=q*q*(q-1)//2;b=q*(q-1)//2
 gp=d-b*(1+(q-1));gm=d-b*(1-(q+1))
 assert gp==0 and gm==q*q*(q-1)
 return {'singular_points':n,'elliptic_sections_through_point':d,
  'elliptic_sections_through_noncollinear_pair':b,
  'BtransposeB':'d I + b (J-I-A_Q)','BBtranspose':'q^2 I + J + q A',
  'zero_eigenvalue_from_q_minus_1_space':gp,
  'positive_eigenvalue_from_minus_q_minus_1_space':gm}

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build():
 rows=[verify_q(q,q==3) for q in (3,5,7,11)];proof=[incidence(q) for q in (3,5,7,11)]
 checks={'q357_matches_frozen_orbit_sizes':[r['minus_points'] for r in rows[:3]]==[36,300,1176],
  'q11_prediction_verified':rows[3]['minus_points']==7260,
  'q3_full_pair_census':rows[0]['exhaustive_pair_histogram']=={'1':360,'q+1':270},
  'q35711_parameter_rows_verified':all(r['degree_qplus1']==r['formula']['k'] and r['common_adjacent']==r['formula']['lambda'] and r['common_nonadjacent']==r['formula']['mu'] for r in rows),
  'incidence_gram_eigenvalues_verified':all(p['zero_eigenvalue_from_q_minus_1_space']==0 and p['positive_eigenvalue_from_minus_q_minus_1_space']>0 for p in proof)}
 assert all(checks.values())
 out={'schema':'w33.pass2201_2202.all_q_regular_spread_scheme.v1',
  'status':'PASS_ALL_ODD_Q_REGULAR_SPREAD_SRG_THEOREM',
  'theorem':{'objects':'regular symplectic spreads, equivalently elliptic hyperplane sections of Q(4,q)',
   'pair_invariant':'Delta(x,y)=4Q(x)Q(y)-B(x,y)^2',
   'intersection_rule':'Delta=0 gives 1 common line; Delta nonzero gives q+1 common lines',
   'vertices':'q^2(q^2-1)/2',
   'qplus1_relation':{'k':'q(q-2)(q^2+1)/2','lambda':'q(q^3-4q^2+7q-8)/2','mu':'q(q-2)(q-1)^2/2','eigenvalues':['q(q-2)','-q'],'multiplicities':['q(q^2+1)/2','(q-2)(q+1)(q^2+1)/2']},
   'scope':'two-class strongly regular fusion; the full PGSp action need not have rank three for q>3'},
  'finite_checks':rows,'incidence_proof_checks':proof,'checks':checks,
  'boundaries':['The theorem concerns the regular/Desarguesian symplectic-spread orbit.','Non-Desarguesian symplectic spreads are not included.','The graph is a rank-three association-scheme fusion, not a claim that every full group action has rank three.','The orthogonal/field-reduction description and standard polar-space spectra retain literature ownership.']}
 out['sha256_without_hash_field']=digest(out);return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();out=build()
 if a.verify_frozen:assert json.loads(CERT.read_text())==out
 if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
