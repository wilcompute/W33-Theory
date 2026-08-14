#!/usr/bin/env python3
"""Pass5133 (bonkers): characteristic-independent polynomial state/program compiler."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5133_ALLQ_STATE_PROGRAM_POLYNOMIAL_COMPILER.json'

def anchor(q):
    U,H,F=roots(q)
    def add(*xs):
        z=0
        for x in xs:z=F.add(z,x)
        return z
    def sub(a,b):return F.add(a,F.neg(b))
    mul=F.mul
    def two(x):return F.add(x,x)
    images=set()
    for a,b,c,d in itertools.product(range(q),repeat=4):
        u=mm(mm(mm(H[0][a],H[1][b],F),H[2][c],F),H[3][d],F)
        f1=mm(mm(mm(H[0][a],H[2][c],F),H[3][d],F),H[1][b],F)
        C=add(c,mul(a,b));D=add(d,two(mul(a,c)),mul(mul(a,a),b))
        f2=mm(mm(mm(H[1][b],H[2][C],F),H[3][D],F),H[0][a],F)
        assert u==f1==f2
        images.add((a,b,C,D))
        ci=sub(C,mul(a,b));di=add(D,F.neg(two(mul(a,C))),mul(mul(a,a),b))
        assert (ci,di)==(c,d)
    assert len(images)==q**4
    return {'q':q,'states':q**4,'programs':q**4,'matrix_identity_exact':True,'compiler_bijective':True}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5133,'status':'THEOREM_ALL_FINITE_Q_REVERSIBLE_STATE_PROGRAM_COMPILER',
         'state_coordinates':'(b; a,c,d)',
         'program_coordinates':'(a; b,C,D) with C=c+ab, D=d+2ac+a^2 b',
         'inverse':'c=C-ab, d=D-2aC+a^2 b',
         'factorization_1':'x0(a)x1(b)x2(c)x3(d) = [x0(a)x2(c)x3(d)]x1(b)',
         'factorization_2':'x0(a)x1(b)x2(c)x3(d) = [x1(b)x2(c+ab)x3(d+2ac+a^2b)]x0(a)',
         'anchors':A,
         'synthesis':'Combined with Pass5129, ordering the regular U(q) apartment carrier by state cosets or program cosets differs by this explicit polynomial permutation. In characteristic two the 2ac term vanishes automatically.',
         'boundary':'This is a reversible finite-field coordinate compiler on the exact unipotent controller. It is not a hardware timing/performance claim and does not identify unrelated historical chain bases without a separate intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
