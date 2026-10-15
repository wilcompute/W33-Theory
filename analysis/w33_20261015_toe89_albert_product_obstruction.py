"""TOE89 multiplication-level obstruction to a *naive* Albert bridge.

Over F2, binary H1 ~= regular H27 augmentation (TOE88). A very
natural equivariant commutative product on augmentation is projected
pointwise multiplication. It is NOT a Jordan algebra as a polynomial
identity: F4 scalar-extension yields an explicit counterexample.

The full pointwise 27D permutation algebra is associative/Jordan but
has 27 pairwise-orthogonal primitive idempotents and is not Albert J3(O)
(rank/degree 3). Neither observation forbids an alternative exceptional
H27-equivariant multiplication on the 26D module.
"""
from __future__ import annotations
import json,random
from analysis.w33_20261015_toe85_h2_relation_module import ROOT
from analysis.w33_20261015_toe86_geometry_integral_routing import H,IDX,mul
from analysis.w33_20261015_toe88_tate_albert_bridge import augmentation_action

def times(a,b):
    z=0
    for j in range(2):
        if b&(1<<j):z^=a<<j
    if z&4:z^=7
    return z
def project(w):
    s=0
    for x in w:s^=x
    return [x^s for x in w]
def star(x,y):
    return project([times(a,b) for a,b in zip(x,y)])
def perm(g,x):
    out=[0]*27
    for h in H:out[IDX[mul(g,h)]]=x[IDX[h]]
    return out
def jordan_defect(x,y):
    x2=star(x,x)
    return [a^b for a,b in zip(star(star(x2,y),x),star(x2,star(y,x)))]
def gf4_vec(raw):
    out=raw+[0]*(27-len(raw))
    assert len(out)==27
    assert sum(out)<1000
    out[-1]=0
    for v in out[:-1]:out[-1]^=v
    assert project(out)==out
    return out
def certificate():
    x=gf4_vec([3,1,2,1,0,1])
    y=gf4_vec([2,3,1,1,0,1])
    defect=jordan_defect(x,y)
    assert any(defect),(x,y)
    assert all(star(perm(g,x),perm(g,y))==perm(g,star(x,y)) for g in H)
    assert all(perm(g,project(x))==project(perm(g,x)) for g in H)
    assert all(star(x,[0]*27)==[0]*27 for x in (x,y))
    # Binary vectors have x^2=x in this product, hiding non-Jordan
    # behavior when only checking F2-valued elements.
    rng=random.Random(8915)
    for _ in range(80):
        v=gf4_vec([rng.randrange(2) for j in range(26)])
        w=gf4_vec([rng.randrange(2) for j in range(26)])
        assert star(v,v)==v
        assert not any(jordan_defect(v,w))
    aug=augmentation_action(2)
    assert len(aug[(0,0,0)])==26
    binary_iso=json.loads((ROOT/"data/w33_20261015_toe88_tate_albert_bridge.json").read_text())["binary_aug_equivariant_isomorphism_to_selected_H1"]
    assert binary_iso["rank"]==26
    return {
      "canonical_27D_permutation_algebra":"F2^27 with coordinatewise associative multiplication; H27 acts by permuting coordinates.",
      "27D_orthogonal_primitive_idempotent_count":27,
      "Albert_degree_rank_comparison":"The split Albert cubic Jordan algebra has degree/rank 3; the 27D pointwise product has 27 primitive mutually orthogonal idempotents, so it is not Albert multiplication.",
      "26D_binary_aug_H27_isomorphism_rank":26,
      "natural_26D_binary_product":"x star y = P(x coordinatewise*y), P(w) = w - (sum w)/27 * 1; for F2 (27=1), subtraction equals addition.",
      "product_H27_equivariant_over_GF4":True,
      "non_Jordan_under_scalar_extension_GF4":True,
      "GF4_definition":"GF4=F2[t]/(t^2+t+1); values 0,1,t,t+1 encoded as integers 0,1,2,3.",
      "Jordan_identity_test":"(x star x star y) star x == (x star x) star (y star x); parentheses: ((x*x)*y)*x vs (x*x)*(y*x)",
      "explicit_counterexample_x":x,
      "explicit_counterexample_y":y,
      "explicit_nonzero_Jordan_defect":defect,
      "defect_support":[i for i,v in enumerate(defect) if v],
      "binary_only_test_false_negative_demonstrated":80,
      "scope":"Rules out the NATURAL projected coordinatewise multiplication as an exceptional Jordan product. Does not rule out another H27-equivariant 26D exceptional Jordan-related construction."}
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe89_albert_product_obstruction.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("ALBERT",d["defect_support"],d["non_Jordan_under_scalar_extension_GF4"])
