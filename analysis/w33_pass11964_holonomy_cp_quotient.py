"""Gauge-invariant CP diagnostic for TOE57's finite spinless holonomy model.

Fixed beta=4, mu=0. No claim of a chiral SM or a global vacuum theorem.
The spanning-tree criterion is exact; the extremum search is numerical.
"""
from pathlib import Path
import itertools
import json
import sys
import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep, cycle_row
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords


def cp_loop_residual(phases, edges):
    """Gauge-invariant distance from conjugation equivalence, via tree loops.

    U and U* are vertex-gauge equivalent iff every fundamental Wilson loop
    is real. Tree gauge removes tree phases; chord phases are loop phases.
    This tests the specified conjugation operation, without graph relabeling.
    """
    chords = set(spanning_chords(edges))
    adj = [[] for _ in range(80)]
    for j, (a, b) in enumerate(edges):
        if j not in chords:
            adj[a].append((b, phases[j]))
            adj[b].append((a, -phases[j]))
    potential = np.zeros(80)
    seen = {0}; queue = [0]
    for a in queue:
        for b, angle in adj[a]:
            if b not in seen:
                seen.add(b); queue.append(b)
                potential[b] = potential[a] + angle
    assert len(seen) == 80
    loops = np.array([phases[j] + potential[a] - potential[b]
                      for j, (a, b) in enumerate(edges) if j in chords])
    return float(np.max(abs(np.sin(loops)))), loops


def setup():
    edges, volts, lookup, octs, comm, picked, *_ = prep()
    # Three selected fundamental chords carry unit voltages, all others zero.
    assert np.array_equal(volts[picked], np.eye(3, dtype=int))
    P = np.array([cycle_row(w, edges, volts, lookup, np.zeros(3)).real
                  for w in octs + comm])
    assert np.max(abs(P @ volts)) == 0
    return edges, volts, picked


def free_energy(phi, edges, volts, beta=4.):
    phases = volts @ phi
    H = np.zeros((80, 80), complex)
    for angle, (a, b) in zip(phases, edges):
        H[a, b] -= np.exp(1j * angle)
        H[b, a] -= np.exp(-1j * angle)
    levels = np.linalg.eigvalsh(H)
    return float(-np.logaddexp(0., -beta * levels).sum() / beta)


def local_derivatives(phi, edges, volts, beta=4.):
    """Spectral divided-difference Hessian, including degenerate eigenvalues."""
    H = np.zeros((80,80),complex)
    dH = np.zeros((3,80,80),complex)
    ddH = np.zeros((3,3,80,80),complex)
    for row, (a,b) in zip(volts,edges):
        z = np.exp(1j*row@phi)
        H[a,b] -= z; H[b,a] -= z.conjugate()
        for i in range(3):
            dH[i,a,b] -= 1j*row[i]*z
            dH[i,b,a] += 1j*row[i]*z.conjugate()
            for j in range(3):
                ddH[i,j,a,b] += row[i]*row[j]*z
                ddH[i,j,b,a] += row[i]*row[j]*z.conjugate()
    ev,U = np.linalg.eigh(H)
    occupation = 1/(1+np.exp(beta*ev))
    gap=ev[:,None]-ev[None,:]
    diff=occupation[:,None]-occupation[None,:]
    close=abs(gap)<1e-10
    divided=np.zeros_like(gap)
    np.divide(diff,gap,out=divided,where=~close)
    midpoint=(occupation[:,None]+occupation[None,:])/2
    divided[close]=(-beta*midpoint*(1-midpoint))[close]
    V=np.array([U.conj().T@x@U for x in dH])
    grad=np.array([np.dot(occupation,np.diag(x)).real for x in V])
    hessian=np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            direct=np.dot(occupation,np.diag(U.conj().T@ddH[i,j]@U)).real
            hessian[i,j]=direct+np.sum(divided*V[i]*V[j].T).real
    assert np.max(abs(hessian-hessian.T))<1e-12
    return grad,hessian


