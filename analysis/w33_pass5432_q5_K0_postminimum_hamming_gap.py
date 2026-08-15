#!/usr/bin/env python3
"""Pass5432: q=5 zero-footprint residual post-minimum Hamming gap.

Inputs already proved in the repo:
- Pass5262: K0 has P-block distance 25.
- Pass5259/5268: every nonzero local even P-block word has Hamming weight >=40.
- Pass5284: the complete K0 block-minimum shell (support size 25) consists of
  exactly 2340 words, all of Hamming weight 1000.

Because the 325 P-components partition the apartment coordinates, global weight
is the sum of local block weights.  Hence any K0 word outside the 2340-word
minimum shell has block support >=26 and therefore Hamming weight >=26*40=1040.
Thus K0=[73125,560,1000]_2 has a certified open interval in its weight spectrum:
there are no nonzero weights 1001,...,1039.  This is a lower bound on the second
nonzero weight, not a claim that weight 1040 is attained.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5432_Q5_K0_POSTMINIMUM_HAMMING_GAP.json'

def main():
    block_distance=25;local_even_min=40;minimum=block_distance*local_even_min
    next_support=26;lower=next_support*local_even_min
    assert minimum==1000 and lower==1040
    out={
      'pass':5432,'status':'THEOREM_Q5_K0_POSTMINIMUM_HAMMING_GAP',
      'code':'K0=[73125,560,1000]_2',
      'inputs':{
        'Pass5262':'P-block distance(K0)=25',
        'Pass5259_5268':'every nonzero local even P-component restriction has Hamming weight >=40',
        'Pass5284':'all support-25 K0 words are exactly 2340 chamber-star differences and all have Hamming weight1000'},
      'minimum_shell_size':2340,
      'minimum_weight':1000,
      'postminimum_support_lower_bound':26,
      'second_nonzero_weight_lower_bound':1040,
      'forbidden_weight_interval':[1001,1039],
      'gap_width':39,
      'proof':'Any word not in the complete support-25 shell has at least26 active disjoint P blocks; each contributes at least40 apartment coordinates.',
      'boundary':'No weight-1040 witness is asserted. The theorem proves d_2(K0)>=1040, not equality.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
