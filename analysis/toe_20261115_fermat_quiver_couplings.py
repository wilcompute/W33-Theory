"""Specialize Wijnholt's nine-node superpotential to a marked Fermat cubic."""

from collections import Counter
from itertools import combinations, permutations, product
from math import lcm

import sympy as sp


FIELD = sp.QQ.algebraic_field(sp.sqrt(-3))
OMEGA = FIELD.from_sympy((-1 + sp.sqrt(-3)) / 2)
ONE, ZERO = FIELD.one, FIELD.zero
MARKING = (0, 3, 1, 4, 2, 5)


def determinant(rows):
    size = len(rows)
    if size == 1:
        return rows[0][0]
    return sum(
        ((-1)**column * rows[0][column] * determinant([row[:column] + row[column+1:] for row in rows[1:]])
         for column in range(size)),
        ZERO,
    )


def fermat_lines():
    lines = {}
    for pairing in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
        for a, b in product(range(3), repeat=2):
            i, j, k, l = pairing
            first, second = [ZERO]*4, [ZERO]*4
            first[i], first[j] = -OMEGA**a, ONE
            second[k], second[l] = -OMEGA**b, ONE
            lines[(i, j, a, b)] = [first, second]
    return lines


def plane_through(left, right):
    for rows in combinations(left + right, 3):
        normal = [(-1)**i * determinant([row[:i] + row[i+1:] for row in rows]) for i in range(4)]
        if any(normal):
            return normal
    raise ValueError("Coincident lines")


def fermat_blowup_points(marking=tuple(range(6))):
    lines = fermat_lines()
    exceptional = [lines[(0, 1, a, a)] for a in range(3)]
    exceptional += [lines[(0, 2, a, (a+1) % 3)] for a in range(3)]
    exceptional = [exceptional[i] for i in marking]
    assert all(determinant(left + right) for left, right in combinations(exceptional, 2))
    remaining = {
        tuple(i for i, e in enumerate(exceptional, start=1) if not determinant(e + line)): line
        for line in lines.values() if line not in exceptional
    }
    assert len(remaining) == 21

    def ratio(numerator, denominator, line):
        for vector in line + [[a+t*b for a, b in zip(*line)] for t in (ONE, OMEGA, OMEGA**2)]:
            bottom = sum((x*y for x, y in zip(denominator, vector)), ZERO)
            if bottom:
                top = sum((x*y for x, y in zip(numerator, vector)), ZERO)
                return top / bottom
        raise ValueError("Coordinate divisor contains exceptional line")

    # Divide anticanonical sections sharing the same residual conic Q_j.
    # Their quotient is a ratio of two coordinate linear forms on P^2.
    y_num = plane_through(remaining[(1, 3)], exceptional[0])
    y_den = plane_through(remaining[(2, 3)], exceptional[1])
    z_num = plane_through(remaining[(1, 2)], exceptional[0])
    z_den = plane_through(remaining[(2, 3)], exceptional[2])
    points = [[ONE, ratio(y_num, y_den, line), ratio(z_num, z_den, line)] for line in exceptional[3:]]
    frame = points[0]
    return [[value/scale for value, scale in zip(point, frame)] for point in points[1:]]


def cubic_coefficients(z, w):
    """Eq. (3.35), indexed by nodes 1+i, 4+j, 7+k."""
    z0, z1, z2 = z
    w0, w1, w2 = w
    f1 = (z1-z0)*z2*w0**2 + (z0**2-z1*z2)*w0*w2 + z0*(z2-z0)*w1*w2
    f2 = z0*(z1-z2)*w1*w2 + (z0-z1)*z2*w0*w1 + (z2-z0)*z1*w0*w2
    f3 = -z1*(z2-z1)*w0*w2 - (z0-z1)*z2*w1**2 - (z1**2-z0*z2)*w1*w2
    det = f2**2-f1*f3
    rows = [
        ((ONE, -ONE, ONE), (ONE, -ONE, ONE), (-f2**2-f2*f3, f1*f3+f2*f3, det)),
        ((z2, -z2, z1), (z0, -z1, z1), (-f2*f3*z0-f2**2*z1, f2*f3*z0+f1*f3*z1, z1*det)),
        ((w2, -w2, w1), (w0, -w1, w1), (-f2*f3*w0-f2**2*w1, f2*f3*w0+f1*f3*w1, w1*det)),
    ]
    return {(i, j, k): rows[i][k][j] for i, j, k in product(range(3), repeat=3)}


def check_couplings():
    z, w = fermat_blowup_points(MARKING)
    coeff = cubic_coefficients(z, w)
    assert all(coeff.values())
    alternate = cubic_coefficients(*fermat_blowup_points())
    assert sum(not value for value in alternate.values()) == 3

    def invariant(tensor, i, j, k):
        return (tensor[i,j,k]*tensor[i,0,0]*tensor[0,j,0]*tensor[0,0,k]
                / (tensor[i,j,0]*tensor[i,0,k]*tensor[0,j,k]*tensor[0,0,0]))

    probes = list(product((1, 2), repeat=3))
    base = [invariant(coeff, *key) for key in probes]
    stabilizer = Counter()
    orders = Counter()
    for shift in range(3):
        for maps in product(permutations(range(3)), repeat=3):
            def image(key):
                return tuple(maps[(i+shift) % 3][key[(i+shift) % 3]] for i in range(3))

            pulled_back = {key: coeff[image(key)] for key in coeff}
            if [invariant(pulled_back, *key) for key in probes] == base:
                stabilizer[shift] += 1
                action = {(block, node): ((block-shift) % 3, maps[block][node])
                          for block, node in product(range(3), repeat=2)}
                lengths = []
                while action:
                    first = next(iter(action))
                    target = action.pop(first)
                    length = 1
                    while target != first:
                        target = action.pop(target)
                        length += 1
                    lengths.append(length)
                orders[lcm(*lengths)] += 1

    def display(value):
        return str(FIELD.to_sympy(value))

    return {
        "exceptional_line_marking": MARKING,
        "fermat_marked_points": [[display(v) for v in p] for p in (z, w)],
        "alternate_marking_zero_coefficients": ["".join(str(i+1) for i in key) for key, value in alternate.items() if not value],
        "coefficients": {"".join(str(i+1) for i in key): display(value) for key, value in coeff.items()},
        "field_rescaling_invariants": [display(value) for value in base],
        "directed_stabilizer_by_block_rotation": dict(stabilizer),
        "directed_stabilizer_order": sum(stabilizer.values()),
        "directed_stabilizer_element_orders": dict(sorted(orders.items())),
    }


if __name__ == "__main__":
    print(check_couplings())
