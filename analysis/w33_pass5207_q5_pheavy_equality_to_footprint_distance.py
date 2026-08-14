#!/usr/bin/env python3
"""Pass5207: the remaining q=5 P-heavy equality shell injects into footprint wt<=24.

Pass5201 gives an intrinsic P-component parity vector s=F^T a for every q=5
apartment-code word.  P components partition the apartment coordinates, so the
parity of |s| equals the total apartment weight.  Thus every weight-625 word has
s!=0.

Each nonzero P-component restriction lies in the [225,25,25]_2 tensor code of
Pass5177/5179.  Its minimum words have weight exactly 25 and are P-heavy-free.
Consequently a P-heavy word has at least one nonzero component whose weight is
strictly greater than 25.  If t=wt(s), each of the t odd components is nonzero
and costs at least 25 apartments.  Designating one P-heavy component costs at
least 26, so

  625 >= 26 + 25(t-1),

hence t<=24.  Therefore

  P-heavy exotic weight625 => a nonzero footprint-code word of weight <=24.

Conversely the 156 W-point footprint rows have weight 25 (Pass5186/5203), so the
footprint code has d<=25.  Thus proving d>=25, equivalently excluding weights
1..24, would give d=25 and would eliminate every P-heavy equality candidate.
Pass5191 already proves every P-heavy-free weight625 word is a chamber star, so
this single footprint-distance statement would classify the complete q=5
weight-625 shell.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5207_Q5_PHEAVY_EQUALITY_FOOTPRINT_REDUCTION.json'

def main():
    max_t=(625-26)//25+1
    assert max_t==24
    assert 26+25*(24-1)==601
    assert 26+25*(25-1)==626>625
    out={'pass':5207,'status':'THEOREM_Q5_PHEAVY_EQUALITY_IMPLIES_FOOTPRINT_WEIGHT_AT_MOST_24',
      'total_weight':625,
      'footprint_parity_nonzero':'P components partition apartment coordinates and 625 is odd, so the P-component parity vector s is nonzero.',
      'local_component_code':'Every nonzero P component has weight >=25; every weight-25 component is a minimum tensor atom and is P-heavy-free.',
      'Pheavy_cost':'A P-heavy word has at least one nonzero component of weight >25, hence at least 26.',
      'inequality':'625 >= 26 + 25(t-1), where t=wt(s), hence t<=24.',
      'consequence':'Any exotic q5 weight625 word must yield a nonzero word of weight <=24 in the Pass5201 footprint code im(F^T).',
      'closure_target':'Because the 156 point footprints have weight25, proving d(im(F^T))>=25 gives d=25 and, together with Pass5191, proves every q5 weight625 word is a chamber star.',
      'boundary':'This is an exact reduction, not yet a proof that the footprint code has minimum distance 25 and not a sub-625 distance proof.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
