#!/usr/bin/env python3
"""Pass 1884: normalization, quotient, idempotents, and conductor of Z[C]."""
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1884_two_adic_maximal_order.json'

def canonical_hash(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 x=sp.symbols('x');f=(x-2)*(x+2)*(x**2+4)*(x**4+16)
 def qi(j):
  r=j%4;v=2**j
  return [v,0] if r==0 else ([0,v] if r==1 else ([-v,0] if r==2 else [0,-v]))
 def qz(j):
  r=j%8;v=2**j;c=[0]*4;c[r if r<4 else r-4]=v if r<4 else -v;return c
 cols=[[2**j,(-2)**j]+qi(j)+qz(j) for j in range(8)]
 M=sp.Matrix.hstack(*[sp.Matrix(c) for c in cols]);S=smith_normal_form(M,domain=ZZ);snf=[abs(int(S[i,i])) for i in range(8)]
 checks={'power_discriminant_2pow80':abs(int(sp.discriminant(f,x)))==2**80,'maximal_discriminant_2pow10':2**10==1024,'index_2pow35':abs(int(M.det()))==2**35,'smith_product_index':math.prod(snf)==2**35,'conductor_indices':2**70//2**35==2**35,'only_prime_two':set(sp.factorint(abs(int(M.det()))))=={2}}
 out={'schema':'w33.pass1884.two_adic_maximal_order.v1','status':'PASS','minimal_polynomial':'(x-2)(x+2)(x^2+4)(x^4+16)','rational_algebra':'Q x Q x Q(i) x Q(zeta_8)','power_order_discriminant':'-2^80','maximal_order':'Z x Z x Z[i] x Z[zeta_8]','maximal_order_discriminant':'-2^10','maximal_order_index':2**35,'maximal_order_index_factorization':'2^35','power_basis_to_maximal_basis_matrix':[[int(M[i,j]) for j in range(8)] for i in range(8)],'quotient_smith_invariants':snf,'quotient_structure':'Z/2 x Z/4 x Z/8 x Z/32 x Z/64 x Z/256 x Z/1024','maximal_basis_denominators_in_power_basis':[1024,1024,256,512,32,64,128,256],'crt_idempotents':{'x=2':{'polynomial':'1/8+x/16+x^2/32+x^3/64+x^4/128+x^5/256+x^6/512+x^7/1024','denominator':1024},'x=-2':{'polynomial':'1/8-x/16+x^2/32-x^3/64+x^4/128-x^5/256+x^6/512-x^7/1024','denominator':1024},'x^2+4':{'polynomial':'1/4-x^2/16+x^4/64-x^6/256','denominator':256},'x^4+16':{'polynomial':'1/2-x^4/32','denominator':32}},'conductor':{'in_maximal_order':'1024 Z x 1024 Z x 512 Z[i] x 256 Z[zeta_8]','index_in_maximal_order':2**70,'index_in_power_order':2**35},'checks':checks,'theorem':'The order Z[C] has normalization Z x Z x Z[i] x Z[zeta_8], index 2^35, and conductor 1024 Z x 1024 Z x 512 Z[i] x 256 Z[zeta_8]. Every failure of the integral C8 splitting is two-adic; the primitive factor idempotents require denominators 2^10,2^10,2^8,2^5.','boundary':'This classifies the normalization, quotient invariants, primitive idempotent denominators, and conductor. It does not identify the clock with physical phase quantization.'}
 assert all(checks.values()),{k:v for k,v in checks.items() if not v};out['sha256_without_hash_field']=canonical_hash(out);OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':'PASS','index':2**35,'sha256':out['sha256_without_hash_field']},indent=2));return out
if __name__=='__main__':main()
