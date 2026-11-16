"""Verify the angular cut and the dense KK limit using independent measures."""

from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, fsum, isqrt, pi, sqrt
from pathlib import Path
import json


def integrate(function, intervals=128):
    step = 1 / intervals
    interior = fsum(
        (4 if i % 2 else 2) * function(i * step) for i in range(1, intervals)
    )
    return step * (function(0) + interior + function(1)) / 3


def angular_kernel(beta_sq, cosine):
    def angular_integrand(x):
        # Keep the two positive pieces separate near beta_sq = 1.
        w = sqrt(1 - beta_sq + beta_sq * 2 * (1 - cosine) * x * (1 - x))
        return 2 / (w * (1 + w))

    return integrate(angular_integrand)


def orthogonal_moment(order):
    """Integral of [x^2+(1-x)^2]^order, from the beta integral."""
    return sum(
        F(comb(order, j) * factorial(2*j) * factorial(2*(order-j)),
          factorial(2*order+1))
        for j in range(order+1)
    )


def sphere_coefficient(order, half_dimension):
    rising = factorial(half_dimension + order - 1) // factorial(half_dimension - 1)
    return F(factorial(2*order+1), 4**order * factorial(order) * rising)


def shell_counts(radius, weights):
    counts = Counter({0: 1})
    limit = radius**2
    for weight in weights:
        coordinate = Counter(weight * n*n for n in range(-isqrt(limit//weight), isqrt(limit//weight)+1))
        updated = Counter()
        for norm, multiplicity in counts.items():
            for extra, repeats in coordinate.items():
                if norm + extra < limit:
                    updated[norm + extra] += multiplicity * repeats
        counts = updated
    del counts[0]
    return counts


def first_threshold_fixture():
    rows = []
    for velocity_sq in (1e-2, 1e-3, 1e-4):
        angular = angular_kernel(velocity_sq, 0)
        linear = (angular - 1) / velocity_sq
        assert abs(linear - 0.5) < velocity_sq
        rows.append({"beta_squared": velocity_sq, "angular_average": angular})
    return rows


def isospectral_fixture():
    # Cervino and Hein, Section 2.6. The generators are the columns.
    plus = ((3, 1, 1, 1), (1, -3, 1, -1), (-1, 1, 3, -1), (-1, -1, 1, 3))
    minus = ((-3, 1, 1, 1), (-1, -3, -1, 1), (-1, 1, -3, -1), (-1, -1, 1, -3))

    def dot(left, right):
        return sum(weight * a * b for weight, (a, b) in enumerate(zip(left, right), 1))

    def low_shells(matrix):
        columns = tuple(zip(*matrix))
        for i, j in product(range(4), repeat=2):
            assert sum(a*b for a, b in zip(columns[i], columns[j])) == 12 * (i == j)
        # Euclidean orthogonality bounds each integer coefficient by sqrt(60/12).
        # The two added directions each have squared length 100.
        shells = {}
        for coordinates in product(range(-2, 3), repeat=4):
            vector = tuple(sum(a*b for a, b in zip(row, coordinates)) for row in matrix)
            norm = dot(vector, vector)
            if 0 < norm <= 60:
                shells.setdefault(norm, []).append(vector)
        return shells

    def energy_interval(norms):
        # Rational lower and upper bounds at milli-unit resolution.
        lower = sum(isqrt(norm * 1_000_000) for norm in norms)
        return lower, lower + len(norms)

    left, right = (low_shells(matrix) for matrix in (plus, minus))
    spectrum = {norm: len(vectors) for norm, vectors in left.items()}
    assert spectrum == {norm: len(vectors) for norm, vectors in right.items()}
    assert sorted(spectrum)[:4] == [18, 26, 34, 36]
    assert all(size == 2 for norm, size in spectrum.items() if norm < 60)
    minima = []
    for shells, wanted in ((left, 2), (right, 4)):
        assert {abs(dot(v, w)) for v, w in product(shells[18], shells[26])} == {wanted}
        minima.append((18, 26, 18 + 26 - 2*wanted))
    # Exclude all rank-one triples, triples with a norm >= 60, and remaining
    # rank-two triples, respectively. Below norm 60 every shell is one sign pair.
    for competing in ((18, 18, 72), (18, 18, 60), (18, 34, 36)):
        assert energy_interval(competing)[0] > energy_interval(minima[0])[1]
    assert energy_interval(minima[1])[1] < 15_500 < energy_interval(minima[0])[0]
    return {"low_norm_shells": dict(sorted(spectrum.items())),
            "first_charge_balanced_plus_norms": minima[0],
            "first_charge_balanced_minus_norms": minima[1],
            "first_energy_plus": sum(sqrt(norm) for norm in minima[0]),
            "first_energy_minus": sum(sqrt(norm) for norm in minima[1])}


def main():
    moments = [orthogonal_moment(k) for k in range(121)]
    assert moments[:3] == [1, F(2, 3), F(7, 15)]
    for k in range(121):
        beta_moment = F(24, (k+2)*(k+3)*(k+4))
        assert beta_moment * sphere_coefficient(k, 2) == sphere_coefficient(k, 5)

    # The 11D angular answer comes directly from S9 and has no KK sum.
    angular_11d = fsum(float(moment * sphere_coefficient(k, 5))
                       for k, moment in enumerate(moments))
    expected = angular_11d / 24
    rows = []
    for weights, sqrt_det in (((1, 1, 1, 1, 1, 1), 1), ((1, 1, 1, 1, 1, 4), 2)):
        for radius in (4, 8, 16, 32):
            counts = shell_counts(radius, weights)
            if radius == 4 and sqrt_det == 1:
                assert counts[1] == 12 and counts[2] == 60
            weighted_cut = 0.0
            for norm_sq, multiplicity in counts.items():
                beta_sq = 1 - norm_sq / radius**2
                weighted_cut += multiplicity * beta_sq * angular_kernel(beta_sq, 0)
            ratio = sqrt_det * weighted_cut / (radius**6 * (expected * pi**3))
            if radius == 32:
                assert abs(ratio - 1) < 2e-5, ratio
            rows.append({"weights": weights, "radius": radius, "mode_count": sum(counts.values()),
                         "ratio_to_11d_cut": ratio})

    data = {"first_threshold": first_threshold_fixture(),
            "sphere_coefficient_identity_orders": 121,
            "s9_angular_average_at_90_degrees": angular_11d,
            "continuum_comparison": rows,
            "isospectral_pair": isospectral_fixture()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_kk_unitarity.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified opening slope, 121 angular moments, and two six-dimensional lattices.")


if __name__ == "__main__":
    main()
