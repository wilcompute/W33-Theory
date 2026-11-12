"""Heavy monopole channel count and exact radial boundary spectral-flow controls."""

import json

import sympy as sp

import toe_20261110_global_gauge_topology as topology
import toe_20261113_sm_threshold_theta as thresholds


OUT = 'data/toe_20261113_monopole_heavy_phase_flow.json'


def channel_weights():
    previous = topology.flat.read(thresholds.OUT)
    monopole = sp.Matrix(previous['monopole_primitive'])
    electric = sp.Matrix([-sp.Rational(1, 3)]*3+[1, 0])
    basis = [sp.eye(5)[:, i] for i in range(5)]
    adjoint = [basis[0]-basis[1], basis[0]-basis[2], basis[4]-basis[3]]
    triplet = [basis[0]]*3
    for weights, expected in zip((adjoint, triplet), previous['monopole_electric_shift_representatives']):
        assert all(weight.dot(monopole) == 1 for weight in weights)
        assert sum(weights, sp.zeros(5, 1)) == sp.Matrix(expected)
        assert sum(weight.dot(electric) for weight in weights) == -1
    return [
        dict(phase=name, unit_flux_weights=[list(map(int, weight)) for weight in weights],
             individual_electric_Q=list(map(str, [weight.dot(electric) for weight in weights])),
             massive_fixed_boundary_downward_crossings=3,
             product_of_crossing_endpoint_characters=-1)
        for name, weights in (('adjoint', adjoint), ('triplet', triplet))
    ]


def massive_boundary():
    mass = sp.symbols('M', positive=True)
    c, s = sp.symbols('c s', real=True)
    # After the constant boundary phase is absorbed, the boundary spinor
    # is (1,1). The decay exponent is M sin(phi-beta).
    hamiltonian = sp.Matrix([[sp.I*mass*s, mass*(c-sp.I*s)],
                             [mass*(c+sp.I*s), -sp.I*mass*s]])
    boundary_spinor = sp.ones(2, 1)
    assert (hamiltonian*boundary_spinor).applyfunc(sp.expand) == mass*c*boundary_spinor
    derivative_at_crossing = sp.Matrix([[0, -mass], [-mass, 0]])
    assert (boundary_spinor.T*derivative_at_crossing*boundary_spinor)[0]/2 == -mass
    weights = [sp.Rational(9, 25), sp.Rational(16, 25)]
    slope = -sum(weights)/(weights[0]/2+weights[1]/3)
    assert slope == -sp.Rational(150, 59)
    return dict(decay='M*sin(phi-beta)>0', eigenvalue='M*cos(phi-beta)',
                zero_crossing='phi=beta+pi/2 mod 2*pi', crossing_direction='downward',
                unequal_mass_example_crossing_slope=str(slope))


def mixed_boundary():
    z = sp.symbols('z')
    a, b = sp.Rational(3, 5), sp.Rational(4, 5)
    u = sp.Matrix([[a, b], [-b, a]])
    assert u.T*u == sp.eye(2) and u.det() == 1
    outgoing_to_incoming = sp.factor(u[1, 1]+u[1, 0]*u[0, 1]/(z-u[0, 0]))
    assert sp.cancel(outgoing_to_incoming-(1-a*z)/(a-z)) == 0
    assert sp.cancel(outgoing_to_incoming*outgoing_to_incoming.subs(z, 1/z)) == 1
    # z is the unit-modulus decaying-heavy boundary value. The pole
    # lies in the disk and the zero outside, so reflection winds +1.
    numerator, denominator = sp.fraction(outgoing_to_incoming)
    pole, = sp.solve(denominator, z)
    zero, = sp.solve(numerator, z)
    assert abs(pole) < 1 < abs(zero)
    winding_u = sp.diag(z, 1)*u
    assert winding_u.det() == z
    compensated = sp.cancel(winding_u[1, 1]+winding_u[1, 0]*winding_u[0, 1]
                            /(z-winding_u[0, 0]))
    assert compensated == -1
    # Explicit determinant check of the Schur complement with two
    # heavy channels and one light channel, with nontrivial mixing.
    full = sp.diag(u, 1)*sp.Matrix([[a, 0, b], [0, 1, 0], [-b, 0, a]])
    assert full.T*full == sp.eye(3)
    heavy = full[:2, :2]
    expected = full.det()*(sp.eye(2)-z*heavy.T).det()
    assert sp.expand((full-sp.diag(z, z, 0)).det()-expected) == 0
    # A finite-radius flux-preserving transfer cannot change the winding
    # of the full boundary graph. Check its elementary Möbius action.
    flux = sp.diag(1, -1)
    transfer = sp.Matrix([[sp.Rational(5, 3), sp.Rational(4, 3)],
                          [sp.Rational(4, 3), sp.Rational(5, 3)]])
    assert transfer.T*flux*transfer == flux
    transported = sp.factor((transfer[1, 0]+transfer[1, 1]*z)
                            /(transfer[0, 0]+transfer[0, 1]*z))
    top, bottom = sp.fraction(transported)
    assert abs(sp.solve(top, z)[0]) < 1 < abs(sp.solve(bottom, z)[0])
    return dict(mixing_boundary=[[str(x) for x in row] for row in u.tolist()],
                outgoing_to_incoming_amplitude=str(outgoing_to_incoming),
                pole=str(pole), zero=str(zero), fixed_boundary_bound_crossings=0,
                incoming_to_outgoing_reflection_winding=1,
                winding_boundary_control=dict(boundary_determinant='z', reflection=str(compensated)),
                flux_preserving_boundary_transport=str(transported),
                three_channel_controls=[
                    dict(decoupled_heavy=3-k, mixed_heavy=k, downward_bound_crossings=3-k,
                         reflection_winding=k)
                    for k in range(4)
                ])


def calculate():
    return dict(status='PASS', monopole_channel_count=channel_weights(),
                massive_boundary=massive_boundary(), mixed_boundary=mixed_boundary(),
                asymptotic_mass_determinant_winding=3,
                smooth_core_boundary_winding='undetermined')


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (topology.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
