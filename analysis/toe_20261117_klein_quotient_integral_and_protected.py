"""Integral topology and a protected harmonic subsector of the free Klein-link quotient.

Parent: toe_20261117_11cell_klein_cubic_link.py, commit3095ad3e9.
The report supplies the Poincare-duality and Cartan-Leray arguments; these
checks certify their finite arithmetic, a universal pairing model, Chern
restrictions and two independent invariant-series counts. This is not a
triangulation computation or a complete supergravity spectrum.
"""
import json
from itertools import combinations, product
from pathlib import Path

import sympy as s
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

from toe_20261117_11cell_klein_cubic_link import monomials

WEIGHTS = (1, 9, 4, 3, 5)
ROOT = Path(__file__).resolve().parents[1]


def integral_coinvariant_argument():
    # A model for a unimodular alternating lattice with cyclotomic D.
    # It checks universal pairing identities, not an identified H3(X) basis.
    D = s.zeros(10)
    D[1:10, 0:9] = s.eye(9)
    D[:, 9] = -s.ones(10, 1)
    B = s.zeros(10)
    for i in range(9):
        B[i, i+1], B[i+1, i] = 1, -1
    assert B.det() == 1 and D.T*B*D == B
    assert D**11 == s.eye(10)
    t = s.Symbol('t')
    assert D.charpoly(t).as_expr() == sum(t**i for i in range(11))
    A = D-s.eye(10)
    smith = smith_normal_form(A, domain=ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(10)]
    assert diagonal == [1]*9+[11]
    pairing = B*A.inv()
    integral = lambda m: all(v.q == 1 for v in m)
    assert integral(pairing-pairing.T)
    assert integral(A.T*pairing) and integral(pairing*A)
    # Nondegenerate mod-Z pairing: the radical is exactly A Z^10.
    assert integral(pairing*A) and abs(pairing.det()) == s.Rational(1, 11)
    factors = {}
    for k in range(1, 11):
        comparison = B*(D**k-s.eye(10)).inv()
        multiplier = pow(k, -1, 11)
        assert integral(comparison-multiplier*pairing)
        factors[k] = multiplier
    inverse_conjugation = pow(9, -1, 11)
    assert inverse_conjugation == 5 and factors[5] == 9
    # Negative control: the ordinary cyclotomic lattice has the same rational
    # character but its natural semilinear P preserves the Z11 coinvariant.
    # It cannot preserve a unimodular symplectic form. Dropping the actual
    # Poincare-duality pairing would therefore give the wrong quotient group.
    e0 = s.eye(10)[:, 0]
    natural_P = s.Matrix.hstack(*[D**(9*j)*e0 for j in range(10)])
    assert natural_P**5 == s.eye(10)
    assert natural_P*D*natural_P.inv() == D**9
    assert natural_P.trace() == 0
    assert integral(A.inv()*(natural_P-s.eye(10)))
    assert natural_P.T*B*natural_P != B
    # Positive control: use the G-stable ideal (zeta-1)^3 instead.
    # In its natural integral basis, P=(1+D+...+D^8)^3 natural_P.
    cyclotomic_unit = sum((D**j for j in range(9)), s.zeros(10))
    symplectic_P = cyclotomic_unit**3*natural_P
    alternating_coefficients = [0, 3, -4, 3, -2, 2, -2, 2, -3, 4, -3]
    symplectic_B = s.Matrix(10, 10, lambda i, j: alternating_coefficients[(j-i) % 11])
    assert symplectic_B.det() == 1
    assert symplectic_P**5 == s.eye(10)
    assert symplectic_P*D == D**9*symplectic_P
    assert D.T*symplectic_B*D == symplectic_B
    assert symplectic_P.T*symplectic_B*symplectic_P == symplectic_B
    assert integral(A.inv()*(symplectic_P-3*s.eye(10)))
    full_smith = smith_normal_form(s.Matrix.hstack(A, symplectic_P-s.eye(10)), domain=ZZ)
    assert [abs(full_smith[i, i]) for i in range(10)] == [1]*10
    # For the ACTUAL cubic H3 lattice, P preserves its unimodular
    # alternating form. Therefore b(Px,Py)=9 b(x,y) on Z11, so alpha^2=9.
    # P^5=1 selects alpha=3, independent of any integral basis choice.
    roots = [a for a in range(1, 11) if a*a % 11 == 9 and pow(a, 5, 11) == 1]
    assert roots == [3]
    assert s.gcd(roots[0]-1, 11) == 1
    return dict(cyclotomic_D_minus_I_Smith=diagonal,
                pairing_model_determinant=str(pairing.det()),
                inverse_power_pairing_multipliers=factors,
                actual_lattice_inputs='H3 of a smooth cubic threefold is a rank10 unimodular '
                    'symplectic lattice; D has characteristic polynomial Phi11; P is symplectic '
                    'and P D P^-1=D^9. Parent establishes the rational character.',
                pairing_proof='b(x,y)=B(x,(D-1)^(-1)y) mod Z is a perfect symmetric pairing '
                    'on L/(D-1)L=Z11. P^-1 D P=D^5 implies b(Px,Py)=9 b(x,y). '
                    'The scalar alpha obeys alpha^2=9 and alpha^5=1, hence alpha=3.',
                C5_action_on_C11_coinvariant=roots[0],
                full_group_coinvariant_free_lattice=0,
                negative_control='The natural semilinear action on Z[zeta11] has the '
                    'same rational character but acts as1 on its Z11 coinvariant. It '
                    'does not preserve the unimodular symplectic form; rational '
                    'character data alone would leave an erroneous order11 sector.',
                positive_control=dict(ideal='(zeta11-1)^3 Z[zeta11]',
                    P_matrix=[list(map(int, symplectic_P.row(i))) for i in range(10)],
                    B_circulant_coefficients=alternating_coefficients,
                    B_determinant=1, full_coinvariant_Smith=[1]*10,
                    P_action_on_C11_coinvariant=3,
                    scope='An explicit admissible integral symplectic F55 model, not a '
                        'proved identification with the cubic period lattice. The '
                        'basis-independent argument supplies the actual cubic conclusion.'),
                scope='The companion matrix is a universal arithmetic control, not an '
                    'assertion that its symplectic basis is the cubic period lattice.')


