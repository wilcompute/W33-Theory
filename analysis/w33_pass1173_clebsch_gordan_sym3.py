#!/usr/bin/env python3
"""Pass 1173 v2: dimension census only; no Clebsch--Gordan claim."""
import json
from math import comb
from pathlib import Path
WE6_IRREP_DIMS=[1,1,6,6,10,15,15,15,15,20,20,20,24,24,30,30,60,60,60,64,64,80,81,81,90]
def main():
    terms={'Sym3_V24':comb(26,3),'Sym2_V24_x_V15':comb(25,2)*15,'Sym2_V15_x_V24':comb(16,2)*24}
    result={'schema':'w33.pass1173.sym3_dimension_census.v2','status':'PASS','exact_we6_irrep_degrees':WE6_IRREP_DIMS,
      'degree_square_sum':sum(d*d for d in WE6_IRREP_DIMS),'sym3_dominant_terms':terms,
      'steinberg_packet':{'dimension':243,'exact_kernel_multiplicity':'3*81_minus from Pass 1135'},
      'residual_1952':{'dimension':1952,'exact_decomposition_source':'Pass 1135','commutant_dimension':1109},
      'scope_barrier':'Dimension partitions are not Clebsch--Gordan coefficients. No plethysm decomposition is asserted without character values.',
      'superseded_claims':['unique 81-dimensional W(E6) irrep','prime-factor obstruction determines module structure']}
    assert result['degree_square_sum']==51840 and terms['Sym3_V24']==2600
    Path('data/CLEBSCH_GORDAN_SYM3_2026_07_27.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1173 v2 dimension census only');return result
if __name__=='__main__':main()
