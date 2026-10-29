"""Five independent post-minimal-native-gauge W33 regression tracks."""
from analysis.w33_20261028_five_fronts_followup import (
    action_and_reduction,native_bloch_and_gauss,compact_quantum,E6_charge_response
)

def test_reflection_endpoint_exchange_and_perturbed_cone():
    c=action_and_reduction()
    assert c["endpoint_exchange"]
    assert c["rank_H_ends"]==[3,3]
    s=c["single_cone_splitting"]
    assert max(s["0"])-min(s["0"])<1e-12
    assert max(s["1/100"])-min(s["1/100"])>0.002

def test_dimensional_orthogonality_and_odd_line():
    c=action_and_reduction()["dimensional_reduction"]
    assert c["even_determinant"]==648
    assert c["odd_norm_squared"]==18
    assert c["three_even_period_metric"]==[[10,0,-6],[0,12,-6],[-6,-6,12]]

def test_real_native_link_loops_gauss_and_all_bloch_corners():
    c=native_bloch_and_gauss()
    assert c["integer_lifted_gauss_exact"]
    assert c["electric_gram"]==[[794,-42,768],[-42,22,-52],[768,-52,766]]
    assert len(c["corners"])==16
    assert [x["mixed_rank"] for x in c["corners"]]==[105]+[108]*15

def test_compact_rotor_spectral_residual_and_variational_control():
    c=compact_quantum()
    assert c["hessian_exact"]
    assert len(c["samples"])==6
    for g in (.1,.2):
        s=[x for x in c["samples"] if x["g"]==g]
        assert s[0]["ground_energy"]>s[1]["ground_energy"]
        assert s[2]["ground_energy"]<=s[1]["ground_energy"]+1e-9
        assert abs(s[2]["ground_energy"]-s[1]["ground_energy"])<1e-6
        assert all(x["max_Ritz_residual"]<1e-8 for x in s)
        assert all(x["excitation_gap_in_truncated_sector"]>0 for x in s)

def test_E6_two_charge_cubic_ward_and_conditional_polarization():
    c=E6_charge_response()
    assert c["equal_matter_response_trace_metric"]==[[120,0],[0,72]]
    assert sum(c["cubic_counts"].values())==45
    for k in ("1,0","0,1","1,1","3,0","0,3","2,1","1,2"):
        assert c["moments"][k]==0
