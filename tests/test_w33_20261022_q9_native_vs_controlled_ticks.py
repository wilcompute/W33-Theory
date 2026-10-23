"""Exact group closure in GF(9), native versus controlled transvections."""
from analysis.w33_20261022_q9_native_vs_controlled_ticks import (
    certify,add,mul,neg,generated_group,determinant
)


def test_GF9_field_axioms():
    for a in range(9):
        assert add(a,neg(a))==0
        for b in range(9):
            assert add(a,b)==add(b,a)
            assert mul(a,b)==mul(b,a)
            for c in range(9):
                assert mul(a,add(b,c))==add(mul(a,b),mul(a,c))
    assert mul(3,3)==2


def test_all_shear_parameters_and_native_square_classes():
    c=certify()
    assert c["native_possible_lower_parameters"]==[1,2,3,6]
    assert c["native_possible_generated_orders"]==[24,120]
    assert {x["order"] for x in c["active_nonsquare_parameters"]}=={720}
    assert c["full_SL29_order"]==720
    assert {x["order"] for x in c["native_all_scalings"]}=={24,120}
