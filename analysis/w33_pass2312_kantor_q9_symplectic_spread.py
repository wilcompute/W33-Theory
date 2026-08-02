#!/usr/bin/env python3
"""Pass 2312: exact regular/Kantor symplectic-spread comparison in PG(3,9)."""
from __future__ import annotations
import hashlib,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass2312_kantor_q9_symplectic_spread.json'
EXPECTED='a8c878b2a98ac7592fcbb54093810ae73e8c467ebecca0d3dc8c9dfc70147eb3'
def add(x,y):return ((x%3+y%3)%3)+3*((x//3+y//3)%3)
def neg(x):return (-x%3)+3*((-(x//3))%3)
def sub(x,y):return add(x,neg(y))
def mul(x,y):
 a,b=x%3,x//3;c,d=y%3,y//3
 return (a*c+2*b*d)%3+3*((a*d+b*c)%3)
def pw(x,n):
 r=1
 while n:
  if n&1:r=mul(r,x)
  x=mul(x,x);n//=2
 return r
def inv(x):assert x;return pw(x,7)
def smul(a,v):return tuple(mul(a,x) for x in v)
def vadd(v,w):return tuple(add(a,b) for a,b in zip(v,w))
def norm(v):
 for x in v:
  if x:return tuple(mul(inv(x),y) for y in v)
 raise ValueError
def line(v,w):
 return tuple(sorted({norm(vadd(smul(a,v),smul(b,w))) for a in range(9) for b in range(9) if a or b}))
def spread(g):
 z=[line((0,0,1,0),(0,0,0,1))]
 for x in range(9):
  for y in range(9):z.append(line((0,1,x,y),(1,0,neg(y),g(x,y))))
 return tuple(sorted(set(z)))
def beta(v,w):return add(sub(mul(v[0],w[3]),mul(v[3],w[0])),sub(mul(v[2],w[1]),mul(v[1],w[2])))
def verify(S):
 seen=set()
 for L in S:
  assert len(L)==10 and not seen.intersection(L)
  assert all(beta(x,y)==0 for x,y in itertools.combinations(L,2))
  seen.update(L)
 return len(seen)
def sh(S):return hashlib.sha256(json.dumps([[list(p) for p in L] for L in S],separators=(',',':')).encode()).hexdigest()
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build():
 n=4;squares={mul(x,x) for x in range(1,9)};assert n not in squares
 R=spread(lambda x,y:neg(mul(n,x)));K=spread(lambda x,y:neg(mul(n,pw(x,3))))
 fixed=[x for x in range(9) if pw(x,3)==x];common=len(set(R)&set(K))
 d={'schema':'w33.pass2312.kantor_q9_symplectic_spread.v1','status':'PASS_WITH_SINGLE_MIXED_PAIR_NOT_ORBIT_CLASSIFICATION',
 'field':{'name':'GF(9)=GF(3)[u]/(u^2+1)','encoding':'a+3b represents a+b*u','u_squared':2,'nonsquare_n':'1+u','nonsquare_encoding':4,'kantor_exponent':3},
 'construction':{'ambient':'PG(3,9)','line_at_infinity':'span((0,0,1,0),(0,0,0,1))','affine_lines':'span((0,1,x,y),(1,0,-y,g(x,y))) for x,y in GF(9)','regular_function':'g(x,y)=-n*x','kantor_function':'g(x,y)=-n*x^3','symplectic_form':'beta(v,w)=v0*w3-v3*w0-v1*w2+v2*w1'},
 'verification':{'projective_points':820,'regular_lines':len(R),'kantor_lines':len(K),'points_per_line':10,'regular_union_points':verify(R),'kantor_union_points':verify(K),'pairwise_disjoint_within_each_spread':True,'all_lines_totally_isotropic':True,'regular_spread_sha256':sh(R),'kantor_spread_sha256':sh(K)},
 'intersection':{'common_lines':common,'expected_from_fixed_field':'1 + 9*3 = 28','fixed_points_of_frobenius_x3':fixed,'explanation':'The two affine lines with the same (x,y) coincide exactly when x^3=x. This holds for the three elements of the fixed subfield GF(3); y is arbitrary, giving 27 affine common lines, plus the common line at infinity.','not_in_regular_family_values':{'one':1,'qplus1':10}},
 'checks':{'gf9_nonzero_inverses':all(mul(x,inv(x))==1 for x in range(1,9)),'n_is_nonsquare':n not in squares,'both_82_lines':len(R)==len(K)==82,'both_partition_pg3_points':verify(R)==verify(K)==820,'both_symplectic':True,'frobenius_fixed_field_is_gf3':fixed==[0,1,2],'intersection_28':common==28,'intersection_not_1_or_10':common not in (1,10)},
 'theorem':'The regular symplectic spread g=-n x and the Kantor symplectic spread g=-n x^3 in PG(3,9) share exactly 28 lines. Therefore the 1-or-(q+1) intersection rigidity of the regular Desarguesian orbit does not extend to arbitrary symplectic spreads.','boundary':'This is one explicit regular/Kantor mixed pair at q=9. It does not classify the Kantor orbit, intersections among two Kantor spreads, or all non-Desarguesian symplectic spreads.'}
 assert all(d['checks'].values());d['sha256_without_hash_field']=digest(d);return d
def main():
 d=build();assert d['sha256_without_hash_field']==EXPECTED;assert d==json.loads(OUT.read_text())
 print(json.dumps({'status':d['status'],'certificate':EXPECTED,'common_lines':28},sort_keys=True))
if __name__=='__main__':main()
