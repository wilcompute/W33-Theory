"""Quadric alternative: local A4 source, real quotient, C4 gauge holonomy.

Companion: analysis/2026-11-18_quadric_local_SU5_and_SM_Wilson.md.
Known V5,2 SE metric/local ADE physics are inputs. Exact geometry, topology,
root and scalar-harmonic controls below do not establish chiral matter,
the full localized supersymmetric action or a selected observed vacuum.
"""
import json
from collections import Counter
from itertools import product
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[1]


def quadric_and_group():
    z = s.symbols('z0:3')
    u, v = s.symbols('u v')
    f = sum(t*t for t in z)+u*v
    assert s.expand(f.subs({u: 2*u, v: v/2})-f) == 0
    # C5 acts(u,v)->(zeta5*u,zeta5^-1*v). Fixed setu=v=0 is the
    # punctured quadratic surface inC3, with transverseA4 quotient.
    # In orthogonal coordinates u=w3+i*w4,v=w3-i*w4, K conjugates allw.
    # Thus K:(z,u,v)->(barz,barv,baru), COMMUTING with the realSO2 action.
    elements = list(product(range(5), range(2)))
    mul = lambda a, b: ((a[0]+b[0]) % 5, (a[1]+b[1]) % 2)
    identity = (0, 0)
    assert len({mul(a, b) for a in elements for b in elements}) == 10
    for a in range(1, 5):
        assert mul((a, 1), (a, 1)) == (2*a % 5, 0) != identity
    # Pure K has no link fixed points: on its fixed real slice the quadric
    # is sum of five REAL squares, zero only at the removed cone vertex.
    return dict(cone='sum_(i=0)^4 w_i^2=0 inC5', link='V5,2',
                local_gauge_group_input='unfrozenA4 -> su5 along Q=V3,2=RP3',
                action='C5 rotates the real(w3,w4) plane; K conjugates allw_i',
                orbifold_group='C5 x C2, order10',
                fixed_holomorphic_locus='u=v=0, sum_(i=0)^2 z_i^2=0',
                transverse_weights=[1, -1],
                all_antiholomorphic_elements_free_on_link=True,
                freeness_argument='K-fixed real positive quadric has no nonzero point. '
                    'If g^a K fixed a point for a!=0, its squareg^(2a) would fix it, '
                    'forcing it intoQ, whereg acts trivially andK is free.',
                underlying_space_pi1='C2, by quotienting the acting group by itsC5 isotropy',
                gauge_locus='Qprime=RP3/K, a spherical3-manifold with pi1=C4',
                spin_input='K preserves J^2/2+ReOmega4 and projects the standardSU4 '
                    'singlet pair to one, as verified in the companionKleinSpin7 producer.')


def gauge_locus_double_cover():
    ar, ai, br, bi = s.symbols('ar ai br bi', real=True)
    a, b = ar+s.I*ai, br+s.I*bi
    def q(a, b):
        return s.Matrix([a*a-b*b, s.I*(a*a+b*b), 2*a*b])
    zz = q(a, b)
    assert s.expand(sum(t*t for t in zz)) == 0
    assert all(s.expand(t) == 0 for t in q(-a, -b)-zz)
    norm = s.expand(sum(t*s.conjugate(t) for t in zz))
    assert s.expand(norm-2*(ar*ar+ai*ai+br*br+bi*bi)**2) == 0
    A = s.Matrix([[0, -s.I], [s.I, 0]])
    lift = A*s.conjugate(s.Matrix([a, b]))
    assert all(s.simplify(t) == 0 for t in q(*lift)-s.conjugate(zz))
    assert A*s.conjugate(A) == -s.eye(2)
    # The real-linear lift is right multiplication byi*sigma_x onSU2.
    G = s.Matrix([[a, -s.conjugate(b)], [b, s.conjugate(a)]])
    right = s.Matrix([[0, s.I], [s.I, 0]])
    lifted_G = s.Matrix([[lift[0], -s.conjugate(lift[1])],
                         [lift[1], s.conjugate(lift[0])]])
    assert all(s.simplify(t) == 0 for t in G*right-lifted_G)
    assert right**2 == -s.eye(2) and right**4 == s.eye(2)
    return dict(covering='S3 -> RP3 -> Qprime; full deck groupC4',
                parametrization=[str(t) for t in q(s.Symbol('a'), s.Symbol('b'))],
                real_involution_lift='(a,b)->(-i*barb,i*bara)',
                lift_square='minus identity', pi1_Qprime='C4', H1_Qprime='Z4',
                H2_Qprime=0, H3_Qprime='Z',
                reason='The free lift has order4, with its square the original '
                    'antipodalC2. This distinguishesC4 fromC2xC2.',
                ambient_inclusion='The gauge-locusC4 maps to ambientC2 by reduction '
                    'mod2; a brane-localized order4 holonomy need not extend to bulk.')


