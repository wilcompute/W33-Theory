#!/usr/bin/env python3
"""Pass 1352: solve the exact rational conjugacy between Repsn and carrier models."""
from __future__ import annotations
from pathlib import Path
import json,hashlib,math
from functools import reduce
from math import gcd
import sympy as sp
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
IN=DATA/'w33_pass1352_repsn_degree20_matrices.json'
FROZEN=DATA/'w33_pass1341_atlas_standard_20_matrices.json'
OUT=DATA/'w33_pass1352_atlas_carrier_conjugacy.json'

def pair_matrix(raw):return sp.Matrix([[sp.Rational(a,b) for a,b in row] for row in raw])
def str_matrix(M):return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
def lcm(a,b):return abs(a*b)//math.gcd(a,b) if a and b else 0

def solve_intertwiner(A,B,C,D):
    n=A.rows;I=sp.eye(n)
    K=(sp.kronecker_product(I,A)-sp.kronecker_product(C.T,I)).col_join(
      sp.kronecker_product(I,B)-sp.kronecker_product(D.T,I))
    ns=K.nullspace()
    assert len(ns)==1, f'intertwiner dimension {len(ns)}'
    v=ns[0]
    X=sp.Matrix(n,n,lambda i,j:v[j*n+i])
    assert A*X==X*C and B*X==X*D and X.det()!=0
    return X,len(ns)

def primitive_integer(M):
    dens=[sp.Rational(x).q for x in M];den=reduce(lcm,dens,1)
    ints=[int(sp.Rational(x)*den) for x in M];g=reduce(gcd,[abs(x) for x in ints if x])
    ints=[x//g for x in ints]
    if next(x for x in ints if x)<0:ints=[-x for x in ints]
    return sp.Matrix(M.rows,M.cols,ints),sp.Rational(g,den)

def main(write=True):
    rep=json.loads(IN.read_text());fr=json.loads(FROZEN.read_text())
    A=pair_matrix(rep['matrices']['c']);B=pair_matrix(rep['matrices']['d'])
    C=sp.Matrix([[sp.Rational(x) for x in row] for row in fr['matrices']['c']])
    D=sp.Matrix([[sp.Rational(x) for x in row] for row in fr['matrices']['d']])
    X,dim=solve_intertwiner(A,B,C,D);Xi,scale=primitive_integer(X)
    assert A*Xi==Xi*C and B*Xi==Xi*D and Xi.det()!=0
    raw=';'.join(','.join(str(Xi[i,j]) for j in range(20)) for i in range(20)).encode()
    result={'schema':'w33.pass1352.atlas_carrier_conjugacy.v1','status':'PASS','group':'U4(2).2',
      'repsn_character_position':11,'generator_traces':[10,-1],'hom_space_dimension':dim,
      'convention':'A_repsn X = X A_carrier for both standard generators c,d',
      'integer_intertwiner':str_matrix(Xi),'integer_intertwiner_determinant':str(Xi.det()),
      'rational_normalization_scale_X_equals_scale_times_integer':str(1/scale),
      'integer_intertwiner_sha256':hashlib.sha256(raw).hexdigest(),
      'checks':{'c_intertwines':True,'d_intertwines':True,'invertible':True,'hom_dimension_one':True}}
    if write:OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result
if __name__=='__main__':
    r=main();print(json.dumps({k:r[k] for k in ['status','hom_space_dimension','integer_intertwiner_determinant','integer_intertwiner_sha256']},indent=2))
