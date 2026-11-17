"""Dynamics on the norm-seven triangular torus: dispersion and overlap index.

Prior geometry: toe_20261117_csaszar_szilassi_hexagonal_modes.py.
Prior square overlap control: toe_20261105_overlap_flux_chirality_index.py.
This is an explicitly chosen regulator and flux, not a derivation of families.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import minimize

from toe_20261117_csaszar_szilassi_hexagonal_modes import PERIODS, Q, WAVES

STEPS = ((1, 0), (0, 1), (1, -1))
VECTORS = ((1., 0.), (.5, np.sqrt(3)/2), (.5, -np.sqrt(3)/2))
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.diag([1., -1.])


def dispersion():
    x, y = sp.symbols('kx ky', real=True)
    vectors = ((1, 0), (sp.Rational(1, 2), sp.sqrt(3)/2),
               (sp.Rational(1, 2), -sp.sqrt(3)/2))
    sums = {p: sp.expand(sum((a*x+b*y)**p for a, b in vectors)) for p in (2, 4, 6)}
    assert sp.expand(sp.Rational(2, 3)*sums[2]-x*x-y*y) == 0
    error2 = sp.factor(-sums[4]/18)
    error4 = sp.factor(-sums[6]/135)
    assert error2 == -(x*x+y*y)**2/16
    inverse = np.array(PERIODS.inv().T, float)
    continuum = float(4*sp.pi**2*(sp.Matrix([1, 0]).T*PERIODS.inv()*Q.inv()
                                *PERIODS.inv().T*sp.Matrix([1, 0]))[0])
    assert sp.simplify(4*sp.pi**2*(sp.Matrix([1, 0]).T*PERIODS.inv()*Q.inv()
                                 *PERIODS.inv().T*sp.Matrix([1, 0]))[0]
                       -16*sp.pi**2/21) == 0
    rows = []
    for n in (1, 2, 3, 4, 8, 16, 32):
        values, improved = [], []
        for wave in WAVES:
            theta = 2*np.pi*(inverse@np.array(wave))/n
            phase = np.array([np.dot(theta, step) for step in STEPS])
            base = 4*np.sin(phase/2)**2
            values.append(2*n*n/3*np.sum(base))
            improved.append(2*n*n/3*np.sum(base*(1+np.sin(phase/2)**2/3)))
        assert np.ptp(values) < 1e-11 and np.ptp(improved) < 1e-11
        rows.append(dict(N=n, sites=7*n*n, nearest=values[0], improved=improved[0],
                         nearest_relative_error=values[0]/continuum-1,
                         improved_relative_error=improved[0]/continuum-1))
    assert abs(rows[0]['nearest']-14/3) < 1e-12
    assert abs(rows[-1]['nearest_relative_error']/rows[-2]['nearest_relative_error']-.25) < .001
    assert abs(rows[-1]['improved_relative_error']/rows[-2]['improved_relative_error']-.0625) < .001
    return dict(continuum_first_shell=continuum, continuum_exact='16*pi**2/21',
                nearest_h_squared_error=str(error2), improved_h_fourth_error=str(error4),
                positivity='4 sin(t/2)^2 * (1+sin(t/2)^2/3) in each direction', records=rows)


def transport(n, flux=0, holonomy=(0., 0.)):
    """Straight links in Landau gauge on periods (7n,0), (4n,n).

    The latter columns are the column Hermite normal form of n*PERIODS.
    holonomy gives boundary phases around these two period columns.
    """
    assert n >= 1 and isinstance(flux, int)
    size = 7*n*n
    field = 2*np.pi*flux/size
    operators = []
    for dx, dy in STEPS:
        matrix = np.zeros((size, size), complex)
        for a in range(7*n):
            for b in range(n):
                target_x, target_y = a+dx, b+dy
                winding_y, reduced_y = divmod(target_y, n)
                winding_x, reduced_x = divmod(target_x-4*n*winding_y, 7*n)
                # Boundary transition implements A(x+P)=A(x)+d chi_P.
                transition = field*(winding_y*n*reduced_x
                                    +2*n*n*winding_y*(winding_y-1))
                phase = -field*dx*(b+dy/2)+transition
                phase += winding_x*holonomy[0]+winding_y*holonomy[1]
                matrix[a*n+b, reduced_x*n+reduced_y] = np.exp(1j*phase)
        assert np.max(abs(matrix@matrix.conj().T-np.eye(size))) < 1e-12
        operators.append(matrix)
    tx, ty, td = operators
    # Both counterclockwise elementary triangles have equal principal flux.
    plaquettes = (tx@td.conj().T@ty.conj().T, td@ty@tx.conj().T)
    expected = np.exp(1j*field/2)*np.eye(size)
    assert max(np.max(abs(p-expected)) for p in plaquettes) < 2e-12
    winding = sum(np.angle(np.diag(p)).sum() for p in plaquettes)/(2*np.pi)
    if abs(field/2) < np.pi:
        assert abs(winding-flux) < 1e-10
    return operators, float(winding)


def overlap(n, flux, mass=1., holonomy=(0., 0.), verify_vectors=False,
            noise=0., gauge_seed=None):
    transports, winding = transport(n, flux, holonomy)
    size = 7*n*n
    if noise:
        random = np.random.default_rng(20261117)
        transports = [np.exp(1j*random.uniform(-noise, noise, size))[:, None]*t
                      for t in transports]
    if gauge_seed is not None:
        gauge = np.exp(1j*np.random.default_rng(gauge_seed).uniform(-np.pi, np.pi, size))
        transports = [gauge[:, None]*t*gauge.conj()[None, :] for t in transports]
    tx, ty, td = transports
    phases = np.concatenate([np.angle(np.diag(p)) for p in
                             (tx@td.conj().T@ty.conj().T, td@ty@tx.conj().T)])
    winding = float(phases.sum()/(2*np.pi))
    assert abs(winding-flux) < 1e-10
    identity = np.eye(size)
    wilson = -mass*np.eye(2*size, dtype=complex)
    for t, (x, y) in zip(transports, VECTORS):
        wilson += np.kron((t-t.conj().T)/3, x*SX+y*SY)
        wilson += np.kron((2*identity-t-t.conj().T)/3, np.eye(2))
    gamma = np.kron(identity, SZ)
    hermitian = gamma@wilson
    assert np.max(abs(hermitian-hermitian.conj().T)) < 1e-12
    ev, vectors = np.linalg.eigh(hermitian)
    gap = float(min(abs(ev)))
    assert gap > 1e-7, (n, flux, mass, gap)
    index = int(round(-np.sign(ev).sum()/2))
    record = dict(N=n, sites=size, flux=flux, measured_triangle_flux=winding,
                  holonomy=list(holonomy), mass=mass, index=index, Wilson_gap=gap,
                  background_uniform_triangle_phase=np.pi*flux/size,
                  maximum_actual_triangle_phase=float(max(abs(phases))),
                  gauge_action_unit_coupling=float(np.sum(1-np.cos(phases))),
                  link_noise_bound=noise, site_gauge_seed=gauge_seed)
    if verify_vectors:
        sign = (vectors*np.sign(ev))@vectors.conj().T
        operator = np.eye(2*size)+gamma@sign
        gw = float(np.max(abs(gamma@operator+operator@gamma-operator@gamma@operator)))
        assert gw < 2e-12
        singular_vectors = np.linalg.eigh(operator.conj().T@operator)
        zero = singular_vectors[1][:, singular_vectors[0] < 1e-12]
        chiralities = np.linalg.eigvalsh(zero.conj().T@gamma@zero)
        assert abs(chiralities.sum()-index) < 1e-8
        record.update(GW_error=gw, zero_modes=zero.shape[1],
                      zero_mode_chiralities=chiralities.tolist())
    return record


def free_doublers():
    """Analytic momentum zeros: Gamma, three M points and two K points."""
    p, q = sp.symbols('p q', real=True)
    derivative = sp.Matrix([sp.sin(p)+(sp.sin(q)+sp.sin(p-q))/2,
                            sp.sqrt(3)*(sp.sin(q)-sp.sin(p-q))/2])*sp.Rational(2, 3)
    jacobian = derivative.jacobian([p, q])
    result = []
    for name, u, v in (('Gamma', 0, 0), ('M1', sp.pi, 0), ('M2', 0, sp.pi),
                       ('M3', sp.pi, sp.pi), ('K1', 2*sp.pi/3, -2*sp.pi/3),
                       ('K2', -2*sp.pi/3, 2*sp.pi/3)):
        at = {p:u, q:v}
        assert derivative.subs(at) == sp.zeros(2, 1)
        w = sp.simplify(sp.Rational(2, 3)*(3-sp.cos(u)-sp.cos(v)-sp.cos(u-v)))
        charge = int(sp.sign(jacobian.det().subs(at)))
        result.append(dict(point=name, momentum=[str(u), str(v)], Wilson_value=str(w),
                           orientation=charge))
    assert sum(r['orientation'] for r in result) == 0
    return result


def scalar_matrix_checks():
    """Check the Fourier dispersion against actual quotient hopping matrices."""
    inverse = np.array(PERIODS.inv().T, float)
    rows = []
    for n in (1, 2, 3):
        transports, _ = transport(n)
        identity = np.eye(7*n*n)
        laplacian = 2*n*n/3*sum(2*identity-t-t.conj().T for t in transports)
        maximum = 0.
        for wave in WAVES:
            theta = 2*np.pi*(inverse@np.array(wave))/n
            vector = np.array([np.exp(1j*np.dot(theta, (a, b)))
                               for a in range(7*n) for b in range(n)])
            expected = 2*n*n/3*sum(4*np.sin(np.dot(theta, step)/2)**2 for step in STEPS)
            maximum = max(maximum, float(np.max(abs(laplacian@vector-expected*vector))))
        assert maximum < 1e-11
        rows.append(dict(N=n, maximum_plane_wave_residual=maximum))
    return rows


def magnetic_scalar_levels():
    """Continuum Landau-level control on the same triangular gauge field."""
    rows = []
    for flux in (1, 3):
        target = 4*np.pi*flux/(7*np.sqrt(3))
        for n in (2, 3, 4, 8):
            transports, _ = transport(n, flux)
            identity = np.eye(7*n*n)
            operator = 2*n*n/3*sum(2*identity-t-t.conj().T for t in transports)
            eigenvalues = np.linalg.eigvalsh(operator)
            # Each continuum level has flux-fold degeneracy. Finite-spacing
            # band splittings are retained, rather than assumed to vanish.
            first = eigenvalues[:flux]
            second = eigenvalues[flux:2*flux]
            rows.append(dict(N=n, flux=flux, continuum_ground=target,
                             lowest_band=first.tolist(), next_band=second.tolist(),
                             lowest_band_relative_error=float(np.mean(first)/target-1),
                             next_band_relative_error=float(np.mean(second)/(3*target)-1)))
        assert abs(rows[-1]['lowest_band_relative_error']) < abs(rows[-2]['lowest_band_relative_error'])/3
    return rows


def lowest_band_quartic():
    """Local multistart minimization, not a certificate of global optimality."""
    triangular = sum(np.exp(-2*np.pi/np.sqrt(3)*(a*a+a*b+b*b))
                     for a in range(-8, 9) for b in range(-8, 9))
    rows = []
    random = np.random.default_rng(20261117)
    for flux in (1, 3):
        for n in (3, 4, 6, 8):
            transports, _ = transport(n, flux)
            size = 7*n*n
            identity = np.eye(size)
            operator = 2*n*n/3*sum(2*identity-t-t.conj().T for t in transports)
            eigenvalues, eigenvectors = np.linalg.eigh(operator)
            basis = eigenvectors[:, :flux]

            def objective(real):
                state = basis@(real[:flux]+1j*real[flux:])
                density = abs(state)**2
                return float(size*np.sum(density**2))

            def jacobian(real):
                state = basis@(real[:flux]+1j*real[flux:])
                grad = 4*size*(basis.conj().T@((abs(state)**2)*state))
                return np.concatenate((grad.real, grad.imag))

            constraint = dict(type='eq', fun=lambda real: np.dot(real, real)-1,
                              jac=lambda real: 2*real)
            minima = []
            for _ in range(1 if flux == 1 else 16):
                start = random.normal(size=2*flux)
                start /= np.linalg.norm(start)
                result = minimize(objective, start, jac=jacobian, constraints=constraint,
                                  method='SLSQP', options=dict(ftol=1e-12, maxiter=500))
                assert result.success, result.message
                assert abs(np.linalg.norm(result.x)-1) < 1e-10
                minima.append(float(result.fun))
            rows.append(dict(N=n, flux=flux, candidate_beta=min(minima),
                             all_local_values=minima, continuum_triangular_beta=float(triangular),
                             lowest_band_width=float(eigenvalues[flux-1]-eigenvalues[0])))
    assert abs(rows[-1]['candidate_beta']-triangular) < .002
    return dict(records=rows, scope='Projected lowest-band local multistart search; '
                'finite band splitting neglected in quartic minimization; fixed external magnetic flux.')


def landau_selection_rule():
    """Exact oscillator expansion; cutoff is above all occupied test levels."""
    size = 9
    lowering = sp.zeros(size)
    for j in range(1, size):
        lowering[j-1, j] = sp.sqrt(j)
    raising = lowering.T
    px = (lowering+raising)/sp.sqrt(2)
    py = (lowering-raising)/(sp.I*sp.sqrt(2))
    vacuum = sp.eye(size)[:, 0]
    directions = ((1, 0), (sp.Rational(1, 2), sp.sqrt(3)/2),
                  (sp.Rational(1, 2), -sp.sqrt(3)/2))
    fourth = sum(((x*px+y*py)**4*vacuum for x, y in directions), sp.zeros(size, 1)).applyfunc(sp.simplify)
    sixth = sum(((x*px+y*py)**6*vacuum for x, y in directions), sp.zeros(size, 1)).applyfunc(sp.simplify)
    assert fourth == sp.Rational(9, 4)*vacuum
    assert sixth == sp.Rational(45, 8)*vacuum+9*sp.sqrt(5)/2*sp.eye(size)[:, 6]
    return dict(fourth_power_action_on_LLL='(9/4) B^2 |0>',
                sixth_power_action_on_LLL='B^3 [(45/8)|0>+(9 sqrt(5)/2)|6>]',
                ground_energy_expansion='B-h^2 B^2/8+h^4 B^3/96+O(h^6)',
                first_wavefunction_mixing='-h^4 B^2 sqrt(5)/1440 |6>+O(h^6)',
                scope='Formal smooth-field expansion at fixed B>0 for the nearest triangular stencil; '
                      'the h^2 correction shifts energy without mixing higher Landau levels.')


def flux_selection_boundary():
    field, coupling2, density, v2, lam, kinetic_plus = sp.symbols(
        'B g2 rho v2 lambda Kplus', real=True)
    # Integrated identity for positive flux, D=partial-iA:
    # integral |D phi|^2 = integral |(D1+i D2)phi|^2+B|phi|^2.
    energy = kinetic_plus+field*density+field**2/(2*coupling2)+lam*(density-v2)**2
    completed = (kinetic_plus+(field-coupling2*(v2-density))**2/(2*coupling2)
                 +(lam-coupling2/2)*(density-v2)**2+field*v2)
    assert sp.simplify(energy-completed) == 0
    return dict(BPS_tuning='lambda=g^2/2; mu^2=g^2 v^2',
                BPS_area_bound='Area >= 2*pi*abs(Q)/(g^2 v^2)',
                flux_energy_bound='E_relative >= 2*pi*abs(Q)*v^2 for lambda>=g^2/2',
                global_classical_minimum='For any lambda>0 and g^2>0, Q=0 with '
                    'B=0, D phi=0, |phi|^2=v^2 attains zero relative energy. '
                    'Nonzero-flux sectors cannot attain zero. No external field or flux constraint included.',
                scope='Standard Abelian-Higgs square completion and Bradlow boundary; '
                      'not a theorem for the full E6 or gravity system.')


def certificate():
    records = [overlap(n, flux, mass, verify_vectors=(n == 3 and mass == 1.))
               for n in (1, 2, 3, 4) for flux in (-3, -1, 0, 1, 3)
               for mass in (.5, 1., 2.)]
    flat = [overlap(3, 0, holonomy=angles, verify_vectors=True)
            for angles in ((0., 0.), (.37, .81), (np.pi, 0.), (np.pi, np.pi))]
    assert all(row['index'] == -row['flux'] for row in records if row['N'] >= 2)
    assert all(row['index'] == 0 for row in flat)
    assert [row['zero_modes'] for row in flat] == [2, 0, 0, 0]
    assert next(row['index'] for row in records if row['N'] == 1
                and row['flux'] == 3 and row['mass'] == 1.) == 0
    robust = [overlap(2, 3, noise=eta, gauge_seed=seed, verify_vectors=True)
              for eta, seed in ((0., 42), (.02, None), (.02, 42))]
    reference = next(row for row in records if row['N'] == 2 and row['flux'] == 3
                     and row['mass'] == 1.)
    norm_bound = float(8*np.sin(.02/2))
    assert reference['Wilson_gap'] > norm_bound
    assert all(row['index'] == -3 for row in robust)
    assert abs(robust[0]['Wilson_gap']-reference['Wilson_gap']) < 1e-12
    assert abs(robust[1]['Wilson_gap']-robust[2]['Wilson_gap']) < 1e-12
    branch = [overlap(4, 1, mass) for mass in (1., 2.8, 3.5)]
    assert [row['index'] for row in branch] == [-1, 2, 0]
    coarse = [overlap(1, 3, mass, verify_vectors=True) for mass in (1., 2.)]
    assert [row['zero_modes'] for row in coarse] == [0, 2]
    return dict(status='PASS', dispersion=dispersion(), free_doublers=free_doublers(),
                scalar_matrix_checks=scalar_matrix_checks(),
                magnetic_scalar_levels=magnetic_scalar_levels(), coarse_failure_records=coarse,
                lowest_band_quartic=lowest_band_quartic(),
                landau_selection_rule=landau_selection_rule(),
                flux_selection_boundary=flux_selection_boundary(),
                overlap_records=records, flat_holonomy_records=flat,
                robustness_records=robust, mass_branch_records=branch,
                kernel_noise_norm_bound=norm_bound,
                limitations='Flux and regulator are supplied. This is a 2D internal Euclidean spinor operator, '
                            'not a derivation of SM representations, generations, anomalies or gravity.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]
                        /'data/toe_20261117_hexagonal_regulator.json')
    args = parser.parse_args()
    result = certificate()
    args.output.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=result['status'], overlap_scans=len(result['overlap_records']),
                          flat_scans=len(result['flat_holonomy_records']), output=str(args.output))))
