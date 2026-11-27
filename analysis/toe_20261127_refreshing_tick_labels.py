"""Replica transfer for locally refreshed tick labels on a ring."""
import json
from math import log

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from toe_20261127_full_tick_transfer_cycles import tick_projectors


def refresh_both(matrix, epsilon):
    """Apply M tensor M without materializing its square matrix."""
    size = len(matrix)
    stay = 1-epsilon
    uniform = epsilon/size
    return (stay**2*matrix + stay*uniform*(matrix.sum(0)+matrix.sum(1)[:, None])
            + uniform**2*matrix.sum())


def build():
    P = tick_projectors()
    size = len(P)
    classes = np.rint(np.einsum("aij,bji->ab", P, P).real).astype(int)
    s = .5
    z = 3+6*s*s
    overlaps = (9*s*s+6*s*(1-s)+(1-s)**2*classes)/z
    root = np.sqrt(overlaps)
    masks = [classes == c for c in (3, 0, 1)]
    predicted = (3*11+117*17)/size**2
    rows = []
    for epsilon in (1., .25, .05, .01, .002, .0005):
        M = (1-epsilon)*np.eye(size)+epsilon/size
        def apply(v):
            return (root*refresh_both(root*v.reshape(size, size), epsilon)).ravel()
        S = LinearOperator((size**2, size**2), matvec=apply, dtype=float)
        x = np.arange(size**2, dtype=float).reshape(size, size)/size**2
        assert np.max(abs(refresh_both(x,epsilon)-M@x@M.T)) < 1e-13
        # Each class is an orbit of permutations of directions and their outcomes.
        basis = np.column_stack([(mask/np.sqrt(mask.sum())).ravel() for mask in masks])
        sub = S @ basis[:, 0], S @ basis[:, 1], S @ basis[:, 2]
        sub = np.column_stack(sub)
        quotient = basis.T @ sub
        assert np.max(abs(sub-basis@quotient)) < 1e-13
        assert np.max(abs(quotient-quotient.T)) < 1e-13
        lam = float(np.linalg.eigvalsh(quotient)[-1])
        full = eigsh(S,k=2,which="LA",tol=1e-11,
                     v0=np.random.default_rng(41).normal(size=size**2),
                     return_eigenvectors=False)
        assert abs(lam-full[-1]) < 1e-11
        if epsilon == 1:
            assert abs(lam-overlaps.mean()) < 1e-13
        # Independent two-site hidden-label contraction and physical purity.
        A = s*np.eye(9)+(1-s)*P
        K2 = np.einsum("ab,aij,bkl->ikjl",M**2,A,A,optimize=True).reshape(81,81)
        K2 /= np.sum(M**2)
        measured = np.trace(K2@K2).real/z**2
        # Trace S^2 uses the entrywise squared single-label kernel.
        squared = M**2
        expected = np.sum(overlaps*(squared@overlaps@squared.T))/np.sum(squared)**2
        assert abs(measured-expected) < 1e-12
        gap = float(full[-1]-full[-2])
        rows.append({"refresh_probability": epsilon,"replica_perron_root": lam,
                     "replica_gap": gap, "gap_over_epsilon_squared": gap/epsilon**2,
                     "classical_label_length": -1/log(1-epsilon) if epsilon < 1 else 0.,
                     "replica_relative_gap_length": -1/log(full[-2]/lam) if full[-2] > 1e-13 else 0.,
                     "two_site_bulk_normalized_trace": float(expected)})
    assert abs(rows[-1]["gap_over_epsilon_squared"]/predicted-1) < .03
    return {"status": "PASS", "replica_gap_small_refresh_coefficient": predicted,
            "rows": rows, "cycle_fugacity_ratio_after_bulk_normalization":
                {"zero_refresh": "1/120", "positive_fixed_refresh": "1"}}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