def root_monodromy_and_Wilson():
    roots = [s.eye(5)[:, i]-s.eye(5)[:, i+1] for i in range(4)]
    J = s.zeros(5)
    for i in range(5):
        J[4-i, i] = 1
    assert J.det() == 1 and J**2 == s.eye(5)
    assert all(J*roots[i] == -roots[3-i] for i in range(4))
    # Swap of the ALE coordinates reverses the exceptional chain;
    # anti-holomorphic conjugation reverses each curve's orientation.
    # Combined action is minus-reversal, the INNER longest Weyl element.
    cases = []
    for color, weak in product(range(4), repeat=2):
        if (3*color+2*weak) % 4 or color == weak:
            continue
        charges = [color]*3+[weak]*2
        invariant = 4+sum(i != j and (charges[i]-charges[j]) % 4 == 0
                          for i in range(5) for j in range(5))
        assert invariant == 12
        cases.append(dict(color_charge=color, weak_charge=weak,
                          order=2 if (color, weak) == (0, 2) else 4,
                          adjoint_character_multiplicities=dict(Counter(
                              [0]*4+[(charges[i]-charges[j]) % 4
                                      for i in range(5) for j in range(5) if i != j])),
                          unbroken_dimension=invariant))
    assert [(r['color_charge'], r['weak_charge']) for r in cases] == [(0, 2), (2, 1), (2, 3)]
    W = s.diag(-1, -1, -1, s.I, s.I)
    assert W.det() == 1 and W**4 == s.eye(5) and W**2 != s.eye(5)
    all_count_patterns = []
    for n0, n1, n2 in product(range(6), repeat=3):
        n3 = 5-n0-n1-n2
        if n3 >= 0 and (n1+2*n2+3*n3) % 4 == 0:
            all_count_patterns.append([n0, n1, n2, n3])
    return dict(A4_cycle_action='[E_i]->-[E_(5-i)]',
                cycle_action_equals_longest_Weyl=True,
                no_forced_outer_Dynkin_folding=True,
                monodromy_scope='The cycle action is inner, so the gauge algebra can '
                    'be described as anSU5 bundle after inner untwisting. This does not '
                    'automatically choose a flat connection or breakSU5.',
                chosen_Wilson_matrix='diag(-1,-1,-1,i,i)',
                chosen_character_charges=[2, 2, 2, 1, 1],
                chosen_holonomy_order=4, centralizer='S(U3 x U2)',
                centralizer_Lie_algebra='su3+su2+u1', centralizer_dimension=12,
                all_3plus2_C4_choices=cases,
                all_SU5_C4_conjugacy_multiplicity_patterns=all_count_patterns,
                flat_local_system_cohomology_dimensions=[12, 0, 0, 12],
                cohomology_reason='Over characteristic zero, averaging over the '
                    'finiteC4 deck group is exact and S3 has onlyH0,H3. The adjoint '
                    'invariant space has dimension12. This is local-system cohomology, '
                    'not the full flux-coupled physical multiplet spectrum.',
                vacuum_selection='All flat choices, including trivial holonomy with '
                    'unbrokenSU5, haveF=0 and zero classical Yang-Mills energy. '
                    'No dynamical selection of the SM sectors is proved.',
                global_group_scope='Uses the simply connectedSU5 lift. Global electric '
                    'charge form and full orbifold C-field gluing remain uncomputed.')


