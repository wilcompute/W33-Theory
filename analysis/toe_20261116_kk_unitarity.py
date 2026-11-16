"""Verify the angular cut and the dense KK limit using independent measures."""

from collections import Counter
from fractions import Fraction as F
from itertools import permutations, product
from math import comb, factorial, fsum, isqrt, pi, prod, sqrt
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


def threshold_tree(norms):
    """Evaluate the KLT sums for scalar and noncompact graviton beams."""
    first_norm, second_norm, third_norm = norms
    inner_product = F(third_norm - first_norm - second_norm, 2)
    p = sqrt(first_norm)
    transverse = sqrt(first_norm * second_norm - inner_product**2) / p
    internal = [complex(p), complex(inner_product / p, transverse)]
    internal.append(-sum(internal))
    masses = tuple(map(sqrt, norms))
    total_energy = sum(masses)
    beam_factor = 1j * sqrt(total_energy)
    spinors = {1: (beam_factor, 0), 2: (0, beam_factor)}
    for leg, momentum in enumerate(internal, 3):
        root_energy = sqrt(abs(momentum))
        spinors[leg] = (root_energy, momentum / root_energy)

    def bracket(i, j):
        a, b = spinors[i]
        c, d = spinors[j]
        return a*d - b*c

    def invariant(i, j):
        return abs(bracket(i, j))**2 * (-1 if (i < 3) != (j < 3) else 1)

    def parke_taylor(order, numerator):
        cyclic_pairs = zip(order, order[1:] + order[:1])
        return numerator / prod(bracket(i, j) for i, j in cyclic_pairs)

    def klt_terms(numerator):
        first = (invariant(1, 2) * invariant(3, 4)
                 * parke_taylor((1, 2, 3, 4, 5), numerator)
                 * parke_taylor((2, 1, 4, 3, 5), numerator))
        second = (invariant(1, 3) * invariant(2, 4)
                  * parke_taylor((1, 3, 2, 4, 5), numerator)
                  * parke_taylor((3, 1, 4, 2, 5), numerator))
        return first, second

    first, second = klt_terms(bracket(1, 2)**4)
    q = bracket(1, 2) * bracket(3, 4) / (bracket(1, 3) * bracket(2, 4))
    assert abs(second / first + q**2 / abs(q)**2) < 1e-12
    # Since q = 1 - exp(i angle), |1 - q^2 / |q|^2|^2 = 2 + 2 cos(angle).
    squared_ratio = abs((first + second) / first)**2
    assert abs(squared_ratio - (2 + 2 * inner_product / (masses[0] * masses[1]))) < 1e-12
    stripped_scalar = abs(first + second)**2
    stripped_graviton = abs(sum(klt_terms(bracket(1, 2)**2 * bracket(3, 4)**2)))**2
    expected_scalar = total_energy**10 / prod(norms)
    expected_graviton = total_energy**6 * (total_energy - 2*masses[2])**4 / prod(norms)
    assert abs(stripped_scalar / expected_scalar - 1) < 1e-12
    assert abs(stripped_graviton / expected_graviton - 1) < 1e-12
    return squared_ratio, stripped_graviton


def scaled_three_body_phase_space(masses, excess):
    """Exact five-dimensional recursive phase space divided by excess cubed."""
    a, b, c = masses
    energy = a + b + c + excess

    def kernel(x):
        pair_energy = a + b + x * excess
        outer_momentum_sq_scaled = (
            (1-x) * (energy+pair_energy+c) * (energy+pair_energy-c)
            * (energy-pair_energy+c) / (4 * energy**2)
        )
        inner_momentum_sq_scaled = (
            x * (pair_energy+a+b) * (pair_energy+a-b)
            * (pair_energy-a+b) / (4 * pair_energy**2)
        )
        return outer_momentum_sq_scaled * inner_momentum_sq_scaled

    return integrate(kernel) / (256 * pi**3 * energy)


