#!/usr/bin/env python3
"""Pass 2203: exact q=27 Ree--Tits nonregular symplectic-spread control."""
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2203_ree_tits_nonregular_control.json'

def coeff(a):return a%3,(a//3)%3,(a//9)%3
def enc(c):return c[0]%3+3*(c[1]%3)+9*(c[2]%3)
def add0(a,b):
 A,B=coeff(a),coeff(b);return enc(((A[0]+B[0])%3,(A[1]+B[1])%3,(A[2]+B[2])%3))
def neg0(a):
 A=coeff(a);return enc(((-A[0])%3,(-A[1])%3,(-A[2])%3))
def mul0(a,b):
 A,B=coeff(a),coeff(b);c=[0]*5
 for i,x in enumerate(A):
  for j,y in enumerate(B):c[i+j]=(c[i+j]+x*y)%3
 for k in (4,3):
  x=c[k]%3;c[k]=0;c[k-2]=(c[k-2]+x)%3;c[k-3]=(c[k-3]+2*x)%3
 return enc(c[:3])
ADD=[[add0(a,b) for b in range(27)] for a in range(27)]
NEG=[neg0(a) for a in range(27)]
MUL=[[mul0(a,b) for b in range(27)] for a in range(27)]
def powf(a,n):
 r=1
 while n:
  if n&1:r=MUL[r][a]
  a=MUL[a][a];n//=2
 return r
INV=[0]+[powf(a,25) for a in range(1,27)]

def rref2(u,v):
 rows=[list(u),list(v)];r=0
 for c in range(4):
  p=next((i for i in range(r,2) if rows[i][c]),None)
  if p is None:continue
  rows[r],rows[p]=rows[p],rows[r];z=INV[rows[r][c]];rows[r]=[MUL[z][x] for x in rows[r]]
  for i in range(2):
   if i!=r and rows[i][c]:
    f=rows[i][c];rows[i]=[ADD[rows[i][j]][NEG[MUL[f][rows[r][j]]]] for j in range(4)]
  r+=1
  if r==2:break
 assert r==2;return tuple(rows[0]+rows[1])

def spread(g):
 S={rref2((0,0,0,1),(0,0,1,0))}
 for x in range(27):
  for y in range(27):S.add(rref2((0,1,x,y),(1,0,NEG[y],g(x,y))))
 assert len(S)==730;return frozenset(S)

def symp(x,v):
 z=ADD[MUL[x[0]][v[3]]][NEG[MUL[x[3]][v[0]]]]
 z=ADD[z][NEG[MUL[x[1]][v[2]]]];return ADD[z][MUL[x[2]][v[1]]]
def tv(x,v,lam):
 c=MUL[lam][symp(x,v)];return tuple(ADD[x[i]][MUL[c][v[i]]] for i in range(4))
def tline(L,v,lam):return rref2(tv(L[:4],v,lam),tv(L[4:],v,lam))
def tspread(S,v,lam):return frozenset(tline(L,v,lam) for L in S)
def orbit(start,vectors):
 gens=[(v,l) for v in vectors for l in (1,2)];seen={start};dq=deque([start])
 while dq:
  S=dq.popleft()
  for v,l in gens:
   T=tspread(S,v,l)
   if T not in seen:seen.add(T);dq.append(T)
 return seen

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build():
 regular=lambda x,y:NEG[MUL[3][x]]
 ree=lambda x,y:NEG[ADD[powf(x,21)][powf(y,9)]]
 cases=0
 for a in range(27):
  a2=MUL[a][a]
  for b in range(27):
   vals=[]
   for x in range(27):
    axb=ADD[MUL[a][x]][NEG[b]];vals.append(ADD[ree(x,axb)][MUL[a2][x]])
   assert len(set(vals))==27;cases+=1
 R,T=spread(regular),spread(ree);assert len(R&T)==28
 specs={'two_coordinate_planes':[(1,0,0,0),(0,0,0,1),(0,1,0,0),(0,0,1,0)],
  'rank_two_control':[(1,0,0,0),(0,0,0,1)],
  'mixed_three_vector':[(1,0,0,0),(0,0,0,1),(1,1,0,0)]}
 rows={};values=set()
 for name,vs in specs.items():
  O=orbit(R,vs);h=Counter(len(S&T) for S in O);values.update(h)
  rows[name]={'orbit_size':len(O),'intersection_histogram':{str(k):v for k,v in sorted(h.items())}}
 outside=sorted(x for x in values if x not in (1,28));assert outside==[19,37,46,55]
 assert rows['two_coordinate_planes']=={'orbit_size':144,'intersection_histogram':{'19':34,'28':76,'37':28,'46':4,'55':2}}
 checks={'gf27_nonzero_inverses':all(MUL[a][INV[a]]==1 for a in range(1,27)),
  'ball_zieve_permutation_cases_729':cases==729,'both_spreads_have_730_lines':len(R)==len(T)==730,
  'base_pair_meets_in_qplus1':len(R&T)==28,'closed_144_spread_suborbit':rows['two_coordinate_planes']['orbit_size']==144,
  'regular_two_intersection_extension_refuted':bool(outside)};assert all(checks.values())
 out={'schema':'w33.pass2203.ree_tits_nonregular_control.v1','status':'PASS_NONREGULAR_CONTROL_REFUTES_UNIFORM_TWO_INTERSECTION_EXTENSION',
  'field':'GF(27)=F3[t]/(t^3+2t+1)','ree_tits_slice':'g(x,y)=-x^21-y^9','regular_control':'g(x,y)=-t x',
  'ball_zieve_permutation_cases':cases,'base_intersection':len(R&T),'subgroup_orbits':rows,
  'intersection_values_outside_regular_scheme':outside,'checks':checks,
  'theorem':'The regular-spread {1,q+1} intersection scheme does not extend unchanged to the q=27 Ree--Tits symplectic spread: an exact closed 144-spread suborbit already exhibits intersections 19,28,37,46,55.',
  'boundaries':['This is an exact counterexample to an unchanged regular-scheme extension, not a classification of non-Desarguesian spreads.','The Ree--Tits and Ball--Zieve coordinate constructions retain literature ownership.','The observed congruence of all intersection values modulo 9 is recorded only as a future question.']}
 out['sha256_without_hash_field']=digest(out);return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();out=build()
 if a.verify_frozen:assert json.loads(CERT.read_text())==out
 if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
