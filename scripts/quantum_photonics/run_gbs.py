"""Small Gaussian Boson Sampling benchmark script
Usage: python scripts/quantum_photonics/run_gbs.py --modes 6 --squeezing 0.8 --loss 0.9 --shots 1000

This script uses Strawberry Fields for Gaussian sampling and The Walrus for hafnian-based probabilities on small instances.
"""

import argparse
import json
import math

import matplotlib.pyplot as plt
import numpy as np

try:
    import strawberryfields as sf
    from strawberryfields.ops import Interferometer, MeasureFock, Sgate
    from thewalrus import hafnian
except Exception as e:
    print("Missing quantum photonics dependencies:", e)
    raise


def build_interferometer(modes, seed=0):
    np.random.seed(seed)
    # random unitary via QR
    X = np.random.normal(size=(modes, modes)) + 1j * np.random.normal(
        size=(modes, modes)
    )
    Q, R = np.linalg.qr(X)
    return Q


from collections import Counter
from math import log

from scipy.stats import entropy


def compute_exact_probs_fock(modes, squeezing, U, cutoff=6):
    """Use the Fock backend to compute exact probabilities (small instances)."""
    eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff})
    prog = sf.Program(modes)
    with prog.context as q:
        for i in range(modes):
            Sgate(squeezing) | q[i]
        Interferometer(U) | q
        # measure all modes in Fock basis to obtain the full distribution
        for i in range(modes):
            MeasureFock() | q[i]
    state = eng.run(prog).state
    # all_fock_probs returns an N-dimensional array with shape (cutoff,)*modes
    probs = state.all_fock_probs()
    import numpy as _np

    probs = _np.asarray(probs)
    d = {}
    for idx, p in _np.ndenumerate(probs):
        d[idx] = float(p)
    return d


def sample_gbs(modes=6, squeezing=0.8, U=None, backend="gaussian", shots=200, cutoff=6):
    if U is None:
        U = build_interferometer(modes)
    if backend == "fock":
        # many Fock backends do not implement multi-shot MeasureFock; instead compute exact distribution
        exact = compute_exact_probs_fock(modes, squeezing, U, cutoff=cutoff)
        # build categorical distribution and draw samples
        import random

        keys = list(exact.keys())
        probs = [exact[k] for k in keys]
        # normalize (numerical stability)
        s = sum(probs)
        if s <= 0:
            # fallback: draw all-zero samples
            return np.zeros((shots, modes), dtype=int)
        probs = [p / s for p in probs]
        draws = random.choices(keys, weights=probs, k=shots)
        samples = np.array(draws, dtype=int)
        return samples
    else:
        # gaussian sampling (note: gaussian backend cannot update conditional state after Fock measurements)
        eng = sf.Engine("gaussian")
        prog = sf.Program(modes)
        with prog.context as q:
            for i in range(modes):
                Sgate(squeezing) | q[i]
            Interferometer(U) | q
            for i in range(modes):
                MeasureFock() | q[i]
        results = eng.run(prog, shots=shots)
        samples = results.samples
        return samples


def kl_between_empirical_and_exact(emp_samples, exact_probs, cutoff=6):
    # compute empirical distribution over keys present in exact_probs (tuples)
    total = len(emp_samples)
    counts = Counter(tuple(s) for s in emp_samples)
    # build aligned probability vectors
    keys = list(exact_probs.keys())
    p_emp = []
    p_exact = []
    eps = 1e-12
    for k in keys:
        p_emp.append(counts.get(k, 0) / total)
        p_exact.append(exact_probs.get(k, 0.0))
    # avoid zeros in p_exact for KL
    p_exact = [max(eps, v) for v in p_exact]
    p_emp = [max(eps, v) for v in p_emp]
    return entropy(p_emp, p_exact)


# -- Hafnian-based analytic probabilities (unnormalized weight -> normalized prob) --
from math import factorial


def _pattern_iterator(modes, max_total):
    """Yield all photon-number patterns (tuples) with total photons <= max_total."""
    from itertools import product

    for tup in product(range(max_total + 1), repeat=modes):
        if sum(tup) <= max_total:
            yield tup