def graviton_cut_fixture(norms):
    masses = tuple(map(sqrt, norms))
    threshold = sum(masses)
    phase_space = prod(masses) / (48 * (2*pi)**3 * threshold**2)
    finite_energy_checks = []
    for excess in (1e-2, 1e-3, 1e-4):
        ratio = scaled_three_body_phase_space(masses, excess) / phase_space
        assert abs(ratio - 1) < excess
        finite_energy_checks.append({"excess_energy": excess, "ratio_to_threshold": ratio})
    cut_coefficients = {}
    for ordered in permutations(norms):
        _, stripped_tree = threshold_tree(ordered)
        coefficient = stripped_tree * phase_space
        singled_mass = sqrt(ordered[-1])
        expected = threshold**4 * (threshold - 2*singled_mass)**4 / (48 * (2*pi)**3 * prod(masses))
        assert abs(coefficient / expected - 1) < 1e-12
        if ordered[-1] in cut_coefficients:
            assert abs(coefficient / cut_coefficients[ordered[-1]] - 1) < 1e-12
        cut_coefficients[ordered[-1]] = coefficient
    return {"phase_space_coefficient": phase_space,
            "finite_energy_checks": finite_energy_checks,
            "stripped_cut_coefficient_by_plane_helicity_leg_norm": dict(sorted(cut_coefficients.items()))}


def triangle_reconstruction_fixture():
    """Recover the pair Gram histogram on a bounded square-lattice example."""
    cap = 20
    vectors = {(x, y): x*x + y*y for x, y in product(range(-4, 5), repeat=2)
               if x*x + y*y <= cap}
    shells = Counter(vectors.values())
    primitive_directions = {}
    for norm in sorted(shells.keys() - {0}):
        imprimitive = sum(2 * primitive_directions.get(norm // k**2, 0)
                          for k in range(2, isqrt(norm)+1) if norm % k**2 == 0)
        assert (shells[norm] - imprimitive) % 2 == 0
        primitive_directions[norm] = (shells[norm] - imprimitive) // 2

    directly_counted = Counter()
    triangles = Counter()
    for (x, y), (u, v) in product(vectors, repeat=2):
        if (x+u, y+v) not in vectors:
            continue
        a, b, c = vectors[x, y], vectors[u, v], vectors[x+u, y+v]
        directly_counted[a, b, x*u + y*v] += 1
        if x*v != y*u:
            triangles[a, b, c] += 1
    reconstructed = Counter({(a, b, (c-a-b)//2): count
                             for (a, b, c), count in triangles.items()})
    for norm, count in primitive_directions.items():
        bound = isqrt(cap // norm)
        for i, j in product(range(-bound, bound+1), repeat=2):
            if (i or j) and (i+j)**2 * norm <= cap:
                reconstructed[norm*i*i, norm*j*j, norm*i*j] += count
    reconstructed[0, 0, 0] = 1
    assert reconstructed == directly_counted
    energy_collision = []
    for (x, y), (u, v) in (((12, 9), (0, -4)), ((12, 0), (-6, 8))):
        assert x*v != y*u
        squares = (x*x + y*y, u*u + v*v, (x+u)**2 + (y+v)**2)
        masses = tuple(sorted(map(isqrt, squares)))
        assert sorted(squares) == [mass**2 for mass in masses]
        assert sum(masses) == 32
        energy_collision.append(masses)
    assert energy_collision == [(4, 13, 15), (10, 10, 12)]
    return {"squared_norm_cap_on_v_w_and_sum": cap,
            "ordered_rank_two_pairs": sum(triangles.values()),
            "distinct_gram_matrices": len(reconstructed),
            "distinct_mass_triples_at_total_energy_32": energy_collision}


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
            "first_energy_minus": sum(sqrt(norm) for norm in minima[1]),
            "klt_sum_squared_over_first_term_squared": {
                "plus": threshold_tree(minima[0])[0], "minus": threshold_tree(minima[1])[0]},
            "pure_noncompact_graviton_cut": {
                "plus": graviton_cut_fixture(minima[0]), "minus": graviton_cut_fixture(minima[1])}}


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
            "isospectral_pair": isospectral_fixture(),
            "square_lattice_gram_reconstruction": triangle_reconstruction_fixture()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_kk_unitarity.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified the KK cut, KLT polarization channels, and three-body onset coefficients.")


if __name__ == "__main__":
    main()
