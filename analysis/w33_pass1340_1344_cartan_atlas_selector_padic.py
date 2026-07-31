#!/usr/bin/env python3
"""Exact verifier for Passes 1340--1344.

Reconstructs the literal 26-dimensional Hecke tensor from Pass 1321 and verifies
modular Cartan data, frozen Atlas-standard matrices, and literal cycle orbits.
Pass 1343 p-adic lifting is independently verified by its dedicated executable.
"""
from __future__ import annotations
from pathlib import Path
import hashlib,json,sys
import sympy as sp

ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass1330_1334_modular_triality_cycle_atlas as old
P=old.P;ONE=[1]+[0]*25;BASIS=[[int(i==j) for i in range(26)] for j in range(26)]
CERT=json.loads((DATA/'w33_pass1340_1344_cartan_atlas_selector_padic.json').read_text())
ATLAS=json.loads((DATA/'w33_pass1341_atlas_standard_20_matrices.json').read_text())
ODIM=[1,2,1,1,3,2,1,2,1]

def span(vs,p):
 out=[]
 for v in vs:
  v=[int(x)%p for x in v]
  if old.rank(out+[v],p)>len(out):out.append(v)
 return out
def mul(x,y,m):
 z=[0]*26
 for i,a in enumerate(x):
  if a%m:
   for j,b in enumerate(y):
    if b%m:
     for k,c in enumerate(P[i,j]):z[k]=(z[k]+a*b*int(c))%m
 return z
def sub(x,y,m):return [(a-b)%m for a,b in zip(x,y)]
def scale(c,x,m):return [(c*a)%m for a in x]
def solve(A,b,p):
 M=[[int(x)%p for x in row]+[int(y)%p] for row,y in zip(A,b)];r=0;piv=[];n=len(M[0])-1
 for c in range(n):
  q=next((i for i in range(r,len(M)) if M[i][c]),None)
  if q is None:continue
  M[r],M[q]=M[q],M[r];iv=pow(M[r][c],-1,p);M[r]=[(iv*x)%p for x in M[r]]
  for i in range(len(M)):
   if i!=r and M[i][c]:
    z=M[i][c];M[i]=[(M[i][j]-z*M[r][j])%p for j in range(n+1)]
  piv.append(c);r+=1
 x=[0]*n
 for i,c in enumerate(piv):x[c]=M[i][n]
 return x
def inverse(x,m):
 L=sp.Matrix.hstack(*[sp.Matrix(mul(x,e,m)) for e in BASIS])
 return [int(v)%m for v in L.inv_mod(m)*sp.Matrix(ONE)]
def lift(x,m):
 for steps in range(20):
  err=sub(mul(x,x,m),x,m)
  if not any(err):return x,steps
  x=sub(x,mul(err,inverse(sub(scale(2,x,m),ONE,m),m),m),m)
 raise RuntimeError('Newton lift failed')
def qdata(p):
 rec=json.loads((DATA/'w33_pass1330_modular_quotient_maps.json').read_text())['records'][str(p)];images=[]
 for i in range(26):
  row=[]
  for b in rec['matrix_blocks']:row+=b['images'][i]
  row += [c[i] for c in rec['scalar_characters']];images.append([x%p for x in row])
 targets=[];off=0;qdim=len(images[0])
 for bi,b in enumerate(rec['matrix_blocks']):
  n=b['size']
  for r in range(n):
   t=[0]*qdim;t[off+r*n+r]=1;targets.append((t,bi))
  off+=n*n
 for si in range(len(rec['scalar_characters'])):
  t=[0]*qdim;t[off+si]=1;targets.append((t,len(rec['matrix_blocks'])+si))
 return images,targets
def primitive_system(p):
 images,targets=qdata(p);rem=ONE[:];out=[]
 for target,component in targets:
  x=solve(list(map(list,zip(*images))),target,p);x=mul(mul(rem,x,p),rem,p);x,s=lift(x,p)
  for e,_,_ in out:assert not any(mul(x,e,p)) and not any(mul(e,x,p))
  out.append((x,component,s));rem=sub(rem,x,p)
 assert not any(rem);return out
