#!/usr/bin/env python3
"""Pass 1178 v2: arithmetic candidates only, using exact W(E6) degrees."""
import json
from pathlib import Path
WE6_DIMS=[1,1,6,6,10,15,15,15,15,20,20,20,24,24,30,30,60,60,60,64,64,80,81,81,90]
TARGET=2600
def main():
    result={'schema':'w33.pass1178.sym3_v24_arithmetic_candidates.v2','status':'PASS','target':TARGET,
      'exact_degree_vocabulary':WE6_DIMS,'sum_of_squares':sum(d*d for d in WE6_DIMS),'plethysm_decomposition_computed':False,
      'required_input':'Character values of the selected 24-dimensional irrep and Adams operations.',
      'scope_barrier':'A dimension partition is not a plethysm or Clebsch--Gordan decomposition.'}
    assert result['sum_of_squares']==51840
    Path('data/SYM3_V24_PLETHYSM_SEARCH_2026_07_27.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1178 v2 arithmetic-only plethysm boundary');return result
if __name__=='__main__':main()
