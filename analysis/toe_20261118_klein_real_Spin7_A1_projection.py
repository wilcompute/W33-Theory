"""Real involution of the Klein link: spin projection, A1 strata and Wilson cost.

Companion exact odd-Weil generator: toe_20261118_klein_odd_Weil_fixed_strata.g.
Published SE existence, Spin7 anti-holomorphic quotient construction and local
M-theory ADE physics are inputs. No chiral SM or completed quantum orbifold.
Companion proof: analysis/2026-11-18_Klein_Weil_ADE_and_real_Spin7.md.
"""
import json
from itertools import product
from pathlib import Path

import sympy as s
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def group_and_isotropy(with_P):
    size_b = 5 if with_P else 1
    elements = list(product(range(11), range(size_b), range(2)))
    def mul(g, h):
        a, b, e = g
        c, d, f = h
        return ((a+pow(9, b, 11)*(-1)**e*c) % 11, (b+d) % size_b, (e+f) % 2)
    identity = (0, 0, 0)
    inverse = {g: next(h for h in elements if mul(g, h) == identity) for g in elements}
    involutions = [g for g in elements if g != identity and mul(g, g) == identity]
    reflections = [(a, 0, 1) for a in range(11)]
    assert involutions == reflections
    # Every other antiholomorphic element has nonidentity holomorphic square,
    # which is free on Y by the parent F55 result. Thus it cannot fix a point.
    for g in elements:
        if g[2] and g not in reflections:
            assert mul(g, g) != identity and mul(g, g)[2] == 0
    for a in range(11):
        h = (a, 0, 0)
        assert mul(mul(h, (0, 0, 1)), inverse[h]) == (2*a % 11, 0, 1)
    assert len({2*a % 11 for a in range(11)}) == 11
    for g, h in product(reflections, repeat=2):
        if g != h:
            gh = mul(g, h)
            assert gh[0] != 0 and gh[1:] == (0, 0)
    # Normal closure of all nonempty isotropy subgroups. Each reflection's
    # fixed locus is a conjugate of the nonempty real locus, and two are disjoint.
    normal = {identity}
    queue = [identity]
    for g in queue:
        for h in reflections:
            k = mul(g, h)
            if k not in normal:
                normal.add(k)
                queue.append(k)
    assert len(normal) == 22
    assert all(mul(mul(g, h), inverse[g]) in normal for g in elements for h in normal)
    return dict(group_order=len(elements), normal_forms='D^a P^b K^e; K D K=D^-1, K P K=P',
                antiholomorphic_involution_count=len(reflections),
                other_antiholomorphic_elements_free=True,
                pairwise_disjoint_reflection_fixed_loci=True,
                isotropy_normal_closure_order=len(normal),
                underlying_quotient_pi1='C5' if with_P else 'trivial',
                orbifold_pi1='(C11:C5):C2' if with_P else 'dihedral22',
                singular_set='R/C5' if with_P else 'R',
                R='Y intersect R5, a smooth compact real3-manifold; connectedness not computed',
                local_stabilizer='C2, acting as minus identity on four real normal directions',
                gauge_scope='Each connected component has local A1 transverse type; '
                    'no connected-component count or full gauge spectrum inferred.')


def real_locus_checks():
    x = s.symbols('x0:5', real=True)
    f = sum(x[i]**2*x[(i+1) % 5] for i in range(5))
    grad = [s.diff(f, z) for z in x]
    assert s.expand(sum(z*d for z, d in zip(x, grad))-3*f) == 0
    e0 = {x[i]: int(i == 0) for i in range(5)}
    assert f.subs(e0) == 0 and sum(d.subs(e0)**2 for d in grad) == 1
    return dict(nonempty_point=[1, 0, 0, 0, 0], real_link_dimension=3,
                smoothness_proof='The complex cone has no nonzero critical point. '
                    'On f=0 intersectS4, a vanishing tangential gradient would give '
                    'grad f=c*x; Euler givesc=0, contradicting cone smoothness.',
                no_fixed_locus_intersections='Two distinct reflections multiply to a '
                    'nonidentity D power, free on Y. Thus their fixed loci are disjoint.',
                associative_reason='K sends eta and transverse omega to their negatives '
                    'and the complex3-form to its conjugate. The fixed real3-locus '
                    'is special Legendrian, hence associative for the invariant weakG2 form.',
                not_computed='Topology/connected components of R, calibrated volumes, '
                    'charged localized spectra, resolutions and their backreaction.')


