#!/usr/bin/env python3
"""Pass5155: one universal augmentation relation versus hidden native rank defect."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5155_NATIVE_AUGMENTATION_DEFECT.json'

def main():
    rows=[
      {'q':2,'p':2,'rows':16,'cols':32,'generic_rank':15,'native_rank':15},
      {'q':3,'p':3,'rows':81,'cols':108,'generic_rank':69,'native_rank':68},
      {'q':4,'p':2,'rows':256,'cols':256,'generic_rank':184,'native_rank':180},
      {'q':5,'p':5,'rows':625,'cols':500,'generic_rank':405,'native_rank':397},
      {'q':7,'p':7,'rows':2401,'cols':1372,'generic_rank':1183,'native_rank':1173},
    ]
    for r in rows:
        r['rank_drop']=r['generic_rank']-r['native_rank']
        r['minimum_hidden_beyond_one_explicit_relation']=max(0,r['rank_drop']-1)
    assert [r['rank_drop'] for r in rows]==[0,1,4,8,10]
    out={'pass':5155,'status':'THEOREM_NATIVE_AUGMENTATION_PLUS_HIDDEN_DEFECT',
         'universal_relation':'Every root-coset column has q entries. If q=p^f, the all-ones left functional satisfies 1^T M=q 1^T=0 in characteristic p.',
         'rows':rows,
         'conclusion':'The displayed augmentation relation supplies one explicit native relation, but the observed rank drops at q=4,5,7 exceed one; at least 3,7,9 additional modular rank-loss dimensions remain respectively.',
         'q3_special':'The total q3 drop is exactly one, compatible with the unique Z/3 Smith torsion direction.',
         'q4_special':'Pass5153 proves the four-dimensional F2 loss is exactly four Z/2 Smith torsion directions.',
         'boundary':'q2,q3,q5,q7 ranks are prior certified inputs; this pass does not re-own them or identify the hidden q5/q7 modular composition factors.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
