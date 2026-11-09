#!/usr/bin/env python3
"""Five independent, fail-closed W33 research checks, 2026-11-09.

Only elementary finite fields, exact fractions and numpy are required.  This is
not a continuum quantum field theory, a cosmological likelihood or a hardware
experiment. Run: python analysis/w33_20261109_five_fronts.py [json-output].
"""
import itertools
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np


def s5_singlet():
    # Nine copies of the 5-dimensional standard representation of S6,
    # conditional on the independently established W33 sentinel-to-S6 map.
    T = np.stack([np.eye(6)[:, i] - np.eye(6)[:, 5] for i in range(5)], axis=1)
    B, _ = np.linalg.qr(T)
    def perm(a, b):
        Q = np.eye(6)
        Q[[a, b], :] = Q[[b, a], :]
        return B.T @ Q @ B
    stars = [perm(k, 5) for k in range(5)]
    R = sum(stars)
    # high-M 9-dim eigenspace is the S5 invariant component, not a generic
    # chiral multiplet; each standard S6 rep restricts to 1 + standard S5.
    high = (4 * np.eye(5) - R) / 5
    low = (R + np.eye(5)) / 5
    assert np.max(np.abs(high @ high - high)) < 1e-12
    assert np.max(np.abs(low @ low - low)) < 1e-12
    assert abs(np.trace(high) - 1) < 1e-12
    assert abs(np.trace(low) - 4) < 1e-12
    for a, b in itertools.combinations(range(5), 2):
        assert np.max(np.abs(perm(a, b) @ high - high)) < 1e-12
    return dict(star_eigenvalues=sorted(np.linalg.eigvalsh(R).round(10).tolist()),
                high_M_eigenvalue='16/9', high_M_S5_singlets=9,
                low_M_eigenvalue='1/9', low_M_standard_S5_copies=9,
                projection_formula='P_high=(4*I-R)/5, P_low=(R+I)/5',
                scope='abstract S6 calculation; W33 identification is the prior sentinel theorem')


def normalize(v):
    x = next(z for z in v if z)
    return tuple(z * pow(x, -1, 3) % 3 for z in v)


def symplectic(u, v):
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3


