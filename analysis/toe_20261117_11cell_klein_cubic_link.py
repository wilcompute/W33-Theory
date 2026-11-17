"""From the 11-cell's PSL2(11) to the Klein cubic and its seven-dimensional link.

The group/cubic identification and KE existence are published inputs.
Polynomial, deformation, Chern and integral Gysin calculations are executed here.
No Standard Model or spacetime dimension is derived from a cell count.
"""
import json
from itertools import product
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


def monomials(degree, variables=5):
    if variables == 1:
        return [(degree,)]
    return [(a,)+tail for a in range(degree+1)
            for tail in monomials(degree-a, variables-1)]


def cubic_calculation():
    x = sp.symbols('x0:5')
    f = sum(x[i]**2*x[(i+1) % 5] for i in range(5))
    weights = (1, 9, 4, 3, 5)
    assert all((2*weights[i]+weights[(i+1) % 5]) % 11 == 0 for i in range(5))
    assert sum(weights) % 11 == 0
    degree3 = monomials(3)
    invariant_monomials = [m for m in degree3 if sum(a*b for a, b in zip(m, weights)) % 11 == 0]
    assert len(invariant_monomials) == 5
    assert set(invariant_monomials) == {tuple(2*(j == i)+(j == (i+1) % 5) for j in range(5))
                                       for i in range(5)}
    # A cyclic coordinate permutation is transitive on these five monomials.
    # Thus the C11:C5-invariant cubic space is exactly the displayed line.
    assert all(2*weights[i] % 11 == -weights[(i+1) % 5] % 11 for i in range(5))
    derivatives = [sp.diff(f, z) for z in x]
    assert sp.expand(sum(z*d for z, d in zip(x, derivatives))-3*f) == 0
    groebner = sp.groebner(derivatives, *x, order='grevlex')
    assert groebner.is_zero_dimensional
    leading = [p.LM(order=groebner.order).exponents for p in groebner.polys]
    hilbert = [sum(not any(all(a >= b for a, b in zip(m, lm)) for lm in leading)
                   for m in monomials(d)) for d in range(7)]
    assert hilbert == [1, 5, 10, 10, 5, 1, 0]
    relations = [sp.Poly(z*d, *x) for z in x for d in derivatives]
    matrix = sp.Matrix([[p.coeff_monomial(m) for p in relations] for m in degree3])
    assert matrix.rank() == 25 and len(degree3)-matrix.rank() == 10
    zero_rows = [i for i, m in enumerate(degree3) if m in invariant_monomials]
    # Weight-zero relations x_i df/dx_i fill the entire invariant degree3 space.
    zero_relations = sp.Matrix([[sp.Poly(x[j]*derivatives[j], *x).coeff_monomial(degree3[i])
                                for j in range(5)] for i in zero_rows])
    assert zero_relations.rank() == 5 and abs(zero_relations.det()) == 33
    assert all(w % 11 for w in weights)
    return dict(polynomial=str(f), C11_weights=list(weights), C11_invariant_cubic_monomials=5,
                C11_semidirect_C5_invariant_cubic_dimension=1,
                smoothness_proof='If one critical coordinate vanishes, all do. Otherwise multiplying '
                    'the five derivative equations gives 32 product(x)^2=-product(x)^2, '
                    'impossible in characteristic zero.',
                Jacobian_Hilbert_dimensions=hilbert, cone_Milnor_number=sum(hilbert),
                cubic_deformation_dimension=10, C11_fixed_cubic_deformations=0,
                H21_dimension=hilbert[1], C11_fixed_H21=0,
                proof_scope='The characteristic-zero polynomial checks are exact. '
                    'Aut(X)=PSL2(11) and KE existence are published inputs, not reclassified here.')


def characteristic_classes():
    h = sp.Symbol('h')
    total = sp.series((1+h)**5/(1+3*h), h, 0, 4).removeO().expand()
    c1, c2, c3 = [total.coeff(h, j) for j in (1, 2, 3)]
    assert (c1, c2, c3) == (2, 4, -2)
    p1 = c1**2-2*c2
    assert p1 == -4
    return dict(total_Chern_polynomial=str(total), degree=3, Euler_X=int(c3*3),
                c1='2H', c2='4H^2', p1='-4H^2=-12L, with H^2=3L and integral(H L)=1',
                base_spin=True, link_spin=True, link_p1_torsion_coefficient_mod3=(-12) % 3,
                link_lambda_p1_over2='0 (multiplication by2 is invertible on Z3)',
                caveat='Vanishing characteristic shift does not determine a Page-charge or brane spectrum.')


