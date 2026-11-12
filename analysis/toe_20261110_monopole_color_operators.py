"""Residual color and Pauli constraints for W33 monopole boundary operators."""

from collections import Counter
import json

import sympy as sp

import toe_20261110_monopole_boundary_lattice as boundary

OUT = 'data/toe_20261110_monopole_color_operators.json'
COLOR_ROOT = (2, -1, 0, 0, 0, 0)
WINO_NUMBER = (0, 0, -3, 1, -4, 0)


def flavor_weights():
    charged, alpha, m, fundamental = boundary.angular_weights()
    direct, holes, paired = boundary.signed_pairs(charged[-1], charged[1], alpha)
    in_bl = {1: (1, 0), 2: (-1, 0), 6: (0, -1)}
    out_bl = {-4: (-1, 0), -3: (0, 1), 1: (1, 0)}
    incoming = [w + in_bl[w[-1]] for w in direct] * 3 + [w + (0, 0) for w in holes]
    outgoing = [w + out_bl[w[-1]] for w in paired] * 3
    outgoing += [boundary.negative(w) + (0, 0) for w in holes]
    assert sp.Matrix(COLOR_ROOT[:4]).dot(m) == 0
    # The defining five restricts to the unique color doublet plus three singlets.
    doublet = [tuple(fundamental[:, i]) for i in range(fundamental.cols)
               if abs(fundamental[0, i]) == 1 and fundamental[3, i] == -2]
    assert len(doublet) == 2
    assert boundary.add(max(doublet), boundary.negative(min(doublet))) == COLOR_ROOT[:4]
    for states in [incoming, outgoing]:
        assert all(w[0] in (-1, 0, 1) for w in states)
        counts = Counter(states)
        assert all(counts[w] == counts[boundary.add(w, COLOR_ROOT)]
                   for w in counts if w[0] == -1)
        assert all(counts[w] == counts[boundary.add(w, boundary.negative(COLOR_ROOT))]
                   for w in counts if w[0] == 1)
    return incoming, outgoing, alpha


def wino_number(weight):
    numerator = sum(q * c for q, c in zip(weight, WINO_NUMBER))
    number, remainder = divmod(numerator, 6)
    assert not remainder
    return number


def exterior_characters(particle_and_hole, maximum):
    layers = [Counter() for _ in range(maximum + 1)]
    layers[0][(0,) * 6] = 1
    for weight in particle_and_hole:
        for count in range(maximum, 0, -1):
            for total, multiplicity in layers[count - 1].items():
                layers[count][boundary.add(total, weight)] += multiplicity
    for count, layer in enumerate(layers):
        assert sum(layer.values()) == sp.binomial(len(particle_and_hole), count)
    return layers


def irrep_multiplicity(character, highest):
    # Adding the simple root raises 2J3 by two and fixes all central charges.
    assert highest[0] >= 0
    result = character(highest) - character(boundary.add(highest, COLOR_ROOT))
    assert result >= 0
    return result


