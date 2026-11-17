"""Continue wrapped M5 stripe probes by their exact hyperbolic first integral."""

import json
from math import cos, pi, sinh, sqrt
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import hyp2f1


def area(radius):
    return sinh(radius)**4


def volume(radius):
    if radius < 0.4:
        s = sinh(radius)
        return s**5/5*hyp2f1(0.5, 2.5, 3.5, -s*s)
    return sinh(4*radius)/32-sinh(2*radius)/4+3*radius/8


def family(alpha):
    round_radius = float(np.arctanh(alpha))
    pressure = 4/alpha
    round_action = area(round_radius)-pressure*volume(round_radius)
    round_period = pi*sinh(round_radius)

    def action_density(radius):
        return area(radius)-pressure*volume(radius)

    cap_radius = brentq(action_density, round_radius, round_radius+3)

    def orbit(fraction):
        energy = fraction*round_action
        neck = brentq(lambda r: action_density(r)-energy, 0, round_radius) if fraction else 0.
        bulge = brentq(lambda r: action_density(r)-energy, round_radius, cap_radius+1e-10)
        midpoint = (neck+bulge)/2
        width = (bulge-neck)/2

        def integrands(angle):
            radius = midpoint-width*cos(angle)
            surface = area(radius)
            pressure_volume = pressure*volume(radius)
            radicand = (action_density(radius)-energy)*(surface+energy+pressure_volume)
            assert radicand > 0
            root = sqrt(radicand)
            jacobian = width*np.sin(angle)
            return (energy+pressure_volume)*jacobian/root, root*jacobian

        period = 2*quad(lambda t: integrands(t)[0], 0, pi, epsabs=1e-8, epsrel=3e-8)[0]
        integral = 2*quad(lambda t: integrands(t)[1], 0, pi, epsabs=1e-8, epsrel=3e-8)[0]
        normalized_excess = (integral-(round_action-energy)*period)/(round_action*round_period)
        return {"first_integral_over_round_action_density": fraction,
                "neck_over_round_radius": neck/round_radius,
                "bulge_over_round_radius": bulge/round_radius,
                "period_over_round_threshold": period/round_period,
                "action_excess_over_round_action_at_threshold": normalized_excess,
                "action_over_round_action_at_threshold":
                    (energy*period+integral)/(round_action*round_period)}

    samples = [orbit(value) for value in (0, .001, .01, .05, .1, .2, .35, .5, .65, .8, .9, .95, .98)]
    periods = [row["period_over_round_threshold"] for row in samples]
    excess = [row["action_excess_over_round_action_at_threshold"] for row in samples]
    cap_crossing = samples[0]["action_over_round_action_at_threshold"]
    assert periods[0] < cap_crossing < 1
    assert all(y > x for x, y in zip(periods, periods[1:]))
    assert all(value > 0 for value in excess)
    # At fixed pressure, the first integral is the derivative of the action
    # with respect to the period. Check this independently at interior points.
    for value in (.1, .4, .8):
        left, right = orbit(value-.001), orbit(value+.001)
        slope = ((right["action_over_round_action_at_threshold"] -
                  left["action_over_round_action_at_threshold"]) /
                 (right["period_over_round_threshold"]-left["period_over_round_threshold"]))
        assert abs(slope-value) < 2e-5, (alpha, value, slope)
    return {"alpha": alpha, "round_radius_in_local_ads_units": round_radius,
            "round_threshold_period": round_period,
            "cap_bulge_radius": cap_radius,
            "cap_action_crossing_period_over_round_threshold": cap_crossing,
            "samples": samples}


def main():
    index = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_probe_action.json"
    physical_examples = json.loads(index.read_text(encoding="utf-8"))["near_resonant_probe_examples"]
    examples = (.1, .3, .6, .85, .95, .99, .999)
    data = {"small_alpha_limits": {"cap_period_over_round_threshold": "5/(2*pi)",
                                   "crossing_period_over_round_threshold": "15625/16384"},
            "families": [family(alpha) for alpha in examples],
            "actual_warped_backgrounds": [
                {"chern_pair": row["chern_pair"], **family(row["tension_to_charge_ratio"])}
                for row in physical_examples
            ]}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_M5_finite_stripe.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    for row in data["families"]:
        print(row["alpha"], row["samples"][0]["period_over_round_threshold"],
              row["cap_action_crossing_period_over_round_threshold"])


if __name__ == "__main__":
    main()
