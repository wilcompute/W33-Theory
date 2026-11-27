"""A local boson-Grassmann determinant ratio for component weights."""
import json
from itertools import combinations, permutations
from math import acosh, exp, expm1, log

import numpy as np

from toe_20261127_free_square_gluing_components import orbit_count


def normalized_log_error(eigenvalues, epsilon, delta, components):
    """Remove the exact zero-mode contribution before numerical evaluation."""
    assert np.count_nonzero(abs(eigenvalues)<1e-9) == components
    positive = eigenvalues[components:]
    return float(np.sum(np.log1p(epsilon/positive)-np.log1p(delta/positive)))


def exhaustive_graphs(n):
    edges = list(combinations(range(n),2))
    delta = n**-3
    epsilon = delta/n**2
    max_error = 0.
    for mask in range(1<<len(edges)):
        laplacian = np.zeros((n,n))
        sets = [{v} for v in range(n)]
        for j,(u,v) in enumerate(edges):
            if mask>>j&1:
                laplacian[u,u] += 1
                laplacian[v,v] += 1
                laplacian[u,v] -= 1
                laplacian[v,u] -= 1
                sets[u] = sets[v] = sets[u]|sets[v]
                for w in sets[u]:
                    sets[w] = sets[u]
        sizes = [len(block) for block in {frozenset(block) for block in sets}]
        m = len(sizes)
        es = np.linalg.eigvalsh(laplacian)
        error = normalized_log_error(es,epsilon,delta,m)
        bound = (delta-epsilon)*sum((v*v-1)/6 for v in sizes)
        assert -bound-1e-12 <= error <= 1e-12
        max_error = max(max_error,-error)
    path_eigenvalues = 2-2*np.cos(np.pi*np.arange(1,n)/n)
    assert abs(np.sum(1/path_eigenvalues)-(n*n-1)/6)<1e-12
    return {"n":n,"graphs":1<<len(edges),"worst_log_error":max_error,
            "path_trace_pseudoinverse":float(sum(1/path_eigenvalues))}


def flat_permutation_check(n):
    q = n**-2
    delta = n**-3
    epsilon = q*delta
    perms = list(permutations(range(n)))
    target, local = [], []
    connected = []
    I = np.eye(n)
    matrices = {p:I[:,p] for p in perms}
    for a in perms:
        for b in perms:
            if not all(a[b[i]]==b[a[i]] for i in range(n)):
                continue
            m = orbit_count(a,b)
            Pa,Pb = matrices[a],matrices[b]
            es = np.linalg.eigvalsh(4*I-Pa-Pa.T-Pb-Pb.T)
            weight = q**m
            target.append(weight)
            local.append(weight*exp(normalized_log_error(es,epsilon,delta,m)))
            connected.append(m==1)
    a,b = np.array(target),np.array(local)
    a /= a.sum()
    b /= b.sum()
    distance = float(np.sum(abs(a-b))/2)
    assert distance <= expm1((delta-epsilon)*n*n/6)
    return {"n":n,"commuting_pairs":len(a),"total_variation":distance,
            "connected_ideal":float(a[connected].sum()),"connected_local":float(b[connected].sum())}


def controls():
    epsilon,delta = .01,.1
    rows = []
    for n in (8,32,128,512):
        ratio = exp(2*(log(-expm1(-n*acosh(1+epsilon/2)))
                       -log(-expm1(-n*acosh(1+delta/2)))))
        spectral = 2-2*np.cos(2*np.pi*np.arange(n)/n)
        log_direct = np.log(spectral+epsilon).sum()-np.log(spectral+delta).sum()
        assert abs(log_direct-n*(acosh(1+epsilon/2)-acosh(1+delta/2))-log(ratio))<1e-10
        rows.append({"cycle_length":n,"massive_bulk_normalized_weight":ratio})
    n = 12
    delta = 1e-6
    epsilon = delta/100
    twisted = []
    for turn in (0.,1/3):
        es = 2-2*np.cos(2*np.pi*(np.arange(n)+turn)/n)
        w = float(np.exp(np.log(es+epsilon).sum()-np.log(es+delta).sum()))
        twisted.append({"holonomy_turns":turn,"determinant_ratio":w})
    assert abs(twisted[0]["determinant_ratio"]-.01)<1e-6
    assert twisted[1]["determinant_ratio"]>.999
    return rows,twisted


def build():
    fixed, twisted = controls()
    return {"status":"PASS","all_graphs":[exhaustive_graphs(n) for n in (3,4,5)],
            "flat_cover_check":flat_permutation_check(5),
            "fixed_mass_controls":fixed,"holonomy_controls":twisted,
            "uniform_error":"0 <= c*log(q)-log(Z) <= (delta-epsilon)*n^2/6"}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