def payload():
    edges, volts, picked = setup()
    F = lambda phi: free_energy(np.asarray(phi), edges, volts)
    F0 = F(np.zeros(3))
    corners = []
    for bits in itertools.product((0, 1), repeat=3):
        phi = np.pi * np.array(bits)
        cp, _ = cp_loop_residual(volts @ phi, edges)
        assert cp < 1e-14
        corners.append(dict(pi_bits=list(bits), energy=F(phi), cp_residual=cp))
    # Fixed starts cover eight conjugation-fixed corners and random torus points.
    rng = np.random.default_rng(11964)
    starts = [np.pi*np.array(c['pi_bits']) for c in corners]
    starts += list(rng.uniform(-np.pi, np.pi, (24, 3)))
    roots = []
    for x in starts:
        fit = minimize(F, x, method='BFGS', options={'gtol':1e-7, 'maxiter':200})
        phi = (fit.x + np.pi) % (2*np.pi) - np.pi
        cp, _ = cp_loop_residual(volts @ phi, edges)
        roots.append(dict(phi=phi.tolist(), energy=F(phi),
                          success=bool(fit.success), cp_residual=cp))
    best = min(roots, key=lambda r:r['energy'])
    corner = min(corners, key=lambda r:r['energy'])
    phi_corner=np.pi*np.array(corner['pi_bits'])
    grad,hess=local_derivatives(phi_corner,edges,volts)
    assert max(abs(grad))<1e-12
    eig=np.linalg.eigvalsh(hess)
    assert min(eig)>0
    # Verify a genuine local minimum with an independent difference calculation.
    eps=.01; finite=np.zeros((3,3)); eye=np.eye(3)
    for i in range(3):
        finite[i,i]=(F(phi_corner+eps*eye[i])+F(phi_corner-eps*eye[i])-2*F(phi_corner))/eps**2
        for j in range(i+1,3):
            finite[i,j]=finite[j,i]=(F(phi_corner+eps*(eye[i]+eye[j]))-F(phi_corner+eps*(eye[i]-eye[j]))-F(phi_corner+eps*(-eye[i]+eye[j]))+F(phi_corner-eps*(eye[i]+eye[j])))/(4*eps**2)
    assert np.max(abs(finite-hess))<1e-5
    # CP-positive control and arbitrary vertex-gauge transformation.
    trial = np.array([.3, -.7, .9]); phases=volts@trial
    cp, loops = cp_loop_residual(phases, edges)
    assert abs(cp-max(abs(np.sin(trial)))) < 1e-13
    chi = rng.normal(size=80)
    shifted = phases + np.array([chi[b]-chi[a] for a,b in edges])
    cp2, loops2 = cp_loop_residual(shifted, edges)
    gauge_err = float(np.max(abs(np.exp(1j*loops)-np.exp(1j*loops2))))
    assert gauge_err < 1e-13 and abs(cp-cp2)<1e-13
    assert abs(F(trial)-F(-trial))<1e-12
    return dict(status='PASS', model='TOE57 native spinless hopping, beta=4, mu=0, unit hopping',
                selected_chords=list(map(int,picked)), zero_energy=F0,
                exact_criterion='U and conjugate(U) are vertex-gauge equivalent iff every fundamental Wilson loop is real; in this unit-voltage family iff phi_i=0 or pi modulo2pi.',
                corners=corners, numerical_multistart=roots, best_numerical=best,
                best_conjugation_fixed_corner=corner,
                corner_gradient=grad.tolist(),corner_hessian=hess.tolist(),
                corner_hessian_eigenvalues=eig.tolist(),
                hessian_finite_difference_max_error=float(np.max(abs(finite-hess))),
                energy_difference_best_vs_corner=best['energy']-corner['energy'],
                gauge_invariance_residual=gauge_err,
                cp_breaking_positive_control=cp,
                scope='Exact conjugation quotient criterion. Numerical32-start extremum survey is not a certified global minimum, thermodynamic spontaneous symmetry breaking, physical CP transformation with spatial parity, or a chiral Standard Model. Lieb1994 is motivation, not a theorem applied to this nonplanar marked graph.',
                prior=['analysis/w33_20261013_toe57_fermion_holonomy.py',
                       'analysis/w33_20261013_toe57_one_loop_competition.py'],
                primary='https://arxiv.org/abs/cond-mat/9410025')


if __name__ == '__main__':
    result = payload()
    (ROOT/'data/w33_pass11964_holonomy_cp_quotient.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','zero_energy','best_numerical','best_conjugation_fixed_corner','energy_difference_best_vs_corner')}),flush=True)