def link_gysin():
    # Integral cubic-threefold cohomology ranks and cup-H maps.
    ranks = {0:1, 1:0, 2:1, 3:10, 4:1, 5:0, 6:1}
    def cup(degree):
        target, source = ranks.get(degree+2, 0), ranks.get(degree, 0)
        matrix = sp.zeros(target, source)
        if degree in (0, 2, 4):
            matrix[0, 0] = 3 if degree == 2 else 1
        return matrix
    groups = []
    for degree in range(8):
        incoming, outgoing = cup(degree-2), cup(degree-1)
        smith = smith_normal_form(incoming, domain=ZZ)
        torsion = [abs(int(smith[i, i])) for i in range(min(smith.shape)) if abs(smith[i, i]) > 1]
        free = ranks.get(degree, 0)-incoming.rank()+ranks.get(degree-1, 0)-outgoing.rank()
        groups.append(dict(degree=degree, free_rank=free, torsion=torsion))
    assert [r['free_rank'] for r in groups] == [1, 0, 0, 10, 10, 0, 0, 1]
    assert [r['torsion'] for r in groups] == [[], [], [], [], [3], [], [], []]
    assert sum((-1)**r['degree']*r['free_rank'] for r in groups) == 0
    return dict(circle_Euler_class='H (primitive)', integral_cohomology=groups,
                H3_homology='Z^10 + Z3', flat_C_field_characters='U(1)^10 x Z3',
                two_connected=True, unique_spin_structure=True,
                C11_fixed_continuous_C3_modes=0,
                torsion_C_field_sectors=3,
                torsion_action='C11:C5, and PSL2(11), act trivially on Z3: Aut(Z3)=Z2.',
                torsion_linking_form='plus or minus 1/3 on a generator, depending on orientation',
                caveat='Three discrete flat C-field sectors are not three matter generations.')


def free_order55_quotient():
    weights = (1, 9, 4, 3, 5)
    assert set(weights+tuple((-w) % 11 for w in weights)) == set(range(1, 11))
    elements = list(product(range(11), range(5)))
    def multiply(g, h):
        a, b = g
        c, d = h
        return ((a+pow(9, b, 11)*c) % 11, (b+d) % 5)
    assert len({multiply(g, h) for g in elements for h in elements}) == 55
    fixed_line_checks = []
    for a, b in elements:
        if not b:
            if a:
                assert all(a*w % 11 for w in weights)
            continue
        s = a*pow((1-pow(9, b, 11)) % 11, -1, 11) % 11
        assert all((a*w+s*weights[(i+b) % 5]-s*w) % 11 == 0
                   for i, w in enumerate(weights))
        # Fixed line is D^s*(1,1,1,1,1); every cubic monomial is1 on it.
        assert all((2*s*weights[i]+s*weights[(i+1) % 5]) % 11 == 0 for i in range(5))
        fixed_line_checks.append([a, b, s])
    assert len(fixed_line_checks) == 44
    volume_ratio = sp.Rational(2**4*3, 4**4)
    assert volume_ratio == sp.Rational(3, 16)
    quotient_ratio = volume_ratio/55
    assert quotient_ratio == sp.Rational(3, 880)
    return dict(group='C11 semidirect C5, with P D P^-1=D^9', order=55,
                elements=[list(g) for g in elements], conjugating_powers=fixed_line_checks,
                free_on_link=True,
                freeness_proof='Nonidentity D powers have no eigenvalue1. All other elements '
                    'are conjugate to a nonidentity coordinate5-cycle. Its fixed line has '
                    'f(t,t,t,t,t)=5t^3, so it misses the punctured cone.',
                holomorphic_residue_preserved=True,
                residue_reason='det D=det P=1 and f is invariant; the cone residue4-form is invariant.',
                quotient_pi1='C11:C5', quotient_H1_homology='Z5',
                quotient_rational_Betti_numbers=[1, 0, 0, 0, 0, 0, 0, 1],
                quotient_unique_spin=True,
                quotient_H4_torsion_3_primary='Z3 (coprime-order transfer)',
                full_integral_quotient_cohomology='Not computed; additional5- or11-primary torsion is not excluded.',
                internal_Vol_Y_over_Vol_S7=str(volume_ratio),
                internal_Vol_quotient_over_Vol_S7=str(quotient_ratio),
                quotient_volume='pi^4/880 for Ric=6g',
                leading_AdS4_free_energy='pi*sqrt(1760/27)*N^(3/2), standard large-N holographic formula',
                physics_scope='A free holomorphic volume-preserving quotient of the Sasaki-Einstein '
                    'link gives a smooth supersymmetric Freund-Rubin route. The induced Euclidean '
                    'link metric is not asserted to be Einstein. No SM or flux-sector selection derived.')


if __name__ == '__main__':
    result = dict(status='PASS', cubic=cubic_calculation(), characteristic_classes=characteristic_classes(),
                  seven_link=link_gysin(),
                  free_quotient=free_order55_quotient(),
                  geometry='Y7={f=0} intersect S9 in C5; smooth link of the isolated cone singularity.',
                  metric_input='All smooth cubic threefolds admit KE metrics (Liu-Xu). The associated '
                      'regular Sasaki-Einstein link has Ric(Y)=6g after normalization.',
                  eleven_dimensional_route='Standard supersymmetric Freund-Rubin AdS4 x Y7, with '
                      'AdS radius half internal radius. This is an existing construction applied to '
                      'the Klein cubic, not an observed Standard Model or a new classification theorem.',
                  limitations='No explicit KE metric, complete KK spectrum, physical couplings, '
                      'four-dimensional Minkowski vacuum, SM gauge sector or flux-sector selection computed.')
    output = Path(__file__).resolve().parents[1]/'data/toe_20261117_11cell_klein_cubic_link.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], polynomial=result['cubic']['polynomial'],
                          cohomology=result['seven_link']['integral_cohomology'])))
