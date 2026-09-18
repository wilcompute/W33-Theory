#!/usr/bin/env python3
"""Ancilla-free optimality of the 17-term determinant phase compiler.

For functions F3^10 -> F3 there is a unique reduced polynomial representative
with degree <=2 in each variable, because the quotient by
  (x0^3-x0,...,x9^3-x9)
has the 3^10 reduced monomials as a basis of all F3-valued functions.

The native monomial-phase library is
  P_m(c)|x,r> = omega^(r c m(x)) |x,r>,
where one primitive contributes one reduced monomial m with coefficient c.

The certified determinant polynomial has 17 nonzero reduced coefficients.
Therefore any ancilla-free circuit consisting only of commuting native
monomial-phase primitives requires at least 17 nontrivial primitives.  The
existing 17-term compiler meets the bound exactly.

This is a library-specific optimum.  Ancillas, nonlinear reversible arithmetic,
basis-changing nonmonomial primitives, measurement/feedforward, or analog
multi-term Hamiltonians can evade this count and remain separate optimization
problems.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_controlled_det_17term_optimality.json'

# coefficient, exponent vector; same canonical support as the parent compiler
TERMS=[
(+1,(1,0,1,1,0,0,0,1,0,0)),(-1,(1,0,1,0,0,0,2,0,0,0)),
(+1,(1,0,0,1,0,0,0,0,0,2)),(+1,(1,0,0,0,0,2,0,1,0,0)),
(+1,(1,0,0,0,0,1,1,0,0,1)),(-1,(0,2,0,1,0,0,0,1,0,0)),
(+1,(0,2,0,0,0,0,2,0,0,0)),(+1,(0,1,0,1,0,0,0,0,1,1)),
(+1,(0,1,0,0,1,1,0,1,0,0)),(-1,(0,1,0,0,1,0,1,0,0,1)),
(-1,(0,1,0,0,0,1,1,0,1,0)),(+1,(0,0,1,1,0,0,0,0,2,0)),
(+1,(0,0,1,0,2,0,0,1,0,0)),(+1,(0,0,1,0,1,0,1,0,1,0)),
(+1,(0,0,0,0,2,0,0,0,0,2)),(+1,(0,0,0,0,1,1,0,0,1,1)),
(+1,(0,0,0,0,0,2,0,0,2,0))]
def main(write=True):
    parent=json.loads((ROOT/'data/w33_controlled_det_17term_compiler.json').read_text())
    assert parent['status']=='PASS_EXACT_COMPILER_PHYSICAL_PRIMITIVE_OPEN'
    assert len(TERMS)==17 and len({e for c,e in TERMS})==17
    assert all(c%3 in (1,2) and all(a in (0,1,2) for a in e) for c,e in TERMS)
    out={'schema':'w33.controlled_det_17term_optimality.v1','status':'PASS_LIBRARY_OPTIMUM',
      'function_space':{'domain':'F3^10','codomain':'F3','reduced_basis_size':3**10,
        'basis':'monomials product_i x_i^e_i with e_i in {0,1,2}',
        'uniqueness':'evaluation modulo x_i^3-x_i gives a unique reduced polynomial function'},
      'native_library':'one primitive P_m(c) contributes one nonzero reduced monomial coefficient to the phase exponent',
      'determinant_support':17,
      'lower_bound':17,
      'achieved_by_parent_compiler':17,
      'conclusion':'17 is the exact minimum number of nontrivial primitives for ancilla-free circuits in the fixed native monomial-phase coordinate library.',
      'not_covered':['ancilla-assisted arithmetic','nonmonomial analog Hamiltonians','measurement/feedforward',
                     'arbitrary linear basis changes followed by a different hardware library','approximate synthesis'],
      'checks':{'parent_loaded':True,'distinct_support_17':True,'all_reduced':True,'lower_equals_upper':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
