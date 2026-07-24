from analysis.w33_rh_correspondence_analytic_operator import (
    build, frontier1, frontier2, frontier4, frontier5, pair_second_difference
)


def test_release_passes():
    payload=build()
    assert payload["status"]=="PASS"
    assert payload["claim_boundary"]["classical_RH_proved"] is False


def test_correspondence_ranks():
    p=frontier1()
    assert p["checks"]["ranks_1_24_15"]
    assert p["checks"]["cohomological_ranks_48_30"]


def test_conditional_kernel_and_nonconverse():
    assert pair_second_difference(14.134725141734695,0.2)>0
    p=frontier2()
    assert p["checks"]["off_line_quartet_can_remain_positive"]


def test_automorphic_packet_local_signature():
    p=frontier4()
    assert p["census"]["W33_signature_primes"]==[11]


def test_compact_resolvent_weyl_class():
    p=frontier5()
    assert p["checks"]["compact_resolvent"]
    assert float(p["first20"]["mean_absolute_relative_error"])<0.06
