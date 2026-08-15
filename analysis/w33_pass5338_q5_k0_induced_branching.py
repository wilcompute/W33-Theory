#!/usr/bin/env python3
"""Pass5338: exact induced-branching decomposition of the q=5 K0 shell module.

Pass5337 gives
  C[G/H] = Ind_P^G(1 + 4 + 2*5)
from the local A5/V4 fiber. Pass5332 gives the global shell decomposition
  1 + 104 + 65_a + 520 + 3*90 + 2*65_b + 2*625.
Pass5333 identifies the point module
  Ind_P^G(1)=1+90+65_a.

Subtracting leaves the 2184-dimensional vertical module. Since the local 5 occurs
twice, every constituent contributed by 2*Ind_P^G(5) has even multiplicity. The
only odd-multiplicity vertical constituents are 104 and 520, and
104+520=624=[G:P]*4. Hence

  Ind_P^G(4) = 104 + 520,
  Ind_P^G(5) = 90 + 65_b + 625.

This distinguishes the two global 65-dimensional irreducibles by their local
branch source.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5338_Q5_K0_INDUCED_BRANCHING.json'

def main():
    index=156
    point={'1':1,'90':1,'65a':1}
    ind4={'104':1,'520':1}
    ind5={'90':1,'65b':1,'625':1}
    def dim(D):
        sizes={'1':1,'90':90,'65a':65,'65b':65,'104':104,'520':520,'625':625}
        return sum(sizes[k]*m for k,m in D.items())
    assert dim(point)==index
    assert dim(ind4)==index*4==624
    assert dim(ind5)==index*5==780
    # Reassemble shell = Ind1 + Ind4 + 2 Ind5.
    total={}
    for D,f in ((point,1),(ind4,1),(ind5,2)):
        for k,m in D.items():total[k]=total.get(k,0)+f*m
    assert total=={'1':1,'90':3,'65a':1,'104':1,'520':1,'65b':2,'625':2}
    assert dim(total)==2340
    vertical={k:v for k,v in total.items()};vertical['1']-=1;vertical['90']-=1;vertical['65a']-=1
    vertical={k:v for k,v in vertical.items() if v}
    assert dim(vertical)==2184==index*14
    out={'pass':5338,'status':'THEOREM_Q5_K0_EXACT_LOCAL_TO_GLOBAL_INDUCED_BRANCHING',
      'local_fiber_module':'A5/V4: 15 = 1 + 4 + 2*5',
      'point_induction':'Ind_P^G(1) = 1 + 90 + 65_a',
      'four_induction':'Ind_P^G(4) = 104 + 520',
      'five_induction':'Ind_P^G(5) = 90 + 65_b + 625',
      'shell_reassembly':'1+104+65_a+520+3*90+2*65_b+2*625 = 2340',
      'vertical_module':'104 + 520 + 2*90 + 2*65_b + 2*625 = 2184 = 156*14',
      'derivation':'After removing the point module, the only odd-multiplicity vertical constituents are 104 and520. Their dimensions sum to624=156*4, forcing them to be Ind(4); the remaining half gives Ind(5).',
      'conclusion':'The two 65-dimensional global irreducibles are now representation-theoretically separated: 65_a comes from the point/trivial local sector, while 65_b comes from the local A5 five-dimensional sector.',
      'boundary':'Complex representation branching theorem. No characteristic-2 identification of either 65-space is inferred.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