def corner(e,f,p):return len(span([mul(mul(e,b,p),f,p) for b in BASIS],p))
def leftdim(e,p):return len(span([mul(b,e,p) for b in BASIS],p))
def verify_cartan():
 for ps,rec in CERT['pass1340_modular_cartan'].items():
  p=int(ps);D=sp.Matrix(rec['decomposition_matrix']);assert (D.T*D).tolist()==rec['cartan_matrix']
  assert all(sum(a*b for a,b in zip(row,rec['modular_simple_dimensions']))==d for row,d in zip(rec['decomposition_matrix'],ODIM))
  lifts=primitive_system(p);reps=[];seen=set()
  for e,c,_ in lifts:
   if c not in seen:seen.add(c);reps.append(e)
  assert [[corner(e,f,p) for f in reps] for e in reps]==rec['cartan_matrix']
  assert [leftdim(e,p) for e in reps]==rec['projective_indecomposable_dimensions']
def matrix(raw):return sp.Matrix([[sp.Rational(x) for x in row] for row in raw])
def evalword(word,C,D):
 if word.startswith('('):w,n=word[1:].split(')^');n=int(n)
 else:w,n=word,1
 X=sp.eye(20)
 for ch in w:X=X*(C if ch=='c' else D)
 return X**n
WORDS=['(cdcdcddcdcdddcdd)^4','(cdd)^4','(cdcdcddcdcdddcdd)^2','(cdcdd)^4','(ccdcdddcddd)^2','(cddcdcdddcdd)^2','(cdd)^2','cdcdcddcdcdddcdd','(cd)^2','(cdcdd)^2','ccdcdddcddd','cddcdcdddcdd','(cdcdcdd)^2','d','cdcdd','(ccdcdcddcdcdddcddcddcdcdddcdd)^3','(cdcdddcdd)^3','(cdcdcdd)^3','dcdcdcdd','ccdcdcddcdcdddcddcddcdcdddcdd','dcdd','cdcdddcdd','cdd','cd','cdcdcdd']
def verify_atlas():
 C,D=matrix(ATLAS['matrices']['c']),matrix(ATLAS['matrices']['d']);I=sp.eye(20)
 assert C**2==I and D**9==I and (C*D)**10==I
 assert [int(sp.trace(evalword(w,C,D))) for w in WORDS]==ATLAS['class_trace_vector']
 payload={'c':ATLAS['matrices']['c'],'d':ATLAS['matrices']['d']}
 assert hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()==ATLAS['matrix_sha256']
def canon(c):
 c=tuple(c);n=len(c);return min([x[i:]+x[:i] for x in (c,tuple(reversed(c))) for i in range(n)])
def cycles(adj,n):
 out=set()
 for s in range(40):
  path=[s];used={s}
  def dfs():
   if len(path)==n:
    if path[-1] in adj[path[0]]:out.add(canon(path))
    return
   for z in adj[path[-1]]:
    if z not in used:used.add(z);path.append(z);dfs();path.pop();used.remove(z)
  dfs()
 return out
def verify_cycles():
 pts,gens=old.point_model();G=old.group(gens);adj=[[] for _ in pts]
 for i,x in enumerate(pts):
  for j,y in enumerate(pts):
   if i!=j and old.symp(x,y)==0:adj[i].append(j)
 for n,total,count in zip(range(3,7),[160,1740,18144,146880],[1,2,2,11]):
  unseen=cycles(adj,n);assert len(unseen)==total;sizes=[]
  while unseen:
   c=min(unseen);o={canon(tuple(g[x] for x in c)) for g in G};unseen-=o;sizes.append(len(o))
  assert len(sizes)==count
  frozen=CERT['pass1342_minimal_cycle_idempotent_selector']['cycle_orbits'][str(n)]
  assert sorted(sizes)==sorted(row['orbit_size'] for row in frozen['orbits'])
  assert sorted(51840//size for size in sizes)==sorted(row['stabilizer_order'] for row in frozen['orbits'])
def main():
 section=sys.argv[1] if len(sys.argv)>1 else None
 table={'cartan':verify_cartan,'atlas':verify_atlas,'cycles':verify_cycles}
 if section not in table:raise SystemExit('usage: script.py cartan|atlas|cycles')
 table[section]();assert CERT['status']=='PASS' and all(CERT['checks'].values())
 print(f'PASS 1340-1344 {section} verifier')
if __name__=='__main__':main()
