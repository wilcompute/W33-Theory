"""Regression for the exact W33 point/line plaquette partition-function gap."""
import math
from analysis.w33_20261031_plaquette_strict_duality_gap import (
    enumerate_weights, factor_coeffs, geometry, kernel_gf2, poly_mul
)

def codes():
    points,lines=geometry()
    rows=[sum(1<<j for j,L in enumerate(lines) if i in L) for i in range(40)]
    columns=[sum(1<<i for i in L) for L in lines]
    return enumerate_weights(kernel_gf2(rows,40)[0]),enumerate_weights(kernel_gf2(columns,40)[0])

def test_incidence_is_40_by_40_regular():
    points,lines=geometry()
    assert len(points)==len(lines)==40
    assert all(len(L)==4 for L in lines)
    assert all(sum(i in L for L in lines)==4 for i in range(40))

def test_complete_code_weight_enumerators_and_duality_gap():
    route,address=codes()
    assert sum(route.values())==sum(address.values())==32768
    assert route[10]==216 and address[8]==45
    assert route.get(8,0)==0 and address.get(10,0)==0
    delta=[address.get(k,0)-route.get(k,0) for k in range(41)]
    assert delta==factor_coeffs()+[0]*(41-len(factor_coeffs()))
    assert all(route[k]==route[40-k] for k in range(41))
    assert all(address[k]==address[40-k] for k in range(41))

def test_eighth_order_endpoint_contact():
    route,address=codes()
    delta=[address.get(k,0)-route.get(k,0) for k in range(41)]
    deriv=lambda j: sum(delta[k]*math.factorial(k)//math.factorial(k-j)
            for k in range(j,41))
    assert all(deriv(j)==0 for j in range(8))
    assert deriv(8)==9*math.factorial(8)*2**8*80

def test_positive_gap_on_ferromagnetic_interval():
    for t in (0.001,0.1,0.3,0.5,0.9,0.999):
        factor=9*t**8*(1-t*t)**8*(5*t**8+16*t**6+38*t**4+16*t*t+5)
        assert factor>0
