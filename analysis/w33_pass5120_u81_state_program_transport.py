#!/usr/bin/env python3
"""Pass5120: explicit polynomial state/root/program coordinates in U81."""
from __future__ import annotations
import itertools,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5120_U81_STATE_PROGRAM_TRANSPORT.json'

def E(i,j):
    M=sp.zeros(4);M[i,j]=1;return M
I=sp.eye(4)
X0=E(0,1)-E(3,2);X1=E(1,3);X2=E(0,3)+E(1,2);X3=E(0,2)
def x(X,t):return I+t*X

def main():
    a,b,c,d=sp.symbols('a b c d')
    root=x(X0,a)*x(X1,b)*x(X2,c)*x(X3,d)
    bp=b;cp=c+a*b;dp=d+2*a*c+a*a*b
    program=x(X1,bp)*x(X2,cp)*x(X3,dp)*x(X0,a)
    assert sp.simplify(root-program)==sp.zeros(4)
    state=x(X0,a)*x(X2,c)*x(X3,d)*x(X1,b)
    assert sp.simplify(root-state)==sp.zeros(4)
    # Exact q=3 bijection of both coordinate systems onto all 81 matrices.
    def key(M):return tuple(int(z)%3 for z in M)
    root_seen={};prog_seen={};state_seen={}
    for A,B,C,D in itertools.product(range(3),repeat=4):
        R=x(X0,A)*x(X1,B)*x(X2,C)*x(X3,D)
        root_seen[key(R)]=(A,B,C,D)
        state_seen[key(x(X0,A)*x(X2,C)*x(X3,D)*x(X1,B))]=(B,A,C,D)
        CP=(C+A*B)%3;DP=(D+2*A*C+A*A*B)%3
        prog_seen[key(x(X1,B)*x(X2,CP)*x(X3,DP)*x(X0,A))]=(A,B,CP,DP)
    assert len(root_seen)==len(state_seen)==len(prog_seen)==81
    assert set(root_seen)==set(state_seen)==set(prog_seen)
    out={'pass':5120,'status':'THEOREM_EXPLICIT_U81_STATE_ROOT_PROGRAM_TRANSPORT',
         'root_normal_form':'u(a,b,c,d)=x0(a)x1(b)x2(c)x3(d)',
         'state_factorization':'u=[x0(a)x2(c)x3(d)] x1(b)',
         'state_coordinates':['b','a','c','d'],
         'program_factorization':'u=[x1(b)x2(c+ab)x3(d+2ac+a^2b)] x0(a)',
         'program_coordinates':['a','b','c+ab','d+2ac+a^2 b'],
         'symbolic_matrix_identity':True,'q3_elements':81,'q3_bijection':True,
         'regular_basis_transport':'Order the delta_u basis of F3[U81] by either state cosets H27*x1(b) or program cosets F3^3*x0(a). The displayed polynomial coordinate change gives the exact permutation between the two orderings.',
         'relation_to_Pass5105':'Pass5105 proves protected H1(F3) is one regular F3[U81] module, so this is an explicit coordinate transport on the canonical regular controller model.',
         'boundary':'The formula is an exact U81/group-algebra compiler. It is not asserted to equal BT865 independently seeded chain-level bases without an additional seed-to-regular-basis comparison.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
