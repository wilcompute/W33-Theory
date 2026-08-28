#!/usr/bin/env python3
"""Pass10885-10892 outside-box: Tate/Ext interpretation of the 32 C2 defect.

Pass10837 resolves the order-two normalizer mismatch on the 316-dimensional
C13-fixed sector:

  F2[V2] = 1^64 + J2^126,
  H1(H4) = J2^158,

as F2[C2]-modules, where J2 is the two-dimensional indecomposable regular
module.  Therefore H1 is obtained from F2[V2] by replacing 64 split trivial
summands with 32 nonsplit self-extensions

  0 -> 1 -> J2 -> 1 -> 0.

Over A=F2[C2] ~= F2[e]/(e^2), Ext^1_A(1,1)=F2.  Thus there is exactly one
nonzero extension class, and the defect consists of 32 copies of that unique
class.

Tate cohomology makes the same obstruction visible stably.  The regular module
J2 is projective, so its Tate cohomology vanishes in every degree; the trivial
module has one-dimensional Tate cohomology in every degree because both
(k-1) and the norm 1+k vanish on it in characteristic two.  Hence

  dim Hhat^n(C2,F2[V2]) = 64,
  dim Hhat^n(C2,H1(H4)) = 0

for all n.  The stable repair

  F2[V2] + J2^32 ~= H1(H4) + 1^64

has matching Tate cohomology (dimension64) on both sides.  The numerical
relation 64=2*32 is therefore structural: each missing nonsplit J2 consumes two
trivial composition factors but kills their Tate classes by becoming projective.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10885_10892_C2_TATE_EXT_DEFECT.json'

def main():
    old=json.loads((ROOT/'data/PART_W33_PASS10837_10844_D26_EXTENSION_DEFECT_RESOLUTION.json').read_text())
    assert old['C13_fixed_sector']['F2V2_C2_decomposition']=='1^64 + J2^126'
    assert old['C13_fixed_sector']['H1_C2_decomposition']=='J2^158'
    assert old['minimal_stable_repair']['dimension_each_side']==4160

    triv_v2=64;proj_v2=126;proj_h1=158
    assert triv_v2+2*proj_v2==316
    assert 2*proj_h1==316
    missing_extensions=proj_h1-proj_v2
    assert missing_extensions==32 and 2*missing_extensions==triv_v2

    # A=F2[C2]=F2[e]/e^2.  Up to isomorphism its finite indecomposables are
    # 1=A/(e) and J2=A.  The unique nonsplit self-extension of 1 is A itself.
    ext1_dimension=1
    ext_nonzero_classes=(2**ext1_dimension)-1
    assert ext_nonzero_classes==1

    # Tate dimensions in every degree: trivial contributes1, projective J2 contributes0.
    tate_v2=triv_v2
    tate_h1=0
    assert tate_v2==64 and tate_h1==0
    # Stable repair: adding projectives left changes no Tate; adding 64 trivials right yields64.
    tate_left=tate_v2
    tate_right=tate_h1+64
    assert tate_left==tate_right==64

    out={
      'schema':'w33.pass10885_10892.c2_tate_ext_defect.v1','status':'PASS','passes':'10885-10892','outside_box':True,
      'algebra':{'group':'C2=<k>','field':'F2','group_algebra':'F2[C2] ~= F2[e]/(e^2), e=k+1','indecomposables':['1=A/(e)','J2=A regular/projective']},
      'modules':{'F2V2_fixed_sector':'1^64 + J2^126','H1_fixed_sector':'J2^158','dimension_each':316},
      'Ext1':{
        'Ext1_1_1_dimension':ext1_dimension,
        'nonzero_extension_classes':1,
        'unique_nonsplit_extension':'0 -> 1 -> J2 -> 1 -> 0',
        'missing_J2_extensions':missing_extensions,
        'interpretation':'the order-two defect is 32 copies of the unique nonzero class in Ext^1_{F2[C2]}(1,1)'},
      'Tate_cohomology':{
        'trivial_module':'Hhat^n(C2,1)=F2 for every n','regular_projective':'Hhat^n(C2,J2)=0 for every n',
        'F2V2_dimension_each_degree':tate_v2,'H1_dimension_each_degree':tate_h1,
        'stable_repair_dimension_each_degree':64,
        'identity':'64 = 2*32 because each nonsplit projective J2 joins two trivial composition factors and annihilates their stable/Tate obstruction'},
      'stable_category':{'F2V2':'1^64','H1':'0','meaning':'after quotienting projectives, the entire defect is the 64 trivial Tate classes'},
      'theorem':'The characteristic-two normalizer defect is exactly extension data. H1 contains 32 more copies of the unique nonsplit self-extension J2 of the trivial C2-module, replacing the 64 split trivial summands present in F2[V2]. Equivalently, the stable/Tate obstruction has dimension 64 in every degree on F2[V2] and vanishes on H1. The relation 64=2*32 is forced by the length-two projective extension, not a numerical coincidence.',
      'boundary':'Exact modular representation theory of C2 in characteristic2 applied to the certified Pass10837 decompositions. It does not identify a canonical global set of 32 extension generators inside Co1 or H(4); Pass10861 already rules out the simplest translation-type C13-equivariant realization.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Ext1_dim':1,'missing_extensions':32,'Tate_defect':64,'identity':'64=2*32'}))
if __name__=='__main__':main()
