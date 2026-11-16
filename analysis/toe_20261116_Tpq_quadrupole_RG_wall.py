"""Check the matched five-dimensional quadrupole wall and its scales."""

import json
from fractions import Fraction
from math import log
from pathlib import Path

import sympy as sp


def match_effective_action():
    detuning, amplitude = sp.symbols("t x", real=True)
    mixing, level = sp.symbols("m2 lambda", real=True)
    spectrum = level+16-8*sp.sqrt(level+4)
    assert spectrum.subs(level, 32) == 0
    assert sp.diff(spectrum, level).subs(level, 32) == sp.Rational(1, 3)
    coupling = sp.Rational(256, 3)
    kinetic = sp.solve(mixing/(144*coupling**2)-sp.Rational(1, 65536), mixing)[0]
    assert kinetic == 16

    superpotential = 6+kinetic*(detuning*amplitude**2/24-coupling*amplitude**3/36)
    slope = sp.diff(superpotential, amplitude)
    potential = slope*slope/(2*kinetic)-superpotential**2/3
    radius_derivative = -slope/kinetic
    scalar_equation = (
        sp.diff(radius_derivative, amplitude)*radius_derivative
        + 4*(superpotential/6)*radius_derivative-sp.diff(potential, amplitude)/kinetic
    )
    assert sp.expand(scalar_equation) == 0
    assert sp.expand((superpotential/6)**2+potential/12-kinetic*radius_derivative**2/24) == 0
    assert sp.expand(sp.diff(superpotential/6, amplitude)*radius_derivative
                     +kinetic*radius_derivative**2/6) == 0
    u = sp.Symbol("u", real=True)
    assert sp.expand(radius_derivative.subs(amplitude, detuning*u/coupling)
                     +detuning**2*u*(1-u)/(12*coupling)) == 0
    transfer_functions = (u*(1-u), u, u/(1-u)**3)
    multiplet_factors = (1-2*u, 1-u, 1+2*u)
    for transfer, factor in zip(transfer_functions, multiplet_factors):
        assert sp.simplify(u*(1-u)*sp.diff(transfer, u)-factor*transfer) == 0
    c_ratio = (6/superpotential.subs(amplitude, detuning/coupling))**3
    assert sp.series(c_ratio, detuning, 0, 4).removeO() == 1-detuning**3/65536

    field = sp.Symbol("phi")
    canon = sp.expand(superpotential.subs(amplitude, field/sp.sqrt(kinetic)))
    assert canon == 6+detuning*field**2/24-sp.Rational(16, 27)*field**3
    return {"axial_kinetic_coefficient": int(kinetic),
            "canonical_superpotential": str(canon),
            "linearized_physical_mass_divided_by_static_slope": "-1/3",
            "axial_and_biaxial_warped_mass_squared_at_first_order": ["t/3", "-t"],
            "leading_axial_rotational_biaxial_transfer": [str(x) for x in transfer_functions],
            "model_central_charge_ratio": str(sp.factor(c_ratio)),
            "source_to_vev_wall_coordinate": "u=1/(1+exp(t*(r-r0)/12))"}


def examples():
    certificate = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_warp_resonance.json"
    detuned = json.loads(certificate.read_text(encoding="utf-8"))["neutral_near_resonances"]
    rows = []
    for sequence in detuned:
        norm = sequence["norm"]
        limit = -Fraction(sequence["asymptotic_detuning_times_p_squared"])
        assert limit == Fraction(5*norm, 12)
        example = sequence["examples"][1]
        p, q = example["chern_pair"]
        t = -example["neutral_eigenvalue_minus_32"]
        assert abs(t*p*p/float(limit)-1) < 1e-7
        rows.append({"chern_pair": [p, q], "t": t, "UV": "unwarped" if t > 0 else "warped",
                     "wall_log_energy_width_10_to_90_leading": 24*log(9)/abs(t),
                     "fixed_charge_central_charge_shift_leading": -t**3/65536})
    return rows


def main():
    data = match_effective_action()
    data["pell_sequences"] = examples()
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_quadrupole_RG_wall.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the matched quadrupole normalization, wall equations, and anomaly jump.")


if __name__ == "__main__":
    main()