def volumes_and_vector_KK():
    degree, index = 2, 3
    base_curve_area = s.pi*s.Rational(index, 4)*2
    Reeb_period = 2*s.pi*s.Rational(index, 4)
    Qvolume = s.simplify(base_curve_area*Reeb_period)
    assert Qvolume == 9*s.pi**2/4
    Qprime = Qvolume/2
    cover_ratio = s.Rational(degree*index**4, 4**4)
    assert cover_ratio == s.Rational(81, 128)
    cover_volume = cover_ratio*s.pi**4/3
    assert cover_volume == 27*s.pi**4/128
    orbifold_volume = cover_volume/10
    # SU2 left-invariant one-forms normalized so(a,c)=(1,1) is unitS3.
    horizontal2, fiber2 = s.Rational(3, 2), s.Rational(9, 4)
    assert 2*s.pi**2*horizontal2*s.sqrt(fiber2)/4 == Qprime
    def eigen(ell, m):
        return ell*(ell+2)/horizontal2+(1/fiber2-1/horizontal2)*m*m
    first = {}
    for character in range(4):
        allowed = []
        for ell in range(13):
            for m in range(ell, -1, -2):
                chars = [ell % 4] if m == 0 else [ell % 4, (ell+2) % 4]
                if character in chars:
                    allowed.append((eigen(ell, m), ell, m))
        first[character] = min(allowed)
    assert [first[k][0] for k in range(4)] == [0, s.Rational(16, 9), s.Rational(40, 9), s.Rational(16, 9)]
    # This finite scan has an analytic tail bound: eigen >=(4/9)ell^2+(4/3)ell.
    for ell in range(13):
        assert s.simplify(eigen(ell, ell)-(s.Rational(4, 9)*ell**2+s.Rational(4, 3)*ell)) == 0
    assert eigen(3, 3) > s.Rational(40, 9)
    # StandardFR quantization6R^6Vol=(2pi lp)^6 N, no finite-N/Page shifts.
    R6_over_lp6_per_N = s.simplify((2*s.pi)**6/(6*orbifold_volume))
    assert R6_over_lp6_per_N == s.Rational(40960, 81)*s.pi**2
    gauge_geometric_coefficient = s.simplify(Qprime*s.sqrt(R6_over_lp6_per_N))
    assert gauge_geometric_coefficient == 8*s.sqrt(10)*s.pi**3
    return dict(Vol_V52=str(cover_volume), Vol_total_quotient=str(orbifold_volume),
                gauge_Qprime_volume=str(Qprime),
                Berger_lift_horizontal_radius_squared=str(horizontal2),
                Berger_lift_fiber_radius_squared=str(fiber2),
                scalar_eigenvalue_formula='(2/3)ell(ell+2)-(2/9)m^2; m=-ell,-ell+2,...,ell',
                deck_generator='right multiplication byi*sigma_x, square=-I',
                deck_character_rule='On each nonzero|m| pair: characters i^ell and-i^ell; '
                    'the m0 line has i^ell. Left degeneracyell+1.',
                first_scalar_eigenvalues_by_C4_character={str(k): str(first[k][0]) for k in first},
                analytic_tail_bound='lambda >=(4/9)ell^2+(4/3)ell, increasing; ell>=3 '
                    'is above both displayed nontrivial minima.',
                broken_vector_mass2_AdS_units_order4='4/9',
                broken_vector_mass2_AdS_units_order2='10/9',
                vector_scope='The two-derivative localized gauge action, using internal '
                    'scalar harmonics for external vector components. Not the full '
                    'fermion/scalar/brane coupled spectrum.',
                R6_over_lp6_per_flux_N=str(R6_over_lp6_per_N),
                tree_g4_inverse_squared='8*pi^3*sqrt(10*N)/c, ifg7^2=c*lp^3',
                tree_unification='g3=g2=g5, gY^2=(3/5)g5^2; sin^2thetaW=3/8 at the '
                    'unmatchedcompactification scale, standardSU5 normalization.',
                limitation='Order5, fluxN and flat holonomy are choices. Broken gauge '
                    'masses remain at the AdS scale; no parametric scale separation '
                    'or observed coupling/cosmology follows.')


def extra_vectors_and_simple_deformation_obstruction():
    pairs = [(i, j) for i in range(5) for j in range(i+1, 5)]
    variables = s.symbols('a0:10')
    general = s.zeros(5)
    for a, (i, j) in zip(variables, pairs):
        general[i, j], general[j, i] = a, -a
    rotation = s.zeros(5)
    rotation[3, 4], rotation[4, 3] = 1, -1
    commutator = general*rotation-rotation*general
    constraints = s.Matrix(list(commutator)).jacobian(variables)
    assert constraints.rank() == 6
    centralizer = 10-constraints.rank()
    assert centralizer == 4
    bp = []
    for p in range(2, 13):
        index_fraction = s.Rational(3, 2)+s.Rational(2, p)-1
        u_charge = s.Rational(4, p)/index_fraction
        bp.append(dict(p=p, minimal_u_v_charge=str(u_charge),
                       Lichnerowicz_obstructed=bool(u_charge < 1)))
    assert next(r for r in bp if r['p'] == 5)['minimal_u_v_charge'] == '8/9'
    assert all(r['Lichnerowicz_obstructed'] for r in bp if r['p'] >= 5)
    return dict(surviving_geometric_continuous_algebra='so3 + so2',
                geometric_KK_vector_dimension=centralizer,
                Reeb_U1_projected_by_K=True,
                actual_claim='The12-dimensional result is a localized SM subsector, '
                    'not the full gauge algebra. Four additional geometric vector '
                    'candidates survive the simple quotient.',
                Brieskorn_controls=bp,
                deformation_family='z0^2+z1^2+z2^2+u^p+v^p, p>=5',
                obstruction='Addingu^5+v^5 is a tempting way to remove the normal '
                    'uv phase isometry while preservingC5. In the stated family '
                    'the u,v Reeb charge is4/(p/2+2)<1. A holomorphic harmonic '
                    'would have lambda=q(q+6)<7, violating Lichnerowicz for Ric=6g.',
                scope='This rules out that specific SE deformation family. It is '
                    'not a no-go for all nonhomogeneous cones, flux deformations or gauge completions.')


if __name__ == '__main__':
    result = dict(status='PASS', geometry=quadric_and_group(),
                  gauge_locus=gauge_locus_double_cover(),
                  gauge=root_monodromy_and_Wilson(), spectrum=volumes_and_vector_KK(),
                  extra_gauge_and_obstruction=extra_vectors_and_simple_deformation_obstruction(),
                  limits='No chiral families, anomaly completion, full localized '
                    'supersymmetric action, flux/Page/gluing completion, vacuum selection '
                    'or observedTOE derived. The proposed gauge geometry is a candidate.')
    (ROOT/'data/toe_20261118_quadric_A4_C4_SM_gauge.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], local_ADE='A4',
                         gauge_locus_pi1='C4', unbroken_gauge_dimension=12,
                         broken_vector_mass2_AdS='4/9')))
