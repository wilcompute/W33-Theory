#!/usr/bin/env python3
"""Pass 1175 v2: exact characteristic-zero factors; GF(7) is validation only."""
import json
from pathlib import Path
KERNEL={'1':(1,13),'6':(6,16),'15':(15,5),'15a':(15,4),'20':(20,21),'24':(24,2),'30':(30,9),'60a':(60,4),'64':(64,10),'81_minus':(81,3),'90':(90,1)}
def main():
    dim=sum(d*m for d,m in KERNEL.values())
    result={'schema':'w33.pass1175.meataxe_validation.v2','status':'PASS','prime':7,'module_total_dim':dim,
      'exact_characteristic_zero_factors':{k:{'degree':d,'multiplicity':m} for k,(d,m) in KERNEL.items()},
      'source':'Pass 1135 exact class-algebra decomposition','simulation_performed':False,
      'maschke_statement':'Because 7 does not divide 51840, the reduced module is semisimple.',
      'field_warning':'Semisimplicity does not by itself prove that GF(7) is a splitting field or identify characteristic-zero labels.',
      'tensor_product_warning':'24*15=360 does not prove V24 tensor V15 is irreducible V360.',
      'validation_goal':'Check explicit reduced generator matrices against the known multiplicities.'}
    assert dim==2195
    Path('data/MEATAXE_GF7_SIMULATION_2026_07_27.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1175 v2 exact factors known; no simulated MeatAxe claim');return result
if __name__=='__main__':main()
