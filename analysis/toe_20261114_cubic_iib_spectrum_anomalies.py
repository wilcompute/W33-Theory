"""Exact cubic-link charged levels and geometric/quiver anomaly comparison."""

import json
from itertools import combinations_with_replacement
from math import comb
from pathlib import Path

import sympy as sp


def verify(root):
    line_data = json.loads((root / "data" / "toe_20261114_cubic_iib_spin.json").read_text(encoding="utf-8"))
    charges = sp.Matrix(line_data["wrapped_line_charge_vectors_in_simple_root_basis"])
    lattice_data = json.loads((root / "data" / "toe_20261114_cubic_surface_flux.json").read_text(encoding="utf-8"))
    gram = sp.Matrix(lattice_data["negative_intersection_gram"])
    count, rank = charges.shape
    assert (count, rank) == (27, 6)
    assert sp.ones(1, count)*charges == sp.zeros(1, rank)
    assert charges.T*charges == 6*gram
    for i, j, k in combinations_with_replacement(range(rank), 3):
        assert sum(row[i]*row[j]*row[k] for row in charges.tolist()) == 0

    # BPT eqs. (2.20), (2.22) and (2.23), with six unweighted permutations.
    fiber = 2*sp.pi/3
    volume = sp.pi**3/9
    reeb_factor = 4*sp.pi/3
    rr_wavefunction_factor = -sp.pi/(3*volume)
    omega_sq = sp.pi**2/3
    bulk_rrr = 3*rr_wavefunction_factor**2*reeb_factor*fiber*omega_sq
    bulk_rbb = -reeb_factor/fiber*gram
    assert bulk_rrr == 8
    assert bulk_rbb == -2*gram

    fermion_r = -sp.Rational(1, 3)
    assert 9+count*fermion_r**3 == bulk_rrr
    assert fermion_r*charges.T*charges == bulk_rbb
    assert 9+count*fermion_r == 0  # leading large-n5 trace of R
    assert sp.Rational(9, 32)*bulk_rrr == sp.Rational(9, 4)

    levels = {}
    for k in range(1, 9):
        mass = 9*k*k+12*k
        multiplicity = (3*k*k+3*k+2)//2
        assert multiplicity == comb(k+3, 3) - comb(k, 3)
        assert (3*k+4)*(3*k) == mass
        levels[k] = {"mass_squared_times_ads_radius_squared": mass,
                     "complex_multiplicity_per_sign": multiplicity,
                     "spin_two_conformal_dimension": 3*k+4}
    assert levels[1]["mass_squared_times_ads_radius_squared"] == 21

    return {
        "charged_sector_minima_for_abs_circle_charge": levels,
        "full_first_spin_two_mass_squared_interval_in_ads_units": "(12, 21]",
        "leading_RRR_per_n5_squared": int(bulk_rrr),
        "leading_R_baryon_baryon_per_n5_squared": [[int(x) for x in row] for row in bulk_rbb.tolist()],
        "leading_RR_baryon_and_baryon_cubic": 0,
    }


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[1]
    report = json.dumps(verify(repository), indent=2) + "\n"
    path = repository / "data" / "toe_20261114_cubic_iib_spectrum_anomalies.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
