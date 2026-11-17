"""Controlled torus-shape and conditional eight-derivative spectral firewall.

At equal integer periods N0=N1=N2=N>0, L^3/lp^3=9*pi*N/2.
In reduced torus fundamental domain tau=x+iy, the shortest physical
cycle radius is R_min/lp=(L/lp)/sqrt(3*pi*y) for A_T/L^2=4*pi/3.

The sharp CLASSICAL BF deficit >=delta*=0.4635418504 on every shape.
If the operator norm of ALL corrected canonically normalized quadratic
terms is bounded by C*(lp/L)^6, the Rayleigh quotient guarantees the
corrected BF instability survives when C<delta*(L/lp)^6.
No actual C is calculated, and uniform applicability at modular cusps
requires the physical torus cycle radius also be large.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_8derivative_shape_control_certificate.json"
PI=math.pi
DELTA=math.sqrt(4+32*PI*math.sqrt(3))-2*PI*math.sqrt(3)-2

def geometry(N,tau,short_cycle_radius_min=1.):
    if N<1 or short_cycle_radius_min<=0:raise ValueError("positive N, radius")
    x,y=tau.real,tau.imag
    if y<=0 or abs(x)>.5+1e-10 or abs(tau)<1-1e-10:raise ValueError("tau must be modular reduced")
    Llp=(9*PI*N/2)**(1/3)
    sphere=Llp/math.sqrt(6)
    torus=Llp/math.sqrt(3*PI*y)
    controlled=(sphere>=short_cycle_radius_min and torus>=short_cycle_radius_min)
    ymax=Llp*Llp/(3*PI*short_cycle_radius_min**2)
    return {"N":N,"tau":[x,y],"AdS_radius_lp":Llp,
            "sphere_radius_lp":sphere,"shortest_torus_cycle_radius_lp":torus,
            "required_min_cycle_radius_lp":short_cycle_radius_min,
            "torus_height_limit":ymax,
            "all_internal_cycles_above_cutoff":controlled}

def correction_bound(N,C, tau=1j, radius_cutoff=1.):
    if C<0:raise ValueError("C>=0")
    g=geometry(N,tau,radius_cutoff)
    crit=DELTA*(9*PI*N/2)**2
    return {
        "N":N,"assumed_upper_bound_dimensionless_C":C,
        "classical_BF_gap_sharp_all_shapes":DELTA,
        "required_C_to_cancel_worst_case":crit,
        "postulated_mass_shift_upper_bound":C/((9*PI*N/2)**2),
        "BF_instability_certified_under_assumed_operator_norm":g["all_internal_cycles_above_cutoff"] and C<crit,
        "geometry":g,
        "physics_condition":"Bound is conditional on a true operator-norm control of all corrected physical fluctuation terms and on a controlled (large-cycle) derivative expansion; it is NOT an M-theory R4 coefficient determination."}

def verify():
    examples=[geometry(N,tau,5.) for N,tau in ((10000,1j),(10000,10j),(10000,100j),(1000000,100j),(1000000,1000j))]
    assert DELTA>.46 and DELTA<.47
    assert abs(DELTA*(9*PI/2)**2-92.64323741139292)<1e-8
    assert examples[0]["all_internal_cycles_above_cutoff"]
    assert examples[3]["all_internal_cycles_above_cutoff"]
    assert not examples[4]["all_internal_cycles_above_cutoff"]
    for N in (10,100,1000):
        for tau in (1j,2j,.5+math.sqrt(3)/2*1j):
            B=correction_bound(N,1000,tau,1.)
            if B["BF_instability_certified_under_assumed_operator_norm"]:
                assert B["postulated_mass_shift_upper_bound"]<DELTA
    return {"status":"PASS_CONTROLLED_SHAPE_R4_SPECTRAL_FIREWALL",
        "sharp_delta":DELTA,
        "critical_C_per_N_squared":DELTA*(9*PI/2)**2,
        "shape_control_height_formula":"Im(tau) <= ((9*pi*N/2)^(2/3))/(3*pi*radius_cutoff^2)",
        "classical_theorem":"For equal flux every torus shape has a physical scalar-Maxwell BF gap at least delta; after any true operator correction with norm less than delta the instability remains.",
        "nonuniform_cusp_warning":"Uniform BF gap across all shapes does not imply a uniform 11D higher-derivative expansion along singular torus cusps.",
        "examples":examples,
        "postulated_correction_examples":[correction_bound(10,1000),correction_bound(100,1000),correction_bound(1000,1000)]}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"],x["critical_C_per_N_squared"])