def local_operators(incoming, outgoing):
    wino = (0, 0, -2, 0, 0, 0)
    assert [w for w in outgoing if wino_number(w)] == [wino]
    particles_and_holes = outgoing + list(map(boundary.negative, outgoing))
    layers = exterior_characters(particles_and_holes, 7)

    def one_derivative(count, weight):
        return sum(layers[count - 1][boundary.add(weight, boundary.negative(mode))]
                   for mode in particles_and_holes)

    # Per fixed incoming family and per complete residual SU(2) multiplet.
    expected = {
        (1, -1, 1, 1, 1, 0): ('Q', 3, 6, 5, -1, 0, 36),
        (0, -1, 0, 2, -1, 0): ('Dc', 3, 3, 5, 1, 0, 45),
        (0, 0, 0, 6, 0, -1): ('Ec', 3, 3, 5, 1, 0, 27),
        (0, 0, 1, 3, 0, 0): ('Hu Higgsino', 1, 1, 7, 1, 1, 81),
        (1, -2, 0, 0, 0, 0): ('gluino', 1, 1, 7, -1, 1, 30),
        (0, 0, 2, 0, 0, 0): ('wino', 1, 1, 7, -1, 0, 30),
    }
    highest = Counter(w for w in incoming if w[0] >= 0)
    assert set(highest) == set(expected)
    results = {}
    for weight, (name, k0, m0, k1, delta, derivatives, m1) in expected.items():
        conserving = {count: irrep_multiplicity(layers[count].__getitem__, weight)
                      for count in (1, 3, 5, 7)}
        assert min(count for count, number in conserving.items() if number) == k0
        assert conserving[k0] == m0
        first = {}
        for count in (1, 3, 5, 7):
            for dl in range(-count - 1, count + 2):
                if not dl:
                    continue
                target = boundary.add(weight, (0, 0, 0, 0, 3 * dl, dl))
                net_wino = wino_number(target)
                assert net_wino == wino_number(weight) - 2 * dl
                undifferentiated = irrep_multiplicity(layers[count].__getitem__, target)
                if abs(net_wino) > 1:
                    assert undifferentiated == 0
                if undifferentiated:
                    first.setdefault((count, 0), {})[dl] = undifferentiated
                if count >= 3:
                    differentiated = irrep_multiplicity(lambda w: one_derivative(count, w), target)
                    if differentiated:
                        first.setdefault((count, 1), {})[dl] = differentiated
        assert min(first) == (k1, derivatives)
        assert first[(k1, derivatives)] == {delta: m1}
        # The lower bound on particle multiplicity is independent of derivatives.
        # It follows from the charge-sum enumeration in the preceding certificate.
        if derivatives:
            assert wino_number(weight) == 0
            assert not any(order == 0 for _, order in first)
        results[name] = dict(highest_weight=weight, incoming_family_copies=highest[weight],
                             color_dimension=weight[0] + 1,
                             conserving_outgoing_fermions=k0, conserving_copies=m0,
                             violating_outgoing_fermions=k1, delta_b_equals_delta_l=delta,
                             minimum_radial_derivatives=derivatives, violating_copies=m1,
                             free_boundary_dimension=(1 + k1) // 2 + derivatives,
                             net_violating_winos=wino_number(weight) - 2 * delta)
    return results


def color_current_check(incoming, outgoing):
    # Currents have bosonized exponent e_high - e_low for each color doublet.
    # Check each root exponent, including the sign-reversed outgoing gluino.
    root = COLOR_ROOT
    eye = sp.eye(16)
    incoming_roots = []
    for low, weight in enumerate(incoming):
        if weight[0] == -1:
            high, = [j for j in range((low // 4) * 4, (low // 4 + 1) * 4)
                     if incoming[j] == boundary.add(weight, root)]
            incoming_roots.append(eye[:, high] - eye[:, low])
    assert len(incoming_roots) == 4
    signs = sp.diag(*([1] * 12 + [-1] * 4))
    particle_weights = boundary.columns(outgoing)
    for blocks in [[range(12)], [range(4 * a, 4 * a + 4) for a in range(3)]]:
        gluing = signs
        for block in blocks:
            gluing = gluing * boundary.reflection(block)
        images = [gluing * exponent for exponent in incoming_roots]
        for image in images:
            assert sorted(v for v in image if v) == [-1, 1]
            assert particle_weights * image == sp.Matrix(root)
    return dict(incoming_doublet_current_exponents=len(incoming_roots),
                both_gluings_send_each_to_an_outgoing_root_exponent=True)


def calculate():
    incoming, outgoing, alpha = flavor_weights()
    phase_contribution = sp.Rational(sum(q * c for q, c in zip(alpha, WINO_NUMBER)), 6)
    assert phase_contribution == -sp.Rational(1, 3)
    return dict(status='PASS', residual_group='S(U(1) x U(2) x U(1) x U(1))',
                color_root=COLOR_ROOT[:4], charge_labels=['c1', 'c2', '2T3', '6Y', '3B', 'L'],
                wino_number_numerator=WINO_NUMBER, wino_number_denominator=6,
                phase_exchange_wino_shift_per_root_step=str(phase_contribution),
                local_operators=local_operators(incoming, outgoing),
                gluing_color_current_exponents=color_current_check(incoming, outgoing))


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2, default=int) + '\n'
    (boundary.core.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
