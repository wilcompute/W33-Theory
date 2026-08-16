#!/usr/bin/env python3
"""Pass5618: test whether the derived Z3 connection itself selects E6 matter couplings.

The repo's E6/firewall construction has 36 allowed cubic triads, organized as
three Z3 lifts of each of 12 AG(2,3) affine lines, and 9 forbidden fiber triads.
After the block-dependent gauge shift, an allowed line has lift coordinates

    (k, k+lambda, k+2 lambda), k in F3.

Every such cubic is Z3-neutral.  But the forbidden fiber (0,1,2) is neutral too.
Therefore simple Z3 charge conservation does NOT explain the firewall 36/9
selection.  The selector must live in the affine incidence/holonomy/L-infinity
structure, not merely in total Z3 charge.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5618_GAUGE_MATTER_PHASE_SELECTION.json'

def main():
    allowed=[]
    # 12 affine lines; lambda can be 0,1,2. Neutrality is independent of its value.
    # Enumerate one representative of each lambda for each of four direction classes,
    # then three intercept/lift choices: 4*3*3=36 triads.
    for direction in range(4):
        for lam in range(3):
            for k in range(3):
                t=(k,(k+lam)%3,(k+2*lam)%3)
                assert sum(t)%3==0
                allowed.append({'direction_class':direction,'lambda':lam,'k':k,'t':list(t)})
    assert len(allowed)==36
    forbidden=[]
    for block in range(9):
        t=(0,1,2);assert sum(t)%3==0
        forbidden.append({'block':block,'t':list(t)})
    assert len(forbidden)==9
    out={'pass':5618,'status':'Z3_NEUTRALITY_UNIVERSAL_SO_NOT_THE_FIREWALL_SELECTOR',
         'allowed_cubic_count':36,'forbidden_fiber_count':9,'all_45_Z3_neutral':True,
         'allowed_lift_law':'t_i=k+i lambda mod 3, i=0,1,2, hence sum_i t_i=0 mod 3',
         'forbidden_fiber_law':'0+1+2=0 mod 3',
         'positive_bridge':'the same derived AG(2,3)+Z3 connection labels allowed E6 Yukawa triads and supplies the nonzero gauge curvature used in Pass5617',
         'negative_result':'total Z3 charge cannot distinguish the 36 allowed cubics from the 9 firewall cubics; a matter-selection claim based only on charge neutrality is false',
         'next_physical_selector_candidates':['Wilson/triangle holonomy','affine-line incidence class','L-infinity l3 support on bad9','CE2/metaplectic phase','chirality under the q=3 vector double cover'],
         'physics_firewall':'This is a selection-rule falsifier. It does not assign observed fermions or Yukawa magnitudes; it identifies what the existing Z3 connection can and cannot explain.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