def compute_hafnian_probs(modes, squeezings, U, max_total_photons=4):
    """Compute (normalized) probability distribution over small photon-number patterns using loop-hafnian weights.

    This computes weights proportional to |loop_hafnian(A_sub)|^2 / prod(factorial(n_i)), where
    A = U @ diag(tanh(r)) @ U.T, and A_sub is the matrix formed by repeating rows/cols according to the pattern.
    The result is normalized over all patterns with total photons <= max_total_photons.
    """
    import numpy as _np
    import thewalrus as _tw

    t = _np.tanh(_np.asarray(squeezings))
    D = _np.diag(t)
    A = U @ D @ U.T

    probs = {}
    weights = {}
    total_weight = 0.0
    for patt in _pattern_iterator(modes, max_total_photons):
        N = sum(patt)
        if N == 0:
            # vacuum probability weight handled via hafnian of zero-dim matrix = 1
            w = 1.0
        else:
            # build repeated index list
            idxs = []
            for i, k in enumerate(patt):
                idxs.extend([i] * k)
            if len(idxs) == 0:
                w = 1.0
            else:
                sub = A[_np.ix_(idxs, idxs)]
                # loop_hafnian returns complex; weight from magnitude squared
                lh = _tw.loop_hafnian(sub)
                # normalization by product of factorials to account for repeated photons
                norm = (
                    _np.prod([factorial(k) for k in patt if k > 0])
                    if any(k > 0 for k in patt)
                    else 1
                )
                # include product of tanh(r_i)^{n_i} as heuristic prefactor
                tanh_pref = (
                    float(_np.prod([t[i] ** patt[i] for i in range(modes)]))
                    if any(k > 0 for k in patt)
                    else 1.0
                )
                w = (_np.abs(lh) ** 2) * tanh_pref / float(norm)
        weights[patt] = float(w)
        total_weight += float(w)
    if total_weight <= 0:
        # fallback: make vacuum probability 1
        return {tuple([0] * modes): 1.0}
    for patt, w in weights.items():
        probs[patt] = w / total_weight
    return probs


# -- Threshold detection probabilities using TheWalrus --


def apply_loss_to_cov_mu(mu, cov, eta, hbar=2.0):
    """Apply independent loss eta to each mode's (mu, cov) in xp ordering.

    For each mode, quadrature transforms: x' = sqrt(eta) x + sqrt(1-eta) x_vac
    Therefore, cov' = eta cov + (1-eta) * (hbar/2) * I
    and mu' = sqrt(eta) * mu
    """
    import numpy as _np

    mu = _np.asarray(mu)
    cov = _np.asarray(cov)
    modes = mu.size // 2
    # scale mean
    mu2 = _np.copy(mu)
    for m in range(modes):
        mu2[2 * m : 2 * m + 2] = _np.sqrt(eta) * mu2[2 * m : 2 * m + 2]
    # scale cov
    cov2 = eta * cov + (1.0 - eta) * (hbar / 2.0) * _np.eye(2 * modes)
    return mu2, cov2


def compute_threshold_probs(modes, squeezings, U, eta=1.0):
    """Compute threshold (click/no-click) detection probabilities for all 2^m patterns.

    Uses Strawberry Fields Gaussian backend to compute the Gaussian state's mean and covariance
    and then calls TheWalrus's threshold_detection_prob for each binary detection pattern.
    """
    import numpy as _np
    import thewalrus as _tw

    # build SF Gaussian state and extract mu/cov in xp ordering
    prog = sf.Program(modes)
    with prog.context as q:
        for i in range(modes):
            Sgate(squeezings[i]) | q[i]
        Interferometer(U) | q
    eng = sf.Engine("gaussian")
    res = eng.run(prog)
    state = res.state
    mu = _np.asarray(state.means())  # shape (2*modes,)
    cov = _np.asarray(state.cov())  # shape (2*modes,2*modes)
    # apply loss
    mu2, cov2 = apply_loss_to_cov_mu(mu, cov, eta)
    # enumerate patterns
    probs = {}
    from itertools import product

    for patt in product([0, 1], repeat=modes):
        patt_arr = _np.array(patt, dtype=int)
        p = float(_tw.threshold_detection_prob(mu2, cov2, patt_arr, hbar=2.0))
        probs[tuple(patt)] = p
    # normalize (numerical)
    s = sum(probs.values())
    if s <= 0:
        # degenerate fallback
        return {tuple([0] * modes): 1.0}
    for k in list(probs.keys()):
        probs[k] = probs[k] / s
    return probs


def run_gbs(modes=6, squeezing=0.8, loss=1.0, shots=200, backend="gaussian", cutoff=6):
    """Run GBS sampling and return samples and optional exact probabilities (if backend='fock' or requested)."""
    U = build_interferometer(modes)
    samples = sample_gbs(
        modes=modes,
        squeezing=squeezing,
        U=U,
        backend=backend,
        shots=shots,
        cutoff=cutoff,
    )
    exact = None
    kl = None
    if backend == "fock":
        exact = compute_exact_probs_fock(modes, squeezing, U, cutoff=cutoff)
        kl = kl_between_empirical_and_exact(samples, exact, cutoff=cutoff)
    return samples, exact, kl


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--modes", type=int, default=6)
    p.add_argument("--squeezing", type=float, default=0.8)
    p.add_argument("--loss", type=float, default=1.0)
    p.add_argument("--shots", type=int, default=200)
    args = p.parse_args()

    samples = run_gbs(
        modes=args.modes, squeezing=args.squeezing, loss=args.loss, shots=args.shots
    )
    print("Sample shape", samples.shape)
    # simple histogram of total photons
    totals = np.sum(samples, axis=1)
    import matplotlib.pyplot as plt

    plt.hist(totals, bins=range(int(totals.max()) + 2))
    plt.title(f"GBS photon counts modes={args.modes} r={args.squeezing}")
    plt.savefig("gbs_photon_hist.png")
    print("Saved gbs_photon_hist.png")


if __name__ == "__main__":
    main()
