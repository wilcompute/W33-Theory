#!/usr/bin/env python3
"""17-term exact compiler for the controlled determinant gate.

The certified H1 controller uses the 10-coordinate sp4(F3) basis frozen by
w33_h1_adjoint_nonlinear_invariants.py.  In those coordinates x0,...,x9,

X =
[[2x4,2x8,x0,x1],
 [2x5,2x9,x1,x2],
 [ x3, x6,x4,x5],
 [ x6, x7,x8,x9]] mod 3.

Expanding det(X) over F3 gives exactly 17 nonzero quartic monomials. Therefore

 U_det = sum_x |x><x| tensor z^det(X)

factorizes into 17 mutually commuting diagonal monomial-phase primitives
P_m(c): |x,r> -> omega^(r*c*m(x)) |x,r>, c=+/-1.

This is an exact circuit-level reduction of the nonlinear target.  It does not
claim that the current Holonet hardware already supplies P_m for arbitrary
quartic monomials.  Qutrit shelving/cross-Kerr and high-dimensional controlled-
phase experiments are implementation templates, not certificates for this
specific gate.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_controlled_det_17term_compiler.json'

TERMS=[
(+1,(1,0,1,1,0,0,0,1,0,0)),
(-1,(1,0,1,0,0,0,2,0,0,0)),
(+1,(1,0,0,1,0,0,0,0,0,2)),
(+1,(1,0,0,0,0,2,0,1,0,0)),
(+1,(1,0,0,0,0,1,1,0,0,1)),
(-1,(0,2,0,1,0,0,0,1,0,0)),
(+1,(0,2,0,0,0,0,2,0,0,0)),
(+1,(0,1,0,1,0,0,0,0,1,1)),
(+1,(0,1,0,0,1,1,0,1,0,0)),
(-1,(0,1,0,0,1,0,1,0,0,1)),
(-1,(0,1,0,0,0,1,1,0,1,0)),
(+1,(0,0,1,1,0,0,0,0,2,0)),
(+1,(0,0,1,0,2,0,0,1,0,0)),
(+1,(0,0,1,0,1,0,1,0,1,0)),
(+1,(0,0,0,0,2,0,0,0,0,2)),
(+1,(0,0,0,0,1,1,0,0,1,1)),
(+1,(0,0,0,0,0,2,0,0,2,0)),
]
def det4(A):
    A=[list(row) for row in A];d=1
    for c in range(4):
        p=next((i for i in range(c,4) if A[i][c]%3),None)
        if p is None:return 0
        if p!=c:A[c],A[p]=A[p],A[c];d=-d
        pv=A[c][c]%3;d=d*pv%3;iv=pow(pv,-1,3)
        for i in range(c+1,4):
            if A[i][c]%3:
                f=A[i][c]*iv%3
                A[i]=[(A[i][j]-f*A[c][j])%3 for j in range(4)]
    return d%3
def matrix(x):
    return [[2*x[4],2*x[8],x[0],x[1]],
            [2*x[5],2*x[9],x[1],x[2]],
            [x[3],x[6],x[4],x[5]],
            [x[6],x[7],x[8],x[9]]]
def poly(x):
    z=0
    for c,e in TERMS:
        m=1
        for i,a in enumerate(e):m=m*pow(x[i],a,3)%3
        z=(z+c*m)%3
    return z
def fmt(c,e):
    fs=[]
    for i,a in enumerate(e):
        if a==1:fs.append(f'x{i}')
        elif a==2:fs.append(f'x{i}^2')
    return ('+' if c==1 else '-')+' '.join(fs)

def main(write=True):
    census=[0,0,0]
    for x in itertools.product(range(3),repeat=10):
        a=det4(matrix(x));b=poly(x)
        assert a==b
        census[a]+=1
    assert sum(census)==3**10 and len(TERMS)==17
    out={'schema':'w33.controlled_det_17term_compiler.v1','status':'PASS_EXACT_COMPILER_PHYSICAL_PRIMITIVE_OPEN',
      'controller_matrix':'[[2x4,2x8,x0,x1],[2x5,2x9,x1,x2],[x3,x6,x4,x5],[x6,x7,x8,x9]] mod3',
      'determinant_polynomial':[
          {'coefficient_mod3':c%3,'coefficient_signed':c,'exponents':list(e),'monomial':fmt(c,e)} for c,e in TERMS],
      'nonzero_monomials':17,
      'all_59049_controller_points_verified':True,
      'det_value_census':{'0':census[0],'1':census[1],'2':census[2]},
      'gate_factorization':'U_det = product over 17 commuting primitives P_m(c), P_m(c)|x,r>=omega^(r c m(x))|x,r>',
      'resource_upper_bound':{'quartic_or_lower_phase_primitives':17,'ancilla_for_truth_table':0,
                              'commuting_layers_if_parallel_hardware_supports_all_monomials':1},
      'classical_controller_fast_path':'If X is measured/classical, compute det(X) digitally and apply z^det(X); this does not realize coherent non-Clifford controller dynamics.',
      'coherent_physical_route':'Implement the 17 state-dependent monomial phases with multilevel controlled-phase primitives (for example shelving/conditional-Stark/cross-Kerr style interactions), then multiply them. Existing experiments motivate the primitive but do not certify this exact W33 realization.',
      'single_photon_boundary':'The present deterministic time-frequency SUM compiler does not by itself provide quartic monomial phases. A fully single-photon deterministic 17-term implementation remains open.',
      'checks':{'17_terms':True,'exhaustive_3pow10_identity':True,'all_terms_degree4':all(sum(e)==4 for c,e in TERMS)}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
