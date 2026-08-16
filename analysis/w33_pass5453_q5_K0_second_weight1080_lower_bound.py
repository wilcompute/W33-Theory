#!/usr/bin/env python3
"""Pass5453: q=5 K0 post-minimum Hamming gap strengthens to 1080.

Inputs:
- Pass5262: K0 block distance is25.
- Pass5284: every block-support-25 K0 word is in the complete2340-word minimum
  shell and has Hamming weight1000.
- Pass5268: every nonzero local even P-block restriction has Hamming weight>=40.
- Pass5452: no nonzero K0 word has block support26.

Therefore any K0 word outside the complete minimum shell has at least27 active
P-blocks, hence Hamming weight at least27*40=1080.  Thus K0=[73125,560,1000]_2
has no nonzero weights1001,...,1079.

No weight1080 witness is asserted; the exact second nonzero Hamming weight remains
open pending block-support27/local-syndrome analysis.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5453_Q5_K0_SECOND_WEIGHT1080_LOWER_BOUND.json'

def main():
    minimum_support=25;forbidden_support=26;next_support=27;local_min=40
    minimum_weight=1000;lower=next_support*local_min
    assert minimum_support*local_min==minimum_weight
    assert lower==1080
    out={
      'pass':5453,'status':'THEOREM_Q5_K0_POSTMINIMUM_HAMMING_GAP_TO1080',
      'code':'K0=[73125,560,1000]_2',
      'complete_minimum_shell_words':2340,
      'minimum_block_support':25,
      'forbidden_block_support':26,
      'next_possible_block_support_lower_bound':27,
      'local_even_block_minimum_weight':40,
      'second_nonzero_Hamming_weight_lower_bound':1080,
      'forbidden_weight_interval':[1001,1079],
      'gap_width':79,
      'proof':'Pass5284 exhausts support25 at weight1000; Pass5452 excludes support26; every nonzero local even block contributes at least40.',
      'boundary':'No Hamming-weight1080 or block-support27 witness is asserted. Exact second nonzero weight remains open.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