def quotient_groups():
    # LHS: at prime11 use C5 invariants of H_(2k-1)(C11)=Z11.
    # Conjugation acts by9^k. At prime5 the C11 rows vanish after localization.
    group_homology = []
    for n in range(1, 5):
        at5 = 5 if n % 2 else 1
        at11 = 11 if n % 2 and pow(9, (n+1)//2, 11) == 1 else 1
        group_homology.append(dict(degree=n, torsion_order=at5*at11))
    assert [r['torsion_order'] for r in group_homology] == [5, 1, 5, 1]
    # In total degree3, Cartan-Leray has only (0,3)=Z3 and (3,0)=Z5.
    # The only possible incoming differential to (0,3) is d4 from H4(G)=0.
    # There are no other incoming/outgoing maps because H1(Y)=H2(Y)=0.
    homology = [dict(degree=n, free_rank=int(n in (0, 7)),
                     torsion=([5] if n in (1, 5) else [15] if n == 3 else []))
                for n in range(8)]
    cohomology = []
    for n in range(8):
        # UCT: Hom(H_n,Z) plus Ext(H_(n-1),Z).
        torsion = homology[n-1]['torsion'] if n else []
        cohomology.append(dict(degree=n, free_rank=homology[n]['free_rank'], torsion=torsion))
    for n in range(8):
        assert homology[7-n]['free_rank'] == cohomology[n]['free_rank']
        assert homology[7-n]['torsion'] == cohomology[n]['torsion']
    assert sum((-1)**n*homology[n]['free_rank'] for n in range(8)) == 0
    return dict(group_homology_through_degree4=group_homology,
                Cartan_Leray_total_degree3=[dict(p=0, q=3, group='Z3'),
                                           dict(p=3, q=0, group='Z5')],
                extension='0 -> Z3 -> H3(M) -> Z5 -> 0; coprime primary parts give Z15.',
                integral_homology=homology, integral_cohomology=cohomology,
                positive_degree_ring_generators={'u': {'degree': 2, 'order': 5},
                    'v': {'degree': 4, 'order': 3}, 'orientation': {'degree': 7, 'order': 'infinite'}},
                ring_products='u^2 generates the5-primary part of H4; u^3 generates H6. '
                    'All other positive-degree products vanish by coprime torsion or dimension.',
                ring_proof='At prime5, D-1 has determinant11 and is invertible on the cover '
                    'middle lattices. Normal C11 invariants therefore kill rows3 and4 of '
                    'the cohomological Cartan-Leray sequence. Below degree7 the edge map '
                    'H*(BF55,Z_(5))->H*(M,Z_(5)) is an isomorphism of rings. Its generator '
                    'u has degree2 and5u=0; u^2,u^3 survive. At prime3 only H4 torsion remains.',
                flat_degree4_C_field_group='Z15',
                flat_C_field_sector_count=15,
                supersedes='Parent3095ad3e9 left5/11-primary quotient torsion uncomputed. '
                    'The new argument gives Z5 plus Z3 in H4, and no11-primary part.',
                not_computed='5-primary linking unit/quadratic refinement, '
                    'Page-charge shifts and a wrapped-brane dictionary.')


def tangent_and_flux_shift():
    rows = []
    for prime, weights in ((11, WEIGHTS), (5, tuple(range(5)))):
        chern = [sum(s.prod(term) for term in combinations(weights, k)) for k in range(1, 6)]
        residues = [int(c % prime) for c in chern]
        assert residues[:2] == [0, 0]
        rows.append(dict(subgroup_order=prime, weights=list(weights),
                         integral_elementary_coefficients=list(map(int, chern)),
                         Chern_residues=residues))
    assert s.gcd(5, 11) == 1
    return dict(restrictions=rows,
                stable_real_tangent='TM plus R^3 is the real bundle associated to rho:C11:C5 -> SU5.',
                exact_sequence='On the punctured invariant hypersurface, T(cone) plus C = '
                    'C^5_rho equivariantly, because df has trivial target; radial restriction '
                    'gives the stated stable real tangent bundle downstairs.',
                transfer_argument='Both Sylow restrictions of c2(rho) vanish. Transfer then '
                    'annihilates c2 by both5 and11, hence c2=0 integrally on BG.',
                p1=0, spin_lambda_p1_over2=0,
                lambda_reason='For an SU bundle lambda(real rho)=-c2(rho). Stable pullback '
                    'therefore gives lambda(TM)=0, including all torsion.',
                string_structure_exists=True,
                string_structure_unique='H3(M,Z)=0, so the set of lifts has one homotopy class.',
                quantization_scope='No internal gravitational half-shift in the usual '
                    '[G4/(2pi)]-lambda/2 integral law. A flat torsion class is not de Rham '
                    'G4 flux. This does not compute the electric M2 Page charge or one-loop terms.')


def protected_invariants():
    t = s.Symbol('t')
    # Exact C11 invariant series, reducing every coordinate exponent modulo11.
    numerator = [0]*51
    for powers in product(range(11), repeat=5):
        if sum(a*b for a, b in zip(powers, WEIGHTS)) % 11 == 0:
            numerator[sum(powers)] += 1
    assert sum(numerator) == 11**4
    hc11 = sum(c*t**i for i, c in enumerate(numerator))/(1-t**11)**5
    # Each nonidentity C5 power is a5-cycle; diagonal conjugates have the
    # same trace generating function1/(1-t^5).
    ambient = s.cancel((hc11+4/(1-t**5))/5)
    cone = s.factor(s.cancel((1-t**3)*ambient))
    direct_ambient = []
    direct_cone = []
    for degree in range(19):
        weight_zero = [m for m in monomials(degree)
                       if sum(a*b for a, b in zip(m, WEIGHTS)) % 11 == 0]
        # Independent orbit enumeration, rather than relying on Burnside.
        orbits = {min(tuple(m[k:]+m[:k]) for k in range(5)) for m in weight_zero}
        direct_ambient.append(len(orbits))
        direct_cone.append(len(orbits)-(direct_ambient[degree-3] if degree >= 3 else 0))
    series = s.series(cone, t, 0, 19).removeO().expand()
    assert [int(series.coeff(t, d)) for d in range(19)] == direct_cone
    assert direct_cone[:13] == [1, 0, 0, 0, 1, 3, 3, 5, 6, 9, 13, 16, 20]
    assert s.cancel(cone.subs(t, 1/t)-t**2*cone) == 0
    algebraic_pole = s.limit((1-t)**4*cone, t, 1)
    assert algebraic_pole == s.Rational(3, 55)
    # Residue Omega has ordinary degree5-3=2; normalize its Reeb charge to4.
    coordinate_Reeb_charge = s.Rational(4, 5-3)
    volume_ratio = algebraic_pole/coordinate_Reeb_charge**4
    assert volume_ratio == s.Rational(3, 880)
    x = s.symbols('x0:5')
    quartic = sum(x[i]**2*x[(i+2) % 5]*x[(i+4) % 5] for i in range(5))
    quartic_terms = s.Poly(quartic, *x).monoms()
    assert all(sum(a*b for a, b in zip(m, WEIGHTS)) % 11 == 0 for m in quartic_terms)
    assert len({tuple(m[k:]+m[:k]) for m in quartic_terms for k in range(5)}) == 5
    q = int(4*coordinate_Reeb_charge)
    laplacian = q*(q+6)
    assert q == 8 and laplacian == 112
    spin2_dimension = s.Rational(q, 2)+3
    assert spin2_dimension*(spin2_dimension-3) == s.Rational(laplacian, 4)
    return dict(ambient_Hilbert_series=str(s.factor(ambient)), cone_Hilbert_series=str(cone),
                cone_dimensions_degrees0_through18=direct_cone,
                verified_degree_count=len(direct_cone),
                first_nonconstant_degree=4, first_invariant=str(quartic),
                first_Reeb_charge=q, first_holomorphic_scalar_Laplacian=laplacian,
                associated_spin2_mass_squared_AdS_units=laplacian//4,
                associated_spin2_CFT_dimension=int(spin2_dimension),
                algebraic_pole_coefficient=str(algebraic_pole),
                Gorenstein_reciprocity='H(1/t)=t^2 H(t)',
                coordinate_Reeb_charge=int(coordinate_Reeb_charge),
                independent_volume_over_S7=str(volume_ratio),
                charge4_holomorphic_marginal_functions=direct_cone[2],
                continuous_flat_C3_modes=0,
                marginal_scope='No charge4 holomorphic functions, hence no deformations '
                    'in the standard holomorphic superpotential/flux class of Ashmore1809.03503. '
                    'This does not classify every modulus or every quantum deformation.',
                spectrum_scope='Only the holomorphic harmonic subsector and its spin2 lift. '
                    'Not the lowest eigenvalue of the full scalar Laplacian or full KK spectrum.')


if __name__ == '__main__':
    result = dict(status='PASS', parent='3095ad3e9',
                  coinvariants=integral_coinvariant_argument(),
                  quotient=quotient_groups(), tangent=tangent_and_flux_shift(),
                  protected=protected_invariants(),
                  scope='Exact arithmetic plus the written topological derivation. '
                    'No observed SM, physical family count or complete TOE derived.')
    output = ROOT/'data/toe_20261117_klein_quotient_integral_and_protected.json'
    output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], H4='Z15', lambda_class=0,
                         protected_dimensions=result['protected']['cone_dimensions_degrees0_through18'],
                         volume_ratio=result['protected']['independent_volume_over_S7'])))