def spin_and_cayley():
    X = s.Matrix([[0, 1], [1, 0]])
    Y = s.Matrix([[0, -s.I], [s.I, 0]])
    Z = s.diag(1, -1)
    I = s.eye(2)
    def tensor(factors):
        result = s.ones(1, 1)
        for f in factors:
            result = s.kronecker_product(result, f)
        return result
    gammas = [tensor([Z]*j+[p]+[I]*(3-j)) for j in range(4) for p in (X, Y)]
    lift = s.eye(16)
    for j in (1, 3, 5, 7):
        lift = lift*gammas[j]
    assert lift**2 == s.eye(16)
    for j, gamma in enumerate(gammas):
        assert lift*gamma*lift.inv() == (-1 if j % 2 else 1)*gamma
    # SU4-invariant positive-chirality spinors: vacuum and volume state.
    singlets = lift.extract([0, 15], [0, 15])
    assert singlets**2 == s.eye(2) and singlets.trace() == 0
    assert singlets.eigenvals() == {-1: 1, 1: 1}
    # Formal forms in an orthonormal local complex4 frame. K reverses all
    # four imaginary directions, preserving J^2 and ReOmega but reversing J.
    def wedge(a, b):
        out = {}
        for u, c in a.items():
            for v, d in b.items():
                if set(u).intersection(v):
                    continue
                sign = (-1)**sum(i > j for i in u for j in v)
                key = tuple(sorted(u+v))
                out[key] = s.expand(out.get(key, 0)+sign*c*d)
        return {k: v for k, v in out.items() if v != 0}
    def pullback(form):
        return {u: (-1)**sum(j % 2 for j in u)*c for u, c in form.items()}
    J = {(2*j, 2*j+1): 1 for j in range(4)}
    Omega = {(): 1}
    for j in range(4):
        Omega = wedge(Omega, {(2*j,): 1, (2*j+1,): s.I})
    real = {u: s.re(c) for u, c in Omega.items() if s.re(c) != 0}
    imaginary = {u: s.im(c) for u, c in Omega.items() if s.im(c) != 0}
    J2 = {u: c/2 for u, c in wedge(J, J).items()}
    Phi = {u: J2.get(u, 0)+real.get(u, 0) for u in J2.keys() | real.keys()}
    assert pullback(J) == {u: -c for u, c in J.items()}
    assert pullback(real) == real and pullback(Phi) == Phi
    assert pullback(imaginary) == {u: -c for u, c in imaginary.items()}
    assert len(Phi) == 14
    return dict(real_orientation_preserved=True, normal_real_codimension=4,
                spin_lift_square=1, SU4_singlet_spin_action=[[int(v) for v in singlets.row(i)] for i in range(2)],
                SU4_pair_invariant_spinors=1,
                Cayley_invariant=True, Cayley_term_count=len(Phi),
                transformation='K:J->-J, Omega4->barOmega4; Phi=J^2/2+ReOmega4 invariant.',
                supersymmetry_scope='Projects the known SU4-invariant spinor pair to one. '
                    'Published Spin7 quotient construction supplies the standardN1 AdS route; '
                    'no full interacting localized spectrum or accidental spinors computed.')


def Wilson_cost():
    W = [2, 2, 2, -3, -3]
    assert sorted(a % 11 for a in W) != sorted(-a % 11 for a in W)
    parity = [0, 0, 0, 1, 1]
    assert sum(parity) % 2 == 0
    ordinary_Z5_split = [(a, b) for a, b in product(range(5), repeat=2)
                         if (3*a+2*b) % 5 == 0 and a != b]
    assert ordinary_Z5_split == []
    return dict(C11_SM_Wilson_line_extends_to_dihedral22_inside_SU5=False,
                reason='K D K=D^-1 would require W and W^-1 to be conjugate. '
                    'Their eigenvalue multisets differ, so the previous3+2 Wilson line does not extend.',
                underlying_dihedral_quotient_has_no_nontrivial_flat_holonomy=True,
                larger_110_underlying_pi1='C5, which still cannot split standardSU5 by an ordinary Wilson line',
                possible_orbifold_gauge_parity=parity,
                parity_scope='diag(1,1,1,-1,-1) is a valid conditionalSU5 isotropy '
                    'projection. It is not a flat Wilson line on the underlying space '
                    'and does not supply anSU5 gauge sector.',
                C_field_scope='Neither363 nor15 smooth flat-C counts is inherited '
                    'without a new orbifold/differential calculation. Isotropy and2-primary data matter.')


