"""Controlled M-theory derivative expansion and probe M5 no-cure scaling.

The previously verified 2-derivative exact equal-flux torus KK
BF gap is >= sqrt(4+32pi sqrt3)-2pi sqrt3-2.
AdS radius (L/lp)^3 = 9pi N/2.
Reduced flat-torus modulus tau=x+iy gives shortest cycle
Rmin/lp=(L/lp)/sqrt(3pi*y).

The 8-derivative expansion parameter measured against torus
short cycle is (lp/Rmin)^6=4*pi*y^3/(3*N^2).
At modular cusp y~N^(2/3) it remains O(1), not perturbative,
and the number of unstable KK harmonics along long cycle grows
as N^(1/3). For y=o(N^(2/3)) the parameter vanishes.

A probe M5 has T_M5 L^6 divided by a bulk characteristic
L^9/(2kappa11^2) = 16pi²/(9N) under standard tensions.
This assumes comparable geometry factors and finite wrapping.
A finite number of probes cannot parametrically cure order-1
bulk BF gap by their O(1/N) backreaction; exact coefficient is unknown.
"""
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_11D_cusp_probe_BF_scaling.json"
PI=math.pi
BF_SHARP=math.sqrt(4+32*PI*math.sqrt(3))-2*PI*math.sqrt(3)-2

def case(N,y,n_probes=1):
    if N<1 or y<math.sqrt(3)/2 or n_probes<0:raise ValueError("reduced tau y>=sqrt3/2, N>=1")
    Llp=(9*PI*N/2)**(1/3)
    Rmin=Llp/math.sqrt(3*PI*y)
    eps_torus=(1/Rmin)**6
    eps_exact=4*PI*y**3/(3*N**2)
    assert abs(eps_torus-eps_exact)<1e-9*max(1,eps_exact)
    eps_sphere=(math.sqrt(6)/Llp)**6
    assert abs(eps_sphere-32/(3*PI**2*N**2))<1e-9
    m5=16*PI**2/(9*N)*n_probes
    # Only a subset of unstable torus momentum with k=(m,0);
    # lambda(m,0)=3pi*m^2/y. The band 0<lambda<12
    # => m^2 < 4y/pi.
    m_max=max(0,math.ceil(math.sqrt(4*y/PI))-1)
    return {"N":N,"Im_tau":y,"n_probe_M5":n_probes,
       "AdS_radius_lp":Llp,"shortest_torus_cycle_radius_lp":Rmin,
       "torus_8derivative_parameter":eps_torus,
       "sphere_8derivative_parameter":eps_sphere,
       "M5_to_bulk_characteristic_action_ratio":m5,
       "at_least_this_many_signed_classical_unstable_long_cycle_modes":2*m_max,
       "sharp_classical_BF_deficit":BF_SHARP}

def verify():
    rows=[case(N,N**p) for N in (10**3,10**6,10**9)
          for p in (0,.5,2/3,.75)]
    for N in (10**3,10**6,10**9):
        a=case(N,N**.5)
        b=case(N,N**(2/3))
        c=case(N,N**.75)
        assert b["torus_8derivative_parameter"]==4*PI/3 or abs(b["torus_8derivative_parameter"]-4*PI/3)<1e-9
        assert a["torus_8derivative_parameter"]<b["torus_8derivative_parameter"]<c["torus_8derivative_parameter"]
        assert a["at_least_this_many_signed_classical_unstable_long_cycle_modes"]>=2
    assert case(1000,1)["M5_to_bulk_characteristic_action_ratio"]<.02
    assert case(1000000,1)["M5_to_bulk_characteristic_action_ratio"]<.00002
    return {"status":"PASS_M5_PROBE_NO_CURE_AND_TORUS_CUSP_EFT_FIREWALL",
        "exact_equal_flux_constants":{"BF_gap_lower_bound":BF_SHARP,
           "torus_epsilon":"(lp/Rmin)^6 = 4*pi*(Im tau)^3 / (3*N^2)",
           "sphere_epsilon":"(lp/r_S2)^6 = 32/(3*pi^2*N^2)",
           "M5_probe_to_bulk_action":"(2*kappa11^2*T_M5/L^3)*n_M5 = 16*pi^2*n_M5/(9*N)",
           "long_cycle_unstable_harmonics":"At least 2*(ceil(sqrt(4 Im tau/pi))-1) signed Fourier modes, counting only vectors (m,0)."},
        "large_N_consequences":"At y=o(N^(2/3)), torus short-cycle 8-derivative expansion parameter tends to zero. At y~N^(2/3), it is O(1), with O(N^(1/3)) unstable long-cycle harmonics. A fixed number of M5 probes contributes O(1/N) relative bulk action and cannot compensate an O(1) bulk instability under bounded backreaction response.",
        "not_yet_physics":"Actual corrected gravity-plus-M5 fluctuation matrix, tension wrapping, possible large localized mode enhancements and flux-dependent R4 coefficients remain uncomputed.",
        "examples":rows}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(x["status"],x["exact_equal_flux_constants"]["BF_gap_lower_bound"])
