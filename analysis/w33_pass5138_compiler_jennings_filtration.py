#!/usr/bin/env python3
"""Pass5138: the all-q state/program compiler is a filtered group-algebra isomorphism.

Write U in state coordinates x0(a)x1(b)x2(c)x3(d), and in program coordinates
x1(b)x2(C)x3(D)x0(a).  Pass5133's polynomial compiler is exactly the change of
coordinates between these two multiplication laws.  Therefore its linear
extension to k[U] preserves the augmentation ideal and every power J^r,
hence the complete Jennings filtration and associated graded module.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import FF
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5138_COMPILER_JENNINGS_FILTRATION.json'

def sub(F,a,b):return F.add(a,F.neg(b))
def add3(F,a,b,c):return F.add(F.add(a,b),c)

def state_mul(F,x,y):
    a,b,c,d=x;A,B,C,D=y
    return (F.add(a,A),F.add(b,B),sub(F,F.add(c,C),F.mul(A,b)),
            add3(F,d,D,F.add(F.mul(F.mul(A,A),b),F.neg(F.mul(F.add(A,A),c)))))

def phi(F,x):
    a,b,c,d=x
    C=F.add(c,F.mul(a,b))
    D=add3(F,d,F.mul(F.add(a,a),c),F.mul(F.mul(a,a),b))
    return (a,b,C,D)

def invphi(F,x):
    a,b,C,D=x;c=sub(F,C,F.mul(a,b))
    d=F.add(sub(F,D,F.mul(F.add(a,a),C)),F.mul(F.mul(a,a),b))
    return (a,b,c,d)

def program_mul(F,x,y):
    a,b,C,D=x;A,B,E,H=y
    return (F.add(a,A),F.add(b,B),add3(F,C,E,F.mul(a,B)),
            add3(F,D,H,F.add(F.mul(F.add(a,a),E),F.mul(F.mul(a,a),B))))

def anchor(q):
    F=FF(q);els=list(itertools.product(range(q),repeat=4));checked=0
    for x in els:
      assert invphi(F,phi(F,x))==x
      for y in els:
        lhs=phi(F,state_mul(F,x,y));rhs=program_mul(F,phi(F,x),phi(F,y))
        assert lhs==rhs,(q,x,y,lhs,rhs);checked+=1
    return {'q':q,'states':q**4,'ordered_products_checked':checked,'compiler_bijection':True,'multiplication_intertwined':True}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5138,'status':'THEOREM_ALL_Q_FILTERED_GROUP_ALGEBRA_COMPILER',
      'state_law':'(a,b,c,d)*(A,B,C,D)=(a+A,b+B,c+C-Ab,d+D-2Ac+A^2b)',
      'compiler':'Phi(a,b,c,d)=(a,b,c+ab,d+2ac+a^2b)',
      'program_law':'(a,b,C,D) o (A,B,E,H)=(a+A,b+B,C+E+aB,D+H+2aE+a^2B)',
      'anchors':A,
      'filtered_module_theorem':'Phi is a group isomorphism between the two coordinate laws. Its k-linear extension sends each basis element representing u to the basis element representing the same u, hence sends the augmentation ideal J to J and J^r to J^r for every r. Therefore it induces an isomorphism on every Jennings layer J^r/J^(r+1).',
      'connection':'The Pass5122 root-height/Jennings protected-memory profile is coordinate-independent under the Pass5133 state/program compiler.',
      'boundary':'This is an algebraic filtration-preservation theorem; it does not assign physical latency or error rates to the compiler.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