def holomorphic_A1_gauge_control():
    cert = json.loads((ROOT/'data/toe_20261118_klein_odd_Weil_fixed_strata.json').read_text())
    assert cert['status'] == 'PASS' and cert['group_order'] == 660
    # Independent export round-trip and finite-field closure control.
    weights = cert['D_weights']
    numerators = cert['generator_S_cyclotomic_numerators']
    zeta = np.exp(2j*np.pi/11)
    matrix = np.array([[sum(c*zeta**k for k, c in enumerate(entry))/11
                        for entry in row] for row in numerators])
    assert np.max(abs(matrix@matrix-np.eye(5))) < 1e-12
    assert np.max(abs(matrix.imag)) < 1e-12
    prime, root = 23, 2
    assert pow(root, 11, prime) == 1 and root != 1
    Smod = np.array([[sum(c*pow(root, k, prime) for k, c in enumerate(entry))*pow(11, -1, prime) % prime
                     for entry in row] for row in numerators], dtype=np.int64)
    Dmod = np.diag([pow(root, w, prime) for w in weights]).astype(np.int64)
    identity = np.eye(5, dtype=np.int64)
    key = lambda m: tuple(int(a) for a in m.flat)
    seen, queue = {key(identity)}, [identity]
    for current in queue:
        for gen in (Smod, Dmod):
            following = gen@current % prime
            if key(following) not in seen:
                seen.add(key(following))
                queue.append(following)
    assert len(seen) == 660
    assert sum(row['class_size'] for row in cert['class_census']) == 660
    for row in cert['class_census']:
        if row['order'] > 2:
            assert row['ambient_fixed_complex_dimension'] <= 1
    involutions = [row for row in cert['class_census'] if row['order'] == 2]
    assert len(involutions) == 1 and involutions[0]['class_size'] == 55
    assert cert['involution_centralizer_order'] == 12
    degree, index = 3, 2
    base_curve_area = s.pi*s.Rational(index, 4)*degree
    fiber_period = s.pi
    Q_volume = s.simplify(fiber_period*base_curve_area)
    assert Q_volume == 3*s.pi**2/2
    residual_order = cert['involution_centralizer_order']//2
    quotient_volume = Q_volume/residual_order
    assert quotient_volume == s.pi**2/4
    return dict(projective_involution_fixed_locus='smooth plane cubic E plus a projective line',
                exported_generator_mod23_closure=660,
                exported_generator_square_error=float(np.max(abs(matrix@matrix-np.eye(5)))),
                link_fixed_locus='Q, the circle bundle over E with Euler degree3',
                Q_H1='Z^2 plus Z3', Q_H2='Z^2', Q_H3='Z',
                Q_genus_base=1, Q_volume_Ric6=str(Q_volume),
                full_PSL_quotient_generic_A1_stratum_volume=str(quotient_volume),
                volume_reason='Base Kahler class(pi/2)H gives area(E)=3pi/2; '
                    'Reeb periodpi gives volume3pi^2/2. Full quotient divides by '
                    'the effective involution centralizer of order6.',
                higher_ADE_codimension4_excluded_for_holomorphic_PSL=True,
                exclusion_proof='Every noninvolution has ambient fixed dimension<=1, '
                    'hence no fixed link vector by invariant-cubic smoothness and Euler. '
                    'A higher finiteSU2 subgroup has an element of order>2. Thus only '
                    'genericA1 codimension4 singularities occur in this holomorphic quotient.',
                V4_intersections='Three circle directions perV4 fixed binary cubic; '
                    'local cone C x (C^3/V4), codimension6 on the link, not anA2 codimension4 locus.',
                tree_gauge_kinetic_coefficient='g4^-2=R^3 Vol(Q_unit)/g7^2, '
                    'with Vol(Q_unit)=3pi^2/2 for the singleC2 quotient, pi^2/4 '
                    'for the fullPSL generic-stratum orbifold volume.',
                physics_scope='Standard localADE gauge-action reduction, conditional '
                    'on the unfrozen local theory. The normalized7D gauge coupling, '
                    'thresholds, flux interactions and singular-intersection matter '
                    'are not calculated. These formulas are not observed coupling predictions.')


if __name__ == '__main__':
    out = dict(status='PASS', real_locus=real_locus_checks(), spin=spin_and_cayley(),
               dihedral22=group_and_isotropy(False), extended110=group_and_isotropy(True),
               Wilson_tradeoff=Wilson_cost(),
               holomorphic_gauge_control=holomorphic_A1_gauge_control(),
               geometric_input='Published KE existence and uniqueness make complex '
                    'conjugation an isometry of the real cubic SE construction.',
               physics='Standard unfrozen A1 local model supports an su2 gauge algebra '
                    'along each singular real3-component. Full orbifold quantum consistency, '
                    'gauge multiplicities, colorSU3 and chiralSM are not supplied.')
    target = ROOT/'data/toe_20261118_klein_real_Spin7_A1_projection.json'
    target.write_text(json.dumps(out, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=out['status'], invariant_pair_spinors=1,
                         isotropy='A1 codimension4', underlying_pi1=['trivial', 'C5'])))