def geometry():
    pts = sorted({normalize(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    idx = {v: i for i, v in enumerate(pts)}
    lines = set()
    for u, v in itertools.combinations(pts, 2):
        if symplectic(u, v):
            continue
        line = frozenset(idx[normalize(tuple((a * u[k] + b * v[k]) % 3 for k in range(4)))]
                         for a, b in itertools.product(range(3), repeat=2) if a or b)
        if len(line) == 4:
            lines.add(line)
    lines = sorted(lines, key=lambda v: tuple(sorted(v)))
    assert len(pts) == len(lines) == 40
    incidents = [set(j for j, line in enumerate(lines) if p in line) for p in range(40)]
    assert all(len(v) == 4 for v in incidents)
    return pts, lines, incidents


def gauge_geometry_and_action():
    pts, lines, incidents = geometry()
    collinear = [set().union(*(lines[j] for j in incidents[p])) - {p} for p in range(40)]
    edges = [(p, 40 + l) for l, line in enumerate(lines) for p in sorted(line)]
    edgeidx = {edge: k for k, edge in enumerate(edges)}
    loops = {}
    for p in range(40):
        for l1, l4 in itertools.combinations(sorted(incidents[p]), 2):
            for q in lines[l1] - {p}:
                for t in lines[l4] - {p}:
                    mids = collinear[q] & collinear[t] - {p}
                    assert len(mids) == 3
                    for s in mids:
                        l2 = next(j for j in incidents[q] if s in lines[j])
                        l3 = next(j for j in incidents[t] if s in lines[j])
                        body = (p, 40 + l1, q, 40 + l2, s, 40 + l3, t, 40 + l4)
                        orderings = [body, body[::-1]]
                        key = min(tuple(v[k:] + v[:k]) for v in orderings for k in range(8))
                        loops[key] = key + (key[0],)
    assert len(loops) == 1620
    # No 4- or 6-cycles: a GQ has no triangles of collinear points and no
    # pair of points shares more than one line.
    assert all(len(lines[a] & lines[b]) <= 1 for a, b in itertools.combinations(range(40), 2))
    for p, q, t in itertools.combinations(range(40), 3):
        if q in collinear[p] and t in collinear[p] and t in collinear[q]:
            assert any({p, q, t} <= set(line) for line in lines)
    masks = []
    for path in loops.values():
        signs = []
        mask = 0
        for a, b in zip(path, path[1:]):
            k = edgeidx[(min(a, b), max(a, b))]
            signs.append((k, 1 if a < b else -1))
            mask ^= 1 << k
        masks.append((mask, signs))
    basis = {}
    for mask, _ in masks:
        while mask:
            leading = mask.bit_length() - 1
            if leading in basis:
                mask ^= basis[leading]
            else:
                basis[leading] = mask
                break
    assert len(basis) == len(edges) - 80 + 1 == 81
    rng = np.random.default_rng(20261109)
    theta = rng.uniform(-0.8, 0.8, len(edges))
    psi = rng.normal(size=80) + 1j * rng.normal(size=80)
    chi = rng.uniform(-1.0, 1.0, 80)
    theta2 = theta + np.array([chi[p] - chi[l] for p, l in edges])
    psi2 = psi * np.exp(1j * chi)
    def action(phase, field):
        kinetic = sum(abs(field[p] - np.exp(1j * phase[k]) * field[l]) ** 2
                      for k, (p, l) in enumerate(edges))
        curvature = sum(1 - np.cos(sum(sign * phase[k] for k, sign in signs))
                        for _, signs in masks)
        return (kinetic + 0.13 * curvature + 0.15 * np.sum(abs(field)**2)
                + 0.02 * np.sum(abs(field)**4)).real
    before, after = action(theta, psi), action(theta2, psi2)
    relative = abs(after - before) / max(1.0, abs(before))
    assert relative < 2e-12
    L = np.zeros((80, 80), dtype=complex)
    for k, (p, l) in enumerate(edges):
        U = np.exp(1j * theta[k])
        L[p, p] += 1; L[l, l] += 1
        L[p, l] -= U; L[l, p] -= U.conjugate()
    ph = np.exp(1j * chi)
    Lnew = ph[:, None] * L * ph.conj()[None, :]
    lap_cov_error = np.max(abs(Lnew @ psi2 - ph * (L @ psi)))
    assert lap_cov_error < 2e-12
    return dict(points=40, lines=40, incidence_graph_vertices=80,
                incidence_edges=len(edges), girth=8, distinct_eight_cycles=len(loops),
                binary_cycle_rank=len(basis), cycle_dependencies=len(loops)-len(basis),
                free_U1_cycle_fluxes=len(edges)-80+1,
                if_all_loops_attached_as_2cells_beta2=len(loops)-len(basis),
                finite_gauge_action='sum |psi_p-exp(i theta_e)psi_l|^2 + .13 sum_(8cycles)(1-cos holonomy) + .15 sum|psi|^2 + .02 sum|psi|^4',
                relative_gauge_action_error=relative,
                laplacian_covariance_error=float(lap_cov_error),
                scope='kinematic, U(1) covariant finite-graph action; not time evolution, 3+1D limit or Einstein gravity')


I = (1, 0, 0, 1)
def matmul(a, b):
    x, y, z, w = a; u, v, s, t = b
    return ((x*u + y*s) % 3, (x*v + y*t) % 3,
            (z*u + w*s) % 3, (z*v + w*t) % 3)

def matord(a):
    x = I
    for j in range(1, 25):
        x = matmul(x, a)
        if x == I: return j
    raise AssertionError(a)

def q8_choi():
    group = sorted(s for s in itertools.product(range(3), repeat=4)
                   if (s[0]*s[3] - s[1]*s[2]) % 3 == 1)
    q8 = frozenset(x for x in group if matord(x) in (1, 2, 4))
    assert len(group) == 24 and len(q8) == 8
    cosets = sorted({frozenset(matmul(g, q) for q in q8) for g in group}, key=lambda x: sorted(x))
    assert len(cosets) == 3
    w = np.exp(2j * np.pi/3)
    Fourier = np.array([[w**(i*j) for j in range(3)] for i in range(3)], complex) / np.sqrt(3)
    Phase = np.diag([1, 1, w]).astype(complex)
    gates = [((0, 2, 1, 0), Fourier), ((1, 0, 1, 1), Phase)]
    U = {I: np.eye(3, dtype=complex)}
    queue = [I]
    for s in queue:
        for t, unitary in gates:
            st = matmul(s, t)
            if st not in U:
                U[st] = U[s] @ unitary
                queue.append(st)
    assert len(U) == 24
    X = np.roll(np.eye(3), 1, axis=0)
    Z = np.diag([w**j for j in range(3)])
    families=[]
    for coset in cosets:
        bases=[]
        for g in sorted(coset):
            basis = [((np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b) @ U[g]).T.reshape(9)/np.sqrt(3))
                     for a,b in itertools.product(range(3), repeat=2)]
            bases.append(np.column_stack(basis))
        families.append(bases)
    return families


def collision_variance(p, shots):
    c = np.sum(p**2)
    r = np.sum(p**3)
    return (2*(c-c*c)+4*(shots-2)*(r-c*c))/(shots*(shots-1))


def u_stat_variance_exact(p):
    # N=3 exact complete enumeration of all 9^3 measurement sequences.
    c = float(np.dot(p,p))
    v = 0.0
    for a,b,d in itertools.product(range(9), repeat=3):
        val = (int(a == b)+int(a == d)+int(b == d))/3
        v += float(p[a]*p[b]*p[d])*(val-c)**2
    return v


def photonic_meter():
    families = q8_choi()
    cases = {
        'product': np.array([1,0,0], float),
        'partially_entangled': np.sqrt(np.array([.7,.2,.1])),
        'maximally_entangled': np.ones(3)/np.sqrt(3),
    }
    rows={}
    max_error=0.0
    efficiency=np.array([0.63 + 0.045*j for j in range(9)])
    for name, schmidt in cases.items():
        v=np.zeros(9, complex)
        for j in range(3): v[4*j]=schmidt[j]
        rho=np.outer(v,v.conj())
        expected_L=1-float(np.sum(schmidt**4))
        cs=[]; variances=[]; distorted=[]; corrected=[]
        for bases in families:
            c_list=[]; v_list=[]; distorted_list=[]; corrected_list=[]
            for E in bases:
                p=np.real(np.sum(E.conj()*(rho@E), axis=0))
                assert abs(sum(p)-1)<1e-12 and min(p)>-1e-11
                c_list.append(float(np.dot(p,p)))
                v_list.append(float(collision_variance(p, 256)))
                observed=efficiency*p/np.dot(efficiency,p)
                distorted_list.append(float(observed@observed))
                unwarped=(observed/efficiency); unwarped/=sum(unwarped)
                corrected_list.append(float(unwarped@unwarped))
                if name=='partially_entangled':
                    max_error=max(max_error,abs(float(collision_variance(p,3))-u_stat_variance_exact(p)))
            cs.append(sum(c_list))
            variances.append(2.25*sum(v_list))
            distorted.append(sum(distorted_list))
            corrected.append(sum(corrected_list))
        inferred=[1.5*(c-4/3) for c in cs]
        assert max(abs(x-expected_L) for x in inferred)<1e-11
        assert max(abs(x-cs[0]) for x in corrected)<1e-11
        rows[name]=dict(actual_linear_entropy=expected_L, per_coset_collision_sums=cs,
                        recovered_linear_entropies=inferred,
                        u_stat_256_shots_per_basis_standard_error=math.sqrt(variances[0]),
                        mean_efficiency_distorted_collision=sum(distorted)/3,
                        apparent_entropy_if_loss_ignored=1.5*(sum(distorted)/3-4/3),
                        max_calibrated_loss_correction_error=max(abs(x-cs[0]) for x in corrected),
                        efficiency_distorted_max_minus_min=max(distorted)-min(distorted))
    eta=0.82
    schmidt=cases['partially_entangled']; v=np.zeros(9,complex)
    for j in range(3):v[4*j]=schmidt[j]
    rhop=eta*np.outer(v,v.conj())+(1-eta)*np.eye(9)/9
    mix=[]
    for bases in families:
        c=sum(float(p@p) for E in bases
              for p in [np.real(np.sum(E.conj()*(rhop@E),axis=0))])
        mix.append(c)
    pure_centered=rows['partially_entangled']['per_coset_collision_sums'][0]-8/9
    mixed_centered=mix[0]-8/9
    assert max(abs(x-mix[0]) for x in mix)<1e-11
    assert abs(mixed_centered-eta*eta*pure_centered)<1e-11
    rng=np.random.default_rng(419)
    # Independent Monte Carlo for the U statistic, no MUB matrix involved.
    sample_p=np.array([.31,.25,.16,.12,.08,.04,.02,.015,.005]); sample_p/=sum(sample_p)
    N=30; B=2500; us=[]
    for _ in range(B):
        counts=rng.multinomial(N,sample_p)
        us.append(float(sum(counts*(counts-1))/(N*(N-1))))
    predicted=float(collision_variance(sample_p,N))
    mc=float(np.var(us, ddof=1))
    assert abs(mc/predicted-1)<.13
    eps=.1; alpha=.05
    pairs=math.ceil(9*math.log(2/alpha)/eps**2)
    return dict(three_Q8_cosets=3, nine_outcomes_per_basis=9,
                exact_formula='L_pure=3/2*(sum_(8 bases,j) p_bj^2-4/3)',
                unbiased_estimator='c_hat_b=sum_j n_bj(n_bj-1)/(N(N-1))',
                exact_Ustat_variance='[2(c-c^2)+4(N-2)(r-c^2)]/[N(N-1)], r=sum p_j^3',
                exact_N3_variance_error=max_error,
                Monte_Carlo_variance_ratio=mc/predicted,
                Hoeffding_95pct_epsilon_0_1_pairs_per_basis=pairs,
                Hoeffding_95pct_epsilon_0_1_total_preparations_per_coset=16*pairs,
                depolarizing_eta=eta, depolarizing_scale_factor=mixed_centered/pure_centered,
                calibrated_eta_recovers_pure_entanglement=True,
                input_cases=rows,
                diagnostic_warning='product state exhibits zero three-coset spread but a positive apparent entanglement under identical outcome-dependent loss; cross-coset agreement is NOT a loss-free certificate',
                scope='ideal projective measurements, IID source, known settings; mixed-state entropy is not determined without purity/depolarization model')


def chirality_anomaly_and_no_go():
    # Left-handed Weyl fields of one SM family; nu^c permitted at Y=0.
    Q, u, d, L, e = F(1,6), F(-2,3), F(1,3), F(-1,2), F(1)
    cubic_su3=2-1-1
    su3square_u1=2*Q+u+d
    su2square_u1=3*Q+L
    fields=[(6,Q),(3,u),(3,d),(2,L),(1,e),(1,F(0))]
    u1cube=sum(n*y**3 for n,y in fields)
    gravitational_u1=sum(n*y for n,y in fields)
    witten_doublets=3+1
    anomalies=dict(SU3_cubic=cubic_su3, SU3square_U1=str(su3square_u1),
                   SU2square_U1=str(su2square_u1), U1_cubic=str(u1cube),
                   gravsquare_U1=str(gravitational_u1), Witten_SU2_doublets=witten_doublets)
    assert cubic_su3==su3square_u1==su2square_u1==u1cube==gravitational_u1==0
    assert witten_doublets%2==0
    assert all((n*su3square_u1,n*u1cube)==(0,0) for n in range(1,11))
    # V(sigma)=(sigma^2-1)^2, symmetric under sigma -> -sigma;
    # h*sigma is an explicit, externally provided parity-breaking field.
    minima={str(s):dict(even_potential=(s*s-1)**2,second_derivative=12*s*s-4)
            for s in (-1,1)}
    assert minima['-1']==minima['1']
    return dict(per_family_anomalies=anomalies,
                all_family_counts_from_1_to_10_anomaly_free=True,
                finite_parity_symmetric_double_well_minima=minima,
                selection='no unique sign without extra symmetry breaking or boundary/thermodynamic prescription',
                regulator='must build gauge-covariant Weyl operator, prove anomaly cancellation and no light mirrors, controlled continuum',
                scope='anomaly cancellation alone does not select three families or chiral handedness; E8 order-3 shift restriction is an additional assumption')


def cosmo_prereg_audit(repo_root):
    path=repo_root/'analysis'/'toe_uv'/'prereg_noshear.json'
    frozen=json.loads(path.read_text(encoding='utf-8'))['S9_shear_no_split']
    assert frozen['frozen']=='2026-11-08'
    result={}
    for survey, v in frozen['current_values'].items():
        gap=v['CPL']-v['free_neg']
        peak=max(abs(v[k]-v['LCDM']) for k in ('free_neg','free_pos','CPL'))
        assert abs(gap)<2 and peak<4
        result[survey]=dict(delta_chi2_CPL_minus_fading=gap,
                            largest_abs_delta_chi2_from_LCDM=peak,
                            margin_to_predicted_2_gap=2-abs(gap),
                            margin_to_predicted_4_LCDM=4-peak)
    return dict(frozen_date=frozen['frozen'], controls=result,
                predictions_apply_only_to='FUTURE DES Y6, KiDS successor, HSC Y3 or Euclid DR1 using same pipeline and cuts',
                reuses_repository_numbers_not_new_likelihood=True,
                nonlinear_model='only corrected scalar-field Halofit/HMcode; original scalar-field shear comparisons withdrawn',
                evidence='baseline control passes frozen numerical criterion; future independent survey not evaluated',
                interpretation='current data do not distinguish fading from CPL; no unique scalar-field dynamics derived')


def main(out=None):
    root=Path(__file__).resolve().parent.parent
    result=dict(status='PASS_ALL_FIVE_NUMERICAL_AND_EXACT_INTERNAL_CHECKS_WITH_LIMITATIONS',
                pentad=s5_singlet(),
                photonic=photonic_meter(),
                gauge_dynamics=gauge_geometry_and_action(),
                chirality=chirality_anomaly_and_no_go(),
                cosmology=cosmo_prereg_audit(root))
    if out: Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS', json.dumps({
        'pentad_high_singlets':result['pentad']['high_M_S5_singlets'],
        'gauge_flux_rank':result['gauge_dynamics']['binary_cycle_rank'],
        'gauge_action_error':result['gauge_dynamics']['relative_gauge_action_error'],
        'photonic_variance_exact_error':result['photonic']['exact_N3_variance_error'],
        'cosmology_control_gaps':{k:round(v['delta_chi2_CPL_minus_fading'],5) for k,v in result['cosmology']['controls'].items()}}))
    return result

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else None)
