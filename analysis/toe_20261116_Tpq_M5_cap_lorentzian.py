"""Continue the capped M5 into Lorentzian AdS and locate first contact."""

import json
from math import pi, sin, sqrt
from pathlib import Path

import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq


def open_volume(time):
    if time < 0.2:
        # Integral of sin(t)^4, expanded near the removable zero.
        return time**5*(1/5-2*time**2/21+time**4/45-34*time**6/10395)
    return 3*time/8-sin(2*time)/4+sin(4*time)/32


def velocity(time, pressure):
    source = pressure*open_volume(time)
    return source/sqrt(sin(time)**8+source**2)


def displacement(time, pressure):
    return quad(lambda point: velocity(point, pressure), 0, time,
                epsabs=2e-12, epsrel=2e-12)[0]


def exact_checks():
    t, radius, c, source, weight = sp.symbols("tau r c V S", positive=True)
    open_primitive = 3*t/8-sp.sin(2*t)/4+sp.sin(4*t)/32
    euclidean_primitive = 3*radius/8-sp.sinh(2*radius)/4+sp.sinh(4*radius)/32
    assert sp.simplify(sp.diff(open_primitive, t)-sp.sin(t)**4) == 0
    assert sp.simplify(euclidean_primitive.subs(radius, sp.I*t)-sp.I*open_primitive) == 0
    assert sp.series(open_primitive, t, 0, 12).removeO() == (
        t**5/5-2*t**7/21+t**9/45-sp.Rational(34, 10395)*t**11
    )
    speed = c*source/sp.sqrt(weight**2+c*c*source**2)
    gamma = sp.simplify(1/sp.sqrt(1-speed**2))
    assert sp.simplify(weight*speed*gamma-c*source) == 0
    assert sp.simplify((1+speed**2)/(1-speed**2)-(1+2*(c*source/weight)**2)) == 0


def track(row):
    pressure = 4/row["alpha"]
    threshold = row["round_threshold_period"]
    cap_length = threshold*row["samples"][0]["period_over_round_threshold"]
    equal_action_length = threshold*row["cap_action_crossing_period_over_round_threshold"]
    full_displacement = displacement(pi, pressure)
    maximum_contact_length_before_refocus = cap_length+2*full_displacement
    assert cap_length < equal_action_length < threshold < maximum_contact_length_before_refocus

    def encounter(length):
        time = brentq(lambda t: 2*displacement(t, pressure)-(length-cap_length), 0, pi, xtol=2e-13)
        speed = velocity(time, pressure)
        assert 0 < speed < 1
        assert abs(2*displacement(time, pressure)+cap_length-length) < 2e-11
        return {"longitudinal_length_over_round_threshold": length/threshold,
                "open_AdS_time": time, "proper_speed_of_each_front": speed,
                "relative_Lorentz_factor": (1+speed**2)/(1-speed**2)}

    return {"chern_pair": row["chern_pair"],
            "initial_cap_width": cap_length,
            "width_at_first_refocus_without_collision": maximum_contact_length_before_refocus,
            "round_radial_threshold": threshold,
            "at_equal_probe_action": encounter(equal_action_length),
            "at_round_radial_threshold": encounter(threshold)}


def main():
    exact_checks()
    data_dir = Path(__file__).resolve().parents[1]/"data"
    input_path = data_dir/"toe_20261116_Tpq_M5_finite_stripe.json"
    finite_stripes = json.loads(input_path.read_text(encoding="utf-8"))
    result = {"open_AdS_chart_refocus_time": pi,
              "rows": [track(row) for row in finite_stripes["actual_warped_backgrounds"]]}
    output = data_dir/"toe_20261116_Tpq_M5_cap_lorentzian.json"
    output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print("Verified the Lorentzian continuation and torus front contact on three warped backgrounds.")


if __name__ == "__main__":
    main()
